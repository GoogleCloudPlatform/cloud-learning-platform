'''Context Endpoints'''
import traceback
from fastapi import APIRouter
from common.utils.logging_handler import Logger
from common.utils.errors import ResourceNotFoundException, ValidationError
from common.utils.http_exceptions import (ResourceNotFound, InternalServerError,
                                          BadRequest)
from utils.request_handler import get_method
from schemas.context_schema import ContextResponseModel
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
def get_context_details(context_id: str, context_type: str):
  """Get the details of the context based on the context type and id
    
    Args:
        context_id (str): unique id of the Context
        context_type (str): Type of the Context

    Raises:
        ResourceNotFoundException: If the context does not exist.
        HTTPException: 500 Internal Server Error if something fails.

    Returns:
        ContextResponseModel: Context object for the given id
        NotFoundErrorResponseModel: if the context is not found,
        InternalServerErrorResponseModel: if the get Context raises an exception
    """
  try:
    if context_type == "section":
      get_section_url = f"http://lms/lms/api/v1/sections/{context_id}"
      context_res = get_method(url=get_section_url, use_bot_account=True)

      if context_res.status_code == 200:
        context_data = context_res.json().get("data")
      else:
        Logger.error(
            f"Error 1100 response: Status code: {context_res.status_code}; Response: {context_res.text}"
        )
        raise Exception("Request failed with error code 1100")

    elif context_type == "course_template":
      get_template_url = f"http://lms/lms/api/v1/course_templates/{context_id}"

      context_res = get_method(url=get_template_url, use_bot_account=True)

      if context_res.status_code == 200:
        context_data = context_res.json()
      else:
        Logger.error(
            f"Error 1110 response: Status code: {context_res.status_code}; Response: {context_res.text}"
        )
        raise Exception("Request failed with error code 1110")
    else:
      Logger.error(
          f"Error 1120: Context type not provided for the given request with course id -{context_id}"
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
