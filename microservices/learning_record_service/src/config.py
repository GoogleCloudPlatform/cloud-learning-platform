"""
  Learning Record Service config file
"""
# pylint: disable=unspecified-encoding
import os
from common.utils.logging_handler import Logger
from schemas.error_schema import (UnauthorizedResponseModel,
                                  InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel)

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80
PROJECT_ID = os.environ.get("PROJECT_ID", "")
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")

try:
  with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r",
            encoding="utf-8", errors="ignore") as \
    ns_file:
    namespace = ns_file.readline()
    JOB_NAMESPACE = namespace
except FileNotFoundError as e:
  JOB_NAMESPACE = "default"
  Logger.info("Namespace File not found, setting job namespace as default")

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

BQ_LRS_DATASET = DATABASE_PREFIX + os.getenv("BQ_LRS_DATASET", "lrs")

BQ_LRS_TABLE = os.getenv("BQ_LRS_TABLE", "statements")

PAYLOAD_FILE_SIZE = 2097152  #2MB

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

VALID_OBJECTS_TYPE = [
    "learning_experiences", "curriculum_pathways", "learning_objects",
    "learning_resources", "assessment_items"
]

COMPLETED_RULE_VERBS = ["completed", "submitted", "evaluated"]

STARTED_RULE_VERBS = ["started"]

RESUMED_RULE_VERBS = ["resumed"]

VALID_VERBS = STARTED_RULE_VERBS + COMPLETED_RULE_VERBS\
   + RESUMED_RULE_VERBS

SERVICES = {
    "student-learner-profile": {
        "host": "student-learner-profile",
        "port": 80
    }
}
