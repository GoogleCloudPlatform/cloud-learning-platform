# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
  Sample Service config file
"""
import os
from google.cloud import secretmanager
from common.utils.token_handler import UserCredentials
# pylint: disable=line-too-long,broad-except

secrets = secretmanager.SecretManagerServiceClient()

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80
PROJECT_ID = os.environ.get("PROJECT_ID") or \
    os.environ.get("GOOGLE_CLOUD_PROJECT")
PUB_SUB_PROJECT_ID=os.getenv("PUB_SUB_PROJECT_ID") or \
  PROJECT_ID
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
BQ_DATASET = DATABASE_PREFIX + "lms_analytics"

BQ_TABLE_DICT = {
    "BQ_COLL_SECTION_TABLE": "section",
    "BQ_COLL_COHORT_TABLE": "cohort",
    "BQ_COLL_COURSETEMPLATE_TABLE": "courseTemplate",
    "BQ_ANALYTICS_VIEW": "gradeBookEnrichedView",
    "BQ_ENROLLMENT_RECORD" : "sectionEnrollmentRecord",
    "EXISTS_IN_CLASSROOM_NOT_IN_DB_VIEW":"roastersExitsInClassroomNotInDB",
    "EXISTS_IN_DB_NOT_IN_CLASSROOM_VIEW":"roastersExitsInDBNotInClassroom",
    "BQ_NOTIFICATION_TABLE":"lms-notifications"
}

ENABLE_UVICORN_LOGS = bool(
    os.getenv("ENABLE_UVICORN_LOGS", "false").lower() in ("true",))
SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/cloud-platform.read-only",
    "https://www.googleapis.com/auth/devstorage.full_control",
    "https://www.googleapis.com/auth/devstorage.read_only",
    "https://www.googleapis.com/auth/devstorage.read_write"
]

COLLECTION = os.getenv("COLLECTION")

API_BASE_URL = os.getenv("API_BASE_URL")

CLASSROOM_ADMIN_EMAIL = os.getenv("CLASSROOM_ADMIN_EMAIL").lower()

SERVICES = {"user-management": {"host": "user-management", "port": 80}}

USER_MANAGEMENT_BASE_URL = f"http://{SERVICES['user-management']['host']}:" \
                  f"{SERVICES['user-management']['port']}" \
                  f"/user-management/api/v1"

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

auth_client = UserCredentials(LMS_BACKEND_ROBOT_USERNAME,
                              LMS_BACKEND_ROBOT_PASSWORD)
