"""Course template list and Course template CRUD API e2e tests"""
import os
import pytest
import json

import requests
from common.utils.errors import ResourceNotFoundException
from secrets_helper import get_required_emails_from_secret_manager
from googleapiclient.discovery import build
from google.oauth2 import service_account
from common.testing.example_objects import create_fake_data, TEST_COURSE_TEMPLATE2, TEST_COHORT2, TEST_SECTION2
from common.utils.jwt_creds import JwtCredentials
from testing_objects.test_config import API_URL
from testing_objects.token_fixture import get_token,sign_up_user

DATABASE_PREFIX = os.environ.get("DATABASE_PREFIX")
EMAILS = get_required_emails_from_secret_manager()


def create_course(name, description, section, owner_id):
  """Create course Function in classroom

  Args: course_name ,description of course, section,owner_id of course
  Returns:
    new created course details
    """ ""
  scopes = [
      "https://www.googleapis.com/auth/classroom.courses",
      "https://www.googleapis.com/auth/classroom.courses.readonly"
  ]
  classroom_key = json.loads(os.environ.get("GKE_POD_SA_KEY"))
  classroom_admin_email = os.environ.get("CLASSROOM_ADMIN_EMAIL")
  a_creds = service_account.Credentials.from_service_account_info(
      classroom_key, scopes=scopes)
  creds = a_creds.with_subject(classroom_admin_email)
  service = build("classroom", "v1", credentials=creds)
  new_course = {}
  new_course["name"] = name
  new_course["section"] = section
  new_course["description"] = description
  # new_course["room"]=course["room"]
  new_course["ownerId"] = owner_id
  # new_course["descriptionHeading"]=course["description_heading"]
  course = service.courses().create(body=new_course).execute()
  course_name = course.get("name")
  course_id = course.get("id")
  print("___________Course created___________________",course)
  return course

def test_create_section(get_token):

  """
  create a Course template and cohort is created  by  user  
  then user clicks on create section button and makes a section 
  by providing section name ,description,course_template_id,cohort_id
  and list of teachers .A record is created in database and a course
  with details of course template is created in classroom
  """
  # Create fake classroom in Google Classroom
  course = create_course(DATABASE_PREFIX + "test_course", "This is test",
                         "test", "me")
  # Create fake Master course in Firestore
  classroom_id = course["id"]
  test_course_template_dict = TEST_COURSE_TEMPLATE2
  test_course_template_dict["name"] = DATABASE_PREFIX + "test_course"
  test_course_template_dict["instructional_designer"] = EMAILS["instructional_designer"]
  fake_data = create_fake_data(test_course_template_dict, TEST_COHORT2,
                               TEST_SECTION2, classroom_id)
  url = f"{API_URL}/sections"

  data = {
      "name": "e2e_test_section",
      "description": "string",
      "course_template": fake_data[0].id,
      "cohort": fake_data[1].id,
      "max_students":25
  }
  resp = requests.post(url=url, json=data, headers=get_token)
  resp_json = resp.json()
  print("Response Json create section", resp_json)
  assert resp.status_code == 202, "Status 202"

def test_create_section_course_template_not_found(get_token):
  """ 
  create a Course template and cohort is created by user
  then user clicks on create section button and makes a section 
  by providing section name,description,course_template_id,cohort_id
  and list of teachers. Given course template id is wrong and course template
  id not found error is thrown
  """
  # Create fake classroom in Google Classroom
  course = create_course(DATABASE_PREFIX + "test_course", "This is test",
                         "test", "me")
  # Create fake Master course in Firestore
  classroom_id = course["id"]
  fake_data = create_fake_data(TEST_COURSE_TEMPLATE2, TEST_COHORT2,
                               TEST_SECTION2, classroom_id)
  url = f"{API_URL}/sections"

  data = {
      "name": "string",
      "description": "string",
      "course_template": "fake_template_id_new",
      "cohort": fake_data[1].id,
      "max_students":25
  }

  resp = requests.post(url=url, json=data, headers=get_token)
  assert resp.status_code == 404

def test_get_section(get_token):
  """
    Get a sections details for a section by giving section_id as query parameter
  """
  course = create_course(DATABASE_PREFIX + "test_course", "This is test",
                         "test", "me")
  classroom_id = course["id"]
  fake_data = create_fake_data(TEST_COURSE_TEMPLATE2, TEST_COHORT2,
                               TEST_SECTION2, classroom_id)
  url = f"{API_URL}/sections/{fake_data[2].id}"
  resp = requests.get(url=url, headers=get_token)
  resp_json = resp.json()
  print("Response Json get section details", resp_json)
  assert resp.status_code == 200, "Status 200"


def test_list_sections(get_token):
  """
    List all the sections
  """
  course = create_course(DATABASE_PREFIX + "test_course", "This is test",
                         "test", "me")
  classroom_id = course["id"]
  create_fake_data(TEST_COURSE_TEMPLATE2, TEST_COHORT2, TEST_SECTION2,
                   classroom_id)
  url = f"{API_URL}/sections?skip=0&limit=10"
  print("List sections API url----",url)
  resp = requests.get(url=url, headers=get_token)
  resp_json = resp.json()
  print("This is response Json list sections", resp_json)
  assert resp.status_code == 200, "Status 200"

def test_update_section(get_token):
  """ 
  User click on edit button for a section 
  User Updates the section name ,description,course_state by providing expected 
  values and details get updated in firestore and classroom course
  """
  # Create fake classroom in Google Classroom
  course = create_course(DATABASE_PREFIX + "test_course", "This is test",
                         "test", "me")
  # Create fake Master course in Firestore
  classroom_id = course["id"]
  fake_data = create_fake_data(TEST_COURSE_TEMPLATE2, TEST_COHORT2,
                               TEST_SECTION2, classroom_id)
  url = f"{API_URL}/sections"

  data = {
      "id": fake_data[2].id,
      "course_id": classroom_id,
      "section_name": "section_updated",
      "description": "test_description_updated",
      "max_students":25
  }
  resp = requests.patch(url=url, json=data, headers=get_token)
  resp_json = resp.json()
  print("Response Json update section", resp_json)
  assert resp.status_code == 200, "Status 200"

def test_update_section_course_not_found_in_classroom(get_token):
  """
  User click on edit button for a section
  User Updates the section name ,description,course_state by providing expected
  values but given course_id of classroom is incorrect, so it gives course not found error
  """
  # Create fake classroom in Google Classroom
  course = create_course(DATABASE_PREFIX + "test_course", "This is test",
                         "test", "me")
  # Create fake Master course in Firestore
  classroom_id = course["id"]
  fake_data = create_fake_data(TEST_COURSE_TEMPLATE2, TEST_COHORT2,
                               TEST_SECTION2, classroom_id)
  url = f"{API_URL}/sections"

  data = {
      "id": fake_data[2].id,
      "course_id": "test1222",
      "section_name": "section_updated",
      "description": "test_description_updated",
      "max_students":25
  }
  resp = requests.patch(url=url, json=data, headers=get_token)
  assert resp.status_code == 500
