"""Content Selection APIs"""
import traceback
from fastapi import APIRouter
from common.models import LTIContentItem
from common.utils.logging_handler import Logger
from common.utils.errors import ResourceNotFoundException, ValidationError
from common.utils.http_exceptions import (ResourceNotFound, InternalServerError,
                                          BadRequest)
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ValidationErrorResponseModel)
# pylint: disable=line-too-long

router = APIRouter(
    tags=["Content Selection APIs"],
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


@router.get("/{context_id}/tools-and-content-items")
def get_tool_and_context_list(context_id: str, tool_id: str):
  """API to return content items for give tool id and context id"""
  try:
    content_items = LTIContentItem.filter_with_context_id_and_tool_id(
        tool_id, context_id)
    return {
        "success": True,
        "message": "Data fetched successfully",
        "data": content_items
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
