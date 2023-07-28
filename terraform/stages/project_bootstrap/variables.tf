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

variable "billing_account" {
  type        = string
  description = "The billing account ID of your org"
}

variable "org_domain_name" {
  type        = string
  description = "The domain name provided in your org. For argolis use: YOUR_LDAP.altostrat.com"
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

variable "create_new_project" {
  type        = bool
  default     = false
  description = "Whether or not to create a new project"
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
