locals {
  project = var.project_id
}

# main service account to be used by kubernetes pods running the aplpications
module "gke_pod_sa" {
  source       = "terraform-google-modules/service-accounts/google"
  version      = "~> 4.1"
  project_id   = var.project_id
  names        = ["gke-pod-sa"]
  display_name = "gke-pod-sa"
  description  = "Service account is used as the kubernetes service account (ksa)"
  project_roles = [for i in [
    "roles/datastore.owner",
    "roles/cloudtrace.agent",
    "roles/compute.admin",
    "roles/firebase.admin",
    "roles/logging.admin",
    # required for CRUD operation on pub/sub Topic
    "roles/pubsub.admin",
    # required to run queries and create tables
    "roles/bigquery.user",
    "roles/secretmanager.secretAccessor",
    "roles/iam.serviceAccountTokenCreator",
    "roles/storage.admin",
    "roles/aiplatform.admin",
    "roles/iam.workloadIdentityUser",
    "roles/bigquery.dataEditor",
  ] : "${var.project_id}=>${i}"]
  generate_keys = false
}

module "deployment_sa" {
  source       = "terraform-google-modules/service-accounts/google"
  version      = "~> 4.1"
  project_id   = var.project_id
  names        = ["deployment"]
  display_name = "deployment"
  description  = "Service account is used by CI/CD Systems for Deployment"
  project_roles = [for i in [
    # to deploy to firebase
    "roles/firebase.admin",
    # to create cloud Build jobs
    "roles/cloudbuild.builds.editor",
    # needed to stream logs from cloud build
    "roles/viewer",
    # needed to deploy to GKE
    "roles/container.admin",
    # needed to setup KSA, etc
    "roles/iam.securityAdmin",
    # needed to access secrets for GHA jobs
    "roles/secretmanager.secretAccessor",
    # needed to create e2e datasets and tables
    "roles/bigquery.dataOwner",
  ] : "${var.project_id}=>${i}"]
  generate_keys = false
}


# renamed the original SA module to just include gke_pod_sa
moved {
  from = module.service_accounts
  to   = module.gke_pod_sa
}
