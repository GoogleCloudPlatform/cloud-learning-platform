locals {
  # roles for TF CICD bootstrap SA
  project_roles = [
    "roles/appengine.appAdmin",              # Read/Write/Modify access to all application configuration and settings (firebase)
    "roles/appengine.appCreator",            # Ability to create the App Engine resource for the project (firebase)
    "roles/cloudbuild.builds.editor",        # create Cloud Build trigger
    "roles/compute.networkAdmin",            # create VPC, NAT router, etc
    "roles/compute.securityAdmin",           # set compute security policies
    "roles/container.admin",                 # project k8s admin
    "roles/firebase.admin",                  # to enable firebase
    "roles/iam.securityAdmin",               # set IAM policies
    "roles/iam.serviceAccountAdmin",         # create and administer service accounts
    "roles/iam.serviceAccountKeyAdmin",      # create SA key
    "roles/iam.serviceAccountUser",          # so can create resources that run as SA (i.e. gke clusters)
    "roles/logging.admin",                   # access to logging
    "roles/monitoring.admin",                # dashboards
    "roles/pubsub.admin",                    # pubsub
    "roles/resourcemanager.projectIamAdmin", # to create firebase project
    "roles/secretmanager.admin",             # create secrets
    "roles/serviceusage.serviceUsageAdmin",  # to create firebase project?
    "roles/storage.admin",                   # access to GCS and TF bucket
  ]
}

module "service_account" {
  source        = "terraform-google-modules/service-accounts/google"
  version       = "~> 4.1"
  project_id    = var.project_id
  names         = ["terraform-cicd"]
  display_name  = "terraform-cicd"
  description   = "Terraform Service Account"
  project_roles = [for i in local.project_roles : "${var.project_id}=>${i}"]
  generate_keys = false
}

# project/Owner (or custom role) needed to create Firebase app
resource "google_project_iam_member" "project" {
  count   = var.add_project_owner ? 1 : 0
  project = var.project_id
  role    = "roles/owner"
  member  = "serviceAccount:${module.service_account.email}"
}

resource "google_storage_bucket" "tfstate-bucket" {
  name                        = "${var.project_id}-tfstate"
  location                    = var.bucket_region_or_multiregion
  project                     = var.project_id
  force_destroy               = false
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }
}
