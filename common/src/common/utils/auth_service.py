"""Firebase token validation"""
import json
import requests
from fastapi import Depends
from fastapi.security import HTTPBearer
from common.utils.errors import InvalidTokenError
from common.utils.http_exceptions import Unauthenticated, InternalServerError
from common.utils.config import SERVICES

auth_scheme = HTTPBearer(auto_error=False)

# pylint: disable = consider-using-f-string
def validate_token(token: auth_scheme = Depends()):
  """_summary_

  Args:
      token (auth_scheme, optional): _description_. Defaults to Depends().

  Raises:
      InvalidTokenError: _description_
      Unauthenticated: _description_
      InternalServerError: _description_

  Returns:
      Boolean: token is valid or not
  """
  try:
    if token is None:
      raise InvalidTokenError("Unauthorized")
    token_dict = dict(token)
    if token_dict["credentials"]:
      api_endpoint = "http://authentication/authentication/api/v1/validate"
      res = requests.get(
          url=api_endpoint,
          headers={
              "Content-Type":
              "application/json",
              "Authorization":
              f"{token_dict['scheme']} {token_dict['credentials']}"
          },
          timeout=60)
      data = res.json()
      if res.status_code == 200 and data["success"] is True:
        return data.get("data")
      else:
        raise InvalidTokenError(data["message"])
    else:
      raise InvalidTokenError("Unauthorized")
  except InvalidTokenError as e:
    raise Unauthenticated(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


def validate_user_type_and_token(accepted_user_types: list,
                                 token: auth_scheme = Depends()):
  """_summary_

  Args:
      token (auth_scheme, optional): _description_. Defaults to Depends().

  Raises:
      InvalidTokenError: _description_
      Unauthenticated: _description_
      InternalServerError: _description_

  Returns:
      Boolean: token is valid or not
  """
  try:
    if token is None:
      raise InvalidTokenError("Unauthorized")
    token_dict = dict(token)
    if token_dict["credentials"]:
      api_endpoint = "http://authentication/authentication/api/v1/validate"
      res = requests.get(
          url=api_endpoint,
          headers={
              "Content-Type":
              "application/json",
              "Authorization":
              f"{token_dict['scheme']} {token_dict['credentials']}"
          },
          timeout=60)
      data = res.json()
      if res.status_code == 200 and data["success"] is True and data["data"][
          "user_type"] in accepted_user_types:
        return data.get("data")
      else:
        raise InvalidTokenError(data["message"])
    else:
      raise InvalidTokenError("Unauthorized")
  except InvalidTokenError as e:
    raise Unauthenticated(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


def validate_user(token: auth_scheme = Depends()):
  return validate_user_type_and_token(["other", "faculty", "admin", "robot"],
                                      token)


def user_verification(token: str) -> json:
  """
  Verify the user with firebase IDToken
  :param token:
  :return: json
  """
  api_endpoint = "http://{}:{}/authentication/api/v1/validate".format(
    SERVICES["authentication"]["host"], SERVICES["authentication"]["port"])
  response = requests.get(
    url=api_endpoint,
    headers={
      "Content-Type": "application/json",
      "Authorization": token
    },
  )

  return response
