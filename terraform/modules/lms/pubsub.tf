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

data "google_project" "project" {
  project_id = var.project_id
}

# This module used to create topic
module "pubsub" {
  source  = "terraform-google-modules/pubsub/google"
  version = "~> 5.0"

  project_id          = var.project_id
  topic               = "classroom-notifications"
  grant_token_creator = false
}

# Subscription created in seperate resource to avoid 'invalid for_each argument' issue
# while creating following pubsub iam bindings
resource "google_pubsub_subscription" "pull_subscriptions" {
  ack_deadline_seconds         = 600
  enable_exactly_once_delivery = false
  enable_message_ordering      = false
  name                         = "classroom-notifications-sub"
  project                      = var.project_id
  topic                        = module.pubsub.id
  retain_acked_messages        = false

  dead_letter_policy {
    dead_letter_topic     = module.dead_letter_topic.id
    max_delivery_attempts = 5
  }
}

# This resource is used to assign gcp-sa-pubsub service agent a subscriber role on main topic subscription
resource "google_pubsub_subscription_iam_member" "pull_subscription_binding" {
  member       = "serviceAccount:service-${data.google_project.project.number}@gcp-sa-pubsub.iam.gserviceaccount.com"
  project      = var.project_id
  role         = "roles/pubsub.subscriber"
  subscription = google_pubsub_subscription.pull_subscriptions.id
}

# This module is used to create and dead_letter topic and bq subscription to it
module "dead_letter_topic" {
  source  = "terraform-google-modules/pubsub/google"
  version = "~> 5.0"

  project_id          = var.project_id
  topic               = "classroom-notifications-dead-letter"
  grant_token_creator = false

  bigquery_subscriptions = [
    {
      name                = "classroom-notifications-dead-letter-bq-sub"
      table               = "${google_bigquery_table.dead_letter.project}:${google_bigquery_table.dead_letter.dataset_id}.${google_bigquery_table.dead_letter.table_id}"
      use_topic_schema    = true
      write_metadata      = true
      drop_unknown_fields = false
    }
  ]
  depends_on = [
    google_bigquery_table.dead_letter
  ]
}

# This resource is used to assign gcp-sa-pubsub service agent a publisher role on dead_letter topic
resource "google_pubsub_topic_iam_member" "dead_letter_publisher_binding" {
  member  = "serviceAccount:service-${data.google_project.project.number}@gcp-sa-pubsub.iam.gserviceaccount.com"
  project = var.project_id
  role    = "roles/pubsub.publisher"
  topic   = module.dead_letter_topic.id
}

resource "google_project_iam_member" "project_pubsub_publisher" {
  project = var.project_id
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:classroom-notifications@system.gserviceaccount.com"
}