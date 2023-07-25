output "web_app_domain" {
  value = module.learning_platform_backend.web_app_domain
}

output "ckt_app_domain" {
  value = module.learning_platform_backend.ckt_app_domain
}

output "api_domain" {
  value = module.learning_platform_backend.api_domain
}

output "ingress_ip_address" {
  value = module.learning_platform_backend.ingress_ip_address
}

output "gclb_ingress_ip_address" {
  value = module.learning_platform_backend.ingress_gclb_ip_address
}

output "api_gclb_domain" {
  value = module.learning_platform_backend.api_gclb_domain
}

output "ai_tutor_firebase_api_key" {
  value = module.learning_platform_backend.ai_tutor_firebase_api_key
}
