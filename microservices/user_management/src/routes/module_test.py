"""
  Unit tests for module endpoints
"""
import os
from copy import deepcopy
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.module import router
from testing.test_config import (API_URL, TESTING_FOLDER_PATH)
from schemas.schema_examples import BASIC_MODULE_MODEL_EXAMPLE, \
  BASIC_ACTION_MODEL_EXAMPLE
from common.models import Module, Action
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/user-management/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/module"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_get_module(clean_firestore):
  module_dict = {**BASIC_MODULE_MODEL_EXAMPLE}
  module = Module.from_dict(module_dict)
  module.uuid = ""
  module.save()
  module.uuid = module.id
  module.update()
  module_dict["uuid"] = module.id

  url = f"{api_url}/{module.uuid}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  del json_response["data"]["created_time"]
  del json_response["data"]["last_modified_time"]
  assert resp.status_code == 200, "Status 200"
  assert json_response.get("data") == module_dict, "Response received"


def test_get_module_negative(clean_firestore):
  """Get a module with incorrect uuid"""
  uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{uuid}"
  data = {
      "success": False,
      "message": f"Module with uuid {uuid} not found",
      "data": None
  }

  resp = client_with_emulator.get(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == data, "Response received"


def test_get_all_modules(clean_firestore):
  module_dict = {**BASIC_MODULE_MODEL_EXAMPLE}

  # module
  module = Module.from_dict(module_dict)
  module.uuid = ""
  module.save()
  module.uuid = module.id
  module.update()

  params = {"skip": 0, "limit": "30"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"
  retrieved_ids = [i.get("uuid") for i in json_response.get("data")]
  assert module.uuid in retrieved_ids, "expected data not retrieved"

def test_get_all_modules_negative_param(clean_firestore):
  module_dict = {**BASIC_MODULE_MODEL_EXAMPLE}

  # module
  module = Module.from_dict(module_dict)
  module.uuid = ""
  module.save()
  module.uuid = module.id
  module.update()

  params = {"skip": 0, "limit": "-3"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422, "Status should be 422"
  assert json_response["message"] == "Validation Failed"

def test_get_all_modules_negative(clean_firestore):
  module_dict = {**BASIC_MODULE_MODEL_EXAMPLE}

  # module
  module = Module.from_dict(module_dict)
  module.uuid = ""
  module.save()
  module.uuid = module.id
  module.update()

  params = {"skip": 0, "limit": "105"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422, "Status should be 422"
  assert json_response["message"] == "Validation Failed"


def test_post_module(clean_firestore):
  action_dict = {**BASIC_ACTION_MODEL_EXAMPLE}
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()
  action_dict["uuid"] = action.id

  input_module = {**BASIC_MODULE_MODEL_EXAMPLE, "actions": [action.id]}
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_module)
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
  loaded_module = Module.find_by_uuid(uuid)
  loaded_module_dict = loaded_module.to_dict()

  # popping id and key for equivalency test
  loaded_module_dict.pop("id")
  loaded_module_dict.pop("key")
  loaded_module_dict.pop("created_by")
  loaded_module_dict.pop("created_time")
  loaded_module_dict.pop("last_modified_by")
  loaded_module_dict.pop("last_modified_time")
  loaded_module_dict.pop("archived_at_timestamp")
  loaded_module_dict.pop("archived_by")
  loaded_module_dict.pop("deleted_at_timestamp")
  loaded_module_dict.pop("deleted_by")

  # assert that rest of the fields are equivalent
  assert loaded_module_dict == post_json_response.get("data")

def test_post_module_negative1(clean_firestore):
  module_dict = {**BASIC_MODULE_MODEL_EXAMPLE}
  module = Module.from_dict(module_dict)
  module.uuid = ""
  module.save()
  module.uuid = module.id
  module.update()

  input_module = BASIC_MODULE_MODEL_EXAMPLE
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_module)
  post_resp_json = post_resp.json()

  assert post_resp_json.get("success") is False, "Success not False"
  assert post_resp.status_code == 500
  assert post_resp_json.get("message") == \
    "Module with the given name: learning resource already exists"

def test_update_module(clean_firestore):
  action_dict = {**BASIC_ACTION_MODEL_EXAMPLE}
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()
  action_dict["uuid"] = action.id

  module_dict = {**BASIC_MODULE_MODEL_EXAMPLE, "actions": [action.id]}
  module = Module.from_dict(module_dict)
  module.uuid = ""
  module.save()
  module.uuid = module.id
  module.update()
  module_uuid = module.id

  url = f"{api_url}/{module_uuid}"
  updated_data = deepcopy(module_dict)
  updated_data["name"] = "new module name"
  resp = client_with_emulator.put(url, json=updated_data)
  update_response = resp.json()

  assert update_response.get("success") is True, "Success not true"
  assert update_response.get(
      "message"
  ) == "Successfully updated the module", "Expected response not same"
  assert update_response.get("data").get(
      "name") == "new module name", "Expected response not same"


def test_update_module_negative1(clean_firestore):
  module_dict = {**BASIC_MODULE_MODEL_EXAMPLE}
  module = Module.from_dict(module_dict)
  module.uuid = ""
  module.save()
  module.uuid = module.id
  module.update()
  uuid = "U2DDBkl3Ayg0PWudzhI"
  module_dict["name"] = "module-test"

  url = f"{api_url}/{uuid}"
  response = {
      "success": False,
      "message": "Module with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.put(url, json=module_dict)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"

def test_update_module_negative2(clean_firestore):
  module_dict = {**BASIC_MODULE_MODEL_EXAMPLE}
  module = Module.from_dict(module_dict)
  module.uuid = ""
  module.save()
  module.uuid = module.id
  module.update()
  uuid = "U2DDBkl3Ayg0PWudzhI"

  url = f"{api_url}/{uuid}"
  response = {
      "success": False,
      "message": "Module with the given name: learning resource already exists",
      "data": None
  }
  resp = client_with_emulator.put(url, json=module_dict)
  json_response = resp.json()

  assert resp.status_code == 500, "Status not 500"
  assert json_response == response, "Expected response not same"

def test_delete_module(clean_firestore):
  module_dict = {**BASIC_MODULE_MODEL_EXAMPLE}
  module = Module.from_dict(module_dict)
  module.uuid = ""
  module.save()
  module.uuid = module.id
  module.update()

  uuid = module.uuid
  module_dict["uuid"] = module.id

  url = f"{api_url}/{uuid}"
  resp = client_with_emulator.delete(url)
  del_json_response = resp.json()

  expected_data = {
      "success": True,
      "message": "Successfully deleted the module"
  }
  assert resp.status_code == 200, "Status code not 200"
  assert del_json_response == expected_data, "Expected response not same"


def test_delete_module_negative(clean_firestore):
  uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{uuid}"
  response = {
      "success": False,
      "message": "Module with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"
