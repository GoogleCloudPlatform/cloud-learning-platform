"""config file """
import os
from common.utils.logging_handler import Logger
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel,
                                  NotFoundErrorResponseModel)
PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80
GCP_PROJECT = os.environ.get("GCP_PROJECT", "gcp-classroom-dev")
os.environ["GOOGLE_CLOUD_PROJECT"] = GCP_PROJECT


SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/cloud-platform.read-only",
    "https://www.googleapis.com/auth/devstorage.full_control",
    "https://www.googleapis.com/auth/devstorage.read_only",
    "https://www.googleapis.com/auth/devstorage.read_write",
]
try:
  with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace","r",\
    encoding="utf-8", errors="ignore") as ns_file:
    namespace = ns_file.readline()
    JOB_NAMESPACE = namespace
except FileNotFoundError as e:
  JOB_NAMESPACE = "default"
  Logger.info("Namespace File not found, setting job namespace as default")

API_BASE_URL = os.getenv("API_BASE_URL")
SERVICE_NAME = os.getenv("SERVICE_NAME")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
MODEL_WEIGHTS_PATH = os.getenv(
  "MODEL_WEIGHTS_PATH","gs://gcp-classroom-dev/ml-models/dkt")
GCS_BUCKET = os.environ.get("GCP_PROJECT", "gcp-classroom-dev")
MODEL_PARAMS_DIR = "model_params"
IS_DEVELOPMENT = bool(os.getenv("IS_DEVELOPMENT", "").lower() \
    in ("True", "true"))
DKT_JOB_TYPE = "deep-knowledge-tracing"

SERVICES = {}

BATCH_JOB_LIMITS = {
      "cpu": "3",
      "memory": "7000Mi"
    }
BATCH_JOB_REQUESTS = {
      "cpu": "3",
      "memory": "7000Mi"
    }

#more file types can be added as we scale upto JSONs
ALLOWED_FILE_TYPES = [".csv"]

#TODO: REQUIRED FIELDS needs to be udpated as per new Data model udpates
# parent node  needs to be renamed to user_id
#issue refernece: 3485

REQUIRED_FIELDS = {
  "learning_item_id": str,
  "activity_type": str,
  "user_id": str,
  "learning_unit": str,
  "course_id": str,
  "is_correct": [1,0],
  "session_id": str
}

GCP_BUCKET = os.environ.get("GCP_PROJECT", "gcp-classroom-dev")

ERROR_RESPONSES = {
    500: {
        "model": InternalServerErrorResponseModel
    },
    404: {
        "model": NotFoundErrorResponseModel
    },
    422: {
        "model": ValidationErrorResponseModel
    }
}
