variable "project_id" {
  type        = string
  description = "GCP Project ID"
}

variable "enable_firebase_community_builder_container_creation" {
  type        = bool
  description = "Enable Firebase Community Builder Container Creation"
  default     = true
}
