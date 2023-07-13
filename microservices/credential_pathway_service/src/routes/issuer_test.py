"""
  Unit tests for issuer endpoints
"""
import os
import json
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.issuer import router
from testing.test_config import (API_URL, TESTING_FOLDER_PATH)
from schemas.schema_examples import BASIC_ISSUER_EXAMPLE
from common.models.credential_pathway_model import Issuer
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/credential-pathway-service/api/v1")

ISSUER_TESTDATA_FILENAME = os.path.join(TESTING_FOLDER_PATH, "issuer.json")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/issuer"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_get_issuer(clean_firestore):
  issuer_dict = BASIC_ISSUER_EXAMPLE
  issuer = Issuer.from_dict(issuer_dict)
  issuer.uuid = ""
  issuer.save()
  issuer.uuid = issuer.id
  issuer.update()
  issuer_dict["uuid"] = issuer.id

  url = f"{api_url}/{issuer.uuid}"
  resp = client_with_emulator.get(url)

  json_response = resp.json()
  del json_response["data"]["created_time"]
  del json_response["data"]["last_modified_time"]

  assert resp.status_code == 200, "Status should be 200"
  assert json_response.get("data") == issuer_dict, "Response received"


def test_get_issuer_negative(clean_firestore):
  uuid = "ASS345Dl3Ayg0PWudzhI"
  url = f"{api_url}/{uuid}"
  data = {
      "success": False,
      "message": f"Issuer with uuid {uuid} not found",
      "data": None
  }

  resp = client_with_emulator.get(url)
  json_response = json.loads(resp.text)
  assert resp.status_code == 404, "Status should be 404"
  assert json_response == data, "Response received"


def test_post_issuer(clean_firestore):
  input_issuer = BASIC_ISSUER_EXAMPLE
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_issuer)
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
  loaded_issuer = Issuer.find_by_uuid(uuid)
  loaded_issuer_dict = loaded_issuer.to_dict()

  # popping id and key for equivalency test
  loaded_issuer_dict.pop("id")
  loaded_issuer_dict.pop("key")
  loaded_issuer_dict.pop("created_by")
  loaded_issuer_dict.pop("created_time")
  loaded_issuer_dict.pop("last_modified_by")
  loaded_issuer_dict.pop("last_modified_time")


def test_update_issuer(clean_firestore):
  issuer_dict = BASIC_ISSUER_EXAMPLE
  issuer = Issuer.from_dict(issuer_dict)
  issuer.uuid = ""
  issuer.save()
  issuer.uuid = issuer.id
  issuer.update()
  issuer_uuid = issuer.id

  url = f"{api_url}/{issuer_uuid}"
  updated_data = {
      "name": "Jon",
      "email": "jon@example.com",
      "url": "https://www.example.com"
  }
  updated_data["description"] = "issuer added"
  resp = client_with_emulator.put(url, json=updated_data)
  json_response_update_req = resp.json()

  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get(
      "message"
  ) == "Successfully update the issuer", "Expected response not same"
  assert json_response_update_req.get("data").get(
      "description") == "issuer added", "Expected response not same"


def test_update_issuer_negative(clean_firestore):
  issuer_dict = {
      "name": "Jon",
      "email": "jon@example.com",
      "url": "https://www.example.com"
  }
  issuer_uuid = "ASS345Dl3Ayg0PWudzhI"
  url = f"{api_url}/{issuer_uuid}"
  response = {
      "success": False,
      "message": "Issuer with uuid ASS345Dl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.put(url, json=issuer_dict)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_delete_issuer(clean_firestore):
  issuer_dict = BASIC_ISSUER_EXAMPLE
  issuer = Issuer.from_dict(issuer_dict)
  issuer.uuid = ""
  issuer.save()
  issuer.uuid = issuer.id
  issuer.update()
  issuer_dict["uuid"] = issuer.id

  uuid = issuer.uuid
  issuer_dict["uuid"] = uuid

  url = f"{api_url}/{uuid}"
  resp = client_with_emulator.delete(url)
  del_json_response = resp.json()

  expected_data = {
      "success": True,
      "message": "Successfully deleted the issuer"
  }
  assert resp.status_code == 200, "Status code not 200"
  assert del_json_response == expected_data, "Expected response not same"


def test_delete_issuer_negative(clean_firestore):
  issuer_uuid = "ASS345Dl3Ayg0PWudzhI"
  url = f"{api_url}/{issuer_uuid}"
  response = {
      "success": False,
      "message": "Issuer with uuid ASS345Dl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"

  issuer_dict = BASIC_ISSUER_EXAMPLE
  issuer = Issuer.from_dict(issuer_dict)
  issuer.save()


def test_import_issuer(clean_firestore):
  url = f"{api_url}/import/json"
  with open(ISSUER_TESTDATA_FILENAME, encoding="UTF-8") as issuer_json_file:
    resp = client_with_emulator.post(url, files={"json_file": issuer_json_file})

  json_response = resp.json()
  assert resp.status_code == 200, "Status not 200"
  assert isinstance(json_response.get("data"), list), "Response is not a list"
  assert len(json_response.get("data")) > 0, "Empty list returned"
