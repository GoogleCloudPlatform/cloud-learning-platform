"""Utility method to validate user based on Id Token"""
import re

from fastapi import Request
from common.utils.logging_handler import Logger
from common.utils.errors import InvalidTokenError
from common.utils.auth_service import user_verification


# pylint: disable = consider-using-f-string
def get_user_identity(req: Request) -> dict:
  """
  Get user identity from firebase token
  :param req:
  :return: json/dict
  """
  try:
    token = req.headers["Authorization"]
    res = user_verification(token=token)
    data = res.json()

    if res.status_code == 200:
      if data["success"] is True:
        user_id = data["data"]["user_id"]
        user_email = data["data"]["email"]
        return {"success": True, "user_id": user_id,
                "user_email": user_email, "token":token}
      if data["success"] is False:
        raise InvalidTokenError(data["message"])
    else:
      raise InvalidTokenError(data["message"])
  except InvalidTokenError as e:
    Logger.error("Token error: %s" % e)
    return {
        "success": False,
        "message": re.split(",", e.error)[0],
        "data": None
    }
  except Exception as e: # pylint: disable = broad-except
    Logger.error("Token error: %s" % e)
    return {"success": False, "message": "Internal Server Error", "data": None}
