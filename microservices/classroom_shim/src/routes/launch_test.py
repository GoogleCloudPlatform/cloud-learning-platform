"""
  Tests for Context endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import,line-too-long
import os
import pytest
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
  with mock.patch("routes.launch.Logger"):
    from routes.launch import router
    from testing.test_config import API_URL

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/classroom-shim/api/v1")

client_with_emulator = TestClient(app)

os.environ[
    "PYTHONPATH"] = "/home/pavansareddy/Documents/Projects/SNHU/cloud-learning-platform/common/src"


@pytest.mark.parametrize(
    "create_lti_assignment", [LTI_ASSIGNMENT_EXAMPLE], indirect=True)
@mock.patch("routes.launch.get_teacher_details")
@mock.patch("routes.launch.get_student_details")
@mock.patch("routes.launch.get_user_details")
@mock.patch("common.utils.auth_service.validate_token")
def test_launch_assignment(
    mock_decoded_token,
    mock_user_data,
    mock_student_data,
    mock_teacher_data,
    clean_firestore,
    create_lti_assignment):
  """Test for launch assignment API"""
  test_assignment = create_lti_assignment
#   test_context_id = "BQ5M3b1vHS436n"
  mock_decoded_token.return_value = {"email": "testuser@email.com"}
  mock_user_data.return_value = {
      "data": [{
          "user_id": "Njy9sg2v9pnH6y8",
          "email": "testuser@email.com"
      }]
  }
  mock_teacher_data.return_value = {
      "user_id": "VmwB3s2nOsF42q8T",
      "user_type": "faculty",
      "status": "active",
      "email": "testuser@email.com"
  }
  mock_student_data.return_value = {
      "user_id": "V2e4brBn4uT78",
      "user_type": "student",
      "status": "active",
      "email": "testuser@email.com"
  }
  mock_decoded_token = {"email": "testuser@email.com"}
  params = {"lti_assignment_id": test_assignment.id}
  headers = {"Authorization": "Bearer asvm28.dsiq.vuwmo"}
  with mock.patch("common.utils.auth_service", return_value=mock_decoded_token):

    resp = client_with_emulator.get(
        f"{API_URL}/launch-assignment", headers=headers, params=params)

    print("Resp", resp.status_code, resp.text)
    assert resp.status_code == 200, "Status should be 200"
    json_response = resp.json()
    assert LTI_ASSIGNMENT_EXAMPLE.get("context_id") in json_response.get(
        "url"), "Incorrect response received"
    assert LTI_ASSIGNMENT_EXAMPLE.get(
        "lti_content_item_id") in json_response.get(
            "url"), "Incorrect response received"
