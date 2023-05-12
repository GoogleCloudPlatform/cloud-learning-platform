"""
  Learning Object Service config file
"""
# pylint: disable=unspecified-encoding
import os
import json
from typing_extensions import Literal
from common.utils.logging_handler import Logger
from common.models import LOS_LITERALS, ASSESSMENT_LITERALS
from schemas.error_schema import (UnauthorizedResponseModel,
                                  InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel)

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80
GCP_PROJECT = os.environ.get("GCP_PROJECT", "")
os.environ["GOOGLE_CLOUD_PROJECT"] = GCP_PROJECT
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")

CONTENT_SERVING_BUCKET = os.environ.get("CONTENT_SERVING_BUCKET", "")
SIGNURL_SA_KEY_PATH = "./keys/{}-signurl-sa-key.json".format(GCP_PROJECT)

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

PAYLOAD_FILE_SIZE = 2097152 #2MB
CONTENT_FILE_SIZE = 1024*1024*200 #200MB

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

RESOURCE_BASE_PATH = "learning-resources"
FAQ_BASE_PATH = "faq-resources"

# Batch Job types
VALIDATE_AND_UPLOAD_ZIP = "validate_and_upload_zip"
ZIP_EXTRACTION_FOLDER = "zip_extraction_folder"

with open("testing/valid_themes.json") as json_file:
  json_data = json.load(json_file)
ALLOWED_THEMES = Literal[tuple(json_data + [""])]

CP_TYPES = Literal[tuple(LOS_LITERALS["CP_TYPES"])]
CP_ALIASES = Literal[tuple(LOS_LITERALS["CP_ALIASES"])]
LE_TYPES = Literal[tuple(LOS_LITERALS["LE_TYPES"])]
LE_ALIASES = Literal[tuple(LOS_LITERALS["LE_ALIASES"])]
LO_TYPES = Literal[tuple(LOS_LITERALS["LO_TYPES"])]
LO_ALIASES = Literal[tuple(LOS_LITERALS["LO_ALIASES"])]
LR_TYPES = Literal[tuple(LOS_LITERALS["LR_TYPES"])]
LR_TYPES_LIST = LOS_LITERALS["LR_TYPES"]
LR_ALIASES = Literal[tuple(LOS_LITERALS["LR_ALIASES"])]
ASSESSMENT_TYPES = Literal[tuple(ASSESSMENT_LITERALS["AS_TYPES"])]
ASSESSMENT_ALIASES = Literal[tuple(ASSESSMENT_LITERALS["AS_ALIASES"])]
ALL_ALIASES = LOS_LITERALS["CP_ALIASES"] + \
              LOS_LITERALS["LE_ALIASES"] + \
              LOS_LITERALS["LO_ALIASES"] + \
              LOS_LITERALS["LR_ALIASES"] + \
              ASSESSMENT_LITERALS["AS_ALIASES"]
ALLOWED_RESOURCE_STATUS = Literal["initial", "draft","published","unpublished"]
MADCAP_PATTERNS_TO_EXCLUDE = ["/Templates/","Search.htm"]

SERVICES = {
    "user-management": {
        "host": "user-management",
        "port": 80
    },
    "assessment-service": {
        "host": "assessment-service",
        "port": 80
    }
}

UM_BASE_URL = f"http://{SERVICES['user-management']['host']}:" \
               f"{SERVICES['user-management']['port']}" \
               f"/user-management/api/v1"
# pylint: disable = line-too-long
ASSESSMENT_SERVICE_BASE_URL = f"http://{SERVICES['assessment-service']['host']}:" \
               f"{SERVICES['assessment-service']['port']}" \
               f"/assessment-service/api/v1"
