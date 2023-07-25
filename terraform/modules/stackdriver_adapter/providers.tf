terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "> 4.50.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.7.0"
    }
  }
}
