"""
  Tests for Launch endpoints
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
from schemas.schema_examples import INSERT_LTI_ASSIGNMENT_EXAMPLE
with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  with mock.patch("routes.launch.Logger"):
    from routes.launch import router, validate_token
    from testing.test_config import API_URL

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/classroom-shim/api/v1")

client_with_emulator = TestClient(app)


def mock_learner_token():
  return {"email": "testuser@email.com", "user_type": "learner"}


def mock_faculty_token():
  return {"email": "testuser@email.com", "user_type": "faculty"}


@pytest.mark.parametrize(
    "create_lti_assignment", [INSERT_LTI_ASSIGNMENT_EXAMPLE], indirect=True)
@mock.patch("routes.launch.get_student_details")
@mock.patch("routes.launch.get_user_details")
def test_launch_assignment_section_student(mock_user_data, mock_student_data,
                                           clean_firestore,
                                           create_lti_assignment):
  """Test for launch assignment API"""
  email = "testuser@email.com"
  user_type = "learner"
  app.dependency_overrides[validate_token] = mock_learner_token
  test_assignment = create_lti_assignment
  mock_user_data.return_value = {
      "success": True,
      "data": [{
          "user_id": "Njy9sg2v9pnH6y8",
          "email": email
      }]
  }
  mock_student_data.return_value = {
      "user_id": "V2e4brBn4uT78",
      "user_type": user_type,
      "status": "active",
      "email": email
  }
  params = {"lti_assignment_id": test_assignment.id}
  headers = {"Authorization": "Bearer asvm28.dsiq.vuwmo"}

  resp = client_with_emulator.get(
      f"{API_URL}/launch-assignment", headers=headers, params=params)

  assert resp.status_code == 200, "Status should be 200"
  json_response = resp.json()
  assert INSERT_LTI_ASSIGNMENT_EXAMPLE.get("context_id") in json_response.get(
      "url"), "Incorrect response received"
  assert INSERT_LTI_ASSIGNMENT_EXAMPLE.get(
      "lti_content_item_id") in json_response.get(
          "url"), "Incorrect response received"


@pytest.mark.parametrize(
    "create_lti_assignment", [INSERT_LTI_ASSIGNMENT_EXAMPLE], indirect=True)
@mock.patch("routes.launch.get_teacher_details")
@mock.patch("routes.launch.get_user_details")
def test_launch_assignment_section_teacher(mock_user_data, mock_teacher_data,
                                           clean_firestore,
                                           create_lti_assignment):
  """Test for launch assignment API"""
  email = "testuser@email.com"
  user_type = "faculty"
  app.dependency_overrides[validate_token] = mock_faculty_token
  test_assignment = create_lti_assignment
  mock_user_data.return_value = {
      "success": True,
      "data": [{
          "user_id": "Njy9sg2v9pnH6y8",
          "email": email
      }]
  }
  mock_teacher_data.return_value = {
      "user_id": "VmwB3s2nOsF42q8T",
      "user_type": user_type,
      "status": "active",
      "email": email
  }
  params = {"lti_assignment_id": test_assignment.id}
  headers = {"Authorization": "Bearer asvm28.dsiq.vuwmo"}

  resp = client_with_emulator.get(
      f"{API_URL}/launch-assignment", headers=headers, params=params)

  assert resp.status_code == 200, "Status should be 200"
  json_response = resp.json()
  assert INSERT_LTI_ASSIGNMENT_EXAMPLE.get("context_id") in json_response.get(
      "url"), "Incorrect response received"
  assert INSERT_LTI_ASSIGNMENT_EXAMPLE.get(
      "lti_content_item_id") in json_response.get(
          "url"), "Incorrect response received"


test_example = {
    **INSERT_LTI_ASSIGNMENT_EXAMPLE, "context_type": "course_template"
}


@pytest.mark.parametrize("create_lti_assignment", [test_example], indirect=True)
@mock.patch("routes.launch.get_instruction_designer_details")
@mock.patch("routes.launch.get_user_details")
def test_launch_assignment_course_template(mock_user_data, mock_id_data,
                                           clean_firestore,
                                           create_lti_assignment):
  """Test for launch assignment API"""
  email = "testuser@email.com"
  user_type = "faculty"
  app.dependency_overrides[validate_token] = mock_faculty_token
  test_assignment = create_lti_assignment
  mock_user_data.return_value = {
      "success": True,
      "data": [{
          "user_id": "Njy9sg2v9pnH6y8",
          "email": email
      }]
  }
  mock_id_data.return_value = {
      "user_id": "VmwB3s2nOsF42q8T",
      "user_type": user_type,
      "status": "active",
      "email": email
  }
  params = {"lti_assignment_id": test_assignment.id}
  headers = {"Authorization": "Bearer asvm28.dsiq.vuwmo"}

  resp = client_with_emulator.get(
      f"{API_URL}/launch-assignment", headers=headers, params=params)

  assert resp.status_code == 200, "Status should be 200"
  json_response = resp.json()
  assert INSERT_LTI_ASSIGNMENT_EXAMPLE.get("context_id") in json_response.get(
      "url"), "Incorrect response received"
  assert INSERT_LTI_ASSIGNMENT_EXAMPLE.get(
      "lti_content_item_id") in json_response.get(
          "url"), "Incorrect response received"
