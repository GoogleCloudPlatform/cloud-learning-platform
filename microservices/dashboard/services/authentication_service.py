"""Utility method to interact with Authentication Microservice"""
import requests
from config import SERVICES
from common.utils.logging_handler import Logger

# pylint: disable= consider-using-f-string,missing-timeout
def get_auth_service_response(token):
  """
        Calls endpoint of authentication microservice to
        validate token issued to user.
        Args:
            token: String
        Returns:
            auth details: Dict
            or Error
    """
  Logger.info("Passing token to Authentication Microservice")
  api_endpoint = "http://{}:{}/authentication/api/v1/validate".format(
      SERVICES["authentication"]["host"], SERVICES["authentication"]["port"])
  response = requests.get(
      url=api_endpoint,
      headers={
          "Content-Type": "application/json",
          "Authorization": token
      },
  ).json()

  return response
