"""Returns User Ability tree"""

from fastapi import APIRouter
import traceback
from services.ability_tree import get_ability_tree
from common.models import User
from common.utils.http_exceptions import InternalServerError, ResourceNotFound
from common.utils.errors import ResourceNotFoundException
from common.utils.logging_handler import Logger
from schemas.ability_schema import LevelEnum
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel,
                                  NotFoundErrorResponseModel)

router = APIRouter(
    prefix="/ability",
    tags=["User Ability"],
    responses={
        500: {
            "model": InternalServerErrorResponseModel
        },
        422: {
            "model": ValidationErrorResponseModel
        }
    })


# pylint: disable=broad-except
@router.get("/", responses={404: {"model": NotFoundErrorResponseModel}})
def get_user_ability(user_id: str, level: LevelEnum, doc_id: str):
  """Returns ability of a user at a particular level"""
  try:
    user = User.find_by_id(user_id)
    data = get_ability_tree(level, doc_id, user)
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
  return data
