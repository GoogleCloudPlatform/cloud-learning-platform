"""
  LTI Service config file
"""
# pylint: disable=line-too-long, broad-except
import os
from common.utils.token_handler import Authentication
from schemas.error_schema import (UnauthorizedResponseModel,
                                  InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel)
from google.cloud import secretmanager

secrets = secretmanager.SecretManagerServiceClient()

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80

PROJECT_ID = os.environ.get("PROJECT_ID", "")
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")

API_BASE_URL = os.getenv("API_BASE_URL")

SERVICE_NAME = os.getenv("SERVICE_NAME")

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

TOKEN_TTL = 3600

LTI_ISSUER_DOMAIN = os.getenv("LTI_ISSUER_DOMAIN", "http://localhost")

LTI_PLATFORM_UNIQUE_ID = os.getenv("LTI_PLATFORM_UNIQUE_ID")

LTI_PLATFORM_NAME = os.getenv("LTI_PLATFORM_NAME")

try:
  LTI_SERVICE_PLATFORM_PUBLIC_KEY = secrets.access_secret_version(
      request={
          "name":
              f"projects/{PROJECT_ID}/secrets/lti-service-public-key/versions/latest"
      }).payload.data.decode("utf-8")
except Exception as e:
  LTI_SERVICE_PLATFORM_PUBLIC_KEY = None

try:
  LTI_SERVICE_PLATFORM_PRIVATE_KEY = secrets.access_secret_version(
      request={
          "name":
              f"projects/{PROJECT_ID}/secrets/lti-service-private-key/versions/latest"
      }).payload.data.decode("utf-8")
except Exception as e:
  LTI_SERVICE_PLATFORM_PRIVATE_KEY = None

try:
  LTI_SERVICE_TOOL_PUBLIC_KEY = secrets.access_secret_version(
      request={
          "name":
              f"projects/{PROJECT_ID}/secrets/lti-service-public-key/versions/latest"
      }).payload.data.decode("utf-8")
except Exception as e:
  LTI_SERVICE_TOOL_PUBLIC_KEY = None

try:
  LTI_SERVICE_TOOL_PRIVATE_KEY = secrets.access_secret_version(
      request={
          "name":
              f"projects/{PROJECT_ID}/secrets/lti-service-private-key/versions/latest"
      }).payload.data.decode("utf-8")
except Exception as e:
  LTI_SERVICE_TOOL_PRIVATE_KEY = None

try:
  LMS_BACKEND_ROBOT_USERNAME = secrets.access_secret_version(
      request={
          "name":
              f"projects/{PROJECT_ID}/secrets/lms-backend-robot-username/versions/latest"
      }).payload.data.decode("utf-8")
except Exception as e:
  LMS_BACKEND_ROBOT_USERNAME = None

try:
  LMS_BACKEND_ROBOT_PASSWORD = secrets.access_secret_version(
      request={
          "name":
              f"projects/{PROJECT_ID}/secrets/lms-backend-robot-password/versions/latest"
      }).payload.data.decode("utf-8")
except Exception as e:
  LMS_BACKEND_ROBOT_PASSWORD = None

auth_client = UserCredentialsLMS_BACKEND_ROBOT_USERNAME,
                             LMS_BACKEND_ROBOT_PASSWORD)
