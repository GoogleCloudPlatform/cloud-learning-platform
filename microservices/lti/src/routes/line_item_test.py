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
from testing.test_config import API_URL
from common.models import LineItem
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers
with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  from routes.line_item import router
  from schemas.schema_examples import (BASIC_LINE_ITEM_EXAMPLE,
                                       BASIC_SCORE_EXAMPLE)

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/lti/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/dummy_context_id/line_items"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

test_scope = {
    "scope":
        "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem \
          https://purl.imsglobal.org/spec/lti-ags/scope/lineitem.readonly \
            https://purl.imsglobal.org/spec/lti-ags/scope/score \
              https://purl.imsglobal.org/spec/lti-ags/scope/result.readonly"
}

test_keyset = {"public_keyset": "gGet21v2brb"}


@mock.patch("services.validate_service.get_platform_public_keyset")
@mock.patch("services.validate_service.decode_token")
@mock.patch("services.validate_service.get_unverified_token_claims")
def test_post_and_get_line_item(mock_unverified_token, mock_token_scopes,
                                mock_keyset, clean_firestore):
  mock_unverified_token.return_value = test_scope
  mock_token_scopes.return_value = test_scope
  mock_keyset.return_value = test_keyset
  input_line_item = copy.deepcopy(BASIC_LINE_ITEM_EXAMPLE)

  url = api_url
  headers = {"Authorization": "Bearer test_token"}
  post_resp = client_with_emulator.post(
      url, json=input_line_item, headers=headers)

  assert post_resp.status_code == 200, "Status code not 200 for POST line_item"

  post_json_response = post_resp.json()
  uuid = post_json_response.get("uuid")

  # now see if GET endpoint returns same data
  url = f"{api_url}/{uuid}"
  get_resp = client_with_emulator.get(url, headers=headers)
  get_json_response = get_resp.json()
  assert get_json_response == post_json_response


@mock.patch("services.validate_service.get_platform_public_keyset")
@mock.patch("services.validate_service.decode_token")
@mock.patch("services.validate_service.get_unverified_token_claims")
def test_negative_get_line_item(mock_unverified_token, mock_token_scopes,
                                mock_keyset, clean_firestore):
  mock_unverified_token.return_value = test_scope
  mock_token_scopes.return_value = test_scope
  mock_keyset.return_value = test_keyset
  # Hit GET endpoint with unknown id
  headers = {"Authorization": "Bearer test_token"}
  url = f"{api_url}/123123"
  get_resp = client_with_emulator.get(url, headers=headers)
  assert get_resp.status_code == 404


@mock.patch("services.validate_service.get_platform_public_keyset")
@mock.patch("services.validate_service.decode_token")
@mock.patch("services.validate_service.get_unverified_token_claims")
def test_get_all_line_items(mock_unverified_token, mock_token_scopes,
                            mock_keyset, clean_firestore):
  mock_unverified_token.return_value = test_scope
  mock_token_scopes.return_value = test_scope
  mock_keyset.return_value = test_keyset

  input_line_item = copy.deepcopy(BASIC_LINE_ITEM_EXAMPLE)

  url = api_url
  headers = {"Authorization": "Bearer test_token"}
  post_resp = client_with_emulator.post(
      url, json=input_line_item, headers=headers)
  assert post_resp.status_code == 200, "Status code not 200 for POST line_item"

  # now see if GET all endpoint returns data
  get_resp = client_with_emulator.get(url, headers=headers)
  get_json_response = get_resp.json()
  assert len(get_json_response) > 0


@mock.patch("services.validate_service.get_platform_public_keyset")
@mock.patch("services.validate_service.decode_token")
@mock.patch("services.validate_service.get_unverified_token_claims")
def test_update_line_item(mock_unverified_token, mock_token_scopes, mock_keyset,
                          clean_firestore):
  mock_unverified_token.return_value = test_scope
  mock_token_scopes.return_value = test_scope
  mock_keyset.return_value = test_keyset

  input_line_item = copy.deepcopy(BASIC_LINE_ITEM_EXAMPLE)

  headers = {"Authorization": "Bearer test_token"}
  url = api_url
  post_resp = client_with_emulator.post(
      url, json=input_line_item, headers=headers)
  assert post_resp.status_code == 200, "Status code not 200 for POST line_item"

  post_json_response = post_resp.json()
  print(post_json_response)
  uuid = post_json_response.get("uuid")

  # update line item here
  url = f"{api_url}/{uuid}"

  post_json_response["scoreMaximum"] = 100
  update_resp = client_with_emulator.put(
      url, json=post_json_response, headers=headers)
  assert update_resp.status_code == 200, "Status code not 200 for PUT line_item"

  update_json_response = update_resp.json()

  # now see if GET endpoint returns same data
  get_resp = client_with_emulator.get(url, headers=headers)
  get_json_response = get_resp.json()
  print(get_json_response)
  assert get_json_response["scoreMaximum"] == update_json_response[
      "scoreMaximum"]


@mock.patch("services.validate_service.get_platform_public_keyset")
@mock.patch("services.validate_service.decode_token")
@mock.patch("services.validate_service.get_unverified_token_claims")
def test_delete_line_item(mock_unverified_token, mock_token_scopes, mock_keyset,
                          clean_firestore):
  mock_unverified_token.return_value = test_scope
  mock_token_scopes.return_value = test_scope
  mock_keyset.return_value = test_keyset

  input_line_item = copy.deepcopy(BASIC_LINE_ITEM_EXAMPLE)

  headers = {"Authorization": "Bearer test_token"}
  url = api_url
  post_resp = client_with_emulator.post(
      url, json=input_line_item, headers=headers)
  assert post_resp.status_code == 200, "Status code not 200 for POST line_item"

  post_json_response = post_resp.json()
  print(post_json_response)
  uuid = post_json_response.get("uuid")

  # delete line item here
  url = f"{api_url}/{uuid}"
  delete_resp = client_with_emulator.delete(url, headers=headers)
  print("delete_resp.text", delete_resp.text)
  assert delete_resp.status_code == 200, \
  "Status code not 200 for DELETE line_item"


@mock.patch("services.validate_service.get_platform_public_keyset")
@mock.patch("services.validate_service.decode_token")
@mock.patch("services.validate_service.get_unverified_token_claims")
@pytest.mark.parametrize(
    "create_line_item", [BASIC_LINE_ITEM_EXAMPLE], indirect=True)
def test_post_score(mock_unverified_token, mock_token_scopes, mock_keyset,
                    clean_firestore, create_line_item):
  mock_unverified_token.return_value = test_scope
  mock_token_scopes.return_value = test_scope
  mock_keyset.return_value = test_keyset

  headers = {"Authorization": "Bearer test_token"}
  line_item = create_line_item
  line_item_id = line_item.uuid

  input_score = copy.deepcopy(BASIC_SCORE_EXAMPLE)
  url = f"{api_url}/{line_item_id}/scores"
  post_resp = client_with_emulator.post(url, json=input_score, headers=headers)

  assert post_resp.status_code == 200, "Status code not 200 for POST line_item"
  json_resp = post_resp.json()
  assert json_resp.get("userId") == input_score.get("userId")
