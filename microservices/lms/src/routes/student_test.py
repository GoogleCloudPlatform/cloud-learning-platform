"""
  Tests for User endpoints
"""
import os
import mock
import pytest
import datetime

# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from common.testing.client_with_emulator import client_with_emulator
from common.testing.firestore_emulator import firestore_emulator, clean_firestore
from common.models import CourseTemplate, Cohort ,TempUser,CourseEnrollmentMapping,Section
from testing.test_config import BASE_URL
from schemas.schema_examples import COURSE_TEMPLATE_EXAMPLE,\
   COHORT_EXAMPLE, TEMP_USER,CREDENTIAL_JSON
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

def test_enroll_student_negative(client_with_emulator):
  url = BASE_URL + "/cohorts/fake_id_cohort/students"
  input_data = {
      "email": "student@gmail.com",
      "access_token": CREDENTIAL_JSON["token"]
  }
  with mock.patch("routes.section.classroom_crud.enroll_student"):
    with mock.patch("routes.section.Logger"):
      resp = client_with_emulator.post(url, json=input_data)

  assert resp.status_code == 404, "Status 404"
  assert resp.json()["success"] is False, "Check success"

def test_enroll_student(client_with_emulator, create_fake_data):

  url = BASE_URL + f"/cohorts/{create_fake_data['cohort']}/students"
  input_data = {
      "email": "student@gmail.com",
      "access_token": CREDENTIAL_JSON["token"]
  }
  with mock.patch("routes.section.classroom_crud.enroll_student",
  return_value ={"user_id":"test_user_id"}):
    with mock.patch("routes.section.Logger"):
      resp = client_with_emulator.post(url, json=input_data)
  assert resp.status_code == 200, "Status 200"
  assert resp.json()["success"] is True

def test_get_assignment(client_with_emulator,create_fake_data):
  url = BASE_URL + \
      f"/sections/{create_fake_data['section']}/assignments/5789246"
  course_work_data = {
      "courseId": "555555555",
      "id": "5789246",
      "title": "test assignment",
      "state": "PUBLISHED",
      "alternateLink": "https://classroom.google.com/xyz",
      "creationTime": "2023-02-16T10:45:49.833Z",
      "updateTime": "2023-02-16T10:46:06.699Z",
      "dueDate": {
          "year": 2023,
          "month": 2,
          "day": 28
      },
      "dueTime": {
          "hours": 18,
          "minutes": 29
      },
      "maxPoints": 100,
      "workType": "ASSIGNMENT",
      "assigneeMode": "ALL_STUDENTS",
  }
  with mock.patch("routes.section.classroom_crud.get_course_work",
                  return_value=course_work_data):
    resp=client_with_emulator.get(url)
  data=resp.json()
  assert resp.status_code==200,"Status 200"
  assert data["id"] == course_work_data["id"], "Data id doesn't Match"
  assert data["classroom_id"] == course_work_data[
    "courseId"], "Data course id doesn't Match"
  assert data["description"] is None, "Data description doesn't Match"
  assert datetime.date.fromisoformat(data["due_date"])== datetime.date(
    year=course_work_data["dueDate"]["year"],
    month=course_work_data["dueDate"]["month"],
    day=course_work_data["dueDate"]["day"]),"Data due date doesn't Match"


def test_negative_get_assignment(client_with_emulator, create_fake_data):
  url = BASE_URL + \
      "/sections/fake_id/assignments/5789246"
  course_work_data = {
      "courseId": "555555555",
      "id": "5789246",
      "title": "test assignment",
      "state": "PUBLISHED",
      "alternateLink": "https://classroom.google.com/xyz",
      "creationTime": "2023-02-16T10:45:49.833Z",
      "updateTime": "2023-02-16T10:46:06.699Z",
      "dueDate": {
          "year": 2023,
          "month": 2,
          "day": 28
      },
      "dueTime": {
          "hours": 18,
          "minutes": 29
      },
      "maxPoints": 100,
      "workType": "ASSIGNMENT",
      "assigneeMode": "ALL_STUDENTS",
  }
  with mock.patch("routes.section.classroom_crud.get_course_work",
                  return_value=course_work_data):
    resp = client_with_emulator.get(url)
  data = resp.json()
  assert resp.status_code == 404, "Status 404"
  assert data["success"] is False, "Data doesn't Match"