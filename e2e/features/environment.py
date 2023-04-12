import os
import json
import time
import requests
from behave import fixture, use_fixture
from common.models import CourseTemplate, Cohort,Section, TempUser ,CourseEnrollmentMapping
from common.testing.example_objects import TEST_SECTION,TEST_COHORT
from google.oauth2 import service_account
from googleapiclient.discovery import build
from testing_objects.test_config import API_URL_AUTHENTICATION_SERVICE,API_URL
from e2e.gke_api_tests.secrets_helper import get_user_email_and_password_for_e2e,get_student_email_and_token,get_required_emails_from_secret_manager
from testing_objects.course_template import COURSE_TEMPLATE_INPUT_DATA
from testing_objects.user import TEST_USER
from google.oauth2.credentials import Credentials
import logging

USER_EMAIL_PASSWORD_DICT = get_user_email_and_password_for_e2e()

EMAILS = get_required_emails_from_secret_manager()
TEACHER_EMAIL = EMAILS["teacher"]
CLASSROOM_KEY = json.loads(os.environ.get("GKE_POD_SA_KEY"))
CLASSROOM_ADMIN_EMAIL = os.environ.get("CLASSROOM_ADMIN_EMAIL")
SCOPES = [
  "https://www.googleapis.com/auth/classroom.courses",
  "https://www.googleapis.com/auth/classroom.courses.readonly",
  "https://www.googleapis.com/auth/classroom.coursework.students",
  "https://www.googleapis.com/auth/classroom.rosters",
  "https://www.googleapis.com/auth/classroom.coursework.me",
  "https://www.googleapis.com/auth/classroom.topics",
  "https://www.googleapis.com/auth/drive",
  "https://www.googleapis.com/auth/forms.body.readonly",
  "https://www.googleapis.com/auth/classroom.profile.photos",
  "https://www.googleapis.com/auth/classroom.courseworkmaterials",
  "https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly"
          ]

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
  personFields="metadata,photos,names").execute()
  gaia_id = profile["metadata"]["sources"][0]["id"]
  # Call user API
  data = {
  "first_name": profile["names"][0]["givenName"],
  "last_name": profile["names"][0]["familyName"],
  "email":student_email,
  "user_type": "learner",
  "user_type_ref": "",
  "user_groups": [],
  "status": "active",
  "is_registered": True,
  "failed_login_attempts_count": 0,
  "access_api_docs": False,
  "gaia_id":gaia_id,
  "photo_url":profile["photos"][0]["url"]
  }
  return data

def accept_invite(access_token,email,invitation_id):
  """Add student to the classroom using student google auth token
  Args:
    access_token(str): Oauth access token which contains student credentials
    invitation_id(str): unique classroom id which is required to get the classroom
    email(str): student email id
  Return:
    dict: returns a dict which contains student and classroom details
  """
  creds = Credentials(token=access_token)
  service = build("classroom", "v1", credentials=creds)
  data = service.invitations().accept(id=invitation_id).execute()
  return data

def invite_user(course_id, email,role):
  """Invite teacher to google classroom using course id and email

  Args:
      course_id (str): google classroom unique id
      teacher_email (str): teacher email id

  Raises:
      CustomHTTPException: custom exception for HTTP exceptions
      InternalServerError: 500 Internal Server Error if something fails

  Returns:
      dict: response from create invitation method
  """
  a_creds = service_account.Credentials.from_service_account_info(
      CLASSROOM_KEY, scopes=SCOPES)
  creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
  service = build("classroom", "v1", credentials=creds)
  body = {"courseId": course_id, "role": role, "userId": email}
  invitation = service.invitations().create(body=body).execute()
  return invitation

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
  context.sections=section
  yield context.sections

def create_student_enrollment_record(student_data,section):
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
  return{
    "user_id":temp_user.user_id,
    "course_enrollment_mapping_id":course_enrollment_mapping.id
  }


@fixture
def enroll_student_course(context):
  """Fixture to enroll studnet in course"""
 
  section = use_fixture(create_section,context)
  classroom_code = section.classroom_code
  classroom_id = section.classroom_id
  student_email_and_token = get_student_email_and_token()
  student_data = enroll_student_classroom(student_email_and_token["access_token"],
  classroom_id,student_email_and_token["email"].lower(),classroom_code)  
  courese_enrollment_mapping = create_student_enrollment_record(student_data=student_data,section=section)
  # course_enrollment_mapping = CourseEnrollmentMapping()
  # course_enrollment_mapping.role = "learner"
  # course_enrollment_mapping.section = section
  # course_enrollment_mapping.status ="active"
  # temp_user = TempUser.from_dict(student_data)
  # temp_user.user_id = ""
  # temp_user.save()
  # temp_user.user_id = temp_user.id
  # temp_user.update()
  # course_enrollment_mapping.user = temp_user.user_id
  # course_enrollment_mapping.save()
  context.enroll_student_data = {
    "section_id": section.id,
    "user_id":courese_enrollment_mapping["user_id"],
    "email": student_email_and_token["email"].lower(),
    "cohort_id":section.cohort.id,
    "access_token":student_email_and_token["access_token"]
    }
  print("Enroll student fixture cohort id",section.cohort.id)
  yield context.enroll_student_data

@fixture
def import_google_form_grade(context):
  section = use_fixture(create_section,context)
  a_creds = service_account.Credentials.from_service_account_info(
      CLASSROOM_KEY, scopes=SCOPES)
  creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
  service = build("classroom", "v1", credentials=creds)
  body={"title": "Test_quize",
      "description":"test desc",
      "workType": "ASSIGNMENT",
      "materials":[
    {"link":
      {"url": "https://docs.google.com/forms/d/1oZrH6Wc1TSMSQDwO17Y_TCf38Xdpw55PYRRVMMS0fBM/edit",
       "state": "PUBLISHED",
       }}
      ] }
  coursework = service.courses().courseWork().create(courseId=section.classroom_id,
                                                 body=body).execute()
  context.coursework_id = coursework.get("id")
  context.coursework = coursework
  classroom_code = section.classroom_code
  classroom_id = section.classroom_id
  student_email_and_token = get_student_email_and_token()
  student_data = enroll_student_classroom(student_email_and_token["access_token"],
  classroom_id,student_email_and_token["email"].lower(),classroom_code)  
  courese_enrollment_mapping = create_student_enrollment_record(student_data=student_data,section=section)
  print("IMport Grade fixture worked complete for section ,coursework_id",
        section.id,coursework.get("id"),section.classroom_code,student_data["email"])
  yield context.coursework

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

# @fixture
# def create_assignment_with_google_form(context):
#   """Create assignment fixture"""
#   section = use_fixture(create_section, context)
#   a_creds = service_account.Credentials.from_service_account_info(
#       CLASSROOM_KEY, scopes=SCOPES)
#   creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
#   service = build("classroom", "v1", credentials=creds)
#   result = service.courses().courseWork().create(courseId=section.classroom_id,
#                                                  body={
#                                                      "title": "Quize assignment",
#                                                      "description": "test desc",
#                                                      "workType": "ASSIGNMENT"
#                                                  }).execute()

#   result["section_id"] = section.id
#   context.assignment = result
#   yield context.assignment

@fixture
def create_analytics_data(context):
  """Create Analytics data"""
  print("Analytics data fixture")
  header=use_fixture(get_header,context)
  data={}
  section=use_fixture(create_section,context)
  res=requests.post(url=f'{API_URL}/sections/{section.id}/enable_notifications',
                    headers=header)
  res.raise_for_status()
  student_email_and_token = get_student_email_and_token()
  res=requests.post(url=f'{API_URL}/cohorts/{section.cohort.id}/students',
                    json=student_email_and_token,
                    headers=header)
  res.raise_for_status()
  resp=requests.get(headers=header,
url=f'{API_URL}/sections/{section.id}/students/{res.json()["data"]["student_email"]}')
  resp.raise_for_status()
  data["student_data"]=resp.json()["data"]
  data["course_details"]={
    "id":section.classroom_id,
    "name":section.name,
    "section":section.section
    }
  a_creds = service_account.Credentials.from_service_account_info(
      CLASSROOM_KEY, scopes=SCOPES)
  creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
  service = build("classroom", "v1", credentials=creds)
  result = service.courses().courseWork(
    ).create(courseId=section.classroom_id,
        body={
              "title": "test course work",
              "description": "test desc",
              "workType": "ASSIGNMENT",
              "state": "PUBLISHED",
               "maxPoints": 100,
               "associatedWithDeveloper": True
          }).execute()
  data["course_work"]=result
  context.analytics_data=data
  result_sub = service.courses().courseWork(
    ).studentSubmissions(
      ).list(courseId=result["courseId"],
        courseWorkId=result["id"],
        userId=data["student_data"]["gaia_id"]).execute()
  data["submission"]=result_sub["studentSubmissions"][0]
  # creds = Credentials(token=student_email_and_token["access_token"])
  # service = build("classroom", "v1", credentials=creds)
  service.courses().courseWork().studentSubmissions().patch(
        courseId=data["submission"]["courseId"],
        courseWorkId=data["submission"]["courseWorkId"],
        id=data["submission"]["id"],
        updateMask="assignedGrade,draftGrade",
        body={"assignedGrade":10,"draftGrade":10}).execute()
  yield context.analytics_data

def wait(secs):
  def decorator(func):
    def wrapper(*args, **kwargs):
      time.sleep(secs)
      return func(*args, **kwargs)
    return wrapper
  return decorator

@fixture
def invite_student(context):
  """Invite student fixture"""
  section = use_fixture(create_section, context)
  student_data = get_student_email_and_token()
  invitation_dict=invite_user(section.classroom_id ,
  student_data["invite_student_email"].lower(),
  "STUDENT")
  course_enrollment_mapping = CourseEnrollmentMapping()
  course_enrollment_mapping.role = "learner"
  course_enrollment_mapping.section = section
  course_enrollment_mapping.status ="invited"
  course_enrollment_mapping.invitation_id=invitation_dict["id"]
  temp_user = TempUser.from_dict(TEST_USER)

  temp_user.user_id = ""
  temp_user.email=student_data["invite_student_email"]
  temp_user.gaia_id = ""
  temp_user.photo_url = ""
  temp_user.save()
  temp_user.user_id = temp_user.id
  temp_user.update()
  course_enrollment_mapping.user = temp_user.user_id
  course_enrollment_id=course_enrollment_mapping.save().id
  context.invitation_data = {
    "section_id": section.id,
    "user_id":temp_user.id,
    "email": student_data["invite_student_email"].lower(),
    "cohort_id":section.cohort.id,
    "course_enrollment_id":course_enrollment_id,
    "invitation_id":invitation_dict["id"]
    }
  # ACcepting invite using student access token
  yield context.invitation_data

@fixture
def get_header(context):
  req = requests.post(f"{API_URL_AUTHENTICATION_SERVICE}/sign-in/credentials",
                      json=USER_EMAIL_PASSWORD_DICT,
                      timeout=60)
  res = req.json()
  if res is None or res["data"] is None:
    raise Exception("User sign-in failed")
  token = req.json()['data']['idToken']
  context.header={"Authorization": f"Bearer {token}"}
  yield context.header

fixture_registry = {
    "fixture.create.course_template": create_course_templates,
    "fixture.create.cohort": create_cohort,
    "fixture.create.section":create_section,
    "fixture.create.enroll_student_course":enroll_student_course,
    "fixture.get.header": get_header,
    "fixture.create.assignment": create_assignment,
    "fixture.invite.student": invite_student,
    "fixture.create.analytics.data":create_analytics_data,
    "fixture.import.google_form_grade":import_google_form_grade
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