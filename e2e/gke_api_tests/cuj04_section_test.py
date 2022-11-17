"""Course template list and Course template CRUD API e2e tests"""
import os
import pytest
import requests
import uuid
import requests
import mock
import os
import json
from endpoint_proxy import get_baseurl
from common.models import CourseTemplate
from common.testing.example_objects import TEST_COURSE_TEMPLATE
from common.utils.errors import ResourceNotFoundException
from secrets_helper import get_required_emails_from_secret_manager
import datetime
from common.models.cohort import Cohort
from common.models.section import Section
from common.models.course_template import CourseTemplate
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from common.testing.example_objects import TEST_COURSE_TEMPLATE2,TEST_COHORT2,TEST_SECTION2
DATABASE_PREFIX = os.environ.get("DATABASE_PREFIX")
EMAILS  =  get_required_emails_from_secret_manager()
TEACHER_EMAIL = EMAILS["instructional_designer"]

def create_fake_data(classroom_id):
  """Function to create temprory data"""

  # TEST_COURSE_TEMPLATE = {
  #     "name": "test-name",
  #     "uuid":"fake_template_id",
  #     "description": "test-description",
  #     "admin": "test-admin@gmail.com",
  #     "instructional_designer": "IDesiner@gmail.com",
  #     "classroom_id": "fake_classroom_id",
  #     "classroom_code": "fake-classroom_code"}
  TEST_COURSE_TEMPLATE["classroom_id"]=classroom_id
  course_template = CourseTemplate.from_dict(TEST_COURSE_TEMPLATE)
  course_template.save()
  
  # TEST_COHORT = {
  #   "uuid":"fake_cohort_id",
  #   "name": "name",
  #   "description": "description",
  #   "course_template":course_template,
  #   "start_date": datetime.datetime(year=2022,month=10, day=14),
  #   "end_date": datetime.datetime(year=2022,month=12, day=25),
  #   "registration_start_date": datetime.datetime(year=2022,month=10, day=20),
  #   "registration_end_date": datetime.datetime(year=2022,month=11, day=14),
  #   "max_student": 0,
  #   "enrolled_student_count":0
  # }
  TEST_COHORT =TEST_COHORT2
  TEST_COHORT["course_template"]=course_template
  
  cohort = Cohort.from_dict(TEST_COHORT)
  cohort.save()

  # TEST_SECTION = {
  #   "uuid":"fake_section_id",
  #   "name" : "section_name",
  #   "section" : "section c",
  #   "description": "description",
  #   "classroom_id" :"cl_id",
  #   "classroom_code" :"cl_code",
  #   "course_template":course_template,
  #   "cohort":cohort,    
  #   "teachers_list":[TEACHER_EMAIL]
  # }
  TEST_SECTION = TEST_SECTION2
  TEST_SECTION["cohort"]=cohort
  TEST_SECTION["course_template"] = course_template
  section = Section.from_dict(TEST_SECTION)
  section.save()
  return course_template , cohort,section
  
def create_course(name,description,section,owner_id):
  """Create course Function in classroom

  Args: course_name ,description of course, section,owner_id of course
  Returns:
    new created course details
    """""
  SCOPES = ["https://www.googleapis.com/auth/classroom.courses",
  "https://www.googleapis.com/auth/classroom.courses.readonly"]
  CLASSROOM_KEY = json.loads(os.environ.get("GKE_POD_SA_KEY"))
  CLASSROOM_ADMIN_EMAIL=os.environ.get("CLASSROOM_ADMIN_EMAIL")
  a_creds = service_account.Credentials.from_service_account_info(CLASSROOM_KEY,scopes=SCOPES)
  creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
  service = build("classroom", "v1", credentials=creds)
  new_course = {}
  new_course["name"]=name
  new_course["section"]=section
  new_course["description"]=description
  # new_course["room"]=course["room"]
  new_course["ownerId"]=owner_id
  # new_course["descriptionHeading"]=course["description_heading"]
  course = service.courses().create(body=new_course).execute()
  course_name = course.get("name")
  course_id = course.get("id")
  return course

def test_create_section():
  """ 
  create a Course template and cohort is created  by  user  
  then user clicks on create section button and makes a section 
  by providing section name ,description,course_template_id,cohort_id
  and list of teachers .A record is created in database and a course
  with details of course template is created in classroom
  """
  # Create fake classroom in google classroom
  course=create_course(DATABASE_PREFIX+"test_course","This is test","test","me")
  # Create fake Mastr course in Firestore
  print("THIS IS FAKE MASTER COURSEE ",course)
  classroom_id = course["id"]
  create_fake_data(classroom_id)
  base_url = get_baseurl("lms")
  if not base_url:
      raise ResourceNotFoundException("Unable to locate the service URL for lms")
  url = base_url + f"/lms/api/v1/sections"

  print(base_url)
  data = {
  "name": "string",
  "description": "string",
  "course_template": "fake_template_id",
  "cohort": "fake_cohort_id",
  "teachers_list": [TEACHER_EMAIL]}

  resp = requests.post(url=url, json=data)
  resp_json = resp.json()
  print(resp_json)
  assert resp.status_code == 200, "Status 200"

def test_create_section_course_template_not_found():
  """ 
  create a Course template and cohort is created  by  user  
  then user clicks on create section button and makes a section 
  by providing section name ,description,course_template_id,cohort_id
  and list of teachers .Given course template id is wrong and course template 
  id not found error is thrown
  """
  # Create fake classroom in google classroom
  course=create_course(DATABASE_PREFIX+"test_course","This is test","test","me")
  # Create fake Mastr course in Firestore
  print("THIS IS FAKE MASTER COURSEE ",course)
  classroom_id = course["id"]
  create_fake_data(classroom_id)
  base_url = get_baseurl("lms")
  if not base_url:
      raise ResourceNotFoundException("Unable to locate the service URL for lms")
  url = base_url + f"/lms/api/v1/sections"

  print(base_url)
  data = {
  "name": "string",
  "description": "string",
  "course_template": "fake_template_id_new",
  "cohort": "fake_cohort_id",
  "teachers_list": [TEACHER_EMAIL]}

  resp = requests.post(url=url, json=data)
  resp_json = resp.json()
  print(resp_json)
  assert resp.status_code == 404

def test_get_list_sections():
  """ 
  Get a sections list for a perticular cohort by giving cohort_id as query paramter 
  """
  course=create_course(DATABASE_PREFIX+"test_course","This is test","test","me")
  classroom_id = course["id"]
  create_fake_data(classroom_id)
  base_url = get_baseurl("lms")
  url = base_url + "/lms/api/v1/sections/fake_cohort_id"
  print(base_url)
  resp = requests.get(url=url)
  resp_json = resp.json()
  assert resp.status_code == 200, "Status 200"

def test_get_section():
  """
    Get a sections details for a  section by giving section_id as query paramter 
  """
  course=create_course(DATABASE_PREFIX+"test_course","This is test","test","me")
  classroom_id = course["id"]
  create_fake_data(classroom_id)
  base_url = get_baseurl("lms")
  url = base_url + "/lms/api/v1/sections/get_section/fake_section_id"
  print(base_url)
  resp = requests.get(url=url)
  resp_json = resp.json()
  assert resp.status_code == 200, "Status 200"    

def test_update_section():
  """ 
  User click on edit button for a section 
  User Updates the section name ,description,course_state by providing expected 
  values and details get updated in firestore and classroom course
  """
  # Create fake classroom in google classroom
  course=create_course(DATABASE_PREFIX+"test_course","This is test","test","me")
  # Create fake Mastr course in Firestore
  print("THIS IS FAKE MASTER COURSEE ",course)
  classroom_id = course["id"]
  create_fake_data(classroom_id)
  base_url = get_baseurl("lms")
  if not base_url:
      raise ResourceNotFoundException("Unable to locate the service URL for lms")
  url = base_url + f"/lms/api/v1/sections/update_section"

  print(base_url)
  data={
"uuid": "fake_section_id",
"course_id": classroom_id,
"section_name": "section_updated",
"description": "test_description_updated",
"course_state": "ACTIVE"
  }
  resp = requests.post(url=url, json=data)
  resp_json = resp.json()
  print(resp_json)
  assert resp.status_code == 200, "Status 200"

def test_update_section_course_not_found_in_classroom():
  """ 
  User click on edit button for a section 
  User Updates the section name ,description,course_state by providing expected 
  values but given course_id of classroom is incorrect so it gives course not found error
  """
  # Create fake classroom in google classroom
  course=create_course(DATABASE_PREFIX+"test_course","This is test","test","me")
  # Create fake Mastr course in Firestore
  print("THIS IS FAKE MASTER COURSEE ",course)
  classroom_id = course["id"]
  create_fake_data(classroom_id)
  base_url = get_baseurl("lms")
  if not base_url:
      raise ResourceNotFoundException("Unable to locate the service URL for lms")
  url = base_url + f"/lms/api/v1/sections/update_section"

  print(base_url)
  data={
"uuid": "fake_section_id",
"course_id":"test1222",
"section_name": "section_updated",
"description": "test_description_updated",
"course_state": "ACTIVE"}
  resp = requests.post(url=url, json=data)
  assert resp.status_code == 500