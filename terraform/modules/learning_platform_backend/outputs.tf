# output "gke_cluster" {
#   value = module.gke.gke_cluster
# }

output "web_app_domain" {
  value = local.web_app_domain
}

output "ckt_app_domain" {
  value = local.ckt_app_domain
}

output "api_domain" {
  value = local.api_domain
}

output "ingress_ip_address" {
  value = module.ingress.ingress_ip_address
}

output "ingress_gclb_ip_address" {
  value = var.lms_enabled ? one(module.ingress_gclb[*]).ingress_gclb_ip_address : null
}

output "api_gclb_domain" {
  value = var.lms_enabled ? local.gclb_api_domain : null
}

output "ai_tutor_firebase_api_key" {
  value = module.firebase.ai_tutor_firebase_api_key
}

output "lms_firebase_web_app_id" {
  value = one(module.lms[*].firebase_web_app_id)
}

output "lms_firebase_web_app_api_key" {
  value = one(module.lms[*].firebase_web_app_api_key)
}

output "gke_cluster" {
  value = module.gke
}

# Adding try() to wrap those dependant variables below as a workaround to
# bypass the cyclic dependencies on cluster creation and providers. This
# approach remove the need to comment providers out first then uncomment later.
# See the usage of these vars in demo_environment/providers.tf.
output "gke_cluster_id" {
  value = try(module.gke.gke_cluster_id, null)
}

output "gke_endpoint" {
  value = try(module.gke.endpoint, null)
}

output "ca_certificate" {
  value = try(module.gke.ca_certificate, null)
}
