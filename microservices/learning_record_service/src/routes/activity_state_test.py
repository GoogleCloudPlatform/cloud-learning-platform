"""
  Unit Tests for Activity State endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
import os
import pytest
from copy import deepcopy
from fastapi import FastAPI
from fastapi.testclient import TestClient
from testing.test_config import API_URL, TESTING_FOLDER_PATH
from routes.activity_state import router
from schemas.schema_examples import BASIC_ACTIVITY_STATE_MODEL_EXAMPLE
from common.models import ActivityState
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/learning-record-service/api/v1")

client_with_emulator = TestClient(app)

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_post_and_get_activity_state(clean_firestore):
  activity_state_dict = deepcopy(BASIC_ACTIVITY_STATE_MODEL_EXAMPLE)

  url = f"{API_URL}/activity-state"
  resp = client_with_emulator.post(url, json=activity_state_dict)
  json_response = resp.json()
  activity_state_uuid = json_response["data"]["uuid"]

  assert resp.status_code == 200, "Status is not 200"
  assert json_response.get("success") is True, "Success not true"
  assert json_response.get("message") == \
    "Successfully created the activity state", "Expected response not same"
  assert json_response.get("data").get("agent_id") == activity_state_dict.get(
      "agent_id"), "Expected response not same"

  url = f"{API_URL}/activity-state/{activity_state_uuid}"
  resp = client_with_emulator.get(url)
  json_response_get_req = resp.json()

  assert resp.status_code == 200, "Status code not 200"
  assert json_response_get_req.get("data") == json_response.get(
      "data"), "Expected response not same"


def test_get_activity_state_negative(clean_firestore):
  invalid_activity_state_uuid = "random_id"
  url = f"{API_URL}/activity-state/{invalid_activity_state_uuid}"
  response = {
      "success": False,
      "message": "Activity State with uuid random_id not found",
      "data": None
  }
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_delete_activity_state_positive(clean_firestore):
  activity_state_dict = deepcopy(BASIC_ACTIVITY_STATE_MODEL_EXAMPLE)

  url = f"{API_URL}/activity-state"
  resp = client_with_emulator.post(url, json=activity_state_dict)
  json_response = resp.json()
  activity_state_uuid = json_response["data"]["uuid"]

  url = f"{API_URL}/activity-state/{activity_state_uuid}"
  resp = client_with_emulator.delete(url)
  json_response_delete_req = resp.json()

  expected_data = {
      "success": True,
      "message": "Successfully deleted the activity state"
  }
  assert resp.status_code == 200, "Status code not 200"
  assert json_response_delete_req == expected_data, "Expected response not same"


def test_delete_activity_state_negative(clean_firestore):
  invalid_activity_state_uuid = "random_id"
  url = f"{API_URL}/activity-state/{invalid_activity_state_uuid}"
  response = {
      "success": False,
      "message": "Activity State with uuid random_id not found",
      "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_update_activity_state_positive(clean_firestore):
  activity_state_dict = deepcopy(BASIC_ACTIVITY_STATE_MODEL_EXAMPLE)
  url = f"{API_URL}/activity-state"

  resp = client_with_emulator.post(url, json=activity_state_dict)
  json_response = resp.json()

  updated_data = json_response["data"]
  updated_data["agent_id"] = "updated_agent_id"

  uuid = updated_data.get("uuid")
  url = f"{API_URL}/activity-state/{uuid}"
  resp = client_with_emulator.put(url, json=updated_data)
  json_response_update_req = resp.json()

  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get("message") == \
    "Successfully updated the activity state", "Expected response not same"
  assert json_response_update_req.get("data").get("agent_id") == \
    "updated_agent_id", "Expected response not same"


def test_update_activity_state_negative(clean_firestore):
  req_json = deepcopy(BASIC_ACTIVITY_STATE_MODEL_EXAMPLE)
  uuid = req_json["uuid"] = "random_id"
  response = {
      "success": False,
      "message": "Activity State with uuid random_id not found",
      "data": None
  }

  url = f"{API_URL}/activity-state/{uuid}"
  resp = client_with_emulator.put(url, json=req_json)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_import_activity_state(clean_firestore):
  url = f"{API_URL}/activity-state/import/json"
  file_path = os.path.join(TESTING_FOLDER_PATH, "activity_states.json")
  with open(file_path, "rb") as file:
    resp = client_with_emulator.post(url, files={"json_file": file})

  json_response = resp.json()

  assert resp.status_code == 200, "Success not 200"
  assert isinstance(json_response.get("data"), list), "Response is not a list"
  assert len(json_response.get("data")) == 3, "returned length is not same"


def test_get_activity_states(clean_firestore):
  activity_state_dict = deepcopy(BASIC_ACTIVITY_STATE_MODEL_EXAMPLE)
  activity_state_dict["agent_id"] = "agent_id_new"
  activity_state = ActivityState.from_dict(activity_state_dict)
  activity_state.uuid = ""
  activity_state.save()
  activity_state.uuid = activity_state.id
  activity_state.update()
  params = {"skip": 0, "limit": "30"}

  url = f"{API_URL}/activity-states"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  saved_agent_ids = [i.get("agent_id") for i in json_response.get(
    "data")["records"]]
  assert activity_state_dict["agent_id"] in saved_agent_ids,\
    "all data not retrieved"


def test_get_activity_states_negative(clean_firestore):
  activity_state_dict = deepcopy(BASIC_ACTIVITY_STATE_MODEL_EXAMPLE)
  activity_state = ActivityState.from_dict(activity_state_dict)
  activity_state.uuid = ""
  activity_state.save()
  activity_state.uuid = activity_state.id
  activity_state.update()
  params = {"skip": "-1", "limit": "30"}

  url = f"{API_URL}/activity-states"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422, "Status not 422"
  assert json_response.get("message") == \
    "Validation Failed", \
    "unknown response received"
