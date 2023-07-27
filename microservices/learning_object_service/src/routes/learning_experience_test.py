"""
  Unit tests for Learning Experience endpoints
"""
import os
import copy
import pytest
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.learning_experience import router
from schemas.schema_examples import (BASIC_CURRICULUM_PATHWAY_EXAMPLE,
                                     BASIC_LEARNING_EXPERIENCE_EXAMPLE,
                                     UPDATE_LEARNING_EXPERIENCE_EXAMPLE,
                                     BASIC_LEARNING_OBJECT_EXAMPLE)
from testing.test_config import (API_URL, TESTING_FOLDER_PATH, DEL_KEYS)
from common.models import LearningExperience, LearningObject
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/learning-object-service/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/learning-experience"
LEARNING_EXPERIENCES_TESTDATA_FILENAME = os.path.join(
    TESTING_FOLDER_PATH, "learning_experiences.json")

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


@pytest.mark.parametrize(
    "create_learning_experience", [BASIC_LEARNING_EXPERIENCE_EXAMPLE],
    indirect=True)
def test_search_learning_experience(clean_firestore,
                                    create_learning_experience):
  learning_experience_dict = copy.deepcopy(BASIC_LEARNING_EXPERIENCE_EXAMPLE)
  learning_experience = create_learning_experience
  learning_experience_dict["uuid"] = learning_experience.id
  params = {"name": "Kubernetes"}

  url = f"{api_url}/search"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  DEL_KEYS.append("uuid")
  for key in DEL_KEYS:
    if key in json_response["data"][0]:
      del json_response["data"][0][key]
    if key in learning_experience_dict:
      del learning_experience_dict[key]
  assert resp.status_code == 200, "Status code not 200"
  assert json_response.get("data") == [learning_experience_dict]

  #Checking for deleted learning experience
  learning_experience_dict = copy.deepcopy(BASIC_LEARNING_EXPERIENCE_EXAMPLE)
  learning_experience_dict["name"] = "Kubernetes Container Orchestration"
  learning_experience = LearningExperience.from_dict(learning_experience_dict)
  learning_experience.uuid = ""
  learning_experience.save()
  learning_experience.is_deleted = True
  learning_experience.uuid = learning_experience.id
  learning_experience.update()
  learning_experience_dict["uuid"] = learning_experience.id

  params = {"name": "Kubernetes Container Orchestration"}
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert len(json_response.get("data")) == 0


@pytest.mark.parametrize(
    "create_learning_experience", [BASIC_LEARNING_EXPERIENCE_EXAMPLE],
    indirect=True)
def test_get_learning_experience(clean_firestore, create_learning_experience):
  learning_experience_dict = copy.deepcopy(BASIC_LEARNING_EXPERIENCE_EXAMPLE)
  learning_experience = create_learning_experience
  uuid = learning_experience_dict["uuid"] = learning_experience.id

  url = f"{api_url}/{uuid}"
  # fetch only the document with given uuid
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  for key in DEL_KEYS:
    if key in json_response["data"]:
      del json_response["data"][key]
  del learning_experience_dict["uuid"]
  assert resp.status_code == 200, "Status code not 200"
  assert json_response.get("data") == learning_experience_dict,\
        "Response received"


def test_get_learning_experience_negative(clean_firestore):
  uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{uuid}"
  data = {
      "success": False,
      "message": f"Learning Experience with uuid {uuid} not found",
      "data": None
  }

  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 404, "Status code not 404"
  assert json_response == data, "Response received"


@pytest.mark.parametrize(
    "create_learning_object", [BASIC_LEARNING_OBJECT_EXAMPLE], indirect=True)
def test_post_learning_experience(clean_firestore, create_learning_object):
  learning_object = create_learning_object
  input_learning_experience = copy.deepcopy(BASIC_LEARNING_EXPERIENCE_EXAMPLE)
  input_learning_experience["child_nodes"]["learning_objects"].append(
      learning_object.uuid)
  url = api_url
  for key in DEL_KEYS:
    if key in input_learning_experience:
      del input_learning_experience[key]
  post_resp = client_with_emulator.post(url, json=input_learning_experience)
  assert post_resp.status_code == 200, "Status code not 200"

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
  loaded_learning_experience = LearningExperience.find_by_uuid(uuid)
  loaded_learning_experience_dict = loaded_learning_experience.to_dict()

  # popping id and key for equivalency test
  keys_to_delete = [
      "id", "key", "is_deleted", "created_by", "created_time",
      "last_modified_by", "last_modified_time", "archived_at_timestamp",
      "archived_by", "deleted_by", "deleted_at_timestamp"
  ]
  for key in keys_to_delete:
    loaded_learning_experience_dict.pop(key)

  # assert that rest of the fields are equivalent
  assert loaded_learning_experience_dict == post_json_response.get("data")

  # assert the learning object has reference of learning experience in it's
  # parent nodes field
  learning_object = LearningObject.find_by_uuid(learning_object.uuid)
  learning_object_dict = learning_object.to_dict()
  assert uuid in learning_object_dict.get("parent_nodes").get(
      "learning_experiences")


def test_update_learning_experience(clean_firestore):
  learning_objects = []
  for _ in range(3):
    learning_object = LearningObject.from_dict(
        copy.deepcopy(BASIC_LEARNING_OBJECT_EXAMPLE))
    learning_object.uuid = ""
    learning_object.version = 1
    learning_object.save()
    learning_object.uuid = learning_object.id
    learning_object.update()
    learning_objects.append(learning_object)

  learning_object_1 = learning_objects[0]
  learning_object_2 = learning_objects[1]
  learning_object_3 = learning_objects[2]

  learning_experience_dict = copy.deepcopy(BASIC_LEARNING_EXPERIENCE_EXAMPLE)
  del learning_experience_dict["resource_path"]
  learning_experience_dict["child_nodes"]["learning_objects"].append(
      learning_object_1.uuid)
  learning_experience_dict["child_nodes"]["learning_objects"].append(
      learning_object_2.uuid)

  url = f"{api_url}"
  post_resp = client_with_emulator.post(url, json=learning_experience_dict)

  print(post_resp.json())
  assert post_resp.status_code == 200, "Status code not 200"
  post_json_response = post_resp.json()
  uuid = learning_experience_dict["uuid"] = post_json_response.get("data").get(
      "uuid")

  # assert the learning object has reference of learning experience in it's
  # parent nodes field
  learning_object = LearningObject.find_by_uuid(learning_object_1.uuid)
  learning_object_dict = learning_object.to_dict()
  assert uuid in learning_object_dict.get("parent_nodes").get(
      "learning_experiences")

  learning_object = LearningObject.find_by_uuid(learning_object_2.uuid)
  learning_object_dict = learning_object.to_dict()
  assert uuid in learning_object_dict.get("parent_nodes").get(
      "learning_experiences")

  updated_data = copy.deepcopy(learning_experience_dict)
  updated_data["name"] = "Terraform"
  updated_data["is_archived"] = False
  updated_data["child_nodes"]["learning_objects"].append(learning_object_3.uuid)
  updated_data["child_nodes"]["learning_objects"].remove(learning_object_1.uuid)
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
  ) == "Successfully updated the learning experience", \
  "Expected response not same"
  assert json_response_update_req.get("data").get("name") == "Terraform"

  # Test to verify the child learning object references are updated
  # assert the learning object has reference of learning experience in it's
  # parent nodes field
  learning_object = LearningObject.find_by_uuid(learning_object_1.uuid)
  learning_object_dict = learning_object.to_dict()
  assert uuid not in learning_object_dict.get("parent_nodes").get(
      "learning_experiences")

  learning_object = LearningObject.find_by_uuid(learning_object_2.uuid)
  learning_object_dict = learning_object.to_dict()
  assert uuid in learning_object_dict.get("parent_nodes").get(
      "learning_experiences")

  learning_object = LearningObject.find_by_uuid(learning_object_3.uuid)
  learning_object_dict = learning_object.to_dict()
  assert uuid in learning_object_dict.get("parent_nodes").get(
      "learning_experiences")

  # Test to create version of the document
  params = {"create_version": True}
  updated_data["name"] = "Docker"
  updated_data["is_archived"] = False
  resp = client_with_emulator.put(url, params=params, json=updated_data)
  json_response_update_req = resp.json()

  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get(
      "message"
  ) == "Successfully updated the learning experience", \
  "Expected response not same"
  assert json_response_update_req.get("data").get("name") == "Docker"
  assert json_response_update_req.get("data").get("version") == 2


@pytest.mark.parametrize(
    "create_learning_experience", [UPDATE_LEARNING_EXPERIENCE_EXAMPLE],
    indirect=True)
def test_update_learning_experience_negative(clean_firestore,
                                             create_learning_experience):
  learning_experience_dict = copy.deepcopy(UPDATE_LEARNING_EXPERIENCE_EXAMPLE)
  uuid = learning_experience_dict["uuid"] = "U2DDBkl3Ayg0PWudzhI"

  response = {
      "success": False,
      "message": "Learning Experience with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  url = f"{api_url}/{uuid}"
  learning_experience_dict["version"] = 4
  # Negative test when updating the document itself with wrong request body
  params = {"create_version": False}
  resp = client_with_emulator.put(
      url, params=params, json=learning_experience_dict)
  json_response = resp.json()

  assert resp.status_code == 422, "Status code not 422"

  # Negative test when creating version document with wrong request body
  params = {"create_version": True}
  resp = client_with_emulator.put(
      url, params=params, json=learning_experience_dict)
  json_response = resp.json()

  assert resp.status_code == 422, "Status code not 422"

  url = f"{api_url}/{uuid}"
  response = {
      "success": False,
      "message": "Learning Experience with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  # Negative test when updating the document itself with wrong uuid
  params = {"create_version": False}
  DEL_KEYS.append("uuid")
  for key in DEL_KEYS:
    if key in learning_experience_dict:
      del learning_experience_dict[key]
  # del learning_experience_dict["uuid"]
  del learning_experience_dict["resource_path"]
  resp = client_with_emulator.put(
      url, params=params, json=learning_experience_dict)
  json_response = resp.json()
  assert resp.status_code == 404, "Status code not 404"
  assert json_response == response, "Expected response not same"

  # Negative test when creating version document with wrong uuid
  params = {"create_version": True}
  resp = client_with_emulator.put(
      url, params=params, json=learning_experience_dict)
  json_response = resp.json()

  assert resp.status_code == 404, "Status code not 404"
  assert json_response == response, "Expected response not same"


@pytest.mark.parametrize(
    "create_learning_object", [BASIC_LEARNING_OBJECT_EXAMPLE], indirect=True)
def test_delete_learning_experience(clean_firestore, create_learning_object):
  learning_object = create_learning_object

  learning_experience = copy.deepcopy(BASIC_LEARNING_EXPERIENCE_EXAMPLE)
  learning_experience["child_nodes"]["learning_objects"].append(
      learning_object.uuid)

  url = f"{api_url}"
  post_resp = client_with_emulator.post(url, json=learning_experience)
  assert post_resp.status_code == 200, "Status code not 200"
  post_json_response = post_resp.json()
  uuid = post_json_response.get("data").get("uuid")

  # assert the learning object has reference of learning experience in it's
  # parent nodes field
  learning_object = LearningObject.find_by_uuid(learning_object.uuid)
  learning_object_dict = learning_object.to_dict()
  assert uuid in learning_object_dict.get("parent_nodes").get(
      "learning_experiences")

  url = f"{api_url}/{uuid}"
  resp = client_with_emulator.delete(url)
  del_json_response = resp.json()

  expected_data = {
      "success": True,
      "message": "Successfully deleted the learning experience"
  }
  assert resp.status_code == 200, "Status code not 200"
  assert del_json_response == expected_data, "Expected response not same"

  # assert the learning object do not have the reference of learning experience
  # in it's parent nodes field
  learning_object = LearningObject.find_by_uuid(learning_object.uuid)
  learning_object_dict = learning_object.to_dict()
  assert uuid not in learning_object_dict.get("parent_nodes").get(
      "learning_experiences")

  # assert that the learning experience exists in the database and is soft
  # deleted
  learning_experience = LearningExperience.find_by_uuid(uuid, is_deleted=True)
  assert learning_experience


def test_delete_learning_experience_negative(clean_firestore):
  learning_experience_uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{learning_experience_uuid}"
  response = {
      "success": False,
      "message": "Learning Experience with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status code not404"
  assert json_response == response, "Expected response not same"


def test_import_learning_experiences(clean_firestore):
  url = f"{api_url}/import/json"
  with open(
      LEARNING_EXPERIENCES_TESTDATA_FILENAME,
      encoding="UTF-8") as learning_experiences_json_file:
    resp = client_with_emulator.post(
        url, files={"json_file": learning_experiences_json_file})

  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  assert isinstance(json_response.get("data"), list), "Response is not a list"
  assert len(json_response.get("data")) > 0, "Empty list returned"


@pytest.mark.parametrize(
    "create_learning_experience, create_learning_object, \
    create_curriculum_pathway",
    [(BASIC_LEARNING_EXPERIENCE_EXAMPLE, BASIC_LEARNING_OBJECT_EXAMPLE,
      BASIC_CURRICULUM_PATHWAY_EXAMPLE)],
    indirect=True)
def test_get_learning_experiences(clean_firestore, create_learning_experience,
                                  create_learning_object,
                                  create_curriculum_pathway):
  learning_experience = create_learning_experience

  # create an archived object
  archived_learning_experience_dict = copy.deepcopy(
      BASIC_LEARNING_EXPERIENCE_EXAMPLE)
  archived_learning_experience_dict["name"] = "Python"
  archived_learning_experience = LearningExperience.from_dict(
      archived_learning_experience_dict)
  archived_learning_experience.uuid = ""
  archived_learning_experience.save()
  archived_learning_experience.uuid = archived_learning_experience.id
  archived_learning_experience.is_archived = True
  archived_learning_experience.update()

  params = {"skip": 0, "limit": "30"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_names = [i.get("name") for i in json_response.get(
    "data")["records"]]
  assert learning_experience.name in saved_names, "all data not retrived"
  assert archived_learning_experience.name in saved_names, (
      "all data not retrived")

  # Test archival functionality: Fetch all archived objects
  params = {"skip": 0, "limit": "30", "fetch_archive": True}
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_uuids = [i.get("uuid") for i in json_response.get(
    "data")["records"]]
  assert archived_learning_experience.uuid in saved_uuids

  # Test archival functionality: Fetch all non archived objects
  params = {"skip": 0, "limit": "30", "fetch_archive": False}
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_uuids = [i.get("uuid") for i in json_response.get(
    "data")["records"]]
  assert learning_experience.uuid in saved_uuids

  # test get learning experiences with filters
  params = {"skip": 0, "limit": "30", "author": "TestUser"}
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_names = [i.get("author") for i in json_response.get(
    "data")["records"]]
  assert len(list(set(saved_names))) == 1, "Unnecessary data retrieved"
  assert list(set(saved_names))[0] == params["author"], "Wrong data retrieved"

  # test get learning experiences with child node filters
  child_learning_object = create_learning_object
  learning_experience.child_nodes = {
    "learning_objects": [child_learning_object.uuid]}
  learning_experience.update()

  params = {
      "skip": 0,
      "limit": "10",
      "learning_object": child_learning_object.uuid
  }
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_los = [i.get("child_nodes") for i in json_response.get(
    "data")["records"]]
  assert params["learning_object"] in saved_los[0][
      "learning_objects"], "Wrong parent_learning_object retrieved"

  parent_curriculum_pathway = create_curriculum_pathway
  learning_experience.parent_nodes = {
    "curriculum_pathways": [parent_curriculum_pathway.uuid]}
  learning_experience.update()
  params = {
      "skip": 0,
      "limit": "30",
      "curriculum_pathway": parent_curriculum_pathway.uuid
  }
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_cps = [i.get("parent_nodes") for i in json_response.get(
    "data")["records"]]

  assert len(saved_cps) == 1, "Unnecessary data retrieved"
  assert saved_cps[0]["curriculum_pathways"][0] == params[
      "curriculum_pathway"], "Wrong parent_curriculum_pathway retrieved"

  # To-Do: Commenting this code since parent child is not implemented in
  # credentials and pathway service and assessment service
  # params = {
  #     "skip": 0,
  #     "limit": "30",
  #     "author": "TestUser",
  #     "learning_opportunity": "LO_UUID"
  # }
  # url = f"{api_url}s"
  # resp = client_with_emulator.get(url, params=params)
  # json_response = resp.json()
  # assert resp.status_code == 200, "Status code not 200"
  # saved_names = [i.get("author") for i in json_response.get("data")]
  # saved_los = [i.get("parent_nodes") for i in json_response.get("data")]

  # assert len(list(set(saved_names))) == 1, "Unnecessary data retrieved"
  # assert list(
  #     set(saved_names))[0] == params["author"], "Wrong data retrieved"

  # assert len(saved_los) == 1, "Unnecessary data retrieved"
  # assert saved_los[0]["learning_opportunities"][0] == params[
  #     "learning_opportunity"], "Wrong parent_learning_resource retrieved"

  # params = {
  #     "skip": 0,
  #     "limit": "30",
  #     "author": "TestUser",
  #     "assessment": "Assessment_UUID"
  # }
  # url = f"{api_url}s"
  # resp = client_with_emulator.get(url, params=params)
  # json_response = resp.json()
  # assert resp.status_code == 200, "Status code not 200"
  # saved_names = [i.get("author") for i in json_response.get("data")]
  # saved_assessments = [
  #     i.get("child_nodes") for i in json_response.get("data")
  # ]

  # assert len(list(set(saved_names))) == 1, "Unnecessary data retrieved"
  # assert list(
  #     set(saved_names))[0] == params["author"], "Wrong data retrieved"

  # assert len(saved_assessments) == 1, "Unnecessary data retrieved"
  # assert saved_assessments[0]["assessments"][0] == params[
  #     "assessment"], "Wrong parent_assessment retrieved"


@pytest.mark.parametrize(
    "create_learning_experience", [BASIC_LEARNING_EXPERIENCE_EXAMPLE],
    indirect=True)
def test_copy_learning_experience(clean_firestore, create_learning_experience):
  learning_experience_dict = copy.deepcopy(BASIC_LEARNING_EXPERIENCE_EXAMPLE)
  learning_experience = create_learning_experience
  uuid = learning_experience_dict["uuid"] = learning_experience.id

  url = f"{api_url}/copy/{uuid}"
  resp = client_with_emulator.post(url)
  json_response = resp.json()
  DEL_KEYS.append("uuid")
  for key in DEL_KEYS:
    if key in json_response["data"]:
      del json_response["data"][key]
  del learning_experience_dict["uuid"]
  assert resp.status_code == 200, "Status code not 200"
  assert json_response.get(
      "data") == learning_experience_dict, "Response received"
