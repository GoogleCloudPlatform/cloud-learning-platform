output "alert_policies" {
  description = "List of Alert Policies"
  value       = [for policy in google_monitoring_alert_policy.alerting_policy : policy.id]
}

output "notification_emails" {
  description = "List of Notification Channel - Emails"
  value       = [for email in google_monitoring_notification_channel.notify_email : email.id]
}
