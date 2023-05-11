"""Utility method for Token generation."""
import requests
from config import FIREBASE_API_KEY
from utils.exception_handler import InvalidRefreshTokenError


def generate_token(req_body):
  """
    Calls get_id_token method from refresh_token_service
    and Returns Response or Error.
    Args:
        req_body: Dict
    Returns
        token_credentials: Dict
  """

  payload = (
      f"grant_type=refresh_token&"
      f"refresh_token={req_body['refresh_token']}"
  )
  response = get_id_token(payload)
  if "error" in response:
    raise InvalidRefreshTokenError(response["error"]["message"])
  return response


def get_id_token(payload):
  """
    Calls Google API using refresh_token as payload to generate
    new Id Token
    Args:
        payload: Dict(Object)
        API_KEY: String
    Returns:
        Token Credentials: Dict(Object)
  """
  resp = requests.post(
      "https://securetoken.googleapis.com/v1/token",
      payload,
      headers={"Content-Type": "application/x-www-form-urlencoded"},
      params={"key": FIREBASE_API_KEY},
      timeout=60)
  return resp.json()
