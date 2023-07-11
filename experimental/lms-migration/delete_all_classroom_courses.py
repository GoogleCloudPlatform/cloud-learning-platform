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
  Deletes courses from google classroom  
"""
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
import traceback
import json

PROJECT_ID = os.getenv("PROJECT_ID")
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", None)
GKE_POD_SA_KEY=json.loads(os.environ.get("GKE_POD_SA_KEY"))
CLASSROOM_ADMIN_EMAIL=os.environ.get("CLASSROOM_ADMIN_EMAIL")
SCOPES = ["https://www.googleapis.com/auth/classroom.courses",
  "https://www.googleapis.com/auth/classroom.courses.readonly",
  "https://www.googleapis.com/auth/drive",
  "https://www.googleapis.com/auth/drive.file"
  ]
a_creds = service_account.Credentials.from_service_account_info(GKE_POD_SA_KEY,scopes=SCOPES)
creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)

def delete_classroom_courses():
  SCOPES = ["https://www.googleapis.com/auth/classroom.courses",
    "https://www.googleapis.com/auth/classroom.courses.readonly"]
  a_creds = service_account.Credentials.from_service_account_info(GKE_POD_SA_KEY,scopes=SCOPES)
  creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
  service = build('classroom', 'v1', credentials=creds)
  courses = []
  final_list=[]
  next_page_token=None
  while(True):
    response = service.courses().list(pageToken=next_page_token).execute()
    courses.extend(response.get('courses', []))
    next_page_token= response.get('nextPageToken', None)
    if not next_page_token:
      break
    else:
      print("In continue list")
  count = 0
  save_classroom_ids = []
  for course in courses:
    if course["id"] not in save_classroom_ids:
      count+=1
      print("For deletion Course_name "+course["name"]+" ID ",course["id"])
      final_list.append(course["name"])
      file_id = course["teacherFolder"]["id"]
      classroom_delete_drive_folder(file_id,course["id"])
      course = service.courses().get(id=course["id"]).execute()
      course['courseState'] = 'ARCHIVED'
      course = service.courses().update(id=course["id"], body=course).execute()
      print(f" Updated Course and state  is :  {course.get('name')},{course.get('courseState')}")
      course = service.courses().delete(id=course["id"]).execute()
    else :
      print("Classroom Id is a LTI classromm not delete",course["id"])
  print("Count of deleted classroooms",count)
  return final_list

  
def classroom_delete_drive_folder(classroom_folder,classroom_id):
  service= build("drive", "v2", credentials=creds)
  try:
    drive_file = service.files().get(fileId=classroom_folder).execute()
    file_object = service.files().delete(fileId=classroom_folder).execute()
    print("Delete_drive_folder",drive_file["title"],classroom_folder,file_object)
    return None
  except HttpError as hte:
    print(f"Error occured: {hte}")
    err = traceback.format_exc().replace("\n", " ")
    print(err)
    return classroom_id


if __name__ == "__main__":
  
  result = delete_classroom_courses()
