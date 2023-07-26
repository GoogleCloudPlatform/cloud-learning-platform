variable "project_id" {
  type        = string
  description = "project ID"
}


variable "gke_pod_microservices_common_roles" {
  description = "Common roles utilized by each microservice's service account"
  default     = []
}

variable "gke_pod_microservices_sa_iam_bindings" {
  description = " A list of objects, where each object represents a microservice's service account and its associated IAM bindings."
  type = list(object({
    sa_name          = string
    use_common_roles = bool
    additional_roles = list(string)
  }))
  default = []
}
