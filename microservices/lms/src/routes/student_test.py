"""
  Tests for User endpoints
"""
import os
import json
import datetime
from routes import copy_course
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
# from common.testing.firestore_emulator import client_with_emulator, firestore_emulator, clean_firestore
from common.testing.firestore_emulator import firestore_emulator, clean_firestore
from common.testing.client_with_emulator import client_with_emulator

from common.models import User
import mock

# assigning url
API_URL = "http://localhost/lms/api/v1"


os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"
SUCCESS_RESPONSE = {"status": "Success"}


def test_get_student_course_progress_percent(client_with_emulator):
  url = API_URL + "/student/get_progress_percentage/?course_id=504551481098&student_email=test_user_1@dhodun.altostrat.com"
  with mock.patch("routes.student.classroom_crud.get_course_work_list", return_value = [{},{}]):
      with mock.patch("routes.student.classroom_crud.get_submitted_course_work_list", return_value = [{"state":"TURNED_IN"},{"state":"TURNED_IN"}]):
        resp = client_with_emulator.get(url)
  json_response = json.loads(resp.text)
  assert resp.status_code == 200  