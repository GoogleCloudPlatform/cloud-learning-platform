resource "null_resource" "firebase_community_builder_container" {
  count = var.enable_firebase_community_builder_container_creation ? 1 : 0

  provisioner "local-exec" {
    command = "${path.module}/build_firebase_container.sh"

    environment = {
      PROJECT_ID = var.project_id
    }
  }
}
