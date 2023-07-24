"""
  Unit Tests for Approved Experience endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
import os
import pytest
from copy import deepcopy
from fastapi import FastAPI
from fastapi.testclient import TestClient
from testing.test_config import API_URL, TESTING_FOLDER_PATH
from routes.approved_experience import router
from schemas.schema_examples import BASIC_APPROVED_EXPERIENCE_MODEL_EXAMPLE
from common.models import ApprovedExperience
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/prior-learning-assessment/api/v1")

client_with_emulator = TestClient(app)

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_post_and_get_approved_experience(clean_firestore):
  approved_experience_dict = deepcopy(BASIC_APPROVED_EXPERIENCE_MODEL_EXAMPLE)
  url = f"{API_URL}/approved-experience"
  resp = client_with_emulator.post(url, json=approved_experience_dict)
  json_response = resp.json()
  print(json_response)
  approved_experience_uuid = json_response["data"]["uuid"]

  assert resp.status_code == 200, "Status is not 200"
  assert json_response.get("success") is True, "Success not true"
  assert json_response.get("message") == \
    "Successfully created the approved experience", "Expected response not same"
  assert json_response.get("data").get("organization") == \
    approved_experience_dict.get("organization"), "Expected response not same"

  url = f"{API_URL}/approved-experience/{approved_experience_uuid}"
  resp = client_with_emulator.get(url)
  json_response_get_req = resp.json()

  assert resp.status_code == 200, "Status code not 200"
  assert json_response_get_req.get("data") == json_response.get(
      "data"), "Expected response not same"


def test_get_approved_experience_negative(clean_firestore):
  invalid_approved_experience_uuid = "random_id"
  url = f"{API_URL}/approved-experience/{invalid_approved_experience_uuid}"
  response = {
      "success": False,
      "message": "Approved Experience with uuid random_id not found",
      "data": None
  }
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_delete_approved_experience_positive(clean_firestore):
  approved_experience_dict = deepcopy(BASIC_APPROVED_EXPERIENCE_MODEL_EXAMPLE)

  url = f"{API_URL}/approved-experience"
  resp = client_with_emulator.post(url, json=approved_experience_dict)
  json_response = resp.json()
  approved_experience_uuid = json_response["data"]["uuid"]

  url = f"{API_URL}/approved-experience/{approved_experience_uuid}"
  resp = client_with_emulator.delete(url)
  json_response_delete_req = resp.json()

  expected_data = {
      "success": True,
      "message": "Successfully deleted the approved experience"
  }
  assert resp.status_code == 200, "Status code not 200"
  assert json_response_delete_req == expected_data, "Expected response not same"

  resp_get = client_with_emulator.get(url)
  resp_get_json = resp_get.json()

  assert resp_get_json["message"] == \
    f"Approved Experience with uuid {approved_experience_uuid} not found",\
    "Approved Experience not deleted"


def test_delete_approved_experience_negative(clean_firestore):
  invalid_approved_experience_uuid = "random_id"
  url = f"{API_URL}/approved-experience/{invalid_approved_experience_uuid}"
  response = {
      "success": False,
      "message": "Approved Experience with uuid random_id not found",
      "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_update_approved_experience_positive(clean_firestore):
  approved_experience_dict = deepcopy(BASIC_APPROVED_EXPERIENCE_MODEL_EXAMPLE)
  url = f"{API_URL}/approved-experience"

  resp = client_with_emulator.post(url, json=approved_experience_dict)
  json_response = resp.json()

  updated_data = json_response["data"]
  updated_data["organization"] = "updated_organization"

  uuid = updated_data.get("uuid")
  url = f"{API_URL}/approved-experience/{uuid}"
  resp = client_with_emulator.put(url, json=updated_data)
  json_response_update_req = resp.json()

  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get("message") == \
    "Successfully updated the approved experience", "Expected response not same"
  assert json_response_update_req.get("data").get("organization") == \
    "updated_organization", "Expected response not same"


def test_update_approved_experience_negative(clean_firestore):
  req_json = deepcopy(BASIC_APPROVED_EXPERIENCE_MODEL_EXAMPLE)
  uuid = req_json["uuid"] = "random_id"
  response = {
      "success": False,
      "message": "Approved Experience with uuid random_id not found",
      "data": None
  }

  url = f"{API_URL}/approved-experience/{uuid}"
  resp = client_with_emulator.put(url, json=req_json)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_import_approved_experience(clean_firestore):
  url = f"{API_URL}/approved-experience/import/json"
  file_path = os.path.join(TESTING_FOLDER_PATH, "approved_experiences.json")
  with open(file_path, "rb") as file:
    resp = client_with_emulator.post(url, files={"json_file": file})

  json_response = resp.json()

  assert resp.status_code == 200, "Success not 200"
  assert isinstance(json_response.get("data"), list), "Response is not a list"
  assert len(json_response.get("data")) == 4, "returned length is not same"


def test_get_approved_experiences(clean_firestore):
  approved_experience_dict = deepcopy(BASIC_APPROVED_EXPERIENCE_MODEL_EXAMPLE)
  approved_experience_dict["organization"] = "new_organization"
  url = f"{API_URL}/approved-experience"
  resp = client_with_emulator.post(url, json=approved_experience_dict)
  params = {"skip": 0, "limit": "10"}

  url = f"{API_URL}/approved-experiences"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  saved_orgs = [i.get("organization") for i in json_response.get(
    "data")["records"]]
  assert approved_experience_dict["organization"] in saved_orgs,\
    "all data not retrieved"


def test_get_approved_experiences_negative(clean_firestore):
  approved_experience_dict = deepcopy(BASIC_APPROVED_EXPERIENCE_MODEL_EXAMPLE)
  url = f"{API_URL}/approved-experience"
  resp = client_with_emulator.post(url, json=approved_experience_dict)
  params = {"skip": "-1", "limit": "50"}

  url = f"{API_URL}/approved-experiences"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422, "Status not 422"
  assert json_response.get("message") == "Validation Failed"

def test_import_and_get_organisation(clean_firestore):
  url = f"{API_URL}/approved-experience/import/json"
  file_path = os.path.join(TESTING_FOLDER_PATH, "approved_experiences.json")
  with open(file_path, "rb") as file:
    resp = client_with_emulator.post(url, files={"json_file": file})

  json_response = resp.json()

  assert resp.status_code == 200, "Success not 200"
  assert isinstance(json_response.get("data"), list), "Response is not a list"
  assert len(json_response.get("data")) == 4, "returned length is not same"

  url = f"{API_URL}/approved-experiences"
  resp = client_with_emulator.get(url)
  json_response_get_experiences = resp.json()

  #Fetch the unique organisations from the imported data
  orgs = []
  for approved_experience in json_response_get_experiences.get(
    "data")["records"]:
    orgs.append(approved_experience["organization"])
  orgs = sorted(list(set(orgs)))

  url = f"{API_URL}/approved-experience/organisations/unique"
  resp = client_with_emulator.get(url)
  json_response_get_req_orgs = resp.json()

  assert resp.status_code == 200, "Status code not 200"
  assert sorted(json_response_get_req_orgs.get("data")) == orgs,\
    "Expected response not same"

def test_get_keywordsearch(clean_firestore):
  prior_experience_dict = deepcopy(BASIC_APPROVED_EXPERIENCE_MODEL_EXAMPLE)
  url = f"{API_URL}/approved-experience"
  resp = client_with_emulator.post(url, json=prior_experience_dict)
  params = {"keyword": "Fundamentals of Accounting"}
  search_url = f"{API_URL}/approved-experience/search"
  resp = client_with_emulator.get(search_url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert params["keyword"] == json_response[
    "data"]["records"][0]["title"]
  assert json_response.get("message") == \
    "Successfully fetched the Approved Experiences"
