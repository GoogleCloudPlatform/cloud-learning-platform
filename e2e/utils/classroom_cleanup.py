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
CLASSROOM_ADMIN_EMAIL=os.environ.get("CLASSROOM_ADMIN_EMAIL")
GKE_POD_SA_KEY=json.loads(os.environ.get("GKE_POD_SA_KEY"))
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
