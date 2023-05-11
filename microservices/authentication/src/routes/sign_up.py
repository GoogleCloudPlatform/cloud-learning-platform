""" Sign Up endpoints """
import requests
import traceback
from copy import deepcopy
from fastapi import APIRouter
from requests.exceptions import ConnectTimeout
from config import ERROR_RESPONSES, FIREBASE_API_KEY, IDP_URL
from common.models import TempUser
from common.utils.errors import (InvalidRequestPayloadError,
                                 UnauthorizedUserError)
from common.utils.http_exceptions import (BadRequest, InternalServerError,
                                          Unauthorized, ConnectionTimeout,
                                          ServiceUnavailable)
from schemas.sign_up_schema import (SignUpWithCredentialsModel,
                                    SignUpWithCredentialsResponseModel)
from schemas.error_schema import ConnectionErrorResponseModel
from services.create_session_service import create_session

ERROR_RESPONSE_DICT = deepcopy(ERROR_RESPONSES)
del ERROR_RESPONSE_DICT[401]
ERROR_RESPONSE_DICT[503] = {"model": ConnectionErrorResponseModel}

# pylint: disable = broad-exception-raised
router = APIRouter(
    tags=["Sign Up"],
    prefix="/sign-up",
    responses=ERROR_RESPONSE_DICT)


@router.post(
    "/credentials",
    response_model=SignUpWithCredentialsResponseModel)
def sign_up_with_credentials(credentials: SignUpWithCredentialsModel):
  """ This endpoint creates a new user with the given email and password
  by making an HTTP POST request to the IDP auth signUp endpoint and
  returns id token and refresh token.
  ### Args:
  credentials: `SignUpWithCredentialsModel`
    Credentials will consist of email and password
  ### Raises:
  UnauthorizedUserError:
    If the user does not exist in firestore <br/>
  ConnectionTimeout:
    Connection Timeout Error. If API request gets timed-out. <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong <br/>
  ServiceUnavailable:
    Connection Error. If other service being called internally is not available
  ### Returns:
  Token: `SignUpWithCredentialsResponseModel`
    Returns the id token as well as refresh token
  """
  try:
    user_data = TempUser.find_by_email(credentials.email)
    if not user_data:
      raise UnauthorizedUserError("Unauthorized")
    if user_data.get_fields(reformat_datetime=True).get("status") == "inactive":
      raise UnauthorizedUserError("Unauthorized")
    url = f"{IDP_URL}:signUp?key={FIREBASE_API_KEY}"
    data = {
        "email": credentials.email,
        "password": credentials.password,
        "returnSecureToken": True
    }
    resp = requests.post(url, data,timeout=60)
    resp_data =  resp.json()
    print("IDP SIGNUP RESPONSE", resp_data)
    if resp.status_code == 200:
      res = resp.json()
      res["user_id"] = user_data.user_id
      session_res = create_session(user_data.user_id)
      print("SESSION_RES: ", session_res)
      res["session_id"] = session_res.get("session_id")
      return {"success": True, "message": "Successfully signed up", "data": res}
    if resp.status_code == 400:
      res = resp.json()
      raise InvalidRequestPayloadError(res.get("error").get("message"))
    if resp.status_code == 403:
      raise Exception("Firebase API key missing")
  except UnauthorizedUserError as e:
    print(traceback.print_exc())
    raise Unauthorized(str(e)) from e
  except InvalidRequestPayloadError as e:
    print(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except ConnectTimeout as e:
    print(traceback.print_exc())
    raise ConnectionTimeout(str(e)) from e
  except ConnectionError as e:
    print(traceback.print_exc())
    raise ServiceUnavailable(str(e)) from e
  except Exception as e:
    print(traceback.print_exc())
    raise InternalServerError(str(e)) from e
