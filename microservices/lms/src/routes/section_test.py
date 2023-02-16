"""
  Tests for User endpoints
"""
import os
import mock
import pytest
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
  return {
      "cohort": cohort.id,
      "course_template": course_template.id,
      "section": section.id
  }


def test_get_user(client_with_emulator):
  url = BASE_URL + "/sections/get_courses/"
  with mock.patch("routes.section.classroom_crud.get_course_list"):
    resp = client_with_emulator.get(url)
  assert resp.status_code == 200

mocked_value = {"id":"123456789","name":{"givenName":"user1",
    "familyName":"last_name"},"photoUrl":"http://mockurl.com"}

def test_copy_course(client_with_emulator):
  url = BASE_URL + "/sections/copy_course/"
  course_details = {"course_id": "TEST123"}
  with mock.patch("routes.section.classroom_crud.get_course_by_id"):
    with mock.patch("routes.section.classroom_crud.create_course"):
      with mock.patch("routes.section.classroom_crud.get_topics"):
        with mock.patch("routes.section.classroom_crud.create_topics"):
          with mock.patch("routes.section.classroom_crud.get_coursework"):
            with mock.patch(
                "routes.section.classroom_crud.create_coursework"):
              resp = client_with_emulator.post(url, json=course_details)
  assert resp.status_code == 200


def test_copy_course_not_found(client_with_emulator):
  url = BASE_URL + "/sections/copy_course/"
  course_details = {"course_id": "TEST123"}
  with mock.patch("routes.section.classroom_crud.get_course_by_id",
                  return_value=None):
    with mock.patch("routes.section.classroom_crud.create_course"):
      with mock.patch("routes.section.classroom_crud.get_topics"):
        with mock.patch("routes.section.classroom_crud.create_topics"):
          with mock.patch("routes.section.classroom_crud.get_coursework"):
            with mock.patch(
                "routes.section.classroom_crud.create_coursework"):
              resp = client_with_emulator.post(url, json=course_details)
  assert resp.status_code == 200


def test_create_section(client_with_emulator, create_fake_data):
  url = BASE_URL + "/sections"
  section_details = {
      "name": "section_20",
      "description": "This is description",
      "course_template": create_fake_data["course_template"],
      "cohort": create_fake_data["cohort"],
      "teachers": ["teachera@gmail.com"]
  }
  mock_return_course = {
      "id": "57690009090",
      "enrollmentCode": "as3rr",
      "name": "Jhjiuiui",
      "alternateLink": "https://classroom.google.com"
  }

  with mock.patch("routes.section.classroom_crud.get_course_by_id"):
    with mock.patch("routes.section.classroom_crud.create_course",
                    return_value=mock_return_course):
      with mock.patch("routes.section.classroom_crud.get_topics"):
        with mock.patch("routes.section.classroom_crud.create_topics"):
          with mock.patch("routes.section.classroom_crud.get_coursework"):
            with mock.patch(
                "routes.section.classroom_crud.create_coursework"):
              with mock.patch("routes.section.classroom_crud.add_teacher"):
                
                with mock.patch(
                    "routes.section.classroom_crud.delete_teacher"):
                  with mock.patch(
                    "routes.section.classroom_crud.enable_notifications"):
                    with mock.patch(
                  "routes.section.classroom_crud.invite_teacher",
                    return_value={"id":"12wewew"}):
                      with mock.patch(
              "routes.section.classroom_crud.get_user_profile_information",
                        return_value=mocked_value):
                        with mock.patch(
                "routes.section.classroom_crud.acceept_invite"):
                          with mock.patch(
                      "routes.section.common_service.create_teacher"):
                            with mock.patch(
                    "routes.section.classroom_crud.get_coursework_material"):
                              with mock.patch(
                    "routes.section.classroom_crud.create_coursework_material"):
                                resp = client_with_emulator.post(url,
                              json=section_details)
  assert resp.status_code == 200


def test_create_section_course_template_not_found(client_with_emulator,
                                                  create_fake_data):

  url = BASE_URL + "/section"
  section_details = {
      "name": "section_20",
      "description": "This is description",
      "course_template": "fake-classroom-id_new",
      "cohort": create_fake_data["cohort"],
      "teachers": ["teachera@gmail.com"]
  }
  mock_return_course = {
      "id": "57690009090",
      "enrollmentCode": "as3rr",
      "name": "Jhjiuiui",
      "alternateLink": "https://classroom.google.com"
  }
  with mock.patch("routes.section.classroom_crud.get_course_by_id"):
    with mock.patch("routes.section.classroom_crud.create_course",
                    return_value=mock_return_course):
      with mock.patch("routes.section.classroom_crud.get_topics"):
        with mock.patch("routes.section.classroom_crud.create_topics"):
          with mock.patch("routes.section.classroom_crud.get_coursework"):
            with mock.patch(
                "routes.section.classroom_crud.create_coursework"):
              with mock.patch("routes.section.classroom_crud.invite_teacher"):
                with mock.patch(
                "routes.section.classroom_crud.get_user_profile_information",
                return_value=mocked_value):
                  with mock.patch(
              "routes.section.classroom_crud.acceept_invite"):
                    with mock.patch(
            "routes.section.common_service.create_teacher"):
                      with mock.patch(
            "routes.section.classroom_crud.get_coursework_material"):
                        with mock.patch(
            "routes.section.classroom_crud.create_coursework_material"):
                          resp = client_with_emulator.post(url,
                      json=section_details)
  assert resp.status_code == 404


def test_create_section_cohort_not_found(client_with_emulator,
                                         create_fake_data):

  url = BASE_URL + "/sections"
  section_details = {
      "name": "section_20",
      "description": "This is description",
      "course_template": create_fake_data["course_template"],
      "cohort": "fake-cohort-id-new",
      "teachers": ["teachera@gmail.com"]
  }
  mock_return_course = {
      "id": "57690009090",
      "enrollmentCode": "as3rr",
      "name": "Jhjiuiui",
      "alternateLink": "https://classroom.google.com"
  }
  mocked_value = {"id":"123456789","name":{"givenName":"user1",
    "familyName":"last_name"},"photoUrl":"http://mockurl.com"}
  with mock.patch("routes.section.classroom_crud.get_course_by_id"):
    with mock.patch("routes.section.classroom_crud.create_course",
                    return_value=mock_return_course):
      with mock.patch("routes.section.classroom_crud.get_topics"):
        with mock.patch("routes.section.classroom_crud.create_topics"):
          with mock.patch("routes.section.classroom_crud.get_coursework"):
            with mock.patch(
                "routes.section.classroom_crud.create_coursework"):
              with mock.patch("routes.section.classroom_crud.acceept_invite"):
                with mock.patch(
        "routes.section.classroom_crud.get_user_profile_information",
                return_value=mocked_value):
                  with mock.patch(
        "routes.section.classroom_crud.invite_teacher"):
                    with mock.patch(
        "routes.section.common_service.create_teacher"):
                      with mock.patch(
              "routes.section.classroom_crud.get_coursework_material"):
                        with mock.patch(
                "routes.section.classroom_crud.create_coursework_material"):
                          resp = client_with_emulator.post(url,
                      json=section_details)
  assert resp.status_code == 404


def test_list_section(client_with_emulator, create_fake_data):

  url = BASE_URL + "/sections"
  resp = client_with_emulator.get(url)
  assert resp.status_code == 200


def test_list_section_validation_error(client_with_emulator, create_fake_data):

  url = BASE_URL + "/sections?skip=-1&limit=10"
  resp = client_with_emulator.get(url)
  assert resp.status_code == 422


def test_get_section(client_with_emulator, create_fake_data):

  url = BASE_URL + f"/sections/{create_fake_data['section']}"

  resp = client_with_emulator.get(url)
  assert resp.status_code == 200


def test_get_section_not_found(client_with_emulator):

  url = BASE_URL + "/sections/test_case_id_does_not_exists"
  resp = client_with_emulator.get(url)
  assert resp.status_code == 404


def test_update_section(client_with_emulator, create_fake_data):

  section = Section.find_by_id(create_fake_data["section"])
  data = {
      "id": create_fake_data["section"],
      "course_id": "561822649300",
      "section_name": "tsection",
      "description": "tdescription",
      "teachers": section.teachers
  }
  url = BASE_URL + "/sections"
  with mock.patch("routes.section.classroom_crud.update_course"):
    with mock.patch("routes.section.classroom_crud.acceept_invite"):
      with mock.patch(
    "routes.section.classroom_crud.get_user_profile_information",
      return_value=mocked_value):
        with mock.patch("routes.section.classroom_crud.acceept_invite"):
          with mock.patch("routes.section.common_service.create_teacher"):
            resp = client_with_emulator.patch(url, json=data)
  assert resp.status_code == 200


def test_update_section_section_id_not_found(client_with_emulator):

  data = {
      "id": "fake-section-id_new",
      "course_id": "561822649300",
      "section_name": "tsection",
      "description": "tdescription",
      "teachers": ["teachera@gmail.com", "teacherb@gmail.com"]
  }
  url = BASE_URL + "/sections"

  with mock.patch("routes.section.classroom_crud.update_course"):
    with mock.patch("routes.section.classroom_crud.acceept_invite"):
      with mock.patch(
        "routes.section.classroom_crud.get_user_profile_information",
      return_value=mocked_value):
        with mock.patch("routes.section.classroom_crud.acceept_invite"):
          with mock.patch("routes.section.common_service.create_teacher"):
            resp = client_with_emulator.patch(url, json=data)
  assert resp.status_code == 404


def test_update_section_course_id_not_found(client_with_emulator,
                                            create_fake_data):

  data = {
      "id": create_fake_data["section"],
      "course_id": "561822649300",
      "section_name": "tsection",
      "description": "tdescription",
      "teachers": ["teachera@gmail.com", "teacherb@gmail.com"]
  }
  url = BASE_URL + "/sections"
  with mock.patch("routes.section.classroom_crud.update_course",
                  return_value=None):
    resp = client_with_emulator.patch(url, json=data)
  resp.json()
  assert resp.status_code == 404




def test_delete_section(client_with_emulator, create_fake_data):

  url = BASE_URL + f"/sections/{create_fake_data['section']}"
  with mock.patch("routes.section.classroom_crud.update_course_state",
                  return_value=[]):
    resp = client_with_emulator.delete(url)
  assert resp.status_code == 200


def test_enable_notifications_using_course_id(client_with_emulator):

  url = BASE_URL + "/sections/enable_notifications"
  input_data = {"course_id": "57690009090", "feed_type": "COURSE_WORK_CHANGES"}
  data = {
      "success": True,
      "message":
      "Successfully enable the notifications of the course using " +
      f"{input_data['course_id']} id",
      "data": {
          "registrationId": "2345667",
          "feed": {
              "feedType": "COURSE_ROSTER_CHANGES",
              "courseRosterChangesInfo": {
                  "courseId": input_data["course_id"]
              }
          },
          "expiryTime": "20xx-0x-x0T1x:xx:0x.x1xZ"
      }
  }
  with mock.patch("routes.section.classroom_crud.enable_notifications",
                  return_value=data["data"]):
    with mock.patch("routes.section.Logger"):
      resp = client_with_emulator.post(url, json=input_data)
  assert resp.status_code == 200, "Status 200"
  assert resp.json() == data, "Data doesn't Match"


def test_enable_notifications_using_section_id(client_with_emulator,
                                               create_fake_data):

  url = BASE_URL + "/sections/enable_notifications"
  input_data = {"section_id": create_fake_data["section"],
  "feed_type": "COURSE_WORK_CHANGES"}
  section=Section.find_by_id(create_fake_data["section"])
  data = {
      "success":
      True,
      "message":
      "Successfully enable the notifications of the course using section " +
      f"{section.id} id",
      "data": {
          "registrationId": "2345667",
          "feed": {
              "feedType": "COURSE_ROSTER_CHANGES",
              "courseRosterChangesInfo": {
                  "courseId": section.classroom_id
              }
          },
          "expiryTime": "20xx-0x-x0T1x:xx:0x.x1xZ"
      }
  }
  with mock.patch("routes.section.classroom_crud.enable_notifications",
                  return_value=data["data"]):
    with mock.patch("routes.section.Logger"):
      resp = client_with_emulator.post(url, json=input_data)
  assert resp.status_code == 200, "Status 200"
  assert resp.json() == data, "Data doesn't Match"


def test_enable_notifications_using_fake_section_id(client_with_emulator):

  url = BASE_URL + "/sections/enable_notifications"
  input_data = {"section_id": "fake_section_id",
    "feed_type": "COURSE_WORK_CHANGES"}
  with mock.patch("routes.section.classroom_crud.enable_notifications"):
    with mock.patch("routes.section.Logger"):
      resp = client_with_emulator.post(url, json=input_data)
  assert resp.status_code == 404, "Status 404"
  assert resp.json()["success"] is False, "Data doesn't Match"

def test_negative_enable_notifications(client_with_emulator):
  url = BASE_URL + "/sections/enable_notifications"
  input_data = {"section_id": "", "feed_type": "COURSE_WORK_CHANGES"}
  with mock.patch("routes.section.classroom_crud.enable_notifications"):
    with mock.patch("routes.section.Logger"):
      resp = client_with_emulator.post(url, json=input_data)
  assert resp.status_code==422,"Status 422"
  assert resp.json()["success"] is False, "Data doesn't Match"
