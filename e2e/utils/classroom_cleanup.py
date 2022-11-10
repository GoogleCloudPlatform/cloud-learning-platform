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
  Deletes datasets from firestore and bigquery when the github actions
  complete running tests
"""
import os
import firebase_admin
import json
from firebase_admin import credentials, firestore
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials

PROJECT_ID = os.getenv("PROJECT_ID")
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", None)

# Initializing Firebase client.
firebase_admin.initialize_app(credentials.ApplicationDefault(), {
    "projectId": PROJECT_ID,
})


def delete_classroom_courses():
  GKE_POD_SA_KEY=json.loads(os.environ.get("GKE_POD_SA_KEY"))
  CLASSROOM_ADMIN_EMAIL=os.environ.get("CLASSROOM_ADMIN_EMAIL")
  SCOPES = ["https://www.googleapis.com/auth/classroom.courses",
    "https://www.googleapis.com/auth/classroom.courses.readonly",""]
  a_creds = service_account.Credentials.from_service_account_info(GKE_POD_SA_KEY,scopes=SCOPES)
  creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
  service = build('classroom', 'v1', credentials=creds)
  courses = []
  final_list=[]
    # pylint: disable=maybe-no-member
  response = service.courses().list().execute()
  courses.extend(response.get('courses', []))
  for course in courses:
    print("Course_name"+course["name"]+" ID ",course["id"])
    if "e2e_pr50_" in course["name"]:
      final_list.append(course)
      course = service.courses().delete(id=course["id"]).execute()
  return final_list

if __name__ == "__main__":
  if DATABASE_PREFIX is None:
    raise Exception("DATABASE_PREFIX is not defined. Database cleanup skipped.")
  print("Deleting Courses from classroom")
  print(delete_classroom_courses())
