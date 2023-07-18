"""
  Unit tests for permission endpoints
"""
import os
from copy import deepcopy
from uuid import uuid4
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.permission import router
from testing.test_config import (API_URL, TESTING_FOLDER_PATH)
from schemas.schema_examples import (BASIC_PERMISSION_MODEL_EXAMPLE,
                                     BASIC_ACTION_MODEL_EXAMPLE,
                                     BASIC_MODULE_MODEL_EXAMPLE,
                                     BASIC_APPLICATION_MODEL_EXAMPLE,
                                     BASIC_GROUP_MODEL_EXAMPLE,
                                     POST_USERGROUP_MODEL_EXAMPLE)
from common.models import Permission, Action, Module, Application, UserGroup
from common.utils.collection_references import collection_references
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/user-management/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/permission"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def create_documents(collection_name, input_body):
  doc = collection_references[collection_name].from_dict(input_body)
  doc.uuid = ""
  doc.save()
  doc.uuid = doc.id
  doc.update()
  return doc.uuid


def test_get_permission(clean_firestore):
  permission_dict = {
    **BASIC_PERMISSION_MODEL_EXAMPLE,
    "application_id": create_documents("applications", {
      **BASIC_APPLICATION_MODEL_EXAMPLE, "modules": []
    }),
    "module_id": create_documents("modules", {
      **BASIC_MODULE_MODEL_EXAMPLE, "actions": []
    }),
    "action_id": create_documents("actions", {**BASIC_ACTION_MODEL_EXAMPLE}),
    "user_groups": []
  }

  permission = Permission.from_dict(permission_dict)
  permission.uuid = ""
  permission.save()
  permission.uuid = permission.id
  permission.update()
  permission_dict["uuid"] = permission.id

  url = f"{api_url}/{permission.uuid}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  del json_response["data"]["created_time"]
  del json_response["data"]["last_modified_time"]
  assert resp.status_code == 200, "Status 200"
  assert json_response.get("data") == permission_dict, "Response received"


def test_get_permission_negative(clean_firestore):
  """Get a permission with incorrect uuid"""
  uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{uuid}"
  data = {
    "success": False,
    "message": f"Permission with uuid {uuid} not found",
    "data": None
  }

  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 404, "Status 404"
  assert json_response == data, "Response received"


def test_get_all_permissions(clean_firestore):
  permission_dict = {**BASIC_PERMISSION_MODEL_EXAMPLE}
  permission = Permission.from_dict(permission_dict)
  permission.uuid = ""
  permission.save()
  permission.uuid = permission.id
  permission.update()

  params = {"skip": 0, "limit": "30"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"
  retrieved_ids = [i.get("uuid") for i in json_response.get("data")["records"]]
  assert permission.uuid in retrieved_ids, "expected data not retrieved"


def test_get_all_applications_negative(clean_firestore):
  params = {"skip": 0, "limit": "105"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422, "Status should be 422"
  assert json_response["message"] == "Validation Failed"


def test_get_all_permissions_by_application_id(clean_firestore):
  permission_dict = {**BASIC_PERMISSION_MODEL_EXAMPLE}
  permission_dict["application_id"] = "Dfchd56otyghfgfjioiK"
  permission = Permission.from_dict(permission_dict)
  permission.uuid = ""
  permission.save()
  permission.uuid = permission.id
  permission.update()

  params = {
    "skip": 0,
    "limit": "50",
    "application_id": permission_dict["application_id"]
  }

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"
  assert json_response["data"][
    "records"][0]["application_id"] == permission_dict[
    "application_id"]


def test_permission_search(clean_firestore):
  permission_dict = {
    **BASIC_PERMISSION_MODEL_EXAMPLE,
    "application_id": create_documents("applications", {
      **BASIC_APPLICATION_MODEL_EXAMPLE, "modules": []
    }),
    "module_id": create_documents("modules", {
      **BASIC_MODULE_MODEL_EXAMPLE, "actions": []
    }),
    "action_id": create_documents("actions", {**BASIC_ACTION_MODEL_EXAMPLE}),
    "user_groups": []
  }
  permission = Permission.from_dict(permission_dict)
  permission.uuid = ""
  permission.save()
  permission.uuid = permission.id
  permission.update()

  params = {"search_query": "assessment", "skip": 0, "limit": 30}

  url = f"{api_url}/search"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"
  retrieved_ids = [i.get(
    "uuid") for i in json_response.get("data")["records"]]
  assert permission.uuid in retrieved_ids, "expected data not retrieved"


def test_application_search(clean_firestore):
  permission_dict = {
    **BASIC_PERMISSION_MODEL_EXAMPLE,
    "application_id": create_documents("applications", {
      **BASIC_APPLICATION_MODEL_EXAMPLE, "modules": []
    }),
    "module_id": create_documents("modules", {
      **BASIC_MODULE_MODEL_EXAMPLE, "actions": []
    }),
    "action_id": create_documents("actions", {**BASIC_ACTION_MODEL_EXAMPLE}),
    "user_groups": []
  }
  permission = Permission.from_dict(permission_dict)
  permission.uuid = ""
  permission.save()
  permission.uuid = permission.id
  permission.update()

  params = {"search_query": BASIC_APPLICATION_MODEL_EXAMPLE["name"]}

  url = f"{api_url}/search"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"
  retrieved_ids = [i.get(
    "uuid") for i in json_response.get("data")["records"]]
  assert permission.uuid in retrieved_ids, "expected data not retrieved"


def test_module_search(clean_firestore):
  permission_dict = {
    **BASIC_PERMISSION_MODEL_EXAMPLE,
    "application_id": create_documents("applications", {
      **BASIC_APPLICATION_MODEL_EXAMPLE, "modules": []
    }),
    "module_id": create_documents("modules", {
      **BASIC_MODULE_MODEL_EXAMPLE, "actions": []
    }),
    "action_id": create_documents("actions", {**BASIC_ACTION_MODEL_EXAMPLE}),
    "user_groups": []
  }
  permission = Permission.from_dict(permission_dict)
  permission.uuid = ""
  permission.save()
  permission.uuid = permission.id
  permission.update()

  params = {"search_query": BASIC_MODULE_MODEL_EXAMPLE["name"]}

  url = f"{api_url}/search"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"
  retrieved_ids = [i.get(
    "uuid") for i in json_response.get("data")["records"]]
  assert permission.uuid in retrieved_ids, "expected data not retrieved"


def test_action_search(clean_firestore):
  permission_dict = {
    **BASIC_PERMISSION_MODEL_EXAMPLE,
    "application_id": create_documents("applications", {
      **BASIC_APPLICATION_MODEL_EXAMPLE, "modules": []
    }),
    "module_id": create_documents("modules", {
      **BASIC_MODULE_MODEL_EXAMPLE, "actions": []
    }),
    "action_id": create_documents("actions", {**BASIC_ACTION_MODEL_EXAMPLE}),
    "user_groups": []
  }
  permission = Permission.from_dict(permission_dict)
  permission.uuid = ""
  permission.save()
  permission.uuid = permission.id
  permission.update()

  params = {"search_query": BASIC_ACTION_MODEL_EXAMPLE["name"]}

  url = f"{api_url}/search"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"
  retrieved_ids = [i.get(
    "uuid") for i in json_response.get("data")["records"]]
  assert permission.uuid in retrieved_ids, "expected data not retrieved"


def test_permission_search_negative(clean_firestore):
  permission_dict = {
    **BASIC_PERMISSION_MODEL_EXAMPLE,
    "application_id": create_documents("applications", {
      **BASIC_APPLICATION_MODEL_EXAMPLE, "modules": []
    }),
    "module_id": create_documents("modules", {
      **BASIC_MODULE_MODEL_EXAMPLE, "actions": []
    }),
    "action_id": create_documents("actions", {**BASIC_ACTION_MODEL_EXAMPLE}),
    "user_groups": []
  }
  permission = Permission.from_dict(permission_dict)
  permission.uuid = ""
  permission.save()
  permission.uuid = permission.id
  permission.update()

  params = {"search_query": "Hello"}

  url = f"{api_url}/search"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"
  assert json_response["data"]["records"] == []


def test_post_permission(clean_firestore):
  permission_dict = {
    **BASIC_PERMISSION_MODEL_EXAMPLE,
    "application_id": create_documents("applications", {
      **BASIC_APPLICATION_MODEL_EXAMPLE, "modules": []
    }),
    "module_id": create_documents("modules", {
      **BASIC_MODULE_MODEL_EXAMPLE, "actions": []
    }),
    "action_id": create_documents("actions", {**BASIC_ACTION_MODEL_EXAMPLE})
  }
  del permission_dict["user_groups"]
  url = api_url
  post_resp = client_with_emulator.post(url, json=permission_dict)
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
  loaded_permission = Permission.find_by_uuid(uuid)
  loaded_permission_dict = loaded_permission.to_dict()

  # popping id and key for equivalency test
  loaded_permission_dict.pop("id")
  loaded_permission_dict.pop("key")
  loaded_permission_dict.pop("created_by")
  loaded_permission_dict.pop("created_time")
  loaded_permission_dict.pop("last_modified_by")
  loaded_permission_dict.pop("last_modified_time")

  # assert that rest of the fields are equivalent
  assert loaded_permission_dict == post_json_response.get("data")


def test_update_permission(clean_firestore):
  permission_dict = {
    **BASIC_PERMISSION_MODEL_EXAMPLE,
    "application_id": create_documents("applications", {
      **BASIC_APPLICATION_MODEL_EXAMPLE, "modules": []
    }),
    "module_id": create_documents("modules", {
      **BASIC_MODULE_MODEL_EXAMPLE, "actions": []
    }),
    "action_id": create_documents("actions", {**BASIC_ACTION_MODEL_EXAMPLE}),
    "user_groups": []
  }
  permission = Permission.from_dict(permission_dict)
  permission.uuid = ""
  permission.save()
  permission.uuid = permission.id
  permission.update()
  permission_uuid = permission.id

  url = f"{api_url}/{permission_uuid}"
  updated_data = {"name": "new permission name"}
  resp = client_with_emulator.put(url, json=updated_data)
  update_response = resp.json()

  assert update_response.get("success") is True, "Success not true"
  assert update_response.get(
    "message"
  ) == "Successfully updated the permission", "Expected response not same"
  assert update_response.get("data").get(
    "name") == "new permission name", "Expected response not same"


def test_update_permission_negative(clean_firestore):
  permission_dict = {**BASIC_PERMISSION_MODEL_EXAMPLE}
  del permission_dict["user_groups"]
  permission = Permission.from_dict(permission_dict)
  permission.uuid = ""
  permission.save()
  permission.uuid = permission.id
  permission.update()
  uuid = "U2DDBkl3Ayg0PWudzhI"

  url = f"{api_url}/{uuid}"
  response = {
    "success": False,
    "message": "Permission with uuid U2DDBkl3Ayg0PWudzhI not found",
    "data": None
  }
  resp = client_with_emulator.put(
    url, json={"name": "random", "description": "random descr"})
  json_response = resp.json()
  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_delete_permission(clean_firestore):
  permission_dict = {
    **BASIC_PERMISSION_MODEL_EXAMPLE, "user_groups": ["test_group_id"]
  }
  permission = Permission.from_dict(permission_dict)
  permission.uuid = ""
  permission.save()
  permission.uuid = permission.id
  permission.update()

  uuid = permission.uuid
  permission_dict["uuid"] = permission.id

  group_dict = {**BASIC_GROUP_MODEL_EXAMPLE, "permissions": [permission.uuid]}
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = "test_group_id"
  group.update()
  group_dict["uuid"] = "test_group_id"

  url = f"{api_url}/{uuid}"
  resp = client_with_emulator.delete(url)
  del_json_response = resp.json()
  expected_data = {
    "success": True,
    "message": "Successfully deleted the permission"
  }
  group_fields = UserGroup.find_by_uuid(group.uuid).get_fields()
  assert resp.status_code == 200, "Status code is 200"
  assert group_fields["permissions"] == []
  assert del_json_response == expected_data, "Expected response is same"


def test_delete_permission_negative(clean_firestore):
  uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{uuid}"
  response = {
    "success": False,
    "message": "Permission with uuid U2DDBkl3Ayg0PWudzhI not found",
    "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_get_filtered_permissions_1(clean_firestore):
  application_dict = deepcopy(BASIC_APPLICATION_MODEL_EXAMPLE)
  application = Application.from_dict(application_dict)
  application.uuid = ""
  application.save()
  application.uuid = application.id
  application.update()
  application_dict["uuid"] = application.id

  module_dict = deepcopy(BASIC_MODULE_MODEL_EXAMPLE)
  module = Module.from_dict(module_dict)
  module.uuid = ""
  module.save()
  module.uuid = module.id
  module.update()
  module_dict["uuid"] = module.id

  action_dict = deepcopy(BASIC_ACTION_MODEL_EXAMPLE)
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()
  action_dict["uuid"] = action.id

  permission_dict = deepcopy(BASIC_PERMISSION_MODEL_EXAMPLE)
  permission = Permission.from_dict(permission_dict)
  permission.application_id = application_dict["uuid"]
  permission.module_id = module_dict["uuid"]
  permission.action_id = action_dict["uuid"]
  permission.user_groups = []
  permission.uuid = ""
  permission.save()
  permission.uuid = permission.id
  permission.update()
  permission_dict["uuid"] = permission.id

  params = {
    "skip": 0,
    "limit": 10,
    "application_ids": application_dict["uuid"],
  }

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  assert len(json_response["data"]["records"]) == 1


def test_get_filtered_permissions_2(clean_firestore):
  application_dict = deepcopy(BASIC_APPLICATION_MODEL_EXAMPLE)
  application = Application.from_dict(application_dict)
  application.uuid = ""
  application.save()
  application.uuid = application.id
  application.update()
  application_dict["uuid"] = application.id

  module_dict = deepcopy(BASIC_MODULE_MODEL_EXAMPLE)
  module = Module.from_dict(module_dict)
  module.uuid = ""
  module.save()
  module.uuid = module.id
  module.update()
  module_dict["uuid"] = module.id

  action_dict = deepcopy(BASIC_ACTION_MODEL_EXAMPLE)
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()
  action_dict["uuid"] = action.id

  user_group_dict = deepcopy(POST_USERGROUP_MODEL_EXAMPLE)
  user_group = UserGroup.from_dict(user_group_dict)
  user_group.uuid = ""
  user_group.save()
  user_group.uuid = user_group.id
  user_group.update()
  user_group_dict["uuid"] = user_group.id

  permission_dict = deepcopy(BASIC_PERMISSION_MODEL_EXAMPLE)
  permission = Permission.from_dict(permission_dict)
  permission.application_id = application_dict["uuid"]
  permission.module_id = module_dict["uuid"]
  permission.action_id = action_dict["uuid"]
  permission.user_groups = [user_group_dict["uuid"]]
  permission.uuid = ""
  permission.save()
  permission.uuid = permission.id
  permission.update()
  permission_dict["uuid"] = permission.id

  params = {
    "skip": 0,
    "limit": 10,
    "application_ids": application_dict["uuid"] + ",application_id",
    "module_ids": module_dict["uuid"] + ",module_id",
    "action_ids": action_dict["uuid"] + ",action_id",
    "user_groups": user_group_dict["uuid"]
  }

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  assert len(json_response["data"]["records"]) == 1


def test_get_filtered_permissions_negative_1(clean_firestore):
  application_dict = deepcopy(BASIC_APPLICATION_MODEL_EXAMPLE)
  application = Application.from_dict(application_dict)
  application.uuid = ""
  application.save()
  application.uuid = application.id
  application.update()
  application_dict["uuid"] = application.id

  module_dict = deepcopy(BASIC_MODULE_MODEL_EXAMPLE)
  module = Module.from_dict(module_dict)
  module.uuid = ""
  module.save()
  module.uuid = module.id
  module.update()
  module_dict["uuid"] = module.id

  action_dict = deepcopy(BASIC_ACTION_MODEL_EXAMPLE)
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()
  action_dict["uuid"] = action.id

  user_group_dict = deepcopy(POST_USERGROUP_MODEL_EXAMPLE)
  user_group = UserGroup.from_dict(user_group_dict)
  user_group.uuid = ""
  user_group.save()
  user_group.uuid = user_group.id
  user_group.update()
  user_group_dict["uuid"] = user_group.id

  permission_dict = deepcopy(BASIC_PERMISSION_MODEL_EXAMPLE)
  permission = Permission.from_dict(permission_dict)
  permission.application_id = application_dict["uuid"]
  permission.module_id = module_dict["uuid"]
  permission.action_id = action_dict["uuid"]
  permission.user_groups = [user_group_dict["uuid"]]
  permission.uuid = ""
  permission.save()
  permission.uuid = permission.id
  permission.update()
  permission_dict["uuid"] = permission.id

  params = {
    "skip": 0,
    "limit": 10,
    "application_ids": "invalid_app_id",
    "module_ids": module_dict["uuid"],
    "action_ids": action_dict["uuid"],
    "user_groups": user_group_dict["uuid"]
  }

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)

  assert resp.status_code == 200, "Status 200"


def test_get_filtered_permissions_negative_2(clean_firestore):
  application_dict = deepcopy(BASIC_APPLICATION_MODEL_EXAMPLE)
  application = Application.from_dict(application_dict)
  application.uuid = ""
  application.save()
  application.uuid = application.id
  application.update()
  application_dict["uuid"] = application.id

  module_dict = deepcopy(BASIC_MODULE_MODEL_EXAMPLE)
  module = Module.from_dict(module_dict)
  module.uuid = ""
  module.save()
  module.uuid = module.id
  module.update()
  module_dict["uuid"] = module.id

  action_dict = deepcopy(BASIC_ACTION_MODEL_EXAMPLE)
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()
  action_dict["uuid"] = action.id

  user_group_dict = deepcopy(POST_USERGROUP_MODEL_EXAMPLE)
  user_group = UserGroup.from_dict(user_group_dict)
  user_group.uuid = ""
  user_group.save()
  user_group.uuid = user_group.id
  user_group.update()
  user_group_dict["uuid"] = user_group.id

  permission_dict = deepcopy(BASIC_PERMISSION_MODEL_EXAMPLE)
  permission = Permission.from_dict(permission_dict)
  permission.application_id = application_dict["uuid"]
  permission.module_id = module_dict["uuid"]
  permission.action_id = action_dict["uuid"]
  permission.user_groups = [user_group_dict["uuid"]]
  permission.uuid = ""
  permission.save()
  permission.uuid = permission.id
  permission.update()
  permission_dict["uuid"] = permission.id

  params = {
    "skip": 0,
    "limit": 10,
    "application_ids": "random_app_uuid",
    "module_ids": module_dict["uuid"],
    "action_ids": action_dict["uuid"],
    "user_groups": user_group_dict["uuid"]
  }

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200
  assert json_response["success"] is True


def test_permissions_sort_by_application_name(clean_firestore):
  application_dict = deepcopy(BASIC_APPLICATION_MODEL_EXAMPLE)
  application = Application.from_dict(application_dict)
  application.uuid = ""
  application.save()
  application.uuid = application.id
  application.update()
  application_dict["uuid"] = application.id

  application_dict1 = deepcopy(BASIC_APPLICATION_MODEL_EXAMPLE)
  application = Application.from_dict(application_dict1)
  application.uuid = ""
  application.save()
  application.uuid = application.id
  application.update()
  application_dict1["uuid"] = application.id

  module_dict = deepcopy(BASIC_MODULE_MODEL_EXAMPLE)
  module = Module.from_dict(module_dict)
  module.uuid = ""
  module.save()
  module.uuid = module.id
  module.update()
  module_dict["uuid"] = module.id

  action_dict = deepcopy(BASIC_ACTION_MODEL_EXAMPLE)
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()
  action_dict["uuid"] = action.id

  # permission 1
  permission_dict = deepcopy(BASIC_PERMISSION_MODEL_EXAMPLE)
  permission = Permission.from_dict(permission_dict)
  permission.application_id = application_dict["uuid"]
  permission.module_id = module_dict["uuid"]
  permission.action_id = action_dict["uuid"]
  permission.user_groups = []
  permission.uuid = ""
  permission.save()
  permission.uuid = permission.id
  permission.update()
  permission_dict["uuid"] = permission.id

  #permission 2
  permission_dict = deepcopy(BASIC_PERMISSION_MODEL_EXAMPLE)
  permission = Permission.from_dict(permission_dict)
  permission.application_id = application_dict1["uuid"]
  permission.module_id = module_dict["uuid"]
  permission.action_id = action_dict["uuid"]
  permission.user_groups = []
  permission.uuid = ""
  permission.save()
  permission.uuid = permission.id
  permission.update()
  permission_dict["uuid"] = permission.id

  params = {"skip": 0,"limit": "30","fetch_tree":True,"sort_by":"application",\
            "sort_order":"ascending"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"
  assert len(json_response["data"]["records"]) == 2

def test_permissions_sort_by_user_groups(clean_firestore):
  application_dict = deepcopy(BASIC_APPLICATION_MODEL_EXAMPLE)
  application = Application.from_dict(application_dict)
  application.uuid = ""
  application.save()
  application.uuid = application.id
  application.update()
  application_dict["uuid"] = application.id

  module_dict = deepcopy(BASIC_MODULE_MODEL_EXAMPLE)
  module = Module.from_dict(module_dict)
  module.uuid = ""
  module.save()
  module.uuid = module.id
  module.update()
  module_dict["uuid"] = module.id

  action_dict = deepcopy(BASIC_ACTION_MODEL_EXAMPLE)
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()
  action_dict["uuid"] = action.id

  # user group 1
  user_group_dict = deepcopy(POST_USERGROUP_MODEL_EXAMPLE)
  user_group = UserGroup.from_dict(user_group_dict)
  user_group.uuid = ""
  user_group.save()
  user_group.uuid = user_group.id
  user_group.name = f"{uuid4()}-user-group-name"
  user_group.update()
  user_group_dict["uuid"] = user_group.id

  # user group 2
  user_group_dict2 = deepcopy(POST_USERGROUP_MODEL_EXAMPLE)
  user_group = UserGroup.from_dict(user_group_dict2)
  user_group.uuid = ""
  user_group.save()
  user_group.uuid = user_group.id
  user_group.name = f"{uuid4()}-user-group-name"
  user_group.update()
  user_group_dict2["uuid"] = user_group.id

  permission_dict = deepcopy(BASIC_PERMISSION_MODEL_EXAMPLE)
  permission = Permission.from_dict(permission_dict)
  permission.application_id = application_dict["uuid"]
  permission.module_id = module_dict["uuid"]
  permission.action_id = action_dict["uuid"]
  permission.user_groups = [user_group_dict["uuid"]]
  permission.uuid = ""
  permission.save()
  permission.uuid = permission.id
  permission.update()
  permission_dict["uuid"] = permission.id

  permission_dict = deepcopy(BASIC_PERMISSION_MODEL_EXAMPLE)
  permission = Permission.from_dict(permission_dict)
  permission.application_id = application_dict["uuid"]
  permission.module_id = module_dict["uuid"]
  permission.action_id = action_dict["uuid"]
  permission.user_groups = [user_group_dict2["uuid"]]
  permission.uuid = ""
  permission.save()
  permission.uuid = permission.id
  permission.update()
  permission_dict["uuid"] = permission.id

  params = {
    "skip": 0,
    "limit": 10,
    "fetch_tree": True,
    "sort_by": "user_groups", "sort_order":"descending"
  }

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert len(json_response["data"]["records"]) == 2

def test_permissions_unique_filter_without_selection(clean_firestore):
  # application 1
  application_dict_1 = deepcopy(BASIC_APPLICATION_MODEL_EXAMPLE)
  application_1 = Application.from_dict(application_dict_1)
  application_1.uuid = ""
  application_1.save()
  application_1.uuid = application_1.id
  application_1.update()
  application_dict_1["uuid"] = application_1.id

  # application 2
  application_dict_2 = deepcopy(BASIC_APPLICATION_MODEL_EXAMPLE)
  application_2 = Application.from_dict(application_dict_2)
  application_2.uuid = ""
  application_2.name = ""
  application_2.save()
  application_2.uuid = application_2.id
  application_2.name = "application-2"
  application_2.update()
  application_dict_2["uuid"] = application_2.id
  application_dict_2["name"] = application_2.name

  # module 1
  module_dict_1 = deepcopy(BASIC_MODULE_MODEL_EXAMPLE)
  module_1 = Module.from_dict(module_dict_1)
  module_1.uuid = ""
  module_1.save()
  module_1.uuid = module_1.id
  module_1.update()
  module_dict_1["uuid"] = module_1.id

  # module 2
  module_dict_2 = deepcopy(BASIC_MODULE_MODEL_EXAMPLE)
  module_2 = Module.from_dict(module_dict_2)
  module_2.uuid = ""
  module_2.save()
  module_2.uuid = module_2.id
  module_2.name = "module-2"
  module_2.update()
  module_dict_2["uuid"] = module_2.id
  module_dict_2["name"] = module_2.name

  # action 1
  action_dict_1 = deepcopy(BASIC_ACTION_MODEL_EXAMPLE)
  action_1 = Action.from_dict(action_dict_1)
  action_1.uuid = ""
  action_1.save()
  action_1.uuid = action_1.id
  action_1.update()
  action_dict_1["uuid"] = action_1.id

  # action 2
  action_dict_2 = deepcopy(BASIC_ACTION_MODEL_EXAMPLE)
  action_2 = Action.from_dict(action_dict_2)
  action_2.uuid = ""
  action_2.name = ""
  action_2.save()
  action_2.uuid = action_2.id
  action_2.name = "action_2"
  action_2.update()
  action_dict_2["uuid"] = action_2.id
  action_dict_2["name"] = action_2.name

  # user group 1
  user_group_dict_1 = deepcopy(POST_USERGROUP_MODEL_EXAMPLE)
  user_group_1 = UserGroup.from_dict(user_group_dict_1)
  user_group_1.uuid = ""
  user_group_1.name = ""
  user_group_1.save()
  user_group_1.uuid = user_group_1.id
  user_group_1.name = f"{uuid4()}-user-group-name-1"
  user_group_1.update()
  user_group_dict_1["uuid"] = user_group_1.id

  # user group 2
  user_group_dict_2 = deepcopy(POST_USERGROUP_MODEL_EXAMPLE)
  user_group_2 = UserGroup.from_dict(user_group_dict_2)
  user_group_2.uuid = ""
  user_group_2.name = ""
  user_group_2.save()
  user_group_2.uuid = user_group_2.id
  user_group_2.name = f"{uuid4()}-user-group-name-2"
  user_group_2.update()
  user_group_dict_2["uuid"] = user_group_2.id
  user_group_dict_2["name"] = user_group_2.name

  permission_dict_1 = deepcopy(BASIC_PERMISSION_MODEL_EXAMPLE)
  permission = Permission.from_dict(permission_dict_1)
  permission.application_id = application_dict_1["uuid"]
  permission.module_id = module_dict_1["uuid"]
  permission.action_id = action_dict_1["uuid"]
  permission.user_groups = [user_group_dict_1["uuid"]]
  permission.uuid = ""
  permission.save()
  permission.uuid = permission.id
  permission.update()
  permission_dict_1["uuid"] = permission.id

  permission_dict_2 = deepcopy(BASIC_PERMISSION_MODEL_EXAMPLE)
  permission = Permission.from_dict(permission_dict_2)
  permission.application_id = application_dict_2["uuid"]
  permission.module_id = module_dict_2["uuid"]
  permission.action_id = action_dict_2["uuid"]
  permission.user_groups = [user_group_dict_2["uuid"]]
  permission.uuid = ""
  permission.save()
  permission.uuid = permission.id
  permission.update()
  permission_dict_2["uuid"] = permission.id

  url = f"{api_url}_filter/unique"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert len(json_response["data"]["applications"]) == 2

def test_permissions_unique_filter_with_application_filter(clean_firestore):
  permission_dict_1 = {
    **BASIC_PERMISSION_MODEL_EXAMPLE,
    "application_id": create_documents("applications", {
      **BASIC_APPLICATION_MODEL_EXAMPLE, "modules": []
    }),
    "module_id": create_documents("modules", {
      **BASIC_MODULE_MODEL_EXAMPLE, "actions": []
    }),
    "action_id": create_documents("actions", {**BASIC_ACTION_MODEL_EXAMPLE}),
    "user_groups": [create_documents("user_groups",
                                     {**POST_USERGROUP_MODEL_EXAMPLE})]
  }

  permission_1 = Permission.from_dict(permission_dict_1)
  permission_1.uuid = ""
  permission_1.save()
  permission_1.uuid = permission_1.id
  permission_1.update()
  permission_dict_1["uuid"] = permission_1.id

  permission_dict_2 = {
    **BASIC_PERMISSION_MODEL_EXAMPLE,
    "application_id": create_documents("applications", {
      **BASIC_APPLICATION_MODEL_EXAMPLE, "modules": []
    }),
    "module_id": create_documents("modules", {
      **BASIC_MODULE_MODEL_EXAMPLE, "actions": []
    }),
    "action_id": create_documents("actions", {**BASIC_ACTION_MODEL_EXAMPLE}),
    "user_groups": [create_documents("user_groups",
                                     {**POST_USERGROUP_MODEL_EXAMPLE})]
  }

  permission_2 = Permission.from_dict(permission_dict_2)
  permission_2.uuid = ""
  permission_2.save()
  permission_2.uuid = permission_2.id
  permission_2.update()
  permission_dict_2["uuid"] = permission_2.id

  url = f"{api_url}_filter/unique?application="\
    f"{permission_dict_1['application_id']},"\
    f"{permission_dict_2['application_id']}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert len(json_response["data"]["applications"]) == 2


def test_permissions_unique_filter_with_mix_filter_selection(clean_firestore):
  permission_dict_1 = {
    **BASIC_PERMISSION_MODEL_EXAMPLE,
    "application_id": create_documents("applications", {
      **BASIC_APPLICATION_MODEL_EXAMPLE, "modules": []
    }),
    "module_id": create_documents("modules", {
      **BASIC_MODULE_MODEL_EXAMPLE, "actions": []
    }),
    "action_id": create_documents("actions", {**BASIC_ACTION_MODEL_EXAMPLE}),
    "user_groups": [create_documents("user_groups",
                                     {**POST_USERGROUP_MODEL_EXAMPLE})]
  }

  permission_1 = Permission.from_dict(permission_dict_1)
  permission_1.uuid = ""
  permission_1.save()
  permission_1.uuid = permission_1.id
  permission_1.update()
  permission_dict_1["uuid"] = permission_1.id

  permission_dict_2 = {
    **BASIC_PERMISSION_MODEL_EXAMPLE,
    "application_id": create_documents("applications", {
      **BASIC_APPLICATION_MODEL_EXAMPLE, "modules": []
    }),
    "module_id": create_documents("modules", {
      **BASIC_MODULE_MODEL_EXAMPLE, "actions": []
    }),
    "action_id": create_documents("actions", {**BASIC_ACTION_MODEL_EXAMPLE}),
    "user_groups": [create_documents("user_groups",
                                     {**POST_USERGROUP_MODEL_EXAMPLE})]
  }

  permission_2 = Permission.from_dict(permission_dict_2)
  permission_2.uuid = ""
  permission_2.save()
  permission_2.uuid = permission_2.id
  permission_2.update()
  permission_dict_2["uuid"] = permission_2.id

  url = f"{api_url}_filter/unique?application="\
    f"{permission_dict_1['application_id']}"\
    f"&module={permission_dict_1['module_id']}"\
    f"&action={permission_dict_1['action_id']}"\
    f"&user_group={permission_dict_1['user_groups'][0]}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert len(json_response["data"]["applications"]) == 1

def test_permissions_unique_with_filter_negative(clean_firestore):
  permission_dict_1 = {
    **BASIC_PERMISSION_MODEL_EXAMPLE,
    "application_id": create_documents("applications", {
      **BASIC_APPLICATION_MODEL_EXAMPLE, "modules": []
    }),
    "module_id": create_documents("modules", {
      **BASIC_MODULE_MODEL_EXAMPLE, "actions": []
    }),
    "action_id": create_documents("actions", {**BASIC_ACTION_MODEL_EXAMPLE}),
    "user_groups": [create_documents("user_groups",
                                     {**POST_USERGROUP_MODEL_EXAMPLE})]
  }

  permission_1 = Permission.from_dict(permission_dict_1)
  permission_1.uuid = ""
  permission_1.save()
  permission_1.uuid = permission_1.id
  permission_1.update()
  permission_dict_1["uuid"] = permission_1.id


  url = f"{api_url}_filter/unique?application=invalid_filter_id"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert json_response["success"] is True
  assert json_response["data"]["applications"] == []


def test_permissions_unique_with_filter_length_negative(clean_firestore):
  url = f"{api_url}_filter/unique?application=1,2,3,4,5,6,7,8,9,10,"+\
  "11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 422, "Status 422"
  assert json_response["success"] is False
  assert json_response["message"] == "Filter has a limit of 30 values"
