"""
  Tests for Verb endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
import os
import json
import pytest
from copy import deepcopy
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.verb import router
from testing.test_config import API_URL, TESTING_FOLDER_PATH
from schemas.schema_examples import BASIC_VERB_MODEL_EXAMPLE
from common.models import Verb
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/learning-record-service/api/v1")

client_with_emulator = TestClient(app)

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_post_and_get_verb(clean_firestore):
  verb_dict = deepcopy(BASIC_VERB_MODEL_EXAMPLE)

  url = f"{API_URL}/verb"
  resp = client_with_emulator.post(url, json=verb_dict)
  json_response = resp.json()
  verb_uuid = json_response["data"]["uuid"]

  assert resp.status_code == 200, "Status is not 200"
  assert json_response.get("success") is True, "Success not true"
  assert json_response.get(
      "message"
  ) == "Successfully created the verb", "Expected response not same"
  assert json_response.get("data").get("name") == verb_dict.get(
      "name"), "Expected response not same"

  url = f"{API_URL}/verb/{verb_uuid}"
  resp = client_with_emulator.get(url)
  json_response_get_req = resp.json()

  assert resp.status_code == 200, "Status code not 200"
  assert json_response_get_req.get("data") == json_response.get(
      "data"), "Expected response not same"


def test_get_verb_negative(clean_firestore):
  invalid_verb_uuid = "random_id"
  url = f"{API_URL}/verb/{invalid_verb_uuid}"
  response = {
      "success": False,
      "message": "Verb with uuid random_id not found",
      "data": None
  }
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_delete_verb_positive(clean_firestore):
  verb_dict = deepcopy(BASIC_VERB_MODEL_EXAMPLE)

  url = f"{API_URL}/verb"
  resp = client_with_emulator.post(url, json=verb_dict)
  json_response = resp.json()
  verb_uuid = json_response["data"]["uuid"]

  url = f"{API_URL}/verb/{verb_uuid}"
  resp = client_with_emulator.delete(url)
  json_response_delete_req = resp.json()

  expected_data = {"success": True, "message": "Successfully deleted the verb"}
  assert resp.status_code == 200, "Status code not 200"
  assert json_response_delete_req == expected_data, "Expected response not same"


def test_delete_verb_negative(clean_firestore):
  invalid_verb_uuid = "random_id"
  url = f"{API_URL}/verb/{invalid_verb_uuid}"
  response = {
      "success": False,
      "message": "Verb with uuid random_id not found",
      "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_update_verb_positive(clean_firestore):
  verb_dict = deepcopy(BASIC_VERB_MODEL_EXAMPLE)
  url = f"{API_URL}/verb"

  resp = client_with_emulator.post(url, json=verb_dict)
  json_response = resp.json()

  updated_data = json_response["data"]
  updated_data["name"] = "some random name"

  uuid = updated_data.get("uuid")
  url = f"{API_URL}/verb/{uuid}"
  resp = client_with_emulator.put(url, json=updated_data)
  json_response_update_req = resp.json()

  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get(
      "message"
  ) == "Successfully updated the verb", "Expected response not same"
  assert json_response_update_req.get("data").get(
      "name") == "some random name", "Expected response not same"


def test_update_verb_negative(clean_firestore):
  req_json = deepcopy(BASIC_VERB_MODEL_EXAMPLE)
  uuid = req_json["uuid"] = "random_id"
  response = {
      "success": False,
      "message": "Verb with uuid random_id not found",
      "data": None
  }

  url = f"{API_URL}/verb/{uuid}"
  resp = client_with_emulator.put(url, json=req_json)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_import_verbs(clean_firestore):
  url = f"{API_URL}/verb/import/json"
  file_path = os.path.join(TESTING_FOLDER_PATH, "verbs.json")
  with open(file_path, "rb") as file:
    resp = client_with_emulator.post(url, files={"json_file": file})

  json_response = resp.json()

  assert resp.status_code == 200, "Success not 200"
  assert isinstance(json_response.get("data"), list), "Response is not a list"
  assert len(json_response.get("data")) > 0, "Empty list returned"


def test_get_verbs(clean_firestore):
  verb_dict = deepcopy(BASIC_VERB_MODEL_EXAMPLE)
  verb_dict["name"] = "Communicate"
  verb = Verb.from_dict(verb_dict)
  verb.uuid = ""
  verb.save()
  verb.uuid = verb.id
  verb.update()
  params = {"skip": 0, "limit": "30"}

  url = f"{API_URL}/verbs"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  saved_names = [i.get("name") for i in json_response.get("data")]
  assert verb_dict["name"] in saved_names, "all data not retrieved"


def test_get_verbs_negative(clean_firestore):
  verb_dict = deepcopy(BASIC_VERB_MODEL_EXAMPLE)
  verb = Verb.from_dict(verb_dict)
  verb.uuid = ""
  verb.save()
  verb.uuid = verb.id
  verb.update()
  params = {"skip": "-1", "limit": "30"}

  url = f"{API_URL}/verbs"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422, "Status not 422"
  assert json_response.get(
    "message"
  ) == "Validation Failed", \
    "unknown response received"
