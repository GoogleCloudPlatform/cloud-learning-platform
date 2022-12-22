"""
  Tests for Course Template endpoints
"""
import os
import json
import datetime

import pytest
import mock

# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from common.models import CourseTemplate, Cohort
from common.testing.client_with_emulator import client_with_emulator
from common.testing.firestore_emulator import firestore_emulator, clean_firestore
from schemas.schema_examples import COURSE_TEMPLATE_EXAMPLE, COHORT_EXAMPLE
from testing.test_config import BASE_URL, COHORT_LIST_TEST_DATA, INPUT_COHORT_TEST_DATA

# assigning url
API_URL = f"{BASE_URL}/cohorts"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


@pytest.fixture
def create_course_template(client_with_emulator):
  course_template = CourseTemplate.from_dict(COURSE_TEMPLATE_EXAMPLE)
  course_template.save()
  return course_template


def test_get_cohort_list(client_with_emulator, create_course_template):

  for i in COHORT_LIST_TEST_DATA:
    cohort = Cohort.from_dict(i)
    cohort.course_template = create_course_template
    cohort.save()
  data = {"success": True, "message": "Successfully get the Cohort list"}
  # mock logger
  with mock.patch("routes.cohort.Logger"):
    response = client_with_emulator.get(API_URL)
  response_json = response.json()
  assert response.status_code == 200, "Status 200"
  assert len(response_json["cohort_list"]) == len(
      COHORT_LIST_TEST_DATA), "Return data list len doesn't match."
  response_json.pop("cohort_list")
  assert response_json == data, "Return data doesn't match."


def test_get_cohort(client_with_emulator, create_course_template):
  cohort = Cohort.from_dict(COHORT_EXAMPLE)
  cohort.course_template = create_course_template
  cohort.save()

  url = API_URL + f"/{cohort.id}"
  data = COHORT_EXAMPLE
  data["id"] = cohort.id
  data["course_template"] = create_course_template.key
  with mock.patch("routes.cohort.Logger"):
    response = client_with_emulator.get(url)
  response_cohort = json.loads(response.text)
  response_cohort["start_date"] = datetime.datetime.strptime(
      response_cohort.pop("start_date").split("+")[0], "%Y-%m-%dT%H:%M:%S")
  response_cohort["end_date"] = datetime.datetime.strptime(
      response_cohort.pop("end_date").split("+")[0], "%Y-%m-%dT%H:%M:%S")
  response_cohort["registration_start_date"] = datetime.datetime.strptime(
      response_cohort.pop("registration_start_date").split("+")[0],
      "%Y-%m-%dT%H:%M:%S")
  response_cohort["registration_end_date"] = datetime.datetime.strptime(
      response_cohort.pop("registration_end_date").split("+")[0],
      "%Y-%m-%dT%H:%M:%S")
  assert response.status_code == 200, "Status 200"
  assert response_cohort == data, "Return data doesn't match."


def test_create_course_template(client_with_emulator, create_course_template):
  INPUT_COHORT_TEST_DATA["course_template_id"] = create_course_template.id
  with mock.patch("routes.cohort.Logger"):
    response = client_with_emulator.post(API_URL, json=INPUT_COHORT_TEST_DATA)
  response_json = json.loads(response.text)
  assert response.status_code == 200, "Status 200"
  assert response_json["success"] is True, "Response Success"
  assert response_json["cohort"]["name"] == INPUT_COHORT_TEST_DATA[
      "name"], "Check the response cohort name"
  assert response_json["cohort"][
      "course_template"] == create_course_template.key, \
  "Check the response cohort name"


def test_get_nonexist_cohort(client_with_emulator):
  id = "non_exist_id"
  url = API_URL + f"/{id}"
  data = {
      "success": False,
      "message": f"cohorts with id {id} is not found",
      "data": None
  }
  with mock.patch("routes.cohort.Logger"):
    response = client_with_emulator.get(url)
  assert response.status_code == 404, "Status 404"
  assert response.json() == data, "Return data doesn't match."


def test_update_cohort(client_with_emulator, create_course_template):
  cohort = Cohort.from_dict(COHORT_EXAMPLE)
  cohort.course_template = create_course_template
  cohort.save()

  id = cohort.id
  url = API_URL + f"/{id}"
  data = {
      "success": True,
      "message": f"Successfully Updated the Cohort with id {id}"
  }
  json_body = {"max_students": 5000, "end_date": "2023-01-25T00:00:00"}
  with mock.patch("routes.cohort.Logger"):
    response = client_with_emulator.patch(url, json=json_body)
  response_cohort = response.json()
  loaded_cohort = response_cohort.pop("cohort")
  assert response.status_code == 200, "Status 200"
  assert response_cohort == data, "Return data doesn't match."
  assert loaded_cohort[
      "max_students"] == 5000, "Updated max student data doesn't match"
  assert loaded_cohort["end_date"].split("+")[0] == "2023-01-25T00:00:00"


def test_update_cohort_nonexits_course_template(client_with_emulator,
                                                create_course_template):
  cohort = Cohort.from_dict(COHORT_EXAMPLE)
  cohort.course_template = create_course_template
  cohort.save()

  id = cohort.id
  url = API_URL + f"/{id}"
  data = {
      "success": False,
      "message": "course_templates with id non_exits_id is not found",
      "data": None
  }
  json_body = {"max_students": 5000, "course_template": "non_exits_id"}
  with mock.patch("routes.cohort.Logger"):
    response = client_with_emulator.patch(url, json=json_body)
  assert response.status_code == 404, "Status 404"
  assert response.json() == data, "Return data doesn't match."


def test_update_nonexists_cohort(client_with_emulator):
  id = "non_exists_id"
  url = API_URL + f"/{id}"
  data = {
      "success": False,
      "message": f"cohorts with id {id} is not found",
      "data": None
  }
  json_body = {"max_students": 5000, "end_date": "2023-01-25T00:00:00"}
  with mock.patch("routes.cohort.Logger"):
    response = client_with_emulator.patch(url, json=json_body)
  assert response.status_code == 404, "Status 404"
  assert response.json() == data, "Return data doesn't match."


def test_delete_cohort(client_with_emulator, create_course_template):
  cohort = Cohort.from_dict(COHORT_EXAMPLE)
  cohort.course_template = create_course_template
  cohort.save()

  id = cohort.id
  url = API_URL + f"/{id}"
  data = {
      "success": True,
      "message": f"Successfully deleted the Cohort with id {id}",
      "data": None
  }
  with mock.patch("routes.cohort.Logger"):
    response = client_with_emulator.delete(url)
  response_cohort = response.json()
  assert response.status_code == 200, "Status 200"
  assert response_cohort == data, "Return data doesn't match."


def test_delete_nonexist_cohort(client_with_emulator):
  id = "non_exist_id"
  url = API_URL + f"/{id}"
  data = {
      "success": False,
      "message": f"cohorts with id {id} is not found",
      "data": None
  }
  with mock.patch("routes.cohort.Logger"):
    response = client_with_emulator.delete(url)
  assert response.status_code == 404, "Status 404"
  assert response.json() == data, "Return data doesn't match."
