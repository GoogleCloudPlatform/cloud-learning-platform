"""
  Unit tests for Results endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
# pylint: disable=wrong-import-position,line-too-long
import os
import copy
import mock
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from testing.test_config import API_URL
from common.models import LineItem, LTIContentItem, Result
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers
from config import LTI_ISSUER_DOMAIN
from schemas.schema_examples import (BASIC_TOOL_EXAMPLE, POST_LINE_ITEM_EXAMPLE,
                                     BASIC_LINE_ITEM_EXAMPLE,
                                     BASIC_RESULT_EXAMPLE,
                                     BASIC_CONTENT_ITEM_EXAMPLE,
                                     BASIC_SCORE_EXAMPLE)
from uuid import uuid4
with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  from routes.results import router

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/lti/api/v1")

client_with_emulator = TestClient(app)

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

# assigning url
context_id = POST_LINE_ITEM_EXAMPLE["contextId"]
api_url = f"{API_URL}/admin/{context_id}/line_items"


@pytest.mark.parametrize("create_tool", [BASIC_TOOL_EXAMPLE], indirect=True)
def test_post_result(create_tool, clean_firestore):

  test_tool = create_tool

  content_item_example = {
      **BASIC_CONTENT_ITEM_EXAMPLE, "context_id": context_id,
      "tool_id": test_tool.id
  }

  content_item = LTIContentItem.from_dict(content_item_example)
  content_item.save()
  content_item_id = content_item.id

  input_line_item = {
      **POST_LINE_ITEM_EXAMPLE, "resourceLinkId": content_item_id
  }
  line_item = LineItem.from_dict(input_line_item)
  line_item.save()
  line_item_id = line_item.id

  input_result = {
      **BASIC_RESULT_EXAMPLE, "isGradeSyncCompleted": False,
      "lineItemId": line_item_id
  }
  result = Result.from_dict(input_result)
  result.save()
  result_id = result.id

  url = f"{api_url}/{line_item_id}/results"
  get_resp = client_with_emulator.get(url)

  assert get_resp.status_code == 200, "Status code not 200 for GET result"
  json_resp = get_resp.json()

  resp_ids = [i.get("id") for i in json_resp.get("data")]
  res_id = f"{LTI_ISSUER_DOMAIN}/lti/api/v1/{context_id}/line_items/{line_item_id}/results/{result_id}"

  assert res_id in resp_ids, "Incorrect response"


@pytest.mark.parametrize("create_tool", [BASIC_TOOL_EXAMPLE], indirect=True)
def test_get_result(create_tool, clean_firestore):

  test_tool = create_tool

  content_item_example = {
      **BASIC_CONTENT_ITEM_EXAMPLE, "context_id": context_id,
      "tool_id": test_tool.id
  }

  content_item = LTIContentItem.from_dict(content_item_example)
  content_item.save()
  content_item_id = content_item.id

  input_line_item = {
      **POST_LINE_ITEM_EXAMPLE, "resourceLinkId": content_item_id
  }
  line_item = LineItem.from_dict(input_line_item)
  line_item.save()
  line_item_id = line_item.id

  input_result = {
      **BASIC_RESULT_EXAMPLE, "isGradeSyncCompleted": False,
      "lineItemId": line_item_id
  }
  result = Result.from_dict(input_result)
  result.save()
  result_id = result.id

  url = f"{api_url}/{line_item_id}/results/{result_id}"
  get_resp = client_with_emulator.get(url)

  assert get_resp.status_code == 200, "Status code not 200 for GET result"

  json_resp = get_resp.json()
  result_data = json_resp.get("data")

  res_id = f"{LTI_ISSUER_DOMAIN}/lti/api/v1/{context_id}/line_items/{line_item_id}/results/{result_id}"
  assert result_data.get("id") == res_id, "Incorrect response received"


@pytest.mark.parametrize("create_tool", [BASIC_TOOL_EXAMPLE], indirect=True)
def test_update_result(create_tool, clean_firestore):

  test_tool = create_tool

  content_item_example = {
      **BASIC_CONTENT_ITEM_EXAMPLE, "context_id": context_id,
      "tool_id": test_tool.id
  }

  content_item = LTIContentItem.from_dict(content_item_example)
  content_item.save()
  content_item_id = content_item.id

  input_line_item = {
      **POST_LINE_ITEM_EXAMPLE, "resourceLinkId": content_item_id
  }
  line_item = LineItem.from_dict(input_line_item)
  line_item.save()
  line_item_id = line_item.id

  input_result = {
      **BASIC_RESULT_EXAMPLE, "isGradeSyncCompleted": False,
      "lineItemId": line_item_id
  }
  result = Result.from_dict(input_result)
  result.save()
  result_id = result.id

  url = f"{api_url}/{line_item_id}/results/{result_id}"
  update_result = {"isGradeSyncCompleted": True}
  patch_resp = client_with_emulator.patch(url, json=update_result)

  assert patch_resp.status_code == 200, "Status code not 200 for PATCH result"

  url = f"{api_url}/{line_item_id}/results/{result_id}"
  get_resp = client_with_emulator.get(url)

  assert get_resp.status_code == 200, "Status code not 200 for GET result"

  json_resp = get_resp.json()
  result_data = json_resp.get("data")

  assert result_data.get(
      "isGradeSyncCompleted") is True, "Incorrect response received"
