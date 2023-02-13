"""
  Tests for User endpoints
"""
import os
import mock
import pytest

# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from common.testing.client_with_emulator import client_with_emulator
from common.testing.firestore_emulator import firestore_emulator, clean_firestore
from common.models import CourseTemplate, Cohort ,TempUser,CourseEnrollmentMapping,Section
from testing.test_config import BASE_URL
from schemas.schema_examples import COURSE_TEMPLATE_EXAMPLE,\
   COHORT_EXAMPLE, TEMP_USER
from config import USER_MANAGEMENT_BASE_URL




os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"
SUCCESS_RESPONSE = {"status": "Success"}


@pytest.fixture
def create_fake_data():
  """_summary_

  Args:
      course_template_id (_type_): _description_
      cohort_id (_type_): _description_
      section_id (_type_): _description_

  Returns:
      _type_: _description_
  """
  course_template = CourseTemplate.from_dict(COURSE_TEMPLATE_EXAMPLE)
  course_template.save()
  COHORT_EXAMPLE["course_template"] = course_template
  cohort = Cohort.from_dict(COHORT_EXAMPLE)
  cohort.save()

  test_section_dict = {
      "name": "section_name",
      "section": "section c",
      "description": "description",
      "classroom_id": "cl_id",
      "classroom_code": "cl_code",
      "classroom_url": "https://classroom.google.com",
      "course_template": course_template,
      "cohort": cohort,
      "teachers": ["teachera@gmail.com", "teacherb@gmail.com"]
  }

  section = Section.from_dict(test_section_dict)
  section.save()
  temp_user = TempUser.from_dict(TEMP_USER)
  temp_user.user_id = ""
  temp_user.save()
  temp_user.user_id = temp_user.id
  temp_user.update()
  user_id = temp_user.user_id

  course_enrollment_mapping= CourseEnrollmentMapping()
  course_enrollment_mapping.role = "learner"
  course_enrollment_mapping.user = user_id
  course_enrollment_mapping.section = section
  course_enrollment_mapping.status = "active"
  course_enrollment_mapping.save()


  return {
      "cohort": cohort.id,
      "course_template": course_template.id,
      "section": section.id,
      "user_id":user_id
  }


def test_get_student_course_progress_percent(client_with_emulator):
  url = BASE_URL + "/student/get_progress_percentage/" + \
    "?course_id=504551481098&student_email=test_user_1@dhodun.altostrat.com"

  with mock.patch("routes.student.classroom_crud.get_course_work_list",
                  return_value=[{}, {}]):
    with mock.patch(
        "routes.student.classroom_crud.get_submitted_course_work_list",
        return_value=[{
            "state": "TURNED_IN"
        }, {
            "state": "TURNED_IN"
        }]):
      resp = client_with_emulator.get(url)
  assert resp.status_code == 200


def test_list_student_of_section(client_with_emulator):
  url = BASE_URL + "/sections/5/students"

  with mock.patch("routes.student.classroom_crud.list_student_section",
                  return_value=[{}, {}]):
    resp = client_with_emulator.get(url)
  assert resp.status_code == 200

def test_delete_student_from_section(client_with_emulator,create_fake_data):
  user_id = create_fake_data["user_id"]
  section_id = create_fake_data["section"]
  url = BASE_URL + f"/sections/{section_id}/students/{user_id}"
  with mock.patch("routes.student.classroom_crud.delete_student",
                  return_value=[{}, {}]):
    with mock.patch("routes.student.classroom_crud.get_user_details",
                  return_value={"data":{"email":"clplmstestuser1@gmail.com"}}):
      resp = client_with_emulator.delete(url)
  assert resp.status_code == 200

def test_delete_student_sectionid_not_found\
(client_with_emulator,create_fake_data):
  user_id = create_fake_data["user_id"]
  section_id = "test_section_id"
  # url = BASE_URL + f"/student/{user_id}/section/{section_id}"
  url = BASE_URL + f"/sections/{section_id}/students/{user_id}"
  with mock.patch("routes.student.classroom_crud.delete_student",
                  return_value=[{}, {}]):
    with mock.patch("routes.student.classroom_crud.get_user_details",
                  return_value={"data":{"email":"clplmstestuser1@gmail.com"}}):
      resp = client_with_emulator.delete(url)
  assert resp.status_code == 404
