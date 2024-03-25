"""
  Unit tests for Competency endpoints
"""
import os
import json
import pytest
from copy import deepcopy
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.competency import router
from testing.test_config import (API_URL, TESTING_FOLDER_PATH)
from schemas.schema_examples import (BASIC_COMPETENCY_MODEL_EXAMPLE,
                                    BASIC_SUB_DOMAIN_MODEL_EXAMPLE,
                                    BASIC_CATEGORY_MODEL_EXAMPLE,
                                    BASIC_SKILL_MODEL_EXAMPLE)
from common.models import SkillServiceCompetency, SubDomain, Category, Skill
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers
from uuid import uuid4

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/skill-service/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/competency"

TESTDATA_FILENAME = os.path.join(TESTING_FOLDER_PATH, "competencies.json")

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

  category_dict = BASIC_CATEGORY_MODEL_EXAMPLE
  category = Category.from_dict(category_dict)
  category.uuid = ""
  category.save()
  category.uuid = category.id
  category.update()

  skill_dict = BASIC_SKILL_MODEL_EXAMPLE
  skill = Skill.from_dict(skill_dict)
  skill.uuid = ""
  skill.save()
  skill.uuid = skill.id
  skill.update()

  return [sub_domain.uuid, category.uuid, skill.uuid]

def test_get_competency(clean_firestore, add_data):
  sub_domain_uuid = add_data[0]
  category_uuid = add_data[1]
  skill_uuid = add_data[2]

  competency_dict = deepcopy(BASIC_COMPETENCY_MODEL_EXAMPLE)
  competency_dict["parent_nodes"]["categories"] = [category_uuid]
  competency_dict["parent_nodes"]["sub_domains"] = [sub_domain_uuid]
  competency_dict["child_nodes"]["skills"] = [skill_uuid]
  competency = SkillServiceCompetency.from_dict(competency_dict)
  competency.uuid = ""
  competency.save()
  competency.uuid = competency.id
  competency.update()
  competency_dict["uuid"] = competency.id

  url = f"{api_url}/{competency.uuid}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  del json_response["data"]["created_time"]
  del json_response["data"]["last_modified_time"]
  assert resp.status_code == 200, "Status 200"
  assert json_response.get("data") == competency_dict, "Response received"

  ## testing with fetch_tree=True
  resp = client_with_emulator.get(url, params={"fetch_tree": True})
  json_response_get_req = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  parent_sub_domain = json_response_get_req["data"]["parent_nodes"][
    "sub_domains"][0]
  parent_category = json_response_get_req["data"]["parent_nodes"][
    "categories"][0]
  child_skill = json_response_get_req["data"]["child_nodes"][
    "skills"][0]
  assert parent_sub_domain["uuid"] == sub_domain_uuid
  assert parent_category["uuid"] == category_uuid
  assert child_skill["uuid"] == skill_uuid


def test_get_competency_negative(clean_firestore):
  uuid = "random_id"
  url = f"{api_url}/{uuid}"
  data = {
      "success": False,
      "message": f"Competency with uuid {uuid} not found",
      "data": None
  }

  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 404, "Status 404"
  assert json_response == data, "Response received"


def test_post_competency(clean_firestore, add_data):
  sub_domain_uuid = add_data[0]
  category_uuid = add_data[1]
  skill_uuid = add_data[2]

  input_competency = deepcopy(BASIC_COMPETENCY_MODEL_EXAMPLE)
  input_competency["parent_nodes"]["categories"] = [category_uuid]
  input_competency["parent_nodes"]["sub_domains"] = [sub_domain_uuid]
  input_competency["child_nodes"]["skills"] = [skill_uuid]
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_competency)

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
  loaded_competency = SkillServiceCompetency.find_by_uuid(uuid)
  loaded_competency_dict = loaded_competency.to_dict()

  # popping id and key for equivalency test
  loaded_competency_dict.pop("id")
  loaded_competency_dict.pop("key")
  loaded_competency_dict.pop("created_by")
  loaded_competency_dict.pop("created_time")
  loaded_competency_dict.pop("last_modified_by")
  loaded_competency_dict.pop("last_modified_time")
  loaded_competency_dict.pop("archived_at_timestamp")
  loaded_competency_dict.pop("archived_by")
  loaded_competency_dict.pop("deleted_at_timestamp")
  loaded_competency_dict.pop("deleted_by")

  # assert that rest of the fields are equivalent
  assert loaded_competency_dict == post_json_response.get("data")

  sub_domain_doc = SubDomain.find_by_uuid(sub_domain_uuid)
  category_doc = Category.find_by_uuid(category_uuid)
  skill_doc = Skill.find_by_uuid(skill_uuid)
  assert uuid in sub_domain_doc.child_nodes["competencies"]
  assert uuid in category_doc.child_nodes["competencies"]
  assert uuid in skill_doc.parent_nodes["competencies"]


def test_update_competency(clean_firestore, add_data):
  sub_domain_id, category_id, skill_id = add_data
  competency_dict = deepcopy(BASIC_COMPETENCY_MODEL_EXAMPLE)
  competency = SkillServiceCompetency.from_dict(competency_dict)
  competency.uuid = ""
  competency.save()
  competency.uuid = competency.id
  competency.update()
  uuid = competency_dict["uuid"] = competency.id

  updated_data = competency_dict
  updated_data["name"] = "some random name"
  updated_data["parent_nodes"] = {"sub_domains": [sub_domain_id],
                                  "categories": [category_id]}
  updated_data["child_nodes"] = {"skills": [skill_id]}

  url = f"{api_url}/{uuid}"
  resp = client_with_emulator.put(url, json=updated_data)
  json_response_update_req = resp.json()

  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get(
      "message"
  ) == "Successfully updated the competency", "Expected response not same"
  assert json_response_update_req.get("data").get(
      "name") == "some random name", "Expected response not same"
  assert json_response_update_req.get("data").get(
      "child_nodes").get("skills")[0] == skill_id
  assert json_response_update_req.get("data").get(
      "parent_nodes").get("sub_domains")[0] == sub_domain_id
  assert json_response_update_req.get("data").get(
      "parent_nodes").get("categories")[0] == category_id
  # Check if competency is updated in parent nodes of skill:
  skill_obj = Skill.find_by_uuid(skill_id)
  skill_parent_nodes = skill_obj.parent_nodes
  assert skill_parent_nodes["competencies"][0] == uuid
  # Check if competency is updated in child nodes of sub-domain:
  sub_domain_obj = SubDomain.find_by_uuid(sub_domain_id)
  subdomain_child_nodes = sub_domain_obj.child_nodes
  assert subdomain_child_nodes["competencies"][0] == uuid
  # Check if competency is updated in child nodes of category:
  category_obj = Category.find_by_uuid(category_id)
  category_child_nodes = category_obj.child_nodes
  assert category_child_nodes["competencies"][0] == uuid


def test_update_competency_negative(clean_firestore):
  competency_dict = deepcopy(BASIC_COMPETENCY_MODEL_EXAMPLE)
  competency = SkillServiceCompetency.from_dict(competency_dict)
  competency.uuid = ""
  competency.save()
  competency.uuid = competency.id
  competency.update()
  uuid = competency_dict["uuid"] = "random_id"

  url = f"{api_url}/{uuid}"
  response = {
      "success": False,
      "message": f"Competency with uuid {uuid} not found",
      "data": None
  }
  resp = client_with_emulator.put(url, json=competency_dict)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_delete_competency(clean_firestore, add_data):
  sub_domain_uuid, category_uuid, skill_uuid = add_data

  competency_dict = deepcopy(BASIC_COMPETENCY_MODEL_EXAMPLE)
  competency_dict["uuid"] = ""
  competency_dict["parent_nodes"] = {"categories": [category_uuid],
                                    "sub_domains": [sub_domain_uuid]}
  competency_dict["child_nodes"] = {"skills": [skill_uuid]}
  post_url = f"{api_url}"
  post_resp = client_with_emulator.post(post_url, json=competency_dict)
  post_json_response = post_resp.json()
  competency_id = post_json_response["data"]["uuid"]

  url = f"{api_url}/{competency_id}"
  resp = client_with_emulator.delete(url)
  del_json_response = resp.json()

  expected_data = {
      "success": True,
      "message": "Successfully deleted the competency"
  }
  assert resp.status_code == 200, "Status code not 200"
  assert del_json_response == expected_data, "Expected response not same"
  sub_domain_doc = SubDomain.find_by_uuid(sub_domain_uuid)
  category_doc = Category.find_by_uuid(category_uuid)
  skill_doc = Skill.find_by_uuid(skill_uuid)
  assert competency_id not in sub_domain_doc.child_nodes["competencies"]
  assert competency_id not in category_doc.child_nodes["competencies"]
  assert competency_id not in skill_doc.parent_nodes["competencies"]


def test_delete_competency_negative(clean_firestore):
  competency_uuid = "random_id"
  url = f"{api_url}/{competency_uuid}"
  response = {
      "success": False,
      "message": f"Competency with uuid {competency_uuid} not found",
      "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_import_competencies(clean_firestore):
  url = f"{api_url}/import/json"
  with open(TESTDATA_FILENAME, encoding="UTF-8") as competencies_json_file:
    resp = client_with_emulator.post(
        url, files={"json_file": competencies_json_file})

  json_response = resp.json()
  assert resp.status_code == 200, "Status not 200"
  assert isinstance(json_response.get("data"), list), "Response is not a list"
  assert len(json_response.get("data")) > 0, "Empty list returned"


def test_get_competencies(clean_firestore):
  competency_dict = deepcopy(BASIC_COMPETENCY_MODEL_EXAMPLE)
  competency_dict["name"] = "testing name of competency"
  competency = SkillServiceCompetency.from_dict(competency_dict)
  competency.uuid = ""
  competency.save()
  competency.uuid = competency.id
  competency.update()
  params = {"skip": 0, "limit": "50"}

  url = f"{API_URL}/competencies"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  saved_titles = [i.get("name") for i in json_response.get("data")]
  assert competency_dict["name"] in saved_titles, "all data not retrieved"

  # Checking competencies with filter
  level = competency_dict["level"]
  subject_code = competency_dict["subject_code"]
  course_code = competency_dict["course_code"]
  source_name = competency_dict["source_name"]

  filters = f"level={level}&subject_code={subject_code}"
  filters += f"&course_code={course_code}&source_name={source_name}"
  url = f"{API_URL}/competencies?{filters}"

  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"

  saved_levels = [i.get("level") for i in json_response.get("data")]
  saved_subject_codes = [
      i.get("subject_code") for i in json_response.get("data")
  ]
  saved_course_codes = [i.get("course_code") for i in json_response.get("data")]
  saved_source_names = [i.get("source_name") for i in json_response.get("data")]

  assert len(saved_levels) > 0, \
    "Filtered results should contain the provided level"
  assert len(saved_subject_codes) > 0, \
    "Filtered results should contain the provided subject code"
  assert len(saved_course_codes) > 0, \
    "Filtered results should contain the provided course code"
  assert len(saved_source_names) > 0, \
    "Filtered results should contain the provided source name"

  for saved_level in saved_levels:
    assert saved_level == level, "Filtered output is wrong"
  for saved_subject_code in saved_subject_codes:
    assert saved_subject_code == subject_code, "Filtered output is wrong"
  for saved_course_code in saved_course_codes:
    assert saved_course_code == course_code, "Filtered output is wrong"
  for saved_source_name in saved_source_names:
    assert saved_source_name == source_name, "Filtered output is wrong"


def test_get_competencies_negative(clean_firestore):
  competency_dict = deepcopy(BASIC_COMPETENCY_MODEL_EXAMPLE)
  competency = SkillServiceCompetency.from_dict(competency_dict)
  competency.uuid = ""
  competency.save()
  competency.uuid = competency.id
  competency.update()
  params = {"skip": "-1", "limit": "50"}

  url = f"{API_URL}/competencies"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422, "Status not 422"
  assert json_response.get(
    "message"
  ) == "Invalid value passed to \"skip\" query parameter", \
    "unknown response received"


def test_get_skills_from_competencies(clean_firestore):
  skill_dict = deepcopy(BASIC_SKILL_MODEL_EXAMPLE)
  skill_uuids = []
  for _ in range(3):
    skill = Skill.from_dict(skill_dict)
    skill.uuid = ""
    skill.save()
    skill.uuid = skill.id
    skill.update()
    skill_uuids.append(skill.uuid)
  competency_dict = deepcopy(BASIC_COMPETENCY_MODEL_EXAMPLE)
  competency = SkillServiceCompetency.from_dict(competency_dict)
  competency.child_nodes = {"skills": skill_uuids}
  competency.uuid = ""
  competency.save()
  competency.uuid = competency.id
  competency.update()
  url = f"{API_URL}/competencies/fetch_skills"
  params = {"competencies": [competency.uuid]}
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  actual_skill_uuids = [skill.get("skill_id") for skill in json_response
                        ["data"][competency.uuid]]
  assert set(actual_skill_uuids) == set(skill_uuids),\
      "All child skills for the parent competency are not fetched"

def test_get_skills_from_competencies_negative(clean_firestore):
  url = f"{API_URL}/competencies/fetch_skills"
  competency_uuid = str(uuid4())
  params = {"competencies": [competency_uuid]}
  resp = client_with_emulator.get(url, params=params)
  assert resp.status_code == 404,\
      f"Competency with uuid: {competency_uuid} exists"
