variable "project_id" {
  type        = string
  description = "project ID"
}

variable "region" {
  type        = string
  description = "cluster region"
}

variable "gke_cluster_zones" {
  type        = list(string)
  description = "specify the zones for the cluster region"
}

variable "gke_pod_sa_email" {
  type        = string
  description = "the email of the main pod SA"
}

variable "master_authorized_networks" {
  type        = list(object({ cidr_block = string, display_name = string }))
  description = "List of master authorized networks. If none are provided, disallow external access (except the cluster node IPs, which GKE automatically whitelists)."
}

variable "network" {
  type        = string
  description = "VPC network to host the gke cluster"
  default     = "vpc-01"
}

variable "subnetwork" {
  type        = string
  description = "VPC subnetwork which will be used by the cluster"
  default     = "vpc-01-subnet-01"
}

variable "ip_range_pods" {
  type        = string
  description = "The name of the secondary subnet ip range to use for pods"
  default     = "secondary-pod-range-01"
}

variable "ip_range_services" {
  type        = string
  description = "The name of the secondary subnet range to use for services"
  default     = "secondary-service-range-01"
}

variable "network_project_id" {
  type        = string
  description = "The project ID of the shared VPC's host (for shared vpc support)"
}

variable "gpu_np_max_count" {
  type        = string
  description = "Node pool max count for auto scaling (0 to disable GPU nodes)"
}

variable "max_pods_per_node" {
  type        = string
  description = "Maximum pods to be assigned to the nodes"
}

variable "datapath_provider" {
  type        = string
  description = "The desired datapath provider for this cluster. By default, DATAPATH_PROVIDER_UNSPECIFIED enables the IPTables-based kube-proxy implementation. ADVANCED_DATAPATH enables Dataplane-V2 feature."
}

variable "enable_vertical_pod_autoscaling" {
  type        = bool
  description = "Vertical Pod Autoscaling automatically adjusts the resources of pods controlled by it"
}

variable "release_channel" {
  type        = string
  description = "The release channel of this cluster. Accepted values are UNSPECIFIED, RAPID, REGULAR and STABLE. Defaults to UNSPECIFIED."
}

variable "enable_shielded_nodes" {
  type        = bool
  description = "Enable Shielded Nodes features on all nodes in this cluster"
}

variable "node_pools_create_before_destroy" {
  type        = bool
  description = "TODO: copy paste from upstream module"
  default     = true
}

variable "monitoring_enable_managed_prometheus" {
  type        = bool
  description = "Configuration for Managed Service for Prometheus. Whether or not the managed collection is enabled."
  default     = false
}

variable "monitoring_enabled_components" {
  type        = list(string)
  description = "List of services to monitor: SYSTEM_COMPONENTS, WORKLOADS (provider version >= 3.89.0). Empty list is default GKE configuration."
  default     = []
}
