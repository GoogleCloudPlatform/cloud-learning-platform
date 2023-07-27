
resource "google_bigquery_dataset" "lms_analytics" {
  dataset_id                 = "lms_analytics"
  delete_contents_on_destroy = false
  location                   = var.bigquery_location
  project                    = var.project_id

  access {
    role          = "OWNER"
    special_group = "projectOwners"
  }
  access {
    role          = "READER"
    special_group = "projectReaders"
  }
  access {
    role          = "WRITER"
    special_group = "projectWriters"
  }
}

resource "google_bigquery_table" "dead_letter" {
  dataset_id          = "lms_analytics"
  project             = var.project_id
  table_id            = "dead-letter"
  deletion_protection = true
  schema = jsonencode(
    [
      {
        mode = "NULLABLE"
        name = "subscription_name"
        type = "STRING"
      },
      {
        mode = "NULLABLE"
        name = "message_id"
        type = "STRING"
      },
      {
        mode = "NULLABLE"
        name = "publish_time"
        type = "TIMESTAMP"
      },
      {
        mode = "NULLABLE"
        name = "data"
        type = "JSON"
      },
      {
        mode = "NULLABLE"
        name = "attributes"
        type = "JSON"
      },
    ]
  )
  depends_on = [
    google_bigquery_dataset.lms_analytics
  ]
}
