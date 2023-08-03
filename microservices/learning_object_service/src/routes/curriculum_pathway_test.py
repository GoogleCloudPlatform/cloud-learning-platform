"""
  Unit tests for Curriculum Pathway endpoints
"""
import os
import copy
import pytest
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import

from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.curriculum_pathway import router
from schemas.schema_examples import (BASIC_CURRICULUM_PATHWAY_EXAMPLE,
                                     UPDATE_CURRICULUM_PATHWAY_EXAMPLE,
                                     BASIC_LEARNING_EXPERIENCE_EXAMPLE)
from testing.test_config import (API_URL, TESTING_FOLDER_PATH, DEL_KEYS)
from common.models import CurriculumPathway, LearningExperience
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/learning-object-service/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/curriculum-pathway"
CURRICULUM_PATHWAYS_TESTDATA_FILENAME = os.path.join(
    TESTING_FOLDER_PATH, "curriculum_pathways.json")
PATHWAYS_TESTDATA_FILENAME = os.path.join(TESTING_FOLDER_PATH,
                                          "learning_hieararchy_simplified.json")

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


@pytest.mark.parametrize(
    "create_curriculum_pathway", [BASIC_CURRICULUM_PATHWAY_EXAMPLE],
    indirect=True)
def test_search_curriculum_pathway(clean_firestore, create_curriculum_pathway):
  curriculum_pathway_dict = copy.deepcopy(BASIC_CURRICULUM_PATHWAY_EXAMPLE)
  curriculum_pathway = create_curriculum_pathway
  curriculum_pathway_dict["uuid"] = curriculum_pathway.id
  params = {"name": "Kubernetes"}

  url = f"{api_url}/search"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  DEL_KEYS.append("uuid")
  for key in DEL_KEYS:
    if key in json_response["data"][0]:
      del json_response["data"][0][key]
    if key in curriculum_pathway_dict:
      del curriculum_pathway_dict[key]
  assert resp.status_code == 200, "Status code not 200"
  assert json_response.get("data") == [curriculum_pathway_dict]

  #Checking for deleted curriculum pathway
  curriculum_pathway_dict = copy.deepcopy(BASIC_CURRICULUM_PATHWAY_EXAMPLE)
  curriculum_pathway_dict["name"] = "Kubernetes Container Orchestration"
  curriculum_pathway = CurriculumPathway.from_dict(curriculum_pathway_dict)
  curriculum_pathway.uuid = ""
  curriculum_pathway.save()
  curriculum_pathway.is_deleted = True
  curriculum_pathway.uuid = curriculum_pathway.id
  curriculum_pathway.update()
  curriculum_pathway_dict["uuid"] = curriculum_pathway.id

  params = {"name": "Kubernetes Container Orchestration"}
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert len(json_response.get("data")) == 0


@pytest.mark.parametrize(
    "create_curriculum_pathway", [BASIC_CURRICULUM_PATHWAY_EXAMPLE],
    indirect=True)
def test_get_curriculum_pathway(clean_firestore, create_curriculum_pathway):
  curriculum_pathway_dict = copy.deepcopy(BASIC_CURRICULUM_PATHWAY_EXAMPLE)
  curriculum_pathway = create_curriculum_pathway
  uuid = curriculum_pathway_dict["uuid"] = curriculum_pathway.id

  url = f"{api_url}/{uuid}"
  # fetch only the document with given uuid
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  for key in DEL_KEYS:
    if key in json_response["data"]:
      del json_response["data"][key]
  del curriculum_pathway_dict["uuid"]
  assert resp.status_code == 200, "Status code not 200"
  assert json_response.get("data") == curriculum_pathway_dict,\
                                    "Response received"


def test_get_curriculum_pathway_negative(clean_firestore):
  uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{uuid}"
  data = {
      "success": False,
      "message": f"Curriculum Pathway with uuid {uuid} not found",
      "data": None
  }

  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 404, "Status code not 404"
  assert json_response == data, "Response received"


@pytest.mark.parametrize(
    "create_learning_experience", [BASIC_LEARNING_EXPERIENCE_EXAMPLE],
    indirect=True)
def test_post_curriculum_pathway(clean_firestore, create_learning_experience):
  learning_experience = create_learning_experience
  input_curriculum_pathway = copy.deepcopy(BASIC_CURRICULUM_PATHWAY_EXAMPLE)
  input_curriculum_pathway["child_nodes"]["learning_experiences"].append(
      learning_experience.uuid)
  url = api_url
  for key in DEL_KEYS:
    if key in input_curriculum_pathway:
      del input_curriculum_pathway[key]
  post_resp = client_with_emulator.post(url, json=input_curriculum_pathway)
  assert post_resp.status_code == 200, "Status code not 200"

  post_json_response = post_resp.json()
  del post_json_response["data"]["created_time"]
  del post_json_response["data"]["last_modified_time"]
  del post_json_response["data"]["child_nodes_count"]
  uuid = post_json_response.get("data").get("uuid")

  # now see if GET endpoint returns same data
  url = f"{api_url}/{uuid}"
  get_resp = client_with_emulator.get(url)
  get_json_response = get_resp.json()
  del get_json_response["data"]["created_time"]
  del get_json_response["data"]["last_modified_time"]
  del get_json_response["data"]["child_nodes_count"]
  assert get_json_response.get("data") == post_json_response.get("data")

  # now check and confirm it is properly in the databse
  loaded_curriculum_pathway = CurriculumPathway.find_by_uuid(uuid)
  loaded_curriculum_pathway_dict = loaded_curriculum_pathway.to_dict()

  for key in DEL_KEYS:
    if key in loaded_curriculum_pathway_dict:
      loaded_curriculum_pathway_dict.pop(key)
    if key in post_json_response.get("data"):
      post_json_response["data"].pop(key)
  # assert that rest of the fields are equivalent
  assert loaded_curriculum_pathway_dict == post_json_response.get("data")

  # assert the curriculum pathway has reference of learning experience in it's
  # parent nodes field
  learning_experience = LearningExperience.find_by_uuid(
      learning_experience.uuid)
  learning_experience_dict = learning_experience.to_dict()
  assert uuid in learning_experience_dict.get("parent_nodes").get(
      "curriculum_pathways")


def test_update_curriculum_pathway(clean_firestore):
  learning_experiences = []
  for _ in range(3):
    learning_experience = LearningExperience.from_dict(
        copy.deepcopy(BASIC_LEARNING_EXPERIENCE_EXAMPLE))
    learning_experience.uuid = ""
    learning_experience.version = 1
    learning_experience.save()
    learning_experience.uuid = learning_experience.id
    learning_experience.update()
    learning_experiences.append(learning_experience)

  learning_experience_1 = learning_experiences[0]
  learning_experience_2 = learning_experiences[1]
  learning_experience_3 = learning_experiences[2]

  curriculum_pathway_dict = copy.deepcopy(BASIC_CURRICULUM_PATHWAY_EXAMPLE)
  curriculum_pathway_dict["child_nodes"]["learning_experiences"].append(
      learning_experience_1.uuid)
  curriculum_pathway_dict["child_nodes"]["learning_experiences"].append(
      learning_experience_2.uuid)

  url = f"{api_url}"
  post_resp = client_with_emulator.post(url, json=curriculum_pathway_dict)

  assert post_resp.status_code == 200, "Status code not 200"
  post_json_response = post_resp.json()
  uuid = curriculum_pathway_dict["uuid"] = post_json_response.get("data").get(
      "uuid")

  child_curriculum_pathway_dict = copy.deepcopy(
      BASIC_CURRICULUM_PATHWAY_EXAMPLE)
  child_curriculum_pathway_dict["parent_nodes"]["curriculum_pathways"].append(
      uuid)
  child_curriculum_pathway_dict["parent_nodes"]["curriculum_pathways"].append(
      uuid)
  url = f"{api_url}"
  child_post_resp = client_with_emulator.post(
      url, json=child_curriculum_pathway_dict)
  assert child_post_resp.status_code == 200, "Status code not 200"
  child_post_json_response = child_post_resp.json()
  child_cp_uuid = child_curriculum_pathway_dict["uuid"] = \
    child_post_json_response.get("data").get("uuid")

  # assert the parent curriculum pathway has reference of child
  # curriculum pathway in its child nodes
  parent_curriculum_pathway = CurriculumPathway.find_by_uuid(uuid)
  parent_curriculum_pathway_dict = parent_curriculum_pathway.to_dict()
  assert child_cp_uuid in parent_curriculum_pathway_dict.get("child_nodes").get(
      "curriculum_pathways")

  # assert the learning experience has reference of curriculum pathway in it's
  # parent nodes field
  learning_experience = LearningExperience.find_by_uuid(
      learning_experience_1.uuid)
  learning_experience_dict = learning_experience.to_dict()
  assert uuid in learning_experience_dict.get("parent_nodes").get(
      "curriculum_pathways")

  learning_experience = LearningExperience.find_by_uuid(
      learning_experience_2.uuid)
  learning_experience_dict = learning_experience.to_dict()
  assert uuid in learning_experience_dict.get("parent_nodes").get(
      "curriculum_pathways")

  updated_data = copy.deepcopy(curriculum_pathway_dict)
  updated_data["name"] = "Terraform"
  updated_data["is_archived"] = False
  updated_data["child_nodes"]["learning_experiences"].append(
      learning_experience_3.uuid)
  updated_data["child_nodes"]["learning_experiences"].remove(
      learning_experience_1.uuid)
  for key in DEL_KEYS:
    if key in updated_data:
      del updated_data[key]
  url = f"{api_url}/{uuid}"

  # Test to update the document itself
  params = {"create_version": False}
  resp = client_with_emulator.put(url, params=params, json=updated_data)
  json_response_update_req = resp.json()
  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get(
      "message"
  ) == "Successfully updated the curriculum pathway", \
  "Expected response not same"
  assert json_response_update_req.get("data").get("name") == "Terraform"

  # Test to verify the child learning experience references are updated
  # assert the learning experience has reference of curriculum
  # pathway in it's parent nodes field
  learning_experience = LearningExperience.find_by_uuid(
      learning_experience_1.uuid)
  learning_experience_dict = learning_experience.to_dict()
  assert uuid not in learning_experience_dict.get("parent_nodes").get(
      "curriculum_pathways")

  learning_experience = LearningExperience.find_by_uuid(
      learning_experience_2.uuid)
  learning_experience_dict = learning_experience.to_dict()
  assert uuid in learning_experience_dict.get("parent_nodes").get(
      "curriculum_pathways")

  learning_experience = LearningExperience.find_by_uuid(
      learning_experience_3.uuid)
  learning_experience_dict = learning_experience.to_dict()
  assert uuid in learning_experience_dict.get("parent_nodes").get(
      "curriculum_pathways")

  # Test to create version of the document
  params = {"create_version": True}
  updated_data["name"] = "Docker"
  updated_data["is_archived"] = False
  resp = client_with_emulator.put(url, params=params, json=updated_data)
  json_response_update_req = resp.json()

  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get(
      "message"
  ) == "Successfully updated the curriculum pathway", \
  "Expected response not same"
  assert json_response_update_req.get("data").get("name") == "Docker"
  assert json_response_update_req.get("data").get("version") == 2


@pytest.mark.parametrize(
    "create_curriculum_pathway", [UPDATE_CURRICULUM_PATHWAY_EXAMPLE],
    indirect=True)
def test_update_curriculum_pathway_negative(clean_firestore,
                                            create_curriculum_pathway):
  curriculum_pathway_dict = copy.deepcopy(UPDATE_CURRICULUM_PATHWAY_EXAMPLE)
  uuid = curriculum_pathway_dict["uuid"] = "U2DDBkl3Ayg0PWudzhI"

  response = {
      "success": False,
      "message": "Curriculum Pathway with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  url = f"{api_url}/{uuid}"
  curriculum_pathway_dict["version"] = 4
  # Negative test when updating the document itself with wrong request body
  params = {"create_version": False}
  resp = client_with_emulator.put(
      url, params=params, json=curriculum_pathway_dict)
  json_response = resp.json()

  assert resp.status_code == 422, "Status code not 422"

  # Negative test when creating version document with wrong request body
  params = {"create_version": True}
  resp = client_with_emulator.put(
      url, params=params, json=curriculum_pathway_dict)
  json_response = resp.json()

  assert resp.status_code == 422, "Status code not 422"

  url = f"{api_url}/{uuid}"
  response = {
      "success": False,
      "message": "Curriculum Pathway with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  # Negative test when updating the document itself with wrong uuid
  params = {"create_version": False}
  DEL_KEYS.append("uuid")
  for key in DEL_KEYS:
    if key in curriculum_pathway_dict:
      del curriculum_pathway_dict[key]
  # del curriculum_pathway_dict["uuid"]
  resp = client_with_emulator.put(
      url, params=params, json=curriculum_pathway_dict)
  json_response = resp.json()
  assert resp.status_code == 404, "Status code not 404"
  assert json_response == response, "Expected response not same"

  # Negative test when creating version document with wrong uuid
  params = {"create_version": True}
  resp = client_with_emulator.put(
      url, params=params, json=curriculum_pathway_dict)
  json_response = resp.json()

  assert resp.status_code == 404, "Status code not 404"
  assert json_response == response, "Expected response not same"


@pytest.mark.parametrize(
    "create_learning_experience", [BASIC_LEARNING_EXPERIENCE_EXAMPLE],
    indirect=True)
def test_delete_curriculum_pathway(clean_firestore, create_learning_experience):
  learning_experience = create_learning_experience

  curriculum_pathway = copy.deepcopy(BASIC_CURRICULUM_PATHWAY_EXAMPLE)
  curriculum_pathway["child_nodes"]["learning_experiences"].append(
      learning_experience.uuid)

  url = f"{api_url}"
  post_resp = client_with_emulator.post(url, json=curriculum_pathway)
  assert post_resp.status_code == 200, "Status code not 200"
  post_json_response = post_resp.json()
  uuid = post_json_response.get("data").get("uuid")

  # assert the learning experience has reference of curriculum pathway in it's
  # parent nodes field
  learning_experience = LearningExperience.find_by_uuid(
      learning_experience.uuid)
  learning_experience_dict = learning_experience.to_dict()
  assert uuid in learning_experience_dict.get("parent_nodes").get(
      "curriculum_pathways")

  url = f"{api_url}/{uuid}"
  resp = client_with_emulator.delete(url)
  del_json_response = resp.json()

  expected_data = {
      "success": True,
      "message": "Successfully deleted the curriculum pathway"
  }
  assert resp.status_code == 200, "Status code not 200"
  assert del_json_response == expected_data, "Expected response not same"

  # assert the learning experience do not have the reference of curriculum
  # pathway in it's parent nodes field
  learning_experience = LearningExperience.find_by_uuid(
      learning_experience.uuid)
  learning_experience_dict = learning_experience.to_dict()
  assert uuid not in learning_experience_dict.get("parent_nodes").get(
      "curriculum_pathways")

  # assert that the curriculum pathway exists in the database and is soft
  # deleted
  curriculum_pathway = CurriculumPathway.find_by_uuid(uuid, is_deleted=True)
  assert curriculum_pathway


def test_delete_curriculum_pathway_negative(clean_firestore):
  curriculum_pathway_uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{curriculum_pathway_uuid}"
  response = {
      "success": False,
      "message": "Curriculum Pathway with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status code not404"
  assert json_response == response, "Expected response not same"


def test_import_curriculum_pathways(clean_firestore):
  url = f"{api_url}/import/json"
  with open(
      CURRICULUM_PATHWAYS_TESTDATA_FILENAME,
      encoding="UTF-8") as curriculum_pathways_json_file:
    resp = client_with_emulator.post(
        url, files={"json_file": curriculum_pathways_json_file})

  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  assert isinstance(json_response.get("data"), list), "Response is not a list"
  assert len(json_response.get("data")) > 0, "Empty list returned"


@pytest.mark.parametrize(
    "create_curriculum_pathway, create_learning_experience",
    [(BASIC_CURRICULUM_PATHWAY_EXAMPLE, BASIC_LEARNING_EXPERIENCE_EXAMPLE)],
    indirect=True)
def test_get_curriculum_pathways(clean_firestore, create_curriculum_pathway,
                                 create_learning_experience):
  curriculum_pathway = create_curriculum_pathway

  # create an archived object
  archived_curriculum_pathway_dict = copy.deepcopy(
      BASIC_CURRICULUM_PATHWAY_EXAMPLE)
  archived_curriculum_pathway_dict["name"] = "Python"
  archived_curriculum_pathway = CurriculumPathway.from_dict(
      archived_curriculum_pathway_dict)
  archived_curriculum_pathway.uuid = ""
  archived_curriculum_pathway.save()
  archived_curriculum_pathway.uuid = archived_curriculum_pathway.id
  archived_curriculum_pathway.is_archived = True
  archived_curriculum_pathway.update()

  params = {"skip": 0, "limit": "30"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_names = [i.get("name") for i in json_response.get(
    "data")["records"]]
  assert curriculum_pathway.name in saved_names, "all data not retrived"
  assert archived_curriculum_pathway.name in saved_names, (
      "all data not retrived")

  # Test archival functionality: Fetch all archived objects
  params = {"skip": 0, "limit": "30", "fetch_archive": True}
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_uuids = [i.get("uuid") for i in json_response.get(
    "data")["records"]]
  assert archived_curriculum_pathway.uuid in saved_uuids

  # Test archival functionality: Fetch all non archived objects
  params = {"skip": 0, "limit": "30", "fetch_archive": False}
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_uuids = [i.get("uuid") for i in json_response.get(
    "data")["records"]]
  assert curriculum_pathway.uuid in saved_uuids

  # test get curriculum pathways with filters
  params = {"skip": 0, "limit": "30", "author": "TestUser"}
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_names = [i.get("author") for i in json_response.get(
    "data")["records"]]
  assert len(list(set(saved_names))) == 1, "Unnecessary data retrieved"
  assert list(set(saved_names))[0] == params["author"], "Wrong data retrieved"

  # test get curriculum pathways with child node filters
  child_learning_experience = create_learning_experience
  curriculum_pathway.child_nodes = {
    "learning_experiences": [child_learning_experience.uuid]}
  curriculum_pathway.update()

  params = {
      "skip": 0,
      "limit": "10",
      "learning_experience": child_learning_experience.uuid
  }
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_les = [i.get("child_nodes") for i in json_response.get(
    "data")["records"]]
  assert params["learning_experience"] in saved_les[0][
      "learning_experiences"], "Wrong parent_curriculum_pathway retrieved"

  # Test to get child curriculum pathway
  child_curriculum_pathway = create_curriculum_pathway
  curriculum_pathway.child_nodes = {
    "curriculum_pathways": [child_curriculum_pathway.uuid]}
  curriculum_pathway.update()
  params = {
      "skip": 0,
      "limit": "10",
      "child_curriculum_pathway": child_curriculum_pathway.uuid
  }
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_les = [i.get("child_nodes") for i in json_response.get(
    "data")["records"]]
  assert params["child_curriculum_pathway"] in saved_les[0][
      "curriculum_pathways"], "Wrong child_curriculum_pathway retrieved"


@pytest.mark.parametrize(
    "create_curriculum_pathway", [BASIC_CURRICULUM_PATHWAY_EXAMPLE],
    indirect=True)
def test_copy_curriculum_pathway(clean_firestore, create_curriculum_pathway):
  curriculum_pathway_dict = copy.deepcopy(BASIC_CURRICULUM_PATHWAY_EXAMPLE)
  curriculum_pathway = create_curriculum_pathway
  uuid = curriculum_pathway_dict["uuid"] = curriculum_pathway.id
  url = f"{api_url}/copy/{uuid}"
  resp = client_with_emulator.post(url)
  json_response = resp.json()
  DEL_KEYS.append("uuid")
  for key in DEL_KEYS:
    if key in json_response["data"]:
      del json_response["data"][key]
  del curriculum_pathway_dict["uuid"]
  assert resp.status_code == 200, "Status code not 200"
  assert json_response.get(
      "data") == curriculum_pathway_dict, "Response received"

def test_bulk_import_pathway(clean_firestore):
  url = f"{api_url}/bulk-import/json"
  with open(PATHWAYS_TESTDATA_FILENAME, encoding="UTF-8") as pathways_json_file:
    resp = client_with_emulator.post(
        url, files={"json_file": pathways_json_file})

  assert resp.status_code == 200, "Status code not 200"


def test_get_pathway_tree(clean_firestore):
  # import pathway tree
  url = f"{api_url}/bulk-import/json"
  with open(PATHWAYS_TESTDATA_FILENAME, encoding="UTF-8") as pathways_json_file:
    resp = client_with_emulator.post(
        url, files={"json_file": pathways_json_file})

  resp_json = resp.json()

  assert resp.status_code == 200, "Status code not 200"
  assert resp_json["data"] is not None, "Data is not returned"

  curriculum_pathway_id = resp_json["data"][0]

  # get pathway tree
  url = f"{api_url}/{curriculum_pathway_id}"
  resp = client_with_emulator.get(url, params={"fetch_tree": True})

  resp_json = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  assert resp_json["data"] is not None, "Data is not returned"


def fetch_child_nodes_with_filters(clean_firestore):
  """Test for pathway filters"""
  curriculum_pathway_dict = copy.deepcopy(BASIC_CURRICULUM_PATHWAY_EXAMPLE)
  curriculum_pathway_dict["name"] = "Pathway - Program"
  curriculum_pathway_dict["alias"] = "program"
  curriculum_pathway_program = CurriculumPathway.from_dict(
    curriculum_pathway_dict)
  curriculum_pathway_program.uuid = ""
  curriculum_pathway_program.save()
  curriculum_pathway_program.uuid = curriculum_pathway_program.id
  curriculum_pathway_program.update()

  curriculum_pathway_dict = copy.deepcopy(BASIC_CURRICULUM_PATHWAY_EXAMPLE)
  curriculum_pathway_dict["name"] = "Pathway - Level"
  curriculum_pathway_dict["alias"] = "level"
  curriculum_pathway_level = CurriculumPathway.from_dict(
    curriculum_pathway_dict)
  curriculum_pathway_level.uuid = ""
  curriculum_pathway_level.save()
  curriculum_pathway_level.uuid = curriculum_pathway_level.id
  curriculum_pathway_level.update()

  curriculum_pathway_dict = copy.deepcopy(BASIC_CURRICULUM_PATHWAY_EXAMPLE)
  curriculum_pathway_dict["name"] = "Pathway - Discipline"
  curriculum_pathway_dict["alias"] = "discipline"
  curriculum_pathway_discipline = CurriculumPathway.from_dict(
    curriculum_pathway_dict)
  curriculum_pathway_discipline.uuid = ""
  curriculum_pathway_discipline.save()
  curriculum_pathway_discipline.uuid = curriculum_pathway_discipline.id
  curriculum_pathway_discipline.update()

  curriculum_pathway_program.child_nodes = {
    "curriculum_pathways": [curriculum_pathway_level.uuid]
  }
  curriculum_pathway_program.update()

  curriculum_pathway_level.child_nodes = {
    "curriculum_pathways": [curriculum_pathway_discipline.uuid]
  }
  curriculum_pathway_level.update()

  curriculum_pathway_discipline.child_nodes = {}
  curriculum_pathway_discipline.update()

  url = f"{api_url}s/{curriculum_pathway_program.uuid}" + \
            "/nodes/curriculum-pathways?alias=discipline"
  resp = client_with_emulator.get(url)
  resp_json = resp.json()
  assert resp.status_code == 200
  assert resp_json["data"][0]["uuid"] == curriculum_pathway_discipline.uuid
  assert resp_json["data"][0]["alias"] == "discipline"
