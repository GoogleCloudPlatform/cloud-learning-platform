""" User Shim APIs """
from fastapi import APIRouter
from common.utils.http_exceptions import InternalServerError, ResourceNotFound
from common.utils.errors import ResourceNotFoundException
from common.utils.logging_handler import Logger
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ValidationErrorResponseModel)
from services.ext_service_handler import (get_user_details, get_student_details,
                                          get_user_details_with_id)
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


@router.get("/context/{context_id}/user/{user_id}")
def check_student_context_mapping(context_id: str, user_id: str):
  """Check mapping of user and context

  ### Args:
      context_id(str)
      user_id(str)

  """
  try:
    user_details = get_user_details_with_id(user_id)
    student_email = ""
    if user_details:
      student_email = user_details.get("data").get("email")
    else:
      student_email = ""
    user_data = get_student_details(context_id, student_email)
    if user_data is None:
      raise ResourceNotFoundException(
          f"Student with id '{user_id}' not found in context '{context_id}'")
    elif user_data:
      message = f"Student with id '{user_id}'is present in context '{context_id}'"
      return {"success": True, "data": user_data, "message": message}
  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
