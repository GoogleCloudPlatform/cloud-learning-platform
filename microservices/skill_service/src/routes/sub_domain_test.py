"""
  Tests for Sub Domain endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
import os
import pytest
from copy import deepcopy
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.sub_domain import router
from testing.test_config import API_URL
from schemas.schema_examples import (BASIC_SUB_DOMAIN_MODEL_EXAMPLE,
                                    BASIC_CATEGORY_MODEL_EXAMPLE,
                                    BASIC_COMPETENCY_MODEL_EXAMPLE,
                                    BASIC_DOMAIN_MODEL_EXAMPLE)
from common.models.skill import (SubDomain, Category, SkillServiceCompetency,
                                Domain)
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/skill-service/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/sub-domain"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


@pytest.fixture(name="add_data")
def add_data():
  domain_dict = BASIC_DOMAIN_MODEL_EXAMPLE
  domain = Domain.from_dict(domain_dict)
  domain.uuid = ""
  domain.save()
  domain.uuid = domain.id
  domain.update()

  category_dict = BASIC_CATEGORY_MODEL_EXAMPLE
  category = Category.from_dict(category_dict)
  category.uuid = ""
  category.save()
  category.uuid = category.id
  category.update()

  competency_dict = BASIC_COMPETENCY_MODEL_EXAMPLE
  competency = SkillServiceCompetency.from_dict(competency_dict)
  competency.uuid = ""
  competency.save()
  competency.uuid = competency.id
  competency.update()

  return [domain.uuid, category.uuid, competency.uuid]


def test_post_and_get_sub_domain(clean_firestore, add_data):
  domain_uuid, category_uuid, competency_uuid = add_data

  sub_domain_dict = deepcopy(BASIC_SUB_DOMAIN_MODEL_EXAMPLE)
  sub_domain_dict["uuid"] = ""
  sub_domain_dict["parent_nodes"]["domains"] = [domain_uuid]
  sub_domain_dict["child_nodes"]= {"categories": [category_uuid],
                                  "competencies": [competency_uuid]}

  url = api_url
  resp = client_with_emulator.post(url, json=sub_domain_dict)
  json_response = resp.json()
  sub_domain_uuid = json_response["data"]["uuid"]

  assert resp.status_code == 200, "Status 200"
  assert json_response.get("success") is True, "Success not true"
  assert json_response.get(
      "message"
  ) == "Successfully created the sub_domain", "Expected response not same"
  assert json_response.get("data").get("name") == sub_domain_dict.get(
      "name"), "Expected response not same"
  parent_domain_doc = Domain.find_by_uuid(domain_uuid)
  child_competency_doc = SkillServiceCompetency.find_by_uuid(competency_uuid)
  child_category_doc = Category.find_by_uuid(category_uuid)
  assert sub_domain_uuid in parent_domain_doc.child_nodes["sub_domains"]
  assert sub_domain_uuid in child_competency_doc.parent_nodes["sub_domains"]
  assert sub_domain_uuid in child_category_doc.parent_nodes["sub_domains"]

  url = f"{api_url}/{sub_domain_uuid}"
  resp = client_with_emulator.get(url)
  json_response_get_req = resp.json()

  assert resp.status_code == 200, "Status code not 200"
  assert json_response_get_req.get("data") == json_response.get(
      "data"), "Expected response not same"

  ## testing with fetch_tree=True
  get_resp = client_with_emulator.get(url, params={"fetch_tree": True})
  json_response_get_req = get_resp.json()

  assert get_resp.status_code == 200, "Status code not 200"
  child_category = json_response_get_req["data"]["child_nodes"]["categories"][0]
  child_competency = json_response_get_req["data"]["child_nodes"][
    "competencies"][0]
  parent_domain = json_response_get_req["data"]["parent_nodes"]["domains"][0]
  assert child_category["uuid"] == category_uuid
  assert sub_domain_uuid in child_category["parent_nodes"]["sub_domains"]

  assert child_competency["uuid"] == competency_uuid
  assert sub_domain_uuid in child_competency["parent_nodes"]["sub_domains"]

  assert parent_domain["uuid"] == domain_uuid
  assert sub_domain_uuid in parent_domain["child_nodes"]["sub_domains"]


def test_get_sub_domain_negative(clean_firestore):
  sub_domain_uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{sub_domain_uuid}"
  response = {
      "success": False,
      "message": "Sub Domain with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_delete_sub_domain_positive(clean_firestore, add_data):
  domain_uuid = add_data[0]
  category_uuid = add_data[1]
  competency_uuid = add_data[2]

  sub_domain_dict = deepcopy(BASIC_SUB_DOMAIN_MODEL_EXAMPLE)
  sub_domain_dict["parent_nodes"]["domains"] = [domain_uuid]
  sub_domain_dict["child_nodes"]["categories"] = [category_uuid]
  sub_domain_dict["child_nodes"]["competencies"] = [competency_uuid]

  url = api_url
  resp = client_with_emulator.post(url, json=sub_domain_dict)
  json_response = resp.json()
  sub_domain_uuid = json_response["data"]["uuid"]
  parent_domain_doc = Domain.find_by_uuid(domain_uuid)
  child_competency_doc = SkillServiceCompetency.find_by_uuid(competency_uuid)
  child_category_doc = Category.find_by_uuid(category_uuid)
  assert sub_domain_uuid in parent_domain_doc.child_nodes["sub_domains"]
  assert sub_domain_uuid in child_competency_doc.parent_nodes["sub_domains"]
  assert sub_domain_uuid in child_category_doc.parent_nodes["sub_domains"]

  url = f"{api_url}/{sub_domain_uuid}"
  resp = client_with_emulator.delete(url)
  json_response_delete_req = resp.json()

  expected_data = {
      "success": True,
      "message": "Successfully deleted the sub_domain"
  }
  assert resp.status_code == 200, "Status code not 200"
  assert json_response_delete_req == expected_data, "Expected response not same"
  parent_domain_doc = Domain.find_by_uuid(domain_uuid)
  child_competency_doc = SkillServiceCompetency.find_by_uuid(competency_uuid)
  child_category_doc = Category.find_by_uuid(category_uuid)
  assert sub_domain_uuid not in parent_domain_doc.child_nodes["sub_domains"]
  assert sub_domain_uuid not in child_competency_doc.parent_nodes["sub_domains"]
  assert sub_domain_uuid not in child_category_doc.parent_nodes["sub_domains"]


def test_delete_sub_domain_negative(clean_firestore):
  sub_domain_uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{sub_domain_uuid}"
  response = {
      "success": False,
      "message": "Sub Domain with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_update_sub_domain_positive(clean_firestore, add_data):
  domain_id, category_id, competency_id = add_data
  sub_domain_dict = deepcopy(BASIC_SUB_DOMAIN_MODEL_EXAMPLE)

  url = api_url
  resp = client_with_emulator.post(url, json=sub_domain_dict)
  json_response = resp.json()

  updated_data = json_response["data"]
  updated_data["name"] = "some random name"
  updated_data["parent_nodes"] = {"domains": [domain_id]}
  updated_data["child_nodes"] = {"categories": [category_id],
                                "competencies": [competency_id]}

  uuid = updated_data.get("uuid")
  url = f"{api_url}/{uuid}"
  resp = client_with_emulator.put(url, json=updated_data)
  json_response_update_req = resp.json()

  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get(
      "message"
  ) == "Successfully updated the sub_domain", "Expected response not same"
  assert json_response_update_req.get("data").get(
      "name") == "some random name", "Expected response not same"
  assert json_response_update_req.get("data").get(
      "child_nodes").get("competencies")[0] == competency_id
  assert json_response_update_req.get("data").get(
      "child_nodes").get("categories")[0] == category_id
  assert json_response_update_req.get("data").get(
      "parent_nodes").get("domains")[0] == domain_id
  # Check if sub-domain is updated in child nodes of domain:
  domain_obj = Domain.find_by_uuid(domain_id)
  domain_child_nodes = domain_obj.child_nodes
  assert domain_child_nodes["sub_domains"][0] == uuid
  # Check if sub-domain is updated in parent nodes of competencies:
  competency_obj = SkillServiceCompetency.find_by_uuid(competency_id)
  comp_parent_nodes = competency_obj.parent_nodes
  assert comp_parent_nodes["sub_domains"][0] == uuid
  # Check if sub-domain is updated in parent nodes of category:
  category_obj = Category.find_by_uuid(category_id)
  category_parent_nodes = category_obj.parent_nodes
  assert category_parent_nodes["sub_domains"][0] == uuid


def test_update_sub_domain_negative(clean_firestore):
  req_json = deepcopy(BASIC_SUB_DOMAIN_MODEL_EXAMPLE)
  uuid = req_json["uuid"] = "U2DDBkl3Ayg0PWudzhI"
  response = {
      "success": False,
      "message": "Sub Domain with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }

  url = f"{api_url}/{uuid}"
  resp = client_with_emulator.put(url, json=req_json)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_import_sub_domains(clean_firestore):
  url = f"{api_url}/import/json"
  file_path = os.path.join(
      os.path.dirname(__file__), "..", "testing", "sub_domains.json")
  with open(file_path, "rb") as file:
    resp = client_with_emulator.post(url, files={"json_file": file})

  json_response = resp.json()

  assert resp.status_code == 200, "Success not 200"
  assert isinstance(json_response.get("data"), list), "Response is not a list"
  assert len(json_response.get("data")) > 0, "Empty list returned"


def test_get_sub_domains(clean_firestore):
  sub_domain_dict = deepcopy(BASIC_SUB_DOMAIN_MODEL_EXAMPLE)
  sub_domain_dict["name"] = "Communication and general knowledge"
  sub_domain = SubDomain.from_dict(sub_domain_dict)
  sub_domain.uuid = ""
  sub_domain.save()
  sub_domain.uuid = sub_domain.id
  sub_domain.update()
  params = {"skip": 0, "limit": "50"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  saved_names = [i.get("name") for i in json_response.get("data")]
  assert sub_domain_dict["name"] in saved_names, "all data not retrieved"

  # Checking sub domains with filter
  source_name = sub_domain_dict["source_name"]
  url = f"{api_url}s?source_name={source_name}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  saved_source_names = [i.get("source_name") for i in json_response.get("data")]

  assert len(saved_source_names) > 0, \
    "Filtered results should contain the provided source name"

  for saved_source_name in saved_source_names:
    assert saved_source_name == source_name, "Filtered output is wrong"


def test_get_sub_domains_negative(clean_firestore):
  sub_domain_dict = deepcopy(BASIC_SUB_DOMAIN_MODEL_EXAMPLE)
  sub_domain = SubDomain.from_dict(sub_domain_dict)
  sub_domain.uuid = ""
  sub_domain.save()
  sub_domain.uuid = sub_domain.id
  sub_domain.update()
  params = {"skip": "-1", "limit": "50"}

  url = f"{API_URL}/sub-domains"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 422, "Status not 422"
  assert json_response.get(
    "message"
  ) == "Invalid value passed to \"skip\" query parameter", \
    "unknown response received"
