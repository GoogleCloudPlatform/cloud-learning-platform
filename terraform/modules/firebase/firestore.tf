resource "google_app_engine_application" "app" {
  count         = var.firebase_init ? 1 : 0
  project       = var.project_id
  location_id   = var.firestore_region
  database_type = "CLOUD_FIRESTORE"
}
