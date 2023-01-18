"""Course template list and Course template CRUD API e2e tests"""
import datetime
import pytest
import requests
import os
from common.models import Cohort, CourseTemplate, Section
from common.testing.example_objects import TEST_COHORT, TEST_SECTION2
from testing_objects.course_template import COURSE_TEMPLATE_INPUT_DATA
from testing_objects.cohort import COHORT_INPUT_DATA
from testing_objects.test_config import API_URL
from testing_objects.token_fixture import get_token,sign_up_user

DATABASE_PREFIX = os.environ.get("DATABASE_PREFIX")

course_template_id = None


@pytest.fixture(scope="module", autouse=True)
def create_course_template(get_token):
  "create a course template for reference"
  url = f"{API_URL}/course_templates"
  resp = requests.post(url=url,
                       json=COURSE_TEMPLATE_INPUT_DATA,
                       headers=get_token)
  global course_template_id
  course_template_id = resp.json()["course_template"]["id"]


@pytest.fixture
def setup_cohort():
  """Fixture to create temprory data"""
  cohort = Cohort.from_dict(TEST_COHORT)
  course_template = CourseTemplate.find_by_id(course_template_id)
  cohort.course_template = course_template
  cohort.save()
  return cohort


@pytest.fixture()
def create_section(setup_cohort):
  """Fixture to create temprory data"""
  test_section = TEST_SECTION2
  course_template = CourseTemplate.find_by_id(course_template_id)
  test_section["cohort"] = setup_cohort
  test_section["course_template"] = course_template
  section = Section.from_dict(test_section)
  section.save()
  return section


def test_create_cohort(get_token):
  """
  CUJ01 create a Cohort by providing a valid json object
  as a input using that json object creating a Cohort Model object using Third party tool.
  And also finding Course template object.
  Which is required for saving Cohort object in database.
  """

  url = f"{API_URL}/cohorts"
  COHORT_INPUT_DATA["course_template_id"] = course_template_id
  resp = requests.post(headers=get_token, url=url, json=COHORT_INPUT_DATA)
  resp_json = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert resp_json["success"] is True, "Check success"
  assert resp_json["cohort"]["start_date"].split(
      "+")[0] == COHORT_INPUT_DATA["start_date"], "Check start_date of chort"
  assert resp_json["cohort"]["id"] not in ["", None], "Cohort Firebase check"


def test_create_cohort_negative_course_template(get_token):
  """ 
  CUJ02 create a Cohort by providing a valid json object but invalid course_template id
  as a input and calling create Cohort API.
  Which will return Resource not found exception.
  """
  url = f"{API_URL}/cohorts"
  COHORT_INPUT_DATA["course_template_id"] = "fake-id"
  resp = requests.post(url=url, json=COHORT_INPUT_DATA, headers=get_token)
  resp_json = resp.json()
  assert resp.status_code == 404, "Status 404"
  assert resp_json["success"] is False, "Check success"


def test_create_cohort_validation(get_token):
  """
  CUJ03 create a cohort by providing a invalid json object
  as a input using that json object used in calling create cohort API.
  Which will return a validation error response.
  """
  url = f"{API_URL}/cohorts"
  resp = requests.post(url=url,
                       json={
                           "name": "e2e_test_cases",
                           "description": "description"
                       },
                       headers=get_token)
  assert resp.status_code == 422, "Status 422"
  assert resp.json()["success"] is False


def test_get_cohort(setup_cohort, get_token):
  """
  CUJ04 get a Cohort by providing a valid id
  as a path variable and calling get cohort API.
  Which will return a Cohort object.
  """
  url = f"{API_URL}/cohorts/{setup_cohort.id}"
  resp = requests.get(url=url, headers=get_token)
  data = TEST_COHORT
  data["id"] = setup_cohort.id
  course_template = CourseTemplate.find_by_id(course_template_id)
  data["course_template"] = course_template.key
  data["course_template_name"] = course_template.name
  response_cohort = resp.json()
  response_cohort["start_date"] = datetime.datetime.strptime(
      response_cohort.pop("start_date").split("+")[0], '%Y-%m-%dT%H:%M:%S')
  response_cohort["end_date"] = datetime.datetime.strptime(
      response_cohort.pop("end_date").split("+")[0], '%Y-%m-%dT%H:%M:%S')
  response_cohort["registration_start_date"] = datetime.datetime.strptime(
      response_cohort.pop("registration_start_date").split("+")[0],
      '%Y-%m-%dT%H:%M:%S')
  response_cohort["registration_end_date"] = datetime.datetime.strptime(
      response_cohort.pop("registration_end_date").split("+")[0],
      '%Y-%m-%dT%H:%M:%S')
  assert resp.status_code == 200, "Status 200"
  assert response_cohort == data, "Data doesn't Match"


def test_get_cohort_negative(get_token):
  """ 
  CUJ05 get a Cohort by providing a invalid id
  as a path variable and calling get cohort api.
  Which will return a not found error response.
  """
  url = f"{API_URL}/cohorts/fake-id"
  resp = requests.get(url=url, headers=get_token)
  resp_json = resp.json()
  assert resp.status_code == 404, "Status 404"
  assert resp_json["success"] is False, "Data doesn't Match"


def test_update_chort(setup_cohort, get_token):
  """ 
  CUJ06 update a cohort by providing a valid id
  as a path variable and calling Update cohort api.
  Which will return a UpdateCohortResponseModel object as a response.
  """
  url = f"{API_URL}/cohorts/{setup_cohort.id}"
  json_body = {"max_students": 2000}
  resp = requests.patch(url=url, json=json_body, headers=get_token)
  resp_json = resp.json()
  resp_cohort = resp_json["cohort"]
  assert resp.status_code == 200, "Status 200"
  assert resp_json["success"] is True, "Check success"
  assert resp_cohort["max_students"] == 2000, "Check Updated Data"


def test_update_chort_nonexits_course(setup_cohort, get_token):
  """ 
  CUJ07 update a cohort by providing a valid as a path variable id 
  and invalid course template id as json object and calling Update cohort api.
  Which will return a not found error response.
  """

  url = f"{API_URL}/cohorts/{setup_cohort.id}"
  json_body = {"max_students": 2000, "course_template": "non_exits"}
  resp = requests.patch(url=url, json=json_body, headers=get_token)
  resp_json = resp.json()
  assert resp.status_code == 404, "Status 200"
  assert resp_json["success"] is False, "Check success"


def test_update_cohort_negative(get_token):
  """ 
  CUJ09 update a cohort by providing a invalid id
  as a path variable and calling update cohort api.
  Which will return a not found error response.
  """
  url = f"{API_URL}/cohorts/fake-id"
  resp = requests.patch(url=url, json={"max_student": 2000}, headers=get_token)
  resp_json = resp.json()
  assert resp.status_code == 404, "Status 404"
  assert resp_json["success"] is False, "Data doesn't Match"


def test_delete_chort(setup_cohort, get_token):
  """ 
  CUJ09 delete a cohort by providing a valid id
  as a path variable and calling delete cohort api.
  Which will return a DeleteCohortResponseModel object as a response.
  """

  url = f"{API_URL}/cohorts/{setup_cohort.id}"
  resp = requests.delete(url=url, headers=get_token)
  resp_json = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert resp_json["success"] is True, "Check success"


def test_delete_cohort_negative(get_token):
  """ 
  CUJ010 delete a cohort by providing a invalid id
  as a path variable and calling delete cohort api.
  Which will return a not found error response.
  """
  url = f"{API_URL}/cohorts/fake-id"
  resp = requests.delete(url=url, headers=get_token)
  resp_json = resp.json()
  assert resp.status_code == 404, "Status 404"
  assert resp_json["success"] is False, "Data doesn't Match"


def test_get_list_cohort(get_token):
  """ 
  CUJ11 get a cohort list by calling get cohort list api.
  Which will return a CohortListResponseModel object.
  """
  url = f"{API_URL}/cohorts"
  resp = requests.get(url=url, headers=get_token)
  resp_json = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert resp_json["success"] is True, "Check success"


def test_get_list_sections_by_cohort(get_token, create_section):
  """
  Get a sections list for a perticular cohort by giving cohort_id as query paramter 
  """
  url = f"{API_URL}/cohorts/{create_section.cohort.id}/sections"
  resp = requests.get(url=url, headers=get_token)
  resp_json = resp.json()
  assert resp.status_code == 200, "Status 200"


def test_get_list_sections_by_nonexists_cohort(get_token):
  """
  Get a sections list for a perticular cohort by giving cohort_id as query paramter 
  """
  url = f"{API_URL}/cohorts/fake-id/sections"
  resp = requests.get(url=url, headers=get_token)
  resp_json = resp.json()
  assert resp.status_code == 404, "Status 404"
