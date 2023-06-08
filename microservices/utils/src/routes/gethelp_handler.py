"""Class & methods to handle help routes"""
import traceback
from fastapi import APIRouter
from services.gethelp_service import get_help_faqs
from config import GET_HELP_COLLECTION
from common.utils.logging_handler import Logger
from common.utils.http_exceptions import InternalServerError
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel,
                                  UnauthorizedUserErrorResponseModel)


router = APIRouter(
    prefix="/help",
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
def get_help(page: int = 1, topic: str = None):
  try:
    response=get_help_faqs(GET_HELP_COLLECTION, topic, int(page))
    return {
        "success": True,
        "message": "Successfully fetched help me faqs",
        "data": response
    }
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
