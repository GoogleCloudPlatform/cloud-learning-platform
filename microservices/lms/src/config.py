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

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80
PROJECT_ID = os.environ.get("PROJECT_ID") or \
    os.environ.get("GOOGLE_CLOUD_PROJECT")
PUB_SUB_PROJECT_ID=os.getenv("PUB_SUB_PROJECT_ID") or \
  PROJECT_ID
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
BQ_DATASET = DATABASE_PREFIX +  "lms_analytics"
BQ_REGION= os.getenv("BQ_REGION", "US")

BQ_TABLE_DICT = {
    "BQ_COLL_SECTION_TABLE": "section",
    "BQ_COLL_COHORT_TABLE": "cohort",
    "BQ_COLL_COURSETEMPLATE_TABLE": "courseTemplate",
}

ENABLE_UVICORN_LOGS=bool(
  os.getenv("ENABLE_UVICORN_LOGS","false").lower() in ("true",))
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

SERVICES = {
  "user-management": {
    "host": "user-management",
    "port": 80
  }
}

USER_MANAGEMENT_BASE_URL = f"http://{SERVICES['user-management']['host']}:" \
                  f"{SERVICES['user-management']['port']}" \
                  f"/user-management/api/v1"
