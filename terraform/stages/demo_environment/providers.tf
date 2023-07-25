# Terraform Block
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.65.2"
    }
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = ">= 1.14.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.7.0"
    }
  }

  required_version = ">= 1.3.6"
}

provider "google" {
  project = var.project_id
  region  = var.region
}

data "google_client_config" "default" {}

# Used by module.gke
provider "kubernetes" {
  host                   = "https://${module.learning_platform_backend.gke_endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(module.learning_platform_backend.ca_certificate)
}

# Used by module.ingress
provider "kubectl" {
  host                   = "https://${module.learning_platform_backend.gke_endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(module.learning_platform_backend.ca_certificate)
  load_config_file       = false
}

provider "helm" {
  kubernetes {
    host                   = "https://${module.learning_platform_backend.gke_endpoint}"
    token                  = data.google_client_config.default.access_token
    cluster_ca_certificate = base64decode(module.learning_platform_backend.ca_certificate)
  }
}
