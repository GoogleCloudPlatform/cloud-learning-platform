output "gke_cluster" {
  value = module.gke
}

# Adding try() to wrap those dependant variables below as a workaround to
# bypass the cyclic dependencies on cluster creation and providers. This
# approach removes the need to comment providers out first then uncomment later.
output "gke_cluster_id" {
  value = try(module.gke.cluster_id, null)
}

output "endpoint" {
  value = try(module.gke.endpoint, null)
}

output "ca_certificate" {
  value = try(module.gke.ca_certificate, null)
}
