<!-- BEGIN_TF_DOCS -->
Copyright 2023 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
## Resources

| Name | Type |
|------|------|
| [google_logging_metric.log_based_metric](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/logging_metric) | resource |
| [google_logging_project_sink.export_logs_to_gcs](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/logging_project_sink) | resource |
| [google_project_iam_audit_config.audit_config](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/project_iam_audit_config) | resource |
| [google_project_iam_binding.log-writer](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/project_iam_binding) | resource |
| [google_storage_bucket.log-bucket](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket) | resource |
## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_create_logging_project_sink"></a> [create\_logging\_project\_sink](#input\_create\_logging\_project\_sink) | Boolean Variable to enable(value = true)/disable(value = false) the creation of logging project sink | `bool` | `false` | no |
| <a name="input_enable_cloud_audit_logging"></a> [enable\_cloud\_audit\_logging](#input\_enable\_cloud\_audit\_logging) | Boolean Variable to enable(value = true)/disable(value = false) the enabling of clopud audit logging | `bool` | `false` | no |
| <a name="input_logging_metric"></a> [logging\_metric](#input\_logging\_metric) | A list of objects, where each object represents a log based metric and its details. | <pre>list(object({<br>    name        = string<br>    description = optional(string)<br>    filter      = string<br>    metric_descriptor = optional(object({<br>      unit         = optional(string)<br>      value_type   = string<br>      metric_kind  = string<br>      display_name = optional(string)<br>    }))<br>    disabled = optional(bool)<br>  }))</pre> | n/a | yes |
| <a name="input_project_id"></a> [project\_id](#input\_project\_id) | GCP project ID | `string` | n/a | yes |
## Outputs

| Name | Description |
|------|-------------|
| <a name="output_log_based_metric_ids"></a> [log\_based\_metric\_ids](#output\_log\_based\_metric\_ids) | List of Log based metrics |

<!-- END_TF_DOCS -->