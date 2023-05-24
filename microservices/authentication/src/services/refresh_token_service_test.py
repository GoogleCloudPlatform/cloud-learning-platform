"""
    utility methods to execute unit tests for module refresh_token_service.py
"""
import mock
import pytest
from services.refresh_token_service import generate_token, get_id_token
from utils.exception_handler import InvalidRefreshTokenError

token_credentials = {
    "access_token": "eyJhbGciOiJSU........C7h4w",
    "expires_in": 3600,
    "token_type": "Bearer",
    "refresh_token": "AEu4IL2njCpop7p.......CU6sm8",
    "id_token": "eyJhbGciOiJSU.......G2rC7h4w",
    "user_id": "fiurc756IqcdRSs19upxiVLt1Gr2",
    "project_id": "test-project"
}


def mocked_requests_post(*args, **kwargs):
  """Mock requests"""
  class MockResponse:

    def __init__(self, json_data, status_code):
      self.json_data = json_data
      self.status_code = status_code

    def json(self):
      return self.json_data

  if args[
      0] == "https://securetoken.googleapis.com/v1/token" and "key" in kwargs[
          "params"]:
    return MockResponse(token_credentials, 200)

  return MockResponse(None, 404)


@mock.patch("services.refresh_token_service.requests.post")
def test_get_id_token(mock_post):
  # arrange
  refresh_token = "ABC"
  payload = f"grant_type=refresh_token&refresh_token={refresh_token}"

  mock_post.side_effect = mocked_requests_post
  # action
  resp = get_id_token(payload)

  # assert
  assert resp is not None
  assert "id_token" in resp
  assert resp == token_credentials


@mock.patch("services.refresh_token_service.get_id_token")
def test_generate_token(mock_get_id_token):
  # arrange
  req_body = {"refresh_token": "ABC"}
  mock_get_id_token.return_value = token_credentials

  # action
  resp = generate_token(req_body)

  # assert
  assert resp == token_credentials


@mock.patch("services.refresh_token_service.get_id_token")
def test_generate_token_invalid_refresh_token(mock_get_id_token):
  # arrange
  req_body = {"refresh_token": "ABC"}
  mock_get_id_token.return_value = {
      "error": {
          "message": "INVALID_REFRESH_TOKEN"
      }
  }

  # action
  with pytest.raises(InvalidRefreshTokenError) as err:
    generate_token(req_body)

  # assert
  assert str(err.value) == "INVALID_REFRESH_TOKEN"
