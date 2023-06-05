'''Context Endpoints'''
import traceback
from fastapi import APIRouter
from common.utils.logging_handler import Logger
from common.utils.errors import ResourceNotFoundException, ValidationError
from common.utils.http_exceptions import (ResourceNotFound, InternalServerError,
                                          BadRequest)
from utils.request_handler import get_method
from schemas.context_schema import ContextResponseModel, ContextMembersResponseModel
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ValidationErrorResponseModel)
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
    get_section_url = f"http://lms/lms/api/v1/sections/{context_id}"
    section_res = get_method(url=get_section_url, use_bot_account=True)

    if section_res.status_code == 200:
      context_data = section_res.json().get("data")
      context_data["description"] = context_data["section"]
      context_data["context_type"] = "section"

    elif section_res.status_code == 404:
      get_template_url = f"http://lms/lms/api/v1/course_templates/{context_id}"
      template_res = get_method(url=get_template_url, use_bot_account=True)

      if template_res.status_code == 200:
        context_data = template_res.json()
        context_data["context_type"] = "course_template"
      else:
        Logger.error(
            f"Error 1110: Internal error from LMS course template API with \
              Status code: {template_res.status_code}; Response: {template_res.text}"
        )
        raise Exception("Request failed with error code 1110")
    else:
      Logger.error(f"Error 1120:  Internal error from LMS section API with \
            Status code: {section_res.status_code}; Response: {section_res.text}"
                  )
      raise Exception("Request failed with error code 1120")

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
      get_ids_url = f"http://lms/lms/api/v1/course_templates/{context_id}/instructional_designers"
      get_ids_res = get_method(url=get_ids_url, use_bot_account=True)

      if get_ids_res.status_code == 200:
        members_data = get_ids_res.json().get("data")

      else:
        Logger.error(
            f"Error 1130 response: Internal error from LMS get IDs API with \
              Status code: {get_ids_res.status_code}; Response: {get_ids_res.text}"
        )
        raise Exception("Request failed with error code 1130")

    else:
      get_teachers_members_url = f"http://lms/lms/api/v1/sections/{context_id}/teachers"

      teachers_res = get_method(
          url=get_teachers_members_url, use_bot_account=True)

      if teachers_res.status_code == 200:
        teachers_data = teachers_res.json().get("data")
      else:
        Logger.error(
            f"Error 1140 response: Internal error from LMS get students API with \
               Status code: {teachers_res.status_code}; Response: {teachers_res.text}"
        )
        raise Exception("Request failed with error code 1140")

      members_data.extend(teachers_data)

      get_student_members_url = f"http://lms/lms/api/v1/sections/{context_id}/students"

      student_res = get_method(
          url=get_student_members_url, use_bot_account=True)

      if student_res.status_code == 200:
        student_data = student_res.json().get("data")
      else:
        Logger.error(
            f"Error 1150 response: Internal error from LMS get students API \
              Status code: {student_res.status_code}; Response: {student_res.text}"
        )
        raise Exception("Request failed with error code 1150")

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
