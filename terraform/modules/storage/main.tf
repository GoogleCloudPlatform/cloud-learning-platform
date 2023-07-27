resource "google_storage_bucket" "main-assets" {
  name          = var.project_id
  project       = var.project_id
  location      = var.region
  force_destroy = false

  uniform_bucket_level_access = true

  cors {
    origin          = ["https://${var.web_app_domain}"]
    method          = ["GET"]
    response_header = ["Content-Type", "Content-Length", "Content-Range", "Access-Control-Allow-Origin", "X-Requested-With", "X-Goog-Resumable"]
    max_age_seconds = 360
  }
}
