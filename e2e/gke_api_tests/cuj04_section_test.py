"""Course template list and Course template CRUD API e2e tests"""
import os
import pytest
import json
from common.utils.errors import ResourceNotFoundException
from secrets_helper import get_required_emails_from_secret_manager
from googleapiclient.discovery import build
from google.oauth2 import service_account
from common.testing.example_objects import create_fake_data, TEST_COURSE_TEMPLATE2, TEST_COHORT2, TEST_SECTION2
from testing_objects.test_config import API_URL
from testing_objects.session_fixture import get_session

DATABASE_PREFIX = os.environ.get("DATABASE_PREFIX")
EMAILS = get_required_emails_from_secret_manager()
TEACHER_EMAIL = EMAILS["instructional_designer"]


def create_course(name, description, section, owner_id):
  """Create course Function in classroom

  Args: course_name ,description of course, section,owner_id of course
  Returns:
    new created course details
    """ ""
  SCOPES = [
      "https://www.googleapis.com/auth/classroom.courses",
      "https://www.googleapis.com/auth/classroom.courses.readonly"
  ]
  CLASSROOM_KEY = json.loads(os.environ.get("GKE_POD_SA_KEY"))
  CLASSROOM_ADMIN_EMAIL = os.environ.get("CLASSROOM_ADMIN_EMAIL")
  a_creds = service_account.Credentials.from_service_account_info(
      CLASSROOM_KEY, scopes=SCOPES)
  creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
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
  return course


def test_create_section(get_session):
  """
  create a Course template and cohort is created  by  user  
  then user clicks on create section button and makes a section 
  by providing section name ,description,course_template_id,cohort_id
  and list of teachers .A record is created in database and a course
  with details of course template is created in classroom
  """
  # Create fake classroom in google classroom
  course = create_course(DATABASE_PREFIX + "test_course", "This is test",
                         "test", "me")
  # Create fake Mastr course in Firestore
  classroom_id = course["id"]
  create_fake_data(TEST_COURSE_TEMPLATE2, TEST_COHORT2, TEST_SECTION2,
                   classroom_id)
  url = f"{API_URL}/sections"

  data = {
      "name": "string",
      "description": "string",
      "course_template": "fake_template_id",
      "cohort": "fake_cohort_id",
      "teachers_list": [TEACHER_EMAIL]
  }
  resp = get_session.post(url=url, json=data)
  resp_json = resp.json()
  assert resp.status_code == 200, "Status 200"


def test_create_section_course_template_not_found(get_session):
  """ 
  create a Course template and cohort is created  by  user  
  then user clicks on create section button and makes a section 
  by providing section name ,description,course_template_id,cohort_id
  and list of teachers .Given course template id is wrong and course template 
  id not found error is thrown
  """
  # Create fake classroom in google classroom
  course = create_course(DATABASE_PREFIX + "test_course", "This is test",
                         "test", "me")
  # Create fake Mastr course in Firestore
  classroom_id = course["id"]
  create_fake_data(TEST_COURSE_TEMPLATE2, TEST_COHORT2, TEST_SECTION2,
                   classroom_id)
  url = f"{API_URL}/sections"

  data = {
      "name": "string",
      "description": "string",
      "course_template": "fake_template_id_new",
      "cohort": "fake_cohort_id",
      "teachers_list": [TEACHER_EMAIL]
  }

  resp = get_session.post(url=url, json=data)
  resp_json = resp.json()
  assert resp.status_code == 404


def test_get_list_sections(get_session):
  """ 
  Get a sections list for a perticular cohort by giving cohort_id as query paramter 
  """
  course = create_course(DATABASE_PREFIX + "test_course", "This is test",
                         "test", "me")
  classroom_id = course["id"]
  create_fake_data(TEST_COURSE_TEMPLATE2, TEST_COHORT2, TEST_SECTION2,
                   classroom_id)
  url = f"{API_URL}/sections/cohort/fake_cohort_id/sections"
  resp = get_session.get(url=url)
  resp_json = resp.json()
  assert resp.status_code == 200, "Status 200"


def test_get_section(get_session):
  """
    Get a sections details for a  section by giving section_id as query paramter 
  """
  course = create_course(DATABASE_PREFIX + "test_course", "This is test",
                         "test", "me")
  classroom_id = course["id"]
  create_fake_data(TEST_COURSE_TEMPLATE2, TEST_COHORT2, TEST_SECTION2,
                   classroom_id)
  url = f"{API_URL}/sections/fake_section_id"
  resp = get_session.get(url=url)
  resp_json = resp.json()
  assert resp.status_code == 200, "Status 200"


def test_list_sections(get_session):
  """
    List all the sections
  """
  course = create_course(DATABASE_PREFIX + "test_course", "This is test",
                         "test", "me")
  classroom_id = course["id"]
  create_fake_data(TEST_COURSE_TEMPLATE2, TEST_COHORT2, TEST_SECTION2,
                   classroom_id)
  url = f"{API_URL}/sections"
  resp = get_session.get(url=url)
  resp_json = resp.json()
  assert resp.status_code == 200, "Status 200"


def test_update_section(get_session):
  """ 
  User click on edit button for a section 
  User Updates the section name ,description,course_state by providing expected 
  values and details get updated in firestore and classroom course
  """
  # Create fake classroom in google classroom
  course = create_course(DATABASE_PREFIX + "test_course", "This is test",
                         "test", "me")
  # Create fake Mastr course in Firestore
  classroom_id = course["id"]
  create_fake_data(TEST_COURSE_TEMPLATE2, TEST_COHORT2, TEST_SECTION2,
                   classroom_id)
  url = f"{API_URL}/sections"

  data = {
      "uuid": "fake_section_id",
      "course_id": classroom_id,
      "section_name": "section_updated",
      "description": "test_description_updated",
      "course_state": "ACTIVE"
  }
  resp = get_session.patch(url=url, json=data)
  resp_json = resp.json()
  assert resp.status_code == 200, "Status 200"


def test_update_section_course_not_found_in_classroom(get_session):
  """ 
  User click on edit button for a section 
  User Updates the section name ,description,course_state by providing expected 
  values but given course_id of classroom is incorrect so it gives course not found error
  """
  # Create fake classroom in google classroom
  course = create_course(DATABASE_PREFIX + "test_course", "This is test",
                         "test", "me")
  # Create fake Mastr course in Firestore
  classroom_id = course["id"]
  create_fake_data(TEST_COURSE_TEMPLATE2, TEST_COHORT2, TEST_SECTION2,
                   classroom_id)
  url = f"{API_URL}/sections"

  data = {
      "uuid": "fake_section_id",
      "course_id": "test1222",
      "section_name": "section_updated",
      "description": "test_description_updated",
      "course_state": "ACTIVE"
  }
  resp = get_session.patch(url=url, json=data)
  assert resp.status_code == 500
