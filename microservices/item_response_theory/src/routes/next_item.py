"""Returns User Ability tree"""

import traceback
from typing import Optional
from fastapi import APIRouter
from services.next_item import next_item
from schemas.next_item_schema import ActivityType
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel)
from common.utils.logging_handler import Logger
from common.utils.http_exceptions import InternalServerError
# pylint: disable=broad-except

router = APIRouter(
    prefix="/item",
    tags=["Next Assessment Item"],
    responses={
        500: {
            "model": InternalServerErrorResponseModel
        },
        422: {
            "model": ValidationErrorResponseModel
        }
    })


@router.get("/")
def get_next_item(user_id: str,
                  learning_unit_id: str,
                  activity_type: ActivityType,
                  session_id: str,
                  prev_context_count: Optional[int] = -1):
  """Return next item to give to the user based on irt"""
  try:
    data = next_item(learning_unit_id, user_id, activity_type, session_id,
                     prev_context_count)
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
  return data
