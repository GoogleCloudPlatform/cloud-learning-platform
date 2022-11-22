"""
  Tests for User endpoints
"""
import os
import json
import datetime
from routes import copy_course
from common.testing.firestore_emulator import firestore_emulator, clean_firestore
from common.testing.client_with_emulator import client_with_emulator
from common.models import User
from testing.test_config import BASE_URL
import mock


os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"
SUCCESS_RESPONSE = {"status": "Success"}


def test_get_student_course_progress_percent(client_with_emulator):
  url = BASE_URL + "/student/get_progress_percentage/?course_id=504551481098&student_email=test_user_1@dhodun.altostrat.com"
  with mock.patch("routes.student.classroom_crud.get_course_work_list", return_value = [{},{}]):
      with mock.patch("routes.student.classroom_crud.get_submitted_course_work_list", return_value = [{"state":"TURNED_IN"},{"state":"TURNED_IN"}]):
        resp = client_with_emulator.get(url)
  json_response = json.loads(resp.text)
  assert resp.status_code == 200  