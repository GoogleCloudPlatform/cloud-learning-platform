variable "project_id" {
  type        = string
  description = "Project ID"
}

variable "alert_notify_emails" {
  type        = map(string)
  description = "Notification Channel Emails"
}

variable "document_path" {
  type = string
  description = "Alert Policy YAML document"
}
