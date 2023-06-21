"""
  Unit tests for Learner Profile endpoints
"""
import os
import json
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.session import router
from testing.test_config import API_URL
from schemas.schema_examples import (BASIC_USER_MODEL_EXAMPLE,
                                     BASIC_SESSION_EXAMPLE)
from common.models import Session, User, Achievement
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/user-management/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/session"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_get_session(clean_firestore):
  user_dict = BASIC_USER_MODEL_EXAMPLE
  user_dict["email"] = "jon_doe_tgs@gmail.com"
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  user_id = user.id

  session_dict = {**BASIC_SESSION_EXAMPLE}
  session_dict["user_id"] = user_id
  session = Session.from_dict(session_dict)
  session.session_id = ""
  session.save()
  session.session_id = session.id
  session.update()
  session_dict["session_id"] = session.id

  url = f"{api_url}/{session.id}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  print(json_response)

  assert resp.status_code == 200, "Status 200"
  del json_response["data"]["created_time"]
  del json_response["data"]["last_modified_time"]
  assert json_response.get("data") == session_dict, "Response received"


def test_get_session_negative(clean_firestore):
  user_dict = BASIC_USER_MODEL_EXAMPLE
  user_dict["email"] = "jon_doe_tgsn@gmail.com"
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  uuid = "U2DDBkl3Ayg0PWudzhI"

  url = f"{api_url}/{uuid}"
  print(url)
  expected_response = {
      "success": False,
      "message": f"Session with session_id {uuid} not found",
      "data": None
  }

  resp = client_with_emulator.get(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status not 404"
  assert json_response == expected_response, "Response received"


def test_get_all_sessions(clean_firestore):
  user_dict = BASIC_USER_MODEL_EXAMPLE
  user_dict["email"] = "jon_doe_tgas@gmail.com"
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  user_id = user.id

  session_dict = {**BASIC_SESSION_EXAMPLE}
  session_dict["user_id"] = user_id

  # parent session
  parent_session = Session.from_dict(session_dict)
  parent_session.session_id = ""
  parent_session.save()
  parent_session.session_id = parent_session.id
  parent_session.update()
  parent_session_id = parent_session.id

  # session for node_1
  session_node = Session.from_dict(session_dict)
  session_node.parent_session_id = parent_session_id
  session_node.session_data = {"node_id": "node_1"}
  session_node.session_id = ""
  session_node.save()
  session_node.session_id = session_node.id
  session_node.update()
  node_1_session_id = session_node.id

  # session for node_2
  session_node = Session.from_dict(session_dict)
  session_node.parent_session_id = parent_session_id
  session_node.session_data = {"node_id": "node_2"}
  session_node.session_id = ""
  session_node.save()
  session_node.session_id = session_node.id
  session_node.update()
  node_2_session_id = session_node.id

  params = {"user_id": user_id, "node_id": "node_1"}

  url = f"{api_url}"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  retrieved_ids = [i.get("session_id") for i in json_response.get("data")]

  assert len(retrieved_ids) > 0, \
    "At least one result should be there"
  assert node_1_session_id in \
    retrieved_ids, "expected data not retrieved"
  assert node_2_session_id not in \
    retrieved_ids, "expected data not retrieved"


def test_get_all_sessions_1(clean_firestore):
  user_dict = BASIC_USER_MODEL_EXAMPLE
  user_dict["email"] = "jon_doe_tgas1@gmail.com"
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  user_id = user.id

  session_dict = {**BASIC_SESSION_EXAMPLE}
  session_dict["user_id"] = user_id

  # parent session
  parent_session = Session.from_dict(session_dict)
  parent_session.session_id = ""
  parent_session.save()
  parent_session.session_id = parent_session.id
  parent_session.update()
  parent_session_id = parent_session.id

  # session for node_1
  session_node = Session.from_dict(session_dict)
  session_node.parent_session_id = parent_session_id
  session_node.session_data = {"node_id": "node_1"}
  session_node.session_id = ""
  session_node.save()
  session_node.session_id = session_node.id
  session_node.update()
  node_1_session_id = session_node.id

  # parent session 1
  parent_session = Session.from_dict(session_dict)
  parent_session.session_id = ""
  parent_session.save()
  parent_session.session_id = parent_session.id
  parent_session.update()
  parent_session_id_1 = parent_session.id

  # session for node_1
  session_node = Session.from_dict(session_dict)
  session_node.parent_session_id = parent_session_id_1
  session_node.session_data = {"node_id": "node_1"}
  session_node.session_id = ""
  session_node.save()
  session_node.session_id = session_node.id
  session_node.update()
  node_1_session_id_1 = session_node.id

  params = {"user_id": user_id, "node_id": "node_1",\
    "parent_session_id": parent_session_id_1}

  url = f"{api_url}"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  retrieved_ids = [i.get("session_id") for i in json_response.get("data")]

  assert len(retrieved_ids) > 0, \
    "At least one result should be there"
  assert node_1_session_id not in \
    retrieved_ids, "expected data not retrieved"
  assert node_1_session_id_1 in \
    retrieved_ids, "expected data not retrieved"


def test_get_latest_session(clean_firestore):
  user_dict = BASIC_USER_MODEL_EXAMPLE
  user_dict["email"] = "jon_doe_tgls@gmail.com"
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  user_id = user.id

  session_dict = {**BASIC_SESSION_EXAMPLE}
  session_dict["user_id"] = user_id

  # parent session
  parent_session = Session.from_dict(session_dict)
  parent_session.session_id = ""
  parent_session.save()
  parent_session.session_id = parent_session.id
  parent_session.update()
  parent_session_id = parent_session.id

  # session for node_1
  session_node = Session.from_dict(session_dict)
  session_node.parent_session_id = parent_session_id
  session_node.session_data = {"node_id": "node_1"}
  session_node.session_id = ""
  session_node.save()
  session_node.session_id = session_node.id
  session_node.update()
  node_1_session_id = session_node.id

  # session for node_2
  session_node = Session.from_dict(session_dict)
  session_node.parent_session_id = parent_session_id
  session_node.session_data = {"node_id": "node_2"}
  session_node.session_id = ""
  session_node.save()
  session_node.session_id = session_node.id
  session_node.update()

  params = {"user_id": user_id, "node_id": "node_1"}

  url = f"{api_url}/latest"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  assert json_response["data"] is not None, "expected data not retrieved"
  assert json_response["data"]["session_id"] == node_1_session_id, \
    "expected data not retrieved"


def test_get_latest_session_1(clean_firestore):
  user_dict = BASIC_USER_MODEL_EXAMPLE
  user_dict["email"] = "jon_doe_tgls1@gmail.com"
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  user_id = user.id

  session_dict = {**BASIC_SESSION_EXAMPLE}
  session_dict["user_id"] = user_id

  # parent session
  parent_session = Session.from_dict(session_dict)
  parent_session.session_id = ""
  parent_session.save()
  parent_session.session_id = parent_session.id
  parent_session.update()
  parent_session_id = parent_session.id

  # session for node_1
  session_node = Session.from_dict(session_dict)
  session_node.parent_session_id = parent_session_id
  session_node.session_data = {"node_id": "node_1"}
  session_node.session_id = ""
  session_node.save()
  session_node.session_id = session_node.id
  session_node.update()

  # parent session 1
  parent_session = Session.from_dict(session_dict)
  parent_session.session_id = ""
  parent_session.save()
  parent_session.session_id = parent_session.id
  parent_session.update()
  parent_session_id_1 = parent_session.id

  # session for node_1
  session_node = Session.from_dict(session_dict)
  session_node.parent_session_id = parent_session_id_1
  session_node.session_data = {"node_id": "node_1"}
  session_node.session_id = ""
  session_node.save()
  session_node.session_id = session_node.id
  session_node.update()
  node_1_session_id_1 = session_node.id

  params = {"user_id": user_id, "node_id": "node_1",\
    "parent_session_id": parent_session_id_1}

  url = f"{api_url}/latest"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  assert json_response["data"] is not None, "expected data not retrieved"
  assert json_response["data"]["session_id"] == node_1_session_id_1, \
    "expected data not retrieved"


def test_post_session(clean_firestore):
  user_dict = BASIC_USER_MODEL_EXAMPLE
  user_dict["email"] = "jon_doe_tps@gmail.com"
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  user_id = user.id

  session_dict = {**BASIC_SESSION_EXAMPLE}
  session_dict["user_id"] = user_id

  url = f"{api_url}"
  post_resp = client_with_emulator.post(url, json=session_dict)
  post_resp_json = post_resp.json()

  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  post_json_response = json.loads(post_resp.text)
  del post_json_response["data"]["created_time"]
  del post_json_response["data"]["last_modified_time"]
  session_id = post_json_response.get("data").get("session_id")

  # now see if GET endpoint returns same data
  url = f"{api_url}/{session_id}"
  get_resp = client_with_emulator.get(url)
  get_json_response = json.loads(get_resp.text)
  del get_json_response["data"]["created_time"]
  del get_json_response["data"]["last_modified_time"]
  assert get_json_response.get("data") == post_json_response.get("data")

  # now check and confirm it is properly in the database
  loaded_session = Session.find_by_uuid(session_id)
  loaded_session_dict = loaded_session.to_dict()

  # popping id and key for equivalency test
  loaded_session_dict.pop("id")
  loaded_session_dict.pop("key")
  loaded_session_dict.pop("created_by")
  loaded_session_dict.pop("created_time")
  loaded_session_dict.pop("last_modified_by")
  loaded_session_dict.pop("last_modified_time")
  loaded_session_dict.pop("archived_at_timestamp")
  loaded_session_dict.pop("archived_by")
  loaded_session_dict.pop("deleted_at_timestamp")
  loaded_session_dict.pop("deleted_by")

  # assert that rest of the fields are equivalent
  assert loaded_session_dict == post_json_response.get("data")


def test_update_session(clean_firestore):
  user_dict = BASIC_USER_MODEL_EXAMPLE
  user_dict["email"] = "jon_doe_tus@gmail.com"
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  user_id = user.id

  session_dict = {**BASIC_SESSION_EXAMPLE}
  session_dict["user_id"] = user_id
  session = Session.from_dict(session_dict)
  session.session_id = ""
  session.save()
  session.session_id = session.id
  session.update()
  session_id = session.id

  # pylint: disable-next = line-too-long
  url = f"{api_url}/{session_id}"
  learnosity_session = "U2DDBkl3Ayg0PWudzhI"
  updated_data = session_dict
  updated_data["session_data"] = {"learnosity_session_id": learnosity_session}
  del updated_data["user_id"]
  del updated_data["parent_session_id"]

  resp = client_with_emulator.put(url, json=updated_data)
  json_response_update_req = resp.json()

  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get(
      "message"
  ) == "Successfully updated the session", "Expected response not same"
  assert json_response_update_req.get("data").get("session_data").get(
      "learnosity_session_id") == learnosity_session, \
      "Expected response not same"


def test_update_session_negative(clean_firestore):
  user_dict = BASIC_USER_MODEL_EXAMPLE
  user_dict["email"] = "jon_doe_tusn@gmail.com"
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  user_id = user.id

  session_dict = {**BASIC_SESSION_EXAMPLE}
  session_dict["user_id"] = user_id
  session = Session.from_dict(session_dict)
  session.session_id = ""
  session.save()
  session.session_id = session.id
  session.update()
  session_uuid = "U2DDBkl3Ayg0PWudzhI"

  # pylint: disable-next = line-too-long
  url = f"{api_url}/{session_uuid}"
  response = {
      "success": False,
      "message": f"Session with session_id {session_uuid} not found",
      "data": None
  }

  del session_dict["user_id"]
  del session_dict["parent_session_id"]

  resp = client_with_emulator.put(url, json=session_dict)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"
