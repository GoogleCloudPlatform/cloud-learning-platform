"""Class and methods to handle activity routes"""
import traceback
from fastapi import APIRouter
from services.activity_service import get_activity_list
from common.utils.logging_handler import Logger
from common.utils.http_exceptions import InternalServerError
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel,
                                  UnauthorizedUserErrorResponseModel)

router = APIRouter(
    prefix="/activities",
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
def get_activities():
  try:
    response=get_activity_list()
    return {
        "success": True,
        "message": "Successfully fetched all activities",
        "data": response
    }
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e

