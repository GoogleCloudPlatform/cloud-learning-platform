"""
  Tests for Grade endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import,line-too-long
import os
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from common.models import LTIAssignment
from common.testing.firestore_emulator import firestore_emulator, clean_firestore
from common.utils.http_exceptions import add_exception_handlers
import mock
with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  with mock.patch("routes.lti_assignment.Logger"):
    from routes.grade import router
    from schemas.schema_examples import INSERT_LTI_ASSIGNMENT_EXAMPLE, LTI_POST_GRADE_MODEL
    from testing.test_config import API_URL

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/classroom-shim/api/v1")

client_with_emulator = TestClient(app)

api_url = f"{API_URL}/grade"


@pytest.fixture
def create_lti_assignment():
  lti_assignment = LTIAssignment.from_dict(INSERT_LTI_ASSIGNMENT_EXAMPLE)
  lti_assignment.save()
  return lti_assignment


def test_grade(create_lti_assignment):
  lti_assignment = create_lti_assignment

  input_json = {
      **LTI_POST_GRADE_MODEL, "lti_content_item_id":
          lti_assignment.lti_content_item_id
  }
  with mock.patch("routes.grade.auth_client.get_id_token", return_value=True):
    with mock.patch(
        "routes.grade.get_submitted_course_work_list",
        return_value=[{
            "id": "jsh2g1jw3"
        }]):
      with mock.patch("routes.grade.post_grade_of_the_user", return_value=True):
        resp = client_with_emulator.post(api_url, json=input_json)
        assert resp.status_code == 200, "Status should be 200"

        json_response = resp.json()
        print("resp", resp)
        assert json_response.get("success") is True
