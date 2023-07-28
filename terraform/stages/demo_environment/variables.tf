variable "project_id" {
  type        = string
  description = "GCP Project ID"

  validation {
    condition     = length(var.project_id) > 0
    error_message = "The project_id value must be an non-empty string."
  }
}

variable "region" {
  type        = string
  description = "Application region"
  default     = "us-central1"
}

variable "bucket_region_or_multiregion" {
  type        = string
  description = "Region or multi-region for buckets"
  default     = "US"
}

variable "gke_cluster_zones" {
  type        = string
  description = "Zones in which to deploy your regional GKE cluster, in comma-separated string format."
  default     = "us-central1-a"
}

variable "firestore_region" {
  type        = string
  description = "Region for firestore. Options: https://cloud.google.com/appengine/docs/locations - us-central1 and europe-west1 must be us-central and europe-west for legacy reasons."
}

variable "github_owner" {
  type        = string
  description = "Your github username (or github org if enterprise deployment)"
  default     = "GPS-Solutions"
}

variable "github_ref" {
  type        = string
  description = "Github ref to use for cloud build triggers"
  default     = "refs/tags/v2.0.0-beta12.7-demo"
}

variable "cert_issuer_email" {
  type        = string
  description = "email of the cert issuer"
}

variable "base_domain" {
  type        = string
  description = "Base domain for your install, such as cloudpssolutions.com"
}

variable "ai_tutor_whitelist_domains" {
  type        = string
  description = "Comma separate domains to be whitelisted in AI Tutor app. For example: google.com,altostrat.com"
}

variable "ai_tutor_whitelist_emails" {
  type        = string
  description = "Comma separate individual emails to be whitelisted in AI Tutor app. For example: user1@google.com,user2@google.com"
}

variable "ckt_whitelist_domains" {
  type        = string
  description = "Comma separate domains to be whitelisted in CKT. For example: google.com,altostrat.com"
}

variable "ckt_whitelist_emails" {
  type        = string
  description = "Comma separate individual emails to be whitelisted in CKT. For example: user1@google.com,user2@google.com"
}

variable "web_app_domain" {
  type        = string
  description = "Subdomain name for frontend of Aitutor application"
  default     = ""
}

variable "ckt_app_domain" {
  type        = string
  description = "Subdomain name for frontend of CKT application"
  default     = ""
}

variable "api_domain" {
  type        = string
  description = "Subdomain name for backend"
  default     = ""
}

variable "existing_custom_vpc" {
  type        = bool
  description = "custom vpc created by the clients/users (for backward compatibility)"
  default     = false
}

variable "firebase_init" {
  type        = bool
  description = "Flag to deploy App Engine for firestore"
  default     = true
}
