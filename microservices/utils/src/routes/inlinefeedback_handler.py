"""Class & methods to handle inline-feedback routes"""
import traceback
from fastapi import APIRouter, Depends
from services.feedback_service import save_inline_feedback
from config import USER_COLLECTION, INLINE_FEEDBACK_COLLECTION
from common.utils.logging_handler import Logger
from common.utils.http_exceptions import InternalServerError
from common.utils.authentication import get_user_identity
from schemas.feedback_schema import InlineFeedbackRequestModel
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel,
                                  UnauthorizedUserErrorResponseModel)

router = APIRouter(
  prefix="/inlineFeedback",
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


@router.post("")
def post_inlinefeedback(req_body: InlineFeedbackRequestModel,
                        authorized: dict = Depends(get_user_identity)):
  """
  Endpoint to post an inline feedback
  Args:
    req_body: InlineFeedbackRequestModel
    authorized: dict
  Returns:
    InlineFeedbackResponseModel: dictionary
  Raises:
    InternalServerError: 500
  """
  try:
    user_id = authorized["user_id"]
    response = save_inline_feedback(USER_COLLECTION,
                                    INLINE_FEEDBACK_COLLECTION,
                                    req_body.__dict__,
                                    user_id)
    return {
      "success": True,
      "message": "Successfully saved feedback of the user",
      "data": response
    }
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
