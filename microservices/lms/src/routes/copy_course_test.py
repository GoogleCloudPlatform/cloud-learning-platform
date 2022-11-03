"""
  Tests for User endpoints
"""
import os
import json
import datetime
from routes import copy_course
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from common.testing.firestore_emulator import client_with_emulator, firestore_emulator, clean_firestore

from common.models import User
import mock

# assigning url
API_URL = "http://localhost/lms/api/v1"


os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"
SUCCESS_RESPONSE = {"status": "Success"}


def test_get_user(client_with_emulator):
  url = API_URL + "/course/get_courses/"
  print(url)
  with mock.patch("routes.copy_course.classroom_crud.get_course_list"):
    resp = client_with_emulator.get(url)
#   json_response = json.loads(resp)
  print(resp.json())
  assert resp.status_code == 200


def test_copy_course(client_with_emulator):
  url = API_URL + "/course/copy_course/"
  course_details = {"course_id":"TEST123"}
  with mock.patch("routes.copy_course.classroom_crud.get_course_by_id"):
      with mock.patch("routes.copy_course.classroom_crud.create_course"):
          with mock.patch("routes.copy_course.classroom_crud.get_topics"):
              with mock.patch("routes.copy_course.classroom_crud.create_topics"):
                with mock.patch("routes.copy_course.classroom_crud.get_coursework"):
                    with mock.patch("routes.copy_course.classroom_crud.create_coursework"):
                        resp = client_with_emulator.post(url,json=course_details)
  json_response = json.loads(resp.text)
  assert resp.status_code == 200    


def test_copy_course_not_found(client_with_emulator):
  url = API_URL + "/course/copy_course/"
  course_details = {"course_id":"TEST123"}
  with mock.patch("routes.copy_course.classroom_crud.get_course_by_id",return_value =None):
      with mock.patch("routes.copy_course.classroom_crud.create_course"):
          with mock.patch("routes.copy_course.classroom_crud.get_topics"):
              with mock.patch("routes.copy_course.classroom_crud.create_topics"):
                with mock.patch("routes.copy_course.classroom_crud.get_coursework"):
                    with mock.patch("routes.copy_course.classroom_crud.create_coursework"):
                        resp = client_with_emulator.post(url,json=course_details)
  print(resp.json())
  assert resp.status_code == 200   