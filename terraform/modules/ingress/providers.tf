terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "> 4.50.0"
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
}

data "google_client_config" "default" {
}

