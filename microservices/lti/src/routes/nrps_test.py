"""
  Unit tests for NRPS endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
# pylint: disable=wrong-import-position
import os
import mock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from testing.test_config import API_URL
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers
with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  from routes.nrps import router
  from schemas.schema_examples import NRPS_EXAMPLE

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/lti/api/v1")

client_with_emulator = TestClient(app)

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

test_scope = {
    "scope":
        "https://purl.imsglobal.org/spec/lti-nrps/scope/contextmembership.readonly"
}

test_keyset = {"public_keyset": "N34m5wn83m490V4"}


@mock.patch("services.validate_service.get_platform_public_keyset")
@mock.patch("services.validate_service.decode_token")
@mock.patch("services.validate_service.get_unverified_token_claims")
# @mock.patch("common.utils.secrets.get_backend_robot_id_token")
@mock.patch("utils.setup.get_method")
def test_get_members(mock_token, mock_unverified_token, mock_token_scopes,
                     mock_keyset, clean_firestore):

  mock_unverified_token.return_value = test_scope
  mock_token_scopes.return_value = test_scope
  mock_keyset.return_value = test_keyset
  mock_token.return_value = "test_token"

  url = f"{API_URL}/temp_context_id/memberships"
  headers = {"Authorization": "Bearer test_token"}
  get_resp = client_with_emulator.get(url, headers=headers)

  print("get_resp", get_resp.json())
  assert get_resp.status_code == 200, "Status code not 200"

  get_json_response = get_resp.json()

  assert get_json_response == 121
