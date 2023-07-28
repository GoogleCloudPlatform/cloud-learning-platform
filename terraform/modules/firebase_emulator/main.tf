module "firebase_emulator_sa" {
  source       = "terraform-google-modules/service-accounts/google"
  version      = "~> 4.1"
  project_id   = var.project_id
  names        = ["firebase-emulator"]
  display_name = "firebase-emulator"
  description  = "Service account is used to configure a local firebase emulator for GHA unit tests"
  project_roles = [for i in [
    "roles/firebase.admin",
  ] : "${var.project_id}=>${i}"]
  generate_keys = false
}
