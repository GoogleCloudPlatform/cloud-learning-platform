output "firebase_web_app_id" {
  description = "Firebase Application ID"
  value       = "google_firebase_web_app.lms-admin.app_id"
}

output "firebase_web_app_api_key" {
  description = "Firebase API Key"
  value       = data.google_firebase_web_app_config.lms-admin.api_key
}
