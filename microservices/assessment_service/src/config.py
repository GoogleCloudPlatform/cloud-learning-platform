"""
  Assessment Service config file
"""
# pylint: disable=unspecified-encoding,invalid-name
import os
import json
from typing_extensions import Literal
from common.utils.logging_handler import Logger
from common.models import ASSESSMENT_LITERALS
from schemas.error_schema import (UnauthorizedResponseModel,
                                  InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel)
from google.cloud import secretmanager

secrets = secretmanager.SecretManagerServiceClient()

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80
PROJECT_ID = os.environ.get("PROJECT_ID", "core-learning-services-dev")
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
USE_LEARNOSITY_SECRET = bool(os.getenv(
    "USE_LEARNOSITY_SECRET", "").lower() == "true")
print("USE_LEARNOSITY_SECRET: ", os.getenv(
    "USE_LEARNOSITY_SECRET", ""))
CONTENT_SERVING_BUCKET = os.environ.get("CONTENT_SERVING_BUCKET", "")
SIGNURL_SA_KEY_PATH = f"./keys/{PROJECT_ID}-signurl-sa-key.json"

try:
  with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace","r",
            encoding="utf-8",errors="ignore") as \
    ns_file:
    namespace = ns_file.readline()
    JOB_NAMESPACE = namespace
except FileNotFoundError as e:
  JOB_NAMESPACE = "default"
  Logger.info("Namespace File not found, setting job namespace as default")

CONTAINER_NAME = os.getenv("CONTAINER_NAME")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")

API_BASE_URL = os.getenv("API_BASE_URL")

SERVICE_NAME = os.getenv("SERVICE_NAME")

PAYLOAD_FILE_SIZE = 2097152  #2MB
CONTENT_FILE_SIZE = 1024*1024*200 #200MB

ASSESSMENT_SUBMISSION_BASE_PATH = "submissions"
ASSESSMENT_AUTHORING_BASE_PATH = "assessments"

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

PASS_THRESHOLD = 0.8

LEARNOSITY_URL = "https://data.learnosity.com/latest"
if USE_LEARNOSITY_SECRET is True:
  LEARNOSITY_CONSUMER_KEY = secrets.access_secret_version(
    request={
      "name": "projects/" + PROJECT_ID +
        "/secrets/learnosity_consumer_key/versions/latest"
          }).payload.data.decode("utf-8")

  LEARNOSITY_CONSUMER_SECRET = secrets.access_secret_version(
    request={
      "name": "projects/" + PROJECT_ID +
        "/secrets/learnosity_consumer_secret/versions/latest"
          }).payload.data.decode("utf-8")
else:
  LEARNOSITY_CONSUMER_KEY = None
  LEARNOSITY_CONSUMER_SECRET = None

LEARNOSITY_DOMAIN = "demos.learnosity.com"

SERVICES = {
    "user-management": {
        "host": "user-management",
        "port": 80
    },
    "learning-object-service": {
        "host": "learning-object-service",
        "port": 80
    }
}

# User Management BaseUrl
UM_BASE_URL = f"http://{SERVICES['user-management']['host']}:" \
                  f"{SERVICES['user-management']['port']}" \
                  f"/user-management/api/v1"

AUTOGRADED_TAGS = ["AutoGraded"]

with open("testing/valid_themes.json") as json_file:
  json_data = json.load(json_file)
ALLOWED_THEMES = Literal[tuple(json_data)]

ASSESSMENT_TYPES = Literal[tuple(ASSESSMENT_LITERALS["assessments"]["type"])]
ASSESSMENT_ALIASES = Literal[tuple(ASSESSMENT_LITERALS["assessments"]["alias"])]
AUTHORED_ASSESSMENT_TYPES = {
    "static_srl": "SRL",
    "practice": "Formative",
    "project": "Summative"
}

# Temp Folder
TEMP_FOLDER = "temp"
DOWNLOADS_FOLDER = "downloads"
