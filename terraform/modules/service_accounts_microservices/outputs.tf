output "gke_pod_microservices_sa_emails" {
  description = "Service Account Email for each microservice"
  value       = [for sa in module.gke_pod_microservices_sa_iam_bindings : sa.email]
}
