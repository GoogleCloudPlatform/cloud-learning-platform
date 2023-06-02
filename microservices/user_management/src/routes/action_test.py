"""
  Unit tests for action endpoints
"""
import os
from copy import deepcopy
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.action import router
from testing.test_config import (API_URL, TESTING_FOLDER_PATH)
from schemas.schema_examples import BASIC_ACTION_MODEL_EXAMPLE
from common.models import Action
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/user-management/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/action"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_get_action(clean_firestore):
  action_dict = {**BASIC_ACTION_MODEL_EXAMPLE}
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()
  action_dict["uuid"] = action.id

  url = f"{api_url}/{action.uuid}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  del json_response["data"]["created_time"]
  del json_response["data"]["last_modified_time"]
  assert resp.status_code == 200, "Status 200"
  assert json_response.get("data") == action_dict, "Response received"


def test_get_action_negative(clean_firestore):
  """Get a action with incorrect uuid"""
  uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{uuid}"
  data = {
      "success": False,
      "message": f"Action with uuid {uuid} not found",
      "data": None
  }

  resp = client_with_emulator.get(url)
  json_response = resp.json()
  print(json_response)
  assert resp.status_code == 404, "Status 404"
  assert json_response == data, "Response received"


def test_get_all_actions(clean_firestore):
  action_dict = {**BASIC_ACTION_MODEL_EXAMPLE}

  # action
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()

  params = {"skip": 0, "limit": "30"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"
  retrieved_ids = [i.get("uuid") for i in json_response.get("data")]
  assert action.uuid in retrieved_ids, "expected data not retrieved"

def test_get_all_actions_negative_params(clean_firestore):
  action_dict = {**BASIC_ACTION_MODEL_EXAMPLE}

  # action
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()

  params = {"skip": -1, "limit": "30"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  assert resp.status_code == 422, "Status should be 422"

def test_get_all_actions_negative(clean_firestore):
  action_dict = {**BASIC_ACTION_MODEL_EXAMPLE}

  # action
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()

  params = {"skip": 0, "limit": "105"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422, "Status should be 422"
  assert json_response["message"] == "Validation Failed"

def test_post_action(clean_firestore):
  input_action = BASIC_ACTION_MODEL_EXAMPLE
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_action)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  post_json_response = post_resp.json()
  del post_json_response["data"]["created_time"]
  del post_json_response["data"]["last_modified_time"]
  uuid = post_json_response.get("data").get("uuid")

  # now see if GET endpoint returns same data
  url = f"{api_url}/{uuid}"
  get_resp = client_with_emulator.get(url)
  get_json_response = get_resp.json()
  del get_json_response["data"]["created_time"]
  del get_json_response["data"]["last_modified_time"]
  assert get_json_response.get("data") == post_json_response.get("data")

  # now check and confirm it is properly in the database
  loaded_action = Action.find_by_uuid(uuid)
  loaded_action_dict = loaded_action.to_dict()

  # popping id and key for equivalency test
  loaded_action_dict.pop("id")
  loaded_action_dict.pop("key")
  loaded_action_dict.pop("created_by")
  loaded_action_dict.pop("created_time")
  loaded_action_dict.pop("last_modified_by")
  loaded_action_dict.pop("last_modified_time")
  loaded_action_dict.pop("archived_at_timestamp")
  loaded_action_dict.pop("archived_by")
  loaded_action_dict.pop("deleted_at_timestamp")
  loaded_action_dict.pop("deleted_by")

  # assert that rest of the fields are equivalent
  assert loaded_action_dict == post_json_response.get("data")

def test_post_action_negative(clean_firestore):
  action_dict = {**BASIC_ACTION_MODEL_EXAMPLE}
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()

  input_action = BASIC_ACTION_MODEL_EXAMPLE
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_action)
  post_json_response = post_resp.json()

  assert post_json_response.get("success") is False, "Success not False"
  assert post_resp.status_code == 500
  assert post_json_response.get("message") == \
    "Action with the given name: edit already exists"

def test_update_action(clean_firestore):
  action_dict = {**BASIC_ACTION_MODEL_EXAMPLE}
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()
  action_uuid = action.id

  url = f"{api_url}/{action_uuid}"
  updated_data = deepcopy(action_dict)
  updated_data["name"] = "new action name"
  print(action_uuid)
  print("updated data", updated_data)
  resp = client_with_emulator.put(url, json=updated_data)
  update_response = resp.json()
  print("return data", update_response)

  assert update_response.get("success") is True, "Success not true"
  assert update_response.get(
      "message"
  ) == "Successfully updated the action", "Expected response not same"
  assert update_response.get("data").get(
      "name") == "new action name", "Expected response not same"


def test_update_action_negative1(clean_firestore):
  action_dict = {**BASIC_ACTION_MODEL_EXAMPLE}
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()
  uuid = "U2DDBkl3Ayg0PWudzhI"
  action_dict["name"] = "action-test"

  url = f"{api_url}/{uuid}"
  response = {
      "success": False,
      "message": "Action with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.put(url, json=action_dict)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_update_action_negative2(clean_firestore):
  action_dict = {**BASIC_ACTION_MODEL_EXAMPLE}
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()
  uuid = "U2DDBkl3Ayg0PWudzhI"

  url = f"{api_url}/{uuid}"
  response = {
      "success": False,
      "message": f"Action with the given name: {action.name} already exists",
      "data": None
  }
  resp = client_with_emulator.put(url, json=action_dict)
  json_response = resp.json()

  assert resp.status_code == 500, "Status not 500"
  assert json_response == response, "Expected response not same"

def test_delete_action(clean_firestore):
  action_dict = {**BASIC_ACTION_MODEL_EXAMPLE}
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()

  uuid = action.uuid
  action_dict["uuid"] = action.id

  url = f"{api_url}/{uuid}"
  resp = client_with_emulator.delete(url)
  del_json_response = resp.json()

  expected_data = {
      "success": True,
      "message": "Successfully deleted the action"
  }
  assert resp.status_code == 200, "Status code not 200"
  assert del_json_response == expected_data, "Expected response not same"


def test_delete_action_negative(clean_firestore):
  uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{uuid}"
  response = {
      "success": False,
      "message": "Action with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"
