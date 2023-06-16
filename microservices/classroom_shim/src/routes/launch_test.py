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
from schemas.schema_examples import CONTEXT_EXAMPLE, CONTEXT_MEMBERS_EXAMPLE
with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  with mock.patch("routes.launch.Logger"):
    from routes.launch import router
    from testing.test_config import API_URL

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/classroom-shim/api/v1")

client_with_emulator = TestClient(app)


@mock.patch("routes.context.get_teacher_details")
@mock.patch("routes.context.get_student_details")
@mock.patch("routes.context.get_instruction_designer_details")
@mock.patch("routes.context.user_details")
@mock.patch("routes.context.validate_token")
def test_launch_assignment(mock_decoded_token, mock_user_data, mock_id_data,
                           mock_student_data, mock_teacher_data):
  """Test for launch assignment API"""
  test_context_id = "BQ5M3b1vHS436n"
  mock_decoded_token = {"email": "testuser@email.com"}
  mock_user_data.return_value = {
      "user_id": "Njy9sg2v9pnH6y8",
      "email": "testuser@email.com"
  }
  resp = client_with_emulator.get(f"{API_URL}/launch-assignment")

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


@mock.patch("routes.context.get_instructional_designers")
def test_course_template_context_members(mock_ids):
  """Test for Get context members API to fetch the members of course template"""
  test_context_id = "BQ5M3b1vHS436n"

  mock_ids.return_value = [CONTEXT_MEMBERS_EXAMPLE]
  query_params = {"context_type": "course_template"}
  resp = client_with_emulator.get(
      f"{api_url}/{test_context_id}/members", params=query_params)

  assert resp.status_code == 200, "Status should be 200"

  json_response = resp.json()
  resp_data = json_response.get("data")
  assert json_response.get("success") is True, "Response is incorrect"
  user_id_list = [i.get("user_id") for i in resp_data]
  assert CONTEXT_MEMBERS_EXAMPLE[
      "user_id"] in user_id_list, "Incorrect response received"
