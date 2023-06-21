"""Generates Fake data"""

from fastapi import APIRouter
import traceback
from common.utils.logging_handler import Logger
from common.utils.http_exceptions import InternalServerError
from schemas.fake_data import FakeIRTDataRequest, FakeDataResponse, CourseFakeIRTDataRequest
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel)
from services.create_fake_data import generate_irt_data
from services.fake_data_course_level import generate_irt_data_course_level

router = APIRouter(
    prefix="/fake_data",
    tags=["Fake Data"],
    responses={
        500: {
            "model": InternalServerErrorResponseModel
        },
        422: {
            "model": ValidationErrorResponseModel
        }
    })


@router.post("/", response_model=FakeDataResponse)
def create_fake_data(request_body: FakeIRTDataRequest):
  """Generated fake data at a learning unit level"""
  try:
    lu_id = generate_irt_data(request_body.num_users, request_body.num_items,
                              request_body.item_type)
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
  return {
      "success": True,
      "message": "Successfully generated fake data",
      "data": {
          "learning_unit_id": lu_id
      }
  }


@router.post("/course")
def create_fake_data_course_level(request_body: CourseFakeIRTDataRequest):
  """Generates fake data at a course level"""
  try:
    generate_irt_data_course_level(request_body.num_users,
                                   request_body.course_id)
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
  return {
      "success": True,
      "message": "Successfully generated fake data",
      "data": {}
  }
