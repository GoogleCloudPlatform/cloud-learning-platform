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

CLASSROOM_KEY = {
  "type": "service_account",
  "project_id": "core-learning-services-dev",
  "private_key_id": "3ad36ab0c4ceba2824251e549f8398165396d144",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDNRMpkJhIS9ur1\nYah1aWA8/RqAv4meV/E9E6R38Ey4EdYgNTBiAmbOHqYAWKABP1gk3hqzw4iHAUPr\nI8LWqxREdEdgUAgsFji3cdH6cugyaRDBSbcO38v1dP3VOUTAEXLNwm/ZfamW6F5b\nTr7saB/GfF6oQjwoCW8f7o+Z47S4fE9JMyB0QkCj/mUnITZCXOWJ8aOpQU3Ew1Q4\nTytZxC4bfyBSMgFSN9+AIgnyNmzefbOlII/tzJfi+u0Dwl5bQjQQ6oA+ax+Wln+S\npIWk1nHCBi2FcrgLPHflVGZZPL8/+38RVlswdTMSRRlYKrkyGSbEGWI+6idwn4OO\nl+Nr6RuJAgMBAAECggEADn2/bA05VBgVGPhT/uCkPVSrp6Xd/qJmvXvC2Kog6xMX\nSB7Ofkd9H9VkvWbZpOeRPskPSYbm/zZE/TdWbKFB77M7IWmE/4JyGUFHzvkzEJv/\nkCW2xANjUBN6TVtFpz7pbpfoyDSUNxB12NcDqNzmTApBBHqTP0sAiq3k0BBrPxAn\nNB+Sf4KZF/c8MgkOsljEyqx9sZlU+msZ1Ca3IZ9UNeTI7AD4+oLKSflXQO06r5xo\nCLIvN2p3PqQXcMz5mg99zT5khbV1XnG2BqU4r7mz8SsSTjZKmsjIJ8FuHciD9SVR\ndld1HGhP9UqgUtUpiIDw/bNzQW4eWz0bRQ2PEQN0IQKBgQDphL0z4ViLG1LWt47P\nqwm/YOWd3EVnqrSmbNT6r3bYhWEQfd1dD5rjfXf0dMOam9chgeG4jGuD5acCnisV\noF4/BPjr4UceRlilwKDFPH/NrzUKG0fiqxVzBFc19f4/DAMxSsKjHFVEB7zvtFJZ\nch3h2XxjGdB8xHgRhjaNM1qeHwKBgQDhB8+2B+78znF8gw2QmihoOFI8gAQ9igsy\nobC/6wOt0+LP5X08yDuhcijDCAuhmJNC6naex6+mJprYkVEQkRK9ArYE3YwnKl8+\nuaL+18Ed8Fg/9+4lJA8/kv6ifNiYPE9JvKPn91jxF4VX9sKXEByuMe3y7F1ndkEN\n38IMrBjBVwKBgQDM+HNut20V5SzoRYR4KgRLVM0XrEHLhd49eqfTRvLFiQWzCRel\n2M22wunozBjpe8LwqWWsrKyuwITA2n6s4+/11vJ7cWkQXOTw0M0Nc1Ym/5RJw7ps\nbolMRNIcDklVo8Clop6Ht5XsOfKQYLIryuwJ0vHItt72tSlDEJCPjjULNwKBgDxL\nc4Q6q/Zg+ld6ZfAQ3jLOpHpBcuFqU4XFfS5vMhUpaOR7gQsAO7oOdI2NYlByKUMM\nv6vbpVzHi0Xr6eSeen7acxrqodr8p3iPFPVjqgLzmzHIpK6e8tb98+xlt0NTJYuE\nWAaXZ+Vxf/EJ1SnUz1p9Vlx4qK5IKTYmdkAe/KMRAoGBAL+6g46ZasKYD7hXs/FW\nobtf3rC9DGwodV+EsUb+9xmGSvNLuFr9MB7gfxjdLM4J2LsO69uW5RVzRHs98axz\n73zrkdqMq9m6g8b23sU3PkJ8EbNdca8z9JpQdCP3AfkvrbRTVgu651fHNQtLjaGG\nv07ie+HINdOqgVNF1VBt+8Fi\n-----END PRIVATE KEY-----\n",
  "client_email": "gke-pod-sa@core-learning-services-dev.iam.gserviceaccount.com",
  "client_id": "104636564660654922211",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/gke-pod-sa%40core-learning-services-dev.iam.gserviceaccount.com"
}

# CLASSROOM_KEY = json.loads(os.environ.get("GKE_POD_SA_KEY"))
CLASSROOM_ADMIN_EMAIL = os.environ.get("CLASSROOM_ADMIN_EMAIL")
SCOPES = ["https://www.googleapis.com/auth/classroom.courses",
          "https://www.googleapis.com/auth/classroom.courses.readonly",
          "https://www.googleapis.com/auth/classroom.coursework.students"]

def create_course(name,section,description):
  """Create course Function in classroom

  Args: course_name ,description of course, section,owner_id of course
  Returns:
    new created course details
    """""
  a_creds = service_account.Credentials.from_service_account_info(
      CLASSROOM_KEY, scopes=SCOPES)
  creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
  service = build("classroom", "v1", credentials=creds)
  new_course = {}
  new_course["name"] = name
  new_course["section"] = section
  new_course["description"] = description
  new_course["ownerId"] = "me"
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
      course_template.name, "master", course_template.description)
  course_template.classroom_id=classroom["id"]
  course_template.admin=CLASSROOM_ADMIN_EMAIL
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
  classroom=create_course(cohort.course_template.name,
                          section.section,section.description)
  section.classroom_id=classroom["id"]
  section.classroom_code = classroom["enrollmentCode"]
  section.classroom_url = classroom["alternateLink"]
  section.save()
  # Create teachers in the DB 
  temp_user = TempUser.from_dict(TEST_USER)
  temp_user.email = TEST_SECTION["teachers"][0]
  temp_user.user_type = "faculty"
  temp_user.first_name = TEST_SECTION["teachers"][0].split("@")[0]
  temp_user.user_id = ""
  temp_user.save()
  temp_user.user_id = temp_user.id
  temp_user.update()
  temp_user1 = TempUser.from_dict(TEST_USER)
  temp_user1.email = TEST_SECTION["teachers"][1].split("@")[0]
  temp_user1.user_type = "faculty"
  temp_user1.user_id = ""
  temp_user1.save()
  temp_user1.user_id = temp_user.id
  temp_user1.update()
  print("TEST TEACHERS CREATED",TEST_SECTION["teachers"][1].split("@")[0],TEST_SECTION["teachers"][0].split("@")[0])
  context.sections=section
  yield context.sections

@fixture
def enroll_student_course(context):
  """Fixture to enroll studnet in course"""
 
  section = use_fixture(create_section,context)
  classroom_code = section.classroom_code
  classroom_id = section.classroom_id
  student_email_and_token = get_student_email_and_token()
  student_data = enroll_student_classroom(student_email_and_token["access_token"],classroom_id,student_email_and_token["email"],classroom_code)  
  course_enrollment_mapping = CourseEnrollmentMapping()
  course_enrollment_mapping.role = "learner"
  course_enrollment_mapping.section = section
  course_enrollment_mapping.status ="active"
  temp_user = TempUser.from_dict(student_data)

  temp_user.user_id = ""
  temp_user.save()
  temp_user.user_id = temp_user.id
  temp_user.update()
  course_enrollment_mapping.user = temp_user.user_id
  course_enrollment_mapping.save()
  context.enroll_student_data = {
    "section_id": section.id,
    "user_id":temp_user.id,
    "email": student_email_and_token["email"]
    }
  yield context.enroll_student_data


@fixture
def create_assignment(context):
  """Create assignment fixture"""
  section = use_fixture(create_section, context)
  a_creds = service_account.Credentials.from_service_account_info(
      CLASSROOM_KEY, scopes=SCOPES)
  creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
  service = build("classroom", "v1", credentials=creds)
  result = service.courses().courseWork().create(courseId=section.classroom_id,
                                                 body={
                                                     "title": "test course work",
                                                     "description": "test desc",
                                                     "workType": "ASSIGNMENT"
                                                 }).execute()
  result["section_id"] = section.id
  context.assignment = result
  yield context.assignment

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
    "fixture.get.header": get_header,
    "fixture.create.assignment": create_assignment
}

def before_tag(context, tag):
  if tag.startswith("fixture."):
    try:
      fixture_data = fixture_registry.get(tag, None)
      if fixture_data is None:
        raise LookupError("Unknown fixture-tag: %s" % tag)
      return use_fixture(fixture_data, context)
    except Exception as e:
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
