locals {
  services = [
    "cloudresourcemanager.googleapis.com", # Cloud Resource Manager
    "cloudbilling.googleapis.com",         # Cloud Billing
    "serviceusage.googleapis.com",         # Service Usage
  ]
}


# basic APIs needed to get project up and running
resource "google_project_service" "project-apis" {
  for_each                   = toset(local.services)
  project                    = var.project_id
  service                    = each.value
  disable_dependent_services = true
}

# add timer to avoid errors on new project creation and API enables
resource "time_sleep" "wait_90_seconds" {
  depends_on = [google_project_service.project-apis]

  create_duration = "90s"
}

module "terraform_bootstrap" {
  source                       = "../terraform_bootstrap"
  project_id                   = var.project_id
  bucket_region_or_multiregion = var.bucket_region_or_multiregion
  add_project_owner            = var.add_project_owner

  depends_on = [
    time_sleep.wait_90_seconds
  ]
}
