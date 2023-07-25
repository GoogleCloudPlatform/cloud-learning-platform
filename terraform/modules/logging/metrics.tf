# Log based metric
resource "google_logging_metric" "log_based_metric" {
  project  = var.project_id
  for_each = { for metric in var.logging_metric : metric.name => metric }

  name        = each.value.name
  description = each.value.description
  filter      = each.value.filter

  dynamic "metric_descriptor" {
    for_each = each.value.metric_descriptor != null ? [each.value.metric_descriptor] : []
    content {
      unit         = metric_descriptor.value.unit
      value_type   = metric_descriptor.value.value_type
      metric_kind  = metric_descriptor.value.metric_kind
      display_name = metric_descriptor.value.display_name
    }
  }

  disabled = each.value.disabled
}
