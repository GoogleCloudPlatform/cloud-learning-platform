"""
  Unit tests for Learning Resource endpoints
"""
import os
import json
import copy
import pytest

# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.learning_resource import router
from testing.test_config import API_URL, TESTING_FOLDER_PATH
from schemas.schema_examples import (BASIC_LEARNING_RESOURCE_EXAMPLE,
                                     BASIC_LEARNING_OBJECT_EXAMPLE)
from common.models import LearningResource, LearningObject
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/learning-object-service/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/learning-resource"
LEARNING_RESOURCE_TESTDATA_FILENAME = os.path.join(TESTING_FOLDER_PATH,
                                                   "learning_resource.json")

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_search_learning_resource(clean_firestore):
  learning_resource_dict = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.update()
  learning_resource_dict["uuid"] = learning_resource.id

  params = {"name": "Text Books"}

  url = f"{api_url}/search"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert json_response.get("data")[0].get(
      "name") == BASIC_LEARNING_RESOURCE_EXAMPLE.get(
          "name"), "Response received"


def test_get_learning_resource(clean_firestore):
  learning_resource_dict = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.update()
  learning_resource_dict["uuid"] = learning_resource.id

  url = f"{api_url}/{learning_resource.uuid}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  del json_response["data"]["created_time"]
  del json_response["data"]["last_modified_time"]
  assert resp.status_code == 200, "Status code not 200"
  assert json_response["data"]["name"] == learning_resource_dict["name"]
  assert json_response["data"]["description"] == \
    learning_resource_dict["description"]


def test_get_learning_resource_negative(clean_firestore):
  uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{uuid}"
  data = {
      "success": False,
      "message": f"Learning Resource with uuid {uuid} not found",
      "data": None
  }

  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 404, "Status 404"
  assert json_response == data, "Response received"


@pytest.mark.parametrize(
    "create_learning_object", [BASIC_LEARNING_OBJECT_EXAMPLE], indirect=True)
def test_post_learning_resource(clean_firestore, create_learning_object):
  learning_object = create_learning_object
  input_learning_resource = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  input_learning_resource["parent_nodes"]["learning_objects"].append(
      learning_object.uuid)

  url = api_url
  if "uuid" in input_learning_resource:
    del input_learning_resource["uuid"]
  post_resp = client_with_emulator.post(url, json=input_learning_resource)
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
  loaded_learning_resource = LearningResource.find_by_uuid(uuid)
  loaded_learning_resource_dict = loaded_learning_resource.to_dict()

  # popping id and key for equivalency test
  loaded_learning_resource_dict.pop("id")
  loaded_learning_resource_dict.pop("key")
  loaded_learning_resource_dict.pop("created_by")
  loaded_learning_resource_dict.pop("created_time")
  loaded_learning_resource_dict.pop("last_modified_by")
  loaded_learning_resource_dict.pop("last_modified_time")
  assert loaded_learning_resource_dict["name"] == \
  post_json_response["data"]["name"]
  assert loaded_learning_resource_dict["description"] == \
    post_json_response["data"]["description"]

  # assert the learning object has reference of learning resource in it's
  # child nodes field
  learning_object = LearningObject.find_by_uuid(learning_object.uuid)
  learning_object_dict = learning_object.to_dict()
  assert uuid in learning_object_dict.get("child_nodes").get(
      "learning_resources")


@pytest.mark.parametrize(
    "create_learning_object", [BASIC_LEARNING_OBJECT_EXAMPLE], indirect=True)
def test_learning_resource_type_check(clean_firestore, create_learning_object):
  input_learning_resource = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  url = api_url
  if "uuid" in input_learning_resource:
    del input_learning_resource["uuid"]

  # [POST] validation failed for resource type
  input_learning_resource["type"] = "some random type"
  post_resp = client_with_emulator.post(url, json=input_learning_resource)
  assert post_resp.status_code == 422, "Status 422"
  assert post_resp.json()["message"] == "Validation Failed"

  # [POST] validation successful for resource type
  input_learning_resource["type"] = "html"
  post_resp = client_with_emulator.post(url, json=input_learning_resource)
  assert post_resp.status_code == 200, "Status 200"

  resource_id = post_resp.json()["data"]["uuid"]

  # [PUT] validation failed for resource type
  input_update_body = {"type": "some random type"}
  put_resp = client_with_emulator.put(
      url + f"/{resource_id}", json=input_update_body)
  assert put_resp.status_code == 422, "Status 422"
  assert put_resp.json()["message"] == "Validation Failed"

  # [PUT] validation successful for resource type
  input_update_body["type"] = "html"
  put_resp = client_with_emulator.put(
      url + f"/{resource_id}", json=input_update_body)
  assert put_resp.status_code == 200, "Status 200"


def test_update_learning_resource(clean_firestore):
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

  learning_resource_dict = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource_dict["parent_nodes"]["learning_objects"].append(
      learning_object_1.uuid)
  learning_resource_dict["parent_nodes"]["learning_objects"].append(
      learning_object_2.uuid)

  url = f"{api_url}"
  post_resp = client_with_emulator.post(url, json=learning_resource_dict)
  assert post_resp.status_code == 200, "Status code not 200"
  post_json_response = post_resp.json()
  uuid = learning_resource_dict["uuid"] = post_json_response.get("data").get(
      "uuid")

  # assert the learning reference has reference of learning object in it's
  # parent nodes field
  learning_object = LearningObject.find_by_uuid(learning_object_1.uuid)
  learning_object_dict = learning_object.to_dict()
  assert uuid in learning_object_dict.get("child_nodes").get(
      "learning_resources")

  learning_object = LearningObject.find_by_uuid(learning_object_2.uuid)
  learning_object_dict = learning_object.to_dict()
  assert uuid in learning_object_dict.get("child_nodes").get(
      "learning_resources")

  updated_data = copy.deepcopy(learning_resource_dict)
  updated_data["name"] = "Quizzes"
  if "uuid" in updated_data:
    del updated_data["uuid"]
  url = f"{api_url}/{uuid}"

  # Test to update the document itself
  params = {"create_version": False}
  resp = client_with_emulator.put(url, params=params, json=updated_data)
  json_response_update_req = resp.json()
  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get(
      "message"
  ) == "Successfully updated the learning resource", \
    "Expected response not same"
  assert json_response_update_req.get("data").get("name") == "Quizzes"

  # Test to verify the parent learning object references are updated
  # assert the learning object has reference of learning object in it's
  # child nodes field
  learning_object = LearningObject.find_by_uuid(learning_object_1.uuid)
  learning_object_dict = learning_object.to_dict()
  assert uuid in learning_object_dict.get("child_nodes").get(
      "learning_resources")

  learning_object = LearningObject.find_by_uuid(learning_object_2.uuid)
  learning_object_dict = learning_object.to_dict()
  assert uuid in learning_object_dict.get("child_nodes").get(
      "learning_resources")

  learning_object = LearningObject.find_by_uuid(learning_object_3.uuid)
  learning_object_dict = learning_object.to_dict()
  assert uuid not in learning_object_dict.get("child_nodes").get(
      "learning_resources")

  # Test to create version when updating document
  params = {"create_version": True}
  updated_data["name"] = "Algebra"
  resp = client_with_emulator.put(url, params=params, json=updated_data)
  json_response_update_req = resp.json()

  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get("message") == \
    "Successfully updated the learning resource", "Expected response not same"
  assert json_response_update_req.get("data").get("name") == "Algebra"
  assert json_response_update_req.get("data").get("version") == 2


def test_update_learning_resource_negative(clean_firestore):
  learning_resource_dict = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  url = api_url
  create_resp = json.loads(
      client_with_emulator.post(url, json=learning_resource_dict).text)
  uuid = "U2DDBkl3Ayg0PWudzhI"

  response = {
      "success": False,
      "message": "Learning Resource with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }

  url = f"{api_url}/{uuid}"

  # Negative test when updating the document itself with wrong uuid
  params = {"create_version": False}
  # del learning_resource_dict["uuid"]
  resp = client_with_emulator.put(
      url, params=params, json=learning_resource_dict)
  json_response = resp.json()
  assert resp.status_code == 404, "Status code not 404"
  assert json_response == response, "Expected response not same"

  # Negative test when creating the version document with wrong uuid
  params = {"create_version": True}
  resp = client_with_emulator.put(
      url, params=params, json=learning_resource_dict)
  json_response = resp.json()

  assert resp.status_code == 404, "Status code not 404"
  assert json_response == response, "Expected response not same"

  url = f"{api_url}/{create_resp.get('data').get('uuid')}"
  learning_resource_dict["uuid"] = "random_id"
  # Negative test when updating the document itself with wrong request body
  params = {"create_version": False}
  resp = client_with_emulator.put(
      url, params=params, json=learning_resource_dict)
  json_response = resp.json()

  assert resp.status_code == 422, "Status code not 422"

  # Negative test when creating the version document with wrong request body
  params = {"create_version": True}
  resp = client_with_emulator.put(
      url, params=params, json=learning_resource_dict)
  json_response = resp.json()

  assert resp.status_code == 422, "Status code not 422"


@pytest.mark.parametrize(
    "create_learning_object", [BASIC_LEARNING_OBJECT_EXAMPLE], indirect=True)
def test_delete_learning_resource(clean_firestore, create_learning_object):
  learning_object = create_learning_object

  learning_resource = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource["parent_nodes"]["learning_objects"].append(
      learning_object.uuid)

  url = f"{api_url}"
  post_resp = client_with_emulator.post(url, json=learning_resource)
  assert post_resp.status_code == 200, "Status code not 200"
  post_json_response = post_resp.json()
  uuid = post_json_response.get("data").get("uuid")

  # assert the learning object has reference of learning object in it's
  # child nodes field
  learning_object = LearningObject.find_by_uuid(learning_object.uuid)
  learning_object_dict = learning_object.to_dict()
  assert uuid in learning_object_dict.get("child_nodes").get(
      "learning_resources")

  url = f"{api_url}/{uuid}"
  resp = client_with_emulator.delete(url)
  del_json_response = resp.json()

  expected_data = {
      "success": True,
      "message": "Successfully deleted the learning resource"
  }
  assert resp.status_code == 200, "Status code not 200"
  assert del_json_response == expected_data, "Expected response not same"

  # assert the learning object do not have the reference of learning resource
  # in it's child nodes field
  learning_object = LearningObject.find_by_uuid(learning_object.uuid)
  learning_object_dict = learning_object.to_dict()
  assert uuid not in learning_object_dict.get("child_nodes").get(
      "learning_resources")

  # assert that the learning object exists in the database and is soft
  # deleted
  learning_resource = LearningResource.find_by_uuid(uuid, is_deleted=True)
  assert learning_resource


def test_delete_learning_resource_negative(clean_firestore):
  learning_resource_uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{learning_resource_uuid}"
  response = {
      "success": False,
      "message": "Learning Resource with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"

  learning_resource_dict = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.update()


def test_import_learning_resources(clean_firestore):
  url = f"{api_url}/import/json"
  with open(
      LEARNING_RESOURCE_TESTDATA_FILENAME,
      encoding="UTF-8") as learning_resources_json_file:
    resp = client_with_emulator.post(
        url, files={"json_file": learning_resources_json_file})

  json_response = resp.json()
  assert resp.status_code == 200, "Status not 200"
  assert isinstance(json_response.get("data"), list), "Response is not a list"
  assert len(json_response.get("data")) > 0, "Empty list returned"


def test_get_learning_resources(clean_firestore):
  learning_resource_dict = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource_dict["name"] = "Text Books"
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.update()
  params = {"skip": 0, "limit": "30"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  saved_names = [i.get("name") for i in json_response.get("data")]
  assert learning_resource_dict["name"] in saved_names, "all data not retrieved"


def test_get_learning_resources_with_filters(clean_firestore):
  learning_resource_dict = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.update()
  params = {
      "skip": 0,
      "limit": "30",
      "type": "video",
      "course_category": "Testing category"
  }

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert len(json_response.get("data")) != 0
  for lr_data in json_response.get("data"):
    assert lr_data.get("type") == params["type"], "filter not working properly"
    assert lr_data.get("course_category")[0] == params["course_category"],\
      "filter not working properly"

  params = {"skip": 0, "limit": "30", "type": "video", "version": 1}
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert len(json_response.get("data")) != 0
  saved_types = [i.get("type") for i in json_response.get("data")]
  saved_versions = [i.get("version") for i in json_response.get("data")]
  assert len(list(set(saved_types))) == 1, "Unnecessary type retrieved"
  assert list(set(saved_types))[0] == params["type"], "Wrong type retrieved"
  assert len(list(set(saved_versions))) == 1, "Unnecessary versions retrieved"
  assert list(
      set(saved_versions))[0] == params["version"], "Wrong version retrieved"

  params = {"skip": 0, "limit": "30", "fetch_archive": True}

  learning_resource.is_archived = True
  learning_resource.update()
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert len(json_response.get("data")) != 0
  saved_archived_flags = [
      i.get("is_archived") for i in json_response.get("data")
  ]
  assert list(
      set(saved_archived_flags))[0] == params["fetch_archive"],\
        "Wrong is_archived flag retrieved"

  params = {
      "skip": 0,
      "limit": "30",
      "name": "Text Books",
  }
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert len(json_response.get("data")) != 0
  saved_name = [i.get("name") for i in json_response.get("data")]
  assert len(list(set(saved_name))) == 1, "Unnecessary name retrieved"
  assert list(set(saved_name))[0] == params["name"], "Wrong name retrieved"


def test_get_learning_resources_with_filters_negative(clean_firestore):
  learning_resource_dict = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource_dict["type"] = "pdf"
  learning_resource_dict["course_category"] = ["biology"]
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.update()
  params = {
      "skip": "-1",
      "limit": "30",
      "type": "pdf",
      "course_category": "biology"
  }

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422, "Status not 422"
  assert json_response.get(
      "message"
  ) == "Validation Failed", \
    "unknown response received"

def test_copy_learning_resrouce(clean_firestore):
  learning_resource_dict = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.update()
  uuid = learning_resource_dict["uuid"] = learning_resource.id

  url = f"{api_url}/copy/{uuid}"
  resp = client_with_emulator.post(url)
  json_response = resp.json()
  del json_response["data"]["created_time"]
  del json_response["data"]["last_modified_time"]
  del json_response["data"]["uuid"]
  del learning_resource_dict["uuid"]
  assert resp.status_code == 200, "Status code not 200"
  assert json_response["data"]["name"] == learning_resource_dict["name"]
  assert json_response["data"]["description"] == \
    learning_resource_dict["description"]
