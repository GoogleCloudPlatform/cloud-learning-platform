variable "cert_issuer_email" {
  type        = string
  description = "email of the cert issuer"
}

variable "api_domain" {
  type        = string
  description = "api domain name"
}

variable "web_app_domain" {
  type        = string
  description = "web app domain name"
}

variable "ckt_app_domain" {
  type        = string
  description = "ckt app domain name"
}

variable "enable_certman_gcr_io_images" {
  type        = bool
  description = "Enabling this to use cert-manager images from the gcr.io/google-marketplace repository instead of quay.io."
}

variable "additional_nginx_cors_allow_origin" {
  type        = list(string)
  description = "Additional CORS origin filters required for nginx ingress module"
  default     = []
}

variable "create_nginx_ingress" {
  type        = bool
  description = "Create NGINX Ingress"
  default     = true
}
