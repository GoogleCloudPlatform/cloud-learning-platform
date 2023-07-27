variable "project_id" {
  type        = string
  description = "specify the project name"
  default     = "aitutor-dev"
}

variable "gke_cluster_name" {
  type        = string
  description = "specify the GKE cluster name"
  default     = "v3-cluster"
}

variable "gke_cluster_location" {
  type        = string
  description = "specify the GKE cluster location"
  default     = "us-east4-b"
}

variable "gke_namespace" {
  type        = string
  description = "specify the GKE namespace"
  default     = "default"
}
