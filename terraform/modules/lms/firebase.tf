resource "google_firebase_web_app" "lms-admin" {
  provider     = google-beta
  project      = var.firebase_project
  display_name = "${var.project_id}-lms-admin"
}

# to be used to reference outputs from the above
data "google_firebase_web_app_config" "lms-admin" {
  provider   = google-beta
  web_app_id = google_firebase_web_app.lms-admin.app_id
  project    = var.firebase_project
}
