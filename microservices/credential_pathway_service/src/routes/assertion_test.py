"""
  Unit tests for assertion endpoints
"""
import os
import json
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.assertion import router
from testing.test_config import (API_URL, TESTING_FOLDER_PATH)
from schemas.schema_examples import BASIC_ASSERTION_EXAMPLE
from common.models.credential_pathway_model import Assertion
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/credential-pathway-service/api/v1")

ASSERTION_TESTDATA_FILENAME = os.path.join(TESTING_FOLDER_PATH,
                                           "assertion.json")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/assertion"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_get_assertion(clean_firestore):
  assertion_dict = BASIC_ASSERTION_EXAMPLE
  assertion = Assertion.from_dict(assertion_dict)
  assertion.uuid = ""
  assertion.save()
  assertion.uuid = assertion.id
  assertion.update()
  assertion_dict["uuid"] = assertion.id

  url = f"{api_url}/{assertion.uuid}"
  resp = client_with_emulator.get(url)

  json_response = resp.json()
  del json_response["data"]["created_time"]
  del json_response["data"]["last_modified_time"]
  del json_response["data"]["revoked"]
  del json_response["data"]["expires"]
  del assertion_dict["expires"]
  assert resp.status_code == 200, "Status should be 200"
  assert json_response.get("data") == assertion_dict, "Response received"


def test_get_assertion_negative(clean_firestore):
  uuid = "ASS345Dl3Ayg0PWudzhI"
  url = f"{api_url}/{uuid}"
  data = {
      "success": False,
      "message": f"Assertion with uuid {uuid} not found",
      "data": None
  }

  resp = client_with_emulator.get(url)
  json_response = json.loads(resp.text)
  assert resp.status_code == 404, "Status should be 404"
  assert json_response == data, "Response received"


def test_post_assertion(clean_firestore):
  input_assertion = BASIC_ASSERTION_EXAMPLE
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_assertion)
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

  # now check and confirm it is properly in the databse
  loaded_assertion = Assertion.find_by_uuid(uuid)
  loaded_assertion_dict = loaded_assertion.to_dict()
  # popping id and key for equivalency test
  loaded_assertion_dict.pop("id")
  loaded_assertion_dict.pop("key")
  loaded_assertion_dict.pop("created_time")
  loaded_assertion_dict.pop("last_modified_by")
  loaded_assertion_dict.pop("last_modified_time")
  loaded_assertion_dict.pop("expires")
  del post_json_response["data"]["expires"]


def test_update_assertion(clean_firestore):
  assertion_dict = BASIC_ASSERTION_EXAMPLE
  assertion = Assertion.from_dict(assertion_dict)
  assertion.uuid = ""
  assertion.save()
  assertion.uuid = assertion.id
  assertion.update()
  assertion_uuid = assertion.id

  url = f"{api_url}/{assertion_uuid}"
  updated_data = {
      "entity_type": "assertion",
      "entity_id": "986",
      "open_badge_id": "31",
  }
  updated_data["issuer"] = "Jon"
  resp = client_with_emulator.put(url, json=updated_data)
  json_response_update_req = resp.json()

  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get(
      "message"
  ) == "Successfully update the assertion", "Expected response not same"
  assert json_response_update_req.get("data").get(
      "issuer") == "Jon", "Expected response not same"


def test_update_assertion_negative(clean_firestore):
  assertion_dict = {
      "entity_type": "assertion",
      "entity_id": "986",
      "open_badge_id": "31",
  }
  assertion_uuid = "ASS345Dl3Ayg0PWudzhI"
  url = f"{api_url}/{assertion_uuid}"
  response = {
      "success": False,
      "message": "Assertion with uuid ASS345Dl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.put(url, json=assertion_dict)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_delete_assertion(clean_firestore):
  assertion_dict = BASIC_ASSERTION_EXAMPLE
  assertion = Assertion.from_dict(assertion_dict)
  assertion.uuid = ""
  assertion.save()
  assertion.uuid = assertion.id
  assertion.update()
  assertion_dict["uuid"] = assertion.id

  uuid = assertion.uuid
  assertion_dict["uuid"] = uuid

  url = f"{api_url}/{uuid}"
  resp = client_with_emulator.delete(url)
  del_json_response = resp.json()

  expected_data = {
      "success": True,
      "message": "Successfully deleted the assertion"
  }
  assert resp.status_code == 200, "Status code not 200"
  assert del_json_response == expected_data, "Expected response not same"


def test_delete_assertion_negative(clean_firestore):
  assertion_uuid = "ASS345Dl3Ayg0PWudzhI"
  url = f"{api_url}/{assertion_uuid}"
  response = {
      "success": False,
      "message": "Assertion with uuid ASS345Dl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"

  assertion_dict = BASIC_ASSERTION_EXAMPLE
  assertion = Assertion.from_dict(assertion_dict)
  assertion.save()


def test_import_assertion(clean_firestore):
  url = f"{api_url}/import/json"
  with open(
      ASSERTION_TESTDATA_FILENAME, encoding="UTF-8") as assertion_json_file:
    resp = client_with_emulator.post(
        url, files={"json_file": assertion_json_file})

  json_response = resp.json()
  assert resp.status_code == 200, "Status not 200"
  assert isinstance(json_response.get("data"), list), "Response is not a list"
  assert len(json_response.get("data")) > 0, "Empty list returned"
