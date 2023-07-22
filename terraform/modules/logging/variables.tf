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

variable "project_id" {
  type        = string
  description = "GCP project ID"
}

variable "logging_metric" {
  type = list(object({
    name        = string
    description = optional(string)
    filter      = string
    metric_descriptor = optional(object({
      unit         = optional(string)
      value_type   = string
      metric_kind  = string
      display_name = optional(string)
    }))
    disabled = optional(bool)
  }))
  description = "A list of objects, where each object represents a log based metric and its details."
}
