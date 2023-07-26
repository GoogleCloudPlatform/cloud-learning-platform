resource "google_secret_manager_secret" "lms_service_user" {
  secret_id = "lms-service-user"
  project   = var.project_id

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret" "lms_backend_robot_username" {
  secret_id = "lms-backend-robot-username"
  project   = var.project_id

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}


resource "google_secret_manager_secret" "lms_backend_robot_password" {
  secret_id = "lms-backend-robot-password"
  project   = var.project_id

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret" "lms_admin_teacher_username" {
  secret_id = "lms-admin-teacher-username"
  project   = var.project_id

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}


resource "google_secret_manager_secret" "lms_admin_teacher_password" {
  secret_id = "lms-admin-teacher-password"
  project   = var.project_id

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret" "lms_admin_teacher_access_token" {
  secret_id = "lms-admin-teacher-access-token"
  project   = var.project_id

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret" "gke_pod_sa_key" {
  secret_id = "gke-pod-sa-key"
  project   = var.project_id

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}
