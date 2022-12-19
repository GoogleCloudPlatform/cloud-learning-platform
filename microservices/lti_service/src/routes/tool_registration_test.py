"""
  Unit tests for Tool Registration Endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
# pylint: disable=wrong-import-position
import os

os.environ["ISSUER"] = "http://localhost"
import copy
import pytest
import mock
from uuid import uuid4
from fastapi import FastAPI
from fastapi.testclient import TestClient
from testing.test_config import API_URL, DEL_KEYS
from common.models import Tool
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers
with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  from routes.tool_registration import router
  from schemas.schema_examples import BASIC_TOOL_EXAMPLE

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/lti-service/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/tool"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


@pytest.mark.parametrize("create_tool", [BASIC_TOOL_EXAMPLE], indirect=True)
def test_search_tool(clean_firestore, create_tool):
  tool = create_tool
  tool_dict = tool.get_fields(reformat_datetime=True)
  tool_dict["uuid"] = tool.id

  params = {"client_id": tool.client_id}

  url = f"{api_url}/search"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  modified_del_keys = DEL_KEYS + [
      "issuer", "platform_auth_url", "platform_token_url",
      "platform_keyset_url", "is_deleted", "created_by", "last_modified_by"
  ]
  for key in modified_del_keys:
    if key in json_response["data"][0]:
      del json_response["data"][0][key]
    if key in tool_dict:
      del tool_dict[key]
  assert resp.status_code == 200, "Status code not 200"
  assert json_response.get("data")[0] == tool_dict

  tool.is_deleted = True
  tool.update()

  params = {"client_id": tool.client_id}
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert json_response.get("data") is None


@pytest.mark.parametrize("create_tool", [BASIC_TOOL_EXAMPLE], indirect=True)
def test_get_tool(clean_firestore, create_tool):
  tool_dict = copy.deepcopy(BASIC_TOOL_EXAMPLE)
  tool = create_tool
  uuid = tool_dict["uuid"] = tool.id

  url = f"{api_url}/{uuid}"
  # fetch only the document with given uuid
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  modified_del_keys = DEL_KEYS + [
      "issuer", "platform_auth_url", "platform_token_url",
      "platform_keyset_url", "client_id", "deployment_id", "tool_public_key"
  ]
  for key in modified_del_keys:
    if key in json_response["data"]:
      del json_response["data"][key]
  del tool_dict["uuid"]
  assert resp.status_code == 200, "Status code not 200"
  assert json_response.get("data") == tool_dict, "Response received"


def test_get_tool_negative(clean_firestore):
  uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{uuid}"
  data = {
      "success": False,
      "message": f"Tool with uuid {uuid} not found",
      "data": None
  }

  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 404, "Status code not 404"
  assert json_response == data, "Response received"


def test_post_tool(clean_firestore):
  input_tool = copy.deepcopy(BASIC_TOOL_EXAMPLE)
  input_tool["tool_url"] = "https://testplatform.com/test-url"

  url = api_url
  for key in DEL_KEYS:
    if key in input_tool:
      del input_tool[key]
  post_resp = client_with_emulator.post(url, json=input_tool)
  assert post_resp.status_code == 200, "Status code not 200"

  post_json_response = post_resp.json()
  del post_json_response["data"]["created_timestamp"]
  del post_json_response["data"]["last_updated_timestamp"]
  uuid = post_json_response.get("data").get("uuid")

  # now see if GET endpoint returns same data
  url = f"{api_url}/{uuid}"
  get_resp = client_with_emulator.get(url)
  get_json_response = get_resp.json()
  del get_json_response["data"]["created_timestamp"]
  del get_json_response["data"]["last_updated_timestamp"]
  assert get_json_response.get("data") == post_json_response.get("data")


@pytest.mark.parametrize("create_tool", [BASIC_TOOL_EXAMPLE], indirect=True)
def test_update_tool(clean_firestore, create_tool):
  tool = create_tool
  tool_dict = tool.get_fields(reformat_datetime=True)
  tool_dict["name"] = "Test tool"

  modified_del_keys = DEL_KEYS + [
      "is_deleted", "last_modified_by", "created_by", "client_id",
      "deployment_id", "created_timestamp", "last_updated_timestamp"
  ]

  for key in modified_del_keys:
    if key in tool_dict:
      del tool_dict[key]

  url = f"{api_url}/{tool.uuid}"

  # Test to update the document
  resp = client_with_emulator.put(url, json=tool_dict)
  json_response_update_req = resp.json()
  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get(
      "message"
  ) == "Successfully updated the tool", \
  "Expected response not same"
  assert json_response_update_req.get("data").get("name") == "Test tool"


@pytest.mark.parametrize("create_tool", [BASIC_TOOL_EXAMPLE], indirect=True)
def test_update_tool_negative(clean_firestore, create_tool):
  tool_dict = copy.deepcopy(BASIC_TOOL_EXAMPLE)
  uuid = tool_dict["uuid"] = "U2DDBkl3Ayg0PWudzhI"

  url = f"{api_url}/{uuid}"
  response = {
      "success": False,
      "message": "Tool with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }

  # Negative test when updating the document itself with wrong uuid
  for key in DEL_KEYS:
    if key in tool_dict:
      del tool_dict[key]
  resp = client_with_emulator.put(url, json=tool_dict)
  json_response = resp.json()
  assert resp.status_code == 404, "Status code not 404"
  assert json_response == response, "Expected response not same"


@pytest.mark.parametrize("create_tool", [BASIC_TOOL_EXAMPLE], indirect=True)
def test_delete_tool(clean_firestore, create_tool):
  tool = create_tool
  uuid = tool.uuid

  url = f"{api_url}/{uuid}"
  resp = client_with_emulator.delete(url)
  del_json_response = resp.json()

  expected_data = {"success": True, "message": "Successfully deleted the tool"}
  assert resp.status_code == 200, "Status code not 200"
  assert del_json_response == expected_data, "Expected response not same"

  # assert that the tool exists in the database and is soft deleted
  tool = Tool.find_by_uuid(uuid, is_deleted=True)
  assert tool


def test_delete_tool_negative(clean_firestore):
  tool_uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{tool_uuid}"
  response = {
      "success": False,
      "message": "Tool with uuid U2DDBkl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status code not404"
  assert json_response == response, "Expected response not same"


@pytest.mark.parametrize("create_tool", [(BASIC_TOOL_EXAMPLE)], indirect=True)
def test_get_tools(clean_firestore, create_tool):
  tool = create_tool

  # create an archived object
  archived_tool_dict = copy.deepcopy(BASIC_TOOL_EXAMPLE)
  archived_tool_dict["tool_url"] = "https://testplatform.com/test-url"
  archived_tool_dict["client_id"] = str(uuid4())
  archived_tool_dict["deployment_id"] = str(uuid4())

  archived_tool = Tool.from_dict(archived_tool_dict)
  archived_tool.uuid = ""
  archived_tool.save()
  archived_tool.uuid = archived_tool.id
  archived_tool.is_archived = True
  archived_tool.update()

  params = {"skip": 0, "limit": "50"}

  params = {"skip": 0, "limit": "50"}
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_names = [i.get("name") for i in json_response.get("data")]
  assert tool.name in saved_names, "all data not retrived"
  assert archived_tool.name in saved_names, ("all data not retrived")

  # Test archival functionality: Fetch all archived objects
  params = {"skip": 0, "limit": "50", "fetch_archive": True}
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_uuids = [i.get("uuid") for i in json_response.get("data")]
  assert archived_tool.uuid in saved_uuids

  # Test archival functionality: Fetch all non archived objects
  params = {"skip": 0, "limit": "50", "fetch_archive": False}
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_uuids = [i.get("uuid") for i in json_response.get("data")]
  assert tool.uuid in saved_uuids
