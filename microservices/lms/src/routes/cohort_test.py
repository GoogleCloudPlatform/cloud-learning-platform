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
from common.models import CourseTemplate, Cohort, Section
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


def test_get_cohort_list_negative_skip(client_with_emulator):

  url = f"{API_URL}?skip=-1&limit=10"
  with mock.patch("routes.cohort.Logger"):
    response = client_with_emulator.get(url)
  assert response.status_code == 422, "Status 422"


def test_get_cohort(client_with_emulator, create_course_template):
  cohort = Cohort.from_dict(COHORT_EXAMPLE)
  cohort.course_template = create_course_template
  cohort.save()

  url = API_URL + f"/{cohort.id}"
  data = COHORT_EXAMPLE
  data["id"] = cohort.id
  data["course_template"] = create_course_template.key
  data["course_template_name"] = create_course_template.name
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


def test_create_cohort(client_with_emulator, create_course_template):
  INPUT_COHORT_TEST_DATA["course_template_id"] = create_course_template.id
  with mock.patch("routes.cohort.Logger"):
    with mock.patch("routes.cohort.insert_rows_to_bq"):
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
  cohort_id = "non_exist_id"
  url = API_URL + f"/{cohort_id}"
  data = {
      "success": False,
      "message": f"cohorts with id {cohort_id} is not found",
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

  cohort_id = cohort.id
  url = API_URL + f"/{cohort_id}"
  data = {
      "success": True,
      "message": f"Successfully Updated the Cohort with id {cohort_id}"
  }
  json_body = {"max_students": 5000, "end_date": "2023-01-25T00:00:00"}
  with mock.patch("routes.cohort.Logger"):
    with mock.patch("routes.cohort.insert_rows_to_bq"):
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

  cohort_id = cohort.id
  url = API_URL + f"/{cohort_id}"
  data = {
      "success": False,
      "message": "course_templates with id non_exits_id is not found",
      "data": None
  }
  json_body = {"max_students": 5000, "course_template": "non_exits_id"}
  with mock.patch("routes.cohort.Logger"):
    with mock.patch("routes.cohort.insert_rows_to_bq"):
      response = client_with_emulator.patch(url, json=json_body)
  assert response.status_code == 404, "Status 404"
  assert response.json() == data, "Return data doesn't match."


def test_update_nonexists_cohort(client_with_emulator):
  cohort_id = "non_exists_id"
  url = API_URL + f"/{cohort_id}"
  data = {
      "success": False,
      "message": f"cohorts with id {cohort_id} is not found",
      "data": None
  }
  json_body = {"max_students": 5000, "end_date": "2023-01-25T00:00:00"}
  with mock.patch("routes.cohort.Logger"):
    with mock.patch("routes.cohort.insert_rows_to_bq"):
      response = client_with_emulator.patch(url, json=json_body)
  assert response.status_code == 404, "Status 404"
  assert response.json() == data, "Return data doesn't match."


def test_delete_cohort(client_with_emulator, create_course_template):
  cohort = Cohort.from_dict(COHORT_EXAMPLE)
  cohort.course_template = create_course_template
  cohort.save()

  cohort_id = cohort.id
  url = API_URL + f"/{cohort_id}"
  data = {
      "success": True,
      "message": f"Successfully deleted the Cohort with id {cohort_id}",
      "data": None
  }
  with mock.patch("routes.cohort.Logger"):
    response = client_with_emulator.delete(url)
  response_cohort = response.json()
  assert response.status_code == 200, "Status 200"
  assert response_cohort == data, "Return data doesn't match."


def test_delete_nonexist_cohort(client_with_emulator):
  cohort_id = "non_exist_id"
  url = API_URL + f"/{cohort_id}"
  data = {
      "success": False,
      "message": f"cohorts with id {cohort_id} is not found",
      "data": None
  }
  with mock.patch("routes.cohort.Logger"):
    response = client_with_emulator.delete(url)
  assert response.status_code == 404, "Status 404"
  assert response.json() == data, "Return data doesn't match."


def test_list_section_for_one_cohort(client_with_emulator, create_fake_data):

  url = API_URL + f"/{create_fake_data['cohort']}/sections"
  resp = client_with_emulator.get(url)
  # json_response = resp.json()
  assert resp.status_code == 200


def test_list_section_for_one_cohort_negative_skip(client_with_emulator,
                                                   create_fake_data):

  url = API_URL + f"/{create_fake_data['cohort']}/sections?skip=-1&limit=10"
  resp = client_with_emulator.get(url)
  # json_response = resp.json()
  assert resp.status_code == 422, "Status 422"


def test_list_section_cohort_not_found(client_with_emulator):

  url = API_URL + "/fake-cohort-id22/sections"

  resp = client_with_emulator.get(url)
  # json_response = resp.json()

  assert resp.status_code == 404

def test_get_overall_percentage(client_with_emulator,create_fake_data):
  url = BASE_URL+\
  f"/cohorts/{create_fake_data['cohort']}/get_overall_grade/test@gmail.com"
  course_work_data = [{
    "courseId": "608197437928",
      "id": "608197730201",
      "title": "test assignment",
      "state": "PUBLISHED",
      "maxPoints":100,
      "creationTime": "2023-02-16T10:45:49.833Z",
      "materials":[],
      "gradeCategory": {
        "id": "519721188066",
        "name": "category 3",
        "weight": 600000,
        "defaultGradeDenominator": 100
      }
  }]
  submitted_course_work_data=[{
    "courseId": "608197437928",
      "courseWorkId": "608197730201",
      "id": "Cg4I3PC2n7kOEJm_o9vZEQ",
      "userId": "112879484175618986691",
      "creationTime": "2023-05-06T15:23:49.535Z",
      "updateTime": "2023-05-06T15:25:39.348Z",
      "state": "RETURNED",
      "draftGrade": 50,
      "assignedGrade": 50,
  }]
  with mock.patch("routes.cohort.student_service.get_user_id",\
                  return_value="test@gmail.com"):
    with mock.patch("routes.cohort.classroom_crud.get_coursework_list",\
                    return_value=course_work_data):
      with mock.patch\
        ("routes.cohort.classroom_crud.get_submitted_course_work_list",\
                      return_value=submitted_course_work_data):
        resp = client_with_emulator.get(url)
  assert resp.status_code == 200

