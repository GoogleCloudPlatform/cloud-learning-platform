"""
  matching engine service config file
"""
import os
from schemas.error_schema import (UnauthorizedResponseModel,
                                  InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel,
                                  NotFoundErrorResponseModel)

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80
GCP_PROJECT = os.environ.get("GCP_PROJECT","")
os.environ["GOOGLE_CLOUD_PROJECT"] = GCP_PROJECT
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
NETWORK_NAME = os.environ.get("NETWORK_NAME","")
NETWORK_TYPE=os.environ.get("NETWORK_TYPE","normal")
REGION = os.environ.get("REGION","")
PROJECT_ID = GCP_PROJECT
DEFAULT_MACHINE_TYPE = os.environ.get("DEFAULT_MACHINE_TYPE","e2-standard-2")
DEFAULT_MIN_REPLICA = 1
DEFAULT_MAX_REPLICA = 1
ENDPOINT = f"{REGION}-aiplatform.googleapis.com"
PROJECT_NUMBER = os.environ.get("PROJECT_NUMBER","")
PARENT = f"projects/{PROJECT_ID}/locations/{REGION}"
VPC_NETWORK_NAME = f"projects/{PROJECT_NUMBER}/global/networks/{NETWORK_NAME}"
HOST_PROJECT_NUMBER = os.getenv("HOST_PROJECT_NUMBER")
if NETWORK_TYPE=="shared" and HOST_PROJECT_NUMBER:
  VPC_NETWORK_NAME = \
      f"projects/{HOST_PROJECT_NUMBER}/global/networks/{NETWORK_NAME}"
SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/cloud-platform.read-only",
    "https://www.googleapis.com/auth/devstorage.full_control",
    "https://www.googleapis.com/auth/devstorage.read_only",
    "https://www.googleapis.com/auth/devstorage.read_write"
]

COLLECTION = os.getenv("COLLECTION")

API_BASE_URL = os.getenv("API_BASE_URL","api/v1")

SERVICE_NAME = os.getenv("SERVICE_NAME","matching-engine")

IS_CLOUD_LOGGING_ENABLED = bool(os.getenv
            ("IS_CLOUD_LOGGING_ENABLED", "true").lower() in ("true",))

ERROR_RESPONSES = {
    500: {
        "model": InternalServerErrorResponseModel
    },
    401: {
        "model": UnauthorizedResponseModel
    },
    422: {
        "model": ValidationErrorResponseModel
    },
    404: {
          "model": NotFoundErrorResponseModel
        }
}
