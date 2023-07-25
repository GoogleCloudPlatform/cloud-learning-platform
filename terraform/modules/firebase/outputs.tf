output "firebase_project" {
  value = google_firebase_project.default
}

output "ai_tutor_firebase_api_key" {
  value = data.google_firebase_web_app_config.ai-tutor.api_key
}
