"""Class and methods to handle feedback routes"""
import traceback
from fastapi import APIRouter, Depends
from services.feedback_service import get_feedback_options, save_feedback
from config import FEEDBACK_COLLECTION, USER_COLLECTION, USER_SUBCOLLECTION
from common.utils.logging_handler import Logger
from common.utils.http_exceptions import InternalServerError
from common.utils.authentication import get_user_identity
from schemas.feedback_schema import FeedbackRequestModel
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel,
                                  UnauthorizedUserErrorResponseModel)

router = APIRouter(
    prefix="/feedback",
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
def get_feedback():
  try:
    response=get_feedback_options(FEEDBACK_COLLECTION)
    return {
        "success": True,
        "message": "Successfully fetched options for feedback",
        "data": response
    }
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e

@router.post("")
def post_feedback(req_body: FeedbackRequestModel,
                     authorized: dict = Depends(
                       get_user_identity)):
  try:
    user_id = authorized["user_id"]
    req_body.__dict__["token"] = authorized["token"]
    response = save_feedback(USER_COLLECTION, USER_SUBCOLLECTION,
                             req_body.__dict__, user_id)
    return {
        "success": True,
        "message": "Successfully saved feedback of the user",
        "data": response
    }
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
