"""Firebase token validation"""
import requests
from fastapi import Depends
from fastapi.security import HTTPBearer
from common.utils.errors import InvalidTokenError
from common.utils.http_exceptions import Unauthenticated, InternalServerError
from common.utils.token_handler import UserCredentials

auth_scheme = HTTPBearer(auto_error=False)


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


def get_user_data(user_details: dict, auth_client: UserCredentials):
  """
  Get User data from user-management service

  Args:
      token (auth_scheme, optional): _description_. Defaults to Depends().

  Raises:
      InvalidTokenError: _description_
      Unauthenticated: _description_
      InternalServerError: _description_

  Returns:
      Boolean: token is valid or not
  """
  # verify user if it exists
  user_email = user_details.get("email")
  headers = {"Authorization": f"Bearer {auth_client.get_id_token()}"}
  fetch_user_request = requests.get(
      "http://user-management/user-management/api/v1/user/search/email",
      params={"email": user_email},
      headers=headers,
      timeout=60)

  if fetch_user_request.status_code == 200:
    user_data = fetch_user_request.json().get("data")[0]
  elif fetch_user_request.status_code == 404:
    raise UnauthorizedUserError(
        "Access Denied with code 1001, Please contact administrator")
  else:
    raise Exception(
        "Request Denied with code 1002, Please contact administrator")

  return user_data
