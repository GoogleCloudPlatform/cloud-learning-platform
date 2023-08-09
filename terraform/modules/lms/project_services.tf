locals {
  services = [
    "drive.googleapis.com",     # Google Drive
    "forms.googleapis.com",     # Google Forms
    "classroom.googleapis.com", # Google Classroom
  ]
}

resource "google_project_service" "project-apis" {
  for_each                   = toset(local.services)
  project                    = var.project_id
  service                    = each.value
  disable_dependent_services = false
  disable_on_destroy         = false
}
