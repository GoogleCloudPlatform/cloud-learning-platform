""" User Shim APIs """
from fastapi import APIRouter
from common.utils.http_exceptions import InternalServerError, ResourceNotFound
from common.utils.errors import ResourceNotFoundException
from common.utils.logging_handler import Logger
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ValidationErrorResponseModel)
from services.ext_service_handler import get_user_details
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
def search_user_by_email(email: str):
  """Search for users based on the user first name

  ### Args:
      email(str): Email id of the user.

  ### Returns:
      UserSearchResponseModel: List of user objects
  """
  try:
    user_data = get_user_details(email.lower())
    if user_data is None:
      raise ResourceNotFoundException(f"User with email '{email}' not found")
    elif user_data:
      return user_data
  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
