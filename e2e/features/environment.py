"""
Behave setup environment file
"""
import datetime
import os
import json
import time
import requests
from behave import fixture, use_fixture
from common.models import (CourseTemplate, Cohort, Section, TempUser,
                           CourseEnrollmentMapping, User,
                           CourseTemplateEnrollmentMapping)
from common.testing.example_objects import TEST_SECTION, TEST_COHORT
from common.utils.bq_helper import insert_rows_to_bq
from testing_objects.test_config import API_URL_AUTHENTICATION_SERVICE, API_URL
from testing_objects.course_template import COURSE_TEMPLATE_INPUT_DATA
from testing_objects.user import TEST_USER
from testing_objects.bq_helper import BQ_DATASET, BQ_TABLE_DICT
from e2e.gke_api_tests.secrets_helper import (
    get_user_email_and_password_for_e2e, get_student_email_and_token,
    get_required_emails_from_secret_manager)
from e2e.gke_api_tests.classroom_e2e_helper import (
    create_course, get_course_work_submission_list, invite_user,
    patch_course_work_submission, create_course_work,
    enroll_teacher_in_classroom, enroll_student_classroom)
import logging

USER_EMAIL_PASSWORD_DICT = get_user_email_and_password_for_e2e()

EMAILS = get_required_emails_from_secret_manager()
TEACHER_EMAIL = EMAILS["teacher"]
CLASSROOM_KEY = json.loads(os.environ.get("GKE_POD_SA_KEY"))
CLASSROOM_ADMIN_EMAIL = os.environ.get("CLASSROOM_ADMIN_EMAIL")
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=missing-timeout,broad-exception-raised,broad-exception-caught,unused-argument


@fixture
def create_course_templates(context):
  """Fixture to create temporary data"""
  course_template = CourseTemplate.from_dict(COURSE_TEMPLATE_INPUT_DATA)
  classroom = create_course(course_template.name, "master",
                            course_template.description)
  course_template.classroom_id = classroom["id"]
  course_template.admin = CLASSROOM_ADMIN_EMAIL
  course_template.classroom_code = classroom["enrollmentCode"]
  course_template.classroom_url = classroom["alternateLink"]
  course_template.save()
  instructional_designer_email = EMAILS["instructional_designer"]
  profile_information = enroll_teacher_in_classroom(
      course_template.classroom_id, instructional_designer_email)
  temp_user = TempUser.find_by_email(instructional_designer_email)
  if temp_user is None:
    data = {
        "first_name": profile_information["name"]["givenName"],
        "last_name": profile_information["name"]["familyName"],
        "email": instructional_designer_email,
        "user_type": "faculty",
        "user_groups": [],
        "status": "active",
        "is_registered": True,
        "failed_login_attempts_count": 0,
        "access_api_docs": False,
        "gaia_id": profile_information["id"],
        "photo_url": profile_information["photoUrl"]
    }
    temp_user = TempUser.from_dict(data)
    temp_user.user_id = ""
    temp_user.save()
    temp_user.user_id = temp_user.id
    temp_user.update()
  course_enrollment_mapping = CourseTemplateEnrollmentMapping()
  course_enrollment_mapping.course_template = course_template
  course_enrollment_mapping.role = "faculty"
  course_enrollment_mapping.user = User.find_by_user_id(temp_user.user_id)
  course_enrollment_mapping.status = "active"
  course_enrollment_mapping.save()
  context.course_template = course_template
  yield context.course_template


@fixture
def enroll_instructional_designer(context):
  course_template = use_fixture(create_course_templates, context)
  user = User.find_by_email(EMAILS["instructional_designer"])
  enrollment_mapping=CourseTemplateEnrollmentMapping\
    .find_course_enrollment_record(
    course_template.key,
    user.user_id)
  context.enrollment_mapping = enrollment_mapping
  yield context.enrollment_mapping


@fixture
def create_cohort(context):
  """Fixture to create cohort temporary data"""
  cohort = Cohort.from_dict(TEST_COHORT)
  course_template = use_fixture(create_course_templates, context)
  cohort.course_template = course_template
  cohort.save()
  context.cohort = cohort
  yield context.cohort


@fixture
def create_section(context):
  """Fixture to create section temprorary data"""
  section = Section.from_dict(TEST_SECTION)
  cohort = use_fixture(create_cohort, context)
  section.course_template = cohort.course_template
  section.cohort = cohort
  context.course_name = cohort.course_template.name
  context.course_section = section.section
  context.course_description = section.description
  classroom = create_course(cohort.course_template.name, section.section,
                            section.description)
  section.classroom_id = classroom["id"]
  section.classroom_code = classroom["enrollmentCode"]
  section.classroom_url = classroom["alternateLink"]
  section.enrollment_status = "OPEN"
  section.max_students = 25
  section.status = "ACTIVE"
  section.save()
  # Create teachers in the DB
  instructional_designer_email=CourseTemplateEnrollmentMapping.\
    fetch_all_by_course_template(cohort.course_template.key)[0].user.email
  temp_user = TempUser.find_by_email(instructional_designer_email)
  if temp_user is None:
    temp_user = TempUser.from_dict(TEST_USER)
    temp_user.email = instructional_designer_email
    temp_user.user_type = "faculty"
    temp_user.first_name = instructional_designer_email.split("@")[0]
    temp_user.user_id = ""
    temp_user.save()
    temp_user.user_id = temp_user.id
    temp_user.update()
  course_enrollment_mapping = CourseEnrollmentMapping()
  course_enrollment_mapping.section = section
  course_enrollment_mapping.role = "faculty"
  course_enrollment_mapping.user = User.find_by_user_id(temp_user.user_id)
  course_enrollment_mapping.status = "active"
  course_enrollment_mapping.save()
  context.sections = section
  context.classroom_drive_folder_id = classroom["teacherFolder"]["id"]
  yield context.sections


def create_student_enrollment_record(student_data, section):
  course_enrollment_mapping = CourseEnrollmentMapping()
  course_enrollment_mapping.role = "learner"
  course_enrollment_mapping.section = section
  course_enrollment_mapping.status = "active"
  temp_user = TempUser.find_by_email(student_data["email"])
  if temp_user is None:
    print("Creating new user")
    temp_user = TempUser.from_dict(student_data)
    temp_user.user_id = ""
    temp_user.save()
    temp_user.user_id = temp_user.id
    temp_user.update()
  else:
    print(f"User already exist {temp_user.to_dict()}")
  course_enrollment_mapping.user = User.find_by_user_id(temp_user.user_id)
  course_enrollment_mapping.save()
  return {
      "user_id": temp_user.user_id,
      "course_enrollment_mapping_id": course_enrollment_mapping.id
  }


@fixture
def enroll_student_course(context):
  """Fixture to enroll studnet in course"""

  section = use_fixture(create_section, context)
  classroom_code = section.classroom_code
  classroom_id = section.classroom_id
  student_email_and_token = get_student_email_and_token()
  student_data = enroll_student_classroom(
      student_email_and_token["access_token"], classroom_id,
      student_email_and_token["email"].lower(), classroom_code)
  courese_enrollment_mapping = create_student_enrollment_record(
      student_data=student_data, section=section)
  context.enroll_student_data = {
      "section_id":
      section.id,
      "user_id":
      courese_enrollment_mapping["user_id"],
      "email":
      student_email_and_token["email"].lower(),
      "cohort_id":
      section.cohort.id,
      "access_token":
      student_email_and_token["access_token"],
      "course_enrollment_mapping_id":
      courese_enrollment_mapping["course_enrollment_mapping_id"]
  }
  return context.enroll_student_data


@fixture
def enroll_teacher_into_section(context):
  """fixture to enroll teacher to section"""
  section = use_fixture(create_section, context)
  teacher_email = TEACHER_EMAIL
  temp_user = TempUser.find_by_email(teacher_email)
  profile_information = enroll_teacher_in_classroom(section.classroom_id,
                                                    teacher_email)
  if temp_user is None:
    data = {
        "first_name": profile_information["name"]["givenName"],
        "last_name": profile_information["name"]["familyName"],
        "email": teacher_email,
        "user_type": "faculty",
        "user_groups": [],
        "status": "active",
        "is_registered": True,
        "failed_login_attempts_count": 0,
        "access_api_docs": False,
        "gaia_id": profile_information["id"],
        "photo_url": profile_information["photoUrl"]
    }
    temp_user = TempUser.from_dict(data)
    temp_user.user_id = ""
    temp_user.save()
    temp_user.user_id = temp_user.id
    temp_user.update()
  course_enrollment_mapping = CourseEnrollmentMapping()
  course_enrollment_mapping.section = section
  course_enrollment_mapping.role = "faculty"
  course_enrollment_mapping.user = User.find_by_user_id(temp_user.user_id)
  course_enrollment_mapping.status = "active"
  course_enrollment_mapping.save()
  context.enrollment_mapping = course_enrollment_mapping
  return context.enrollment_mapping


@fixture
def import_google_form_grade(context):
  "Fixture for import grade"
  section = use_fixture(create_section, context)
  coursework_body = {
      "title":
      "Test_quize11",
      "description":
      "test desc",
      "workType":
      "ASSIGNMENT",
      "materials": [{
          "link": {
              "title":
              "quize1 assignment",
              "url":
              "https://docs.google.com/forms/d/1oZrH6Wc1TSMSQDwO17Y_TCf38Xdpw55PYRRVMMS0fBM/edit"
          }
      }],
      "state":
      "PUBLISHED"
  }
  coursework = create_course_work(classroom_id=section.classroom_id,
                                  body=coursework_body)
  context.coursework_id = coursework.get("id")
  context.coursework = coursework
  context.section_id = section.id
  classroom_code = section.classroom_code
  classroom_id = section.classroom_id
  student_email_and_token = get_student_email_and_token()
  student_data = enroll_student_classroom(
      student_email_and_token["access_token"], classroom_id,
      student_email_and_token["email"].lower(), classroom_code)
  context.access_token = student_email_and_token["access_token"]
  context.student_email = student_email_and_token["email"].lower()
  context.classroom_id = classroom_id
  create_student_enrollment_record(student_data=student_data, section=section)
  yield context.coursework


@fixture
def create_assignment(context):
  """Create assignment fixture"""
  section = use_fixture(create_section, context)
  body = {
      "title": "test course work",
      "description": "test desc",
      "workType": "ASSIGNMENT"
  }
  result = create_course_work(classroom_id=section.classroom_id, body=body)
  result["section_id"] = section.id
  context.assignment = result
  yield context.assignment


@fixture
def create_analytics_data(context):
  """Create Analytics data"""
  header = use_fixture(get_header, context)
  data = {}
  section = use_fixture(create_section, context)
  res = requests.post(
      url=f"{API_URL}/sections/{section.id}/enable_notifications",
      headers=header)
  res.raise_for_status()
  student_email_and_token = get_student_email_and_token()
  print("In analytics fixturee__ student email and token value",
        student_email_and_token)
  res = requests.post(url=f"{API_URL}/cohorts/{section.cohort.id}/students",
                      json=student_email_and_token,
                      headers=header)
  print("Added student for cohort____", res.status_code)
  res.raise_for_status()
  resp = requests.get(
      headers=header,
      url=
      f'{API_URL}/sections/{section.id}/students/{res.json()["data"]["student_email"]}'
  )
  print("Added student for section____", resp.status_code)
  resp.raise_for_status()
  data["student_data"] = resp.json()["data"]
  data["course_details"] = {
      "id": section.classroom_id,
      "name": section.name,
      "section": section.section
  }
  print("Response of get student in section", data)
  body_data = {
      "title": "test course work",
      "description": "test desc",
      "workType": "ASSIGNMENT",
      "state": "PUBLISHED",
      "maxPoints": 100,
      "associatedWithDeveloper": True
  }
  result = create_course_work(classroom_id=section.classroom_id,
                              body=body_data)
  data["course_work"] = result
  context.analytics_data = data
  print("Contex value for analytics data set")
  result_sub = get_course_work_submission_list(
      classroom_id=result["courseId"],
      course_work_id=result["id"],
      user_id=data["student_data"]["gaia_id"])
  data["submission"] = result_sub["studentSubmissions"][0]
  patch_course_work_submission(
      classroom_id=data["submission"]["courseId"],
      course_work_id=data["submission"]["courseWorkId"],
      submission_id=data["submission"]["id"],
      update_mask="assignedGrade,draftGrade",
      body={
          "assignedGrade": 10,
          "draftGrade": 10
      })
  section_rows = [{
      "sectionId": section.id,
      "courseId": section.classroom_id,
      "classroomUrl": section.classroom_url,
      "name": section.section,
      "description": section.description,
      "status": section.status,
      "cohortId": section.cohort.id,
      "courseTemplateId": section.course_template.id,
      "timestamp": datetime.datetime.utcnow()
  }]
  cohort = section.cohort
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
  course_template = section.course_template
  instructional_designers = [
      i.user.email
      for i in CourseTemplateEnrollmentMapping.fetch_all_by_course_template(
          course_template.key)
  ]
  course_template_rows = [{
      "courseTemplateId": course_template.id,
      "classroomId": course_template.classroom_id,
      "name": course_template.name,
      "description": course_template.description,
      "timestamp": datetime.datetime.utcnow(),
      "instructionalDesigners": instructional_designers
  }]
  insert_rows_to_bq(rows=course_template_rows,
                    dataset=BQ_DATASET,
                    table_name=BQ_TABLE_DICT["BQ_COLL_COURSETEMPLATE_TABLE"])
  insert_rows_to_bq(rows=cohort_rows,
                    dataset=BQ_DATASET,
                    table_name=BQ_TABLE_DICT["BQ_COLL_COHORT_TABLE"])
  insert_rows_to_bq(rows=section_rows,
                    dataset=BQ_DATASET,
                    table_name=BQ_TABLE_DICT["BQ_COLL_SECTION_TABLE"])
  yield context.analytics_data


def wait(secs):
  """Wrapper funtion"""

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
  invitation_dict = invite_user(
      course_id=section.classroom_id,
      email=student_data["invite_student_email"].lower(),
      role="STUDENT")
  course_enrollment_mapping = CourseEnrollmentMapping()
  course_enrollment_mapping.role = "learner"
  course_enrollment_mapping.section = section
  course_enrollment_mapping.status = "invited"
  course_enrollment_mapping.invitation_id = invitation_dict["id"]
  temp_user = TempUser.find_by_email(
      student_data["invite_student_email"].lower())
  if temp_user is None:
    temp_user = TempUser.from_dict(TEST_USER)
    temp_user.user_id = ""
    temp_user.email = student_data["invite_student_email"]
    temp_user.gaia_id = ""
    temp_user.photo_url = ""
    temp_user.save()
    temp_user.user_id = temp_user.id
    temp_user.update()
  course_enrollment_mapping.user = User.find_by_user_id(temp_user.user_id)
  course_enrollment_id = course_enrollment_mapping.save().id
  context.invitation_data = {
      "section_id": section.id,
      "user_id": temp_user.id,
      "email": student_data["invite_student_email"].lower(),
      "cohort_id": section.cohort.id,
      "course_enrollment_id": course_enrollment_id,
      "invitation_id": invitation_dict["id"]
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
  token = req.json()["data"]["idToken"]
  context.header = {"Authorization": f"Bearer {token}"}
  yield context.header


fixture_registry = {
    "fixture.create.course_template": create_course_templates,
    "fixture.create.cohort": create_cohort,
    "fixture.create.section": create_section,
    "fixture.enroll.teacher.section": enroll_teacher_into_section,
    "fixture.enroll.instructional_designer.course_template":
    enroll_instructional_designer,
    "fixture.create.enroll_student_course": enroll_student_course,
    "fixture.get.header": get_header,
    "fixture.create.assignment": create_assignment,
    "fixture.invite.student": invite_student,
    "fixture.create.analytics.data": create_analytics_data,
    "fixture.import.google_form_grade": import_google_form_grade
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
    req = requests.post(
        f"{API_URL_AUTHENTICATION_SERVICE}/sign-up/credentials",
        json=USER_EMAIL_PASSWORD_DICT,
        timeout=40)
    if req.status_code != 200:
      if req.status_code == 422 and req.json().get(
          "message") == "EMAIL_EXISTS":
        print("signup: user email exists")
      else:
        raise Exception("User sign-up failed")
  else:
    print("firestore: user email already exists")


def before_all(context):
  sign_up_user()
