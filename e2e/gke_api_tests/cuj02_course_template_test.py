"""Course template list and Course template CRUD API e2e tests"""
import pytest
from common.models import CourseTemplate
from common.testing.example_objects import TEST_COURSE_TEMPLATE
from common.utils.errors import ResourceNotFoundException
from testing_objects.course_template import COURSE_TEMPLATE_INPUT_DATA
from testing_objects.test_config import API_URL
from testing_objects.session_fixture import get_session,user_login


@pytest.fixture
def setup_course_templates():
  """Fixture to create temprory data"""
  course_template = CourseTemplate.from_dict(TEST_COURSE_TEMPLATE)
  course_template.save()
  course_template.uuid = course_template.id
  course_template.update()
  return course_template


def test_create_course_template(get_session):
  """
  CUJ01 create a Course template by providing a valid json object
  as a input using that json object calling create course template api.
  Which creates a course template and master course in classroom.
  """
  url = f"{API_URL}/course_templates"
  resp = get_session.post(url=url, json=COURSE_TEMPLATE_INPUT_DATA)
  resp_json = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert resp_json["success"] is True, "Check success"
  assert resp_json["course_template"]["classroom_code"] not in [
      "", None
  ], "Course Template classroom check"
  assert resp_json["course_template"]["uuid"] not in [
      "", None
  ], "Course Template Firebase check"


def test_create_course_template_validation(get_session):
  """
  CUJ02 create a Course template by providing a invalid json object
  as a input using that json object calling create course template api.
  Which will return a validation error response.
  """
  url = f"{API_URL}/course_templates"
  resp = get_session.post(url=url,
                     json={
                         "name": "e2e_test_cases",
                         "description": "description"
                     })
  assert resp.status_code == 422, "Status 422"
  assert resp.json()["success"] is False


def test_get_course_template(setup_course_templates, get_session):
  """
  CUJ03 get a Course template by providing a valid uuid
  as a path variable and calling get course template api.
  Which will return a course template object.
  """

  url = f"{API_URL}/course_templates/{setup_course_templates.id}"
  resp = get_session.get(url=url)
  data = TEST_COURSE_TEMPLATE
  data["uuid"] = setup_course_templates.id
  resp_json = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert resp_json == data, "Data doesn't Match"


def test_get_course_template_negative(get_session):
  """
  CUJ04 get a course template by providing a invalid uuid
  as a path variable and calling get course template api.
  Which will return a not found error response.
  """
  url = f"{API_URL}/course_templates/fake-uuid"
  resp = get_session.get(url=url)
  resp_json = resp.json()
  assert resp.status_code == 404, "Status 404"
  assert resp_json["success"] is False, "Data doesn't Match"


def test_delete_course_template(setup_course_templates, get_session):
  """
  CUJ05 delete a course template by providing a valid uuid
  as a path variable and calling delete course template api.
  Which will return a DeleteCourseTemplateModel object as a response.
  """
  url = f"{API_URL}/course_templates/{setup_course_templates.id}"
  resp = get_session.delete(url=url)
  resp_json = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert resp_json["success"] is True, "Check success"


def test_delete_course_template_negative(get_session):
  """
  CUJ06 delete a course template by providing a invalid uuid
  as a path variable and calling delete course template api.
  Which will return a not found error response.
  """
  url = f"{API_URL}/course_templates/fake-uuid"
  resp = get_session.delete(url=url)
  resp_json = resp.json()
  assert resp.status_code == 404, "Status 404"
  assert resp_json["success"] is False, "Data doesn't Match"


def test_get_list_course_template(get_session):
  """
  CUJ07 get a course template list by calling get course template list api.
  Which will return a CourseTemplateList object.
  """
  url = f"{API_URL}/course_templates"
  resp = get_session.get(url=url)
  resp_json = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert resp_json["success"] is True, "Check success"
