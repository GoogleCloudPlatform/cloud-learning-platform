import datetime
import os
import json
import time
import requests
from behave import fixture, use_fixture
from common.models import CourseTemplate, Cohort,Section, TempUser ,CourseEnrollmentMapping
from common.testing.example_objects import TEST_SECTION,TEST_COHORT
from common.utils.bq_helper import insert_rows_to_bq
from google.oauth2 import service_account
from googleapiclient.discovery import build
from e2e.test_config import API_URL_AUTHENTICATION_SERVICE,API_URL,e2e_google_form_id
from e2e.gke_api_tests.secrets_helper import get_user_email_and_password_for_e2e,\
  get_student_email_and_token,\
  get_required_emails_from_secret_manager,create_coursework\
  ,get_gmail_student_email_and_token

from e2e.utils.course_template import COURSE_TEMPLATE_INPUT_DATA
from e2e.utils.user import TEST_USER
from e2e.utils.bq_helper import BQ_DATASET,BQ_TABLE_DICT
from google.oauth2.credentials import Credentials
import logging

import os
import pandas as pd
import json
import traceback
from copy import copy, deepcopy
from behave import fixture, use_fixture
from common.utils.errors import ResourceNotFoundException
from common.utils.gcs_adapter import GcsCrudService

import sys
sys.path.append("..")
from e2e.setup import (GCP_BUCKET,CONTENT_SERVING_BUCKET, user_login)
from common.models import (Learner, Achievement, Goal, LearnerProfile, LearningResource)
from e2e.test_config import TESTING_OBJECTS_PATH
from e2e.test_object_schemas import (DOMAIN_OBJ_TEMPLATE, SUB_DOMAIN_OBJ_TEMPLATE,
  CATEGORY_OBJ_TEMPLATE, COMPETENCY_OBJ_TEMPLATE, LEARNING_OBJECTIVE_OBJ_TEMPLATE,
  LEARNING_CONTENT_OBJ_TEMPLATE, LEARNING_UNIT_OBJ_TEMPLATE, CONCEPT_OBJ_TEMPLATE,
  SUBCONCEPT_OBJ_TEMPLATE, SKILL_OBJ_TEMPLATE, LEARNING_RESOURCE_OBJ_TEMPLATE,
  DUMMY_BATCH_JOB_NAMES, BATCH_JOB_OBJ_TEMPLATE, TEST_KG_LEARNING_CONTENT,
  TEST_KG_CONCEPT, TEST_KG_SUBCONCEPT, TEST_KG_LEARNING_OBJECTIVE, TEST_KG_LEARNING_UNIT)


USER_EMAIL_PASSWORD_DICT = get_user_email_and_password_for_e2e()

EMAILS = get_required_emails_from_secret_manager()
TEACHER_EMAIL = EMAILS["teacher"]
CLASSROOM_KEY = os.environ.get("GKE_POD_SA_KEY")
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


TEST_E2E_SKILLS_PATH = os.path.join(TESTING_OBJECTS_PATH, "test_e2e_wgu_skills.csv")
TEST_DOMAINS_PATH = os.path.join(TESTING_OBJECTS_PATH, "test_e2e_domains.csv")
TEST_SUBDOMAINS_PATH = os.path.join(TESTING_OBJECTS_PATH, "test_e2e_subdomains.csv")
TEST_CATEGORIES_PATH = os.path.join(TESTING_OBJECTS_PATH, "test_e2e_categories.csv")
TEST_COMPETENCIES_PATH = os.path.join(TESTING_OBJECTS_PATH, "test_e2e_competencies.csv")
TEST_CONCEPTS_PATH = os.path.join(TESTING_OBJECTS_PATH, "test_e2e_concepts.csv")
TEST_SUBCONCEPTS_PATH = os.path.join(TESTING_OBJECTS_PATH, "test_e2e_subconcepts.csv")
TEST_LEARNING_OBJECTIVES_PATH = os.path.join(TESTING_OBJECTS_PATH, "test_e2e_learning_objectives.csv")
TEST_LEARNING_UNITS_PATH = os.path.join(TESTING_OBJECTS_PATH, "test_e2e_learning_units.csv")
TEST_LEARNING_RESOURCES_PATH = os.path.join(TESTING_OBJECTS_PATH, "test_e2e_learning_resources.csv")
TEST_LEARNING_CONTENTS_PATH = os.path.join(TESTING_OBJECTS_PATH, "test_e2e_learning_contents.csv")
TEST_DATA_SOURCE_PATH = os.path.join(TESTING_OBJECTS_PATH, "data_sources.json")
TEST_LP_PATH = os.path.join(TESTING_OBJECTS_PATH, "learner_profile.json")
TEST_ACHV_ACHIEVEMENT = os.path.join(TESTING_OBJECTS_PATH, "learner_achievement.json")
TEST_LEARNER_ACHIEVEMENT = os.path.join(TESTING_OBJECTS_PATH, "learner.json")
TEST_GOAL_PATH = os.path.join(TESTING_OBJECTS_PATH, "goals.json")

TEST_CSV_SKILLS_PATH = os.path.join(TESTING_OBJECTS_PATH, "generic_skill.csv")
TEST_INVALID_CSV_SKILLS_PATH = os.path.join(TESTING_OBJECTS_PATH, "invalid_generic_skill.csv")
TEST_CSV_COMPETENCIES_PATH = os.path.join(TESTING_OBJECTS_PATH, "generic_competency.csv")
TEST_INVALID_CSV_COMPETENCIES_PATH = os.path.join(TESTING_OBJECTS_PATH, "invalid_generic_competency.csv")
TEST_CSV_CATEGORIES_PATH = os.path.join(TESTING_OBJECTS_PATH, "generic_category.csv")
TEST_INVALID_CSV_CATEGORIES_PATH = os.path.join(TESTING_OBJECTS_PATH, "invalid_generic_category.csv")
TEST_CSV_SUBDOMAINS_PATH = os.path.join(TESTING_OBJECTS_PATH, "generic_sub_domain.csv")
TEST_INVALID_CSV_SUBDOMAINS_PATH = os.path.join(TESTING_OBJECTS_PATH, "invalid_generic_sub_domain.csv")
TEST_CSV_DOMAINS_PATH = os.path.join(TESTING_OBJECTS_PATH, "generic_domain.csv")
TEST_INVALID_CSV_DOMAINS_PATH = os.path.join(TESTING_OBJECTS_PATH, "invalid_generic_domain.csv")

TEST_LEARNING_HIERARCHY_PATH = os.path.join(TESTING_OBJECTS_PATH, "learning_hierarchy.json")
TEST_INVALID_LEARNING_HIERARCHY_PATH = os.path.join(TESTING_OBJECTS_PATH, "learning_hierarchy_invalid.json")
TEST_LEARNING_HIERARCHY_SIMPLIFIED_PATH = os.path.join(TESTING_OBJECTS_PATH, "learning_hierarchy_simplified.json")
TEST_LEARNING_HIERARCHY_FOR_SRL = os.path.join(TESTING_OBJECTS_PATH, "hierarchy_for_srl.json")
TEST_LEARNING_HIERARCHY_FOR_PROJECT = os.path.join(TESTING_OBJECTS_PATH, "learning_hierarchy_smaller.json")

TEST_CONTENT_SERVING_PATH = os.path.join(TESTING_OBJECTS_PATH, "content_serving.html")
TEST_CONTENT_SERVING_ZIP_PATH = os.path.join(TESTING_OBJECTS_PATH, "content_serving_sample_upload_scorm.zip")
TEST_CONTENT_SERVING_PDF_PATH = os.path.join(TESTING_OBJECTS_PATH, "content_serving_sample_upload_pdf.pdf")
TEST_CONTENT_SERVING_MADCAP_V1_PATH = os.path.join(TESTING_OBJECTS_PATH, "content_serving_sample_upload_madcap_v1.zip")
TEST_CONTENT_SERVING_MADCAP_V2_PATH = os.path.join(TESTING_OBJECTS_PATH, "content_serving_sample_upload_madcap_v2.zip")
TEST_CONTENT_SERVING_SRL_V1_PATH = os.path.join(TESTING_OBJECTS_PATH, "SRL_content_serving_valid.zip")
TEST_CONTENT_SERVING_SRL_V2_PATH = os.path.join(TESTING_OBJECTS_PATH, "SRL_content_serving_v2_valid.zip")
TEST_CONTENT_SERVING_SRL_V3_PATH = os.path.join(TESTING_OBJECTS_PATH, "SRL_content_serving_v3_invalid.zip")

TEST_ASSESSMENT_SUBMISSION_FILE_PATH = os.path.join(TESTING_OBJECTS_PATH, "sample_assessment_submission.txt")

TEST_USER_MANAGEMENT_PATH = os.path.join(TESTING_OBJECTS_PATH, "user_management_student_list.json")

def create_course(name,section,description):
  """Create course Function in classroom

  Args: course_name ,description of course, section,owner_id of course
  Returns:
    new created course details
    """""
  a_creds = service_account.Credentials.from_service_account_file(
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
  a_creds = service_account.Credentials.from_service_account_file(
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
  temp_user=TempUser.find_by_email(TEST_SECTION["teachers"][0])
  if temp_user is None:
    print("Creating new teacher",TEST_SECTION["teachers"][0])
    temp_user = TempUser.from_dict(TEST_USER)
    temp_user.user_type = "faculty"
    temp_user.email =TEST_SECTION["teachers"][0]
    temp_user.first_name = TEST_SECTION["teachers"][0].split("@")[0]
    temp_user.user_id = ""
    temp_user.save()
    temp_user.user_id = temp_user.id
    temp_user.update()
  else:
    print("Teachera already present in db")
  temp_user1 = TempUser.find_by_email(TEST_SECTION["teachers"][1])
  if temp_user1 is None:
    print("Creating a new teacher",TEST_SECTION["teachers"][1])
    temp_user1 = TempUser.from_dict(TEST_USER)
    temp_user1.first_name = TEST_SECTION["teachers"][1].split("@")[0]
    temp_user1.email = TEST_SECTION["teachers"][1]
    temp_user1.user_type = "faculty"
    temp_user1.user_id = ""
    temp_user1.save()
    temp_user1.user_id = temp_user.id
    temp_user1.update()
  else:
    print("Tecaher teaherb already present in db")
  context.sections=section
  context.classroom_drive_folder_id =classroom["teacherFolder"]["id"]
  yield context.sections

def create_student_enrollment_record(student_data,section):
  course_enrollment_mapping = CourseEnrollmentMapping()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
  course_enrollment_mapping.role = "learner"
  course_enrollment_mapping.section = section
  course_enrollment_mapping.status ="active"
  temp_user=TempUser.find_by_email(student_data["email"])
  if temp_user is None:
    print("Creating new user")
    temp_user = TempUser.from_dict(student_data)
    temp_user.user_id = ""
    temp_user.save()
    temp_user.user_id = temp_user.id
    temp_user.update()
  else:
    print(f"User already exist {temp_user.to_dict()}")
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
  context.enroll_student_data = {
    "section_id": section.id,
    "user_id":courese_enrollment_mapping["user_id"],
    "email": student_email_and_token["email"].lower(),
    "cohort_id":section.cohort.id,
    "access_token":student_email_and_token["access_token"],
    "course_enrollment_mapping_id":courese_enrollment_mapping["course_enrollment_mapping_id"]
    }
  return context.enroll_student_data

@fixture
def import_google_form_grade(context):
  "Fixture for import grade"
  section = use_fixture(create_section, context)
  # folder_id = context.classroom_drive_folder_id
  # result =insert_file_into_folder(folder_id,e2e_google_form_id)
  # print("Inserted in classroom folder",result)
  coursework_body = {"title": "Test_quize11",
      "description":"test desc",
      "workType": "ASSIGNMENT",
      "materials":[
    {"link":
      {
        "title": "quize1 assignment",
        "url": "https://docs.google.com/forms/d/1oZrH6Wc1TSMSQDwO17Y_TCf38Xdpw55PYRRVMMS0fBM/edit"
       }}
      ],
      "state":"PUBLISHED"}
  coursework = create_coursework(section.classroom_id,coursework_body)
  context.coursework_id = coursework.get("id")
  context.coursework = coursework
  context.section_id = section.id
  classroom_code = section.classroom_code
  classroom_id = section.classroom_id
  student_email_and_token = get_gmail_student_email_and_token()
  student_data = enroll_student_classroom(student_email_and_token["access_token"],
  classroom_id,student_email_and_token["email"].lower(),classroom_code) 
  context.access_token = student_email_and_token["access_token"]
  context.student_email =student_email_and_token["email"].lower() 
  context.classroom_id = classroom_id 
  courese_enrollment_mapping = create_student_enrollment_record(student_data=student_data,section=section)
  yield context.coursework

@fixture
def create_assignment(context):
  """Create assignment fixture"""
  section = use_fixture(create_section, context)
  a_creds = service_account.Credentials.from_service_account_file(
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
def create_analytics_data(context):
  """Create Analytics data"""
  header=use_fixture(get_header,context)
  data={}
  section=use_fixture(create_section,context)
  res=requests.post(url=f'{API_URL}/sections/{section.id}/enable_notifications',
                    headers=header)
  res.raise_for_status()
  student_email_and_token = get_student_email_and_token()
  print("In analytics fixturee__ student email and token value",student_email_and_token)
  res=requests.post(url=f'{API_URL}/cohorts/{section.cohort.id}/students',
                    json=student_email_and_token,
                    headers=header)
  print("Added student for cohort____",res.status_code)
  res.raise_for_status()
  resp=requests.get(headers=header,
url=f'{API_URL}/sections/{section.id}/students/{res.json()["data"]["student_email"]}')
  print("Added student for section____",resp.status_code)
  resp.raise_for_status()
  data["student_data"]=resp.json()["data"]
  data["course_details"]={
    "id":section.classroom_id,
    "name":section.name,
    "section":section.section
    }
  print("REsponse of get student in section",data)
  a_creds = service_account.Credentials.from_service_account_file(
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
  print("Contex value for analytics data set")
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
  section_rows=[{
      "sectionId":section.id,
      "courseId":section.classroom_id,
      "classroomUrl":section.classroom_url,
      "name":section.section,
      "description":section.description,
      "cohortId":section.cohort.id,
      "courseTemplateId":section.course_template.id,
      "timestamp":datetime.datetime.utcnow()
    }]
  cohort=section.cohort
  cohort_rows=[{
      "cohortId":cohort.id,
      "name":cohort.name,
      "description":cohort.description,\
      "startDate":cohort.start_date,\
      "endDate":cohort.end_date,
      "registrationStartDate":cohort.registration_start_date,
      "registrationEndDate":cohort.registration_end_date,
      "maxStudents":cohort.max_students,
      "timestamp":datetime.datetime.utcnow()
    }]
  course_template=section.course_template
  course_template_rows=[{
      "courseTemplateId":course_template.id,
      "classroomId":course_template.classroom_id,
        "name":course_template.name,
        "description":course_template.description,
        "timestamp":datetime.datetime.utcnow(),
        "instructionalDesigner":course_template.instructional_designer
    }]
  insert_rows_to_bq(
      rows=course_template_rows,
      dataset=BQ_DATASET,
      table_name=BQ_TABLE_DICT["BQ_COLL_COURSETEMPLATE_TABLE"]
      )
  insert_rows_to_bq(
      rows=cohort_rows,
      dataset=BQ_DATASET,
      table_name=BQ_TABLE_DICT["BQ_COLL_COHORT_TABLE"]
      )
  insert_rows_to_bq(
      rows=section_rows,
      dataset=BQ_DATASET,
      table_name=BQ_TABLE_DICT["BQ_COLL_SECTION_TABLE"]
      )
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
  temp_user = TempUser.find_by_email(student_data["invite_student_email"])
  if temp_user is None:
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

# @fixture
# def setup_skills(context):
#   test_skills = pd.read_csv(TEST_E2E_SKILLS_PATH)
#   test_skills["description"] = test_skills["description"].fillna("")
#   id = 0
#   for _, row in test_skills.iterrows():
#     skill_dict = copy(SKILL_OBJ_TEMPLATE)
#     skill_dict["id"] = row["id"]
#     skill_dict["name"] = row["name"]
#     skill_dict["description"] = row["description"]
#     skill_dict["reference_id"] = row["id"]
#     skill_dict["uuid"] = row["id"]
#     if id == 10:
#       skill_dict["source_name"] = "snhu"
#       skill_dict["source_uri"] = f"https://snhu/resources/{row['id']}"
#     else:
#       skill_dict["source_name"] = "e2e_wgu"
#       skill_dict["source_uri"] = f"https://wgu/resources/{row['id']}"
#     skill = Skill.from_dict(skill_dict)
#     skill.save()
#     id+=1
#   yield

# @fixture
# def setup_competencies(context):
#   test_competencies = pd.read_csv(TEST_COMPETENCIES_PATH)
#   test_competencies["description"] = test_competencies["description"].fillna("")
#   for _, row in test_competencies.iterrows():
#     competency_dict = copy(COMPETENCY_OBJ_TEMPLATE)
#     competency_dict["id"] = row["id"]
#     competency_dict["name"] = row["name"]
#     competency_dict["description"] = row["description"]
#     competency_dict["reference_id"] = row["id"]
#     competency_dict["uuid"] = row["id"]
#     competency_dict["source_name"] = "snhu"
#     competency_dict["source_uri"] = f"https://snhu/resources/{row['id']}"
#     competency = SkillServiceCompetency.from_dict(competency_dict)
#     competency.save()
#   yield

# @fixture
# def setup_categories(context):
#   test_categories = pd.read_csv(TEST_CATEGORIES_PATH)
#   test_categories["description"] = test_categories["description"].fillna("")
#   for _, row in test_categories.iterrows():
#     category_dict = copy(CATEGORY_OBJ_TEMPLATE)
#     category_dict["id"] = row["id"]
#     category_dict["name"] = row["name"]
#     category_dict["description"] = row["description"]
#     category_dict["reference_id"] = row["id"]
#     category_dict["uuid"] = row["id"]
#     category_dict["source_name"] = "snhu"
#     category_dict["source_uri"] = f"https://snhu/resources/{row['id']}"
#     category = Category.from_dict(category_dict)
#     category.save()
#   yield

# @fixture
# def setup_subdomains(context):
#   test_subdomains = pd.read_csv(TEST_SUBDOMAINS_PATH)
#   test_subdomains["description"] = test_subdomains["description"].fillna("")
#   for _, row in test_subdomains.iterrows():
#     subdomain_dict = copy(SUB_DOMAIN_OBJ_TEMPLATE)
#     subdomain_dict["id"] = row["id"]
#     subdomain_dict["name"] = row["name"]
#     subdomain_dict["description"] = row["description"]
#     subdomain_dict["reference_id"] = row["id"]
#     subdomain_dict["uuid"] = row["id"]
#     subdomain_dict["source_name"] = "snhu"
#     subdomain_dict["source_uri"] = f"https://snhu/resources/{row['id']}"
#     subdomain = SubDomain.from_dict(subdomain_dict)
#     subdomain.save()
#   yield

# @fixture
# def setup_domains(context):
#   test_domains = pd.read_csv(TEST_DOMAINS_PATH)
#   test_domains["description"] = test_domains["description"].fillna("")
#   for _, row in test_domains.iterrows():
#     domain_dict = copy(DOMAIN_OBJ_TEMPLATE)
#     domain_dict["id"] = row["id"]
#     domain_dict["name"] = row["name"]
#     domain_dict["description"] = row["description"]
#     domain_dict["reference_id"] = row["id"]
#     domain_dict["uuid"] = row["id"]
#     domain_dict["source_name"] = "snhu"
#     domain_dict["source_uri"] = f"https://snhu/resources/{row['id']}"
#     domain = Domain.from_dict(domain_dict)
#     domain.save()
#   yield

# @fixture
# def setup_concepts(context):
#   test_concepts = pd.read_csv(TEST_CONCEPTS_PATH)
#   test_concepts["description"] = test_concepts["description"].fillna("")
#   for _, row in test_concepts.iterrows():
#     concept_dict = copy(CONCEPT_OBJ_TEMPLATE)
#     concept_dict["id"] = row["id"]
#     concept_dict["title"] = row["title"]
#     concept_dict["description"] = row["description"]
#     concept_dict["uuid"] = row["id"]
#     concept = Concept.from_dict(concept_dict)
#     concept.save()
#   yield

# @fixture
# def setup_subconcepts(context):
#   test_subconcepts = pd.read_csv(TEST_SUBCONCEPTS_PATH)
#   test_subconcepts["description"] = test_subconcepts["description"].fillna("")
#   for _, row in test_subconcepts.iterrows():
#     subconcept_dict = copy(SUBCONCEPT_OBJ_TEMPLATE)
#     subconcept_dict["id"] = row["id"]
#     subconcept_dict["title"] = row["title"]
#     subconcept_dict["description"] = row["description"]
#     subconcept_dict["uuid"] = row["id"]
#     subconcept = SubConcept.from_dict(subconcept_dict)
#     subconcept.save()
#   yield

# @fixture
# def setup_learning_objectives(context):
#   test_learning_objectives = pd.read_csv(TEST_LEARNING_OBJECTIVES_PATH)
#   test_learning_objectives["description"] = test_learning_objectives["description"].fillna("")
#   for _, row in test_learning_objectives.iterrows():
#     learning_objective_dict = copy(LEARNING_OBJECTIVE_OBJ_TEMPLATE)
#     learning_objective_dict["id"] = row["id"]
#     learning_objective_dict["title"] = row["title"]
#     learning_objective_dict["description"] = row["description"]
#     learning_objective_dict["uuid"] = row["id"]
#     learning_objective = KnowledgeServiceLearningObjective.from_dict(learning_objective_dict)
#     learning_objective.save()
#   yield

# @fixture
# def setup_learning_units(context):
#   test_learning_units = pd.read_csv(TEST_LEARNING_UNITS_PATH)
#   test_learning_units["text"] = test_learning_units["text"].fillna("")
#   for _, row in test_learning_units.iterrows():
#     learning_unit_dict = copy(LEARNING_UNIT_OBJ_TEMPLATE)
#     learning_unit_dict["id"] = row["id"]
#     learning_unit_dict["title"] = row["title"]
#     learning_unit_dict["description"] = row["text"]
#     learning_unit_dict["uuid"] = row["id"]
#     learning_unit = KnowledgeServiceLearningUnit.from_dict(learning_unit_dict)
#     learning_unit.save()
#   yield

# def setup_batch_jobs(context):
#   job_doc_ids = []
#   for name in DUMMY_BATCH_JOB_NAMES:
#     batch_job_dict = copy(BATCH_JOB_OBJ_TEMPLATE)
#     batch_job_dict["name"] = name
#     batch_job_dict["uuid"] = name
#     batch_job = BatchJobModel.from_dict(batch_job_dict)
#     batch_job.save()
#     job_doc_ids.append(batch_job.id)
#   yield

# @fixture
# def setup_learning_contents(context):
#   test_learning_contents = pd.read_csv(TEST_LEARNING_CONTENTS_PATH)
#   test_learning_contents["description"] = test_learning_contents["description"].fillna("")
#   for _, row in test_learning_contents.iterrows():
#     learning_content_dict = copy(LEARNING_CONTENT_OBJ_TEMPLATE)
#     learning_content_dict["id"] = row["id"]
#     learning_content_dict["title"] = row["title"]
#     learning_content_dict["description"] = row["description"]
#     learning_content_dict["uuid"] = row["id"]
#     learning_content = KnowledgeServiceLearningContent.from_dict(learning_content_dict)
#     learning_content.save()
#   yield

# def upsert_data_source(type, new_object):
#   try:
#     existing_source = DataSource.find_by_type(type)
#     source_fields = existing_source.get_fields()
#     source_list = list(set(source_fields["source"]+new_object["source"]))
#     source_matching_engine_ids = source_fields["matching_engine_index_id"]
#     source_matching_engine_ids.update(new_object["matching_engine_index_id"])
#     setattr(existing_source, "source", source_list)
#     setattr(existing_source, "matching_engine_index_id", source_matching_engine_ids)
#     existing_source.update()
#   except ResourceNotFoundException:
#     data_source = DataSource.from_dict(new_object)
#     data_source.save()

# @fixture
# def setup_data_sources(context):
#   f = open(TEST_DATA_SOURCE_PATH)
#   data = json.load(f)
#   for object in data:
#     upsert_data_source(object["type"], object)


# @fixture
# def setup_skill_graph(context):
#   #add test domain
#   test_domain_dict = deepcopy(DOMAIN_OBJ_TEMPLATE)
#   test_domain_dict["uuid"] = ""
#   test_domain_dict["name"] = "Test Random Domain"
#   test_domain = Domain()
#   test_domain = test_domain.from_dict(test_domain_dict)
#   test_domain.save()
#   test_domain.uuid = test_domain.id
#   test_domain.update()
#   context.domain_id = test_domain.id

#   #add test sub-domain
#   test_sub_domain_dict = deepcopy(SUB_DOMAIN_OBJ_TEMPLATE)
#   test_sub_domain_dict["uuid"] = ""
#   test_sub_domain_dict["name"] = "Test Random Sub-Domain"
#   test_sub_domain_dict["parent_nodes"] = {"domains": [test_domain.id]}
#   test_sub_domain = SubDomain.from_dict(test_sub_domain_dict)
#   test_sub_domain.save()
#   test_domain.child_nodes = {"sub_domains": [test_sub_domain.id]}
#   test_domain.update()
#   test_sub_domain.uuid = test_sub_domain.id
#   test_sub_domain.update()
#   context.sub_domain_id = test_sub_domain.id

#   #add test category
#   test_category_dict = deepcopy(CATEGORY_OBJ_TEMPLATE)
#   test_category_dict["uuid"] = ""
#   test_category_dict["name"] = "Test Random Category"
#   test_category_dict["parent_nodes"] = {"sub_domains": [test_sub_domain.id]}
#   test_category = Category.from_dict(test_category_dict)
#   test_category.save()
#   test_sub_domain.child_nodes = {
#         "categories": [test_category.id],
#         "competencies": []
#     }
#   test_sub_domain.update()
#   test_category.uuid = test_category.id
#   test_category.update()
#   context.category_id = test_category.id

#   #add test competency
#   test_competency_dict = deepcopy(COMPETENCY_OBJ_TEMPLATE)
#   test_competency_dict["uuid"] = ""
#   test_competency_dict["name"] = "Test Random Competency"
#   test_competency_dict["parent_nodes"] = {
#     "sub_domains": [],
#     "categories": [test_category.id]
#     }
#   test_competency = SkillServiceCompetency.from_dict(test_competency_dict)
#   test_competency.save()
#   test_category.child_nodes = {"competencies": [test_competency.id]}
#   test_category.update()
#   test_competency.uuid = test_competency.id
#   test_competency.update()
#   context.competency_id = test_competency.id

#   #add test skill
#   test_skill_dict = deepcopy(SKILL_OBJ_TEMPLATE)
#   test_skill_dict["uuid"] = ""
#   test_skill_dict["name"] = "Test Random Skill"
#   test_skill_dict["source_name"] = "Credentialengine"
#   test_skill_dict["parent_nodes"] = {"competencies": [test_competency.id]}
#   test_skill = Skill.from_dict(test_skill_dict)
#   test_skill.save()
#   test_competency.child_nodes = {"skills": [test_skill.id]}
#   test_competency.update()
#   test_skill.uuid = test_skill.id
#   test_skill.update()
#   context.skill_id = test_skill.id


# @fixture
# def setup_knowledge_graph(context):
#   #add test learning resource
#   test_learning_resource = KnowledgeServiceLearningContent()
#   test_learning_resource = test_learning_resource.from_dict(TEST_KG_LEARNING_CONTENT)
#   test_learning_resource.save()
#   test_learning_resource.uuid = test_learning_resource.id
#   test_learning_resource.update()

#   #add test concept
#   test_concept = Concept.from_dict(TEST_KG_CONCEPT)
#   test_concept.parent_nodes["learning_resource"] = [test_learning_resource.uuid]
#   test_concept.save()
#   test_concept.uuid = test_concept.id
#   test_concept.update()
  
#   test_learning_resource.child_nodes["concepts"] = [test_concept.id]
#   test_learning_resource.update()

#   #add test sub-concept
#   test_subconcept = SubConcept.from_dict(TEST_KG_SUBCONCEPT)
#   test_subconcept.parent_nodes["concepts"] = [test_concept.id]
#   test_subconcept.save()
#   test_subconcept.uuid = test_subconcept.id
#   test_subconcept.update()

#   test_concept.child_nodes["sub_concepts"] = [test_subconcept.uuid]
#   test_concept.update()

#   #add test learning objective
#   test_learning_objective = KnowledgeServiceLearningObjective.from_dict(TEST_KG_LEARNING_OBJECTIVE)
#   test_learning_objective.parent_nodes["sub_concepts"] = [test_subconcept.id]
#   test_learning_objective.save()
#   test_learning_objective.uuid = test_learning_objective.id
#   test_learning_objective.update()

#   test_subconcept.child_nodes["learning_objectives"] = [test_learning_objective.uuid]
#   test_subconcept.update()

#   #add test learning units
#   test_learning_unit = KnowledgeServiceLearningUnit.from_dict(TEST_KG_LEARNING_UNIT)
#   test_learning_unit.parent_nodes["learning_objectives"] = [test_learning_objective.id]
#   test_learning_unit.save()
#   test_learning_unit.uuid = test_learning_unit.id
#   test_learning_unit.update()

#   test_learning_objective.child_nodes["learning_units"] = [test_learning_unit.uuid]

#   context.learning_resource_id = test_learning_resource.id

# @fixture
# def setup_gcs_skill_graph(context):
#   context.gcs_object = GcsCrudService(GCP_BUCKET)
#   context.skill_uri = context.gcs_object.upload_file_to_bucket(
#                                     "dev_testing/testing-files",
#                                     "generic_skill.csv", TEST_CSV_SKILLS_PATH)
#   context.invalid_skill_uri = context.gcs_object.upload_file_to_bucket(
#                                     "dev_testing/testing-files",
#                                     "invalid_generic_skill.csv",
#                                     TEST_INVALID_CSV_SKILLS_PATH)
#   context.competency_uri = context.gcs_object.upload_file_to_bucket(
#                                          "dev_testing/testing-files",
#                                          "generic_competency.csv",
#                                          TEST_CSV_COMPETENCIES_PATH)
#   context.invalid_competency_uri = context.gcs_object.upload_file_to_bucket(
#                                          "dev_testing/testing-files",
#                                          "invalid_generic_competency.csv",
#                                          TEST_INVALID_CSV_COMPETENCIES_PATH)
#   context.category_uri = context.gcs_object.upload_file_to_bucket(
#                                        "dev_testing/testing-files",
#                                        "generic_category.csv",
#                                        TEST_CSV_CATEGORIES_PATH)
#   context.invalid_category_uri = context.gcs_object.upload_file_to_bucket(
#                                        "dev_testing/testing-files",
#                                        "invalid_generic_category.csv",
#                                        TEST_INVALID_CSV_CATEGORIES_PATH)
#   context.sub_domain_uri = context.gcs_object.upload_file_to_bucket(
#                                          "dev_testing/testing-files",
#                                          "generic_sub_domain.csv",
#                                          TEST_CSV_SUBDOMAINS_PATH)
#   context.invalid_sub_domain_uri = context.gcs_object.upload_file_to_bucket(
#                                          "dev_testing/testing-files",
#                                          "invalid_generic_sub_domain.csv",
#                                          TEST_INVALID_CSV_SUBDOMAINS_PATH)
#   context.domain_uri = context.gcs_object.upload_file_to_bucket(
#                                      "dev_testing/testing-files",
#                                      "generic_domain.csv",
#                                      TEST_CSV_DOMAINS_PATH)
#   context.invalid_domain_uri = context.gcs_object.upload_file_to_bucket(
#                                      "dev_testing/testing-files",
#                                      "invalid_generic_domain.csv",
#                                      TEST_INVALID_CSV_DOMAINS_PATH)

# # setup for learner-profile-service

# @fixture
# def setup_lp(context):
#   fileObject = open(TEST_LP_PATH, "r")
#   jsonContent = fileObject.read()
#   aList = json.loads(jsonContent)
#   ids = []
#   for lp_dict in aList:
#     lp = LearnerProfile.from_dict(lp_dict)
#     lp.save()
#     ids.append(lp.id) 
#   yield

# @fixture
# def setup_achievement(context):
#   fileObject = open(TEST_ACHV_ACHIEVEMENT, "r")
#   jsonContent = fileObject.read()
#   acList = json.loads(jsonContent)
#   ids = []
#   for achv_dict in acList:
#     achv = Achievement.from_dict(achv_dict)
#     achv.save()
#     ids.append(achv.id)
#   yield

# @fixture
# def setup_learner(context):
#   fileObject = open(TEST_LEARNER_ACHIEVEMENT, "r")
#   jsonContent = fileObject.read()
#   lList = json.loads(jsonContent)
#   ids = []
#   for learner_dict in lList:
#     learner = Learner.from_dict(learner_dict)
#     learner.save()
#     ids.append(learner.id)
#   yield

# @fixture
# def setup_goals(context):
#   fileObject = open(TEST_GOAL_PATH, "r")
#   jsonContent = fileObject.read()
#   glist = json.loads(jsonContent)
#   ids = []
#   for goal_dict in glist:
#     goal = Goal.from_dict(goal_dict)
#     goal.save()
#     ids.append(goal.id)
#   yield

# #set up for LOS
# @fixture
# def setup_learning_resources(context):
#   test_learning_resources = pd.read_csv(TEST_LEARNING_RESOURCES_PATH)
#   test_learning_resources["description"] = test_learning_resources["description"].fillna("")
#   for _, row in test_learning_resources.iterrows():
#     learning_resource_dict = copy(LEARNING_RESOURCE_OBJ_TEMPLATE)
#     learning_resource_dict["id"] = row["id"]
#     learning_resource_dict["name"] = row["name"]
#     learning_resource_dict["description"] = row["description"]
#     learning_resource_dict["uuid"] = row["id"]
#     learning_resource = LearningResource.from_dict(learning_resource_dict)
#     learning_resource.save()
#   yield

def after_all(context):
  pass


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
  #sign_up_user()
  pass


# def before_all(context):
#   try:
#     user_login()
#     use_fixture(setup_skills, context)
#     use_fixture(setup_competencies, context)
#     use_fixture(setup_categories, context)
#     use_fixture(setup_subdomains, context)
#     use_fixture(setup_domains, context)
#     use_fixture(setup_concepts, context)
#     use_fixture(setup_subconcepts, context)
#     use_fixture(setup_learning_objectives, context)
#     use_fixture(setup_learning_units, context)
#     use_fixture(setup_batch_jobs, context)
#     use_fixture(setup_learning_contents, context)
#     use_fixture(setup_skill_graph, context)
#     use_fixture(setup_knowledge_graph, context)
#     use_fixture(setup_data_sources,context)
#     use_fixture(setup_gcs_skill_graph, context)
#     use_fixture(setup_lp, context)
#     use_fixture(setup_achievement, context)
#     use_fixture(setup_learner, context)
#     use_fixture(setup_goals, context)
#   except Exception as e:
#     print("Failed in before_all hook with error:", str(e))
#     print(traceback.print_exc())
#     sys.exit(1)