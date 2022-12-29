"""
  Unit tests for LTI Platform Auth endpoints
"""
import os
import pytest
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import, line-too-long

from fastapi import FastAPI
from fastapi.testclient import TestClient
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers
from testing.test_config import API_URL
import mock
with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  from routes.platform_auth import router
  from schemas.schema_examples import BASIC_TOOL_EXAMPLE

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/lti/api/v1")

client_with_emulator = TestClient(app)

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

test_key_set = {
    "key": "test_rsa_key",
    "key_id": "key_hash_value",
    "public_keyset": {
        "keys": [{
            "kty": "RSA",
            "alg": "RS256",
            "kid": "key_hash_value",
            "use": "sig",
            "e": "v92b7ey9o",
            "n": "obvr189yr398bPNv"
        }]
    },
    "web_key": {
        "kty": "RSA",
        "alg": "RS256",
        "kid": "key_hash_value",
        "use": "sig",
        "e": "v92b7ey9o",
        "n": "obvr189yr398bPNv"
    }
}


@mock.patch("routes.platform_auth.get_platform_public_keyset")
def test_jwks(mock_key_set, clean_firestore):
  mock_key_set.return_value = test_key_set
  url = f"{API_URL}/jwks"
  resp = client_with_emulator.get(url)

  assert resp.status_code == 200
  assert resp.json() == test_key_set.get("public_keyset")


@mock.patch("routes.platform_auth.generate_token_claims")
@mock.patch("routes.platform_auth.encode_token")
def test_authorize(mock_token, mock_key_set, clean_firestore):
  test_token = "ey7abos8f.8astvd9q.87cb"
  mock_token.return_value = test_token
  req_params = {
      "client_id": "test_client_id",
      "login_hint": "test_user_id",
      "lti_message_hint": "test_resource_id",
      "redirect_uri": "test_redirect_uri",
      "nonce": "1tr8b174b7134813v",
      "state": "b54b725vt9y9",
      "scope": "openid",
      "response_type": "id_token",
      "response_mode": "form_post",
      "prompt": "none"
  }
  mock_key_set.return_value = test_key_set
  url = f"{API_URL}/authorize"
  resp = client_with_emulator.get(url, params=req_params)

  assert resp.status_code == 200
  assert resp.context.get("id_token") == test_token


@pytest.mark.parametrize("create_tool", [BASIC_TOOL_EXAMPLE], indirect=True)
@mock.patch("routes.platform_auth.get_remote_keyset")
@mock.patch("routes.platform_auth.get_unverified_token_claims")
@mock.patch("routes.platform_auth.decode_token")
def test_token(mock_token, mock_claims, mock_key_set, clean_firestore,
               create_tool):

  test_tool = create_tool
  test_claims = {
      "iss": test_tool.tool_url,
      "iat": "token_issued_time",
      "exp": "token_expired_time",
      "aud": "audience_token_url",
      "sub": test_tool.client_id
  }

  mock_token.return_value = test_claims
  mock_claims.return_value = test_claims

  req_data = {
      "grant_type":
          "client_credentials",
      "client_assertion_type":
          "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
      "client_assertion":
          "ey7ot812b.t3s4vb7kra3.tb7i3vsatb92va2tovn",
      "scope":
          "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem"
  }
  mock_key_set.return_value = test_key_set
  url = f"{API_URL}/token"
  headers = {"Content-Type": "application/x-www-form-urlencoded"}
  resp = client_with_emulator.post(url, data=req_data, headers=headers)

  assert resp.status_code == 200
  json_res = resp.json()
  assert json_res.get("sub") == test_claims.get("sub")
