"""
  Tests for Domain endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
import os
import pytest
from copy import deepcopy
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.domain import router
from testing.test_config import API_URL
from schemas.schema_examples import (BASIC_DOMAIN_MODEL_EXAMPLE,
                                    BASIC_SUB_DOMAIN_MODEL_EXAMPLE)
from common.models import Domain, SubDomain
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/skill-service/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/domain"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

@pytest.fixture(name="add_data")
def add_data():
  sub_domain_dict = BASIC_SUB_DOMAIN_MODEL_EXAMPLE
  sub_domain = SubDomain.from_dict(sub_domain_dict)
  sub_domain.uuid = ""
  sub_domain.save()
  sub_domain.uuid = sub_domain.id
  sub_domain.update()

  return [sub_domain.uuid]

def test_post_and_get_domain(clean_firestore, add_data):
  sub_domain_uuid = add_data[0]

  domain_dict = deepcopy(BASIC_DOMAIN_MODEL_EXAMPLE)
  domain_dict["child_nodes"]["sub_domains"] = [sub_domain_uuid]

  url = api_url
  resp = client_with_emulator.post(url, json=domain_dict)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  assert json_response.get("success") is True, "Success not true"
  assert json_response.get(
      "message"
  ) == "Successfully created the domain", "Expected response not same"
  assert json_response.get("data").get("name") == domain_dict.get(
      "name"), "Expected response not same"

  domain_uuid = json_response["data"]["uuid"]

  child_sub_domain_doc = SubDomain.find_by_uuid(sub_domain_uuid)
  assert domain_uuid in child_sub_domain_doc.parent_nodes["domains"]

  url = f"{api_url}/{domain_uuid}"
  resp = client_with_emulator.get(url)
  json_response_get_req = resp.json()

  assert resp.status_code == 200, "Status coede not 200"
  assert json_response_get_req.get("data") == json_response.get(
      "data"), "Expected response not same"

  ## testing with fetch_tree=True
  resp = client_with_emulator.get(url, params={"fetch_tree": True})
  json_response_get_req = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  child_sub_domain = json_response_get_req["data"]["child_nodes"][
    "sub_domains"][0]
  assert child_sub_domain["uuid"] == sub_domain_uuid
  assert domain_uuid in child_sub_domain["parent_nodes"]["domains"]


def test_get_domain_negative(clean_firestore):
  domain_uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{domain_uuid}"
  response = {
      "success": False,
      "message": "Domain with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_delete_domain_positive(clean_firestore, add_data):
  sub_domain_uuid = add_data[0]

  domain_dict = deepcopy(BASIC_DOMAIN_MODEL_EXAMPLE)
  domain_dict["child_nodes"]["sub_domains"] = [sub_domain_uuid]

  url = api_url
  resp = client_with_emulator.post(url, json=domain_dict)
  json_response = resp.json()

  domain_uuid = json_response["data"]["uuid"]

  child_sub_domain_doc = SubDomain.find_by_uuid(sub_domain_uuid)
  assert domain_uuid in child_sub_domain_doc.parent_nodes["domains"]

  url = f"{api_url}/{domain_uuid}"
  resp = client_with_emulator.delete(url)
  json_response_delete_req = resp.json()

  expected_data = {
      "success": True,
      "message": "Successfully deleted the domain"
  }
  assert resp.status_code == 200, "Status coede not 200"
  assert json_response_delete_req == expected_data, "Expected response not same"

  child_sub_domain_doc = SubDomain.find_by_uuid(sub_domain_uuid)
  assert domain_uuid not in child_sub_domain_doc.parent_nodes["domains"]


def test_delete_domain_negative(clean_firestore):
  domain_uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{domain_uuid}"
  response = {
      "success": False,
      "message": "Domain with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_update_domain_positive(clean_firestore, add_data):
  sub_domain_id = add_data[0]
  domain_dict = deepcopy(BASIC_DOMAIN_MODEL_EXAMPLE)

  url = f"{api_url}"
  resp = client_with_emulator.post(url, json=domain_dict)
  json_response = resp.json()

  updated_data = json_response["data"]
  updated_data["name"] = "some random name"
  updated_data["child_nodes"] = {"sub_domains": [sub_domain_id]}

  uuid = updated_data.get("uuid")
  url = f"{api_url}/{uuid}"
  resp = client_with_emulator.put(url, json=updated_data)
  json_response_update_req = resp.json()

  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get(
      "message"
  ) == "Successfully updated the domain", "Expected response not same"
  assert json_response_update_req.get("data").get(
      "name") == "some random name", "Expected response not same"
  assert json_response_update_req.get("data").get(
      "child_nodes").get("sub_domains")[0] == sub_domain_id
  # Check if Domain is updated in parent nodes of sub-domain:
  sub_domain_obj = SubDomain.find_by_uuid(sub_domain_id)
  subdomain_parent_nodes = sub_domain_obj.parent_nodes
  assert subdomain_parent_nodes["domains"][0] == uuid


def test_update_domain_negative(clean_firestore):
  req_json = deepcopy(BASIC_DOMAIN_MODEL_EXAMPLE)
  uuid = req_json["uuid"] = "U2DDBkl3Ayg0PWudzhI"
  response = {
      "success": False,
      "message": "Domain with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }

  url = f"{api_url}/{uuid}"
  resp = client_with_emulator.put(url, json=req_json)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_import_domains(clean_firestore):
  url = f"{api_url}/import/json"
  file_path = os.path.join(
      os.path.dirname(__file__), "..", "testing", "domains.json")
  with open(file_path, "rb") as file:
    resp = client_with_emulator.post(url, files={"json_file": file})

  json_response = resp.json()

  assert resp.status_code == 200, "Success not 200"
  assert isinstance(json_response.get("data"), list), "Response is not a list"
  assert len(json_response.get("data")) > 0, "Empty list returned"


def test_get_domains(clean_firestore):
  domain_dict = deepcopy(BASIC_DOMAIN_MODEL_EXAMPLE)
  domain_dict["name"] = "Cognitive Knowledge"
  domain = Domain.from_dict(domain_dict)
  domain.uuid = ""
  domain.save()
  domain.uuid = domain.id
  domain.update()
  params = {"skip": 0, "limit": "50"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  saved_names = [i.get("name") for i in json_response.get("data")]
  assert domain_dict["name"] in saved_names, "all data not retrieved"

  # Checking domains with filter
  source_name = domain_dict["source_name"]
  url = f"{api_url}s?source_name={source_name}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  saved_source_names = [i.get("source_name") for i in json_response.get("data")]

  assert len(saved_source_names) > 0, \
    "Filtered results should contain the provided source name"

  for saved_source_name in saved_source_names:
    assert saved_source_name == source_name, "Filtered output is wrong"


def test_get_domains_negative(clean_firestore):
  domain_dict = deepcopy(BASIC_DOMAIN_MODEL_EXAMPLE)
  domain = Domain.from_dict(domain_dict)
  domain.uuid = ""
  domain.save()
  domain.uuid = domain.id
  domain.update()
  params = {"skip": "-1", "limit": "50"}

  url = f"{API_URL}/domains"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422, "Status not 422"
  assert json_response.get(
    "message"
  ) == "Invalid value passed to \"skip\" query parameter", \
    "unknown response received"
