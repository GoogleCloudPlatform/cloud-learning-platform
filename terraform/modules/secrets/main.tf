locals {
  signurl_id = "signurl"
}

resource "google_secret_manager_secret" "signurl-sa-key" {
  count     = var.enable_service_account_key_creation ? 1 : 0
  secret_id = "${local.signurl_id}-sa-key"
  project   = var.project_id

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret_version" "signurl-sa-key-latest" {
  count  = var.enable_secret_manager_secret_version_creation ? 1 : 0
  secret = one(google_secret_manager_secret.signurl-sa-key[*]).id

  secret_data = base64decode(one(google_service_account_key.signurl[*]).private_key)
}

resource "google_secret_manager_secret" "lti-service-private-key" {
  secret_id = "lti-service-private-key"
  project   = var.project_id

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}


resource "google_secret_manager_secret" "lti-service-public-key" {
  secret_id = "lti-service-public-key"
  project   = var.project_id

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}


resource "google_secret_manager_secret" "google-kg-api-key" {
  secret_id = "google-kg-api-key"
  project   = var.project_id

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret" "learnosity_consumer_key" {
  secret_id = "learnosity_consumer_key"
  project   = var.project_id

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret" "learnosity_consumer_secret" {
  secret_id = "learnosity_consumer_secret"
  project   = var.project_id

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret" "inspace_client_id" {
  secret_id = "inspace_client_id"
  project   = var.project_id

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret" "inspace_client_secret" {
  secret_id = "inspace_client_secret"
  project   = var.project_id

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret" "inspace_auth_group_id" {
  secret_id = "inspace_auth_group_id"
  project   = var.project_id

  replication {
    automatic = true
  }
}

module "service_accounts" {
  source       = "terraform-google-modules/service-accounts/google"
  version      = "~> 4.2"
  project_id   = var.project_id
  names        = [local.signurl_id]
  display_name = local.signurl_id
  description  = "Service account is used for ${local.signurl_id}"
  project_roles = [for i in [
    "roles/storage.admin",
  ] : "${var.project_id}=>${i}"]
  generate_keys = false
}

resource "google_service_account_iam_member" "signurl_sa_token_creator" {
  service_account_id = module.service_accounts.service_accounts_map[local.signurl_id].name
  role               = "roles/iam.serviceAccountTokenCreator"
  member             = module.service_accounts.service_accounts_map[local.signurl_id].member
}

# note this requires the terraform to be run regularly
resource "time_rotating" "signurl_key_rotation" {
  count         = var.enable_signurl_key_rotation ? 1 : 0
  rotation_days = 30
}

resource "google_service_account_key" "signurl" {
  count              = var.enable_service_account_key_creation ? 1 : 0
  service_account_id = module.service_accounts.service_accounts_map[local.signurl_id].email

  keepers = {
    rotation_time = one(time_rotating.signurl_key_rotation[*]).rotation_rfc3339
  }
}

data "google_secret_manager_secret_version" "sign-url-latest" {
  count   = var.enable_service_account_key_creation ? 1 : 0
  secret  = one(google_secret_manager_secret.signurl-sa-key[*]).id
  project = var.project_id
  version = "latest"

  depends_on = [
    google_secret_manager_secret_version.signurl-sa-key-latest
  ]
}


resource "kubernetes_secret" "signurl" {
  count = var.enable_kubernetes_secret_creation ? 1 : 0
  metadata {
    name = "${local.signurl_id}-sa-key"
  }

  data = {
    "${var.project_id}-signurl-sa-key.json" = one(data.google_secret_manager_secret_version.sign-url-latest[*]).secret_data
  }

  type = "kubernetes.io/opaque"
}
