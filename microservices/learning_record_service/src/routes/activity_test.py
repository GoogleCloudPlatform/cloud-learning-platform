"""
  Tests for Activity endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
import os
import json
import pytest
from copy import deepcopy
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.activity import router
from testing.test_config import API_URL, TESTING_FOLDER_PATH
from schemas.schema_examples import BASIC_ACTIVITY_EXAMPLE
from common.models import Activity
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/learning-record-service/api/v1")

client_with_emulator = TestClient(app)

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


@pytest.fixture(name="add_data")
def add_data():
  activity_dict = deepcopy(BASIC_ACTIVITY_EXAMPLE)
  activity = Activity.from_dict(activity_dict)
  activity.uuid = ""
  activity.save()
  activity.uuid = activity.id
  activity.update()

  return [activity.uuid]


def test_post_and_get_activity(clean_firestore):

  activity_dict = deepcopy(BASIC_ACTIVITY_EXAMPLE)

  url = f"{API_URL}/activity"
  resp = client_with_emulator.post(url, json=activity_dict)
  json_response = resp.json()
  activity_uuid = json_response["data"]["uuid"]

  assert resp.status_code == 200, "Status 200"
  assert json_response.get("success") is True, "Success not true"
  assert json_response.get(
      "message"
  ) == "Successfully created the activity", "Expected response not same"
  assert json_response.get("data").get("name") == activity_dict.get(
      "name"), "Expected response not same"

  url = f"{API_URL}/activity/{activity_uuid}"
  resp = client_with_emulator.get(url)
  json_response_get_req = resp.json()

  assert resp.status_code == 200, "Status code not 200"
  assert json_response_get_req.get("data") == json_response.get(
      "data"), "Expected response not same"


def test_get_activity_negative(clean_firestore):
  activity_uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{API_URL}/activity/{activity_uuid}"
  response = {
      "success": False,
      "message": "Activity with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_delete_activity_positive(clean_firestore):
  activity_dict = deepcopy(BASIC_ACTIVITY_EXAMPLE)

  url = f"{API_URL}/activity"
  resp = client_with_emulator.post(url, json=activity_dict)
  json_response = resp.json()

  activity_uuid = json_response["data"]["uuid"]

  url = f"{API_URL}/activity/{activity_uuid}"
  resp = client_with_emulator.delete(url)
  json_response_delete_req = resp.json()

  expected_data = {
      "success": True,
      "message": "Successfully deleted the Activity"
  }
  assert resp.status_code == 200, "Status code not 200"
  assert json_response_delete_req == expected_data, "Expected response not same"


def test_delete_activity_negative(clean_firestore):
  activity_uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{API_URL}/activity/{activity_uuid}"
  response = {
      "success": False,
      "message": "Activity with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_update_activity_positive(clean_firestore):
  activity_dict = deepcopy(BASIC_ACTIVITY_EXAMPLE)

  url = f"{API_URL}/activity"
  resp = client_with_emulator.post(url, json=activity_dict)
  json_response = resp.json()

  updated_data = json_response["data"]
  updated_data["name"] = "some random name"

  uuid = updated_data.get("uuid")
  url = f"{API_URL}/activity/{uuid}"
  resp = client_with_emulator.put(url, json=updated_data)
  json_response_update_req = resp.json()

  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get(
      "message"
  ) == "Successfully updated the activity", "Expected response not same"
  assert json_response_update_req.get("data").get(
      "name") == "some random name", "Expected response not same"


def test_update_activity_negative(clean_firestore):
  req_json = deepcopy(BASIC_ACTIVITY_EXAMPLE)
  uuid = req_json["uuid"] = "U2DDBkl3Ayg0PWudzhI"
  response = {
      "success": False,
      "message": "Activity with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }

  url = f"{API_URL}/activity/{uuid}"
  resp = client_with_emulator.put(url, json=req_json)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_import_activities(clean_firestore):
  url = f"{API_URL}/activity/import/json"
  file_path = os.path.join(TESTING_FOLDER_PATH, "activities.json")
  with open(file_path, "rb") as file:
    resp = client_with_emulator.post(url, files={"json_file": file})

  json_response = resp.json()

  assert resp.status_code == 200, "Success not 200"
  assert isinstance(json_response.get("data"), list), "Response is not a list"
  assert len(json_response.get("data")) > 0, "Empty list returned"


def test_get_activities(clean_firestore):
  activity_dict = deepcopy(BASIC_ACTIVITY_EXAMPLE)
  activity = Activity.from_dict(activity_dict)
  activity.uuid = ""
  activity.save()
  activity.uuid = activity.id
  activity.update()
  params = {"skip": 0, "limit": "30"}

  url = f"{API_URL}/activities"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  saved_names = [i.get("name") for i in json_response.get("data")]
  assert activity_dict["name"] in saved_names, "all data not retrieved"

  agent = activity_dict.get("name")

  url = f"{API_URL}/activities?agent={agent}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"


def test_get_activities_negative(clean_firestore):
  activity_dict = deepcopy(BASIC_ACTIVITY_EXAMPLE)
  activity = Activity.from_dict(activity_dict)
  activity.uuid = ""
  activity.save()
  activity.uuid = activity.id
  activity.update()
  params = {"skip": "-1", "limit": "30"}

  url = f"{API_URL}/activities"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422, "Status not 422"
  assert json_response.get(
    "message"
  ) == "Validation Failed", \
    "unknown response received"
