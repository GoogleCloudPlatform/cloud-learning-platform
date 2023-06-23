"""
  Unit tests for Authentication endpoint
"""
# from unittest import mock
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
import os
from unittest import mock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from common.models import TempUser
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers
from utils.exception_handler import InvalidRefreshTokenError
from routes.refresh_token import router
from schemas.schema_examples import BASIC_USER_MODEL_EXAMPLE

API_URL = "http://localhost/authentication/api/v1"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

app = FastAPI()
app.include_router(router, prefix="/authentication/api/v1")
add_exception_handlers(app)

client = TestClient(app)

token_credentials = {
    "access_token": "eyJhbGciOiJSU........C7h4w",
    "expires_in": "3600",
    "token_type": "Bearer",
    "refresh_token": "AEu4IL2njCpop7p.......CU6sm8",
    "id_token": "eyJhbGciOiJSU.......G2rC7h4w",
    "user_id": "fiurc756IqcdRSs19upxiVLt1Gr2",
    "project_id": "test-project"
}

auth_details = {
    "name": "Test User",
    "picture": "https://lh3.googleusercontent.com/-I8CTmvNmtLE\
      /AAAAAAAAAAI/AAAAAAAAAAA/ACHi3rdBqybASKV35NeQTu_cEL5eTO5G9w/photo.jpg",
    "iss": "https://securetoken.google.com/my-dummy-project",
    "aud": "my-dummy-project",
    "auth_time": 1579875095,
    "user_id": "fiurc756IqcdRSs19upxiVLt1Gr2",
    "sub": "fiurc756IqcdRSs19upxiVLt1Gr2",
    "iat": 1579875097,
    "exp": 1579878697,
    "email": "test.user@gmail.com",
    "email_verified": True,
    "firebase": {
        "identities": {
            "google.com": [104415576250754890000],
            "microsoft.com": ["96d7dbe4-0abf-495c-bd1d-cab8af465ac4"],
            "email": ["test.user@gmail.com"]
        },
        "sign_in_provider": "google.com"
    },
    "uid": "fiurc756IqcdRSs19upxiVLt1Gr2"
}


@mock.patch("services.firebase_authentication.auth")
@mock.patch("routes.refresh_token.generate_token")
def test_valid_id(mock_generate_token, mock_auth, clean_firestore):

  mock_auth.verify_id_token.return_value = auth_details
  mock_generate_token.return_value = token_credentials

  # new_user = {**BASIC_USER_MODEL_EXAMPLE, "email": USER_EMAIL}
  new_user = BASIC_USER_MODEL_EXAMPLE
  user = TempUser.from_dict(new_user)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  url = f"{API_URL}/generate"

  response = client.post(url, json={"refresh_token": "foobar"})
  assert response.status_code == 200


def test_valid_id_error(mocker):
  url = f"{API_URL}/generate"
  mocker.patch("routes.refresh_token.generate_token"
              ).side_effect = InvalidRefreshTokenError("invalid")
  response = client.post(url, json={"refresh_token": "foobar"})
  assert response.json().get("message") == "invalid"
