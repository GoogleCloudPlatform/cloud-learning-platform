locals {
  sa_iam_bindings = { for obj in var.gke_pod_microservices_sa_iam_bindings : obj.sa_name => flatten(concat(
  obj.use_common_roles == true ? tolist(var.gke_pod_microservices_common_roles) : [], obj.additional_roles)) }
}

module "gke_pod_microservices_sa_iam_bindings" {
  source        = "terraform-google-modules/service-accounts/google"
  version       = "~> 4.1"
  project_id    = var.project_id
  for_each      = local.sa_iam_bindings
  names         = [each.key]
  display_name  = each.key
  description   = "Service account is used as the kubernetes service account (ksa) for ${each.key} microservice"
  project_roles = [for i in each.value : "${var.project_id}=>${i}"]
  generate_keys = false
}
