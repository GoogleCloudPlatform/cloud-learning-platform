/**
 * Copyright 2023 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

# By applying this Terraform configuration, we will
# - create a bucket to store logs in 
# - create a log sink that exports all logs to the specified GCS bucket.
# - Because our sink uses a unique_writer, we grant that writer access to the bucket.


resource "google_storage_bucket" "log-bucket" {
  name                        = "${var.project_id}-log-sink-bucket"
  project                     = var.project_id
  location                    = "US"
  force_destroy               = false
  storage_class               = "MULTI_REGIONAL"
  uniform_bucket_level_access = true
}

resource "google_logging_project_sink" "export_logs_to_gcs" {

  name                   = "export-logs-to-gcs"
  destination            = "storage.googleapis.com/${google_storage_bucket.log-bucket.name}"
  filter                 = ""
  unique_writer_identity = true

  depends_on = [google_storage_bucket.log-bucket]
}

resource "google_project_iam_binding" "log-writer" {

  project = var.project_id
  role    = "roles/storage.objectCreator"
  members = [
    google_logging_project_sink.export_logs_to_gcs.writer_identity,
  ]

  depends_on = [google_logging_project_sink.export_logs_to_gcs]
}
