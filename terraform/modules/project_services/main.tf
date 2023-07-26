# Service account used to run Terraform has permission to manage project APIs roles/serviceusage.serviceUsageAdmin
locals {
  services = [
    "anthosconfigmanagement.googleapis.com", # Anthos Config Management API
    "appengine.googleapis.com",              # App Engine API
    "artifactregistry.googleapis.com",       # Artifact Registry
    "cloudbuild.googleapis.com",             # Cloud Build
    "cloudresourcemanager.googleapis.com",   # Cloud Resource manager
    "compute.googleapis.com",                # Load Balancers, Cloud Armor
    "container.googleapis.com",              # Google Kubernetes Engine
    "containerregistry.googleapis.com",      # Google Container Registry
    "firebase.googleapis.com",               # Firebase
    "firebaseextensions.googleapis.com",     # Firebase Extension API
    "firebasehosting.googleapis.com",        # Firebase Hosting
    "firestore.googleapis.com",              # Firestore
    "gkehub.googleapis.com",                 # GKE HUB API
    "iam.googleapis.com",                    # Cloud IAM
    "language.googleapis.com",               # Natural Language API
    "secretmanager.googleapis.com",          # Secret Manager
    "servicenetworking.googleapis.com",      # Service Networking API
    "storage.googleapis.com",                # Cloud Storage
    "oslogin.googleapis.com",                # OS Login API
  ]
}

resource "google_project_service" "project-apis" {
  for_each                   = toset(local.services)
  project                    = var.project_id
  service                    = each.value
  disable_dependent_services = false
  disable_on_destroy         = false
}
