locals {
  project = var.project_id
  project_roles = [
    "roles/monitoring.viewer",
    "roles/monitoring.metricWriter",
    "roles/logging.logWriter",
    "roles/stackdriver.resourceMetadata.writer",
    "roles/storage.objectViewer",
    "roles/iam.serviceAccountUser",
    "roles/artifactregistry.reader",
  ]

  default_node_pool = {
    name                             = "gke-np-cpu-01"
    machine_type                     = "n1-standard-16"
    location_policy                  = "ANY"
    min_count                        = "1"
    max_count                        = "6"
    disk_size_gb                     = "1000"
    disk_type                        = "pd-standard"
    image_type                       = "COS_CONTAINERD"
    node_pools_create_before_destroy = var.node_pools_create_before_destroy
    auto_repair                      = true
    auto_upgrade                     = true
    # hard coding until resolved: https://github.com/terraform-google-modules/terraform-google-kubernetes-engine/issues/991
    service_account                  = "gke-node-sa@${var.project_id}.iam.gserviceaccount.com"
    preemptible                      = false
    max_pods_per_node                = var.max_pods_per_node
    initial_node_count               = "1"
  }

  node_pools = [
    local.default_node_pool,
    var.gpu_np_max_count > 0 ? merge(
      local.default_node_pool,
      {
        name               = "gke-np-gpu-01"
        machine_type       = "n1-highmem-8"
        max_count          = var.gpu_np_max_count
        disk_size_gb       = "500"
        accelerator_count  = 1
        accelerator_type   = "nvidia-tesla-t4"
      }
    ) : {},
  ]

}

module "service_accounts" {
  source        = "terraform-google-modules/service-accounts/google"
  version       = "~> 4.1"
  project_id    = var.project_id
  names         = ["gke-node-sa"]
  display_name  = "gke-np-sa"
  description   = "Service account is used in the gke node pool"
  project_roles = [for i in local.project_roles : "${var.project_id}=>${i}"]
}


module "gke" {
  source                               = "terraform-google-modules/kubernetes-engine/google//modules/beta-private-cluster-update-variant"
  version                              = "23.3.0"
  project_id                           = var.project_id
  name                                 = format("%s-%s", var.project_id, var.region)
  release_channel                      = var.release_channel
  region                               = var.region
  regional                             = true
  zones                                = var.gke_cluster_zones
  network                              = var.network
  subnetwork                           = var.subnetwork
  ip_range_pods                        = var.ip_range_pods
  ip_range_services                    = var.ip_range_services
  network_project_id                   = var.network_project_id
  http_load_balancing                  = true
  identity_namespace                   = "enabled"
  horizontal_pod_autoscaling           = true
  network_policy                       = var.datapath_provider == "ADVANCED_DATAPATH" ? false : true
  enable_private_endpoint              = false
  enable_private_nodes                 = true
  master_ipv4_cidr_block               = "172.26.1.16/28"
  master_authorized_networks           = var.master_authorized_networks
  create_service_account               = false
  remove_default_node_pool             = true
  datapath_provider                    = var.datapath_provider
  enable_vertical_pod_autoscaling      = var.enable_vertical_pod_autoscaling
  enable_shielded_nodes                = var.enable_shielded_nodes
  add_master_webhook_firewall_rules    = true
  monitoring_enable_managed_prometheus = var.monitoring_enable_managed_prometheus
  monitoring_enabled_components        = var.monitoring_enabled_components
  # gce_persistent_disk_csi_driver_config is enabled using gce_pd_csi_driver (caveat)
  # https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/container_cluster#gcp_filestore_csi_driver_config
  gce_pd_csi_driver                    = true
  enable_intranode_visibility          = true

  node_pools = local.node_pools

  node_pools_oauth_scopes = {

    gke-np-cpu-01 = [
      "https://www.googleapis.com/auth/cloud-platform",
    ],
    gke-np-gpu-01 = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }


  node_pools_metadata = {
    gke-np-cpu-01 = {
      disable-legacy-endpoints = "true",
      node-pool-name           = "gke-np-cpu-01"
    },
    gke-np-gpu-01 = {
      disable-legacy-endpoints = "true",
      node-pool-name           = "gke-np-gpu-01"
    }
  }


  node_pools_taints = {
    gke-np-cpu-01 = [],
    gke-np-gpu-01 = [
      {
        key    = "key"
        value  = "gpu"
        effect = "NO_SCHEDULE"
      },
      {
        key    = "nvidia.com/gpu"
        value  = "present"
        effect = "NO_SCHEDULE"
      },
    ]
  }

  depends_on = [
    module.service_accounts,
  ]

}


# Creating a Kubernetes Service account for Workload Identity
resource "kubernetes_service_account" "ksa" {
  metadata {
    name = "ksa"
    annotations = {
      "iam.gke.io/gcp-service-account" = var.gke_pod_sa_email
    }
  }
  depends_on = [
    module.gke
  ]
}

# Enable the IAM binding between YOUR-GSA-NAME and YOUR-KSA-NAME:
resource "google_service_account_iam_member" "gsa-ksa-binding" {
  service_account_id = "projects/${var.project_id}/serviceAccounts/${var.gke_pod_sa_email}"
  role               = "roles/iam.workloadIdentityUser"

  member = "serviceAccount:${var.project_id}.svc.id.goog[default/ksa]"

  depends_on = [
    module.gke
  ]
}


# taken from https://raw.githubusercontent.com/GoogleCloudPlatform/container-engine-accelerators/master/nvidia-driver-installer/cos/daemonset-preloaded.yaml
resource "kubectl_manifest" "nvidia_driver_installer" {
  yaml_body = <<YAML
# Copyright 2017 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# The Dockerfile and other source for this daemonset are in
# https://cos.googlesource.com/cos/tools/+/refs/heads/master/src/cmd/cos_gpu_installer/
#
# This is the same as ../../daemonset.yaml except that it assumes that the
# docker image is present on the node instead of downloading from GCR. This
# allows easier upgrades because GKE can preload the correct image on the
# node and the daemonset can just use that image.

apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: nvidia-driver-installer
  namespace: kube-system
  labels:
    k8s-app: nvidia-driver-installer
spec:
  selector:
    matchLabels:
      k8s-app: nvidia-driver-installer
  updateStrategy:
    type: RollingUpdate
  template:
    metadata:
      labels:
        name: nvidia-driver-installer
        k8s-app: nvidia-driver-installer
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: cloud.google.com/gke-accelerator
                operator: Exists
      tolerations:
      - operator: "Exists"
      hostNetwork: true
      hostPID: true
      volumes:
      - name: dev
        hostPath:
          path: /dev
      - name: vulkan-icd-mount
        hostPath:
          path: /home/kubernetes/bin/nvidia/vulkan/icd.d
      - name: nvidia-install-dir-host
        hostPath:
          path: /home/kubernetes/bin/nvidia
      - name: root-mount
        hostPath:
          path: /
      - name: cos-tools
        hostPath:
          path: /var/lib/cos-tools
      initContainers:
      - image: "cos-nvidia-installer:fixed"
        imagePullPolicy: Never
        name: nvidia-driver-installer
        resources:
          requests:
            cpu: "0.15"
        securityContext:
          privileged: true
        env:
          - name: NVIDIA_INSTALL_DIR_HOST
            value: /home/kubernetes/bin/nvidia
          - name: NVIDIA_INSTALL_DIR_CONTAINER
            value: /usr/local/nvidia
          - name: VULKAN_ICD_DIR_HOST
            value: /home/kubernetes/bin/nvidia/vulkan/icd.d
          - name: VULKAN_ICD_DIR_CONTAINER
            value: /etc/vulkan/icd.d
          - name: ROOT_MOUNT_DIR
            value: /root
          - name: COS_TOOLS_DIR_HOST
            value: /var/lib/cos-tools
          - name: COS_TOOLS_DIR_CONTAINER
            value: /build/cos-tools
        volumeMounts:
        - name: nvidia-install-dir-host
          mountPath: /usr/local/nvidia
        - name: vulkan-icd-mount
          mountPath: /etc/vulkan/icd.d
        - name: dev
          mountPath: /dev
        - name: root-mount
          mountPath: /root
        - name: cos-tools
          mountPath: /build/cos-tools
      containers:
      - image: "gcr.io/google-containers/pause:2.0"
        name: pause
YAML

  depends_on = [
    module.gke
  ]
}
