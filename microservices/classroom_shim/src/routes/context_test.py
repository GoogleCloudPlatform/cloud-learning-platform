"""
  Tests for Context endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import,line-too-long
import os
from fastapi import FastAPI
from fastapi.testclient import TestClient
from common.utils.http_exceptions import add_exception_handlers
import mock
from schemas.schema_examples import CONTEXT_EXAMPLE
with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  with mock.patch("routes.lti_assignment.Logger"):
    from routes.context import router
    from testing.test_config import API_URL

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/classroom-shim/api/v1")

client_with_emulator = TestClient(app)

api_url = f"{API_URL}/contexts"


@mock.patch("routes.context.get_section_details")
def test_section_context(mock_section):
  """Test for context API to fetch the section details"""
  test_context_id = "BQ5M3b1vHS436n"

  mock_section.return_value = {**CONTEXT_EXAMPLE, "id": test_context_id}
  resp = client_with_emulator.get(f"{api_url}/{test_context_id}")

  assert resp.status_code == 200, "Status should be 200"

  json_response = resp.json()
  resp_data = json_response.get("data")
  assert json_response.get("success") is True, "Response is incorrect"
  assert resp_data.get("id") == test_context_id, "Incorrect response received"


@mock.patch("routes.context.get_section_details")
@mock.patch("routes.context.get_course_template_details")
def test_course_template_context(mock_course_template, mock_section):
  """Test for context API to fetch the course template details"""
  test_context_id = "BQ5M3b1vHS436n"

  mock_section.return_value = None
  mock_course_template.return_value = {**CONTEXT_EXAMPLE, "id": test_context_id}

  resp = client_with_emulator.get(f"{api_url}/{test_context_id}")

  assert resp.status_code == 200, "Status should be 200"

  json_response = resp.json()
  resp_data = json_response.get("data")
  assert json_response.get("success") is True, "Response is incorrect"
  assert resp_data.get("id") == test_context_id, "Incorrect response received"
