"""
    Dashboard env config
"""
import os

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80
PROJECT_ID = os.environ.get("PROJECT_ID", "")
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")

SCOPES = [
  "https://www.googleapis.com/auth/cloud-platform",
  "https://www.googleapis.com/auth/cloud-platform.read-only",
  "https://www.googleapis.com/auth/devstorage.full_control",
  "https://www.googleapis.com/auth/devstorage.read_only",
  "https://www.googleapis.com/auth/devstorage.read_write"
]

API_BASE_URL = os.getenv("API_BASE_URL")

SERVICE_NAME = os.getenv("SERVICE_NAME")

REDIS_HOST = os.getenv("REDIS_HOST")

COURSE_CONTEXT_COLLECTION = os.getenv("COURSE_CONTEXT_COLLECTION")
if COURSE_CONTEXT_COLLECTION:
  COURSE_CONTEXT_COLLECTION = DATABASE_PREFIX + COURSE_CONTEXT_COLLECTION

COLLECTION = os.getenv("COLLECTION")
if COLLECTION:
  COLLECTION = DATABASE_PREFIX + COLLECTION

IS_DEVELOPMENT = bool(os.getenv("IS_DEVELOPMENT", "").lower() \
    in ("True", "true"))

ACTIVITY_ID = "teachme"

SERVICES = {
  "authentication": {
    "host": "authentication",
    "port": 80
  },
  "dashboard": {
    "host": "dashboard",
    "port": 80
  },
  "utils": {
    "host": "utils",
    "port": 80
  },
  "course_ingestion": {
    "host": "course-ingestion",
    "port": 80
  },
  "notes": {
    "host": "notes",
    "port": 80
  }
}

LEVEL_MAPPING = {
  "Course": "level0",
  "Program": "level0",
  "Competency": "level1",
  "http://purl.imsglobal.org/vocab/lis/v2/course#CourseOffering": "level1",
  "Units": "level1",
  "SubCompetency": "level2",
  "Modules": "level2"
}
