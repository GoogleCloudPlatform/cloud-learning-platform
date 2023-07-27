"""
  Learning Object Service config file
"""
# pylint: disable=unspecified-encoding,invalid-name
import os
import json
from typing_extensions import Literal
from common.utils.logging_handler import Logger
from common.models import LOS_LITERALS, ASSESSMENT_LITERALS
from schemas.error_schema import (UnauthorizedResponseModel,
                                  InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel)

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80
PROJECT_ID = os.environ.get("PROJECT_ID", "")
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")

CONTENT_SERVING_BUCKET = os.environ.get("CONTENT_SERVING_BUCKET", "")
SIGNURL_SA_KEY_PATH = f"./keys/{PROJECT_ID}-signurl-sa-key.json"

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

CP_TYPES = Literal[tuple(LOS_LITERALS["curriculum_pathways"]["type"])]
CP_ALIASES = Literal[tuple(LOS_LITERALS["curriculum_pathways"]["alias"])]
LE_TYPES = Literal[tuple(LOS_LITERALS["learning_experiences"]["type"])]
LE_ALIASES = Literal[tuple(LOS_LITERALS["learning_experiences"]["alias"])]
LO_TYPES = Literal[tuple(LOS_LITERALS["learning_objects"]["type"])]
LO_ALIASES = Literal[tuple(LOS_LITERALS["learning_objects"]["alias"])]
LR_TYPES = Literal[tuple(LOS_LITERALS["learning_resources"]["type"])]
LR_TYPES_LIST = LOS_LITERALS["learning_resources"]["type"]
LR_ALIASES = Literal[tuple(LOS_LITERALS["learning_resources"]["alias"])]
ASSESSMENT_TYPES = Literal[tuple(ASSESSMENT_LITERALS["assessments"]["type"])]
ASSESSMENT_ALIASES = Literal[tuple(ASSESSMENT_LITERALS["assessments"]["alias"])]

ALLOWED_RESOURCE_STATUS = Literal["initial", "draft","published","unpublished"]
MADCAP_PATTERNS_TO_EXCLUDE = ["/Templates/","Search.htm"]
LOS_NODES = ["curriculum_pathways", "learning_experiences",
             "learning_objects", "learning_resources", "assessments"]
SKILL_NODES = ["skills", "competencies"]

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

JOB_TYPES = Literal["validate_and_upload_zip"]
