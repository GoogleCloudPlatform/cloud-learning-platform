"""
  Unit tests for group endpoints
"""
import os
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.user_group import router
from testing.test_config import (API_URL)
from schemas.schema_examples import (BASIC_ACTION_MODEL_EXAMPLE,
                                     BASIC_APPLICATION_MODEL_EXAMPLE,
                                     BASIC_GROUP_MODEL_EXAMPLE,
                                     BASIC_USER_MODEL_EXAMPLE,
                                     FULL_USER_MODEL_EXAMPLE,
                                     BASIC_PERMISSION_MODEL_EXAMPLE,
                                     POST_USERGROUP_MODEL_EXAMPLE)
from common.models import UserGroup, User, Permission, Action, Application
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers
from copy import deepcopy

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/user-management/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/user-group"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_get_user_group(clean_firestore):
  group_dict = {**BASIC_GROUP_MODEL_EXAMPLE}
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()
  group_dict["uuid"] = group.id

  url = f"{api_url}/{group.uuid}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  del json_response["data"]["created_time"]
  del json_response["data"]["last_modified_time"]
  assert resp.status_code == 200, "Status 200"
  assert json_response.get("data") == {
    **group_dict, "is_immutable": False
  }, "Response received"


def test_get_user_group_negative(clean_firestore):
  """Get a user group with incorrect uuid"""
  uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{uuid}"
  data = {
    "success": False,
    "message": f"UserGroup with uuid {uuid} not found",
    "data": None
  }

  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 404, "Status 404"
  assert json_response == data, "Response received"


def test_get_all_user_groups(clean_firestore):
  group_dict = {**BASIC_GROUP_MODEL_EXAMPLE}

  # group
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()

  params = {"skip": 0, "limit": "30"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"
  retrieved_ids = [i.get("uuid") for i in json_response.get("data")["records"]]
  assert group.uuid in retrieved_ids, "expected data not retrieved"


def test_sort_user_groups(clean_firestore):
  group_dict = {**BASIC_GROUP_MODEL_EXAMPLE}

  # group
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()

  params = {"skip": 0, "limit": "30", "sort_by": "name",
            "sort_order": "descending"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"
  retrieved_ids = [i.get("uuid") for i in json_response.get("data")["records"]]
  assert group.uuid in retrieved_ids, "expected data not retrieved"


def test_sort_user_groups_negative(clean_firestore):
  params = {"skip": 0, "limit": "30", "sort_by": "name",
            "sort_order": "desc"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422
  assert json_response["success"] is False


def test_get_all_groups_negative_param(clean_firestore):
  group_dict = {**BASIC_GROUP_MODEL_EXAMPLE}

  # group
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()

  params = {"skip": 0, "limit": "-3"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422, "Status should be 422"
  assert json_response["message"] == "Validation Failed"


def test_get_all_groups_negative(clean_firestore):
  group_dict = {**BASIC_GROUP_MODEL_EXAMPLE}

  # group
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()

  params = {"skip": 0, "limit": "105"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422, "Status should be 422"
  assert json_response["message"] == "Validation Failed"


def test_post_user_group(clean_firestore):
  input_group = {**POST_USERGROUP_MODEL_EXAMPLE}
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_group)
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
  loaded_group = UserGroup.find_by_uuid(uuid)
  loaded_group_dict = loaded_group.to_dict()

  # popping id and key for equivalency test
  loaded_group_dict.pop("id")
  loaded_group_dict.pop("key")
  loaded_group_dict.pop("alias")
  loaded_group_dict.pop("roles")
  loaded_group_dict.pop("created_by")
  loaded_group_dict.pop("created_time")
  loaded_group_dict.pop("last_modified_by")
  loaded_group_dict.pop("last_modified_time")
  loaded_group_dict.pop("archived_at_timestamp")
  loaded_group_dict.pop("archived_by")
  loaded_group_dict.pop("deleted_at_timestamp")
  loaded_group_dict.pop("deleted_by")
  # assert that rest of the fields are equivalent
  assert loaded_group_dict == post_json_response.get("data")


def test_post_immutable_user_group(clean_firestore):
  input_group = {**POST_USERGROUP_MODEL_EXAMPLE, "name": "learner"}
  url = f"{api_url}/immutable"
  post_resp = client_with_emulator.post(url, json=input_group)
  post_resp_json = post_resp.json()
  immutable_group_id = post_resp_json["data"]["uuid"]
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  params = {"skip": 0, "limit": "30", "is_immutable": True}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"
  retrieved_ids = [i.get("uuid") for i in json_response.get("data")["records"]]
  assert [immutable_group_id] == retrieved_ids, "expected data not retrieved"


def test_post_immutable_user_group_negative(clean_firestore):
  input_group = {**POST_USERGROUP_MODEL_EXAMPLE, "name": "random_name"}
  url = f"{api_url}/immutable"
  post_resp = client_with_emulator.post(url, json=input_group)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is False, "Success not true"
  assert post_resp.status_code == 422, "Status 200"


def test_update_normal_user_group(clean_firestore):
  group_dict = {**POST_USERGROUP_MODEL_EXAMPLE}
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()
  group_uuid = group.id

  url = f"{api_url}/{group_uuid}"
  updated_data = {"name": "new group name"}
  resp = client_with_emulator.put(url, json=updated_data)
  update_response = resp.json()

  assert update_response.get("success") is True, "Success not true"
  assert update_response.get(
    "message"
  ) == "Successfully updated the user group", "Expected response not same"
  assert update_response.get("data").get(
    "name") == "new group name", "Expected response not same"


def test_update_immutable_user_group(clean_firestore):
  group_dict = {**POST_USERGROUP_MODEL_EXAMPLE, "is_immutable": True}
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()
  group_uuid = group.id

  url = f"{api_url}/{group_uuid}"
  updated_data = {"name": "new_group_name"}
  resp = client_with_emulator.put(url, json=updated_data)
  update_response = resp.json()
  assert update_response.get("success") is False, "Success not true"
  assert update_response.get(
    "message"
  ) == f"Cannot update name of an " \
       f"immutable Usergroup with uuid:{group_uuid}", \
    "Expected response not same"


def test_update_user_group_negative(clean_firestore):
  uuid = "U2DDBkl3Ayg0PWudzhI"

  url = f"{api_url}/{uuid}"
  response = {
    "success": False,
    "message": "UserGroup with uuid U2DDBkl3Ayg0PWudzhI not found",
    "data": None
  }
  resp = client_with_emulator.put(url, json={"name": "random"})
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_delete_user_group(clean_firestore):
  group_dict = {
    **BASIC_GROUP_MODEL_EXAMPLE, "users": ["test_user_id"],
    "permissions": ["test_permission_id"]
  }
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()

  uuid = group.uuid
  group_dict["uuid"] = group.id

  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_groups": [group.uuid]}
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = "test_user_id"
  user.update()
  user_dict["user_id"] = "test_user_id"

  permission_dict = {
    **BASIC_PERMISSION_MODEL_EXAMPLE, "user_groups": [group.uuid]
  }
  permission = Permission.from_dict(permission_dict)
  permission.uuid = ""
  permission.save()
  permission.uuid = "test_permission_id"
  permission.update()
  permission_dict["uuid"] = "test_permission_id"
  url = f"{api_url}/{uuid}"
  resp = client_with_emulator.delete(url)
  del_json_response = resp.json()
  expected_data = {
    "success": True,
    "message": "Successfully deleted the user group"
  }

  permission_fields = Permission.find_by_uuid(permission.uuid).get_fields()
  user_fields = User.find_by_uuid(user.user_id).get_fields()
  assert resp.status_code == 200, "Status code 200"
  assert permission_fields["user_groups"] == []
  assert user_fields["user_groups"] == []
  assert del_json_response == expected_data, "Expected response is the same"


def test_delete_user_group_negative(clean_firestore):
  uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{uuid}"
  response = {
    "success": False,
    "message": "UserGroup with uuid U2DDBkl3Ayg0PWudzhI not found",
    "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_delete_immutable_user_group_negative(clean_firestore):
  group_dict = {**POST_USERGROUP_MODEL_EXAMPLE, "is_immutable": True}
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()
  group_dict["uuid"] = group.id

  url = f"{api_url}/{group.id}"
  resp = client_with_emulator.delete(url)
  mes = f"Cannot delete an immutable Usergroup with uuid:{group.id}"
  json_response = resp.json()

  assert resp.status_code == 422, "Status 404"
  assert json_response["message"] == mes, "Expected response not same"


def test_add_user_to_normal_user_group(clean_firestore):
  group_dict = {**BASIC_GROUP_MODEL_EXAMPLE, "users": []}
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()
  uuid = group.uuid
  group_dict["uuid"] = group.id

  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_groups": [group.uuid]}
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = "test_user_id"
  user.update()
  user_dict["user_id"] = "test_user_id"

  req_body = {"user_ids": [user_dict["user_id"]]}

  url = f"{api_url}/{uuid}/users/add"
  resp = client_with_emulator.post(url, json=req_body)

  updated_json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  assert updated_json_response["data"]["users"] == [
    user_dict["user_id"]
  ], "Expected response not same"


def test_add_user_to_immutable_user_group(clean_firestore):
  group_dict = {
    **BASIC_GROUP_MODEL_EXAMPLE, "name": "assessor",
    "is_immutable": True,
    "users": []
  }
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()
  uuid = group.uuid
  group_dict["uuid"] = group.id

  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_type": "assessor"}
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = "test_user_id"
  user.update()
  user_dict["user_id"] = "test_user_id"

  req_body = {"user_ids": [user_dict["user_id"]]}

  url = f"{api_url}/{uuid}/users/add"
  resp = client_with_emulator.post(url, json=req_body)

  updated_json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  assert updated_json_response["data"]["users"] == [
    user_dict["user_id"]
  ], "Expected response not same"


def test_add_user_to_immutable_user_group_negative(clean_firestore):
  group_dict = {
    **BASIC_GROUP_MODEL_EXAMPLE, "name": "assessor",
    "is_immutable": True
  }
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()
  uuid = group.uuid
  group_dict["uuid"] = group.id

  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_type": "instructor"}
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = "test_user_id"
  user.update()
  user_dict["user_id"] = "test_user_id"

  req_body = {"user_ids": [user_dict["user_id"]]}

  url = f"{api_url}/{uuid}/users/add"
  resp = client_with_emulator.post(url, json=req_body)
  mes = f"User with user_type {user.user_type} cannot be added to user group:" \
        f" {group.name}"
  updated_json_response = resp.json()
  assert resp.status_code == 422, "Status code not 200"
  assert updated_json_response["message"] == mes, "Expected response not same"


def test_add_redundant_users_to_user_group_negative_1(clean_firestore):
  user_dict = {**BASIC_USER_MODEL_EXAMPLE}
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = "test_user_id"
  user.update()
  user_dict["user_id"] = "test_user_id"

  group_dict = {**BASIC_GROUP_MODEL_EXAMPLE, "users": [user_dict["user_id"]]}
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()
  uuid = group.uuid
  group_dict["uuid"] = group.id

  req_body = {"user_ids": [user_dict["user_id"]]}

  url = f"{api_url}/{uuid}/users/add"
  resp = client_with_emulator.post(url, json=req_body)
  updated_json_response = resp.json()
  assert resp.status_code == 422, "Status code not 200"
  assert updated_json_response[
           "message"] == f"UserGroup with uuid {group.id} already contains " \
                         f"users with uuids {user_dict['user_id']}"


def test_add_user_to_user_group_negative_1(clean_firestore):
  group_dict = {**BASIC_GROUP_MODEL_EXAMPLE, "users": []}
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()
  uuid = group.uuid
  group_dict["uuid"] = group.id

  req_body = {"user_ids": ["random_user_id"]}

  url = f"{api_url}/{uuid}/users/add"
  resp = client_with_emulator.post(url, json=req_body)
  updated_json_response = resp.json()

  assert resp.status_code == 404, "Status code not 200"
  assert updated_json_response[
           "message"] == "User with user_id random_user_id not found"


def test_add_user_to_user_group_negative_2(clean_firestore):
  uuid = "random_group_id"
  req_body = {"user_ids": ["random_user_id"]}

  url = f"{api_url}/{uuid}/users/add"
  resp = client_with_emulator.post(url, json=req_body)
  updated_json_response = resp.json()
  assert resp.status_code == 404, "Status code not 200"
  assert updated_json_response[
           "message"] == f"UserGroup with uuid {uuid} not found"


def test_remove_user_from_user_group(clean_firestore):
  group_dict = {**BASIC_GROUP_MODEL_EXAMPLE, "users": ["test_user_id"]}
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()
  uuid = group.uuid
  group_dict["uuid"] = group.id

  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_groups": [group.uuid]}
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = "test_user_id"
  user.update()
  user_dict["user_id"] = "test_user_id"

  req_body = {"user_id": user_dict["user_id"]}

  url = f"{api_url}/{uuid}/user/remove"
  resp = client_with_emulator.post(url, json=req_body)
  updated_json_response = resp.json()

  assert resp.status_code == 200, "Status code not 200"
  assert updated_json_response["data"][
           "users"] == [], "Expected response not same"

  resp = client_with_emulator.post(url, json=req_body)
  updated_json_response = resp.json()
  mes = f"UserGroup with uuid {uuid} doesn't contain given user with uuid" \
        f" {user_dict['user_id']}"
  assert resp.status_code == 422, "Status code not 200"
  assert updated_json_response["message"] == mes, "Expected response not same"


def test_search_user_group(clean_firestore):
  group_dict = {**BASIC_GROUP_MODEL_EXAMPLE}
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()
  group_dict["uuid"] = group.id

  params = {"name": group_dict["name"]}

  url = f"{api_url}/search"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  del json_response["data"][0]["created_time"]
  del json_response["data"][0]["last_modified_time"]
  assert resp.status_code == 200, "Status 200"
  assert json_response["data"][0] == {
    **group_dict, "is_immutable": False
  }, "Response received"
  assert json_response["data"][0]["name"] == group_dict["name"]


def test_search_user_group_negative(clean_firestore):
  group_dict = {**BASIC_GROUP_MODEL_EXAMPLE}
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()
  group_dict["uuid"] = group.id

  params = {"name": "test"}

  url = f"{api_url}/search"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert json_response["data"] == [], "Response received"


def test_add_application_to_user_group(clean_firestore):
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
  action_dict = {**BASIC_ACTION_MODEL_EXAMPLE, "name": "view"}
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()

  permission_dict = {
    **BASIC_PERMISSION_MODEL_EXAMPLE, "application_id": application.id,
    "action_id": action.id
  }
  permission = Permission.from_dict(permission_dict)
  permission.uuid = ""
  permission.save()
  permission.uuid = permission.id
  permission.update()

  req_body = {"applications": [application.id], "action_id": action.id}
  url = f"{api_url}/{group.id}/applications"
  resp = client_with_emulator.put(url, json=req_body)
  assert resp.status_code == 200, "Status coded not 200"
  updated_group = resp.json()
  assert permission.id in updated_group["data"]["permissions"]
  assert application.id in updated_group["data"]["applications"]

  get_permission = Permission.find_by_uuid(permission.id)
  permission = get_permission.get_fields()
  assert group.id in permission.get("user_groups")


def test_remove_application_from_user_group(clean_firestore):
  application_dict = {**BASIC_APPLICATION_MODEL_EXAMPLE}
  application = Application.from_dict(application_dict)
  application.uuid = ""
  application.save()
  application.uuid = application.id
  application.update()

  action_dict = {**BASIC_ACTION_MODEL_EXAMPLE, "name": "random_action"}
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()

  permission_dict = {
    **BASIC_PERMISSION_MODEL_EXAMPLE, "application_id": application.id,
    "action_id": action.id
  }
  permission = Permission.from_dict(permission_dict)
  permission.uuid = ""
  permission.save()
  permission.uuid = permission.id
  permission.update()

  group_dict = {
    **BASIC_GROUP_MODEL_EXAMPLE, "users": [],
    "applications": [application.id],
    "permissions": [permission.id]
  }
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()

  permission.user_groups = [group.id]
  permission.update()

  req_body = {"applications": [], "action_id": action.id}
  url = f"{api_url}/{group.id}/applications"
  resp = client_with_emulator.put(url, json=req_body)
  assert resp.status_code == 200, "Status code not 200"
  updated_group = resp.json()
  assert permission.id not in updated_group["data"]["permissions"]
  assert application.id not in updated_group["data"]["applications"]


def test_update_permissions_to_user_group(clean_firestore):
  application_ids = []
  applications = [{
    **BASIC_APPLICATION_MODEL_EXAMPLE, "name": "application1"
  }, {
    **BASIC_APPLICATION_MODEL_EXAMPLE, "name": "application2"
  }]
  for application_dict in applications:
    application = Application.from_dict(application_dict)
    application.uuid = ""
    application.save()
    application.uuid = application.id
    application.update()
    application_ids.append(application.id)

  actions = [{
    **BASIC_ACTION_MODEL_EXAMPLE, "name": "view"
  }, {
    **BASIC_ACTION_MODEL_EXAMPLE, "name": "edit"
  }]
  action_ids = []
  for action_dict in actions:
    action = Action.from_dict(action_dict)
    action.uuid = ""
    action.save()
    action.uuid = action.id
    action.update()
    action_ids.append(action.id)

  group_dict = {**BASIC_GROUP_MODEL_EXAMPLE, "users": []}
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()

  permissions = [{
    **BASIC_PERMISSION_MODEL_EXAMPLE, "action_id": action_ids[0],
    "application_id": application_ids[0]
  }, {
    **BASIC_PERMISSION_MODEL_EXAMPLE, "action_id": action_ids[1], \
    "application_id": application_ids[0]
  },
    {
      **BASIC_PERMISSION_MODEL_EXAMPLE, "action_id": action_ids[0],
      "application_id": application_ids[1]
    }]
  permission_ids = []
  for permission_dict in permissions:
    permission = Permission.from_dict({
      **permission_dict, "module_id": "module_id"
    })
    permission.uuid = ""
    permission.save()
    permission.uuid = permission.id
    permission.update()
    permission_ids.append(permission.id)

  req_body = {"applications": application_ids, "action_id": action_ids[0]}
  url = f"{api_url}/{group.id}/applications"
  resp = client_with_emulator.put(url, json=req_body)
  assert resp.status_code == 200, "Status coded not 200"
  updated_group = resp.json()

  assert permission_ids[0] in updated_group["data"]["permissions"]
  assert permission_ids[2] in updated_group["data"]["permissions"]
  assert application_ids[0] in updated_group["data"]["applications"]
  assert application_ids[1] in updated_group["data"]["applications"]

  get_permission = Permission.find_by_uuid(permission_ids[0])
  permission = get_permission.get_fields()
  assert group.id in permission.get("user_groups")

  req_body = {"permission_ids": [permission_ids[1]]}
  url = f"{api_url}/{group.id}/application/{application_ids[0]}/permissions"
  resp = client_with_emulator.post(url, json=req_body)
  assert resp.status_code == 200, "Status coded not 200"
  updated_group = resp.json()
  assert permission_ids[1] in updated_group["data"]["permissions"]
  assert permission_ids[2] in updated_group["data"]["permissions"]
  assert permission_ids[0] not in updated_group["data"]["permissions"]

  get_permission = Permission.find_by_uuid(permission_ids[0])
  permission = get_permission.get_fields(reformat_datetime=True)

  assert not group.id in permission.get("user_groups")
  get_permission = Permission.find_by_uuid(permission_ids[1])
  permission = get_permission.get_fields(reformat_datetime=True)
  assert group.id in permission.get("user_groups")


def test_update_permissions_negative_1(clean_firestore):
  """Should not update permissions of invalid application"""

  group_dict = {**BASIC_GROUP_MODEL_EXAMPLE, "users": []}
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()

  req_body = {"permission_ids": ["random_permission_id"]}
  url = f"{api_url}/{group.id}/application/random_application_id/permissions"
  resp = client_with_emulator.post(url, json=req_body)
  resp_json = resp.json()
  mes = "UserGroup doesn't have access to the given application"
  assert resp.status_code == 422, "Status coded not 200"
  assert resp_json["message"] == mes


def test_update_permissions_negative_2(clean_firestore):
  """Should not update permissions related to application which is \
    not assigned to the usergroup.
    Valid application"""

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

  group.applications = [application.id]
  group.update()

  permission = Permission.from_dict({
    **BASIC_PERMISSION_MODEL_EXAMPLE,
    "application_id": "random_application_id"
  })
  permission.uuid = ""
  permission.save()
  permission.uuid = permission.id
  permission.update()

  req_body = {"permission_ids": [permission.id]}
  url = f"{api_url}/{group.id}/application/{application.id}/permissions"
  resp = client_with_emulator.post(url, json=req_body)
  resp_json = resp.json()
  mes = f"The permission with uuid {permission.id} doesn't belong to the " \
        f"application with uuid {application.id}"
  assert resp.status_code == 422, "Status coded not 200"
  assert resp_json["message"] == mes


def test_get_users_to_add_to_user_group(clean_firestore):
  user_dict = {
    **FULL_USER_MODEL_EXAMPLE,
    "user_groups": []
  }
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  group_dict = deepcopy(BASIC_GROUP_MODEL_EXAMPLE)
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()

  url = f"{api_url}/{group.id}/addable-users"
  resp = client_with_emulator.get(url)
  resp_json = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert resp_json["success"] is True
  assert resp_json["message"] == "Successfully fetched users " \
                                 "that can be added to user group"


def test_get_users_to_add_to_user_group_negative(clean_firestore):
  user_dict = {
    **BASIC_USER_MODEL_EXAMPLE,
    "user_groups": []
  }
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  group_dict = deepcopy(BASIC_GROUP_MODEL_EXAMPLE)
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()

  url = f"{api_url}/random_id/addable-users"
  resp = client_with_emulator.get(url)
  resp_json = resp.json()
  assert resp.status_code == 404, "Status 404"
  assert resp_json["success"] is False
  assert resp_json["message"] == "UserGroup with uuid random_id not found"
  assert resp_json["data"] is None
