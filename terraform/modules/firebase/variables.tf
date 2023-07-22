variable "project_id" {
  type        = string
  description = "GCP Project ID"
  default     = "aitutor-dev"

  validation {
    condition     = length(var.project_id) > 0
    error_message = "The project_id value must be an non-empty string."
  }
}

variable "firestore_region" {
  type        = string
  description = "Firestore Region - must be app_engine region"
  # options for firestore: https://cloud.google.com/appengine/docs/locations
  # us-central1 and europe-west1 must be us-central and europe-west for legacy reasons
}

variable "github_owner" {
  type        = string
  description = "Your github username (or github org if enterprise deployment)"
}

variable "github_ref" {
  type        = string
  description = "Github ref to use for cloud build triggers"
  default     = "refs/tags/v2.0.0-beta12.7-demo"
}

variable "api_domain" {
  type        = string
  description = "Domain for the backend APIs"
}

variable "ai_tutor_whitelist_domains" {
  type        = string
  description = "Comma separated list of email domains that should have access to AI Tutor"
}

variable "ai_tutor_whitelist_emails" {
  type        = string
  description = "Comma separated list of individual emails that should have access to AI Tutor"
}

variable "ckt_whitelist_domains" {
  type        = string
  description = "Comma separated list of email domains that should have access to CKT"
}

variable "ckt_whitelist_emails" {
  type        = string
  description = "Comma separated list of individual emails that should have access to CKT"
}

variable "ckt_okta_login" {
  type        = bool
  description = "Support OKTA login in CKT"
  default 	  = false
}

variable "ckt_pp_assessments" {
  type        = bool
  description = "Enable Paraphrase assessments in CKT"
  default 	  = true
}

variable "ckt_ckn_assessments" {
  type        = bool
  description = "Enable Create Knowledge Notes assessments in CKT"
  default 	  = true
}

variable "firebase_init" {
  type        = bool
  description = "Whether to initialize Firebase/Firestore."
  default     = false
}
