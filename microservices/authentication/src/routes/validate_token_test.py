"""
  Unit tests for Authentication endpoint
"""
from fastapi import FastAPI
from fastapi.testclient import TestClient
from schemas.schema_examples import BASIC_VALIDATE_TOKEN_RESPONSE_EXAMPLE
from routes.validate_token import router
from common.utils.http_exceptions import add_exception_handlers

API_URL = "http://localhost/authentication/api/v1"

app = FastAPI()
app.include_router(router, prefix="/authentication/api/v1")
add_exception_handlers(app)

client = TestClient(app)


def test_valid_id(mocker):
  token = "Bearer cXVhbnRpcGhpX3NuaHU6ODc2MnRhZQ=="
  url = f"{API_URL}/validate"
  mocker.patch(
      "routes.validate_token.validate_token",
      return_value=BASIC_VALIDATE_TOKEN_RESPONSE_EXAMPLE)
  response = client.get(url, headers={"Authorization": token})
  assert response.json().get("data") == BASIC_VALIDATE_TOKEN_RESPONSE_EXAMPLE


def test_valid_id_no_header():
  url = f"{API_URL}/validate"
  response = client.get(url, headers={})
  assert response.json().get("message") == "Token not found"
