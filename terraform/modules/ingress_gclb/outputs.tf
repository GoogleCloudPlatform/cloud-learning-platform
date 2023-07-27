output "ingress_gclb_ip_address" {
  value = google_compute_global_address.ingress_gclb_ip_address.address
}
