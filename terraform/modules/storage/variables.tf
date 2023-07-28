variable "project_id" {
  type        = string
  description = "GCP project ID"
}

variable "region" {
  type        = string
  description = "Bucket region or multiregion"
}

variable "web_app_domain" {
  type        = string
  description = "web app domain name"
}
