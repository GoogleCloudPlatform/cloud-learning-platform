"""
  Unit Tests for Password related endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable= unused-argument, redefined-outer-name, unused-import, line-too-long
from unittest import mock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from testing.test_config import API_URL
from routes.password import router
from common.utils.http_exceptions import add_exception_handlers
from schemas.schema_examples import (
    IDP_SEND_PASSWORD_RESET_EMAIL_RESPONSE_EXAMPLE, IDP_RESET_PASSWORD_EXAMPLE,
    IDP_CHANGE_PASSWORD_EXAMPLE,
    IDP_ERROR_SEND_PASSWORD_RESET_EMAIL_RESPONSE_EXAMPLE,
    IDP_ERROR_RESET_PASSWORD_EXAMPLE, IDP_ERROR_CHANGE_PASSWORD_EXAMPLE,
    SEND_PASSWORD_RESET_EMAIL_EXAMPLE, RESET_PASSWORD_EXAMPLE,
    CHANGE_PASSWORD_EXAMPLE)

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/authentication/api/v1")

client_with_emulator = TestClient(app)


@mock.patch("routes.password.requests.post")
def test_send_password_reset_email(mock_post_req, clean_firestore, create_user):
  input_json = SEND_PASSWORD_RESET_EMAIL_EXAMPLE

  mock_post_req.return_value.status_code = 200
  mock_post_req.return_value.json.return_value = IDP_SEND_PASSWORD_RESET_EMAIL_RESPONSE_EXAMPLE

  url = f"{API_URL}/send-password-reset-email"

  resp = client_with_emulator.post(url, json=input_json)

  assert resp.status_code == 200, "Status should be 200"


@mock.patch("routes.password.requests.post")
def test_send_password_reset_email_negative(mock_post_req, clean_firestore,
                                            create_user):
  input_json = SEND_PASSWORD_RESET_EMAIL_EXAMPLE

  mock_post_req.return_value.status_code = 400
  mock_post_req.return_value.json.return_value = IDP_ERROR_SEND_PASSWORD_RESET_EMAIL_RESPONSE_EXAMPLE

  url = f"{API_URL}/send-password-reset-email"

  resp = client_with_emulator.post(url, json=input_json)
  assert resp.status_code == 404, "Incorrect status code received"
  assert resp.json().get(
      "message"
  ) == f"User with email {input_json['email']} not found", "Expected response is not same"


@mock.patch("routes.password.requests.post")
def test_reset_password(mock_post_req):
  input_json = RESET_PASSWORD_EXAMPLE

  mock_post_req.return_value.status_code = 200
  mock_post_req.return_value.json.return_value = IDP_RESET_PASSWORD_EXAMPLE

  url = f"{API_URL}/reset-password"

  resp = client_with_emulator.post(url, json=input_json)

  assert resp.status_code == 200, "Status should be 200"


@mock.patch("routes.password.requests.post")
def test_reset_password_negative(mock_post_req):
  input_json = RESET_PASSWORD_EXAMPLE

  mock_post_req.return_value.status_code = 400
  mock_post_req.return_value.json.return_value = IDP_ERROR_RESET_PASSWORD_EXAMPLE

  url = f"{API_URL}/reset-password"

  resp = client_with_emulator.post(url, json=input_json)

  assert resp.status_code == 422, "Incorrect status code received"


@mock.patch("routes.password.requests.post")
@mock.patch("routes.password.validate_token")
def test_change_password(mock_validate_token, mock_post_req, clean_firestore,
                         create_user):
  input_json = CHANGE_PASSWORD_EXAMPLE

  mock_post_req.return_value.status_code = 200
  mock_post_req.return_value.json.return_value = IDP_CHANGE_PASSWORD_EXAMPLE
  mock_validate_token.return_value = True

  headers = {"Authorization": "Bearer v8273bqo"}
  url = f"{API_URL}/change-password"

  resp = client_with_emulator.post(url, json=input_json, headers=headers)
  assert resp.status_code == 200, "Status 200"


@mock.patch("routes.password.requests.post")
def test_change_password_negative(mock_post_req, clean_firestore, create_user):
  input_json = CHANGE_PASSWORD_EXAMPLE

  mock_post_req.return_value.status_code = 401
  mock_post_req.return_value.json.return_value = IDP_ERROR_CHANGE_PASSWORD_EXAMPLE

  url = f"{API_URL}/change-password"

  resp = client_with_emulator.post(url, json=input_json)

  assert resp.status_code == 422, "Incorrect status code received"
  assert resp.json().get("message") == "Invalid token provided"
