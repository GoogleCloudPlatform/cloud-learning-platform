"""
  Unit tests for Achievement endpoints
"""
import os
import json
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.achievement import router
from testing.test_config import (API_URL, TESTING_FOLDER_PATH)
from schemas.schema_examples import BASIC_ACHIEVEMENT_EXAMPLE
from common.models import Achievement
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/learner-profile-service/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/achievement"

ACHIEVEMENT_TESTDATA_FILENAME = os.path.join(TESTING_FOLDER_PATH,
                                             "achievements.json")

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_post_achievement(clean_firestore):
  input_achievement = {**BASIC_ACHIEVEMENT_EXAMPLE}
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_achievement)
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

  # now check and confirm it is properly in the database
  loaded_achievement = Achievement.find_by_uuid(uuid)
  loaded_achievement_dict = loaded_achievement.to_dict()

  # popping id and key for equivalency test
  loaded_achievement_dict.pop("id")
  loaded_achievement_dict.pop("key")
  loaded_achievement_dict.pop("created_by")
  loaded_achievement_dict.pop("created_time")
  loaded_achievement_dict.pop("last_modified_by")
  loaded_achievement_dict.pop("last_modified_time")
  loaded_achievement_dict.pop("is_deleted")

  # # assert that rest of the fields are equivalent
  # assert loaded_achievement_dict == post_json_response.get("data")


def test_update_achievement(clean_firestore):
  achievement_dict = {**BASIC_ACHIEVEMENT_EXAMPLE}
  achievement = Achievement.from_dict(achievement_dict)
  achievement.uuid = ""
  achievement.save()
  achievement.uuid = achievement.id
  achievement.update()
  achievement_uuid = achievement.id

  url = f"{api_url}/{achievement_uuid}"
  updated_data = achievement_dict
  updated_data["type"] = "competency"
  resp = client_with_emulator.put(url, json=updated_data)
  json_response_update_req = resp.json()

  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get(
      "message"
  ) == "Successfully updated the achievement", "Expected response not same"
  assert json_response_update_req.get("data").get(
      "type") == "competency", "Expected response not same"


def test_update_achievement_negative(clean_firestore):
  achievement_dict = {**BASIC_ACHIEVEMENT_EXAMPLE}
  achievement = Achievement.from_dict(achievement_dict)
  achievement.uuid = ""
  achievement.save()
  achievement.uuid = achievement.id
  achievement.update()
  achievement_uuid = "U2DDBkl3Ayg0PWudzhI"

  url = f"{api_url}/{achievement_uuid}"
  response = {
      "success": False,
      "message": "Achievement with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.put(url, json=achievement_dict)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_delete_achievement(clean_firestore):
  achievement_dict = {**BASIC_ACHIEVEMENT_EXAMPLE}
  achievement = Achievement.from_dict(achievement_dict)
  achievement.uuid = ""
  achievement.save()
  uuid = achievement.uuid = achievement.id
  achievement.update()
  achievement_dict["uuid"] = achievement.id

  url = f"{api_url}/{uuid}"
  resp = client_with_emulator.delete(url)
  del_json_response = resp.json()

  expected_data = {
      "success": True,
      "message": "Successfully deleted the achievement"
  }
  deleted_achievement = Achievement.find_by_uuid(
      achievement.uuid, is_deleted=True)
  assert resp.status_code == 200, "Status code not 200"
  assert deleted_achievement.is_deleted is True, "Document was not deleted"
  assert del_json_response == expected_data, "Expected response not same"


def test_delete_achievement_negative(clean_firestore):
  achievement_uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{achievement_uuid}"
  response = {
      "success": False,
      "message": "Achievement with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_import_achievements(clean_firestore):
  url = f"{api_url}/import/json"
  with open(
      ACHIEVEMENT_TESTDATA_FILENAME,
      encoding="UTF-8") as achievements_json_file:
    resp = client_with_emulator.post(
        url, files={"json_file": achievements_json_file})

  json_response = resp.json()
  assert resp.status_code == 200, "Status not 200"
  assert isinstance(json_response.get("data"), list), "Response is not a list"
  assert len(json_response.get("data")) > 0, "Empty list returned"


def test_get_achievements(clean_firestore):
  achievement_dict = {**BASIC_ACHIEVEMENT_EXAMPLE}
  achievement_dict["type"] = "course equate"

  # achievement
  achievement = Achievement.from_dict(achievement_dict)
  achievement.uuid = ""
  achievement.save()
  achievement.uuid = achievement.id
  achievement.update()

  # deleted achievements
  deleted_achievement = Achievement.from_dict(achievement_dict)
  deleted_achievement.uuid = ""
  deleted_achievement.is_deleted = True
  deleted_achievement.save()
  deleted_achievement.uuid = deleted_achievement.id
  deleted_achievement.update()

  # archived achievement
  archived_achievement = Achievement.from_dict(achievement_dict)
  archived_achievement.uuid = ""
  archived_achievement.is_archived = True
  archived_achievement.save()
  archived_achievement.uuid = archived_achievement.id
  archived_achievement.update()
  params = {"skip": 0, "limit": "30", "fetch_archive": False}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  retrieved_achievement_ids = [
    i.get("uuid") for i in json_response.get("data")["records"]]
  assert achievement.uuid in \
    retrieved_achievement_ids, "expected data not retrived"
  assert deleted_achievement.uuid not in \
    retrieved_achievement_ids, "unexpected data retrived"
  assert archived_achievement.uuid not in \
    retrieved_achievement_ids, "is_archived not working"


def test_get_achievements_with_filters(clean_firestore):
  achievement_dict = {**BASIC_ACHIEVEMENT_EXAMPLE}
  achievement_dict["type"] = "course equate"

  # achievement
  achievement = Achievement.from_dict(achievement_dict)
  achievement.uuid = ""
  achievement.save()
  achievement.uuid = achievement.id
  achievement.update()

  # deleted_achievement
  deleted_achievement = Achievement.from_dict(achievement_dict)
  deleted_achievement.uuid = ""
  deleted_achievement.is_deleted = True
  deleted_achievement.save()
  deleted_achievement.uuid = deleted_achievement.id
  deleted_achievement.update()

  # Filter by achievement_type:
  filter_params = {"achievement_type": "course equate"}
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=filter_params)
  json_response = resp.json()

  assert resp.status_code == 200, "Status should be 200"
  assert len(json_response.get("data")[
    "records"]) > 0, "Results should not be empty"
  retrieved_achievement_ids = [
    i.get("uuid") for i in json_response.get("data")["records"]]
  assert achievement.uuid in \
    retrieved_achievement_ids, "expected data not retrived"
  assert deleted_achievement.uuid not in \
    retrieved_achievement_ids, "unexpected data retrived"
  for i in json_response.get("data")["records"]:
    assert i["type"] == "course equate", "Filtered output is wrong"

  # Filter by Name:
  filter_params_2 = {"name": "ML Professional"}
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=filter_params_2)
  json_response = resp.json()

  assert resp.status_code == 200, "Status should be 200"
  assert len(json_response.get("data")[
    "records"]) > 0, "Results should not be empty"
  retrieved_achievement_ids = [
    i.get("uuid") for i in json_response.get("data")["records"]]
  assert achievement.uuid in \
    retrieved_achievement_ids, "expected data not retrived"
  assert deleted_achievement.uuid not in \
    retrieved_achievement_ids, "unexpected data retrived"
  for i in json_response.get("data")["records"]:
    assert i["name"] == "ML Professional", "Filtered output is wrong"


def test_search_achievement(clean_firestore):
  achievement_dict = {**BASIC_ACHIEVEMENT_EXAMPLE}

  achievement = Achievement.from_dict(achievement_dict)
  achievement.uuid = ""
  achievement.save()
  achievement.uuid = achievement.id
  achievement.update()
  achievement_dict["uuid"] = achievement.id

  params = {"type": "course equate"}

  url = f"{api_url}/search"
  resp = client_with_emulator.get(url, params=params)
  assert resp.status_code == 200, "Status 200"


def test_archive_achievement(clean_firestore):
  achievement_dict = {**BASIC_ACHIEVEMENT_EXAMPLE}
  achievement = Achievement.from_dict(achievement_dict)
  achievement.uuid = ""
  achievement.is_archived = False  # achievement not archived initially
  achievement.save()
  achievement.uuid = achievement.id
  achievement.update()
  achievement_uuid = achievement.id

  url = f"{api_url}/{achievement_uuid}"
  updated_data = achievement_dict
  updated_data["is_archived"] = True
  resp = client_with_emulator.put(url, json=updated_data)
  json_response_update_req = resp.json()

  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get(
      "message"
  ) == "Successfully updated the achievement", "Expected response not same"
  assert json_response_update_req.get("data").get(
      "is_archived") is True, "Expected response not same"
