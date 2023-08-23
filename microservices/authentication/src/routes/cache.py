"""Class and methods for handling validate route."""

import traceback
from fastapi import APIRouter
from common.utils.http_exceptions import InternalServerError
from common.utils.logging_handler import Logger
from utils.cache_service import ping_redis

router = APIRouter()


@router.get("/ping-redis")
def validate_id_token():
  """Validates the Token present in Headers
  ### Raises:
  UnauthorizedUserError:
    If user does not exist in firestore <br/>
  InvalidTokenError:
    If the token is invalid or has expired <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong
  ### Returns:
      ValidateTokenResponseModel: Details related to the token
  """

  try:
    ping_redis()
    return True
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
