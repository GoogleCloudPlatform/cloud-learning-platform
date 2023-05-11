"""
  Unit tests for inspace endpoints
"""
import os
from uuid import uuid4
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from unittest import mock
from fastapi import FastAPI
from fastapi.testclient import TestClient

with mock.patch(
  "google.cloud.secretmanager.SecretManagerServiceClient",
  side_effect=mock.MagicMock()) as mok:
  from routes.inspace_token import router
from schemas.schema_examples import BASIC_USER_MODEL_EXAMPLE
from testing.test_config import API_URL
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.models import TempUser
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/authentication/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/inspace"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


class Request:
  """Mock class for Request"""

  def __init__(self, status_code) -> None:
    self.status_code = status_code

  def json(self):
    return {
      "token": "evbjguynkmjkj"
    }


class TokenGenerator:
  """Mock token gen"""

  def __init__(self) -> None:
    self.status_code = 200

  def json(self):
    return {"token": "evbjguynkmjkj"}


@mock.patch("routes.inspace_token.validate_token", return_value=True)
@mock.patch("routes.inspace_token.get_inspace_user_helper",
            return_value=(200, {"inspaceUser": {"id": 15309}}))
@mock.patch("routes.inspace_token.create_inspace_user_helper",
            return_value=True)
@mock.patch("routes.inspace_token.is_inspace_enabled",
            return_value=True)
@mock.patch("routes.inspace_token.get_inspace_token",
            return_value=TokenGenerator())
@mock.patch("common.utils.inspace.requests.get", return_value=Request(200))
def test_get_inspace_token_without_inspace_user(mock_validate_token,
                                                mock_user, mock_inspace_user,
                                                mock_inspace_api_call,
                                                mock_token, mock_req,
                                                clean_firestore):
  "Get the inspace token with correct user_id and no inspace user"
  user_dict = {**BASIC_USER_MODEL_EXAMPLE}
  user_dict["user_type_ref"] = ""
  user_dict["user_groups"] = []
  user_dict["email"] = f"{uuid4()}@gmail.com"
  user_dict["inspace_user"] = {
    "is_inspace_user": True,
    "inspace_user_id": ""
  }
  user = TempUser.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  user_dict["user_id"] = user.id

  headers = {"Authorization": "Bearer ey8273bqo...obx"}
  url = f"{api_url}/token/{user.user_id}"
  resp = client_with_emulator.get(url, headers=headers)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  assert json_response["data"]["token"] == "evbjguynkmjkj"
  assert json_response["message"] == "Successfully fetched the inspace token"

@mock.patch("routes.inspace_token.validate_token", return_value=True)
def test_get_inspace_token_with_inspace_user_false(mock_validate_token,
                                                   clean_firestore):
  "Should not get token with inspace user false"
  user_dict = {**BASIC_USER_MODEL_EXAMPLE}
  user_dict["user_type_ref"] = ""
  user_dict["user_groups"] = []
  user_dict["email"] = f"{uuid4()}@gmail.com"
  user_dict["inspace_user"] = {
    "is_inspace_user": False,
    "inspace_user_id": ""
  }
  user = TempUser.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  user_dict["user_id"] = user.id

  headers = {"Authorization": "Bearer ey8273bqo...obx"}
  url = f"{api_url}/token/{user.user_id}"
  resp = client_with_emulator.get(url, headers=headers)

  assert resp.status_code == 500
