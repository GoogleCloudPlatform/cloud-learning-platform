"""
  Unit tests for Learning Object endpoints
"""
import os
import copy
import json
import pytest
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.learning_object import router
from schemas.schema_examples import (BASIC_LEARNING_OBJECT_EXAMPLE,
                                     UPDATE_LEARNING_OBJECT_EXAMPLE,
                                     BASIC_LEARNING_EXPERIENCE_EXAMPLE)
from testing.test_config import (API_URL, TESTING_FOLDER_PATH)
from common.models import LearningObject, LearningExperience
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/learning-object-service/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/learning-object"
LEARNING_OBJECTS_TESTDATA_FILENAME = os.path.join(TESTING_FOLDER_PATH,
                                                  "learning_objects.json")

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


@pytest.mark.parametrize(
    "create_learning_object", [BASIC_LEARNING_OBJECT_EXAMPLE], indirect=True)
def test_search_learning_object(clean_firestore, create_learning_object):
  learning_object_dict = copy.deepcopy(BASIC_LEARNING_OBJECT_EXAMPLE)
  learning_object = create_learning_object
  learning_object_dict["uuid"] = learning_object.id
  params = {"name": "Online presentation"}

  url = f"{api_url}/search"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  keys_to_delete = [
      "version", "is_archived", "root_version_uuid", "parent_version_uuid",
      "created_time", "last_modified_time"
  ]
  for key in keys_to_delete:
    del json_response["data"][0][key]
  assert resp.status_code == 200, "Status code not 200"
  assert json_response.get("data") == [learning_object_dict]

  #Checking for deleted learning object
  learning_object_dict = copy.deepcopy(BASIC_LEARNING_OBJECT_EXAMPLE)
  learning_object_dict["name"] = "Kubernetes Container Orchestration"
  learning_object = LearningObject.from_dict(learning_object_dict)
  learning_object.uuid = ""
  learning_object.save()
  learning_object.is_deleted = True
  learning_object.uuid = learning_object.id
  learning_object.update()
  learning_object_dict["uuid"] = learning_object.id

  params = {"name": "Kubernetes Container Orchestration"}
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert len(json_response.get("data")) == 0


@pytest.mark.parametrize(
    "create_learning_object", [BASIC_LEARNING_OBJECT_EXAMPLE], indirect=True)
def test_get_learning_object(clean_firestore, create_learning_object):
  learning_object_dict = copy.deepcopy(BASIC_LEARNING_OBJECT_EXAMPLE)
  learning_object = create_learning_object
  learning_object_dict["uuid"] = learning_object.id

  # fetch only the document with given uuid
  url = f"{api_url}/{learning_object.uuid}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  keys_to_delete = [
      "version", "is_archived", "root_version_uuid", "parent_version_uuid",
      "created_time", "last_modified_time"
  ]
  for key in keys_to_delete:
    del json_response["data"][key]
  assert resp.status_code == 200, "Status code not 200"
  assert json_response.get("data") == learning_object_dict,\
    "Response received"


def test_get_learning_object_negative(clean_firestore):
  uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{uuid}"
  data = {
      "success": False,
      "message": f"Learning Object with uuid {uuid} not found",
      "data": None
  }

  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 404, "Status code not 404"
  assert json_response == data, "Response received"


@pytest.mark.parametrize(
    "create_learning_experience", [BASIC_LEARNING_EXPERIENCE_EXAMPLE],
    indirect=True)
def test_post_learning_object(clean_firestore, create_learning_experience):
  learning_experience = create_learning_experience
  input_learning_object = copy.deepcopy(BASIC_LEARNING_OBJECT_EXAMPLE)
  input_learning_object["parent_nodes"]["learning_experiences"].append(
      learning_experience.uuid)

  url = api_url
  post_resp = client_with_emulator.post(url, json=input_learning_object)
  assert post_resp.status_code == 200, "Status code not 200"

  post_json_response = post_resp.json()
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

  # now check and confirm it is properly in the database
  loaded_learning_object = LearningObject.find_by_uuid(uuid)
  loaded_learning_object_dict = loaded_learning_object.to_dict()

  # popping id and key for equivalency test
  keys_to_delete = [
      "id", "key", "is_deleted", "created_by", "created_time",
      "last_modified_by", "last_modified_time"
  ]
  for key in keys_to_delete:
    loaded_learning_object_dict.pop(key)

  # assert that rest of the fields are equivalent
  assert loaded_learning_object_dict == post_json_response.get("data")

  # assert the learning experience has reference of learning object in it's
  # child nodes field
  learning_experience = LearningExperience.find_by_uuid(
      learning_experience.uuid)
  learning_experience_dict = learning_experience.to_dict()
  assert uuid in learning_experience_dict.get("child_nodes").get(
      "learning_objects")


def test_update_learning_object(clean_firestore):
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

  learning_object_dict = copy.deepcopy(BASIC_LEARNING_OBJECT_EXAMPLE)
  learning_object_dict["parent_nodes"]["learning_experiences"].append(
      learning_experience_1.uuid)
  learning_object_dict["parent_nodes"]["learning_experiences"].append(
      learning_experience_2.uuid)

  url = f"{api_url}"
  post_resp = client_with_emulator.post(url, json=learning_object_dict)
  assert post_resp.status_code == 200, "Status code not 200"
  post_json_response = post_resp.json()
  uuid = learning_object_dict["uuid"] = post_json_response.get("data").get(
      "uuid")

  # assert the learning object has reference of learning experience in it's
  # parent nodes field
  learning_experience = LearningExperience.find_by_uuid(
      learning_experience_1.uuid)
  learning_experience_dict = learning_experience.to_dict()
  assert uuid in learning_experience_dict.get("child_nodes").get(
      "learning_objects")

  learning_experience = LearningExperience.find_by_uuid(
      learning_experience_2.uuid)
  learning_experience_dict = learning_experience.to_dict()
  assert uuid in learning_experience_dict.get("child_nodes").get(
      "learning_objects")

  updated_data = copy.deepcopy(learning_object_dict)
  updated_data["name"] = "Quizzes"
  updated_data["is_archived"] = False
  updated_data["parent_nodes"]["learning_experiences"].append(
      learning_experience_3.uuid)
  updated_data["parent_nodes"]["learning_experiences"].remove(
      learning_experience_1.uuid)

  url = f"{api_url}/{uuid}"

  # Test to update the document itself
  params = {"create_version": False}
  del updated_data["uuid"]
  resp = client_with_emulator.put(url, params=params, json=updated_data)
  json_response_update_req = resp.json()
  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get(
      "message"
  ) == "Successfully updated the learning object", "Expected response not same"
  assert json_response_update_req.get("data").get("name") == "Quizzes"

  # Test to verify the parent learning experience references are updated
  # assert the learning experience has reference of learning object in it's
  # child nodes field
  learning_experience = LearningExperience.find_by_uuid(
      learning_experience_1.uuid)
  learning_experience_dict = learning_experience.to_dict()
  assert uuid not in learning_experience_dict.get("child_nodes").get(
      "learning_objects")

  learning_experience = LearningExperience.find_by_uuid(
      learning_experience_2.uuid)
  learning_experience_dict = learning_experience.to_dict()
  assert uuid in learning_experience_dict.get("child_nodes").get(
      "learning_objects")

  learning_experience = LearningExperience.find_by_uuid(
      learning_experience_3.uuid)
  learning_experience_dict = learning_experience.to_dict()
  assert uuid in learning_experience_dict.get("child_nodes").get(
      "learning_objects")

  # Test to create version when updating document
  params = {"create_version": True}
  updated_data["name"] = "Algebra"
  updated_data["is_archived"] = False
  resp = client_with_emulator.put(url, params=params, json=updated_data)
  json_response_update_req = resp.json()

  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get("message") == \
    "Successfully updated the learning object", "Expected response not same"
  assert json_response_update_req.get("data").get("name") == "Algebra"
  assert json_response_update_req.get("data").get("version") == 2


@pytest.mark.parametrize(
    "create_learning_object", [UPDATE_LEARNING_OBJECT_EXAMPLE], indirect=True)
def test_update_learning_object_negative(clean_firestore,
                                         create_learning_object):
  learning_object_dict = copy.deepcopy(UPDATE_LEARNING_OBJECT_EXAMPLE)
  uuid = learning_object_dict["uuid"] = "U2DDBkl3Ayg0PWudzhI"

  response = {
      "success": False,
      "message": "Learning Object with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }

  url = f"{api_url}/{uuid}"

  # Negative test when updating the document itself with wrong uuid
  params = {"create_version": False}
  del learning_object_dict["uuid"]
  resp = client_with_emulator.put(url, params=params, json=learning_object_dict)
  json_response = resp.json()
  assert resp.status_code == 404, "Status code not 404"
  assert json_response == response, "Expected response not same"

  # Negative test when creating the version document with wrong uuid
  params = {"create_version": True}
  resp = client_with_emulator.put(url, params=params, json=learning_object_dict)
  json_response = resp.json()

  assert resp.status_code == 404, "Status code not 404"
  assert json_response == response, "Expected response not same"

  url = f"{api_url}/{uuid}"
  learning_object_dict["uuid"] = "random_id"
  # Negative test when updating the document itself with wrong request body
  params = {"create_version": False}
  resp = client_with_emulator.put(url, params=params, json=learning_object_dict)
  json_response = resp.json()

  assert resp.status_code == 422, "Status code not 422"

  # Negative test when creating the version document with wrong request body
  params = {"create_version": True}
  resp = client_with_emulator.put(url, params=params, json=learning_object_dict)
  json_response = resp.json()

  assert resp.status_code == 422, "Status code not 422"


@pytest.mark.parametrize(
    "create_learning_experience", [BASIC_LEARNING_EXPERIENCE_EXAMPLE],
    indirect=True)
def test_delete_learning_object(clean_firestore, create_learning_experience):
  learning_experience = create_learning_experience

  learning_object_1 = copy.deepcopy(BASIC_LEARNING_OBJECT_EXAMPLE)
  learning_object_1["parent_nodes"]["learning_experiences"].append(
      learning_experience.uuid)

  url = f"{api_url}"
  post_resp = client_with_emulator.post(url, json=learning_object_1)
  assert post_resp.status_code == 200, "Status code not 200"
  post_json_response = post_resp.json()
  uuid = post_json_response.get("data").get("uuid")

  learning_object_2 = copy.deepcopy(BASIC_LEARNING_OBJECT_EXAMPLE)
  learning_object_2["prerequisites"]["learning_objects"] = [uuid]
  post_resp = client_with_emulator.post(url, json=learning_object_2)
  assert post_resp.status_code == 200, "Status code not 200"
  post_json_response = post_resp.json()
  lo_2_uuid = post_json_response.get("data").get("uuid")

  # assert the learning experience has reference of learning object in it's
  # child nodes field
  learning_experience = LearningExperience.find_by_uuid(
      learning_experience.uuid)
  learning_experience_dict = learning_experience.to_dict()
  assert uuid in learning_experience_dict.get("child_nodes").get(
      "learning_objects")

  url = f"{api_url}/{uuid}"
  resp = client_with_emulator.delete(url)
  del_json_response = resp.json()

  expected_data = {
      "success": True,
      "message": "Successfully deleted the learning object"
  }
  assert resp.status_code == 200, "Status code not 200"
  assert del_json_response == expected_data, "Expected response not same"

  # assert the learning experience do not have the reference of learning object
  # in it's child nodes field
  learning_experience = LearningExperience.find_by_uuid(
      learning_experience.uuid)
  learning_experience_dict = learning_experience.to_dict()
  assert uuid not in learning_experience_dict.get("child_nodes").get(
      "learning_objects")

  # check if deleted LO was removed from other LO's prerequisites
  lo_2 = LearningObject.find_by_uuid(lo_2_uuid)
  assert uuid not in lo_2.prerequisites["learning_objects"]

  # assert that the learning object exists in the database and is soft
  # deleted
  learning_object = LearningObject.find_by_uuid(uuid, is_deleted=True)
  assert learning_object


def test_delete_learning_object_negative(clean_firestore):
  learning_object_uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{learning_object_uuid}"
  response = {
      "success": False,
      "message": "Learning Object with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status code not 404"
  assert json_response == response, "Expected response not same"


def test_import_learning_objects(clean_firestore):
  url = f"{api_url}/import/json"
  with open(
      LEARNING_OBJECTS_TESTDATA_FILENAME,
      encoding="UTF-8") as learning_objects_json_file:
    resp = client_with_emulator.post(
        url, files={"json_file": learning_objects_json_file})

  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  assert isinstance(json_response.get("data"), list), "Response is not a list"
  assert len(json_response.get("data")) > 0, "Empty list returned"


@pytest.mark.parametrize(
    "create_learning_object, create_learning_experience",
    [(BASIC_LEARNING_OBJECT_EXAMPLE, BASIC_LEARNING_EXPERIENCE_EXAMPLE)],
    indirect=True)
def test_get_learning_objects(clean_firestore, create_learning_object,
                              create_learning_experience):
  learning_object_dict = copy.deepcopy(BASIC_LEARNING_OBJECT_EXAMPLE)
  learning_object = create_learning_object

  # create an archived object
  archived_learning_object_dict = copy.deepcopy(BASIC_LEARNING_OBJECT_EXAMPLE)
  archived_learning_object_dict["name"] = "Dialogue simulations"
  archived_learning_object = LearningObject.from_dict(
      archived_learning_object_dict)
  archived_learning_object.uuid = ""
  archived_learning_object.save()
  archived_learning_object.uuid = archived_learning_object.id
  archived_learning_object.is_archived = True
  archived_learning_object.update()

  params = {"skip": 0, "limit": "30"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_names = [i.get("name") for i in json_response.get("data")]
  assert learning_object_dict["name"] in saved_names, "all data not retrived"
  assert archived_learning_object.name in saved_names, "all data not retrived"

  # Test archival functionality: Fetch all archived objects
  params = {"skip": 0, "limit": "30", "fetch_archive": True}
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_uuids = [i.get("uuid") for i in json_response.get("data")]
  assert archived_learning_object.uuid in saved_uuids

  # Test archival functionality: Fetch all non archived objects
  params = {"skip": 0, "limit": "30", "fetch_archive": False}
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_uuids = [i.get("uuid") for i in json_response.get("data")]
  assert learning_object.uuid in saved_uuids

  params = {"skip": 0, "limit": "30", "author": "TestUser"}
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_names = [i.get("author") for i in json_response.get("data")]

  assert len(list(set(saved_names))) == 1, "Unnecessary data retrieved"
  assert list(set(saved_names))[0] == params["author"], "Wrong data retrieved"

  parent_learning_object_dict = copy.deepcopy(BASIC_LEARNING_OBJECT_EXAMPLE)
  parent_learning_object_dict["name"] = "Offline presentation"

  parent_learning_object = create_learning_object
  learning_object.parent_nodes["learning_objects"].append(
      parent_learning_object.uuid)
  learning_object.update()

  params = {
      "skip": 0,
      "limit": "30",
      "learning_object": parent_learning_object.uuid,
      "relation": "parent"
  }
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_los = [
      i.get(f"{params['relation']}_nodes") for i in json_response.get("data")
  ]

  assert params["learning_object"] in saved_los[0][
      "learning_objects"], "Wrong parent_learning_object retrieved"

  child_learning_object_dict = copy.deepcopy(BASIC_LEARNING_OBJECT_EXAMPLE)
  child_learning_object_dict["name"] = "Online report presentation"

  child_learning_object = create_learning_object

  learning_object.child_nodes["learning_objects"].append(
      child_learning_object.uuid)
  learning_object.update()

  params = {
      "skip": 0,
      "limit": "30",
      "learning_object": child_learning_object.uuid,
      "relation": "child"
  }
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_los = [
      i.get(f"{params['relation']}_nodes") for i in json_response.get("data")
  ]
  assert params["learning_object"] in saved_los[0][
      "learning_objects"], "Wrong parent_learning_object retrieved"

  parent_learning_experience = create_learning_experience
  learning_object.parent_nodes["learning_experiences"].append(
      parent_learning_experience.uuid)
  learning_object.update()

  params = {
      "skip": 0,
      "limit": "30",
      "learning_experience": parent_learning_experience.uuid
  }
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_les = [i.get("parent_nodes") for i in json_response.get("data")]
  assert params["learning_experience"] in saved_les[0][
      "learning_experiences"], "Wrong parent_learning_experience retrieved"


# To-Do: Commenting this code since parent child is not implemented in
# learning resource
# params = {
#     "skip": 0,
#     "limit": "30",
#     "author": "TestUser",
#     "learning_resource": "LR_UUID"
# }
# url = f"{api_url}s"
# resp = client_with_emulator.get(url, params=params)
# json_response = resp.json()
# assert resp.status_code == 200, "Status code not 200"
# saved_names = [i.get("author") for i in json_response.get("data")]
# saved_lrs = [i.get("child_nodes") for i in json_response.get("data")]

# assert len(list(set(saved_names))) == 1, "Unnecessary data retrieved"
# assert list(set(saved_names))[0] == params["author"], "Wrong data retrieved"

# assert len(saved_lrs) == 1, "Unnecessary data retrieved"
# assert saved_lrs[0]["learning_resources"][0] == params[
#     "learning_resource"], "Wrong parent_learning_resource retrieved"

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
# assert list(set(saved_names))[0] == params["author"], "Wrong data retrieved"

# assert len(saved_assessments) == 1, "Unnecessary data retrieved"
# assert saved_assessments[0]["assessments"][0] == params[
#     "assessment"], "Wrong parent_assessment retrieved"


@pytest.mark.parametrize(
    "create_learning_object", [BASIC_LEARNING_OBJECT_EXAMPLE], indirect=True)
def test_copy_learning_object(clean_firestore, create_learning_object):
  learning_object_dict = copy.deepcopy(BASIC_LEARNING_OBJECT_EXAMPLE)
  learning_object = create_learning_object
  uuid = learning_object_dict["uuid"] = learning_object.id
  url = f"{api_url}/copy/{uuid}"
  resp = client_with_emulator.post(url)
  json_response = resp.json()
  keys_to_delete = [
      "version", "is_archived", "root_version_uuid", "parent_version_uuid",
      "created_time", "last_modified_time", "uuid"
  ]
  for key in keys_to_delete:
    del json_response["data"][key]
  del learning_object_dict["uuid"]
  assert resp.status_code == 200, "Status code not 200"
  assert json_response.get("data") == learning_object_dict, "Response received"
