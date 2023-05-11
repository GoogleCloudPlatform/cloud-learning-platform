""" Sign In endpoints """
import requests
from copy import deepcopy
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from requests.exceptions import ConnectTimeout
from config import FIREBASE_API_KEY, IDP_URL, ERROR_RESPONSES
from common.models import TempUser
from common.utils.logging_handler import Logger
from common.utils.errors import (InvalidTokenError, InvalidCredentialsError,
                                 UnauthorizedUserError)
from common.utils.http_exceptions import (InternalServerError, Unauthenticated,
                                          BadRequest, Unauthorized,
                                          ConnectionTimeout, ServiceUnavailable)
from schemas.sign_in_schema import (SignInWithCredentialsModel,
                                    SignInWithCredentialsResponseModel,
                                    SignInWithTokenResponseModel)
from schemas.error_schema import ConnectionErrorResponseModel
from services.validate_google_token import validate_google_oauth_token
from services.create_session_service import create_session

ERROR_RESPONSE_DICT = deepcopy(ERROR_RESPONSES)
ERROR_RESPONSE_DICT[503] = {"model": ConnectionErrorResponseModel}

auth_scheme = HTTPBearer(auto_error=False)

# pylint: disable = broad-exception-raised
router = APIRouter(
    tags=["Sign In"], prefix="/sign-in", responses=ERROR_RESPONSE_DICT)


@router.post("/token", response_model=SignInWithTokenResponseModel)
def sign_in_with_token(token: auth_scheme = Depends()):
  """This endpoint will take the Google oauth token as an Authorization header
  and returns the firebase id_token and refresh token.
  ### Args:
  Authorization header: `Bearer token`
  ### Raises:
  UnauthorizedUserError:
    If user does not exist in firestore <br/>
  InvalidTokenError:
    If the token is invalid or has expired <br/>
  ConnectionTimeout:
    Connection Timeout Error. If API request gets timed-out. <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong <br/>
  ServiceUnavailable:
    Connection Error. If other service being called internally is not available
  ### Returns:
  Token: `SignInWithTokenResponseModel`
    Returns the id token as well as refresh token
  """
  try:
    token_dict = dict(token)
    Logger.info(f"request for sign-in: {token_dict}")
    oauth_token = token_dict["credentials"]
    decoded_token = validate_google_oauth_token(oauth_token)
    Logger.info(f"decoded_token: {decoded_token}")
    email = decoded_token.get("email")

    user_data = TempUser.find_by_email(email)
    if not user_data:
      raise UnauthorizedUserError("Unauthorized")

    if user_data.get_fields(reformat_datetime=True).get("status") == "inactive":
      raise UnauthorizedUserError("Unauthorized")

    url = f"{IDP_URL}:signInWithIdp?key={FIREBASE_API_KEY}"
    post_body = f"id_token={oauth_token}&providerId=google.com"
    data = {
      "requestUri": "http://localhost",
      "returnSecureToken": True,
      "postBody": post_body
    }
    resp = requests.post(url, data,timeout=60)
    Logger.info(f"Response from IDP for sign-in: {resp.json()}")

    if resp.status_code == 200:
      res = resp.json()
      res["user_id"] = user_data.user_id
      session_res = create_session(user_data.user_id)
      res["session_id"] = session_res.get("session_id")
      return {"success": True, "message": "Successfully signed in", "data": res}
    if resp.status_code == 403:
      raise Exception("Firebase API key missing")
    if resp.status_code == 400:
      res = resp.json()
      raise InvalidTokenError(res.get("error").get("message"))
  except UnauthorizedUserError as e:
    raise Unauthorized(str(e)) from e
  except InvalidTokenError as e:
    raise Unauthenticated(str(e)) from e
  except ConnectTimeout as e:
    raise ConnectionTimeout(str(e)) from e
  except ConnectionError as e:
    raise ServiceUnavailable(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post("/credentials", response_model=SignInWithCredentialsResponseModel)
def sign_in_with_credentials(credentials: SignInWithCredentialsModel):
  """This endpoint will take the user email and password as an input
  and returns an id token and refresh token from the IDP
  ### Args:
  credentials: `SignInWithCredentialsModel`
    Credentials will consist of email and password
  ### Raises:
  UnauthorizedUserError:
    If the user does not exist in firestore <br/>
  ConnectionTimeout:
    Connection Timeout Error. If API request gets timed-out. <br/>
  InvalidTokenError:
    If the token is invalid or has expired <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong <br/>
  ServiceUnavailable:
    Connection Error. If other service being called internally is not available
  ### Returns:
  Token: `SignInWithCredentialsResponseModel`
    Returns the id token as well as refresh token
  """
  try:
    user_data = TempUser.find_by_email(credentials.email)
    if not user_data:
      raise UnauthorizedUserError("Unauthorized")
    if user_data.get_fields(reformat_datetime=True).get("status") == "inactive":
      raise UnauthorizedUserError("Unauthorized")
    url = f"{IDP_URL}:signInWithPassword?key={FIREBASE_API_KEY}"
    data = {
      "email": credentials.email,
      "password": credentials.password,
      "returnSecureToken": True
    }
    resp = requests.post(url, data,timeout=60)
    if resp.status_code == 200:
      res = resp.json()
      res["user_id"] = user_data.user_id
      session_res = create_session(res["user_id"])
      res["session_id"] = session_res.get("session_id")
      return {"success": True, "message": "Successfully signed in", "data": res}
    if resp.status_code == 400:
      res = resp.json()
      raise InvalidCredentialsError(res.get("error").get("message"))
    if resp.status_code == 403:
      raise Exception("Firebase API key missing")
  except UnauthorizedUserError as e:
    raise Unauthorized(str(e)) from e
  except InvalidCredentialsError as e:
    raise BadRequest(str(e)) from e
  except ConnectTimeout as e:
    raise ConnectionTimeout(str(e)) from e
  except ConnectionError as e:
    raise ServiceUnavailable(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
