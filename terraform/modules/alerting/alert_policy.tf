locals {
  file_components = split(".", var.document_path)
  file_ext        = local.file_components[length(local.file_components) - 1]
  decoded_yaml    = contains(["yml", "yaml"], local.file_ext) ? yamldecode(file(var.document_path)) : null
}

resource "google_monitoring_alert_policy" "alerting_policy" {
  for_each = { for policy in local.decoded_yaml : policy.displayName => policy }

  display_name = each.value["displayName"]
  combiner     = each.value["combiner"]

  dynamic "conditions" {
    for_each = each.value["conditions"]
    content {
      display_name = conditions.value["displayName"]

      condition_threshold {
        dynamic "aggregations" {
          for_each = conditions.value["conditionThreshold"]["aggregations"]
          content {
            alignment_period     = aggregations.value["alignmentPeriod"]
            cross_series_reducer = aggregations.value["crossSeriesReducer"]
            per_series_aligner   = aggregations.value["perSeriesAligner"]
          }
        }
        comparison = conditions.value["conditionThreshold"]["comparison"]
        duration   = conditions.value["conditionThreshold"]["duration"]
        filter     = conditions.value["conditionThreshold"]["filter"]
        trigger {
          count = conditions.value["conditionThreshold"]["trigger"]["count"]
        }
      }
    }
  }
  notification_channels = values(google_monitoring_notification_channel.notify_email)[*].id
  documentation {
    content = each.value["documentation"]["content"]
  }
  enabled = each.value["enabled"]
}
