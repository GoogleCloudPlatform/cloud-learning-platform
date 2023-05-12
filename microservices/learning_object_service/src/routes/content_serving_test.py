"""
  Unit tests for Content Serving endpoints
"""
import os
import pytest
import copy
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
# disabling pylint rules for create learning content long urls and file handling
# pylint: disable = unspecified-encoding
# pylint: disable = consider-using-with
# pylint: disable = line-too-long

from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest import mock
with mock.patch("kubernetes.config", side_effect=mock.MagicMock()) as mok:
  with mock.patch("google.cloud.logging.Client",side_effect=mock.MagicMock()) as mok2:
    from routes.content_serving import router
    from routes.learning_resource import router as router_2
    from routes.curriculum_pathway import router as router_3
from testing.test_config import (API_URL, TESTING_FOLDER_PATH)
from common.models import (LearningResource,
                            LearningObject,
                            LearningExperience)
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers
from schemas.schema_examples import (BASIC_LEARNING_RESOURCE_EXAMPLE,
                                     BASIC_LEARNING_OBJECT_EXAMPLE,
                                     BASIC_LEARNING_EXPERIENCE_EXAMPLE)
from services.helper import get_all_nodes_for_alias

SRL_PATHWAY = os.path.join(TESTING_FOLDER_PATH,
                           "content_serving/hierarchy_for_srl.json")

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/learning-object-service/api/v1")

app_2 = FastAPI()
add_exception_handlers(app_2)
app_2.include_router(router_2, prefix="/learning-object-service/api/v1")

app_3 = FastAPI()
add_exception_handlers(app_3)
app_3.include_router(router_3, prefix="/learning-object-service/api/v1")

client_with_emulator = TestClient(app)
client_with_emulator_2 = TestClient(app_2)
client_with_emulator_3 = TestClient(app_3)

# assigning url
api_url = f"{API_URL}/content-serving"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


class GcsCrudService:
  """
    Mock class for GCSCrudService
  """

  def __init__(self, bucket_name):
    self.bucket_name = bucket_name

  def generate_url(self, prefix, expiration):
    self.prefix = prefix
    return "signed_url_dummy"

  def get_bucket_folders(self, prefix, delimiter="/"):
    return ["folder 1", "folder 2"]

  def get_files_from_folder(self, prefix, delimiter="/"):
    return ["file_1.txt", "file_2.txt", "file_3.txt"]


class FileUtils:
  """
        Mock class for FileUtils
    """

  def __init__(self):
    pass

  def getContentFolderFiles(self, folder_path, list_madcap_contents=False):
    return ["abc"]


# Generate Signed URL API Test
#------------------------------------------------
@pytest.mark.parametrize(
    "create_learning_resource", [{
        **BASIC_LEARNING_RESOURCE_EXAMPLE, "resource_path": "dummy_path"
    }],
    indirect=True)
def test_generate_sign_url_positive_1(clean_firestore, create_learning_resource,
                                      mocker):
  """
    Scenario: Successful Generation of signed URL with JSON response
  """
  mocker.patch(
      "routes.content_serving.GcsCrudService",
      return_value=GcsCrudService("GCP_LEARNING_RESOURCE_BUCKET"))
  mocker.patch("routes.content_serving.is_valid_path", return_value=True)

  learning_resource = create_learning_resource

  url = f"{api_url}/{learning_resource.id}?redirect=false"
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  assert resp.status_code == 200, "Status code not 200"
  assert json_response["data"]["signed_url"] == "signed_url_dummy"
  assert json_response["data"][
      "resource_type"] == BASIC_LEARNING_RESOURCE_EXAMPLE["type"]


@pytest.mark.parametrize(
    "create_learning_resource", [{
        **BASIC_LEARNING_RESOURCE_EXAMPLE, "resource_path": "dummy_path"
    }],
    indirect=True)
def test_generate_sign_url_positive_2(clean_firestore, create_learning_resource,
                                      mocker):
  """
    Scenario: Successful Generation of signed URL with Redirect Response
  """
  mocker.patch(
      "routes.content_serving.GcsCrudService",
      return_value=GcsCrudService("GCP_LEARNING_RESOURCE_BUCKET"))
  mocker.patch("routes.content_serving.is_valid_path", return_value=True)

  learning_resource = create_learning_resource

  url = f"{api_url}/{learning_resource.id}"
  resp = client_with_emulator.get(
      url, params={"redirect": True}, allow_redirects=False)
  assert resp.status_code == 307, "Status code not 200"


def test_generate_sign_url_negative(clean_firestore, mocker):
  """
    Scenario: Learning Resource does not exist in firestore
  """
  random_uuid = "gh657576xfdgfdf"

  url = f"{api_url}/{random_uuid}?redirect=false"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 404, "Status code not 200"
  assert json_response[
      "message"] == f"Learning Resource with uuid {random_uuid} not found"


@pytest.mark.parametrize(
    "create_learning_resource", [{
        **BASIC_LEARNING_RESOURCE_EXAMPLE, "type": "",
        "resource_path": "video.mp4"
    }],
    indirect=True)
def test_generate_sign_url_negative_2(clean_firestore, create_learning_resource,
                                      mocker):
  """
    Scenario: resource_path is empty for given learning resource
  """
  mocker.patch(
      "routes.content_serving.GcsCrudService",
      return_value=GcsCrudService("GCP_LEARNING_RESOURCE_BUCKET"))
  mocker.patch("routes.content_serving.is_valid_path", return_value=True)

  learning_resource = create_learning_resource

  url = f"{api_url}/{learning_resource.id}?redirect=false"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 404, "Status code not 200"

  assertion_str = "No resource type found for resource with uuid "
  assertion_str += learning_resource.id

  assert json_response["message"] == assertion_str


@pytest.mark.parametrize(
    "create_learning_resource", [BASIC_LEARNING_RESOURCE_EXAMPLE],
    indirect=True)
def test_generate_sign_url_negative_3(clean_firestore, create_learning_resource,
                                      mocker):
  """
    Scenario: resource_path is empty for given learning resource
  """
  mocker.patch(
      "routes.content_serving.GcsCrudService",
      return_value=GcsCrudService("GCP_LEARNING_RESOURCE_BUCKET"))
  mocker.patch("routes.content_serving.is_valid_path", return_value=True)

  learning_resource = create_learning_resource

  url = f"{api_url}/{learning_resource.id}?redirect=false"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 404, "Status code not 200"

  assertion_str = "No resource path found for resource with uuid "
  assertion_str += learning_resource.id

  assert json_response["message"] == assertion_str


@pytest.mark.parametrize(
    "create_learning_resource", [{
        **BASIC_LEARNING_RESOURCE_EXAMPLE, "resource_path": "dummy_path"
    }],
    indirect=True)
def test_generate_sign_url_negative_4(clean_firestore, create_learning_resource,
                                      mocker):
  """
    Scenario: Given resource path does not exist on GCS bucket
  """
  mocker.patch(
      "routes.content_serving.GcsCrudService",
      return_value=GcsCrudService("GCP_LEARNING_RESOURCE_BUCKET"))
  mocker.patch("routes.content_serving.is_valid_path", return_value=False)

  learning_resource = create_learning_resource

  url = f"{api_url}/{learning_resource.id}?redirect=false"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 404, "Status code not 404"
  assert json_response[
      "message"] == "Provided resource path does not exist on GCS bucket"


# Disabled: Link Content to Learning Resource
#------------------------------------------------
def link_content_and_create_version_positive(clean_firestore, mocker):
  """
    Positive Scenarios
    1. Cold start - LR is connected to Hierarchy but it doesn"t have
                    resource_path
    2. Generic case - LR with resource_path already exists and a new
                    document should be created
  """
  mocker.patch(
      "routes.content_serving.GcsCrudService",
      return_value=GcsCrudService("GCP_LEARNING_RESOURCE_BUCKET"))
  mocker.patch(
      "services.content_version_handler.is_valid_path", return_value=True)

  # Scenario 1: Cold Start
  learning_resource_dict = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.type = ""
  learning_resource.resource_path = ""
  learning_resource.status = "initial"
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.update()
  learning_resource_dict["uuid"] = learning_resource.id
  parent_uuid = learning_resource.id

  sample_resource_path = "sample/resource/path"

  res = client_with_emulator.put(
      url=f"{api_url}/link/{learning_resource.uuid}",
      json={
          "resource_path": sample_resource_path,
          "type": "docx"
      })
  res_json = res.json()

  assert res.status_code == 200
  assert res_json["success"] is True
  assert res_json[
      "message"] == "Successfully linked learning resource with content"

  new_resource_uuid = res_json["data"]["resource_uuid"]
  assert new_resource_uuid != learning_resource.uuid

  learning_resource = LearningResource.find_by_id(new_resource_uuid)
  assert learning_resource.resource_path == sample_resource_path
  assert learning_resource.status == "draft"
  assert learning_resource.parent_version_uuid == parent_uuid

  # Scenario 2: Generic Case
  res = client_with_emulator.put(
      url=f"{api_url}/link/{learning_resource.uuid}",
      json={
          "resource_path": sample_resource_path,
          "type": "docx"
      })
  res_json = res.json()

  assert res.status_code == 200
  assert res_json["success"] is True
  assert res_json[
      "message"] == "Successfully linked learning resource with content"

  new_resource_uuid_2 = res_json["data"]["resource_uuid"]
  assert new_resource_uuid_2 != new_resource_uuid

  learning_resource = LearningResource.find_by_id(new_resource_uuid_2)
  assert learning_resource.resource_path == sample_resource_path
  assert learning_resource.status == "draft"
  assert learning_resource.parent_version_uuid == new_resource_uuid


def link_content_and_create_version_negative(clean_firestore, mocker):
  """
        Negative Scenarios:
        1. Invalid LR uuid
        2. Validation Error: resource_type not allowed
        3. Resource Not Found: resource path does not exist on GCS bucket
  """
  mocker.patch(
      "routes.content_serving.GcsCrudService",
      return_value=GcsCrudService("GCP_LEARNING_RESOURCE_BUCKET"))
  mocker.patch(
      "services.content_version_handler.is_valid_path", return_value=True)

  # 1. Invalid LR uuid
  random_lr_uuid = "random_lr_uuid"
  sample_resource_path = "sample/resource/path"

  res = client_with_emulator.put(
      url=f"{api_url}/link/{random_lr_uuid}",
      json={
          "resource_path": sample_resource_path,
          "type": "docx"
      })
  res_json = res.json()

  assert res.status_code == 404
  assert res_json["success"] is False
  assert res_json[
      "message"] == f"Learning Resource with uuid {random_lr_uuid} not found"

  # 2. Validation Error: invalid resource_type
  learning_resource_dict = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.type = ""
  learning_resource.resource_path = ""
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.update()
  learning_resource_dict["uuid"] = learning_resource.id

  sample_resource_path = "sample/resource/path"
  sample_resource_type = "random_resource_type"

  res = client_with_emulator.put(
      url=f"{api_url}/link/{learning_resource.uuid}",
      json={
          "resource_path": sample_resource_path,
          "type": sample_resource_type
      })
  res_json = res.json()

  assert res.status_code == 422
  assert res_json["success"] is False
  assert res_json["message"] == "Validation Failed"

  #3. Validation Error: Resource path not found on GCS
  mocker.patch(
      "services.content_version_handler.is_valid_path", return_value=False)
  res = client_with_emulator.put(
      url=f"{api_url}/link/{learning_resource.uuid}",
      json={
          "resource_path": sample_resource_path,
          "type": "docx"
      })
  res_json = res.json()

  assert res.status_code == 404
  assert res_json["success"] is False
  assert res_json[
      "message"] == "Provided resource path does not exist on GCS bucket"


# Disabled: Get Content Versions
#------------------------------------------------
def get_content_versions_positive(clean_firestore, mocker):
  """
    Positive Scenarios:
    1. Cold Start - When a content is linked, the resource_path is overriden
    2. Generic Case - When a content is linked, a new doc is created
    3. Filter by status
    4. Filter by status initial document
  """
  mocker.patch(
      "routes.content_serving.GcsCrudService",
      return_value=GcsCrudService("GCP_LEARNING_RESOURCE_BUCKET"))
  mocker.patch(
      "services.content_version_handler.is_valid_path", return_value=True)

  learning_resource_dict = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.type = ""
  learning_resource.resource_path = ""
  learning_resource.status = "initial"
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.root_version_uuid = learning_resource.id
  learning_resource.update()
  learning_resource_dict["uuid"] = learning_resource.id

  sample_resource_path = "sample/resource/path"

  # 1. Cold start
  res = client_with_emulator.put(
      url=f"{api_url}/link/{learning_resource.uuid}",
      json={
          "resource_path": sample_resource_path,
          "type": "docx"
      })
  res_json = res.json()

  assert res.status_code == 200
  assert res_json["success"] is True
  assert res_json[
      "message"] == "Successfully linked learning resource with content"

  res = client_with_emulator.get(
      url=f"{api_url}/content-versions/{learning_resource.uuid}")
  res_json = res.json()

  assert res.status_code == 200
  assert res_json["success"] is True
  assert res_json[
      "message"] == "Successfully fetched content version for learning resource"
  assert len(res_json["data"]) == 2

  # 2. Generic Case
  res = client_with_emulator.put(
      url=f"{api_url}/link/{learning_resource.uuid}",
      json={
          "resource_path": sample_resource_path,
          "type": "docx"
      })
  res_json = res.json()

  assert res.status_code == 200
  assert res_json["success"] is True
  assert res_json[
      "message"] == "Successfully linked learning resource with content"

  res = client_with_emulator.get(
      url=f"{api_url}/content-versions/{learning_resource.uuid}")
  res_json = res.json()

  assert res.status_code == 200
  assert res_json["success"] is True
  assert res_json[
      "message"] == "Successfully fetched content version for learning resource"
  assert len(res_json["data"]) == 3

  # 3. Filter by status
  learning_resource_dict = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.type = ""
  learning_resource.resource_path = ""
  learning_resource.status = "draft"
  learning_resource.is_implicit = True
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.root_version_uuid = learning_resource.id
  learning_resource.update()
  learning_resource_dict["uuid"] = learning_resource.id
  parent_uuid_1 = learning_resource.id
  root_uuid = learning_resource.id

  learning_resource_dict = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.type = ""
  learning_resource.resource_path = ""
  learning_resource.status = "published"
  learning_resource.is_implicit = True
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.root_version_uuid = root_uuid
  learning_resource.parent_version_uuid = parent_uuid_1
  learning_resource.update()
  learning_resource_dict["uuid"] = learning_resource.id
  parent_uuid_2 = learning_resource.id

  learning_resource_dict = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.type = ""
  learning_resource.resource_path = ""
  learning_resource.status = "unpublished"
  learning_resource.is_implicit = True
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.root_version_uuid = root_uuid
  learning_resource.parent_version_uuid = parent_uuid_2
  learning_resource.update()
  learning_resource_dict["uuid"] = learning_resource.id

  res = client_with_emulator.get(
      url=f"{api_url}/content-versions/{learning_resource.uuid}",
      params={"status": "draft"})
  res_json = res.json()

  assert res.status_code == 200
  assert res_json["success"] is True
  assert res_json[
      "message"] == "Successfully fetched content version for learning resource"
  assert len(res_json["data"]) == 1
  assert res_json["data"][0]["status"] == "draft"

  res = client_with_emulator.get(
      url=f"{api_url}/content-versions/{learning_resource.uuid}",
      params={"status": "published"})
  res_json = res.json()

  assert res.status_code == 200
  assert res_json["success"] is True
  assert res_json[
      "message"] == "Successfully fetched content version for learning resource"
  assert len(res_json["data"]) == 1
  assert res_json["data"][0]["status"] == "published"

  res = client_with_emulator.get(
      url=f"{api_url}/content-versions/{learning_resource.uuid}",
      params={"status": "unpublished"})
  res_json = res.json()

  assert res.status_code == 200
  assert res_json["success"] is True
  assert res_json[
      "message"] == "Successfully fetched content version for learning resource"
  assert len(res_json["data"]) == 1
  assert res_json["data"][0]["status"] == "unpublished"

  # 4. Filter by Status with initial document
  learning_resource_dict = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.type = ""
  learning_resource.resource_path = ""
  learning_resource.status = "initial"
  learning_resource.is_implicit = True
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.root_version_uuid = learning_resource.id
  learning_resource.update()
  learning_resource_dict["uuid"] = learning_resource.id

  res = client_with_emulator.get(
      url=f"{api_url}/content-versions/{learning_resource.uuid}")
  res_json = res.json()

  assert res.status_code == 200
  assert res_json["success"] is True
  assert res_json[
      "message"] == "Successfully fetched content version for learning resource"
  assert len(res_json["data"]) == 1


def get_content_versions_negative(clean_firestore, mocker):
  """
        Negative Scenarios:
        1. Invalid LR uuid
    """
  mocker.patch(
      "routes.content_serving.GcsCrudService",
      return_value=GcsCrudService("GCP_LEARNING_RESOURCE_BUCKET"))
  mocker.patch(
      "services.content_version_handler.is_valid_path", return_value=True)

  random_lr_uuid = "random_lr_uuid"

  sample_resource_path = "sample/resource/path"

  res = client_with_emulator.put(
      url=f"{api_url}/link/{random_lr_uuid}",
      json={
          "resource_path": sample_resource_path,
          "type": "docx"
      })
  res_json = res.json()

  assert res.status_code == 404
  assert res_json["success"] is False
  assert res_json[
      "message"] == f"Learning Resource with uuid {random_lr_uuid} not found"


# Disabled: Content publish
#------------------------------------------------
def handle_publish_event_positive(clean_firestore, mocker):
  """
        Positive Scenarios:
        1. Cold start - Single document
        2. Generic Case - Replace existing Published document
        3. Republish - Create a new document from old document and publish
        4. Publish Initial Document when resource path is not empty
    """
  mocker.patch(
      "routes.content_serving.GcsCrudService",
      return_value=GcsCrudService("GCP_LEARNING_RESOURCE_BUCKET"))
  mocker.patch(
      "services.content_version_handler.is_valid_path", return_value=True)

  # 1. Cold Start
  learning_resource_dict = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.type = ""
  learning_resource.resource_path = ""
  learning_resource.status = "initial"
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.root_version_uuid = learning_resource.id
  learning_resource.update()
  learning_resource_dict["uuid"] = learning_resource.id

  sample_resource_path = "sample/resource/path"

  res = client_with_emulator.put(
      url=f"{api_url}/link/{learning_resource.uuid}",
      json={
          "resource_path": sample_resource_path,
          "type": "docx"
      })
  res_json = res.json()

  assert res.status_code == 200
  assert res_json["success"] is True
  assert res_json[
      "message"] == "Successfully linked learning resource with content"
  assert res_json["data"]["resource_uuid"] != learning_resource.uuid
  new_content_version_uuid = res_json["data"]["resource_uuid"]

  res = client_with_emulator.put(
      url=f"{api_url}/publish/{learning_resource.uuid}",
      params={"target_version_uuid": new_content_version_uuid})

  res_json = res.json()
  assert res.status_code == 200
  assert res_json["success"] is True
  assert res_json["message"] == "Successfully published content"

  # 2. Generic Case
  res = client_with_emulator.put(
      url=f"{api_url}/link/{learning_resource.uuid}",
      json={
          "resource_path": sample_resource_path,
          "type": "docx"
      })
  res_json = res.json()

  assert res.status_code == 200
  assert res_json["success"] is True
  assert res_json[
      "message"] == "Successfully linked learning resource with content"
  assert res_json["data"]["resource_uuid"] != learning_resource.uuid

  new_resource_uuid_1 = res_json["data"]["resource_uuid"]

  res = client_with_emulator.put(
      url=f"{api_url}/publish/{new_content_version_uuid}",
      params={"target_version_uuid": new_resource_uuid_1})

  res_json = res.json()
  assert res.status_code == 200
  assert res_json["success"] is True
  assert res_json["message"] == "Successfully published content"

  old_lr = LearningResource.find_by_id(new_content_version_uuid)
  assert old_lr.status == "unpublished"

  new_lr = LearningResource.find_by_id(new_resource_uuid_1)
  assert new_lr.status == "published"

  # 3. Republish Scenario
  res = client_with_emulator.put(
      url=f"{api_url}/publish/{new_lr.uuid}",
      params={"target_version_uuid": old_lr.uuid})

  res_json = res.json()
  assert res.status_code == 200
  assert res_json["success"] is True
  assert res_json["message"] == "Successfully published content"

  assert res_json["data"]["resource_uuid"] != old_lr.uuid
  assert res_json["data"]["resource_uuid"] != new_lr.uuid

  new_lr_2 = LearningResource.find_by_id(res_json["data"]["resource_uuid"])
  assert new_lr_2.parent_version_uuid == old_lr.uuid
  assert new_lr_2.status == "published"

  old_lr = LearningResource.find_by_id(new_content_version_uuid)
  new_lr = LearningResource.find_by_id(new_resource_uuid_1)

  assert old_lr.status == "unpublished"
  assert new_lr.status == "unpublished"

  # 4. Publish initial document when resource path is not empty
  learning_resource_dict = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.type = "video"
  learning_resource.resource_path = "some/path"
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.root_version_uuid = learning_resource.id
  learning_resource.update()
  learning_resource_dict["uuid"] = learning_resource.id

  res = client_with_emulator.put(
      url=f"{api_url}/publish/{learning_resource.uuid}",
      params={"target_version_uuid": learning_resource.uuid},
      data={})
  assert res.status_code == 200
  res_json = res.json()
  assert res_json["success"] is True
  assert res_json["message"] == "Successfully published content"
  assert res_json["data"]["resource_uuid"] == learning_resource.uuid


def handle_publish_event_negative(clean_firestore, mocker):
  """
        Negative Scenarios:
        1. Unconnected LR uuid
        2. Invalid LR uuid
        3. Invalid Target uuid
        4. Invalid Parent uuid
        5. Publishing Initial Document when resource path is empty
    """
  mocker.patch(
      "routes.content_serving.GcsCrudService",
      return_value=GcsCrudService("GCP_LEARNING_RESOURCE_BUCKET"))
  mocker.patch(
      "services.content_version_handler.is_valid_path", return_value=True)

  # 1. Unconnected LR uuid
  learning_object_dict = copy.deepcopy(BASIC_LEARNING_OBJECT_EXAMPLE)
  learning_object_dict["name"] = "Kubernetes Container Orchestration"
  learning_object = LearningObject.from_dict(learning_object_dict)
  learning_object.uuid = ""
  learning_object.save()
  learning_object.uuid = learning_object.id
  learning_object.update()
  learning_object_dict["uuid"] = learning_object.id

  learning_resource_dict = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.type = ""
  learning_resource.resource_path = ""
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.root_version_uuid = learning_resource.id
  learning_resource.parent_nodes = {
      "learning_objects": [learning_object_dict["uuid"]]
  }
  learning_resource.update()
  learning_resource_dict["uuid"] = learning_resource.id

  sample_resource_path = "sample/resource/path"
  learning_resource_uuid = learning_resource_dict["uuid"]

  # create first link
  res = client_with_emulator.put(
      url=f"{api_url}/link/{learning_resource_uuid}",
      json={
          "resource_path": sample_resource_path,
          "type": "docx"
      })
  res_json = res.json()

  # publish original document
  res = client_with_emulator.put(
      url=f"{api_url}/publish/{learning_resource_uuid}")

  res_json = res.json()
  assert res.status_code == 422
  assert res_json["success"] is False
  assert res_json[
      "message"] == "Given resource uuid is not connected to a valid parent"

  # 2. Invalid LR uuid
  random_lr_uuid = "random_lr_uuid"
  valid_target_uuid = "valid_target_uuid"
  res = client_with_emulator.put(
      url=f"{api_url}/publish/{random_lr_uuid}",
      params={"target_version_uuid": valid_target_uuid})

  res_json = res.json()
  assert res.status_code == 404
  assert res_json["success"] is False
  assert res_json[
      "message"] == f"Learning Resource with uuid {random_lr_uuid} not found"

  # 3. Invalid Target uuid

  learning_resource_dict = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.type = ""
  learning_resource.resource_path = ""
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.root_version_uuid = learning_resource.id
  learning_resource.update()
  learning_resource_dict["uuid"] = learning_resource.id

  sample_resource_path = "sample/resource/path"

  res = client_with_emulator.put(
      url=f"{api_url}/link/{learning_resource.uuid}",
      json={
          "resource_path": sample_resource_path,
          "type": "docx"
      })
  res_json = res.json()

  assert res.status_code == 200
  assert res_json["success"] is True
  assert res_json[
      "message"] == "Successfully linked learning resource with content"

  _ = res_json["data"]["resource_uuid"]
  invalid_target_uuid = "invalid_target_uuid"

  res = client_with_emulator.put(
      url=f"{api_url}/publish/{learning_resource.uuid}",
      params={"target_version_uuid": invalid_target_uuid})

  res_json = res.json()
  assert res.status_code == 404
  assert res_json["success"] is False
  assert res_json[
      "message"] == f"Learning Resource with uuid {invalid_target_uuid} not found"

  # 4. Invalid Parent uuid
  learning_resource_dict = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.type = ""
  learning_resource.resource_path = ""
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.root_version_uuid = learning_resource.id
  learning_resource.parent_nodes = {"learning_objects": ["random_parent"]}
  learning_resource.update()
  learning_resource_dict["uuid"] = learning_resource.id

  sample_resource_path = "sample/resource/path"
  learning_resource_uuid = learning_resource_dict["uuid"]

  # create first link
  res = client_with_emulator.put(
      url=f"{api_url}/link/{learning_resource_uuid}",
      json={
          "resource_path": sample_resource_path,
          "type": "docx"
      })
  res_json = res.json()

  # publish original document
  res = client_with_emulator.put(
      url=f"{api_url}/publish/{learning_resource_uuid}")

  res_json = res.json()
  assert res.status_code == 404
  assert res_json["success"] is False
  assert res_json[
      "message"] == "Learning Object with uuid random_parent not found"

  # 5. Publish Initial document when resource path is empty
  learning_resource_dict = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.type = ""
  learning_resource.resource_path = ""
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.root_version_uuid = learning_resource.id
  learning_resource.update()
  learning_resource_dict["uuid"] = learning_resource.id

  res = client_with_emulator.put(
      url=f"{api_url}/publish/{learning_resource.uuid}",
      params={"target_version_uuid": learning_resource.uuid},
      data={})
  assert res.status_code == 422
  res_json = res.json()
  assert res_json["success"] is False
  assert res_json[
      "message"] == f"resource_path is empty for Learning Resource with uuid {learning_resource.uuid}"


# Get Files List
#------------------------------------------------
def test_get_file_list_positive(clean_firestore, mocker):
  mocker.patch(
      "services.hierarchy_content_mapping.GcsCrudService",
      return_value=GcsCrudService("GCP_LEARNING_RESOURCE_BUCKET"))

  prefix = "abc/"
  res = client_with_emulator.get(
      url=f"{api_url}/list-contents", params={"prefix": prefix})
  res_json = res.json()

  assert res.status_code == 200
  assert res_json["success"] is True
  assert res_json[
      "message"] == "Successfully listed all files and folder at given prefix"
  assert res_json["data"]["prefix"] == prefix


# Upload API test
#------------------------------------------------
def test_upload_api_positive(clean_firestore, mocker):
  mocker.patch(
      "services.hierarchy_content_mapping.GcsCrudService",
      return_value=GcsCrudService("GCP_LEARNING_RESOURCE_BUCKET"))
  mocker.patch("routes.content_serving.is_valid_path", return_value=True)
  mocker.patch("routes.content_serving.upload_file_to_bucket")
  mocker.patch("routes.content_serving.upload_folder")

  file_path = f"{TESTING_FOLDER_PATH}/content_serving/sample_upload_pdf.pdf"
  upload_file = open(file_path)
  resp = client_with_emulator.post(
      f"{api_url}/upload/sync",
      files={
          "content_file":
              ("sample_upload_pdf.pdf", upload_file, "application/pdf")
      })
  resp_json = resp.json()
  assert resp.status_code == 200
  assert resp_json["success"] is True
  assert resp_json["message"] == "Successfully uploaded the learning content"
  assert resp_json["data"].get("prefix") is not None
  assert resp_json["data"].get("files") is not None
  assert resp_json["data"].get("folders") is not None


def test_upload_api_negative(clean_firestore, mocker):
  """
    Negative Scenarios:
    1. Invalid content headers
    2. Extension and content header does not match
  """
  mocker.patch(
      "services.hierarchy_content_mapping.GcsCrudService",
      return_value=GcsCrudService("GCP_LEARNING_RESOURCE_BUCKET"))
  mocker.patch("routes.content_serving.is_valid_path", return_value=True)
  mocker.patch("routes.content_serving.upload_file_to_bucket")
  mocker.patch("routes.content_serving.upload_folder")

  file_path = f"{TESTING_FOLDER_PATH}/content_serving/sample_upload_pdf.pdf"
  upload_file = open(file_path)
  resp = client_with_emulator.post(
      f"{api_url}/upload/sync",
      files={
          "content_file":
              ("sample_upload_pdf.pdf", upload_file, "application/abc")
      })
  resp_json = resp.json()
  assert resp.status_code == 422
  assert resp_json["success"] is False

  resp = client_with_emulator.post(
      f"{api_url}/upload/sync",
      files={
          "content_file":
              ("sample_upload_pdf.pdf", upload_file, "application/zip")
      })
  resp_json = resp.json()
  assert resp.status_code == 422
  assert resp_json["success"] is False


# Alpha Scope: Madcap Upload API at LE
#------------------------------------------------
def test_upload_madcap_positive(clean_firestore, mocker):
  mocker.patch(
      "services.hierarchy_content_mapping.GcsCrudService",
      return_value=GcsCrudService("GCP_LEARNING_RESOURCE_BUCKET"))
  mocker.patch("routes.content_serving.is_valid_path", return_value=True)
  mocker.patch("routes.content_serving.upload_folder")

  learning_experience_dict = copy.deepcopy(BASIC_LEARNING_EXPERIENCE_EXAMPLE)
  learning_experience = LearningExperience.from_dict(learning_experience_dict)
  learning_experience.uuid = ""
  learning_experience.resource_path = ""
  learning_experience.save()
  learning_experience.uuid = learning_experience.id
  learning_experience.root_version_uuid = learning_experience.id
  learning_experience.update()
  learning_experience_dict["uuid"] = learning_experience.id

  file_path = f"{TESTING_FOLDER_PATH}/content_serving/dummy_madcap.zip"

  resp = client_with_emulator.post(
      f"{api_url}/upload/madcap/{learning_experience.uuid}",
      files={
          "content_file": ("dummy_madcap.zip", open(file_path,
                                                    "rb"), "application/zip")
      })
  resp_json = resp.json()
  assert resp.status_code == 200
  assert resp_json["success"] is True
  assert resp_json[
      "message"] == f"Successfully uploaded the content for learning experience with uuid {learning_experience.uuid}"
  assert resp_json["data"].get("prefix") is not None
  assert resp_json["data"].get("files") is not None
  assert resp_json["data"].get("folders") is not None

  le = LearningExperience.find_by_id(learning_experience.uuid)
  assert le.resource_path == "learning-resources/dummy_madcap/"


def test_upload_madcap_negative(clean_firestore, mocker):
  """
        Possible Negative Scenarios:
        1. Uploaded Madcap is invalid
        2. Uploaded Madcap is overriding existing links
        3. LE is invalid
    """
  mocker.patch(
      "services.hierarchy_content_mapping.GcsCrudService",
      return_value=GcsCrudService("GCP_LEARNING_RESOURCE_BUCKET"))
  mocker.patch(
      "services.hierarchy_content_mapping.FileUtils", return_value=FileUtils())
  mocker.patch("routes.content_serving.is_valid_path", return_value=True)
  mocker.patch("routes.content_serving.upload_folder")
  mocker.patch(
      "services.hierarchy_content_mapping.is_missing_linked_files",
      return_value=(False,
                    "Content override is forbidden because of missing files."))
  mocker.patch(
      "services.hierarchy_content_mapping.get_file_and_folder_list",
      return_value=(None, None, ["def"]))

  #-------------------------------------------------------------
  # Setup Steps Start
  #-------------------------------------------------------------
  learning_experience_dict = copy.deepcopy(BASIC_LEARNING_EXPERIENCE_EXAMPLE)
  learning_experience = LearningExperience.from_dict(learning_experience_dict)
  learning_experience.uuid = ""
  learning_experience.resource_path = ""
  learning_experience.save()
  learning_experience.uuid = learning_experience.id
  learning_experience.root_version_uuid = learning_experience.id
  learning_experience.update()
  learning_experience_dict["uuid"] = learning_experience.id

  file_path = f"{TESTING_FOLDER_PATH}/content_serving/dummy_madcap.zip"

  resp = client_with_emulator.post(
      f"{api_url}/upload/madcap/{learning_experience.uuid}",
      files={
          "content_file": ("dummy_madcap.zip", open(file_path,
                                                    "rb"), "application/zip")
      })
  resp_json = resp.json()
  assert resp.status_code == 200
  assert resp_json["success"] is True
  assert resp_json[
      "message"] == f"Successfully uploaded the content for learning experience with uuid {learning_experience.uuid}"
  assert resp_json["data"].get("prefix") is not None
  assert resp_json["data"].get("files") is not None
  assert resp_json["data"].get("folders") is not None

  le = LearningExperience.find_by_id(learning_experience.uuid)
  assert le.resource_path == "learning-resources/dummy_madcap/"

  #-------------------------------------------------------------
  # Setup Steps End
  #-------------------------------------------------------------

  # 1. Uploaded Madcap is invalid

  file_path = f"{TESTING_FOLDER_PATH}/content_serving/sample_upload_scorm.zip"

  resp = client_with_emulator.post(
      f"{api_url}/upload/madcap/{le.uuid}",
      files={
          "content_file": ("sample_upload_scorm.zip", open(file_path, "rb"),
                           "application/zip")
      })
  resp_json = resp.json()
  assert resp.status_code == 422
  assert resp_json["success"] is False
  assert resp_json[
      "message"] == "sample_upload_scorm is not a valid Madcap Export. Default.htm file was not found."

  # 2. Uploaded Madcap is overriding existing links
  file_path = f"{TESTING_FOLDER_PATH}/content_serving/dummy_madcap_v2.zip"

  resp = client_with_emulator.post(
      f"{api_url}/upload/madcap/{le.uuid}",
      files={
          "content_file": ("dummy_madcap_v2.zip", open(file_path,
                                                       "rb"), "application/zip")
      })
  resp_json = resp.json()
  assert resp.status_code == 422
  assert resp_json["success"] is False
  assert resp_json[
      "message"] == "Content override is forbidden because of missing files.\nFollowing files were not found:\n[def]"

  # 3. Invalid LE uuid
  file_path = f"{TESTING_FOLDER_PATH}/content_serving/dummy_madcap_v2.zip"

  invalid_uuid = "random_uuid"
  resp = client_with_emulator.post(
      f"{api_url}/upload/madcap/{invalid_uuid}",
      files={
          "content_file": ("dummy_madcap_v2.zip", open(file_path,
                                                       "rb"), "application/zip")
      })
  resp_json = resp.json()
  assert resp.status_code == 404
  assert resp_json["success"] is False
  assert resp_json[
      "message"] == "Learning Experience with uuid random_uuid not found"


# Alpha Scope: Link Madcap to LR
#------------------------------------------------
def test_link_madcap_to_lr_positive(clean_firestore, mocker):
  mocker.patch(
      "services.hierarchy_content_mapping.GcsCrudService",
      return_value=GcsCrudService("GCP_LEARNING_RESOURCE_BUCKET"))
  mocker.patch(
      "services.hierarchy_content_mapping.FileUtils", return_value=FileUtils())
  mocker.patch("routes.content_serving.is_valid_path", return_value=True)
  mocker.patch("routes.content_serving.upload_folder")
  mocker.patch(
      "services.hierarchy_content_mapping.is_missing_linked_files",
      return_value=(False,
                    "Content override is forbidden because of missing files."))
  mocker.patch(
      "services.hierarchy_content_mapping.get_file_and_folder_list",
      return_value=(None, None, ["def"]))

  #-------------------------------------------------------------
  # Setup Steps Start
  #-------------------------------------------------------------
  learning_experience_dict = copy.deepcopy(BASIC_LEARNING_EXPERIENCE_EXAMPLE)
  learning_experience = LearningExperience.from_dict(learning_experience_dict)
  learning_experience.uuid = ""
  learning_experience.resource_path = ""
  learning_experience.save()
  learning_experience.uuid = learning_experience.id
  learning_experience.root_version_uuid = learning_experience.id
  learning_experience.update()
  learning_experience_dict["uuid"] = learning_experience.id

  file_path = f"{TESTING_FOLDER_PATH}/content_serving/dummy_madcap.zip"

  resp = client_with_emulator.post(
      f"{api_url}/upload/madcap/{learning_experience.uuid}",
      files={
          "content_file": ("dummy_madcap.zip", open(file_path,
                                                    "rb"), "application/zip")
      })
  resp_json = resp.json()
  assert resp.status_code == 200
  assert resp_json["success"] is True
  assert resp_json[
      "message"] == f"Successfully uploaded the content for learning experience with uuid {learning_experience.uuid}"
  assert resp_json["data"].get("prefix") is not None
  assert resp_json["data"].get("files") is not None
  assert resp_json["data"].get("folders") is not None

  le = LearningExperience.find_by_id(learning_experience.uuid)
  assert le.resource_path == "learning-resources/dummy_madcap/"

  learning_object_dict = copy.deepcopy(BASIC_LEARNING_OBJECT_EXAMPLE)
  learning_object_dict["name"] = "Kubernetes Container Orchestration"
  learning_object = LearningObject.from_dict(learning_object_dict)
  learning_object.uuid = ""
  learning_object.parent_nodes = {
      "learning_experiences": [learning_experience.uuid]
  }
  learning_object.save()
  learning_object.uuid = learning_object.id
  learning_object.update()
  learning_object_dict["uuid"] = learning_object.id

  learning_experience.child_nodes = {"learning_objects": [learning_object.uuid]}
  learning_experience.update()

  learning_resource_dict = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.type = ""
  learning_resource.resource_path = ""
  learning_resource.parent_nodes = {"learning_objects": [learning_object.uuid]}
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.update()
  learning_resource_dict["uuid"] = learning_resource.id

  learning_object.child_nodes = {"learning_resources": [learning_resource.uuid]}
  learning_object.update()

  file_path = f"{TESTING_FOLDER_PATH}/content_serving/dummy_madcap.zip"

  resp = client_with_emulator.post(
      f"{api_url}/upload/madcap/{learning_experience.uuid}",
      files={
          "content_file": ("dummy_madcap.zip", open(file_path,
                                                    "rb"), "application/zip")
      })
  resp_json = resp.json()
  assert resp.status_code == 200
  assert resp_json["success"] is True
  assert resp_json[
      "message"] == f"Successfully uploaded the content for learning experience with uuid {learning_experience.uuid}"
  assert resp_json["data"].get("prefix") is not None
  assert resp_json["data"].get("files") is not None
  assert resp_json["data"].get("folders") is not None

  le = LearningExperience.find_by_id(learning_experience.uuid)
  assert le.resource_path == "learning-resources/dummy_madcap/"
  #-------------------------------------------------------------
  # Setup Steps End
  #-------------------------------------------------------------

  resp = client_with_emulator.post(
      url=f"{api_url}/link/madcap/{learning_experience.uuid}/{learning_resource.uuid}",
      json={
          "resource_path": "def",
          "type": "html"
      })

  resp_json = resp.json()

  assert resp.status_code == 200
  assert resp_json["success"] is True
  assert resp_json[
      "message"] == f"Successfully linked content to Learning Resource with uuid {learning_resource.uuid}"

  lr = LearningResource.find_by_id(learning_resource.uuid)
  assert lr.resource_path == "def"
  assert lr.type == "html"


def test_link_madcap_to_lr_negative(clean_firestore, mocker):
  """
        Possible scenarios
        1. Invalid LE uuid
        2. Invalid LR uuid
        3. Invalid LE, LR pair
        4. File does not exists in prefix given by LE
        5. LE does not have a resource_path
    """

  mocker.patch(
      "services.hierarchy_content_mapping.GcsCrudService",
      return_value=GcsCrudService("GCP_LEARNING_RESOURCE_BUCKET"))
  mocker.patch(
      "services.hierarchy_content_mapping.FileUtils", return_value=FileUtils())
  mocker.patch("routes.content_serving.is_valid_path", return_value=True)
  mocker.patch("routes.content_serving.upload_folder")
  mocker.patch(
      "services.hierarchy_content_mapping.is_missing_linked_files",
      return_value=(False,
                    "Content override is forbidden because of missing files."))
  mocker.patch(
      "services.hierarchy_content_mapping.get_file_and_folder_list",
      return_value=(None, None, ["def"]))

  #-------------------------------------------------------------
  # Setup Steps Start
  #-------------------------------------------------------------
  learning_experience_dict = copy.deepcopy(BASIC_LEARNING_EXPERIENCE_EXAMPLE)
  learning_experience = LearningExperience.from_dict(learning_experience_dict)
  learning_experience.uuid = ""
  learning_experience.resource_path = ""
  learning_experience.save()
  learning_experience.uuid = learning_experience.id
  learning_experience.root_version_uuid = learning_experience.id
  learning_experience.update()
  learning_experience_dict["uuid"] = learning_experience.id

  file_path = f"{TESTING_FOLDER_PATH}/content_serving/dummy_madcap.zip"

  resp = client_with_emulator.post(
      f"{api_url}/upload/madcap/{learning_experience.uuid}",
      files={
          "content_file": ("dummy_madcap.zip", open(file_path,
                                                    "rb"), "application/zip")
      })
  resp_json = resp.json()
  assert resp.status_code == 200
  assert resp_json["success"] is True
  assert resp_json[
      "message"] == f"Successfully uploaded the content for learning experience with uuid {learning_experience.uuid}"
  assert resp_json["data"].get("prefix") is not None
  assert resp_json["data"].get("files") is not None
  assert resp_json["data"].get("folders") is not None

  le = LearningExperience.find_by_id(learning_experience.uuid)
  assert le.resource_path == "learning-resources/dummy_madcap/"

  learning_object_dict = copy.deepcopy(BASIC_LEARNING_OBJECT_EXAMPLE)
  learning_object_dict["name"] = "Kubernetes Container Orchestration"
  learning_object = LearningObject.from_dict(learning_object_dict)
  learning_object.uuid = ""
  learning_object.parent_nodes = {
      "learning_experiences": [learning_experience.uuid]
  }
  learning_object.save()
  learning_object.uuid = learning_object.id
  learning_object.update()
  learning_object_dict["uuid"] = learning_object.id

  learning_experience.child_nodes = {"learning_objects": [learning_object.uuid]}
  learning_experience.update()

  learning_resource_dict = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.type = ""
  learning_resource.resource_path = ""
  learning_resource.parent_nodes = {"learning_objects": [learning_object.uuid]}
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.update()
  learning_resource_dict["uuid"] = learning_resource.id

  learning_object.child_nodes = {"learning_resources": [learning_resource.uuid]}
  learning_object.update()

  file_path = f"{TESTING_FOLDER_PATH}/content_serving/dummy_madcap.zip"

  resp = client_with_emulator.post(
      f"{api_url}/upload/madcap/{learning_experience.uuid}",
      files={
          "content_file": ("dummy_madcap.zip", open(file_path,
                                                    "rb"), "application/zip")
      })
  resp_json = resp.json()
  assert resp.status_code == 200
  assert resp_json["success"] is True
  assert resp_json[
      "message"] == f"Successfully uploaded the content for learning experience with uuid {learning_experience.uuid}"
  assert resp_json["data"].get("prefix") is not None
  assert resp_json["data"].get("files") is not None
  assert resp_json["data"].get("folders") is not None

  le = LearningExperience.find_by_id(learning_experience.uuid)
  assert le.resource_path == "learning-resources/dummy_madcap/"
  #-------------------------------------------------------------
  # Setup Steps End
  #-------------------------------------------------------------

  # 1. Invalid LE uuid
  invalid_uuid = "random_uuid"
  resp = client_with_emulator.post(
      url=f"{api_url}/link/madcap/{invalid_uuid}/{learning_resource.uuid}",
      json={
          "resource_path": "def",
          "type": "html"
      })

  resp_json = resp.json()

  assert resp.status_code == 404
  assert resp_json["success"] is False
  assert resp_json[
      "message"] == f"Learning Experience with uuid {invalid_uuid} not found"

  # 2. Invalid LR uuid
  invalid_uuid = "random_uuid"
  resp = client_with_emulator.post(
      url=f"{api_url}/link/madcap/{learning_experience.uuid}/{invalid_uuid}",
      json={
          "resource_path": "def",
          "type": "html"
      })

  resp_json = resp.json()

  assert resp.status_code == 404
  assert resp_json["success"] is False
  assert resp_json[
      "message"] == f"Learning Resource with uuid {invalid_uuid} not found"

  # 3. Invalid LE, LR pair
  learning_resource_dict_2 = copy.deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource_2 = LearningResource.from_dict(learning_resource_dict_2)
  learning_resource_2.uuid = ""
  learning_resource_2.type = ""
  learning_resource_2.resource_path = ""
  learning_resource_2.save()
  learning_resource_2.uuid = learning_resource_2.id
  learning_resource_2.update()
  learning_resource_dict_2["uuid"] = learning_resource_2.id

  resp = client_with_emulator.post(
      url=f"{api_url}/link/madcap/{learning_experience.uuid}/{learning_resource_2.uuid}",
      json={
          "resource_path": "def",
          "type": "html"
      })

  resp_json = resp.json()

  assert resp.status_code == 422
  assert resp_json["success"] is False
  assert resp_json[
      "message"] == f"Given Learning Resource {learning_resource_2.uuid} is not a child of Learning Experience {learning_experience.uuid}"

  # 4. Invalid resource path
  resp = client_with_emulator.post(
      url=f"{api_url}/link/madcap/{learning_experience.uuid}/{learning_resource.uuid}",
      json={
          "resource_path": "hij",
          "type": "html"
      })

  resp_json = resp.json()

  assert resp.status_code == 422
  assert resp_json["success"] is False
  assert resp_json[
      "message"] == "Cannot link Learning Resource with a file that does not belong to the folder given by Learning Experience.Required file path prefix: learning-resources/dummy_madcap/"

  # 5. LE does not have a resource_path
  learning_experience = LearningExperience.find_by_id(
      learning_experience.uuid)
  learning_experience.resource_path = ""
  learning_experience.update()

  resp = client_with_emulator.post(
      url=f"{api_url}/link/madcap/{learning_experience.uuid}/{learning_resource.uuid}",
      json={
          "resource_path": "hij",
          "type": "html"
      })

  resp_json = resp.json()

  assert resp.status_code == 422
  assert resp_json["success"] is False
  assert resp_json[
      "message"] == f"The resource_path of Learning Experience {learning_experience.uuid} is empty. Hence, we cannot link content to Learning resource with uuid {learning_resource.uuid}"


# Alpha Scope: Upload Madcap SRL to LE
#------------------------------------------------
def test_link_madcap_srl_to_le_positive(clean_firestore, mocker):
  """
    Possible Scenarios:
    1. User Uploads Valid SRL to LE once, and all Sibling LEs get access to it
    2. User reuploads Valid SRL to LE
  """

  mocker.patch(
      "services.hierarchy_content_mapping.GcsCrudService",
      return_value=GcsCrudService("GCP_LEARNING_RESOURCE_BUCKET"))
  mocker.patch(
      "services.hierarchy_content_mapping.FileUtils", return_value=FileUtils())
  mocker.patch("routes.content_serving.is_valid_path", return_value=True)
  mocker.patch("routes.content_serving.upload_folder")
  mocker.patch(
      "services.hierarchy_content_mapping.is_missing_linked_files",
      return_value=(True,None))
  mocker.patch(
      "services.hierarchy_content_mapping.get_file_and_folder_list",
      return_value=(None, None, ["abc"]))

  #-------------------------------------------------------------
  # Setup Steps Start
  #-------------------------------------------------------------

  program_uuid = ""

  url = f"{API_URL}/curriculum-pathway/bulk-import/json"
  with open(SRL_PATHWAY, encoding="UTF-8") as pathways_json_file:
    resp = client_with_emulator_3.post(
        url, files={"json_file": pathways_json_file})

    assert resp.status_code == 200
    resp_json = resp.json()
    program_uuid = resp_json["data"][0]

  sibling_le_list = []
  le_list = get_all_nodes_for_alias(
      uuid=program_uuid,
      level="curriculum_pathways",
      final_alias="learning_experience",
      nodes=sibling_le_list)

  le_1_uuid = le_list[0]["uuid"]
  le_2_uuid = le_list[1]["uuid"]

  #-------------------------------------------------------------
  # Setup Steps End
  #-------------------------------------------------------------

  # 1. User Uploads Valid SRL to LE once, and all Sibling LEs get access to it
  file_path = f"{TESTING_FOLDER_PATH}/content_serving/SRL_Dummy.zip"

  resp = client_with_emulator.post(
      url=f"{api_url}/upload/madcap/{le_1_uuid}",
      params={"is_srl": True},
      files={
          "content_file": ("SRL_Dummy.zip", open(file_path,
                                                 "rb"), "application/zip")
      })
  resp_json = resp.json()
  assert resp.status_code == 200
  assert resp_json["success"] is True
  assert resp_json[
      "message"] == f"Successfully uploaded the SRL content for learning experience with uuid {le_1_uuid}"
  assert resp_json["data"].get("prefix") is not None
  assert resp_json["data"].get("files") is not None
  assert resp_json["data"].get("folders") is not None

  le_1 = LearningExperience.find_by_id(le_1_uuid)
  le_2 = LearningExperience.find_by_id(le_2_uuid)
  assert le_1.srl_resource_path == "learning-resources/SRL_Dummy/"
  assert le_2.srl_resource_path == "learning-resources/SRL_Dummy/"

  lo_1 = LearningObject.find_by_id(le_1.child_nodes["learning_objects"][0])

  lr_1 = LearningResource.find_by_id(
      lo_1.child_nodes["learning_resources"][0])

  resp = client_with_emulator.post(
      url=f"{api_url}/link/madcap/{le_1_uuid}/{lr_1.uuid}",
      json={
          "resource_path": "abc",
          "type": "html"
      },
      params={"is_srl": True})

  resp_json = resp.json()

  assert resp.status_code == 200
  assert resp_json["success"] is True
  assert resp_json[
      "message"] == f"Successfully linked content to Learning Resource with uuid {lr_1.uuid}"

  lr_1 = LearningResource.find_by_id(lr_1.uuid)
  assert lr_1.resource_path == "abc"
  assert lr_1.type == "html"

  # 2. User reuploads a valid SRL
  file_path = f"{TESTING_FOLDER_PATH}/content_serving/SRL_Dummy_v2.zip"

  resp = client_with_emulator.post(
      url=f"{api_url}/upload/madcap/{le_1_uuid}",
      params={"is_srl": True},
      files={
          "content_file": ("SRL_Dummy_v2.zip", open(file_path,
                                                 "rb"), "application/zip")
      })
  resp_json = resp.json()
  print(resp_json)
  assert resp.status_code == 200
  assert resp_json["success"] is True
  assert resp_json[
      "message"] == f"Successfully uploaded the SRL content for learning experience with uuid {le_1_uuid}"
  assert resp_json["data"].get("prefix") is not None
  assert resp_json["data"].get("files") is not None
  assert resp_json["data"].get("folders") is not None

  le_1 = LearningExperience.find_by_id(le_1_uuid)
  le_2 = LearningExperience.find_by_id(le_2_uuid)
  assert le_1.srl_resource_path == "learning-resources/SRL_Dummy_v2/"
  assert le_2.srl_resource_path == "learning-resources/SRL_Dummy_v2/"

  lo_1 = LearningObject.find_by_id(le_1.child_nodes["learning_objects"][0])

  lr_1 = LearningResource.find_by_id(
      lo_1.child_nodes["learning_resources"][0])

  assert lr_1.resource_path == "abc"


def test_link_madcap_srl_to_le_negative(clean_firestore, mocker):
  """
    Possible Scenarios:
    1. User Uploads zip with invalid file name
    2. User Reuploads a zip with missing files
  """

  mocker.patch(
      "services.hierarchy_content_mapping.GcsCrudService",
      return_value=GcsCrudService("GCP_LEARNING_RESOURCE_BUCKET"))
  mocker.patch(
      "services.hierarchy_content_mapping.FileUtils", return_value=FileUtils())
  mocker.patch("routes.content_serving.is_valid_path", return_value=True)
  mocker.patch("routes.content_serving.upload_folder")
  mocker.patch(
      "services.hierarchy_content_mapping.is_missing_linked_files",
      return_value=(False,
                    "Content override is forbidden because of missing files."))
  mocker.patch(
      "services.hierarchy_content_mapping.get_file_and_folder_list",
      return_value=(None, None, ["def"]))

  #-------------------------------------------------------------
  # Setup Steps Start
  #-------------------------------------------------------------

  program_uuid = ""

  url = f"{API_URL}/curriculum-pathway/bulk-import/json"
  with open(SRL_PATHWAY, encoding="UTF-8") as pathways_json_file:
    resp = client_with_emulator_3.post(
        url, files={"json_file": pathways_json_file})

    assert resp.status_code == 200
    resp_json = resp.json()
    program_uuid = resp_json["data"][0]

  sibling_le_list = []
  le_list = get_all_nodes_for_alias(
      uuid=program_uuid,
      level="curriculum_pathways",
      final_alias="learning_experience",
      nodes=sibling_le_list)

  le_1_uuid = le_list[0]["uuid"]

  #-------------------------------------------------------------
  # Setup Steps End
  #-------------------------------------------------------------

  # 1. User Uploads zip with invalid file name
  file_path = f"{TESTING_FOLDER_PATH}/content_serving/dummy_madcap.zip"

  resp = client_with_emulator.post(
      url=f"{api_url}/upload/madcap/{le_1_uuid}",
      params={"is_srl": True},
      files={
          "content_file": ("dummy_madcap.zip", open(file_path,
                                                    "rb"), "application/zip")
      })
  resp_json = resp.json()
  assert resp.status_code == 422
  assert resp_json["success"] is False
  assert resp_json[
      "message"] == """File name should start with the prefix "SRL". eg: "SRL_file_1.zip" """

  # 2. User Reuploads a zip with missing files
  file_path = f"{TESTING_FOLDER_PATH}/content_serving/SRL_Dummy_v2.zip"

  resp = client_with_emulator.post(
      url=f"{api_url}/upload/madcap/{le_1_uuid}",
      params={"is_srl": True},
      files={
          "content_file": ("SRL_Dummy_v2.zip", open(file_path,
                                                 "rb"), "application/zip")
      })
  resp_json = resp.json()
  print(resp_json)
  assert resp.status_code == 200
  assert resp_json["success"] is True

  file_path = f"{TESTING_FOLDER_PATH}/content_serving/SRL_Dummy_v3.zip"

  resp = client_with_emulator.post(
      url=f"{api_url}/upload/madcap/{le_1_uuid}",
      params={"is_srl": True},
      files={
          "content_file": ("SRL_Dummy_v3.zip", open(file_path,
                                                 "rb"), "application/zip")
      })
  resp_json = resp.json()
  print(resp_json)
  assert resp.status_code == 422
  assert resp_json["success"] is False
  assert "Content override is forbidden because of missing files." in resp_json["message"]
  