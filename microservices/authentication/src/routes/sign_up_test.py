"""
  Unit tests for Sign Up endpoints
"""
from unittest import mock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.sign_up import router
from testing.test_config import API_URL
from common.utils.http_exceptions import add_exception_handlers
from schemas.schema_examples import (
  SIGN_UP_WITH_CREDENTIALS_API_INPUT_EXAMPLE,
  SIGN_UP_WITH_CREDENTIALS_API_RESPONSE_EXAMPLE,
  SIGN_UP_WITH_CREDENTIALS_RESPONSE_NEGATIVE_EXAMPLE)

# pylint: disable=unused-argument

app = FastAPI()
app.include_router(router, prefix="/authentication/api/v1")
add_exception_handlers(app)

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/sign-up"


@mock.patch("routes.sign_up.requests.post")
@mock.patch("routes.sign_up.create_session")
def test_sign_up_with_credentials(mock_create_session, mock_request,
                                  clean_firestore, create_user):
  url = f"{api_url}/credentials"

  credentials = SIGN_UP_WITH_CREDENTIALS_API_INPUT_EXAMPLE
  mock_create_session.return_value = {"session_id": "asd98798as7dhjgkjsdfh"}
  mock_request.return_value.status_code = 200
  mock_request.return_value.json.return_value = (
    SIGN_UP_WITH_CREDENTIALS_API_RESPONSE_EXAMPLE)

  resp = client_with_emulator.post(url, json=credentials)
  assert resp.status_code == (
    mock_request.return_value.status_code), "Status should be 200"
  assert resp.json().get("data") == (mock_request.return_value.json.return_value
                                     ), "Incorrect response received"


@mock.patch("routes.sign_up.requests.post")
def test_sign_up_with_credentials_negative(mock_request, clean_firestore,
                                           create_user):
  url = f"{api_url}/credentials"

  credentials = SIGN_UP_WITH_CREDENTIALS_API_INPUT_EXAMPLE

  mock_request.return_value.status_code = 400
  mock_request.return_value.json.return_value = (
    SIGN_UP_WITH_CREDENTIALS_RESPONSE_NEGATIVE_EXAMPLE)

  resp = client_with_emulator.post(url, json=credentials)

  assert resp.status_code == 422, "Status should be 422"
  assert resp.json().get(
    "message") == mock_request.return_value.json.return_value.get(
    "error").get("message"), "Incorrect response received"


@mock.patch("routes.sign_up.requests.post")
def test_sign_up_with_credentials_negative_2(mock_request, clean_firestore,
                                             create_user):
  url = f"{api_url}/credentials"

  credentials = SIGN_UP_WITH_CREDENTIALS_API_INPUT_EXAMPLE

  mock_request.return_value.status_code = 400
  mock_request.return_value.json.return_value = (
    SIGN_UP_WITH_CREDENTIALS_RESPONSE_NEGATIVE_EXAMPLE)

  resp = client_with_emulator.post(url, json=credentials)
  assert resp.status_code == 422, "Status should be 422"
  assert resp.json().get(
    "message") == mock_request.return_value.json.return_value.get(
    "error").get("message"), "Incorrect response received"
