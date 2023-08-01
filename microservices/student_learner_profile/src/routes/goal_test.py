"""
  Unit tests for Goal endpoints
"""
import os
import json
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.goal import router
from testing.test_config import (API_URL, TESTING_FOLDER_PATH)
from schemas.schema_examples import BASIC_GOAL_EXAMPLE
from common.models import Goal
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/learner-profile-service/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/goal"

GOAL_TESTDATA_FILENAME = os.path.join(TESTING_FOLDER_PATH, "goals.json")

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_get_goal(clean_firestore):
  goal_dict = {**BASIC_GOAL_EXAMPLE}
  goal = Goal.from_dict(goal_dict)
  goal.uuid = ""
  goal.save()
  goal.uuid = goal.id
  goal.update()
  goal_dict["uuid"] = goal.id
  goal_dict["is_archived"] = False

  url = f"{api_url}/{goal.uuid}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  del json_response["data"]["created_time"]
  del json_response["data"]["last_modified_time"]
  assert resp.status_code == 200, "Status 200"
  assert json_response.get("data") == goal_dict, "Response received"


def test_get_goal_negative_1(clean_firestore):
  """Get a goal with incorrect uuid"""
  uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{uuid}"
  data = {
      "success": False,
      "message": f"Goal with uuid {uuid} not found",
      "data": None
  }

  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 404, "Status 404"
  assert json_response == data, "Response received"


def test_get_goal_negative_2(clean_firestore):
  """Test get deleted goal"""
  goal_dict = {**BASIC_GOAL_EXAMPLE}
  goal = Goal.from_dict(goal_dict)
  goal.uuid = ""
  goal.is_deleted = True
  goal.save()
  goal.uuid = goal.id
  goal.update()

  url = f"{api_url}/{goal.uuid}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  data = {
      "success": False,
      "message": f"Goal with uuid {goal.uuid} not found",
      "data": None
  }
  assert resp.status_code == 404, "Status 404"
  assert json_response == data, "Response received"


def test_get_all_goals(clean_firestore):
  goal_dict = {**BASIC_GOAL_EXAMPLE}

  # goal
  goal = Goal.from_dict(goal_dict)
  goal.uuid = ""
  goal.save()
  goal.uuid = goal.id
  goal.update()

  # deleted goal
  deleted_goal = Goal.from_dict(goal_dict)
  deleted_goal.uuid = ""
  deleted_goal.is_deleted = True
  deleted_goal.save()
  deleted_goal.uuid = deleted_goal.id
  deleted_goal.update()

  # archived goal
  archived_goal = Goal.from_dict(goal_dict)
  archived_goal.uuid = ""
  archived_goal.is_archived = True
  archived_goal.save()
  archived_goal.uuid = archived_goal.id
  archived_goal.update()

  params = {"skip": 0, "limit": "30", "fetch_archive": False}

  url = f"{api_url}"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"
  retrieved_ids = [i.get("uuid") for i in json_response.get("data")["records"]]
  assert goal.uuid in retrieved_ids, "expected data not retrived"
  assert deleted_goal.uuid not in retrieved_ids, "unexpected data retrived"
  assert archived_goal.uuid not in retrieved_ids, "is_archived not working"


def test_get_all_goals_with_filter(clean_firestore):
  goal_dict = {**BASIC_GOAL_EXAMPLE}
  goal_dict["type"] = "Long-term"
  # goal
  goal = Goal.from_dict(goal_dict)
  goal.uuid = ""
  goal.save()
  goal.uuid = goal.id
  goal.update()

  # deleted goal
  deleted_goal = Goal.from_dict(goal_dict)
  deleted_goal.uuid = ""
  deleted_goal.is_deleted = True
  deleted_goal.save()
  deleted_goal.uuid = deleted_goal.id
  deleted_goal.update()

  url = f"{api_url}"
  goal_type = "Long-term"
  url = f"{api_url}?goal_type={goal_type}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"

  assert len(
    json_response.get("data")["records"]) > 0, "Results should not be empty"
  retrieved_ids = [i.get("uuid") for i in json_response.get("data")["records"]]
  assert goal.uuid in retrieved_ids, "expected data not retrived"
  assert deleted_goal.uuid not in retrieved_ids, "unexpected data retrived"
  for i in json_response.get("data")["records"]:
    assert i["type"] == goal_type, "Filtered output is wrong"


def test_post_goal(clean_firestore):
  input_goal = BASIC_GOAL_EXAMPLE
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_goal)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  post_json_response = json.loads(post_resp.text)
  del post_json_response["data"]["created_time"]
  del post_json_response["data"]["last_modified_time"]
  uuid = post_json_response.get("data").get("uuid")

  # now see if GET endpoint returns same data
  url = f"{api_url}/{uuid}"
  get_resp = client_with_emulator.get(url)
  get_json_response = json.loads(get_resp.text)
  del get_json_response["data"]["created_time"]
  del get_json_response["data"]["last_modified_time"]
  assert get_json_response.get("data") == post_json_response.get("data")

  # now check and confirm it is properly in the databse
  loaded_goal = Goal.find_by_uuid(uuid)
  loaded_goal_dict = loaded_goal.to_dict()

  # popping id and key for equivalency test
  loaded_goal_dict.pop("id")
  loaded_goal_dict.pop("key")
  loaded_goal_dict.pop("created_by")
  loaded_goal_dict.pop("created_time")
  loaded_goal_dict.pop("last_modified_by")
  loaded_goal_dict.pop("last_modified_time")
  loaded_goal_dict.pop("is_deleted")

  # assert that rest of the fields are equivalent
  assert loaded_goal_dict == post_json_response.get("data")


def test_update_goal(clean_firestore):
  goal_dict = {**BASIC_GOAL_EXAMPLE}
  goal = Goal.from_dict(goal_dict)
  goal.uuid = ""
  goal.save()
  goal.uuid = goal.id
  goal.update()
  goal_uuid = goal.id

  url = f"{api_url}/{goal_uuid}"
  updated_data = goal_dict
  updated_data["type"] = "Short-term"
  resp = client_with_emulator.put(url, json=updated_data)
  json_response_update_req = resp.json()

  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get(
      "message"
  ) == "Successfully updated the goal", "Expected response not same"
  assert json_response_update_req.get("data").get(
      "type") == "Short-term", "Expected response not same"


def test_update_goal_negative(clean_firestore):
  goal_dict = {**BASIC_GOAL_EXAMPLE}
  goal = Goal.from_dict(goal_dict)
  goal.uuid = ""
  goal.save()
  goal.uuid = goal.id
  goal.update()
  goal_uuid = "U2DDBkl3Ayg0PWudzhI"

  url = f"{api_url}/{goal_uuid}"
  response = {
      "success": False,
      "message": "Goal with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.put(url, json=goal_dict)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_delete_goal(clean_firestore):
  goal_dict = {**BASIC_GOAL_EXAMPLE}
  goal = Goal.from_dict(goal_dict)
  goal.uuid = ""
  goal.save()
  goal.uuid = goal.id
  goal.update()
  goal_dict["uuid"] = goal.id

  uuid = goal.uuid
  goal_dict["uuid"] = uuid

  url = f"{api_url}/{uuid}"
  resp = client_with_emulator.delete(url)
  del_json_response = resp.json()

  expected_data = {"success": True, "message": "Successfully deleted the goal"}
  assert resp.status_code == 200, "Status code not 200"
  deleted_goal = Goal.find_by_uuid(goal.uuid, is_deleted=True)
  assert deleted_goal.is_deleted is True, "Goal was not deleted"
  assert del_json_response == expected_data, "Expected response not same"


def test_delete_goal_negative(clean_firestore):
  goal_uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{goal_uuid}"
  response = {
      "success": False,
      "message": "Goal with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_import_goals(clean_firestore):
  url = f"{api_url}/import/json"
  with open(GOAL_TESTDATA_FILENAME, encoding="UTF-8") as goals_json_file:
    resp = client_with_emulator.post(url, files={"json_file": goals_json_file})

  json_response = resp.json()
  assert resp.status_code == 200, "Status not 200"
  assert isinstance(json_response.get("data"), list), "Response is not a list"
  assert len(json_response.get("data")) > 0, "Empty list returned"


def test_search_goal(clean_firestore):
  goal_dict = {**BASIC_GOAL_EXAMPLE}

  # goal
  goal = Goal.from_dict(goal_dict)
  goal.uuid = ""
  goal.save()
  goal.uuid = goal.id
  goal.update()
  goal_dict["uuid"] = goal.id

  # deleted goal
  deleted_goal = Goal.from_dict(goal_dict)
  deleted_goal.uuid = ""
  deleted_goal.is_deleted = True
  deleted_goal.save()
  deleted_goal.uuid = deleted_goal.id
  deleted_goal.update()

  params = {"name": "Intellectual Skills"}

  url = f"{api_url}/search"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  retrieved_ids = [i.get("uuid") for i in json_response.get("data")]
  assert goal.uuid in retrieved_ids, "expected data not retrived"
  assert deleted_goal.uuid not in retrieved_ids, "unexpected data retrived"
  assert json_response.get("data")[0].get("name") == BASIC_GOAL_EXAMPLE.get(
      "name"), "Response received"


def test_archive_goal(clean_firestore):
  goal_dict = {**BASIC_GOAL_EXAMPLE}
  goal = Goal.from_dict(goal_dict)
  goal.uuid = ""
  goal.is_archived = False  # goal not archived initially
  goal.save()
  goal.uuid = goal.id
  goal.update()
  goal_uuid = goal.id

  url = f"{api_url}/{goal_uuid}"
  updated_data = goal_dict
  updated_data["is_archived"] = True
  resp = client_with_emulator.put(url, json=updated_data)
  json_response_update_req = resp.json()

  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get(
      "message"
  ) == "Successfully updated the goal", "Expected response not same"
  assert json_response_update_req.get("data").get(
      "is_archived") is True, "Expected response not same"
