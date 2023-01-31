"""
  Unit tests for LTI Tool Auth endpoints
"""
import os
from testing.test_config import API_URL, generate_test_rsa_private_key

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

# disabling pylint rules that conflict with pytest fixtures and linter
# pylint: disable=unused-argument,redefined-outer-name,unused-import,
# pylint: disable=wrong-import-position

import pytest
import mock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  from routes.tool_auth import router
  from schemas.schema_examples import BASIC_PLATFORM_EXAMPLE

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/lti/api/v1")

client_with_emulator = TestClient(app)


@pytest.mark.parametrize(
    "create_platform", [BASIC_PLATFORM_EXAMPLE], indirect=True)
def test_jwks(clean_firestore, create_platform, mocker):
  platform = create_platform
  platform_dict = platform.get_fields(reformat_datetime=True)
  platform_id = platform_dict["id"] = platform.id

  url = f"{API_URL}/jwks/{platform_id}"
  private_key = generate_test_rsa_private_key()
  mocker.patch(
      "services.keys_manager.get_tool_private_key", return_value=private_key)
  get_resp = client_with_emulator.get(url)
  assert get_resp.status_code == 200


def test_jwks_negative(clean_firestore):
  platform_id = "1234"
  url = f"{API_URL}/jwks/{platform_id}"
  get_resp = client_with_emulator.get(url)

  assert get_resp.status_code == 404


@pytest.mark.parametrize(
    "create_platform", [BASIC_PLATFORM_EXAMPLE], indirect=True)
def test_oidc_login(clean_firestore, create_platform):
  platform = create_platform
  platform_dict = platform.get_fields(reformat_datetime=True)
  platform_dict["id"] = platform.id

  url = f"{API_URL}/oidc-login"

  input_data = {
      "iss": platform_dict["issuer"],
      "client_id": platform_dict["client_id"],
      "target_link_uri": "https://test_target_link.com",
      "login_hint": "123"
  }
  headers = {"Content-Type": "application/x-www-form-urlencoded"}
  post_resp = client_with_emulator.post(url, data=input_data, headers=headers)

  assert post_resp.status_code == 302


@pytest.mark.parametrize(
    "create_platform", [BASIC_PLATFORM_EXAMPLE], indirect=True)
def test_oidc_login_negative_client_id(clean_firestore, create_platform):
  platform = create_platform
  platform_dict = platform.get_fields(reformat_datetime=True)
  platform_dict["id"] = platform.id

  url = f"{API_URL}/oidc-login"

  test_client_id = "test_client_id"
  input_data = {
      "iss": platform_dict["issuer"],
      "client_id": test_client_id,
      "target_link_uri": "https://test_target_link.com",
      "login_hint": "123"
  }
  headers = {"Content-Type": "application/x-www-form-urlencoded"}
  post_resp = client_with_emulator.post(url, data=input_data, headers=headers)
  assert post_resp.status_code == 422


def test_oidc_login_negative_iss(clean_firestore,):
  url = f"{API_URL}/oidc-login"

  iss = "issuer"
  input_data = {
      "iss": iss,
      "client_id": "client_id",
      "target_link_uri": "https://test_target_link.com",
      "login_hint": "123"
  }
  headers = {"Content-Type": "application/x-www-form-urlencoded"}
  post_resp = client_with_emulator.post(url, data=input_data, headers=headers)
  output_resp = post_resp.json()

  assert post_resp.status_code == 404
  assert output_resp.get("message") == f"Platform with issuer '{iss}' not found"
