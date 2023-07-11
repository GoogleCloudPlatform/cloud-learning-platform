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
  Deletes courses from google classroom  when the github actions
  complete running tests
"""
import os
import json
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
import traceback

PROJECT_ID = os.getenv("PROJECT_ID")
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", None)
DATABASE_PREFIX="e2e_pr1070_"
CLASSROOM_ADMIN_EMAIL=os.environ.get("CLASSROOM_ADMIN_EMAIL")
CLASSROOM_ADMIN_EMAIL="e2e-admin-teacher-3@dhodun.altostrat.com"


# GKE_POD_SA_KEY=json.loads(os.environ.get("GKE_POD_SA_KEY"))
GKE_POD_SA_KEY={
  "type": "service_account",
  "project_id": "core-learning-services-dev",
  "private_key_id": "51a1af5fdad922841de9448af114875002ef58c4",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCyJkFK6JwS/v3n\ngIAjZKJ4bJDN08R5cwuki9tSVse/z5Y05LfYcvb2xPgz+p9YeD2Ivdd9+hZMFssv\ncQKFn9qb8qh9Hro49caLdiS/mEqPbxLUX0p5jHXl/QkJt+QTTEdZP2gwecOQ8fWP\nO+AOP4Z4FJSrUFJkcQaq1rJiUmWfi41vFwXsnaXfNCkWoxQyuX2nAwX6p6EYuzTd\nsv+C5FGJZrW1c+5N8ADx+nCWffr6x9IqfkSTYbId9YnMmfIjCXmwwZxd8DtjNz4v\nYcJNqp63UVr6WD86dK9uAoIHZTuPFTQl13HhuAyTKHOhS8FGbnyKy95bvGmPKmC+\nrVC0RKFZAgMBAAECggEACfcAKveqQe5tIbsQhSpMDjlgZir6GqMCm+B40vkTW5l5\nzkPxkVQTmAe6LHTQifXRLKoVzjBOzqXDFXMYUC96CRlrLvMo49EXmysaG3TMzYt0\nfa2bha4DgEBa9jteMMLRBjR47aaPTQxuZGXV1BDd7YSVMPn2tIiVS2QOqVebje98\nA7WQKWX7PfDxi/k8dp+cf5lRjI2dp4BjMulYve3Vl1DZMVYQRzP3ypdxDFGSkSHu\nK+FWrOf2bl1UbBiYbp2aJTUCXoAKVnqlowlT/s0s64IOc2+xoyQ1eLc7sDphrxNw\n2dp3LOenKpIvvvhzKctLjawP6qHmJWgU+sPmTCu6wwKBgQDZFVJSfQRylhgFW6Pj\nZPI0TrnbszSU3OgmZxO7Etw29V14CtBCCJcAffxvY4mvqIcEDvd1jmnbJMXlGCar\n/okcgNZUiL8m8lGjDGeADGRN/vKG4Egn8Vw+3KczZDow/hpaX/K+7MPdajKQjR1U\nhgqpKGl6kJOQa9p3EqWTXTqqiwKBgQDSFiDv/Bg1AH4qBXSBLlSZTUPKC4smOh9K\nJo3hLCvAsPyNw9Tf6vcYRiQ6pITwr4dCEY0f8KMDreMD8MAxuYNlLFjDcDrJVUdR\nq4dkJn42sbbtUvSzAPHBYfi7QVxTtXWfwVr2BKq2vSKm2/l7M6dplofZfzddqWCr\nVR5Zjcl0KwKBgGwcADlwZUyjjybr8nyGg1ClfE37u03/jeXCI8Ngqyb7nybvS7P3\nDyyBkbvveFxws3zD710uJW2rrJphIrE5PBNj3lmPGJNOznVC8jCE+1cUhrfA7m5l\n9yifPu2LFqfbhEhJzFxlEU4tWy09+cNkVd7Ub2NIqRSdgdkXAjqXjWXtAoGBAL6X\nArSU0GUtGEgJAOO841TcapZemJNKgV5k0awoxVyfc88sjO/DGv2zjGSDInOz2hJP\nF+eVCF5rHxtRCxtRQGnFrJVJOJu0OOpXoZFy9meqG9j7vDC0t54Hwn4m0prCcX5I\nDLxKCZGUzl3wDEn/124L+RyQs+rNoXxt0QXPgqZXAoGAYXpABwQHUNcxnBY47Ebr\n/u1FHrc99kqsohZPHrpsk3kpQKsKleH3vcE+9imyJw61kgfeW7hzjERfR5PnqE0M\nmOr3nD1lUEJR0iUgvZz0S4btXlM//mpM/CSmUEnwb4eTR01YPUoCJT8C/fWR8v+D\n5PvbqXRQpTa6fSbUW9q+xRo=\n-----END PRIVATE KEY-----\n",
  "client_email": "gke-pod-sa@core-learning-services-dev.iam.gserviceaccount.com",
  "client_id": "104636564660654922211",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/gke-pod-sa%40core-learning-services-dev.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
print(CLASSROOM_ADMIN_EMAIL)
print("Admin Email in cleanup")
SCOPES = ["https://www.googleapis.com/auth/classroom.courses",
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file"]
a_creds = service_account.Credentials.from_service_account_info(GKE_POD_SA_KEY,scopes=SCOPES)
creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)

def classroom_delete_drive_folder(classroom_folder,classroom_id):
  service= build("drive", "v2", credentials=creds)
  try:
    drive_file = service.files().get(fileId=classroom_folder).execute()
    file_object = service.files().delete(fileId=classroom_folder).execute()
    print("Delete_drive_folder",drive_file["title"])
    return None
  except HttpError as hte:
    print(f"Error occured: {hte}")
    err = traceback.format_exc().replace("\n", " ")
    print(err)
    return classroom_id

def delete_classroom_courses():
  
  service = build('classroom', 'v1', credentials=creds)
  courses = []
  final_list=[]
  # pylint: disable=maybe-no-member
  response = service.courses().list().execute()
  courses.extend(response.get('courses', []))
  count = 0
  print("Course Names to be deleted",DATABASE_PREFIX,len(DATABASE_PREFIX))
  for course in courses:
    print("Course_name "+course["name"]+" ID ",course["id"])
    if DATABASE_PREFIX in course["name"]:
      if not (count %25):
        print("Wait for delete courses",count)
        time.sleep(60)
      print("Inside IF for delete ")
      final_list.append(course["name"])
      file_id = course["teacherFolder"]["id"]
      classroom_delete_drive_folder(file_id,course["id"])
      course = service.courses().get(id=course["id"]).execute()
      course['courseState'] = 'ARCHIVED'
      course = service.courses().update(id=course["id"], body=course).execute()
      print(f" Updated Course and state  is :  {course.get('name')},{course.get('courseState')}")
      course = service.courses().delete(id=course["id"]).execute()
      print("AFter delete")
      count = count +1
  print("Total classrooms deleted are ",count)
  return final_list

if __name__ == "__main__":
  if DATABASE_PREFIX is None:
    raise Exception("DATABASE_PREFIX is not defined. Classroom cleanup skipped.")
  if not CLASSROOM_ADMIN_EMAIL:
    raise Exception("CLASSROOM_ADMIN_EMAIL is not defined. Classroom cleanup skipped.")
  print("Deleting Courses from classroom")
  result = delete_classroom_courses()
  print(result)
