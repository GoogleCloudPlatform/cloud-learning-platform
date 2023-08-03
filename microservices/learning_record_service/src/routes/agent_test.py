"""
  Unit Tests for Agent endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
import os
import pytest
from copy import deepcopy
from fastapi import FastAPI
from fastapi.testclient import TestClient
from testing.test_config import API_URL, TESTING_FOLDER_PATH
from routes.agent import router
from schemas.schema_examples import BASIC_AGENT_SCHEMA_EXAMPLE, TEST_USER
from common.models import Agent, User
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/learning-record-service/api/v1")

client_with_emulator = TestClient(app)

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_search_agent(clean_firestore):
  agent_dict = deepcopy(BASIC_AGENT_SCHEMA_EXAMPLE)
  agent = Agent.from_dict(agent_dict)
  agent.uuid = ""
  agent.save()
  agent.uuid = agent.id
  agent.update()
  agent_dict["uuid"] = agent.id

  agent_dict = deepcopy(BASIC_AGENT_SCHEMA_EXAMPLE)
  params = {"name": "example agent"}

  url = f"{API_URL}/agent/search"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert json_response.get("data")[0].get(
      "name") == BASIC_AGENT_SCHEMA_EXAMPLE.get("name"), "Response received"


def test_post_and_get_agent(clean_firestore):
  test_user = User()
  data = TEST_USER
  test_user = test_user.from_dict(data)
  test_user.save()

  agent_dict = deepcopy(BASIC_AGENT_SCHEMA_EXAMPLE)

  url = f"{API_URL}/agent"
  resp = client_with_emulator.post(url, json=agent_dict)
  json_response = resp.json()
  agent_uuid = json_response["data"]["uuid"]

  assert resp.status_code == 200, "Status is not 200"
  assert json_response.get("success") is True, "Success not true"
  assert json_response.get("message") == \
    "Successfully created the agent", "Expected response not same"
  assert json_response.get("data").get("user_id") == agent_dict.get(
      "user_id"), "Expected response not same"

  url = f"{API_URL}/agent/{agent_uuid}"
  resp = client_with_emulator.get(url)
  json_response_get_req = resp.json()

  assert resp.status_code == 200, "Status code not 200"
  assert json_response_get_req.get("data") == json_response.get(
      "data"), "Expected response not same"


def test_get_agent_negative(clean_firestore):
  invalid_agent_uuid = "random_id"
  url = f"{API_URL}/agent/{invalid_agent_uuid}"
  response = {
      "success": False,
      "message": "Agent with uuid random_id not found",
      "data": None
  }
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_delete_agent_positive(clean_firestore):
  test_user = User()
  data = TEST_USER
  test_user = test_user.from_dict(data)
  test_user.save()
  agent_dict = deepcopy(BASIC_AGENT_SCHEMA_EXAMPLE)

  url = f"{API_URL}/agent"
  resp = client_with_emulator.post(url, json=agent_dict)
  json_response = resp.json()
  agent_uuid = json_response["data"]["uuid"]

  url = f"{API_URL}/agent/{agent_uuid}"
  resp = client_with_emulator.delete(url)
  json_response_delete_req = resp.json()

  expected_data = {"success": True, "message": "Successfully deleted the agent"}
  assert resp.status_code == 200, "Status code not 200"
  assert json_response_delete_req == expected_data, "Expected response not same"


def test_delete_agent_negative(clean_firestore):
  invalid_agent_uuid = "random_id"
  url = f"{API_URL}/agent/{invalid_agent_uuid}"
  response = {
      "success": False,
      "message": "Agent with uuid random_id not found",
      "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_update_agent_positive(clean_firestore):
  test_user = User()
  data = TEST_USER
  test_user = test_user.from_dict(data)
  test_user.save()

  agent_dict = deepcopy(BASIC_AGENT_SCHEMA_EXAMPLE)
  url = f"{API_URL}/agent"

  resp = client_with_emulator.post(url, json=agent_dict)
  json_response = resp.json()
  updated_data = json_response["data"]
  updated_data["user_id"] = "updated_user_id"
  del updated_data["created_time"]
  del updated_data["last_modified_time"]

  #uuid = updated_data.get("uuid")
  uuid = updated_data["uuid"]
  del updated_data["uuid"]
  del updated_data["is_deleted"]
  url = f"{API_URL}/agent/{uuid}"
  resp = client_with_emulator.put(url, json=updated_data)
  json_response_update_req = resp.json()

  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get("message") == \
    "Successfully updated the agent", "Expected response not same"
  assert json_response_update_req.get("data").get("user_id") == \
    "updated_user_id", "Expected response not same"


def test_update_agent_negative(clean_firestore):
  req_json = deepcopy(BASIC_AGENT_SCHEMA_EXAMPLE)

  uuid = "random_id"
  response = {
      "success": False,
      "message": "Agent with uuid random_id not found",
      "data": None
  }

  url = f"{API_URL}/agent/{uuid}"
  resp = client_with_emulator.put(url, json=req_json)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_import_agent(clean_firestore):
  url = f"{API_URL}/agent/import/json"
  file_path = os.path.join(TESTING_FOLDER_PATH, "agent.json")
  with open(file_path, "rb") as file:
    resp = client_with_emulator.post(url, files={"json_file": file})

  json_response = resp.json()

  assert resp.status_code == 200, "Success not 200"
  assert isinstance(json_response.get("data"), list), "Response is not a list"
  assert len(json_response.get("data")) == 3, "returned length is not same"


def test_get_agents(clean_firestore):
  agent_dict = deepcopy(BASIC_AGENT_SCHEMA_EXAMPLE)
  agent_dict["user_id"] = "user_id_new"
  agent = Agent.from_dict(agent_dict)
  agent.uuid = ""
  agent.save()
  agent.uuid = agent.id
  agent.update()
  params = {"skip": 0, "limit": "30"}

  url = f"{API_URL}/agents"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  saved_user_ids = [i.get("user_id") for i in json_response.get(
    "data")["records"]]
  assert agent_dict["user_id"] in saved_user_ids,\
    "all data not retrieved"


def test_get_agents_negative(clean_firestore):
  agent_dict = deepcopy(BASIC_AGENT_SCHEMA_EXAMPLE)
  agent_dict["user_id"] = "user_id_new"
  agent = Agent.from_dict(agent_dict)
  agent.uuid = ""
  agent.save()
  agent.uuid = agent.id
  agent.update()
  params = {"skip": "-1", "limit": "30"}

  url = f"{API_URL}/agents"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422, "Status not 422"
  assert json_response.get("message") == \
    "Validation Failed", \
    "unknown response received"

def test_get_agent_for_user(clean_firestore):
  agent_dict = deepcopy(BASIC_AGENT_SCHEMA_EXAMPLE)
  agent_dict["user_id"] = "user_id_new"
  agent = Agent.from_dict(agent_dict)
  agent.uuid = ""
  agent.save()
  agent.uuid = agent.id
  agent.update()
  params = {"user_id": "user_id_new"}

  url = f"{API_URL}/agents"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  saved_user_ids = [i.get("user_id") for i in json_response.get(
    "data")["records"]]
  assert agent_dict["user_id"] in saved_user_ids,\
    "all data not retrieved"
