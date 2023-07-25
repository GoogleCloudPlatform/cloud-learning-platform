output "log_based_metric_ids" {
  description = "List of Log based metrics"
  value       = [for metric in google_logging_metric.log_based_metric : metric.id]
}
