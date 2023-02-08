"""
  Unit tests for Platform Registration Endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
# pylint: disable=wrong-import-position
import os
import copy
import pytest
import mock
from uuid import uuid4
from fastapi import FastAPI
from fastapi.testclient import TestClient
from testing.test_config import API_URL, DEL_KEYS
from common.models import Platform
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers
with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  from schemas.schema_examples import BASIC_PLATFORM_EXAMPLE
  from routes.platform_registration import router

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/lti/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/platform"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


@pytest.mark.parametrize(
    "create_platform", [BASIC_PLATFORM_EXAMPLE], indirect=True)
def test_search_platform(clean_firestore, create_platform):
  platform = create_platform
  platform_dict = platform.get_fields(reformat_datetime=True)
  platform_dict["id"] = platform.id
  params = {"client_id": platform.client_id}

  url = f"{api_url}/search"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  modified_del_keys = DEL_KEYS + [
      "id", "tool_url", "tool_login_url", "tool_keyset_url"
  ]
  for key in modified_del_keys:
    if key in json_response["data"][0]:
      del json_response["data"][0][key]
    if key in platform_dict:
      del platform_dict[key]
  assert resp.status_code == 200, "Status code not 200"
  assert json_response.get("data")[0] == platform_dict


@pytest.mark.parametrize(
    "create_platform", [BASIC_PLATFORM_EXAMPLE], indirect=True)
def test_get_platform(clean_firestore, create_platform):
  platform_dict = copy.deepcopy(BASIC_PLATFORM_EXAMPLE)
  platform = create_platform
  platform_id = platform_dict["id"] = platform.id

  url = f"{api_url}/{platform_id}"
  # fetch only the document with given uuid
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  modified_del_keys = DEL_KEYS + [
      "tool_url", "tool_login_url", "tool_keyset_url"
  ]
  for key in modified_del_keys:
    if key in json_response["data"]:
      del json_response["data"][key]
  del platform_dict["id"]
  assert resp.status_code == 200, "Status code not 200"
  assert json_response.get("data") == platform_dict, "Response received"


def test_get_platform_negative(clean_firestore):
  platform_id = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{platform_id}"
  data = {
      "success": False,
      "message": f"platforms with id {platform_id} is not found",
      "data": None
  }

  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 404, "Status code not 404"
  assert json_response == data, "Response received"


def test_post_platform(clean_firestore):
  input_platform = copy.deepcopy(BASIC_PLATFORM_EXAMPLE)

  url = api_url
  for key in DEL_KEYS:
    if key in input_platform:
      del input_platform[key]
  post_resp = client_with_emulator.post(url, json=input_platform)
  post_json_response = post_resp.json()
  assert post_resp.status_code == 200, "Status code not 200"
  del post_json_response["data"]["created_time"]
  del post_json_response["data"]["last_modified_time"]
  platform_id = post_json_response.get("data").get("id")

  # now see if GET endpoint returns same data
  url = f"{api_url}/{platform_id}"
  get_resp = client_with_emulator.get(url)
  get_json_response = get_resp.json()
  del get_json_response["data"]["created_time"]
  del get_json_response["data"]["last_modified_time"]
  assert get_json_response.get("data") == post_json_response.get("data")


@pytest.mark.parametrize(
    "create_platform", [BASIC_PLATFORM_EXAMPLE], indirect=True)
def test_update_platform(clean_firestore, create_platform):
  platform = create_platform
  platform_dict = platform.get_fields(reformat_datetime=True)
  platform_dict["name"] = "Test platform"

  modified_del_keys = DEL_KEYS + [
      "is_deleted", "last_modified_by", "created_by", "created_time",
      "last_modified_time"
  ]

  for key in modified_del_keys:
    if key in platform_dict:
      del platform_dict[key]

  url = f"{api_url}/{platform.id}"

  # Test to update the document
  resp = client_with_emulator.put(url, json=platform_dict)
  json_response_update_req = resp.json()
  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get(
      "message"
  ) == "Successfully updated the platform", \
  "Expected response not same"
  assert json_response_update_req.get("data").get("name") == "Test platform"


@pytest.mark.parametrize(
    "create_platform", [BASIC_PLATFORM_EXAMPLE], indirect=True)
def test_update_platform_negative(clean_firestore, create_platform):
  platform_dict = copy.deepcopy(BASIC_PLATFORM_EXAMPLE)
  platform_id = platform_dict["id"] = "U2DDBkl3Ayg0PWudzhI"

  url = f"{api_url}/{platform_id}"
  response = {
      "success": False,
      "message": "platforms with id U2DDBkl3Ayg0PWudzhI is not found",
      "data": None
  }

  # Negative test when updating the document itself with wrong id
  for key in DEL_KEYS:
    if key in platform_dict:
      del platform_dict[key]
  resp = client_with_emulator.put(url, json=platform_dict)
  json_response = resp.json()
  assert resp.status_code == 404, "Status code not 404"
  assert json_response == response, "Expected response not same"


@pytest.mark.parametrize(
    "create_platform", [BASIC_PLATFORM_EXAMPLE], indirect=True)
def test_delete_platform(clean_firestore, create_platform):
  platform = create_platform
  platform_id = platform.id

  url = f"{api_url}/{platform_id}"
  resp = client_with_emulator.delete(url)
  del_json_response = resp.json()

  expected_data = {
      "success": True,
      "message": "Successfully deleted the platform"
  }
  assert resp.status_code == 200, "Status code not 200"
  assert del_json_response == expected_data, "Expected response not same"


def test_delete_platform_negative(clean_firestore):
  platform_id = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{platform_id}"
  response = {
      "success": False,
      "message": "platforms with id U2DDBkl3Ayg0PWudzhI is not found",
      "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()
  print("resp.status_code", resp.status_code)
  assert resp.status_code == 404, "Status code not 404"
  assert json_response == response, "Expected response not same"


@pytest.mark.parametrize(
    "create_platform", [(BASIC_PLATFORM_EXAMPLE)], indirect=True)
def test_get_platforms(clean_firestore, create_platform):
  platform = create_platform

  params = {"skip": 0, "limit": "50"}
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  saved_names = [i.get("name") for i in json_response.get("data")]
  assert platform.name in saved_names, "all data not retrieved"
