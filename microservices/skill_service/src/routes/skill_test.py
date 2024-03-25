"""
  Tests for Skill endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
import os
import json
import pytest
from copy import deepcopy
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.skill import router
from testing.test_config import API_URL
from schemas.schema_examples import (BASIC_SKILL_MODEL_EXAMPLE,
                                    BASIC_COMPETENCY_MODEL_EXAMPLE)
from common.models import Skill, SkillServiceCompetency
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/skill-service/api/v1")

client_with_emulator = TestClient(app)

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

@pytest.fixture(name="add_data")
def add_data():
  competency_dict = deepcopy(BASIC_COMPETENCY_MODEL_EXAMPLE)
  competency = SkillServiceCompetency.from_dict(competency_dict)
  competency.uuid = ""
  competency.save()
  competency.uuid = competency.id
  competency.update()

  return [competency.uuid]


def test_post_and_get_skill(clean_firestore, add_data):
  competency_uuid = add_data[0]

  skill_dict = deepcopy(BASIC_SKILL_MODEL_EXAMPLE)
  skill_dict["parent_nodes"]["competencies"] = [competency_uuid]

  url = f"{API_URL}/skill"
  resp = client_with_emulator.post(url, json=skill_dict)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  assert json_response.get("success") is True, "Success not true"
  assert json_response.get(
      "message"
  ) == "Successfully created the skill", "Expected response not same"
  assert json_response.get("data").get("name") == skill_dict.get(
      "name"), "Expected response not same"

  skill_uuid = json_response["data"]["uuid"]
  parent_competency_doc = SkillServiceCompetency.find_by_uuid(competency_uuid)
  assert skill_uuid in parent_competency_doc.child_nodes["skills"]

  url = f"{API_URL}/skill/{skill_uuid}"
  resp = client_with_emulator.get(url)
  json_response_get_req = resp.json()

  assert resp.status_code == 200, "Status code not 200"
  assert json_response_get_req.get("data") == json_response.get(
      "data"), "Expected response not same"

  ## testing with fetch_tree=True
  resp = client_with_emulator.get(url, params={"fetch_tree": True})
  json_response_get_req = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  parent_competency = json_response_get_req["data"]["parent_nodes"][
    "competencies"][0]
  assert parent_competency["uuid"] == competency_uuid
  assert skill_uuid in parent_competency["child_nodes"]["skills"]


def test_get_skill_negative(clean_firestore):
  skill_uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{API_URL}/skill/{skill_uuid}"
  response = {
      "success": False,
      "message": "Skill with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_delete_skill_positive(clean_firestore, add_data):
  competency_uuid = add_data[0]

  skill_dict = deepcopy(BASIC_SKILL_MODEL_EXAMPLE)
  skill_dict["parent_nodes"]["competencies"] = [competency_uuid]

  url = f"{API_URL}/skill"
  resp = client_with_emulator.post(url, json=skill_dict)
  json_response = resp.json()

  skill_uuid = json_response["data"]["uuid"]
  parent_competency_doc = SkillServiceCompetency.find_by_uuid(competency_uuid)
  assert skill_uuid in parent_competency_doc.child_nodes["skills"]

  url = f"{API_URL}/skill/{skill_uuid}"
  resp = client_with_emulator.delete(url)
  json_response_delete_req = resp.json()

  expected_data = {"success": True, "message": "Successfully deleted the skill"}
  assert resp.status_code == 200, "Status code not 200"
  assert json_response_delete_req == expected_data, "Expected response not same"

  parent_competency_doc = SkillServiceCompetency.find_by_uuid(competency_uuid)
  assert skill_uuid not in parent_competency_doc.child_nodes["skills"]


def test_delete_skill_negative(clean_firestore):
  skill_uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{API_URL}/skill/{skill_uuid}"
  response = {
      "success": False,
      "message": "Skill with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_update_skill_positive(clean_firestore, add_data):
  competency_id = add_data[0]
  skill_dict = deepcopy(BASIC_SKILL_MODEL_EXAMPLE)

  url = f"{API_URL}/skill"
  resp = client_with_emulator.post(url, json=skill_dict)
  json_response = resp.json()

  updated_data = json_response["data"]
  updated_data["name"] = "some random name"
  updated_data["parent_nodes"] = {"competencies": [competency_id]}

  uuid = updated_data.get("uuid")
  url = f"{API_URL}/skill/{uuid}"
  resp = client_with_emulator.put(url, json=updated_data)
  json_response_update_req = resp.json()

  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get(
      "message"
  ) == "Successfully updated the skill", "Expected response not same"
  assert json_response_update_req.get("data").get(
      "name") == "some random name", "Expected response not same"
  assert json_response_update_req.get("data").get(
      "parent_nodes").get("competencies")[0] == competency_id
  # Check if skill is updated in child nodes of competency:
  competency_obj = SkillServiceCompetency.find_by_uuid(competency_id)
  comp_child_nodes = competency_obj.child_nodes
  assert comp_child_nodes["skills"][0] == uuid


def test_update_skill_negative(clean_firestore):
  req_json = deepcopy(BASIC_SKILL_MODEL_EXAMPLE)
  uuid = req_json["uuid"] = "U2DDBkl3Ayg0PWudzhI"
  response = {
      "success": False,
      "message": "Skill with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }

  url = f"{API_URL}/skill/{uuid}"
  resp = client_with_emulator.put(url, json=req_json)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_import_skills(clean_firestore):
  url = f"{API_URL}/skill/import/json"
  file_path = os.path.join(
      os.path.dirname(__file__), "..", "testing", "skills.json")
  with open(file_path, "rb") as file:
    resp = client_with_emulator.post(url, files={"json_file": file})

  json_response = resp.json()

  assert resp.status_code == 200, "Success not 200"
  assert isinstance(json_response.get("data"), list), "Response is not a list"
  assert len(json_response.get("data")) > 0, "Empty list returned"


def test_get_skills(clean_firestore):
  skill_dict = deepcopy(BASIC_SKILL_MODEL_EXAMPLE)
  skill_dict["name"] = "Communication skills"
  skill = Skill.from_dict(skill_dict)
  skill.uuid = ""
  skill.save()
  skill.uuid = skill.id
  skill.update()
  params = {"skip": 0, "limit": "50"}

  url = f"{API_URL}/skills"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  saved_names = [i.get("name") for i in json_response.get("data")]
  assert skill_dict["name"] in saved_names, "all data not retrieved"

  # Checking skills with filter
  creator = skill_dict["creator"]
  source_name = skill_dict["source_name"]

  url = f"{API_URL}/skills?creator={creator}&source_name={source_name}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  json_response_data = json_response.get("data")
  assert resp.status_code == 200, "Status 200"

  saved_creators = [i.get("creator") for i in json_response_data]
  saved_source_names = [i.get("source_name") for i in json_response_data]

  assert len(saved_creators) > 0, \
    "Filtered results should contain the provided saved creators"

  for saved_creator in saved_creators:
    assert saved_creator == creator, "Filtered output is wrong"

  assert len(saved_source_names) > 0, \
    "Filtered results should contain the provided source name"

  for saved_source_name in saved_source_names:
    assert saved_source_name == source_name, "Filtered output is wrong"


def test_get_skills_negative(clean_firestore):
  skill_dict = deepcopy(BASIC_SKILL_MODEL_EXAMPLE)
  skill = Skill.from_dict(skill_dict)
  skill.uuid = ""
  skill.save()
  skill.uuid = skill.id
  skill.update()
  params = {"skip": "-1", "limit": "50"}

  url = f"{API_URL}/skills"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422, "Status not 422"
  assert json_response.get(
    "message"
  ) == "Invalid value passed to \"skip\" query parameter", \
    "unknown response received"
