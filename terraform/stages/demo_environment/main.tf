module "learning_platform_backend" {
  source                       = "../../modules/learning_platform_backend"
  project_id                   = var.project_id
  region                       = var.region
  firestore_region             = var.firestore_region
  bucket_region_or_multiregion = var.bucket_region_or_multiregion
  github_owner                 = var.github_owner
  github_ref                   = var.github_ref
  cert_issuer_email            = var.cert_issuer_email
  base_domain                  = var.base_domain
  ai_tutor_whitelist_domains   = var.ai_tutor_whitelist_domains
  ai_tutor_whitelist_emails    = var.ai_tutor_whitelist_emails
  ckt_whitelist_domains        = var.ckt_whitelist_domains
  ckt_whitelist_emails         = var.ckt_whitelist_emails
  web_app_domain               = coalesce(var.web_app_domain, var.project_id)
  ckt_app_domain               = coalesce(var.ckt_app_domain, "${var.project_id}-ckt")
  api_domain                   = coalesce(var.api_domain, "${var.project_id}-api")
  existing_custom_vpc          = var.existing_custom_vpc
  firebase_init                = var.firebase_init

  # To able to take either comma-separated string or array for gke cluster zones.
  gke_cluster_zones = split(",", var.gke_cluster_zones)

  # Allow Firebase hosting in CORS
  additional_nginx_cors_allow_origin = [
    "${var.project_id}.web.app",
    "${var.project_id}.firebaseapp.com"
  ]
}
