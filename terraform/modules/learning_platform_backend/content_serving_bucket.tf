
resource "google_storage_bucket" "content_serving_bucket" {

  count = var.content_serving_bucket_name != null ? 1 : 0

  name          = var.content_serving_bucket_name
  project       = var.project_id
  location      = "US"
  force_destroy = false
  storage_class = "MULTI_REGIONAL"

  uniform_bucket_level_access = true

  cors {
    origin          = [for web_domain in toset(concat(["https://${local.web_app_domain}"], var.content_serving_bucket_additional_cors_origins)) : web_domain]
    method          = ["GET"]
    response_header = ["Content-Type", "Content-Length", "Content-Range", "Access-Control-Allow-Origin", "X-Requested-With", "X-Goog-Resumable"]
    max_age_seconds = 360
  }
}

resource "google_storage_bucket_iam_binding" "content_serving_bucket" {

  count = (
    var.content_serving_bucket_name != null
  ) ? 1 : 0

  bucket = google_storage_bucket.content_serving_bucket[0].name
  role   = "roles/storage.objectViewer"
  members = [
    "allUsers"
  ]

  depends_on = [
    google_tags_tag_binding.content_serving_bucket
  ]
}

resource "google_tags_tag_binding" "content_serving_bucket" {

  count = (
    var.content_serving_bucket_name != null &&
    var.content_serving_bucket_tag_value != null
  ) ? 1 : 0

  parent    = "//storage.googleapis.com/projects/_/buckets/${google_storage_bucket.content_serving_bucket[0].name}"
  tag_value = var.content_serving_bucket_tag_value
}
