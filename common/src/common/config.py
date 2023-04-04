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
Config module to setup common environment
"""


import os

PROJECT_ID = os.environ.get("PROJECT_ID", "")

PROJECT_ID = os.environ.get("PROJECT_ID") or \
    os.environ.get("GOOGLE_CLOUD_PROJECT")
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
PUB_SUB_PROJECT_ID=os.getenv("PUB_SUB_PROJECT_ID") or \
  PROJECT_ID

API_BASE_URL = os.getenv("API_BASE_URL")
CLOUD_LOGGING_ENABLED=bool(
  os.getenv("CLOUD_LOGGING_ENABLED","true").lower() in ("true",))

BQ_REGION= os.getenv("BQ_REGION", "US")

SERVICES = {
  "user-management": {
    "host": "user-management",
    "port": 80
  }
}

USER_MANAGEMENT_BASE_URL = f"http://{SERVICES['user-management']['host']}:" \
                  f"{SERVICES['user-management']['port']}" \
                  f"/user-management/api/v1"
CLASSROOM_ADMIN_EMAIL = os.getenv("CLASSROOM_ADMIN_EMAIL")
