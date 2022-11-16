import requests
from endpoint_proxy import get_baseurl
import mock
import os
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from common.utils.errors import ResourceNotFoundException
# from microservices.lms.src import routes

def test_get_course_list():
  base_url = get_baseurl("lms")
  if not base_url:
    raise ResourceNotFoundException("Unable to locate the service URL for lms")
  res = requests.get(base_url + "/lms/api/v1/course/get_courses/")
  result = res.json()
  assert res.status_code == 200

def test_copy_course():
  DATABASE_PREFIX =os.environ.get("DATABASE_PREFIX")
  # Creating a course  with DATABASE_PREFIX NAME 
  SCOPES = ["https://www.googleapis.com/auth/classroom.courses",
    "https://www.googleapis.com/auth/classroom.courses.readonly"]
  CLASSROOM_KEY = json.loads(os.environ.get("GKE_POD_SA_KEY"))
  a_creds = service_account.Credentials.from_service_account_info(CLASSROOM_KEY,scopes=SCOPES)
  creds = a_creds.with_subject(os.environ.get("CLASSROOM_ADMIN_EMAIL"))
  service = build("classroom", "v1", credentials=creds)
  new_course = {}
  new_course["name"]=DATABASE_PREFIX + "test_course"
  new_course["section"]="test_section"
  new_course["description"]="This is description"
  # new_course["room"]=course["room"]
  new_course["ownerId"]="me"
  # new_course["descriptionHeading"]=course["description_heading"]
  course = service.courses().create(body=new_course).execute()
  course_name = course.get("name")
  course_id = course.get("id")
  # Get the course_id of course and hit the copy API to copy the given course
  course_details={
    "course_id":course_id
  }
  base_url = get_baseurl("lms")
  res = requests.post(base_url + "/lms/api/v1/course/copy_course/",json=course_details)
  print(res.json())
  assert res.status_code == 200
