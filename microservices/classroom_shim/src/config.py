"""
  Classroom Shim Service config file
"""
import os
from schemas.error_schema import (UnauthorizedResponseModel,
                                  InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel)

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80

PROJECT_ID = os.environ.get("PROJECT_ID", "")
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")

API_DOMAIN = f"https://{os.getenv('API_DOMAIN')}"

FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")

FIREBASE_AUTH_DOMAIN = f"{PROJECT_ID}.firebaseapp.com"

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
