"""
  Unit tests for LTI Content Item endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
# pylint: disable=wrong-import-position
import os
import copy
import mock
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from testing.test_config import API_URL, DEL_KEYS
from common.models import LTIContentItem
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  from routes.content_item import router
  from schemas.schema_examples import (BASIC_CONTENT_ITEM_EXAMPLE,
                                       BASIC_TOOL_EXAMPLE)

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/lti/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/content-item"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


@pytest.mark.parametrize(
    "create_content_item", [BASIC_CONTENT_ITEM_EXAMPLE], indirect=True)
def test_search_content_item(clean_firestore, create_content_item):
  content_item = create_content_item
  content_item_dict = content_item.get_fields(reformat_datetime=True)
  content_item_dict["uuid"] = content_item.id

  params = {"tool_id": content_item.tool_id}

  url = f"{api_url}/search"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  print("json_response", json_response)
  modified_del_keys = DEL_KEYS + [
      "is_deleted", "created_by", "last_modified_by"
  ]
  for key in modified_del_keys:
    if key in json_response["data"][0]:
      del json_response["data"][0][key]
    if key in content_item_dict:
      del content_item_dict[key]
  assert resp.status_code == 200, "Status code not 200"
  assert json_response.get("data")[0] == content_item_dict


@pytest.mark.parametrize(
    "create_content_item", [BASIC_CONTENT_ITEM_EXAMPLE], indirect=True)
def test_get_content_item(clean_firestore, create_content_item):
  content_item_dict = copy.deepcopy(BASIC_CONTENT_ITEM_EXAMPLE)
  content_item = create_content_item
  uuid = content_item_dict["uuid"] = content_item.id

  url = f"{api_url}/{uuid}"
  # fetch only the document with given uuid
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  for key in DEL_KEYS:
    if key in json_response["data"]:
      del json_response["data"][key]
  del content_item_dict["uuid"]
  assert resp.status_code == 200, "Status code not 200"
  assert json_response.get("data") == content_item_dict, "Response received"


def test_get_content_item_negative(clean_firestore):
  uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{uuid}"
  data = {
      "success": False,
      "message": f"LTI Content item with uuid {uuid} not found",
      "data": None
  }

  resp = client_with_emulator.get(url)
  json_response = resp.json()
  print("json_response", json_response)
  assert resp.status_code == 404, "Status code not 404"
  assert json_response == data, "Response received"


@pytest.mark.parametrize("create_tool", [BASIC_TOOL_EXAMPLE], indirect=True)
def test_post_content_item(clean_firestore, create_tool):
  tool = create_tool

  input_content_item = copy.deepcopy(BASIC_CONTENT_ITEM_EXAMPLE)
  input_content_item["tool_id"] = tool.id

  url = api_url
  for key in DEL_KEYS:
    if key in input_content_item:
      del input_content_item[key]
  post_resp = client_with_emulator.post(url, json=input_content_item)
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


@pytest.mark.parametrize("create_tool", [BASIC_TOOL_EXAMPLE], indirect=True)
@pytest.mark.parametrize(
    "create_content_item", [BASIC_CONTENT_ITEM_EXAMPLE], indirect=True)
def test_update_content_item(clean_firestore, create_content_item, create_tool):
  tool = create_tool
  content_item = create_content_item

  content_item.tool_id = tool.id
  content_item.update()

  content_item_dict = content_item.get_fields(reformat_datetime=True)
  content_item_dict["content_item_type"] = "link"

  modified_del_keys = DEL_KEYS + [
      "is_deleted", "last_modified_by", "created_by"
  ]

  for key in modified_del_keys:
    if key in content_item_dict:
      del content_item_dict[key]

  url = f"{api_url}/{content_item.uuid}"

  # Test to update the document
  resp = client_with_emulator.put(url, json=content_item_dict)
  json_response_update_req = resp.json()
  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get(
      "message"
  ) == "Successfully updated the content item", \
  "Expected response not same"
  assert json_response_update_req.get("data").get("content_item_type") == "link"


@pytest.mark.parametrize(
    "create_content_item", [BASIC_CONTENT_ITEM_EXAMPLE], indirect=True)
def test_update_content_item_negative(clean_firestore, create_content_item):
  content_item_dict = copy.deepcopy(BASIC_CONTENT_ITEM_EXAMPLE)
  uuid = content_item_dict["uuid"] = "U2DDBkl3Ayg0PWudzhI"

  url = f"{api_url}/{uuid}"
  response = {
      "success": False,
      "message": "LTI Content item with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }

  # Negative test when updating the document itself with wrong uuid
  for key in DEL_KEYS:
    if key in content_item_dict:
      del content_item_dict[key]
  resp = client_with_emulator.put(url, json=content_item_dict)
  json_response = resp.json()
  assert resp.status_code == 404, "Status code not 404"
  assert json_response == response, "Expected response not same"


@pytest.mark.parametrize(
    "create_content_item", [BASIC_CONTENT_ITEM_EXAMPLE], indirect=True)
def test_delete_content_item(clean_firestore, create_content_item):
  content_item = create_content_item
  uuid = content_item.uuid

  url = f"{api_url}/{uuid}"
  resp = client_with_emulator.delete(url)
  del_json_response = resp.json()

  expected_data = {
      "success": True,
      "message": "Successfully deleted the content item"
  }
  assert resp.status_code == 200, "Status code not 200"
  assert del_json_response == expected_data, "Expected response not same"

  # assert that the content_item exists in the database and is soft deleted
  content_item = LTIContentItem.find_by_uuid(uuid, is_deleted=True)
  assert content_item


def test_delete_content_item_negative(clean_firestore):
  content_item_uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{content_item_uuid}"
  response = {
      "success": False,
      "message": "LTI Content item with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status code not404"
  assert json_response == response, "Expected response not same"


@pytest.mark.parametrize(
    "create_content_item", [(BASIC_CONTENT_ITEM_EXAMPLE)], indirect=True)
def test_get_content_items(clean_firestore, create_content_item):
  content_item = create_content_item

  # create an archived object
  archived_content_item_dict = copy.deepcopy(BASIC_CONTENT_ITEM_EXAMPLE)

  archived_content_item = LTIContentItem.from_dict(archived_content_item_dict)
  archived_content_item.uuid = ""
  archived_content_item.save()
  archived_content_item.uuid = archived_content_item.id
  archived_content_item.is_archived = True
  archived_content_item.update()

  params = {"skip": 0, "limit": "50"}

  params = {"skip": 0, "limit": "50"}
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_resources = [i.get("uuid") for i in json_response.get("data")]
  assert content_item.uuid in saved_resources, "all data not retrieved"
  assert archived_content_item.uuid in saved_resources, (
      "all data not retrieved")

  # Test archival functionality: Fetch all archived objects
  params = {"skip": 0, "limit": "50", "fetch_archive": True}
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_uuids = [i.get("uuid") for i in json_response.get("data")]
  assert archived_content_item.uuid in saved_uuids

  # Test archival functionality: Fetch all non archived objects
  params = {"skip": 0, "limit": "50", "fetch_archive": False}
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_uuids = [i.get("uuid") for i in json_response.get("data")]
  assert content_item.uuid in saved_uuids
