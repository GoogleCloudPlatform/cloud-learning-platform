"""
Pub Sub Auth
"""
import requests
from fastapi import Depends
from fastapi.security import HTTPBearer
from common.utils.errors import InvalidTokenError
from common.utils.http_exceptions import Unauthenticated, InternalServerError
from config import PROJECT_ID

auth_scheme = HTTPBearer(auto_error=False)
email=f"lms-notifications@{PROJECT_ID}.iam.gserviceaccount.com"
def validate_pub_sub_token(token: auth_scheme = Depends()):
  """_summary_

  Args:
      token (auth_scheme, optional): _description_. Defaults to Depends().

  Raises:
      InvalidTokenError: _description_
      InvalidTokenError: _description_
      InvalidTokenError: _description_
      Unauthenticated: _description_
      InternalServerError: _description_

  Returns:
      _type_: _description_
  """
  try:
    if token is None:
      raise InvalidTokenError("Unauthorized")
    token_dict = dict(token)
    if token_dict["credentials"]:
      api_endpoint = ("https://oauth2.googleapis.com/tokeninfo?id_token="
                      + token_dict["credentials"])
      res = requests.get(
          url=api_endpoint,
          timeout=60
      )
      data = res.json()
      if res.status_code == 200:
        if data["email"]==email:
          return True
        else:
          raise InvalidTokenError("Unauthorized")
      else:
        raise InvalidTokenError(data["error"])
    else:
      raise InvalidTokenError("Unauthorized")
  except InvalidTokenError as e:
    raise Unauthenticated(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
