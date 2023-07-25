variable "project_id" {
  type        = string
  description = "project ID"
}

variable "region" {
  type        = string
  description = "cluster region"
}

variable "firebase_project" {
  type        = string
  description = "firebase project"
}

variable "bigquery_location" {
  type        = string
  description = "Bigquery location ID"
  default     = "US"
}
