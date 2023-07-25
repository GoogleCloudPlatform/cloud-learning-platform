<!-- BEGIN_TF_DOCS -->
## Resources

| Name | Type |
|------|------|
| [google_monitoring_alert_policy.alerting_policy](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/monitoring_alert_policy) | resource |
| [google_monitoring_notification_channel.notify_email](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/monitoring_notification_channel) | resource |
## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_alert_notify_emails"></a> [alert\_notify\_emails](#input\_alert\_notify\_emails) | Notification Channel Emails | `map(string)` | n/a | yes |
| <a name="input_project_id"></a> [project\_id](#input\_project\_id) | Project ID | `string` | n/a | yes |
## Outputs

| Name | Description |
|------|-------------|
| <a name="output_alert_policies"></a> [alert\_policies](#output\_alert\_policies) | List of Alert Policies |
| <a name="output_notification_emails"></a> [notification\_emails](#output\_notification\_emails) | List of Notification Channel - Emails |

<!-- END_TF_DOCS -->