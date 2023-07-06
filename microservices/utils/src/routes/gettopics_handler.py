"""Class & methods to handle topics routes"""
import traceback
from fastapi import APIRouter
from services.gethelp_service import gettopics
from config import GET_TOPICS_COLLECTION
from common.utils.logging_handler import Logger
from common.utils.http_exceptions import InternalServerError
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel,
                                  UnauthorizedUserErrorResponseModel)

router = APIRouter(
  prefix="/topics",
  responses={
    500: {
      "model": InternalServerErrorResponseModel
    },
    422: {
      "model": ValidationErrorResponseModel
    },
    401: {
      "model": UnauthorizedUserErrorResponseModel
    }
  })


@router.get("")
def get_topics(page: int = 1):
  """
  Endpoint to fetch topics
  Args:
    page: integer
  Returns:
    get_topics: dict
  Raises:
    InternalServerError: 500
  """
  try:
    response = gettopics(GET_TOPICS_COLLECTION, int(page))
    return {
      "success": True,
      "message": "Successfully fetched topics",
      "data": response
    }
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
