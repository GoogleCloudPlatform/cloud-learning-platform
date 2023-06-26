"""
  Unit tests for module endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import

import os
import pytest

from copy import deepcopy
from fastapi import FastAPI
from fastapi.testclient import TestClient

from routes.application import router
from testing.test_config import (API_URL, TESTING_FOLDER_PATH)
from schemas.schema_examples import BASIC_ACTION_MODEL_EXAMPLE, \
  BASIC_APPLICATION_MODEL_EXAMPLE, BASIC_GROUP_MODEL_EXAMPLE, \
  BASIC_PERMISSION_MODEL_EXAMPLE, BASIC_MODULE_MODEL_EXAMPLE

from common.models import Application, Action, Permission, UserGroup, Module
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers
from common.utils.errors import ResourceNotFoundException

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/user-management/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/application"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_get_application(clean_firestore):
  application_dict = {**BASIC_APPLICATION_MODEL_EXAMPLE}
  application = Application.from_dict(application_dict)
  application.uuid = ""
  application.save()
  application.uuid = application.id
  application.update()
  application_dict["uuid"] = application.id

  url = f"{api_url}/{application.uuid}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  del json_response["data"]["created_time"]
  del json_response["data"]["last_modified_time"]
  assert resp.status_code == 200, "Status 200"
  assert json_response.get("data") == application_dict, "Response received"


def test_get_application_negative(clean_firestore):
  """Get a module with incorrect uuid"""
  uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{uuid}"
  data = {
    "success": False,
    "message": f"Application with uuid {uuid} not found",
    "data": None
  }

  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 404, "Status 404"
  assert json_response == data, "Response received"


def test_get_all_applications(clean_firestore):
  application_dict = {**BASIC_APPLICATION_MODEL_EXAMPLE}

  # module
  application = Application.from_dict(application_dict)
  application.uuid = ""
  application.save()
  application.uuid = application.id
  application.update()

  params = {"skip": 0, "limit": "30"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"
  retrieved_ids = [i.get("uuid") for i in json_response.get("data")]
  assert application.uuid in retrieved_ids, "Response received"


def test_get_all_applications_negative(clean_firestore):
  application_dict = {**BASIC_APPLICATION_MODEL_EXAMPLE}

  # module
  application = Application.from_dict(application_dict)
  application.uuid = ""
  application.save()
  application.uuid = application.id
  application.update()

  params = {"skip": 0, "limit": "105"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422, "Status should be 422"
  assert json_response["message"] == "Validation Failed"


def test_post_application(clean_firestore):
  action_dict = {**BASIC_ACTION_MODEL_EXAMPLE,
                 "name": "view"}
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()

  module_dict = {**BASIC_MODULE_MODEL_EXAMPLE}
  module = Module.from_dict(module_dict)
  module.uuid = ""
  module.save()
  module.uuid = module.id
  module.update()

  input_application = {**BASIC_APPLICATION_MODEL_EXAMPLE, "modules": [
    module.id]}
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_application)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Response received"
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
  loaded_application = Application.find_by_uuid(uuid)
  loaded_application_dict = loaded_application.to_dict()

  # popping id and key for equivalency test
  loaded_application_dict.pop("id")
  loaded_application_dict.pop("key")
  loaded_application_dict.pop("created_by")
  loaded_application_dict.pop("created_time")
  loaded_application_dict.pop("last_modified_by")
  loaded_application_dict.pop("last_modified_time")
  loaded_application_dict.pop("archived_at_timestamp")
  loaded_application_dict.pop("archived_by")
  loaded_application_dict.pop("deleted_at_timestamp")
  loaded_application_dict.pop("deleted_by")

  # assert that rest of the fields are equivalent
  assert loaded_application_dict == post_json_response.get("data")


def test_post_application_negative(clean_firestore):
  application_dict = {**BASIC_APPLICATION_MODEL_EXAMPLE}
  application = Application.from_dict(application_dict)
  application.uuid = ""
  application.save()
  application.uuid = application.id
  application.update()

  input_application = BASIC_APPLICATION_MODEL_EXAMPLE
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_application)
  post_resp_json = post_resp.json()

  assert post_resp_json.get("success") is False, "Success not False"
  assert post_resp.status_code == 409
  assert post_resp_json.get("message") == \
         "Application with the given name: content management already exists"

def test_post_application_negative_1(clean_firestore):
  input_application = {
    **BASIC_APPLICATION_MODEL_EXAMPLE,
    "name":""}
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_application)
  post_resp_json = post_resp.json()

  assert post_resp_json.get("success") is False, "Success not False"
  assert post_resp.status_code == 422
  assert post_resp_json.get("message") == "Validation Failed"

def test_update_application(clean_firestore):
  action_dict = {**BASIC_ACTION_MODEL_EXAMPLE,
                 "name": "view"}
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()

  module_dict = {**BASIC_MODULE_MODEL_EXAMPLE}
  module = Module.from_dict(module_dict)
  module.uuid = ""
  module.save()
  module.uuid = module.id
  module.update()

  application_dict = {**BASIC_APPLICATION_MODEL_EXAMPLE, "modules": [
    module.id]}
  application = Application.from_dict(application_dict)
  application.uuid = ""
  application.save()
  application.uuid = application.id
  application.update()
  application_uuid = application.id

  url = f"{api_url}/{application_uuid}"
  updated_data = deepcopy(application_dict)
  updated_data["name"] = "new application name"
  resp = client_with_emulator.put(url, json=updated_data)
  update_response = resp.json()

  assert update_response.get("success") is True, "Success"
  assert update_response.get(
    "message") == "Successfully updated the application", "Response received"
  assert update_response.get("data").get(
    "name") == "new application name", "Response received"


def test_update_application_negative1(clean_firestore):
  action_dict = {**BASIC_ACTION_MODEL_EXAMPLE,
                 "name": "view"}
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()

  module_dict = {**BASIC_MODULE_MODEL_EXAMPLE}
  module = Module.from_dict(module_dict)
  module.uuid = ""
  module.save()
  module.uuid = module.id
  module.update()

  application_dict = {**BASIC_APPLICATION_MODEL_EXAMPLE, "modules": [
    module.id]}
  application = Application.from_dict(application_dict)
  application.uuid = ""
  application.save()
  application.uuid = application.id
  application.update()
  uuid = "U2DDBkl3Ayg0PWudzhI"
  application_dict["name"] = "application_test"

  url = f"{api_url}/{uuid}"
  response = {
    "success": False,
    "message": "Application with uuid U2DDBkl3Ayg0PWudzhI not found",
    "data": None
  }
  resp = client_with_emulator.put(url, json=application_dict)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Response received"


def test_update_application_negative2(clean_firestore):
  application_dict = {**BASIC_APPLICATION_MODEL_EXAMPLE}
  application = Application.from_dict(application_dict)
  application.uuid = ""
  application.save()
  application.uuid = application.id
  application.update()
  uuid = "U2DDBkl3Ayg0PWudzhI"

  url = f"{api_url}/{uuid}"
  response = {
    "success": False,
    "message": \
      "Application with the given name: content management already exists",
    "data": None
  }
  resp = client_with_emulator.put(url, json=application_dict)
  json_response = resp.json()

  assert resp.status_code == 500, "Status not 500"
  assert json_response == response, "Response received"


def test_delete_application(clean_firestore):
  application_dict = {**BASIC_APPLICATION_MODEL_EXAMPLE}
  application = Application.from_dict(application_dict)
  application.uuid = ""
  application.save()
  application.uuid = application.id
  application.update()

  uuid = application.uuid
  application_dict["uuid"] = application.id

  url = f"{api_url}/{uuid}"
  resp = client_with_emulator.delete(url)
  del_json_response = resp.json()

  expected_data = {
    "success": True,
    "message": "Successfully deleted the application"
  }
  assert resp.status_code == 200, "Status code 200"
  assert del_json_response == expected_data, "Response received"


def test_delete_application_negative(clean_firestore):
  uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{uuid}"
  response = {
    "success": False,
    "message": "Application with uuid U2DDBkl3Ayg0PWudzhI not found",
    "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Response received"


def test_update_refs_on_application_deletion(clean_firestore):
  group_dict = {**BASIC_GROUP_MODEL_EXAMPLE, "users": []}
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()

  application_dict = {**BASIC_APPLICATION_MODEL_EXAMPLE}
  application = Application.from_dict(application_dict)
  application.uuid = ""
  application.save()
  application.uuid = application.id
  application.update()

  action_dict = {**BASIC_ACTION_MODEL_EXAMPLE,
                 "name": "view"}
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()

  permission_dict = {**BASIC_PERMISSION_MODEL_EXAMPLE,
                     "application_id": application.id, "action_id": action.id}
  permission = Permission.from_dict(permission_dict)
  permission.uuid = ""
  permission.save()
  permission.uuid = permission.id
  permission.update()

  group.applications = [application.id]
  group.permissions = [permission.id]
  group.update()

  permission.user_groups = [group.id]
  permission.update()

  url = f"{api_url}/{application.id}"
  resp = client_with_emulator.delete(url)
  assert resp.status_code == 200, "Status coded not 200"

  with pytest.raises(ResourceNotFoundException):
    Application.find_by_uuid(application.id)
  with pytest.raises(ResourceNotFoundException):
    Permission.find_by_uuid(permission.id)

  user_group = UserGroup.find_by_uuid(group.id)
  user_group_fields = user_group.get_fields()
  assert permission not in user_group_fields.get("permissions")
  assert application not in user_group_fields.get("applications")
