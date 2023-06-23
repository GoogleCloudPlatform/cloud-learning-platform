"""
  Tests for User Shim endpoints
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
with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  with mock.patch("routes.user_shim.Logger"):
    from routes.user_shim import router
    from testing.test_config import API_URL

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/classroom-shim/api/v1")

client_with_emulator = TestClient(app)


@mock.patch("routes.user_shim.get_user_details")
def test_search_user(mock_user_data, clean_firestore):
  """Test for launch assignment API"""
  email = "testuser@email.com"
  mock_user_data.return_value = {
      "success": True,
      "data": [{
          "user_id": "Njy9sg2v9pnH6y8",
          "email": email
      }]
  }
  headers = {"Authorization": "Bearer asvm28.dsiq.vuwmo"}

  params = {"email": email}
  resp = client_with_emulator.get(
      f"{API_URL}/user/search/email", headers=headers, params=params)

  print("Resp", resp.status_code, resp.text)
  assert resp.status_code == 200, "Status should be 200"
  json_response = resp.json()
  assert len(json_response.get("data")) != 0, "Incorrect response received"
  assert email == json_response.get("data")[0].get(
      "email"), "Incorrect response received"
