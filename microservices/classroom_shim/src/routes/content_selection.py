"""Content Selection APIs"""
import traceback
from fastapi import APIRouter
from common.models import LTIContentItem
from common.utils.logging_handler import Logger
from common.utils.errors import ResourceNotFoundException, ValidationError
from common.utils.http_exceptions import (ResourceNotFound, InternalServerError,
                                          BadRequest)
from utils.request_handler import get_method
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


@router.get("/tools-and-content-items")
def get_tool_and_context_list(tool_id: str, context_id: str):
  """API to return tools list and content items for give tool and context id"""
  try:
    # fetch tools list
    req = get_method(
        "http://lti/lti/api/v1/tools",
        query_params={
            "skip": 0,
            "limit": 100
        },
        use_bot_account=True)
    # fetch content context
    content_items = LTIContentItem.filter_with_context_id_and_tool_id(
        tool_id, context_id)
    return {
        "success": True,
        "message": "Data fetched successfully",
        "data": {
            "content_items": content_items,
            "tools_list": req.json().get("data")
        }
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
