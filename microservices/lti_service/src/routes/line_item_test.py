"""
  Unit tests for Line Item endpoints
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
from common.models import LineItem
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers
with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  from routes.line_item import router
  from schemas.schema_examples import (BASIC_LINE_ITEM_EXAMPLE,
                                       BASIC_TOOL_EXAMPLE)

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/lti-service/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/dummy_context_id/line_items"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_post_and_get_line_item(clean_firestore):
  input_line_item = copy.deepcopy(BASIC_LINE_ITEM_EXAMPLE)

  url = api_url
  post_resp = client_with_emulator.post(url, json=input_line_item)
  assert post_resp.status_code == 200, "Status code not 200 for POST line_item"

  post_json_response = post_resp.json()
  uuid = post_json_response.get("uuid")

  # now see if GET endpoint returns same data
  url = f"{api_url}/{uuid}"
  get_resp = client_with_emulator.get(url)
  get_json_response = get_resp.json()
  assert get_json_response == post_json_response


def test_negative_get_line_item(clean_firestore):
  # Hit GET endpoint with unknown id
  url = f"{api_url}/123123"
  get_resp = client_with_emulator.get(url)
  assert get_resp.status_code == 404


def test_get_all_line_items(clean_firestore):
  input_line_item = copy.deepcopy(BASIC_LINE_ITEM_EXAMPLE)

  url = api_url
  post_resp = client_with_emulator.post(url, json=input_line_item)
  assert post_resp.status_code == 200, "Status code not 200 for POST line_item"

  # now see if GET all endpoint returns data
  get_resp = client_with_emulator.get(url)
  get_json_response = get_resp.json()
  assert len(get_json_response) > 0


def test_update_line_item(clean_firestore):
  input_line_item = copy.deepcopy(BASIC_LINE_ITEM_EXAMPLE)

  url = api_url
  post_resp = client_with_emulator.post(url, json=input_line_item)
  assert post_resp.status_code == 200, "Status code not 200 for POST line_item"

  post_json_response = post_resp.json()
  print(post_json_response)
  uuid = post_json_response.get("uuid")

  # update line item here
  url = f"{api_url}/{uuid}"

  post_json_response["scoreMaximum"] = 100
  update_resp = client_with_emulator.put(url, json=post_json_response)
  assert update_resp.status_code == 200, "Status code not 200 for PUT line_item"

  update_json_response = update_resp.json()

  # now see if GET endpoint returns same data
  get_resp = client_with_emulator.get(url)
  get_json_response = get_resp.json()
  print(get_json_response)
  assert get_json_response["scoreMaximum"] == update_json_response[
      "scoreMaximum"]


def test_delete_line_item(clean_firestore):
  input_line_item = copy.deepcopy(BASIC_LINE_ITEM_EXAMPLE)

  url = api_url
  post_resp = client_with_emulator.post(url, json=input_line_item)
  assert post_resp.status_code == 200, "Status code not 200 for POST line_item"

  post_json_response = post_resp.json()
  print(post_json_response)
  uuid = post_json_response.get("uuid")

  # delete line item here
  url = f"{api_url}/{uuid}"
  delete_resp = client_with_emulator.delete(url)
  print("delete_resp.text", delete_resp.text)
  assert delete_resp.status_code == 200, \
  "Status code not 200 for DELETE line_item"
