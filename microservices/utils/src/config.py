"""Config Module for utils microservice"""
import os

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80
GCP_PROJECT = os.environ.get("GCP_PROJECT", "")
os.environ["GOOGLE_CLOUD_PROJECT"] = GCP_PROJECT
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")

SIGNURL_SA_KEY = "keys/{}-signurl-sa-key.json".format(GCP_PROJECT)

SCOPES = [
  "https://www.googleapis.com/auth/cloud-platform",
  "https://www.googleapis.com/auth/cloud-platform.read-only",
  "https://www.googleapis.com/auth/devstorage.full_control",
  "https://www.googleapis.com/auth/devstorage.read_only",
  "https://www.googleapis.com/auth/devstorage.read_write"
]

API_BASE_URL = os.getenv("API_BASE_URL")

SERVICE_NAME = os.getenv("SERVICE_NAME")

FEEDBACK_COLLECTION = os.getenv("FEEDBACK_COLLECTION")
if FEEDBACK_COLLECTION:
  FEEDBACK_COLLECTION = DATABASE_PREFIX + FEEDBACK_COLLECTION

GET_HELP_COLLECTION = os.getenv("GET_HELP_COLLECTION")
if GET_HELP_COLLECTION:
  GET_HELP_COLLECTION = DATABASE_PREFIX + GET_HELP_COLLECTION

GET_TOPICS_COLLECTION = os.getenv("GET_TOPICS_COLLECTION")
if GET_TOPICS_COLLECTION:
  GET_TOPICS_COLLECTION = DATABASE_PREFIX + GET_TOPICS_COLLECTION

USER_COLLECTION = os.getenv("USER_COLLECTION")
if USER_COLLECTION:
  USER_COLLECTION = DATABASE_PREFIX + USER_COLLECTION

USER_SUBCOLLECTION = os.getenv("USER_SUBCOLLECTION")
if USER_SUBCOLLECTION:
  USER_SUBCOLLECTION = DATABASE_PREFIX + USER_SUBCOLLECTION

INLINE_FEEDBACK_COLLECTION = os.getenv("INLINE_FEEDBACK_COLLECTION")
if INLINE_FEEDBACK_COLLECTION:
  INLINE_FEEDBACK_COLLECTION = DATABASE_PREFIX + INLINE_FEEDBACK_COLLECTION

GCP_LEARNING_RESOURCE_BUCKET = os.getenv("GCP_LEARNING_RESOURCE_BUCKET")

IS_DEVELOPMENT = bool(os.getenv("IS_DEVELOPMENT", "").lower() \
    in ("True", "true"))

SERVICES = {
  "authentication": {
    "host": "authentication",
    "port": 80
  },
  "utils": {
    "host": "notes",
    "port": 80
  },
  "dashboard": {
    "host": "dashboard",
    "port": 80
  }
}
