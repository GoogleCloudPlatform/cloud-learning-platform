"""script for loading configuration."""
import os
from typing_extensions import Literal
from schemas.error_schema import (UnauthorizedResponseModel,
                                  InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80
GCP_PROJECT = os.environ.get("PROJECT_ID", "")
os.environ["GOOGLE_CLOUD_PROJECT"] = GCP_PROJECT
GCP_BUCKET = os.environ.get("PROJECT_ID", "core-learning-services-dev")

SCOPES = [
  "https://www.googleapis.com/auth/cloud-platform",
  "https://www.googleapis.com/auth/cloud-platform.read-only",
  "https://www.googleapis.com/auth/devstorage.full_control",
  "https://www.googleapis.com/auth/devstorage.read_only",
  "https://www.googleapis.com/auth/devstorage.read_write"
]

API_BASE_URL = os.getenv("API_BASE_URL")

SERVICE_NAME = os.getenv("SERVICE_NAME")

IS_DEVELOPMENT = bool(os.getenv("IS_DEVELOPMENT", "").lower() in ("", "true"))

IS_CLOUD_LOGGING_ENABLED = bool(os.getenv("IS_CLOUD_LOGGING_ENABLED",
                                          "true").lower() in ("true",))

PAYLOAD_FILE_SIZE = 2097152  # 2MB

ALLOWED_TRANSCRIPT_TYPES = [
  ".pdf", ".csv", ".docx", ".xlsx", ".zip", ".jpeg", ".jpg",
]

ERROR_RESPONSES = {
  500: {
    "model": InternalServerErrorResponseModel
  },
  401: {
    "model": UnauthorizedResponseModel
  },
  404: {
    "model": NotFoundErrorResponseModel
  },
  413: {
    "model": PayloadTooLargeResponseModel
  },
  422: {
    "model": ValidationErrorResponseModel
  }
}

EXPERIENCE_TYPES = Literal["External Course", "Transcripts"]
STUDENT_TYPES = Literal["Undergraduate", "Graduate"]
CLASS_LEVEL = Literal["Lower level", "Mid level", "Upper level"]
STATUS_AP = Literal["Active", "Retired", "Inactive"]
STATUS_PLA_RECORD = Literal["In progress", "Completed"]
RECORD_TYPE = Literal["draft", "saved"]
