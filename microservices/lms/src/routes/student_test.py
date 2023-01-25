"""
  Tests for User endpoints
"""
import os
import mock
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from common.testing.client_with_emulator import client_with_emulator
from common.testing.firestore_emulator import firestore_emulator, clean_firestore
from testing.test_config import BASE_URL

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"
SUCCESS_RESPONSE = {"status": "Success"}


def test_get_student_course_progress_percent(client_with_emulator):
  url = BASE_URL + "/student/get_progress_percentage/" + \
    "?course_id=504551481098&student_email=test_user_1@dhodun.altostrat.com"

  with mock.patch("routes.student.classroom_crud.get_course_work_list",
                  return_value=[{}, {}]):
    with mock.patch(
        "routes.student.classroom_crud.get_submitted_course_work_list",
        return_value=[{
            "state": "TURNED_IN"
        }, {
            "state": "TURNED_IN"
        }]):
      resp = client_with_emulator.get(url)
  assert resp.status_code == 200

def test_list_student_of_section(client_with_emulator):
  url = BASE_URL + "/student/test_section_id"

  with mock.patch("routes.student.classroom_crud.list_student_section",
                  return_value=[{}, {}]):
    resp = client_with_emulator.get(url)
  assert resp.status_code == 200
