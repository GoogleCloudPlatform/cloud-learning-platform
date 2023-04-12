"""
  Tests for Analytics endpoints
"""
import datetime
import os
import mock
import pytest
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from testing.test_config import BASE_URL
from common.testing.client_with_emulator import client_with_emulator
from common.testing.firestore_emulator import firestore_emulator, clean_firestore
from schemas.schema_examples import (
  ANALYTICS_USER_EXAMPLE, ANALYTICS_COURSE_WORK_EXAMPLE,
  ANALYTICS_COURSE_EXAMPLE)
os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"
SUCCESS_RESPONSE = {"status": "Success"}
@pytest.fixture()
def create_fake_data_list(client_with_emulator):
  """_summary_

  Args:
      client_with_emulator (_type_): _description_

  Returns:
      _type_: _description_
  """
  data=ANALYTICS_USER_EXAMPLE.copy()
  course=ANALYTICS_COURSE_EXAMPLE.copy()
  course.pop("course_work_list")
  course_work=ANALYTICS_COURSE_WORK_EXAMPLE.copy()
  course_work["course_work_due_date"]=datetime.datetime.strptime(
    course_work["course_work_due_date"],"%Y-%m-%d").date()
  course_work["course_work_due_time"]=datetime.datetime.strptime(
    course_work["course_work_due_time"],"%H:%M:%S").time()
  # course_work.pop("submission")
  data.update(course)
  data.update(course_work)
  return data

def test_get_analytics(client_with_emulator,create_fake_data_list):
  url = (BASE_URL + "/analytics/students/"
         +f"{create_fake_data_list['user_email_address']}")
  with mock.patch("routes.analytics.student_service.get_user_email",
   return_value=(create_fake_data_list["user_email_address"],"user_id")):
    with mock.patch("routes.analytics.get_key",return_value=None):
      with mock.patch("routes.analytics.set_key"):
        with mock.patch("routes.analytics.run_query",
                      return_value=[create_fake_data_list]):
          resp = client_with_emulator.get(url)
  data={
    "user":ANALYTICS_USER_EXAMPLE,
    "section_list":[ANALYTICS_COURSE_EXAMPLE]
    }
  data["user"]["user_id"]="user_id"
  assert resp.status_code == 200, "Status 200"
  assert resp.json() == data, "Return data doesn't match."

def test_get_analytics_negative(client_with_emulator):
  url= BASE_URL + "/analytics/students/xyz@gmail.com"
  with mock.patch("routes.analytics.student_service.get_user_email",
                  return_value=("xyz@gmail.com","user_id")):
    with mock.patch("routes.analytics.get_key",return_value=None):
      with mock.patch("routes.analytics.set_key"):
        with mock.patch("routes.analytics.run_query",
                      return_value=[]):
          resp = client_with_emulator.get(url)

  assert resp.status_code == 404, "Status 404"
