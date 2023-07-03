"""
  Unit tests for user endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
import os
import pytest
from copy import deepcopy
from unittest import mock
from fastapi import FastAPI
from fastapi.testclient import TestClient

with mock.patch(
  "google.cloud.secretmanager.SecretManagerServiceClient",
  side_effect=mock.MagicMock()) as mok:
  from routes.user import router
from testing.test_config import (API_URL, TESTING_FOLDER_PATH)
from schemas.schema_examples import (BASIC_GROUP_MODEL_EXAMPLE,
                                     BASIC_USER_MODEL_EXAMPLE,
                                     BASIC_APPLICATION_MODEL_EXAMPLE)
from common.utils.errors import ResourceNotFoundException
from common.models import User, UserGroup, Application, Staff
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/user-management/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/user"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


class Request:
  """Mock class for Request"""

  def __init__(self, status_code) -> None:
    self.status_code = status_code

  def json(self):
    return {}


def test_get_user(clean_firestore):
  user_dict = {**BASIC_USER_MODEL_EXAMPLE}
  user_dict["user_type_ref"] = ""
  user_dict["user_groups"] = []
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  user_dict["user_id"] = user.id

  url = f"{api_url}/{user.user_id}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  del json_response["data"]["created_time"]
  del json_response["data"]["last_modified_time"]
  assert resp.status_code == 200, "Status 200"
  assert json_response.get("data") == user_dict, "Response received"


def test_get_user_negative_1(clean_firestore):
  """Get a user with incorrect user_id"""
  user_id = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{user_id}"
  data = {
    "success": False,
    "message": f"User with user_id {user_id} not found",
    "data": None
  }

  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 404, "Status 404"
  assert json_response == data, "Response received"


def test_get_all_users(clean_firestore):
  user_dict = {**BASIC_USER_MODEL_EXAMPLE}
  user_dict["user_type_ref"] = ""
  user_dict["user_groups"] = []
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  params = {"skip": 0, "limit": "30"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"
  retrieved_ids = [i.get("user_id") for i in
                   json_response.get("data")["records"]]
  assert user.user_id in retrieved_ids, "expected data not retrieved"


def test_sort_the_users(clean_firestore):
  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": "",
               "user_groups": []}
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  params = {"skip": 0, "limit": "30", "sort_by": "first_name",
            "sort_order": "descending"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"
  retrieved_ids = [i.get("user_id") for i in
                   json_response.get("data")["records"]]
  assert user.user_id in retrieved_ids, "expected data not retrieved"


def test_sort_the_users_negative(clean_firestore):
  params = {"skip": 0, "limit": "30", "sort_by": "first_name",
            "sort_order": "asc"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 422
  assert json_response["success"] is False


def test_get_all_users_negative_param(clean_firestore):
  user_dict = {**BASIC_USER_MODEL_EXAMPLE}
  user_dict["user_type_ref"] = ""
  # user
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  params = {"skip": 0, "limit": "-3"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422, "Status should be 422"
  assert json_response["message"] == "Validation Failed"


def test_get_all_users_negative(clean_firestore):
  user_dict = {**BASIC_USER_MODEL_EXAMPLE}
  user_dict["user_type_ref"] = ""
  # user
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  params = {"skip": 0, "limit": "105"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422, "Status should be 422"
  assert json_response["message"] == "Validation Failed"


def test_get_all_users_with_filter(clean_firestore):
  user_dict = {**BASIC_USER_MODEL_EXAMPLE}
  user_dict["user_type_ref"] = ""
  user_dict["user_groups"] = []
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  user_type = user.user_type
  url = f"{api_url}s"
  params = {"user_type": user_type}

  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"

  assert len(json_response.get("data")["records"
             ]) > 0, "Results should not be empty"
  retrieved_ids = [i.get("user_id") for i in
                   json_response.get("data")["records"]]
  assert user.user_id in retrieved_ids, "expected data not retrieved"
  for i in json_response.get("data")["records"]:
    assert i["user_type"] == user_type, "Filtered output is wrong"


def test_get_all_users_by_user_group(clean_firestore):
  group_dict = {**BASIC_GROUP_MODEL_EXAMPLE, "name": "learner",
                "is_immutable": True}
  group1 = UserGroup.from_dict(group_dict)
  group1.uuid = ""
  group1.save()
  group1.uuid = group1.id
  group1.update()

  group_dict = {**BASIC_GROUP_MODEL_EXAMPLE, "name": "coach",
                "is_immutable": True}
  group2 = UserGroup.from_dict(group_dict)
  group2.uuid = ""
  group2.save()
  group2.uuid = group2.id
  group2.update()
  group_uuid_2 = group2.id

  ref_grp = group1.id

  users = [{
    **BASIC_USER_MODEL_EXAMPLE, "user_groups": [ref_grp],
    "user_type_ref": ""
  }, {
    **BASIC_USER_MODEL_EXAMPLE, "user_groups": [group_uuid_2],
    "user_type_ref": ""
  }, {
    **BASIC_USER_MODEL_EXAMPLE, "user_groups": [group_uuid_2],
    "user_type_ref": "", "user_type": "coach"
  }]
  for user in users:
    user_dict = {**user}
    create_user = User.from_dict(user_dict)
    create_user.user_id = ""
    create_user.save()
    create_user.user_id = create_user.id
    if ref_grp in user.get("user_groups"):
      ref_user_id = create_user.user_id
    create_user.update()

  url = f"{api_url}s"
  params = {"user_group": ref_grp}

  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"

  assert len(json_response.get("data")["records"
             ]) == 1, "Results should not be empty"
  retrieved_ids = [i.get("user_id") for i in
                   json_response.get("data")["records"]]
  assert ref_user_id in retrieved_ids, "expected data not retrieved"
  for i in json_response.get("data")["records"]:
    assert i["user_groups"][0] == ref_grp, "Filtered users have wrong group"


def test_get_all_users_by_status(clean_firestore):
  users = [{
    **BASIC_USER_MODEL_EXAMPLE, "user_type_ref": "", "user_groups": []
  }, {
    **BASIC_USER_MODEL_EXAMPLE, "status": "inactive",
    "user_type_ref": "", "user_groups": []
  }]
  for user in users:
    user_dict = {**user}
    create_user = User.from_dict(user_dict)
    create_user.user_id = ""
    create_user.save()
    create_user.user_id = create_user.id
    if create_user.status == "active":
      ref_user_id = create_user.user_id
    create_user.update()

  url = f"{api_url}s"
  params = {"status": "active"}

  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"

  assert len(json_response.get("data")["records"
             ]) == 1, "Results should not be empty"
  retrieved_ids = [i.get("user_id") for i in
                   json_response.get("data")["records"]]
  assert ref_user_id in retrieved_ids, "expected data not retrieved"
  for i in json_response.get("data")["records"]:
    assert i["status"] == "active", "Filtered users have wrong status"


@mock.patch(
  "services.json_import.create_learner", return_value="test_learner_id")
@mock.patch("services.json_import.create_learner_profile")
@mock.patch("services.json_import.create_agent")
@mock.patch("routes.user.is_inspace_enabled", return_value=True)
def test_post_user(mock_learner, mock_learner_profile, mock_agent,
                   mock_inspace_api, clean_firestore):
  input_user = deepcopy(BASIC_USER_MODEL_EXAMPLE)
  del input_user["inspace_user"]
  del input_user["is_deleted"]
  input_user["user_groups"] = []
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_user)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  post_json_response = post_resp.json()
  del post_json_response["data"]["created_time"]
  del post_json_response["data"]["last_modified_time"]
  user_id = post_json_response.get("data").get("user_id")

  # now see if GET endpoint returns same data
  url = f"{api_url}/{user_id}"
  get_resp = client_with_emulator.get(url)
  get_json_response = get_resp.json()
  del get_json_response["data"]["created_time"]
  del get_json_response["data"]["last_modified_time"]
  assert get_json_response.get("data") == post_json_response.get("data")

  # now check and confirm it is properly in the database
  loaded_user = User.find_by_uuid(user_id)
  loaded_user_dict = loaded_user.to_dict()

  # popping id and key for equivalency test
  loaded_user_dict.pop("id")
  loaded_user_dict.pop("key")
  loaded_user_dict.pop("created_by")
  loaded_user_dict.pop("created_time")
  loaded_user_dict.pop("last_modified_by")
  loaded_user_dict.pop("last_modified_time")
  loaded_user_dict.pop("archived_at_timestamp")
  loaded_user_dict.pop("archived_by")
  loaded_user_dict.pop("deleted_at_timestamp")
  loaded_user_dict.pop("deleted_by")

  # assert that rest of the fields are equivalent
  assert loaded_user_dict == post_json_response.get("data")


@mock.patch(
  "services.json_import.create_learner", return_value="test_learner_id")
@mock.patch("services.json_import.create_learner_profile")
@mock.patch("services.json_import.create_agent")
@mock.patch("routes.user.create_inspace_user_helper",
            return_value="Successfully created new User, " \
                         "corresponding agent and Inspace User")
@mock.patch("routes.user.is_inspace_enabled", return_value=True)
def test_post_user_and_inspace_user(mock_learner, mock_learner_profile,
                                    mock_agent, mock_inspace_user,
                                    mock_inspace_api, clean_firestore):
  input_user = deepcopy(BASIC_USER_MODEL_EXAMPLE)
  del input_user["inspace_user"]
  del input_user["is_deleted"]
  input_user["user_groups"] = []
  url = api_url
  params = {"create_inspace_user": True}
  post_resp = client_with_emulator.post(url, json=input_user, params=params)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"
  assert post_resp_json.get("data")["inspace_user"]["is_inspace_user"] is True


@mock.patch(
  "services.json_import.create_learner", return_value="test_learner_id")
@mock.patch("services.json_import.create_learner_profile")
@mock.patch("services.json_import.create_agent")
@mock.patch("common.utils.inspace.requests.post", return_value=Request(500))
@mock.patch("routes.user.is_inspace_enabled", return_value=True)
def test_post_user_and_inspace_user_negative(mock_learner,
                                             mock_learner_profile, mock_agent,
                                             mock_inspace_user,
                                             mock_inspace_api, clean_firestore):
  input_user = deepcopy(BASIC_USER_MODEL_EXAMPLE)
  del input_user["inspace_user"]
  del input_user["is_deleted"]
  input_user["user_groups"] = []
  url = api_url
  params = {"create_inspace_user": True}
  post_resp = client_with_emulator.post(url, json=input_user, params=params)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is False, "Success not false"
  assert post_resp.status_code == 500, "Status 500"
  assert post_resp_json.get("data") is None


@mock.patch(
  "services.json_import.create_learner", return_value="test_learner_id")
@mock.patch("services.json_import.create_learner_profile")
@mock.patch("services.json_import.create_agent")
@mock.patch("routes.user.is_inspace_enabled", return_value=True)
def test_post_user_faculty(mock_learner, mock_learner_profile, mock_agent,
                           mock_inspace_api, clean_firestore):
  input_user = deepcopy(BASIC_USER_MODEL_EXAMPLE)
  del input_user["inspace_user"]
  del input_user["is_deleted"]
  input_user["user_groups"] = []
  input_user["user_type"] = "coach"
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_user)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  post_json_response = post_resp.json()
  del post_json_response["data"]["created_time"]
  del post_json_response["data"]["last_modified_time"]
  user_id = post_json_response.get("data").get("user_id")

  # now see if GET endpoint returns same data
  url = f"{api_url}/{user_id}"
  get_resp = client_with_emulator.get(url)
  get_json_response = get_resp.json()
  del get_json_response["data"]["created_time"]
  del get_json_response["data"]["last_modified_time"]
  assert get_json_response.get("data") == post_json_response.get("data")

  # now check and confirm it is properly in the database
  loaded_user = User.find_by_uuid(user_id)
  loaded_user_dict = loaded_user.to_dict()

  # popping id and key for equivalency test
  loaded_user_dict.pop("id")
  loaded_user_dict.pop("key")
  loaded_user_dict.pop("created_by")
  loaded_user_dict.pop("created_time")
  loaded_user_dict.pop("last_modified_by")
  loaded_user_dict.pop("last_modified_time")
  loaded_user_dict.pop("archived_at_timestamp")
  loaded_user_dict.pop("archived_by")
  loaded_user_dict.pop("deleted_at_timestamp")
  loaded_user_dict.pop("deleted_by")

  # assert that rest of the fields are equivalent
  assert loaded_user_dict == post_json_response.get("data")

  # check if Staff is created
  # and the Staff uuid is added in User's user_type_ref
  staff_uuid = loaded_user_dict["user_type_ref"]
  assert Staff.find_by_uuid(staff_uuid).to_dict()["uuid"] == staff_uuid


@mock.patch(
  "services.json_import.create_learner", return_value="test_learner_id")
@mock.patch("services.json_import.create_learner_profile")
@mock.patch("services.json_import.create_agent")
@mock.patch("routes.user.is_inspace_enabled", return_value=True)
def test_post_user_correct_first_name(mock_learner, mock_learner_profile,
                                      mock_agent, mock_inspace_api,
                                      clean_firestore):
  input_user = deepcopy(BASIC_USER_MODEL_EXAMPLE)
  input_user["user_groups"] = []
  del input_user["inspace_user"]
  del input_user["is_deleted"]
  input_user["first_name"] = "Test@Userした"
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_user)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True
  assert post_resp.status_code == 200


@mock.patch(
  "services.json_import.create_learner", return_value="test_learner_id")
@mock.patch("services.json_import.create_learner_profile")
@mock.patch("services.json_import.create_agent")
@mock.patch("routes.user.is_inspace_enabled", return_value=True)
def test_post_user_incorrect_last_name(mock_learner, mock_learner_profile,
                                       mock_agent, mock_inspace_api,
                                       clean_firestore):
  input_user = deepcopy(BASIC_USER_MODEL_EXAMPLE)
  input_user["user_groups"] = []
  input_user["last_name"] = ""
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_user)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is False
  assert post_resp.status_code == 422


@mock.patch(
  "services.json_import.create_learner", return_value="test_learner_id")
@mock.patch("services.json_import.create_learner_profile")
@mock.patch("services.json_import.create_agent")
@mock.patch("routes.user.is_inspace_enabled", return_value=True)
def test_post_user_incorrect_email(mock_learner, mock_learner_profile,
                                   mock_agent, mock_inspace_api,
                                   clean_firestore):
  input_user = deepcopy(BASIC_USER_MODEL_EXAMPLE)
  input_user["user_groups"] = []
  input_user["email"] = "TestEmail"
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_user)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is False
  assert post_resp.status_code == 422


@mock.patch(
  "services.json_import.create_learner", return_value="test_learner_id")
@mock.patch("services.json_import.create_learner_profile")
@mock.patch("services.json_import.create_agent")
@mock.patch("routes.user.is_inspace_enabled", return_value=True)
def test_post_user_with_group(mock_learner, mock_learner_profile, mock_agent,
                              mock_inspace_api, clean_firestore):
  group_dict = {**BASIC_GROUP_MODEL_EXAMPLE, "name": "learner",
                "is_immutable": True}
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()
  group_uuid = group.id
  BASIC_USER_MODEL_EXAMPLE["first_name"] = "steve"
  BASIC_USER_MODEL_EXAMPLE["last_name"] = "jobs"
  BASIC_USER_MODEL_EXAMPLE["email"] = "steve.jobs@apple.inc"
  input_user = {
    **BASIC_USER_MODEL_EXAMPLE,
    "user_groups": [group_uuid]
  }
  del input_user["inspace_user"]
  del input_user["is_deleted"]
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_user)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  post_json_response = post_resp.json()
  del post_json_response["data"]["created_time"]
  del post_json_response["data"]["last_modified_time"]
  user_id = post_json_response.get("data").get("user_id")

  # now see if GET endpoint returns same data
  url = f"{api_url}/{user_id}"
  get_resp = client_with_emulator.get(url)
  get_json_response = get_resp.json()
  del get_json_response["data"]["created_time"]
  del get_json_response["data"]["last_modified_time"]
  assert get_json_response.get("data") == post_json_response.get("data")

  # now check if user is added to group
  get_group = UserGroup.find_by_uuid(group_uuid)
  get_group_dict = get_group.to_dict()
  # assert that user is added to group sccessfully
  assert user_id in get_group_dict.get("users")

  # check if user is added to valid group
  assert group_uuid in post_resp_json["data"].get("user_groups")


@mock.patch("routes.user.get_agent", return_value="test_agent_id")
@mock.patch("routes.user.update_agent")
@mock.patch("routes.user.update_learner")
@mock.patch("routes.user.is_inspace_enabled", return_value=True)
def test_update_groups_for_user(mock_get_agent, mock_update_agent,
                                mock_update_learner,
                                mock_inspace_api, clean_firestore):
  group_list = [{
    **BASIC_GROUP_MODEL_EXAMPLE, "name": "learner", "is_immutable": True,
    "users": []
  }, {
    **BASIC_GROUP_MODEL_EXAMPLE, "name": "group-2",
    "users": []
  }]
  group_uuids = []
  for group in group_list:
    group = UserGroup.from_dict(group)
    group.uuid = ""
    group.save()
    group.uuid = group.id
    group.update()
    group_uuids.append(group.id)

  user_dict = {
    **BASIC_USER_MODEL_EXAMPLE, "user_groups": [group_uuids[0]],
    "user_type_ref": ""
  }
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  user_user_id = user.id

  url = f"{api_url}/{user_user_id}"
  updated_data = {"user_groups": [group_uuids[1]]}
  resp = client_with_emulator.put(url, json=updated_data)
  update_response = resp.json()

  assert update_response.get("success") is True, "Success not true"
  assert update_response.get(
    "message"
  ) == "Successfully updated the user", "Expected response not same"

  # check if user group of users is successflly updated
  updated_user = User.find_by_uuid(user_user_id)
  updated_user_fields = updated_user.get_fields()
  assert updated_user_fields.get("user_groups") == updated_data["user_groups"]

  # check if user is successfully added to new group
  updated_group = UserGroup.find_by_uuid(group_uuids[1])
  updated_group_fields = updated_group.get_fields()
  assert updated_group_fields.get("users") == [user_user_id]

  # check if user is successfully removed from previous group
  updated_group = UserGroup.find_by_uuid(group_uuids[0])
  updated_group_fields = updated_group.get_fields()
  assert not user_user_id in updated_group_fields.get("users")


@mock.patch("routes.user.get_agent", return_value="test_agent_id")
@mock.patch("routes.user.update_agent")
@mock.patch("routes.user.update_learner")
@mock.patch("routes.user.is_inspace_enabled", return_value=True)
def test_update_user(mock_get_agent, mock_update_agent, mock_update_learner,
                     mock_inspace_api, clean_firestore):
  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": "",
               "user_groups": []}
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  user_user_id = user.id

  url = f"{api_url}/{user_user_id}"
  updated_data = {"first_name": "name updated"}
  resp = client_with_emulator.put(url, json=updated_data)
  update_response = resp.json()

  assert update_response.get("success") is True, "Success not true"
  assert update_response.get(
    "message"
  ) == "Successfully updated the user", "Expected response not same"


@mock.patch(
  "services.json_import.create_learner", return_value="test_learner_id")
@mock.patch("services.json_import.create_learner_profile")
@mock.patch("services.json_import.create_agent")
@mock.patch("routes.user.get_agent", return_value="test_agent_id")
@mock.patch("routes.user.update_agent")
@mock.patch("services.learner.update_learner")
@mock.patch("routes.user.is_inspace_enabled", return_value=True)
def test_update_user_staff(mock_create_learner, mock_create_learner_profile,
                           mock_create_agent, mock_get_agent, mock_update_agent,
                           mock_update_learner, mock_inspace_api,
                           clean_firestore):
  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_groups": []}
  del user_dict["inspace_user"]
  del user_dict["is_deleted"]
  user_dict["user_type"] = "coach"
  post_resp = client_with_emulator.post(api_url, json=user_dict)
  post_resp_json = post_resp.json()
  user_id = post_resp_json["data"]["user_id"]
  staff_uuid = post_resp_json["data"]["user_type_ref"]

  update_dict = {"first_name": "udpated_first_name"}
  url = f"{api_url}/{user_id}"
  resp = client_with_emulator.put(url, json=update_dict)
  update_response = resp.json()

  assert update_response["data"]["first_name"] == update_dict["first_name"]
  staff = Staff.find_by_uuid(staff_uuid)
  assert staff.first_name == update_dict["first_name"]


@mock.patch("routes.user.is_inspace_enabled", return_value=True)
def test_update_user_negative(mock_inspace_api, clean_firestore):
  user_dict = {**BASIC_USER_MODEL_EXAMPLE}
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  user_id = "U2DDBkl3Ayg0PWudzhI"

  url = f"{api_url}/{user_id}"
  response = {
    "success": False,
    "message": "User with user_id U2DDBkl3Ayg0PWudzhI not found",
    "data": None
  }
  update_user_dict = {"first_name": "updated name"}
  resp = client_with_emulator.put(url, json=update_user_dict)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


@mock.patch(
  "routes.user.get_agent", return_value="test_agent_id")
@mock.patch("routes.user.delete_agent")
@mock.patch("routes.user.delete_learner_profile")
@mock.patch("routes.user.delete_learner")
@mock.patch("routes.user.is_inspace_enabled", return_value=True)
def test_delete_user(mock_get_agent, mock_delete_agent,
                     mock_delete_learner_profile, mock_delete_learner,
                     mock_inspace_api, clean_firestore):
  user_dict = {**BASIC_USER_MODEL_EXAMPLE}
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  user_id = user.user_id
  user_dict["user_id"] = user.id

  url = f"{api_url}/{user_id}"
  resp = client_with_emulator.delete(url)
  del_json_response = resp.json()
  mes = "Successfully deleted the user and associated agent, learner/faculty"
  expected_data = {"success": True,
                   "message": mes}
  assert resp.status_code == 200, "Status code not 200"
  assert del_json_response == expected_data, "Expected response not same"


@mock.patch(
  "services.json_import.create_learner", return_value="test_learner_id")
@mock.patch("services.json_import.create_learner_profile")
@mock.patch("services.json_import.create_agent")
@mock.patch("routes.user.delete_agent")
@mock.patch("routes.user.get_agent")
@mock.patch("routes.user.is_inspace_enabled", return_value=True)
def test_delete_user_faculty(mock_learner, mock_learner_profile, mock_agent,
                             mock_del_agent, mock_get_agent,
                             mock_inspace_api, clean_firestore):
  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_groups": []}
  del user_dict["inspace_user"]
  del user_dict["is_deleted"]
  user_dict["user_type"] = "coach"
  post_resp = client_with_emulator.post(api_url, json=user_dict)
  post_resp_json = post_resp.json()

  user_id = post_resp_json["data"]["user_id"]

  staff_uuid = post_resp_json["data"]["user_type_ref"]
  assert Staff.find_by_uuid(staff_uuid).to_dict()["uuid"] == staff_uuid

  url = f"{api_url}/{user_id}"
  resp = client_with_emulator.delete(url)
  del_json_response = resp.json()

  with pytest.raises(ResourceNotFoundException):
    Staff.find_by_uuid(staff_uuid)
  mes = "Successfully deleted the user and associated agent, learner/faculty"
  expected_data = {"success": True,
                   "message": mes}
  assert resp.status_code == 200, "Status code not 200"
  assert del_json_response == expected_data, "Expected response not same"


def test_delete_user_negative(clean_firestore):
  user_id = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{user_id}"
  response = {
    "success": False,
    "message": "User with user_id U2DDBkl3Ayg0PWudzhI not found",
    "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_search_user_by_email(clean_firestore):
  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": "",
               "user_groups": []}
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  user_dict["user_id"] = user.id

  params = {"email": user_dict.get("email")}

  url = f"{api_url}/search/email"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert json_response.get("data")[0].get(
    "email") == BASIC_USER_MODEL_EXAMPLE.get("email"), "Response received"


def test_search_user_by_email_negative(clean_firestore):
  params = {"email": "test.email"}

  url = f"{api_url}/search/email"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422
  assert json_response.get("success") is False
  assert json_response.get("data") is None


def test_update_user_status_to_inactive(clean_firestore):
  user_dict = {
    **BASIC_USER_MODEL_EXAMPLE, "status": "active",
    "user_groups": ["test_group_id"],
    "user_type_ref": ""
  }
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  user_user_id = user.id

  group_dict = {**BASIC_GROUP_MODEL_EXAMPLE, "users": [user_user_id]}
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = "test_group_id"
  group.update()
  group_dict["uuid"] = "test_group_id"

  url = f"{api_url}/{user_user_id}/status"
  updated_data = {"status": "inactive"}
  resp = client_with_emulator.put(url, json=updated_data)
  update_response = resp.json()

  assert update_response.get("success") is True, "Success not true"
  assert update_response.get(
    "message"
  ) == "Successfully updated the user status", "Expected response not same"
  assert update_response.get("data").get(
    "status") == "inactive", "Expected response not same"


def test_update_user_status_to_active(clean_firestore):
  user_dict = {
    **BASIC_USER_MODEL_EXAMPLE, "status": "inactive",
    "user_groups": [],
    "user_type_ref": ""
  }
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  user_user_id = user.id

  url = f"{api_url}/{user_user_id}/status"
  updated_data = {"status": "active"}
  resp = client_with_emulator.put(url, json=updated_data)
  update_response = resp.json()

  assert update_response.get("success") is True, "Success not true"
  assert update_response.get(
    "message"
  ) == "Successfully updated the user status", "Expected response not same"
  assert update_response.get("data").get(
    "status") == "active", "Expected response not same"


def test_search_users(clean_firestore):
  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": "",
               "user_groups": []}
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  filter_key = user.first_name
  url = f"{api_url}/search"
  params = {"search_query": filter_key}

  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"
  assert json_response.get("success") is True
  assert len(json_response.get("data")) > 0, "Results should not be empty"
  for i in json_response.get("data"):
    assert i["first_name"] == filter_key, "Filtered output is wrong"


def test_search_users_negative(clean_firestore):
  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  filter_key = user.first_name
  url = f"{api_url}/search"
  params = {"search_query": filter_key, "skip": 0, "limit": 0}

  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422, "Status should not be 200"
  assert json_response.get("success") is False


def test_get_user_applications(clean_firestore):
  user_dict = {
    **BASIC_USER_MODEL_EXAMPLE, "status": "inactive",
    "user_groups": []
  }
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  user_user_id = user.id

  application_dict = {**BASIC_APPLICATION_MODEL_EXAMPLE}
  application = Application.from_dict(application_dict)
  application.uuid = ""
  application.save()
  application.uuid = application.id
  application.update()
  application_uuid = application.id

  group_dict = {
    **BASIC_GROUP_MODEL_EXAMPLE, "users": [user.id],
    "applications": [application_uuid]
  }
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()

  user.user_groups = [group.id]
  user.update()

  url = f"{api_url}/{user_user_id}/applications"
  resp = client_with_emulator.get(url)
  applications_res = resp.json()

  assert applications_res.get("success") is True, "Success not true"
  assert applications_res.get(
    "message") == "Successfully fetched applications assigned to the user", \
    "Expected response not same"
  assert application_uuid in [
    i.get("application_id")
    for i in applications_res.get("data")["applications"]
  ]


@mock.patch(
  "services.json_import.create_learner", return_value="test_learner_id")
@mock.patch("services.json_import.create_learner_profile")
@mock.patch("services.json_import.create_agent")
@mock.patch("routes.user.create_inspace_user_helper",
            return_value="Successfully created new User, " \
                         "corresponding agent and Inspace User")
@mock.patch("routes.user.get_agent", return_value="test_agent_id")
@mock.patch("routes.user.update_agent")
@mock.patch("routes.user.update_learner")
@mock.patch("routes.user.update_inspace_user_helper", return_value=True)
@mock.patch("routes.user.is_inspace_enabled", return_value=True)
def test_update_inspace_user_positive(mock_learner, mock_learner_profile,
                                      mock_agent, mock_inspace_user,
                                      mock_get_agent, mock_update_agent,
                                      mock_update_learner,
                                      mock_update_inspace_user,
                                      mock_inspace_api, clean_firestore):
  input_user = deepcopy(BASIC_USER_MODEL_EXAMPLE)
  del input_user["inspace_user"]
  del input_user["is_deleted"]
  input_user["user_groups"] = []
  url = api_url
  params = {"create_inspace_user": True}
  post_resp = client_with_emulator.post(url, json=input_user, params=params)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"
  assert post_resp_json.get("data")["inspace_user"]["is_inspace_user"] is True

  user_id = post_resp_json.get("data")["user_id"]

  update_payload = {
    "first_name": "updated fname",
    "last_name": "updated lname"
  }
  query_params = {
    "update_inspace_user": True
  }
  res = client_with_emulator.put(f"{url}/{user_id}",
                                 json=update_payload,
                                 params=query_params)
  res_json = res.json()
  assert res.status_code == 200
  assert res_json.get("success") is True
  assert res_json["message"] == "Successfully updated the user and " \
                                "corresponding Inspace user"


@mock.patch(
  "services.json_import.create_learner", return_value="test_learner_id")
@mock.patch("services.json_import.create_learner_profile")
@mock.patch("services.json_import.create_agent")
@mock.patch("routes.user.create_inspace_user_helper",
            return_value="Successfully created new User, " \
                         "corresponding agent and Inspace User")
@mock.patch("routes.user.get_agent", return_value="test_agent_id")
@mock.patch("routes.user.update_agent")
@mock.patch("routes.user.update_learner")
@mock.patch("routes.user.update_inspace_user_helper", return_value=False)
@mock.patch("routes.user.is_inspace_enabled", return_value=True)
def test_update_inspace_user_negative(mock_learner, mock_learner_profile,
                                      mock_agent, mock_inspace_user,
                                      mock_get_agent, mock_update_agent,
                                      mock_update_learner,
                                      mock_update_inspace_user,
                                      mock_inspace_call, clean_firestore):
  input_user = deepcopy(BASIC_USER_MODEL_EXAMPLE)
  del input_user["inspace_user"]
  del input_user["is_deleted"]
  input_user["user_groups"] = []
  url = api_url
  params = {"create_inspace_user": True}
  post_resp = client_with_emulator.post(url, json=input_user, params=params)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"
  assert post_resp_json.get("data")["inspace_user"]["is_inspace_user"] is True

  user_id = post_resp_json.get("data")["user_id"]

  update_payload = {
    "first_name": "updated fname",
    "last_name": "updated lname"
  }
  query_params = {
    "update_inspace_user": True
  }
  res = client_with_emulator.put(f"{url}/{user_id}",
                                 json=update_payload,
                                 params=query_params)
  res_json = res.json()
  assert res.status_code == 200
  assert res_json.get("success") is True
  assert res_json["message"] == "Successfully updated the user but " \
                                "corresponding Inspace user couldn't be updated"


@mock.patch(
  "services.json_import.create_learner", return_value="test_learner_id")
@mock.patch("services.json_import.create_learner_profile")
@mock.patch("services.json_import.create_agent")
@mock.patch("routes.user.create_inspace_user_helper",
            return_value="Successfully created new User, " \
                         "corresponding agent and Inspace User")
@mock.patch(
  "routes.user.get_agent", return_value="test_agent_id")
@mock.patch("routes.user.delete_agent")
@mock.patch("routes.user.delete_learner_profile")
@mock.patch("routes.user.delete_learner")
@mock.patch("routes.user.delete_inspace_user_helper", return_value=True)
@mock.patch("routes.user.is_inspace_enabled", return_value=True)
def test_delete_inspace_user_positive(mock_learner, mock_learner_profile,
                                      mock_agent, mock_inspace_user,
                                      mock_get_agent,
                                      mock_delete_agent,
                                      mock_delete_learner_profile,
                                      mock_delete_learner,
                                      mock_delete_inspace_usere,
                                      mock_inspace_call, clean_firestore):
  input_user = deepcopy(BASIC_USER_MODEL_EXAMPLE)
  del input_user["inspace_user"]
  del input_user["is_deleted"]
  input_user["user_groups"] = []
  url = api_url
  params = {"create_inspace_user": True}
  post_resp = client_with_emulator.post(url, json=input_user, params=params)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"
  assert post_resp_json.get("data")["inspace_user"]["is_inspace_user"] is True

  user_id = post_resp_json.get("data")["user_id"]

  query_params = {
    "delete_inspace_user": True
  }
  mes = "Successfully deleted the user and associated agent, learner/faculty " \
        "and Inspace User"
  res = client_with_emulator.delete(f"{url}/{user_id}", params=query_params)
  res_json = res.json()
  assert res.status_code == 200
  assert res_json.get("success") is True
  assert res_json["message"] == mes


@mock.patch(
  "services.json_import.create_learner", return_value="test_learner_id")
@mock.patch("services.json_import.create_learner_profile")
@mock.patch("services.json_import.create_agent")
@mock.patch("routes.user.create_inspace_user_helper",
            return_value="Successfully created new User, " \
                         "corresponding agent and Inspace User")
@mock.patch(
  "routes.user.get_agent", return_value="test_agent_id")
@mock.patch("routes.user.delete_agent")
@mock.patch("routes.user.delete_learner_profile")
@mock.patch("routes.user.delete_learner")
@mock.patch("routes.user.delete_inspace_user_helper", return_value=False)
@mock.patch("routes.user.is_inspace_enabled", return_value=True)
def test_delete_inspace_user_negative(mock_learner, mock_learner_profile,
                                      mock_agent, mock_inspace_user,
                                      mock_get_agent, mock_delete_agent,
                                      mock_delete_learner_profile,
                                      mock_delete_learner,
                                      mock_delete_inspace_usere,
                                      mock_inspace_call, clean_firestore):
  input_user = deepcopy(BASIC_USER_MODEL_EXAMPLE)
  del input_user["inspace_user"]
  del input_user["is_deleted"]
  input_user["user_groups"] = []
  url = api_url
  params = {"create_inspace_user": True}
  post_resp = client_with_emulator.post(url, json=input_user, params=params)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"
  assert post_resp_json.get("data")["inspace_user"]["is_inspace_user"] is True

  user_id = post_resp_json.get("data")["user_id"]

  query_params = {
    "delete_inspace_user": True
  }
  res = client_with_emulator.delete(f"{url}/{user_id}", params=query_params)
  res_json = res.json()
  assert res.status_code == 200
  assert res_json.get("success") is True
  assert res_json["message"] == "Successfully deleted the user and " \
                                "associated agent, learner/faculty but could" \
                                " not delete Inspace User"
