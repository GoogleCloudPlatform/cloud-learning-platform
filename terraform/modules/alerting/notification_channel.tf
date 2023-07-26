locals {
  emails = var.alert_notify_emails
}

resource "google_monitoring_notification_channel" "notify_email" {
  for_each     = local.emails
  project      = var.project_id
  display_name = each.key
  type         = "email"
  labels = {
    email_address = each.value
  }
  force_delete = true
}
