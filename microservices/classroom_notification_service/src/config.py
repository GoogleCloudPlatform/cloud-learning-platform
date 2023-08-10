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

PROJECT_ID = os.environ.get("PROJECT_ID") or \
    os.environ.get("GOOGLE_CLOUD_PROJECT")
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
PUB_SUB_PROJECT_ID = os.getenv("PUB_SUB_PROJECT_ID") or \
    PROJECT_ID

BQ_DATASET = DATABASE_PREFIX +  "lms_analytics"

BQ_TABLE_DICT = {
    "BQ_LOG_CW_TABLE": "courseWorkLogs",
    "BQ_LOG_RS_TABLE": "rosterLogs",
    "BQ_COLL_USER_TABLE": "userCollection",
    "BQ_COLL_CW_TABLE": "courseWorkCollection",
    "BQ_COLL_SCW_TABLE": "submittedCourseWorkCollections"
}

CLASSROOM_ADMIN_EMAIL = os.getenv("CLASSROOM_ADMIN_EMAIL")

