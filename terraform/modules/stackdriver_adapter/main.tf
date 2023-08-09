
# This will be used as workload identity by custom-metrics-stackdriver-adapter k8s sa
module "service_accounts" {
  source       = "terraform-google-modules/service-accounts/google"
  version      = "~> 3.0"
  project_id   = var.project_id
  names        = ["custom-metrics-sd-adapter-sa"]
  display_name = "custom-metrics-sd-adapter-sa"
  description  = "Service account is used for custom metrics sd adapter(gke)"
  project_roles = [
    for each_role in [
      "roles/monitoring.viewer",
    ] :
    "${var.project_id}=>${each_role}"
  ]
}

# Workload Identity permission
resource "google_service_account_iam_member" "custom_metrics_sd_adapter" {
  service_account_id = module.service_accounts.service_account.id
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[${kubernetes_service_account_v1.default.id}]"
}

resource "kubernetes_namespace_v1" "default" {
  metadata {
    name = "custom-metrics"
  }
}

resource "kubernetes_service_account_v1" "default" {
  metadata {
    name      = "custom-metrics-stackdriver-adapter"
    namespace = kubernetes_namespace_v1.default.metadata.0.name
    annotations = {
      "iam.gke.io/gcp-service-account" = module.service_accounts.email
    }
  }
}

resource "kubernetes_cluster_role_binding_v1" "custom_metrics_system_auth_delegator" {
  metadata {
    name = "custom-metrics:system:auth-delegator"
  }
  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = "system:auth-delegator"
  }
  subject {
    kind      = "ServiceAccount"
    name      = kubernetes_service_account_v1.default.metadata.0.name
    namespace = kubernetes_service_account_v1.default.metadata.0.namespace
  }
}

resource "kubernetes_role_binding_v1" "kube_system_custom_metrics_auth_reader" {
  metadata {
    name      = "custom-metrics-auth-reader"
    namespace = "kube-system"
  }
  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "Role"
    name      = "extension-apiserver-authentication-reader"
  }
  subject {
    kind      = "ServiceAccount"
    name      = kubernetes_service_account_v1.default.metadata.0.name
    namespace = kubernetes_service_account_v1.default.metadata.0.namespace
  }
}

resource "kubernetes_cluster_role_v1" "custom_metrics_resource_reader" {
  metadata {
    name = "custom-metrics-resource-reader"
  }
  rule {
    api_groups = [
      "",
    ]
    resources = [
      "pods",
      "nodes",
      "nodes/stats",
    ]
    verbs = [
      "get",
      "list",
      "watch",
    ]
  }
}

resource "kubernetes_cluster_role_binding_v1" "custom_metrics_resource_reader" {
  metadata {
    name = "custom-metrics-resource-reader"
  }
  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = kubernetes_cluster_role_v1.custom_metrics_resource_reader.metadata.0.name
  }
  subject {
    kind      = "ServiceAccount"
    name      = kubernetes_service_account_v1.default.metadata.0.name
    namespace = kubernetes_service_account_v1.default.metadata.0.namespace
  }
}

resource "kubernetes_deployment_v1" "default" {
  wait_for_rollout = false
  metadata {
    labels = {
      "k8s-app" = "custom-metrics-stackdriver-adapter"
      "run"     = "custom-metrics-stackdriver-adapter"
    }
    name      = "custom-metrics-stackdriver-adapter"
    namespace = kubernetes_namespace_v1.default.metadata.0.name
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        "k8s-app" = "custom-metrics-stackdriver-adapter"
        "run"     = "custom-metrics-stackdriver-adapter"
      }
    }
    template {
      metadata {
        labels = {
          "k8s-app"                       = "custom-metrics-stackdriver-adapter"
          "kubernetes.io/cluster-service" = "true"
          "run"                           = "custom-metrics-stackdriver-adapter"
        }
      }
      spec {
        container {
          command = [
            "/adapter",
            "--use-new-resource-model=true",
            "--fallback-for-container-metrics=true",
          ]
          image             = "gcr.io/gke-release/custom-metrics-stackdriver-adapter:v0.13.1-gke.0"
          image_pull_policy = "Always"
          name              = "pod-custom-metrics-stackdriver-adapter"
          resources {
            limits = {
              cpu    = "250m"
              memory = "200Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "200Mi"
            }
          }
        }
        service_account_name = kubernetes_service_account_v1.default.metadata.0.name
      }
    }
  }
}

resource "kubernetes_service_v1" "custom_metrics_default" {
  metadata {
    labels = {
      "k8s-app"                       = "custom-metrics-stackdriver-adapter"
      "kubernetes.io/cluster-service" = "true"
      "kubernetes.io/name"            = "Adapter"
      "run"                           = "custom-metrics-stackdriver-adapter"
    }
    name      = kubernetes_deployment_v1.default.metadata.0.name
    namespace = kubernetes_deployment_v1.default.metadata.0.namespace
  }
  spec {
    port {
      port        = 443
      protocol    = "TCP"
      target_port = 443
    }
    selector = {
      "k8s-app" = "custom-metrics-stackdriver-adapter"
      "run"     = "custom-metrics-stackdriver-adapter"
    }
    type = "ClusterIP"
  }

}

resource "kubernetes_api_service_v1" "v1beta1_custom_metrics_k8s_io" {
  metadata {
    name = "v1beta1.custom.metrics.k8s.io"
  }
  spec {
    group                    = "custom.metrics.k8s.io"
    group_priority_minimum   = 100
    insecure_skip_tls_verify = true
    service {
      name      = kubernetes_service_v1.custom_metrics_default.metadata.0.name
      namespace = kubernetes_service_v1.custom_metrics_default.metadata.0.namespace
    }
    version          = "v1beta1"
    version_priority = 100
  }
}

resource "kubernetes_api_service_v1" "v1beta2_custom_metrics_k8s_io" {
  metadata {
    name = "v1beta2.custom.metrics.k8s.io"
  }
  spec {
    group                    = "custom.metrics.k8s.io"
    group_priority_minimum   = 100
    insecure_skip_tls_verify = true
    service {
      name      = kubernetes_service_v1.custom_metrics_default.metadata.0.name
      namespace = kubernetes_service_v1.custom_metrics_default.metadata.0.namespace
    }
    version          = "v1beta2"
    version_priority = 200
  }

}

resource "kubernetes_api_service_v1" "v1beta1_external_metrics_k8s_io" {
  metadata {
    name = "v1beta1.external.metrics.k8s.io"
  }
  spec {
    group                    = "external.metrics.k8s.io"
    group_priority_minimum   = 100
    insecure_skip_tls_verify = true
    service {
      name      = kubernetes_service_v1.custom_metrics_default.metadata.0.name
      namespace = kubernetes_service_v1.custom_metrics_default.metadata.0.namespace
    }
    version          = "v1beta1"
    version_priority = 100
  }
}

resource "kubernetes_cluster_role_v1" "external_metrics_reader" {
  metadata {
    name = "external-metrics-reader"
  }
  rule {
    api_groups = [
      "external.metrics.k8s.io",
    ]
    resources = [
      "*",
    ]
    verbs = [
      "list",
      "get",
      "watch",
    ]
  }
}

resource "kubernetes_cluster_role_binding_v1" "external_metrics_reader" {
  metadata {
    name = "external-metrics-reader"
  }
  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = kubernetes_cluster_role_v1.external_metrics_reader.metadata.0.name
  }
  subject {
    kind      = "ServiceAccount"
    name      = "horizontal-pod-autoscaler"
    namespace = "kube-system"
  }
}
