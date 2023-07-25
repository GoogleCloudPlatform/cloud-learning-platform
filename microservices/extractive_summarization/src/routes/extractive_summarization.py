"""Extractive Summarization endpoint"""
import traceback
from fastapi import APIRouter
from utils.errors import ValidationError
from utils.http_exceptions import InternalServerError, BadRequest
from utils.logging_handler import Logger
from services.inference import summarize_text
from schemas.extractive_summarization_schema import RequestModel, ResponseModel
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel)


router = APIRouter(
  tags=["Extractive Summarization"],
  responses={
    500: {
      "model": InternalServerErrorResponseModel
    },
    422: {
      "model": ValidationErrorResponseModel
    }
  }
)

#pylint: disable=broad-except
@router.post("/summarize", response_model=ResponseModel)
def summarize(req_body: RequestModel):
  """
  Generates Extractive Summarization model prediction

  Args:
    req_body (RequestModel): Required request body for Extractive Summarization

  Raises:
    InternalServerError: 500 Internal Server Error if something fails
    BadRequest: 422 Validation Error if request body is not correct

  Returns:
    [JSON]: Prediction by Extractive Summarization model.
    error message if the feedback generation raises an exception
  """
  try:
    response = summarize_text(req_body.__dict__)
    return {
      "success": True,
      "message": "All good",
      "data": response
    }
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
