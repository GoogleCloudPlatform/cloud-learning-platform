""" Password related endpoints  """
import requests
from copy import deepcopy
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from firebase_admin.auth import InvalidIdTokenError, ExpiredIdTokenError

from config import ERROR_RESPONSES, FIREBASE_API_KEY, IDP_URL
from services.validate_token_service import validate_token
from common.utils.errors import (ResourceNotFoundException,
                                 InvalidRequestPayloadError, TokenNotFoundError,
                                 UnauthorizedUserError)
from common.utils.http_exceptions import (BadRequest, InternalServerError,
                                          ResourceNotFound, InvalidToken,
                                          Unauthorized)
from common.models import TempUser
from schemas.password_schema import (SendPasswordResetEmailModel,
                                     SendPasswordResetEmailResponseModel,
                                     ResetPasswordModel,
                                     ResetPasswordResponseModel,
                                     ChangePasswordModel,
                                     ChangePasswordResponseModel)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  UnauthorizedUserErrorResponseModel)

# pylint: disable = broad-exception-raised

ERROR_RESPONSE_DICT = deepcopy(ERROR_RESPONSES)
del ERROR_RESPONSE_DICT[401]

router = APIRouter(tags=["Password"], responses=ERROR_RESPONSE_DICT)

auth_scheme = HTTPBearer(auto_error=False)

@router.post(
  "/send-password-reset-email",
  response_model=SendPasswordResetEmailResponseModel,
  responses={
    404: {
      "model": NotFoundErrorResponseModel
    },
    401: {
      "model": UnauthorizedUserErrorResponseModel
    }
  })
def send_password_reset_email(
  input_send_password_reset_email: SendPasswordResetEmailModel):
  """This endpoint will send a password reset email for a given email address.
  ### Args:
  input_send_password_reset_email: `SendPasswordResetEmailModel`
    Input for sending the password reset email
  ### Raises:
  UnauthorizedUserError:
    If user does not exist in firestore <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong.
  ### Returns:
  Success Response: `SendPasswordResetEmailResponseModel`
  """
  try:
    input_password_reset_email_dict = {**input_send_password_reset_email.dict()}
    url = f"{IDP_URL}:sendOobCode?key={FIREBASE_API_KEY}"
    email = input_password_reset_email_dict.get("email")

    user_data = TempUser.find_by_email(email)
    if not user_data:
      raise UnauthorizedUserError("Unauthorized")
    if user_data.get_fields(reformat_datetime=True).get("status",
                                                        "") == "inactive":
      raise UnauthorizedUserError("Unauthorized")

    input_data = {"requestType": "PASSWORD_RESET", "email": email}
    resp = requests.post(url=url, json=input_data,timeout=60)

    if resp.status_code == 200:
      json_response = resp.json()
      return {
        "success": True,
        "message": "Successfully sent the password reset email",
        "data": json_response
      }

    if resp.status_code == 400:
      raise ResourceNotFoundException(f"User with email {email} not found")
    if resp.status_code == 403:
      raise Exception("Firebase API key missing")
  except UnauthorizedUserError as e:
    raise Unauthorized(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post("/reset-password", response_model=ResetPasswordResponseModel)
def reset_password(input_reset_password: ResetPasswordModel):
  """This endpoint will reset password using the given oobCode
  ### Args:
  input_reset_password: `ResetPasswordModel`
    Input for resetting the password of an user
  ### Raises:
  Exception 500:
    Internal Server Error. Raised if something went wrong.
  ### Returns:
  Success Response: `ResetPasswordResponseModel`
  """
  try:
    input_reset_password_dict = {**input_reset_password.dict()}
    url = f"{IDP_URL}:resetPassword?key={FIREBASE_API_KEY}"

    resp = requests.post(url=url, json=input_reset_password_dict,timeout=60)

    if resp.status_code == 200:
      json_response = resp.json()
      return {
        "success": True,
        "message": "Successfully updated the password",
        "data": json_response
      }

    if resp.status_code == 403:
      raise Exception("Firebase API key missing")

    if resp.status_code == 400:
      json_response = resp.json()
      raise InvalidRequestPayloadError(
        json_response.get("error").get("message"))

  except InvalidRequestPayloadError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
  "/change-password",
  responses={401: {
    "model": UnauthorizedUserErrorResponseModel
  }},
  response_model=ChangePasswordResponseModel)
def change_password(input_password_change: ChangePasswordModel,
                    token: auth_scheme = Depends()):
  """Change password for a given user based on the id token
  ### Args:
  input_password_change: `ChangePasswordModel`
    Input for changing the password
  ### Raises:
  UnauthorizedUserError:
    If user does not exist in firestore <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong.
  ### Returns:
  Success Response: \
  `ChangePasswordResponseModel`
  """
  try:
    if token:
      token_dict = dict(token)
      id_token = token_dict["credentials"]
      validate_token(id_token)
    else:
      raise TokenNotFoundError("Invalid token provided")

    input_password_change_dict = {**input_password_change.dict()}
    url = f"{IDP_URL}:update?key={FIREBASE_API_KEY}"

    input_data = {
      "idToken": id_token,
      "returnSecureToken": True,
      **input_password_change_dict
    }
    resp = requests.post(url=url, json=input_data,timeout=60)
    if resp.status_code == 200:
      json_response = resp.json()
      return {
        "success": True,
        "message": "Successfully changed the password",
        "data": json_response
      }

    if resp.status_code == 400:
      json_response = resp.json()
      raise InvalidRequestPayloadError(
        json_response.get("error").get("message"))

    if resp.status_code == 403:
      raise Exception("Firebase API key missing")

  except UnauthorizedUserError as e:
    raise Unauthorized(str(e)) from e
  except (TokenNotFoundError, InvalidRequestPayloadError) as e:
    raise BadRequest(str(e)) from e
  except (InvalidIdTokenError, ExpiredIdTokenError) as err:
    raise InvalidToken(str(err)) from err
  except Exception as e:
    raise InternalServerError(str(e)) from e
