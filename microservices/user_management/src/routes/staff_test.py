"""
  Unit tests for Learner Profile endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
import os
from copy import deepcopy
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.staff import router
from testing.test_config import API_URL
from schemas.schema_examples import BASIC_STAFF_EXAMPLE
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/user-management/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/staff"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_post_and_get_staff(clean_firestore):
  staff_dict = deepcopy(BASIC_STAFF_EXAMPLE)

  resp = client_with_emulator.post(api_url, json=staff_dict)
  json_response = resp.json()
  staff_uuid = json_response["data"]["uuid"]

  assert resp.status_code == 200, "Status is not 200"
  assert json_response.get("success") is True, "Success not true"
  assert json_response.get("message") == \
         "Successfully created staff", "Expected response not same"
  assert json_response.get("data").get("first_name") == \
         staff_dict.get("first_name"), "Expected response not same"

  resp = client_with_emulator.get(f"{api_url}/{staff_uuid}")
  json_response_get_req = resp.json()

  assert resp.status_code == 200, "Status code not 200"
  assert json_response_get_req.get("data") == json_response.get(
    "data"), "Expected response not same"


def test_get_staff_negative(clean_firestore):
  invalid_staff_uuid = "random_id"
  url = f"{api_url}/{invalid_staff_uuid}"
  response = {
    "success": False,
    "message": "Staff with uuid random_id not found",
    "data": None
  }
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_delete_staff_positive(clean_firestore):
  staff_dict = deepcopy(BASIC_STAFF_EXAMPLE)

  resp = client_with_emulator.post(api_url, json=staff_dict)
  json_response = resp.json()
  staff_uuid = json_response["data"]["uuid"]

  resp = client_with_emulator.delete(f"{api_url}/{staff_uuid}")
  json_response_delete_req = resp.json()

  expected_data = {
    "success": True,
    "message": "Successfully deleted the staff"
  }
  assert resp.status_code == 200, "Status code not 200"
  assert json_response_delete_req == expected_data, "Expected response not same"

  resp_get = client_with_emulator.get(f"{api_url}/{staff_uuid}")
  resp_get_json = resp_get.json()

  assert resp_get_json["message"] == \
         f"Staff with uuid {staff_uuid} not found", "Staff not deleted"


def test_delete_staff_negative(clean_firestore):
  invalid_staff_uuid = "random_id"
  url = f"{api_url}/{invalid_staff_uuid}"
  response = {
    "success": False,
    "message": "Staff with uuid random_id not found",
    "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_update_staff_positive(clean_firestore):
  staff_dict = deepcopy(BASIC_STAFF_EXAMPLE)

  resp = client_with_emulator.post(api_url, json=staff_dict)
  json_response = resp.json()

  updated_data = {"bio": "updated_bio"}

  uuid = json_response["data"].get("uuid")
  resp = client_with_emulator.put(f"{api_url}/{uuid}", json=updated_data)
  json_response_update_req = resp.json()

  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get("message") == \
         "Successfully updated the staff", "Expected response not same"
  assert json_response_update_req.get("data").get("bio") == \
         "updated_bio", "Expected response not same"


def test_update_staff_negative(clean_firestore):
  req_json = {"email" : "dummy email"}
  uuid = "random_id"

  resp = client_with_emulator.put(f"{api_url}/{uuid}", json=req_json)
  json_response = resp.json()

  assert resp.status_code == 422, "Status 404"
  assert json_response["message"] == "Validation Failed",\
      "Expected message not same"


def test_import_staff(clean_firestore):
  url = f"{api_url}/import/json"
  file_path = os.path.join(
    os.getcwd(), "testing/", "staffs.json")
  with open(file_path, "rb") as file:
    resp = client_with_emulator.post(url, files={"json_file": file})

  json_response = resp.json()

  assert resp.status_code == 200, "Success not 200"
  assert isinstance(json_response.get("data"), list), "Response is not a list"
  assert len(json_response.get("data")) == 3, "returned length is not same"


def test_get_staffs_positive(clean_firestore):
  staff_dict = deepcopy(BASIC_STAFF_EXAMPLE)
  staff_dict["bio"] = "great staff"
  resp = client_with_emulator.post(api_url, json=staff_dict)
  params = {"skip": 0, "limit": "30"}

  resp = client_with_emulator.get(f"{api_url}s", params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  saved_bios = [i.get("bio") for i in json_response.get("data")]
  assert staff_dict["bio"] in saved_bios, "all data not retrieved"


def test_get_staffs_negative_param(clean_firestore):
  staff_dict = deepcopy(BASIC_STAFF_EXAMPLE)
  resp = client_with_emulator.post(api_url, json=staff_dict)
  params = {"skip": "-1", "limit": "50"}

  resp = client_with_emulator.get(f"{api_url}s", params=params)
  json_response = resp.json()
  assert resp.status_code == 422, "Status not 422"
  assert json_response["message"] == "Validation Failed"


def test_get_staffs_negative(clean_firestore):
  staff_dict = deepcopy(BASIC_STAFF_EXAMPLE)
  client_with_emulator.post(api_url, json=staff_dict)
  params = {"skip": "1", "limit": "105"}

  resp = client_with_emulator.get(f"{api_url}s", params=params)
  json_response = resp.json()
  assert resp.status_code == 422, "Status not 422"
  assert json_response["message"] == "Validation Failed"


def test_search_staff_positive(clean_firestore):
  staff_dict = deepcopy(BASIC_STAFF_EXAMPLE)
  client_with_emulator.post(api_url, json=staff_dict)

  params = {"email": "ted.turner@email.com"}
  resp = client_with_emulator.get(f"{api_url}/search", params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status not 200"
  assert json_response.get("data")[0]["email"] == staff_dict["email"]


def test_search_staff_negative_1(clean_firestore):
  staff_dict = deepcopy(BASIC_STAFF_EXAMPLE)
  client_with_emulator.post(api_url, json=staff_dict)

  params = {"email": "ted.turner"}
  resp = client_with_emulator.get(f"{api_url}/search", params=params)
  json_response = resp.json()
  assert resp.status_code == 422
  assert json_response.get("success") is False
  assert json_response.get("data") is None


def test_get_profile_fields():
  resp = client_with_emulator.get(f"{api_url}/profile/fields")
  assert resp.status_code == 200, "Status 200"
