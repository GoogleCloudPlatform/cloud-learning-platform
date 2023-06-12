""" User Shim APIs """
import requests
import config
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from common.utils.http_exceptions import InternalServerError
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ValidationErrorResponseModel)
# pylint: disable=line-too-long, broad-exception-raised

router = APIRouter(
    tags=["User Shim APIs"],
    responses={
        500: {
            "model": InternalServerErrorResponseModel
        },
        404: {
            "model": NotFoundErrorResponseModel
        },
        422: {
            "model": ValidationErrorResponseModel
        }
    })


@router.get("/user/search/email")
def search_user_by_email(email: str, request: Request):
  """Search for users based on the user first name

  ### Args:
      email(str): Email id of the user.

  ### Returns:
      UserSearchResponseModel: List of user objects
  """
  try:
    headers = {"Authorization": request.headers.get("Authorization")}
    response = requests.get(
        f"{config.USER_MANAGEMENT_BASE_URL}/user/search/email?email={email.lower()}",
        headers=headers,
        timeout=60)
    return JSONResponse(
        content=response.json(), status_code=response.status_code)
  except Exception as e:
    raise InternalServerError(str(e)) from e
