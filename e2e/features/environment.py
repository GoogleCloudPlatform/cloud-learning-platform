import os
import json
import traceback
from behave import fixture, use_fixture
from common.models import CourseTemplate, Cohort,Section
from common.testing.example_objects import TEST_SECTION,TEST_COHORT
from google.oauth2 import service_account
from googleapiclient.discovery import build
from testing_objects.course_template import COURSE_TEMPLATE_INPUT_DATA
from testing_objects.cohort import COHORT_INPUT_DATA
import logging
from setup import user_login

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
    course_template.uuid = course_template.id
    course_template.update()
    context.course_template=course_template
    yield context.course_template

@fixture
def create_cohort(context):
    """Fixture to create cohort temporary data"""
    cohort=Cohort.from_dict(TEST_COHORT)
    course_template=use_fixture(create_course_templates,context)
    cohort.course_template=course_template
    cohort.save()
    cohort.uuid=cohort.id
    cohort.update()
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
    section.save()
    section.uuid=section.id
    section.update()
    context.sections=section
    yield context.sections

fixture_registry = {
    "fixture.create.course_template": create_course_templates,
    "fixture.create.cohort": create_cohort,
    "fixture.create.section":create_section
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

def before_all(context):
  try:
    user_login()
  except Exception as e:
    print("Failed in before_all hook with error:", str(e))
    print(traceback.print_exc())
