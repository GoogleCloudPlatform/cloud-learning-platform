"""
  Student Learner Profile service config file
"""
# pylint: disable=unspecified-encoding
import os
from schemas.error_schema import (UnauthorizedResponseModel,
                                  InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel)

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80

PROJECT_ID = os.environ.get("PROJECT_ID", "")

os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")

CONTAINER_NAME = os.getenv("CONTAINER_NAME")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")

SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/cloud-platform.read-only",
    "https://www.googleapis.com/auth/devstorage.full_control",
    "https://www.googleapis.com/auth/devstorage.read_only",
    "https://www.googleapis.com/auth/devstorage.read_write"
]

COLLECTION = os.getenv("COLLECTION")

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
