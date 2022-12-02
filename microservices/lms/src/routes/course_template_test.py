"""
  Tests for Course Template endpoints
"""
import os
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
import mock
from schemas.schema_examples import COURSE_TEMPLATE_EXAMPLE, INSERT_COURSE_TEMPLATE_EXAMPLE
from testing.test_config import BASE_URL, COURSE_TEMPLATE_LIST_TEST_DATA
from common.models import CourseTemplate, Cohort
from common.testing.client_with_emulator import client_with_emulator
from common.testing.firestore_emulator import firestore_emulator, clean_firestore

# assigning url
API_URL = f"{BASE_URL}/course_templates"
os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_get_course_template_list(client_with_emulator):
  for i in COURSE_TEMPLATE_LIST_TEST_DATA:
    course_template = CourseTemplate.from_dict(i)
    course_template.save()
    course_template.uuid = course_template.id
    course_template.update()
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


def test_get_course_template(client_with_emulator):
  course_template = CourseTemplate.from_dict(COURSE_TEMPLATE_EXAMPLE)
  course_template.save()
  course_template.uuid = course_template.id
  course_template.update()

  url = API_URL + f'/{course_template.uuid}'
  data = COURSE_TEMPLATE_EXAMPLE
  data["uuid"] = course_template.uuid
  with mock.patch("routes.course_template.Logger"):
    response = client_with_emulator.get(url)
  response_course_template = response.json()
  assert response.status_code == 200, "Status 200"
  assert response_course_template == data, "Return data doesn't match."


def test_create_course_template(client_with_emulator):
  with mock.patch("routes.course_template.Logger"):
    with mock.patch("routes.course_template.classroom_crud.create_course",
                    return_value={
                        "id": "classroom_id",
                        "enrollmentCode": "classroomcode"
                    }):
      with mock.patch("routes.course_template.classroom_crud.add_teacher"):
        response = client_with_emulator.post(
            API_URL, json=INSERT_COURSE_TEMPLATE_EXAMPLE)
  response_json = response.json()
  assert response.status_code == 200, "Status 200"
  assert response_json["success"] is True, "Response Success"
  assert response_json["course_template"][
      "name"] == INSERT_COURSE_TEMPLATE_EXAMPLE[
          "name"], "Check the response course template name"


def test_get_nonexist_course_template(client_with_emulator):
  uuid = "non_exist_uuid"
  url = API_URL + f"/{uuid}"
  data = {
      "success": False,
      "message": f"Course Template with uuid {uuid} is not found",
      "data": None
  }
  with mock.patch("routes.course_template.Logger"):
    response = client_with_emulator.get(url)
  assert response.status_code == 404, "Status 404"
  assert response.json() == data, "Return data doesn't match."


def test_delete_course_template(client_with_emulator):
  course_template = CourseTemplate.from_dict(COURSE_TEMPLATE_EXAMPLE)
  course_template.save()
  course_template.uuid = course_template.id
  course_template.update()

  uuid = course_template.uuid
  url = API_URL + f'/{uuid}'
  data = {
      "success": True,
      "message": f"Successfully deleted the course template with uuid {uuid}",
      "data": None
  }
  with mock.patch("routes.course_template.Logger"):
    response = client_with_emulator.delete(url)
  response_course_template = response.json()
  assert response.status_code == 200, "Status 200"
  assert response_course_template == data, "Return data doesn't match."


def test_delete_nonexist_course_template(client_with_emulator):
  uuid = "non_exist_uuid"
  url = API_URL + f"/{uuid}"
  data = {
      "success": False,
      "message": f"Course Template with uuid {uuid} is not found",
      "data": None
  }
  with mock.patch("routes.course_template.Logger"):
    response = client_with_emulator.delete(url)
  assert response.status_code == 404, "Status 404"
  assert response.json() == data, "Return data doesn't match."
