"""
  Tests for Course Template endpoints
"""
import os
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
import mock
from common.models import CourseTemplate, Cohort
from common.testing.client_with_emulator import client_with_emulator
from common.testing.firestore_emulator import firestore_emulator, clean_firestore
from schemas.schema_examples import COURSE_TEMPLATE_EXAMPLE, INSERT_COURSE_TEMPLATE_EXAMPLE
from testing.test_config import BASE_URL, COURSE_TEMPLATE_LIST_TEST_DATA, COHORT_LIST_TEST_DATA
# assigning url
API_URL = f"{BASE_URL}/course_templates"
os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_get_course_template_list(client_with_emulator):
  for i in COURSE_TEMPLATE_LIST_TEST_DATA:
    course_template = CourseTemplate.from_dict(i)
    course_template.save()
  data = {
      "success": True,
      "message": "Successfully get the course template list"
  }
  # mock logger
  with mock.patch("routes.course_template.Logger"):
    response = client_with_emulator.get(API_URL)
  response_json = response.json()
  assert response.status_code == 200, "Status 200"
  assert len(response_json["course_template_list"]) == len(
      COURSE_TEMPLATE_LIST_TEST_DATA), "Return data list len doesn't match."
  response_json.pop("course_template_list")
  assert response_json == data, "Return data doesn't match."


def test_get_course_template_list_negative_skip(client_with_emulator):
  url = f"{API_URL}?skip=-1&limit=10"
  # mock logger
  with mock.patch("routes.course_template.Logger"):
    response = client_with_emulator.get(url)
  assert response.status_code == 422, "Status 422"


def test_get_course_template(client_with_emulator):
  course_template = CourseTemplate.from_dict(COURSE_TEMPLATE_EXAMPLE)
  course_template.save()

  url = API_URL + f"/{course_template.id}"
  data = COURSE_TEMPLATE_EXAMPLE
  data["id"] = course_template.id
  with mock.patch("routes.course_template.Logger"):
    response = client_with_emulator.get(url)
  response_course_template = response.json()
  assert response.status_code == 200, "Status 200"
  assert response_course_template == data, "Return data doesn't match."


def test_get_cohort_list_by_course_template(client_with_emulator):
  course_template = CourseTemplate.from_dict(COURSE_TEMPLATE_EXAMPLE)
  course_template.save()
  for i in COHORT_LIST_TEST_DATA:
    cohort = Cohort.from_dict(i)
    cohort.course_template = course_template
    cohort.save()

  url = API_URL + f"/{course_template.id}/cohorts"
  data = {
      "success":
      True,
      "message":
      "Successfully get the Cohort list by" +
      f" Course template id {course_template.id}"
  }
  with mock.patch("routes.course_template.Logger"):
    response = client_with_emulator.get(url)
  response_json = response.json()
  assert response.status_code == 200, "Status 200"
  assert len(response_json["cohort_list"]) == len(
      COHORT_LIST_TEST_DATA), "Return data list len doesn't match."
  response_json.pop("cohort_list")
  assert response_json == data, "Return data doesn't match."


def test_get_cohort_list_by_course_template_negative_skip(
    client_with_emulator):
  course_template = CourseTemplate.from_dict(COURSE_TEMPLATE_EXAMPLE)
  course_template.save()

  url = API_URL + f"/{course_template.id}/cohorts?skip=-1&limit=10"
  with mock.patch("routes.course_template.Logger"):
    response = client_with_emulator.get(url)
  assert response.status_code == 422, "Status 422"


def test_get_cohort_list_by_nonexist_course_template(client_with_emulator):
  url = API_URL + "/fake_id/cohorts"
  data = {
      "success": False,
      "message": "course_templates with id fake_id is not found",
      "data": None
  }
  with mock.patch("routes.course_template.Logger"):
    response = client_with_emulator.get(url)
  response_json = response.json()
  assert response.status_code == 404, "Status 404"
  assert response_json == data, "Return data doesn't match."


def test_create_course_template(client_with_emulator):
  with mock.patch("routes.course_template.Logger"):
    with mock.patch("routes.course_template.classroom_crud.create_course",
                    return_value={
                        "id": "classroom_id",
                        "enrollmentCode": "classroomcode"
                    }):
      with mock.patch("routes.course_template.classroom_crud.acceept_invite"):
        with mock.patch("routes.course_template.classroom_crud.invite_teacher"):
          with mock.patch("routes.course_template.classroom_crud.get_user_profile_information"):
            with mock.patch("routes.course_template.common_service.create_teacher"):
              response = client_with_emulator.post(
            API_URL, json=INSERT_COURSE_TEMPLATE_EXAMPLE)
  response_json = response.json()
  assert response.status_code == 200, "Status 200"
  assert response_json["success"] is True, "Response Success"
  assert response_json["course_template"][
      "name"] == INSERT_COURSE_TEMPLATE_EXAMPLE[
          "name"], "Check the response course template name"


def test_get_nonexist_course_template(client_with_emulator):
  course_template_id = "non_exist_id"
  url = API_URL + f"/{course_template_id}"
  data = {
      "success": False,
      "message": f"course_templates with id {course_template_id} is not found",
      "data": None
  }
  with mock.patch("routes.course_template.Logger"):
    response = client_with_emulator.get(url)
  assert response.status_code == 404, "Status 404"
  assert response.json() == data, "Return data doesn't match."


def test_delete_course_template(client_with_emulator):
  course_template = CourseTemplate.from_dict(COURSE_TEMPLATE_EXAMPLE)
  course_template.save()

  course_template_id = course_template.id
  url = API_URL + f"/{course_template_id}"
  data = {
      "success": True,
      "message": "Successfully deleted the " +
      f"course template with id {course_template_id}",
      "data": None
  }
  with mock.patch("routes.course_template.Logger"):
    response = client_with_emulator.delete(url)
  response_course_template = response.json()
  assert response.status_code == 200, "Status 200"
  assert response_course_template == data, "Return data doesn't match."


def test_delete_nonexist_course_template(client_with_emulator):
  course_template_id = "non_exist_id"
  url = API_URL + f"/{course_template_id}"
  data = {
      "success": False,
      "message": f"course_templates with id {course_template_id} is not found",
      "data": None
  }
  with mock.patch("routes.course_template.Logger"):
    response = client_with_emulator.delete(url)
  assert response.status_code == 404, "Status 404"
  assert response.json() == data, "Return data doesn't match."


def test_update_course_template(client_with_emulator):
  course_template = CourseTemplate.from_dict(COURSE_TEMPLATE_EXAMPLE)
  course_template.save()

  course_template_id = course_template.id
  url = API_URL + f"/{course_template_id}"
  data = {
      "success":
      True,
      "message":
      "Successfully Updated the Course " +
      f"Template with id {course_template_id}"
  }
  json_body = {"name": "update_name", "description": "updated_description"}
  with mock.patch("routes.course_template.Logger"):
    response = client_with_emulator.patch(url, json=json_body)
  response_course_template = response.json()
  loaded_course_template = response_course_template.pop("course_template")
  assert response.status_code == 200, "Status 200"
  assert response_course_template == data, "Return data doesn't match."
  assert loaded_course_template["name"] == json_body[
      "name"], "Updated data doesn't match"
  assert loaded_course_template["description"] == json_body[
      "description"], "Updated data doesn't match"


def test_update_nonexists_course_template(client_with_emulator):
  course_template_id = "non_exists_id"
  url = API_URL + f"/{course_template_id}"
  data = {
      "success": False,
      "message": f"course_templates with id {course_template_id} is not found",
      "data": None
  }
  json_body = {"name": "update_name", "description": "updated_description"}
  with mock.patch("routes.course_template.Logger"):
    response = client_with_emulator.patch(url, json=json_body)
  assert response.status_code == 404, "Status 404"
  assert response.json() == data, "Return data doesn't match."
