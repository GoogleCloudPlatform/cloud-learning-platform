locals {
  github_owner    = var.github_owner
  github_repo     = "ailearning-frontend"
  github_url      = "https://github.com/${local.github_owner}/${local.github_repo}"
  ai_tutor_domain = var.project_id
  ckt_domain      = "${var.project_id}-ckt"
}

resource "google_firebase_project" "default" {
  provider = google-beta
  project  = var.project_id
}

# TODO: need google_firebase_project_location?

resource "google_firebase_web_app" "ai-tutor" {
  provider     = google-beta
  project      = google_firebase_project.default.project
  display_name = var.project_id
}

data "google_firebase_web_app_config" "ai-tutor" {
  provider   = google-beta
  web_app_id = google_firebase_web_app.ai-tutor.app_id
  project    = var.project_id
}

resource "google_firebase_web_app" "ckt" {
  provider     = google-beta
  project      = google_firebase_project.default.project
  display_name = "${var.project_id}-ckt"
}

data "google_firebase_web_app_config" "ckt" {
  provider   = google-beta
  web_app_id = google_firebase_web_app.ckt.app_id
  project    = var.project_id
}

resource "google_cloudbuild_trigger" "ai-tutor" {
  name    = "ai-tutor-firebase-app-trigger"
  project = var.project_id

  source_to_build {
    uri       = local.github_url
    ref       = var.github_ref
    repo_type = "GITHUB"
  }

  git_file_source {
    path      = "aitutor/cloudbuild.yaml"
    uri       = local.github_url
    revision  = var.github_ref
    repo_type = "GITHUB"
  }

  substitutions = {
    _API_ENDPOINT      = var.api_domain
    _API_KEY           = data.google_firebase_web_app_config.ai-tutor.api_key
    _APP_ID            = google_firebase_web_app.ai-tutor.app_id
    _MEASUREMENT_ID    = "$MEASUREMENT_ID"
    _MESSAGING_ID      = data.google_firebase_web_app_config.ai-tutor.messaging_sender_id
    _PROJECT_ID        = var.project_id
    _AUTH_DOMAIN       = data.google_firebase_web_app_config.ai-tutor.auth_domain
    _DOMAIN            = local.ai_tutor_domain
    _WHITELIST_DOMAINS = var.ai_tutor_whitelist_domains
    _WHITELIST_EMAILS  = var.ai_tutor_whitelist_emails
  }
}

resource "google_cloudbuild_trigger" "ckt" {
  name    = "ckt-firebase-app-trigger"
  project = var.project_id

  source_to_build {
    uri       = local.github_url
    ref       = var.github_ref
    repo_type = "GITHUB"
  }

  git_file_source {
    path      = "tagging_tool/cloudbuild.yaml"
    uri       = local.github_url
    revision  = var.github_ref
    repo_type = "GITHUB"
  }

  substitutions = {
    _API_ENDPOINT        = var.api_domain
    _API_KEY             = data.google_firebase_web_app_config.ai-tutor.api_key
    _APP_ID              = google_firebase_web_app.ai-tutor.app_id
    _MEASUREMENT_ID      = "$MEASUREMENT_ID"
    _MESSAGING_ID        = data.google_firebase_web_app_config.ai-tutor.messaging_sender_id
    _PROJECT_ID          = var.project_id
    _AUTH_DOMAIN         = data.google_firebase_web_app_config.ai-tutor.auth_domain
    _DOMAIN              = local.ckt_domain
    _WHITELIST_DOMAINS   = var.ckt_whitelist_domains
    _WHITELIST_EMAILS    = var.ckt_whitelist_emails
    _OKTA_LOGIN_REQ      = var.ckt_okta_login
    _PP_ASSESSMENTS_REQ  = var.ckt_pp_assessments
    _CKN_ASSESSMENTS_REQ = var.ckt_ckn_assessments
  }
}


# so Cloud Build can run deploy jobs
data "google_project" "project" {
  project_id = var.project_id
}

resource "google_project_iam_member" "cloud-build-firebase-admin" {
  project = var.project_id
  role    = "roles/firebase.admin"
  member  = "serviceAccount:${data.google_project.project.number}@cloudbuild.gserviceaccount.com"
}
