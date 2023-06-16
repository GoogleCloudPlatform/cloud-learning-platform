'''Context Endpoints'''
import traceback
from fastapi import APIRouter
from common.utils.logging_handler import Logger
from common.utils.errors import ResourceNotFoundException, ValidationError
from common.utils.http_exceptions import (ResourceNotFound, InternalServerError,
                                          BadRequest)
from schemas.context_schema import ContextResponseModel, ContextMembersResponseModel
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ValidationErrorResponseModel)
from services.ext_service_handler import (get_instructional_designers,
                                          get_teachers, get_students,
                                          get_section_details,
                                          get_course_template_details)
# pylint: disable=line-too-long

router = APIRouter(
    tags=["Context"],
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


@router.get("/contexts/{context_id}", response_model=ContextResponseModel)
def get_context_details(context_id: str):
  """Get the details of the context based on the context id

    Args:
        context_id (str): unique id of the Context

    Raises:
        ResourceNotFoundException: If the context does not exist.
        HTTPException: 500 Internal Server Error if something fails.

    Returns:
        ContextResponseModel: Context object for the given id
        NotFoundErrorResponseModel: if the context is not found,
        InternalServerErrorResponseModel: if the get Context raises an exception
    """
  try:
    context_data = get_section_details(context_id)

    if context_data is None:
      context_data = get_course_template_details(context_id)

    return {
        "success": True,
        "message": "Successfully fetched the context details",
        "data": context_data
    }
  except ValidationError as e:
    Logger.error(e)
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
    "/contexts/{context_id}/members",
    response_model=ContextMembersResponseModel)
def get_context_members(context_id: str, context_type: str):
  """Get the details of the members for a given context

    Args:
        context_id (str): unique id of the Context
        context_type (str): Type of the Context

    Raises:
        ResourceNotFoundException: If the context does not exist.
        HTTPException: 500 Internal Server Error if something fails.

    Returns:
        ContextMembersResponseModel: Context object for the given id
        NotFoundErrorResponseModel: if the context is not found,
        InternalServerErrorResponseModel: if the get Context raises an exception
    """
  try:

    members_data = []
    if context_type == "course_template":
      members_data = get_instructional_designers(context_id)

    else:
      teachers_data = get_teachers(context_id)
      members_data.extend(teachers_data)

      student_data = get_students(context_id)
      members_data.extend(student_data)

    return {
        "success": True,
        "message": "Successfully fetched the context details",
        "data": members_data
    }
  except ValidationError as e:
    Logger.error(e)
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
