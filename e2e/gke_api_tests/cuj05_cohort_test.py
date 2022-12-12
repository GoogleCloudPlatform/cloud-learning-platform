"""Course template list and Course template CRUD API e2e tests"""
import datetime
import pytest
from common.models import Cohort, CourseTemplate
from common.testing.example_objects import TEST_COHORT
from testing_objects.course_template import COURSE_TEMPLATE_INPUT_DATA
from testing_objects.cohort import COHORT_INPUT_DATA
from testing_objects.test_config import API_URL
from testing_objects.login_fixture import user_login_fixture
from setup import get_method, post_method, patch_method, delete_method


course_template_uuid=None
@pytest.fixture(scope="session",autouse=True)
def create_course_template():
  "create a course template for reference"
  url =  f"{API_URL}/course_templates"
  resp = post_method(
    url=url, request_body=COURSE_TEMPLATE_INPUT_DATA)
  global course_template_uuid
  course_template_uuid = resp.json()["course_template"]["uuid"]


@pytest.fixture
def setup_cohort():
    """Fixture to create temprory data"""
    cohort = Cohort.from_dict(TEST_COHORT)
    course_template=CourseTemplate.find_by_uuid(course_template_uuid)
    cohort.course_template=course_template
    cohort.save()
    cohort.uuid = cohort.id
    cohort.update()
    return cohort




def test_create_cohort():
  """
  CUJ01 create a Cohort by providing a valid json object
  as a input using that json object creating a Cohort Model object using Third party tool.
  And also finding Course template object.
  Which is required for saving Cohort object in database.
  """
   
  url = f"{API_URL}/cohorts"
  COHORT_INPUT_DATA["course_template_uuid"]=course_template_uuid
  resp = post_method(
  url=url, request_body=COHORT_INPUT_DATA)
  resp_json = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert resp_json["success"] is True, "Check success"
  assert resp_json["cohort"]["start_date"].split("+")[0] == COHORT_INPUT_DATA["start_date"], "Check start_date of chort"
  assert resp_json["cohort"]["uuid"] not in [
    "", None], "Cohort Firebase check"


def test_create_cohort_negative_course_template():
  """ 
  CUJ02 create a Cohort by providing a valid json object but invalid course_template uuid
  as a input and calling create Cohort API.
  Which will return Resource not found exception.
  """
  url = f"{API_URL}/cohorts"
  COHORT_INPUT_DATA["course_template_uuid"] = "fake-uuid"
  resp = post_method(
    url=url, request_body=COHORT_INPUT_DATA)
  resp_json = resp.json()
  assert resp.status_code == 404, "Status 404"
  assert resp_json["success"] is False, "Check success"

def test_create_cohort_validation():
  """
  CUJ03 create a cohort by providing a invalid json object
  as a input using that json object used in calling create cohort API.
  Which will return a validation error response.
  """
  url = f"{API_URL}/cohorts"
  resp = post_method(
  url=url, request_body={"name": "e2e_test_cases",
    "description": "description"})
  assert resp.status_code == 422, "Status 422"
  assert resp.json()["success"] is False


def test_get_cohort(setup_cohort):
  """
  CUJ04 get a Cohort by providing a valid uuid
  as a path variable and calling get cohort API.
  Which will return a Cohort object.
  """
  url =f"{API_URL}/cohorts/{setup_cohort.id}"
  resp = get_method(url=url)
  data = TEST_COHORT
  data["uuid"] = setup_cohort.uuid
  data["course_template"] = CourseTemplate.find_by_uuid(
  course_template_uuid).key
  response_cohort = resp.json()
  response_cohort["start_date"] = datetime.datetime.strptime(
  response_cohort.pop("start_date").split("+")[0], '%Y-%m-%dT%H:%M:%S')
  response_cohort["end_date"] = datetime.datetime.strptime(
  response_cohort.pop("end_date").split("+")[0], '%Y-%m-%dT%H:%M:%S')
  response_cohort["registration_start_date"] = datetime.datetime.strptime(
  response_cohort.pop("registration_start_date").split("+")[0], '%Y-%m-%dT%H:%M:%S')
  response_cohort["registration_end_date"] = datetime.datetime.strptime(
  response_cohort.pop("registration_end_date").split("+")[0], '%Y-%m-%dT%H:%M:%S')
  assert resp.status_code == 200, "Status 200"
  assert response_cohort == data, "Data doesn't Match"


def test_get_cohort_negative():
  """ 
  CUJ05 get a Cohort by providing a invalid uuid
  as a path variable and calling get cohort api.
  Which will return a not found error response.
  """
  url =f"{API_URL}/cohorts/fake-uuid"
  resp = get_method(url=url)
  resp_json = resp.json()
  assert resp.status_code == 404, "Status 404"
  assert resp_json["success"] is False, "Data doesn't Match"


def test_update_chort(setup_cohort):
  """ 
  CUJ06 update a cohort by providing a valid uuid
  as a path variable and calling Update cohort api.
  Which will return a UpdateCohortResponseModel object as a response.
  """
  url = f"{API_URL}/cohorts/{setup_cohort.id}"
  json_body = {
        "max_students": 2000
    }
  resp = patch_method(url=url, request_body=json_body)
  resp_json = resp.json()
  resp_cohort = resp_json["cohort"]
  assert resp.status_code == 200, "Status 200"
  assert resp_json["success"] is True, "Check success"
  assert resp_cohort["max_students"] == 2000, "Check Updated Data"


def test_update_chort_nonexits_course(setup_cohort):
  """ 
  CUJ07 update a cohort by providing a valid as a path variable uuid 
  and invalid course template uuid as json object and calling Update cohort api.
  Which will return a not found error response.
  """
  
  url = f"{API_URL}/cohorts/{setup_cohort.id}"
  json_body = {
    "max_students": 2000,
    "course_template": "non_exits"
    }
  resp = patch_method(url=url, request_body=json_body)
  resp_json = resp.json()
  assert resp.status_code == 404, "Status 200"
  assert resp_json["success"] is False, "Check success"


def test_update_cohort_negative():
  """ 
  CUJ09 update a cohort by providing a invalid uuid
  as a path variable and calling update cohort api.
  Which will return a not found error response.
  """
  url = f"{API_URL}/cohorts/fake-uuid"
  resp = patch_method(url=url, request_body={"max_student": 2000})
  resp_json = resp.json()
  assert resp.status_code == 404, "Status 404"
  assert resp_json["success"] is False, "Data doesn't Match"

def test_delete_chort(setup_cohort):
  """ 
  CUJ09 delete a cohort by providing a valid uuid
  as a path variable and calling delete cohort api.
  Which will return a DeleteCohortResponseModel object as a response.
  """
  
  url=f"{API_URL}/cohorts/{setup_cohort.id}"
  resp = delete_method(url=url)
  resp_json = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert resp_json["success"] is True, "Check success"


def test_delete_cohort_negative():
  """ 
  CUJ010 delete a cohort by providing a invalid uuid
  as a path variable and calling delete cohort api.
  Which will return a not found error response.
  """
  url = f"{API_URL}/cohorts/fake-uuid"
  resp = delete_method(url=url)
  resp_json = resp.json()
  assert resp.status_code == 404, "Status 404"
  assert resp_json["success"] is False, "Data doesn't Match"


def test_get_list_cohort():
  """ 
  CUJ11 get a cohort list by calling get cohort list api.
  Which will return a CohortListResponseModel object.
  """
  url = f"{API_URL}/cohorts"
  resp = get_method(url=url)
  resp_json = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert resp_json["success"] is True, "Check success"
