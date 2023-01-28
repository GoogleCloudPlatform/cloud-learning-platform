"""Firebase token validation"""
import requests
from fastapi import Depends
from fastapi.security import HTTPBearer
from common.utils.errors import InvalidTokenError
from common.utils.http_exceptions import Unauthenticated, InternalServerError

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
