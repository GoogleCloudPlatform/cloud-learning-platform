"""
  Tests for Content Selection endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import,line-too-long
import os
import mock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from common.utils.http_exceptions import add_exception_handlers
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from schemas.schema_examples import LTI_ASSIGNMENT_EXAMPLE
with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  with mock.patch("routes.content_selection.Logger"):
    from routes.content_selection import router
    from testing.test_config import API_URL

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/classroom-shim/api/v1")

client_with_emulator = TestClient(app)

os.environ[
    "PYTHONPATH"] = "/home/pavansareddy/Documents/Projects/SNHU/cloud-learning-platform/common/src"


def test_content_selection():
  """Test for content selection API"""
  test_tool_id = "W4Bg2Th1jYOwnt4"
  test_context_id = "V1v8Bn52b47IbM9"
  test_resp = {
      "tool_id": test_tool_id,
      "content_item_type": "",
      "content_item_info": {
          "name": "Test object"
      },
      "context_id": test_context_id,
  }
  with mock.patch(
      "routes.content_selection.list_content_items", return_value=[test_resp]):
    params = {"tool_id": test_tool_id}

    resp = client_with_emulator.get(
        f"{API_URL}/context/{test_context_id}/content-items", params=params)

    assert resp.status_code == 200, "Status should be 200"

    json_response = resp.json()
    tool_id_list = [i.get("tool_id") for i in json_response.get("data")]
    context_id_list = [i.get("context_id") for i in json_response.get("data")]

    assert test_resp["tool_id"] in tool_id_list
    assert test_resp["context_id"] in context_id_list
