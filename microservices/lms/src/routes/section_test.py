"""
  Tests for Section endpoints
"""
import os
import mock
import pytest
import datetime
from unittest.mock import Mock
from requests.models import Response
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from common.models.section import Section
from common.models import CourseTemplate, Cohort
from common.testing.client_with_emulator import client_with_emulator
from common.testing.firestore_emulator import firestore_emulator, clean_firestore
from testing.test_config import (BASE_URL,
      LIST_COURSEWORK_SUBMISSION_USER,FORM_RESPONSE_LIST,
      GET_COURSEWORK_DATA,EDIT_VIEW_URL_FILE_ID_MAPPING_FORM)
from schemas.schema_examples import COURSE_TEMPLATE_EXAMPLE,\
   COHORT_EXAMPLE, CREDENTIAL_JSON,TEMP_USER

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


mocked_value = {"id":"123456789","name":{"givenName":"user1",
    "familyName":"last_name"},"photoUrl":"http://mockurl.com"}


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
      "name": "test_section",
      "alternateLink": "https://classroom.google.com",
      "teacherFolder": {
    "id": "18iPGzsRSp2LcQqHEvMaEZoraV37UaVkE-L0MhnDnKKyIaGKtK",
    "title": "test_section",
    "alternateLink": "https://drive.google.com/drive/folders/18iPGzsRSp2LcQqH" }
  }

  with mock.patch("routes.section.classroom_crud.get_course_by_id"):
    with mock.patch("services.section_service.classroom_crud.create_course",
                    return_value=mock_return_course):
      with mock.patch(
      "services.section_service.classroom_crud.get_topics"):
        with mock.patch(
          "services.section_service.classroom_crud.create_topics"):
          with mock.patch(
        "services.section_service.classroom_crud.get_coursework_list"):
            with mock.patch(
                "services.section_service.classroom_crud.create_coursework"):
              with mock.patch(
        "services.section_service.classroom_crud.add_teacher"):
                with mock.patch(
                    "services.section_service.classroom_crud.delete_teacher"):
                  with mock.patch(
            "services.section_service.classroom_crud.enable_notifications"):
                    with mock.patch(
                  "services.section_service.classroom_crud.invite_user",
                    return_value={"id":"12wewew"}):
                      with mock.patch(
      "services.section_service.classroom_crud.get_user_profile_information",
                        return_value=mocked_value):
                        with mock.patch(
                "services.section_service.classroom_crud.acceept_invite"):
                          with mock.patch(
                      "services.section_service.common_service.create_teacher"):
                            with mock.patch(
      "services.section_service.classroom_crud.get_coursework_material_list"):
                              with mock.patch(
          "services.section_service.classroom_crud.create_coursework_material"):
                                with mock.patch(
                      "services.section_service.classroom_crud.drive_copy"):
                                  with mock.patch(
                      "services.section_service.classroom_crud.copy_material"):
                                    with mock.patch(
                        "services.section_service.insert_rows_to_bq"):
                                      resp = client_with_emulator.post(url,
                              json=section_details)
  assert resp.status_code == 202


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
          with mock.patch("routes.section.classroom_crud.get_coursework_list"):
            with mock.patch(
                "routes.section.classroom_crud.create_coursework"):
              with mock.patch("routes.section.classroom_crud.invite_user"):
                with mock.patch(
                "routes.section.classroom_crud.get_user_profile_information",
                return_value=mocked_value):
                  with mock.patch(
              "routes.section.classroom_crud.acceept_invite"):
                    with mock.patch(
            "routes.section.common_service.create_teacher"):
                      with mock.patch(
            "routes.section.classroom_crud.get_coursework_material_list"):
                        with mock.patch(
            "routes.section.classroom_crud.create_coursework_material"):
                          with mock.patch(
                      "routes.section.classroom_crud.drive_copy"):
                            with mock.patch(
                      "routes.section.classroom_crud.copy_material"):
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
          with mock.patch("routes.section.classroom_crud.get_coursework_list"):
            with mock.patch(
                "routes.section.classroom_crud.create_coursework"):
              with mock.patch("routes.section.classroom_crud.acceept_invite"):
                with mock.patch(
        "routes.section.classroom_crud.get_user_profile_information",
                return_value=mocked_value):
                  with mock.patch(
        "routes.section.classroom_crud.invite_user"):
                    with mock.patch(
        "routes.section.common_service.create_teacher"):
                      with mock.patch(
              "routes.section.classroom_crud.get_coursework_material_list"):
                        with mock.patch(
                "routes.section.classroom_crud.create_coursework_material"):
                          with mock.patch(
                      "routes.section.classroom_crud.drive_copy"):
                            with mock.patch(
                      "routes.section.classroom_crud.copy_material"):
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
            with mock.patch("routes.section.insert_rows_to_bq"):
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

def test_update_section_classroom_code(client_with_emulator, create_fake_data):
  section = Section.find_by_id(create_fake_data["section"])
  url = BASE_URL + f"/sections/{section.id}/update_classroom_code"
  with mock.patch("routes.section.Logger"):
    with mock.patch("routes.section.classroom_crud.get_course_by_id",
                    return_value={"enrollmentCode":"xyz123z"}):
      resp = client_with_emulator.patch(url)
  assert resp.status_code == 200
  assert resp.json()["data"]["classroom_code"] == "xyz123z"

def test_negative_update_section_classroom_code(client_with_emulator):
  url = BASE_URL + "/sections/xyz/update_classroom_code"
  with mock.patch("routes.section.Logger"):
    with mock.patch("routes.section.classroom_crud.get_course_by_id",
                    return_value={"enrollmentCode":"xyz123z"}):
      resp = client_with_emulator.patch(url)
  assert resp.status_code == 404

def test_list_teachers(client_with_emulator,create_fake_data):


  section_id =  create_fake_data["section"]
  url = BASE_URL + f"/sections/{section_id}"
  with mock.patch("routes.section.common_service.call_search_user_api",
  return_value=TEMP_USER):
    resp = client_with_emulator.get(url)
  assert resp.status_code == 200
  assert resp.json()["success"] is True

def test_get_teacher(client_with_emulator,create_fake_data):
  user_api_response={
  "success": True,
  "message": "Success",
  "data": [TEMP_USER]}
  section_id =  create_fake_data["section"]
  url = BASE_URL + f"/sections/{section_id}/teachers/teachera@gmail.com"
  the_response = Mock(spec=Response)
  the_response.json.return_value = user_api_response
  the_response.status_code = 200
  with mock.patch(
    "routes.section.common_service.call_search_user_api",
    return_value=the_response)  :
    # mock_request.return_value.status_code = 200
    # mock_request.return_value = str(user_api_response)
    resp = client_with_emulator.get(url)
    print("Get User response___",resp)
  assert resp.status_code == 200

def test_delete_section(client_with_emulator, create_fake_data):

  url = BASE_URL + f"/sections/{create_fake_data['section']}"
  with mock.patch("routes.section.classroom_crud.update_course_state",
                  return_value=[]):
    resp = client_with_emulator.delete(url)
  assert resp.status_code == 200


def test_enable_notifications_using_section_id(client_with_emulator,
                                               create_fake_data):
  section_id = create_fake_data["section"]
  url=f"{BASE_URL}/sections/{section_id}/enable_notifications"
  section=Section.find_by_id(section_id)
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
      resp = client_with_emulator.post(url)
  assert resp.status_code == 200, "Status 200"
  assert resp.json()["success"] is True, "Data doesn't Match"
  assert resp.json()["data"][0] ==data["data"], "Data doesn't Match"


def test_enable_notifications_using_fake_section_id(client_with_emulator):

  url = BASE_URL + "/sections/fake_section_id/enable_notifications"
  with mock.patch("routes.section.classroom_crud.enable_notifications"):
    with mock.patch("routes.section.Logger"):
      resp = client_with_emulator.post(url)
  print(resp.json())
  assert resp.status_code == 404, "Status 404"
  assert resp.json()["success"] is False, "Data doesn't Match"


def test_get_assignment(client_with_emulator, create_fake_data):
  url = BASE_URL + \
      f"/sections/{create_fake_data['section']}/assignments/5789246"
  print("========")
  print(url)
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
  assert resp.status_code == 200, "Status 200"
  assert data["id"] == course_work_data["id"], "Data id doesn't Match"
  assert data["classroom_id"] == course_work_data[
      "courseId"], "Data course id doesn't Match"
  assert data["description"] is None, "Data description doesn't Match"
  assert datetime.date.fromisoformat(data["due_date"]) == datetime.date(
      year=course_work_data["dueDate"]["year"],
      month=course_work_data["dueDate"]["month"],
      day=course_work_data["dueDate"]["day"]), "Data due date doesn't Match"


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

def test_get_coursework_list(client_with_emulator,create_fake_data):
  url = BASE_URL + \
      f"/sections/{create_fake_data['section']}/get_coursework_list"
  course_work_data = {
    "courseId": "555555555",
      "id": "5789246",
      "title": "test assignment",
      "state": "PUBLISHED",
      "creationTime": "2023-02-16T10:45:49.833Z",
      "materials":[]
  }
  with mock.patch("routes.section.classroom_crud.get_course_work_list",
                  return_value=[course_work_data]):
    resp = client_with_emulator.get(url)
  assert resp.status_code == 200

def test_form_grade_import_form_with_no_response(client_with_emulator,
                                                 create_fake_data):
  url = BASE_URL + \
      f"/sections/{create_fake_data['section']}/coursework/5789246900"
  with mock.patch(
        "routes.section.classroom_crud.get_course_by_id",
                  return_value={"teacherFolder":{"id":"123344"}}):
    with mock.patch("routes.section.classroom_crud.get_course_work",
                  return_value=GET_COURSEWORK_DATA):
      with mock.patch(
"routes.section.classroom_crud.get_edit_url_and_view_url_mapping_of_form",
return_value={"https://docs.google.com/forms/d/e/1FAIpQL":
              {"file_id":"test123"}}):
        with mock.patch(
        "routes.section.classroom_crud.retrieve_all_form_responses",
                  return_value={}):
          resp = client_with_emulator.patch(url)
  result_json = resp.json()
  assert resp.status_code == 404, "Status 404"
  assert result_json[
    "message"] == "Responses not available for google form","message"


def test_form_grade_import_form_with_response(client_with_emulator,
                                                 create_fake_data):
  url = BASE_URL + \
      f"/sections/{create_fake_data['section']}/coursework/5789246900"
  with mock.patch(
        "routes.section.classroom_crud.get_course_by_id",
                return_value={"teacherFolder":{"id":"123344"}}):
    with mock.patch("routes.section.classroom_crud.get_course_work",
                  return_value=GET_COURSEWORK_DATA):
      with mock.patch(
"routes.section.classroom_crud.get_edit_url_and_view_url_mapping_of_form",
return_value=EDIT_VIEW_URL_FILE_ID_MAPPING_FORM):
        with mock.patch(
        "routes.section.classroom_crud.retrieve_all_form_responses",
                  return_value=FORM_RESPONSE_LIST):
          with mock.patch(
        "routes.section.classroom_crud.list_coursework_submissions_user",
                  return_value=LIST_COURSEWORK_SUBMISSION_USER):
            with mock.patch(
        "routes.section.classroom_crud.patch_student_submission"):
              resp = client_with_emulator.patch(url)
  resp_json = resp.json()
  assert resp.status_code == 202, "Status 202"
  assert resp_json[
    "message"] == "Grades for coursework will be updated shortly","message"
