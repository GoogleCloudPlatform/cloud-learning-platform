"""
  Authentication service config file
"""
import os
from schemas.error_schema import (UnauthorizedUserErrorResponseModel,
                                  InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel)

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80

GCP_PROJECT = os.environ.get("GCP_PROJECT", "")
os.environ["GOOGLE_CLOUD_PROJECT"] = GCP_PROJECT

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")

API_BASE_URL = os.getenv("API_BASE_URL")

SERVICE_NAME = os.getenv("SERVICE_NAME")

REDIS_HOST = os.getenv("REDIS_HOST")

FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")

IDP_URL = "https://identitytoolkit.googleapis.com/v1/accounts"

IS_DEVELOPMENT = bool(os.getenv("IS_DEVELOPMENT", "").lower() in ("True",
                                                                  "true"))

AUTHENTICATION_VERSION = os.getenv("AUTHENTICATION_VERSION", "v1")

ERROR_RESPONSES = {
  500: {
    "model": InternalServerErrorResponseModel
  },
  401: {
    "model": UnauthorizedUserErrorResponseModel
  },
  422: {
    "model": ValidationErrorResponseModel
  }
}
