"""
  Student Learner Profile service config file
"""
# pylint: disable=unspecified-encoding
import os

from schemas.error_schema import (UnauthorizedResponseModel,
                                  InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel)

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80

GCP_PROJECT = os.environ.get("GCP_PROJECT", "")

os.environ["GOOGLE_CLOUD_PROJECT"] = GCP_PROJECT

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")

IS_DEVELOPMENT = bool(os.getenv("IS_DEVELOPMENT", "").lower() \
                      in ("True", "true"))

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
