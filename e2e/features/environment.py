import os
import json
import requests
from behave import fixture, use_fixture
from common.models import CourseTemplate, Cohort,Section, TempUser ,CourseEnrollmentMapping
from common.testing.example_objects import TEST_SECTION,TEST_COHORT
from google.oauth2 import service_account
from googleapiclient.discovery import build
from testing_objects.test_config import API_URL_AUTHENTICATION_SERVICE
from e2e.gke_api_tests.secrets_helper import get_user_email_and_password_for_e2e,get_student_email_and_token
from testing_objects.course_template import COURSE_TEMPLATE_INPUT_DATA
from testing_objects.user import TEST_USER
from google.oauth2.credentials import Credentials
import logging

USER_EMAIL_PASSWORD_DICT = get_user_email_and_password_for_e2e()

def create_course(name,section,description,ownerId):
  """Create course Function in classroom

  Args: course_name ,description of course, section,owner_id of course
  Returns:
    new created course details
    """""
  SCOPES = ["https://www.googleapis.com/auth/classroom.courses",
            "https://www.googleapis.com/auth/classroom.courses.readonly"]
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
  new_course["ownerId"] = ownerId
  new_course["courseState"] = "ACTIVE"
  course = service.courses().create(body=new_course).execute()
  return course

def enroll_student_classroom(access_token,course_id,student_email,course_code):
  """Add student to the classroom using student google auth token
  Args:
    headers :Bearer token
    access_token(str): Oauth access token which contains student credentials
    course_id(str): unique classroom id which is required to get the classroom
    student_email(str): student email id
    course_code(str): unique classroom enrollment code
  Raise:
    InvalidTokenError: Raised if the token is expired or not valid
  Return:
    dict: returns a dict which contains student and classroom details
  """

  creds = Credentials(token=access_token)
  service = build("classroom", "v1", credentials=creds)
  student = {"userId": student_email}
  service.courses().students().create(
      courseId=course_id, body=student, enrollmentCode=course_code).execute()
  # Get the gaia ID of the course
  people_service = build("people", "v1", credentials=creds)
  profile = people_service.people().get(resourceName="people/me",
  personFields="metadata").execute()
  gaia_id = profile["metadata"]["sources"][0]["id"]
  # Call user API
  data = {
  "first_name": "",
  "last_name": "",
  "email":student_email,
  "user_type": "learner",
  "user_type_ref": "",
  "user_groups": [],
  "status": "active",
  "is_registered": True,
  "failed_login_attempts_count": 0,
  "access_api_docs": False,
  "gaia_id":gaia_id
  }
  return data



@fixture
def create_course_templates(context):
  """Fixture to create temporary data"""
  course_template = CourseTemplate.from_dict(COURSE_TEMPLATE_INPUT_DATA)
  classroom = create_course(
      course_template.name, "master", course_template.description,course_template.admin)
  course_template.classroom_id=classroom["id"]
  course_template.classroom_code=classroom["enrollmentCode"]
  course_template.classroom_url = classroom["alternateLink"]
  course_template.save()
  context.course_template=course_template
  yield context.course_template

@fixture
def create_cohort(context):
  """Fixture to create cohort temporary data"""
  cohort=Cohort.from_dict(TEST_COHORT)
  course_template=use_fixture(create_course_templates,context)
  cohort.course_template=course_template
  cohort.save()
  context.cohort=cohort
  yield context.cohort

@fixture
def create_section(context):
  """Fixture to create section temprorary data"""
  section = Section.from_dict(TEST_SECTION)
  cohort=use_fixture(create_cohort,context)
  section.course_template=cohort.course_template
  section.cohort=cohort
  context.course_name = cohort.course_template.name
  context.course_section = section.section
  context.course_description = section.description
  context.course_ownerId = context.cohort.course_template.admin
  classroom=create_course(cohort.course_template.name,section.section,section.description,cohort.course_template.admin)
  section.classroom_id=classroom["id"]
  section.classroom_code = classroom["enrollmentCode"]
  section.classroom_url = classroom["alternateLink"]
  section.save()
  context.sections=section
  yield context.sections

@fixture
def enroll_student_course(context):
  """Fixture to enroll studnet in course"""
  # section = Section.from_dict(TEST_SECTION)
  # cohort=use_fixture(create_cohort,context)
  print("------------INside ENroll student Fixtureee------------------")
  section = use_fixture(create_section,context)
  section_id = section.id
  context.section_id = section_id
  classroom_code = section.classroom_code
  classroom_id = section.classroom_id
  student_email_and_token = get_student_email_and_token()
  print("----------Details -----------",section_id,classroom_code,classroom_id)
  print("Student email",student_email_and_token["email"]) 
  print("Student Access token",student_email_and_token["access_token"])
  student_data = enroll_student_classroom(student_email_and_token["access_token"],classroom_id,student_email_and_token["email"],classroom_code)  
  course_enrollment_mapping = CourseEnrollmentMapping()
  course_enrollment_mapping.role = "learner"
  course_enrollment_mapping.section = section
  course_enrollment_mapping.status ="active"
  temp_user = TempUser.from_dict(student_data)
  temp_user.user_id = ""
  print("Temp user before calling save------------------",temp_user)
  temp_user.save()
  temp_user.user_id = temp_user.id
  temp_user.update()
  user_id = temp_user.user_id
  context.user_id = user_id
  print("USER ID -----------------",user_id)
  course_enrollment_mapping = user_id
  course_enrollment_mapping.save()
  context.course_enrollment_mapping= course_enrollment_mapping
  print("UsER ID from Temp User  -------------",user_id)
  print("COUSRSE Enrollment mapping done")
  yield context.course_enrollment_mapping


@fixture
def get_header(context):
  req = requests.post(f"{API_URL_AUTHENTICATION_SERVICE}/sign-in/credentials",
                      json=USER_EMAIL_PASSWORD_DICT,
                      timeout=60)
  res = req.json()
  if res is None or res["data"] is None:
    raise Exception("User sign-in failed")
  token = req.json()['data']['idToken']
  print(f"User with {USER_EMAIL_PASSWORD_DICT['email']} was logged in with "
        f"token {token}")
  context.header={"Authorization": f"Bearer {token}"}
  #   session=httpx.Client(headers={"Authorization": f"Bearer {token}"})
  yield context.header

fixture_registry = {
    "fixture.create.course_template": create_course_templates,
    "fixture.create.cohort": create_cohort,
    "fixture.create.section":create_section,
    "fixture.create.enroll_student_course":enroll_student_course,
    "fixture.get.header":get_header
}

def before_tag(context, tag):
  if tag.startswith("fixture."):
    try:
      fixture_data = fixture_registry.get(tag, None)
      if fixture_data is None:
        raise LookupError("Unknown fixture-tag: %s" % tag)
      return use_fixture(fixture_data, context)
    except Exception as e:
      print(e)
      logging.error(str(e))

def sign_up_user():
  input_user = {**TEST_USER}
  if not TempUser.find_by_email(input_user["email"]):
    user = TempUser.from_dict(input_user)
    user.user_id = ""
    user.save()
    user.user_id = user.id
    user.update()
    print(f"created_user {user.user_id} ")
    req = requests.post(
        f"{API_URL_AUTHENTICATION_SERVICE}/sign-up/credentials",
        json=USER_EMAIL_PASSWORD_DICT,timeout=40)
    if req.status_code!=200:
      if req.status_code == 422 and req.json().get(
        "message") == "EMAIL_EXISTS":
        print("signup: user email exists")
      else:
        raise Exception("User sign-up failed")
  else:
    print("firestore: user email already exists")
def before_all(context):
  sign_up_user()
