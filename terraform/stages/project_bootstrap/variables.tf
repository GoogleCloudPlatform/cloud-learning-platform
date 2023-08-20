variable "project_id" {
  type        = string
  description = "Project ID"
}

variable "region" {
  type        = string
  description = "GCP Region"
}

variable "zone" {
  type        = string
  description = "GCP Zone"
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
  default     = true
  description = "Whether or not to add the Terraform CICD account as project Owner"
}

# custom vpc network variables
variable "vpc_network" {
  type        = string
  description = "Specify the vpc name"
  default     = "vpc-01"
}

variable "vpc_subnetwork" {
  type        = string
  description = "VPC subnetwork which will be used by the cluster"
  default     = "vpc-01-subnet-01"
}

variable "existing_custom_vpc" {
  type        = bool
  description = "custom vpc created by the clients/users(manually) True/False"
  default     = false
}
