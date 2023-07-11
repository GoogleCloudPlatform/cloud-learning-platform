"""
  User Management config file
"""
import os
from schemas.error_schema import (UnauthorizedResponseModel,
                                  InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel)

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80
PROJECT_ID = os.environ.get("PROJECT_ID", "")
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")

SCOPES = [
  "https://www.googleapis.com/auth/cloud-platform",
  "https://www.googleapis.com/auth/cloud-platform.read-only",
  "https://www.googleapis.com/auth/devstorage.full_control",
  "https://www.googleapis.com/auth/devstorage.read_only",
  "https://www.googleapis.com/auth/devstorage.read_write"
]

COLLECTION = os.getenv("COLLECTION")

if COLLECTION:
  COLLECTION = DATABASE_PREFIX + COLLECTION

API_BASE_URL = os.getenv("API_BASE_URL")

SERVICE_NAME = os.getenv("SERVICE_NAME")

PAYLOAD_FILE_SIZE = 2097152 #2MB

ERROR_RESPONSES = {
  500: {
    "model": InternalServerErrorResponseModel
  },
  401: {
    "model": UnauthorizedResponseModel
  },
  422: {
    "model": ValidationErrorResponseModel
  }
}

SERVICES = {
  "student_learner_profile": {
    "host": "student-learner-profile",
    "port": 80
  },
  "learning_record_service": {
    "host": "learning-record-service",
    "port": 80
  }

}

SLP_BASE_URL = f"http://{SERVICES['student_learner_profile']['host']}:" \
               f"{SERVICES['student_learner_profile']['port']}" \
               f"/learner-profile-service/api/v1"

LRS_BASE_URL = f"http://{SERVICES['learning_record_service']['host']}:" \
               f"{SERVICES['learning_record_service']['port']}" \
               f"/learning-record-service/api/v1"

IMMUTABLE_USER_GROUPS = ["learner", "assessor", "instructor", "coach", "admin",
                         "lxe", "curriculum_designer"]

IMMUTABLE_ASSOCIATION_GROUPS = ["Levelup Discipline association group",
                                "Levelup Learner association group"]
