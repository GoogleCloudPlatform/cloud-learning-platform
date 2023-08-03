variable "project_id" {
  type        = string
  description = "Project ID"
}

variable "bucket_region_or_multiregion" {
  type        = string
  description = "GCP Region or Multiregion"
  validation {
    condition     = length(var.bucket_region_or_multiregion) > 0
    error_message = "The region value must be an non-empty string."
  }
}

variable "add_project_owner" {
  type        = bool
  default     = false
  description = "Whether or not to add the Terraform CICD account as project Owner"
}
