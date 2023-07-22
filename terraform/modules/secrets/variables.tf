variable "project_id" {
  type        = string
  description = "GCP project ID"
}

variable "region" {
  type        = string
  description = "Secret region"
}

variable "enable_secret_manager_secret_version_creation" {
  type        = bool
  description = "Enable Secret Manager Secret Version Creation"
  default     = true
}

variable "enable_signurl_key_rotation" {
  type        = bool
  description = "Enable SignURL Key Rotation"
  default     = true
}

variable "enable_service_account_key_creation" {
  type        = bool
  description = "Enable Service Account Key Creation"
  default     = true
}

variable "enable_kubernetes_secret_creation" {
  type        = bool
  description = "Enable Kubernetes Secret Creation"
  default     = true
}
