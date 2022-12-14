"""
  Tests for User endpoints
"""
import os
import mock
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from common.models.section import Section
from common.models import CourseTemplate, Cohort
from common.testing.client_with_emulator import client_with_emulator
from common.testing.firestore_emulator import firestore_emulator, clean_firestore
from testing.test_config import BASE_URL
from schemas.schema_examples import COURSE_TEMPLATE_EXAMPLE, COHORT_EXAMPLE, CREDENTIAL_JSON

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"
SUCCESS_RESPONSE = {"status": "Success"}


def create_fake_data(course_template_id, cohort_id, section_id):
  """_summary_

  Args:
      course_template_id (_type_): _description_
      cohort_id (_type_): _description_
      section_id (_type_): _description_

  Returns:
      _type_: _description_
  """
  COURSE_TEMPLATE_EXAMPLE["uuid"] = course_template_id
  course_template = CourseTemplate.from_dict(COURSE_TEMPLATE_EXAMPLE)
  course_template.save()

  COHORT_EXAMPLE["uuid"] = cohort_id
  COHORT_EXAMPLE["course_template"] = course_template
  cohort = Cohort.from_dict(COHORT_EXAMPLE)
  cohort.save()

  test_section_dict = {
      "uuid": "fake-section-id",
      "name": "section_name",
      "section": "section c",
      "description": "description",
      "classroom_id": "cl_id",
      "classroom_code": "cl_code",
      "course_template": course_template,
      "cohort": cohort,
      "teachers_list": ["teachera@gmail.com", "teacherb@gmail.com"]
  }

  section = Section.from_dict(test_section_dict)
  section.save()
  return course_template, cohort, section


def test_get_user(client_with_emulator):
  url = BASE_URL + "/sections/get_courses/"
  with mock.patch("routes.copy_course.classroom_crud.get_course_list"):
    resp = client_with_emulator.get(url)
  assert resp.status_code == 200


def test_copy_course(client_with_emulator):
  url = BASE_URL + "/sections/copy_course/"
  course_details = {"course_id": "TEST123"}
  with mock.patch("routes.copy_course.classroom_crud.get_course_by_id"):
    with mock.patch("routes.copy_course.classroom_crud.create_course"):
      with mock.patch("routes.copy_course.classroom_crud.get_topics"):
        with mock.patch("routes.copy_course.classroom_crud.create_topics"):
          with mock.patch("routes.copy_course.classroom_crud.get_coursework"):
            with mock.patch(
                "routes.copy_course.classroom_crud.create_coursework"):
              resp = client_with_emulator.post(url, json=course_details)
  # json_response = json.loads(resp.text)
  assert resp.status_code == 200


def test_copy_course_not_found(client_with_emulator):
  url = BASE_URL + "/sections/copy_course/"
  course_details = {"course_id": "TEST123"}
  with mock.patch("routes.copy_course.classroom_crud.get_course_by_id",
                  return_value=None):
    with mock.patch("routes.copy_course.classroom_crud.create_course"):
      with mock.patch("routes.copy_course.classroom_crud.get_topics"):
        with mock.patch("routes.copy_course.classroom_crud.create_topics"):
          with mock.patch("routes.copy_course.classroom_crud.get_coursework"):
            with mock.patch(
                "routes.copy_course.classroom_crud.create_coursework"):
              resp = client_with_emulator.post(url, json=course_details)
  assert resp.status_code == 200


def test_create_section(client_with_emulator):

  create_fake_data("fake-classroom-id", "fake-cohort-id", "fake-section-id")
  url = BASE_URL + "/sections"
  section_details = {
      "name": "section_20",
      "description": "This is description",
      "course_template": "fake-classroom-id",
      "cohort": "fake-cohort-id",
      "teachers_list": [os.environ.get("CLASSROOM_ADMIN_EMAIL")]
  }
  mock_return_course = {
      "id": "57690009090",
      "enrollmentCode": "as3rr",
      "name": "Jhjiuiui"
  }
  with mock.patch("routes.copy_course.classroom_crud.get_course_by_id"):
    with mock.patch("routes.copy_course.classroom_crud.create_course",
                    return_value=mock_return_course):
      with mock.patch("routes.copy_course.classroom_crud.get_topics"):
        with mock.patch("routes.copy_course.classroom_crud.create_topics"):
          with mock.patch("routes.copy_course.classroom_crud.get_coursework"):
            with mock.patch(
                "routes.copy_course.classroom_crud.create_coursework"):
              with mock.patch("routes.copy_course.classroom_crud.add_teacher"):
                resp = client_with_emulator.post(url, json=section_details)
  # json_response = json.loads(resp.text)
  assert resp.status_code == 200


def test_create_section_course_template_not_found(client_with_emulator):

  # create_fake_data()
  url = BASE_URL + "/section"
  section_details = {
      "name": "section_20",
      "description": "This is description",
      "course_template": "fake-classroom-id_new",
      "cohort": "7888888",
      "teachers_list": ["string"]
  }
  mock_return_course = {
      "id": "57690009090",
      "enrollmentCode": "as3rr",
      "name": "Jhjiuiui"
  }
  with mock.patch("routes.copy_course.classroom_crud.get_course_by_id"):
    with mock.patch("routes.copy_course.classroom_crud.create_course",
                    return_value=mock_return_course):
      with mock.patch("routes.copy_course.classroom_crud.get_topics"):
        with mock.patch("routes.copy_course.classroom_crud.create_topics"):
          with mock.patch("routes.copy_course.classroom_crud.get_coursework"):
            with mock.patch(
                "routes.copy_course.classroom_crud.create_coursework"):
              resp = client_with_emulator.post(url, json=section_details)
  # json_response = json.loads(resp.text)
  assert resp.status_code == 404

  # create_fake_data()
  url = BASE_URL + "/sections"
  section_details = {
      "name": "section_20",
      "description": "This is description",
      "course_template": "fake-classroom-id_new",
      "cohort": "7888888",
      "teachers_list": ["string"]
  }
  mock_return_course = {
      "id": "57690009090",
      "enrollmentCode": "as3rr",
      "name": "Jhjiuiui"
  }
  with mock.patch("routes.copy_course.classroom_crud.get_course_by_id"):
    with mock.patch("routes.copy_course.classroom_crud.create_course",
                    return_value=mock_return_course):
      with mock.patch("routes.copy_course.classroom_crud.get_topics"):
        with mock.patch("routes.copy_course.classroom_crud.create_topics"):
          with mock.patch("routes.copy_course.classroom_crud.get_coursework"):
            with mock.patch(
                "routes.copy_course.classroom_crud.create_coursework"):
              resp = client_with_emulator.post(url, json=section_details)
  # json_response = json.loads(resp.text)
  assert resp.status_code == 404


def test_create_section_cohort_not_found(client_with_emulator):

  create_fake_data("fake-classroom-id", "fake-cohort-id", "fake-section-id")
  url = BASE_URL + "/sections"
  section_details = {
      "name": "section_20",
      "description": "This is description",
      "course_template": "fake-classroom-id",
      "cohort": "fake-cohort-id-new",
      "teachers_list": ["string"]
  }
  mock_return_course = {
      "id": "57690009090",
      "enrollmentCode": "as3rr",
      "name": "Jhjiuiui"
  }
  with mock.patch("routes.copy_course.classroom_crud.get_course_by_id"):
    with mock.patch("routes.copy_course.classroom_crud.create_course",
                    return_value=mock_return_course):
      with mock.patch("routes.copy_course.classroom_crud.get_topics"):
        with mock.patch("routes.copy_course.classroom_crud.create_topics"):
          with mock.patch("routes.copy_course.classroom_crud.get_coursework"):
            with mock.patch(
                "routes.copy_course.classroom_crud.create_coursework"):
              resp = client_with_emulator.post(url, json=section_details)
  # json_response = json.loads(resp.text)
  assert resp.status_code == 404


def test_list_section_for_one_cohort(client_with_emulator):

  create_fake_data("fake-classroom-id", "fake-cohort-id", "fake-section-id")
  url = BASE_URL + "/sections/cohort/fake-cohort-id/sections"
  resp = client_with_emulator.get(url)
  # json_response = resp.json()
  assert resp.status_code == 200


def test_list_section(client_with_emulator):

  create_fake_data("fake-classroom-id", "fake-cohort-id", "fake-section-id")
  url = BASE_URL + "/sections"
  resp = client_with_emulator.get(url)
  # json_response = resp.json()
  assert resp.status_code == 200


def test_list_section_cohort_not_found(client_with_emulator):

  create_fake_data("fake-classroom-id", "fake-cohort-id", "fake-section-id")
  url = BASE_URL + "/sections/cohort/fake-cohort-id22/sections"

  resp = client_with_emulator.get(url)
  # json_response = resp.json()

  assert resp.status_code == 404


def test_get_section(client_with_emulator):

  fake_data_result = create_fake_data("fake-classroom-id", "fake-cohort-id",
                                      "fake-section-id")
  url = BASE_URL + f"/sections/{fake_data_result[2].uuid}"

  resp = client_with_emulator.get(url)
  # json_response = resp.json()
  assert resp.status_code == 200


def test_get_section_not_found(client_with_emulator):

  create_fake_data("fake-classroom-id", "fake-cohort-id", "fake-section-id")
  url = BASE_URL + "/sections/test_case_id_does_not_exists"
  resp = client_with_emulator.get(url)
  # json_response = resp.json()

  assert resp.status_code == 404


def test_update_section(client_with_emulator):

  create_fake_data("fake-classroom-id", "fake-cohort-id", "fake-section-id")
  data = {
      "uuid": "fake-section-id",
      "course_id": "561822649300",
      "section_name": "tsection",
      "description": "tdescription",
      "course_state": "ACTIVEu"
  }
  url = BASE_URL + "/sections"
  with mock.patch("routes.copy_course.classroom_crud.update_course"):
    resp = client_with_emulator.patch(url, json=data)
  # json_response = resp.json()
  assert resp.status_code == 200


def test_update_section_section_id_not_found(client_with_emulator):

  create_fake_data("fake-classroom-id", "fake-cohort-id", "fake-section-id")

  data = {
      "uuid": "fake-section-id_new",
      "course_id": "561822649300",
      "section_name": "tsection",
      "description": "tdescription",
      "course_state": "ACTIVEu"
  }
  url = BASE_URL + "/sections"

  with mock.patch("routes.copy_course.classroom_crud.update_course"):
    resp = client_with_emulator.patch(url, json=data)
  # json_response = resp.json()
  assert resp.status_code == 404


def test_update_section_course_id_not_found(client_with_emulator):

  create_fake_data("fake-classroom-id", "fake-cohort-id", "fake-section-id")
  data = {
      "uuid": "fake-section-id_new",
      "course_id": "561822649300",
      "section_name": "tsection",
      "description": "tdescription",
      "course_state": "ACTIVEu"
  }
  url = BASE_URL + "/sections"
  with mock.patch("routes.copy_course.classroom_crud.update_course",
                  return_value=None):
    resp = client_with_emulator.patch(url, json=data)
  resp.json()
  assert resp.status_code == 404


def test_enroll_student(client_with_emulator):
  create_fake_data("fake-classroom-id", "fake-cohort-id", "fake-section-id")
  url = BASE_URL + "/sections/fake-section-id/students"
  input_data = {"email": "student@gmail.com", "credentials": CREDENTIAL_JSON}
  data = {
      "success": True,
      "message": "Successfully Added the Student with email student@gmail.com",
      "data": None
  }
  with mock.patch("routes.copy_course.classroom_crud.enroll_student"):
    with mock.patch("routes.copy_course.Logger"):
      resp = client_with_emulator.post(url, json=input_data)
  assert resp.status_code == 200, "Status 200"
  assert resp.json() == data, "Data doesn't Match"


def test_enroll_student_negative(client_with_emulator):
  url = BASE_URL + "/sections/fake_uuid_section/students"
  input_data = {"email": "student@gmail.com", "credentials": CREDENTIAL_JSON}
  with mock.patch("routes.copy_course.classroom_crud.enroll_student"):
    with mock.patch("routes.copy_course.Logger"):
      resp = client_with_emulator.post(url, json=input_data)

  assert resp.status_code == 404, "Status 404"
  assert resp.json()["success"] is False, "Check success"

def test_delete_section(client_with_emulator):

  create_fake_data("fake-classroom-id", "fake-cohort-id", "fake-section-id")
  data = {
      "uuid": "fake-section-id",
      "course_id": "561822649300",
      "section_name": "tsection",
      "description": "tdescription",
      "course_state": "ACTIVE"
  }
  url = BASE_URL + "/sections"
  with mock.patch("routes.copy_course.classroom_crud.delete_course_by_id"):
        resp = client_with_emulator.patch(url, json=data)
  assert resp.status_code == 200