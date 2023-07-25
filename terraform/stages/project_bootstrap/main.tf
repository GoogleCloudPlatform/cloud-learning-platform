terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.65.2"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

locals {
  services = [
    "anthosconfigmanagement.googleapis.com", # Anthos Config Management API
    "appengine.googleapis.com",              # App Engine API
    "artifactregistry.googleapis.com",       # Artifact Registry
    "bigquery.googleapis.com",               # BigQuery
    "bigquerydatatransfer.googleapis.com",   # BigQuery Data Transfer
    "cloudbuild.googleapis.com",             # Cloud Build
    "cloudresourcemanager.googleapis.com",   # Cloud Resource manager
    "compute.googleapis.com",                # Load Balancers, Cloud Armor
    "container.googleapis.com",              # Google Kubernetes Engine
    "containerregistry.googleapis.com",      # Google Container Registry
    "dataflow.googleapis.com",               # Cloud Dataflow
    "dns.googleapis.com",                    # Cloud DNS
    "firebase.googleapis.com",               # Firebase
    "firebaseextensions.googleapis.com",     # Firebase Extension API
    "firebasehosting.googleapis.com",        # Firebase Hosting
    "firestore.googleapis.com",              # Firestore
    "gkehub.googleapis.com",                 # GKE HUB API
    "iam.googleapis.com",                    # Cloud IAM
    "iap.googleapis.com",                    # Cloud IAP
    "kgsearch.googleapis.com",               # Knowledge Graph Search API
    "language.googleapis.com",               # Natural Language API
    "logging.googleapis.com",                # Cloud Logging
    "monitoring.googleapis.com",             # Cloud Operations Suite
    "run.googleapis.com",                    # Cloud Run
    "secretmanager.googleapis.com",          # Secret Manager
    "servicenetworking.googleapis.com",      # Service Networking API
    "serviceusage.googleapis.com",           # Service Usage
    "storage.googleapis.com",                # Cloud Storage
  ]

  org_policies_disabled = [
    "iam.disableServiceAccountKeyCreation", # SA key export needed to run further Terraform
    "compute.requireShieldedVm",            # required for GKE
    "compute.requireOsLogin",               # required for GKE
  ]
}

data "google_organization" "org" {
  domain = var.org_domain_name
}

resource "google_project" "create_new_project" {
  count           = var.create_new_project ? 1 : 0
  name            = var.project_id
  project_id      = var.project_id
  org_id          = data.google_organization.org.org_id
  billing_account = var.billing_account
}

# basic APIs needed to get project up and running
resource "google_project_service" "project-apis" {
  depends_on                 = [google_project.create_new_project]
  for_each                   = toset(local.services)
  project                    = var.project_id
  service                    = each.value
  disable_dependent_services = true
}

resource "google_project_organization_policy" "enable_service_account_keys" {
  depends_on = [google_project.create_new_project]
  for_each   = toset(local.org_policies_disabled)
  constraint = each.value
  project    = var.project_id

  boolean_policy {
    enforced = false
  }
}

# need external IPs for serving
resource "google_project_organization_policy" "enable_external_ip" {
  depends_on = [google_project.create_new_project]
  constraint = "compute.vmExternalIpAccess"
  project    = var.project_id

  list_policy {
    allow {
      all = true
    }
  }
}

# Add google.com accounts
resource "google_project_organization_policy" "allow_member_domains" {
  depends_on = [google_project.create_new_project]
  constraint = "iam.allowedPolicyMemberDomains"
  project    = var.project_id

  list_policy {
    allow {
      all = true
    }
  }
}

# add timer to avoid errors on new project creation and API enables
resource "time_sleep" "wait_60_seconds" {
  depends_on      = [google_project_service.project-apis]
  create_duration = "60s"
}

module "vpc_network" {
  depends_on  = [time_sleep.wait_60_seconds]
  source      = "../../modules/networking"
  count       = var.existing_custom_vpc ? 0 : 1
  vpc_network = var.vpc_network
  project_id  = var.project_id
  region      = var.region
}

module "terraform_bootstrap" {
  depends_on                   = [time_sleep.wait_60_seconds]
  source                       = "../../modules/terraform_bootstrap"
  project_id                   = var.project_id
  bucket_region_or_multiregion = var.bucket_region_or_multiregion
  add_project_owner            = var.add_project_owner
}

module "bastion_host" {
  depends_on                = [module.vpc_network]
  source                    = "../../modules/bastion"
  project_id                = var.project_id
  zone                      = var.zone
  vpc_network_self_link     = module.vpc_network[0].network_self_link
  vpc_subnetworks_self_link = module.vpc_network[0].subnets_self_link[0]
}
