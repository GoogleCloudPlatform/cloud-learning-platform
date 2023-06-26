"""Utility methods for token validation."""

from services.firebase_authentication import verify_token
from common.utils.logging_handler import Logger
from common.utils.cache_service import set_key, get_key
from common.utils.errors import UnauthorizedUserError
from common.models import TempUser


def validate_token(bearer_token):
  """
    Validates Token passed in headers, Returns user
    auth details along with user_type = new or old
    In case of Invalid token Throws error
    Args:
        Bearer Token: String
    Returns:
        Decoded Token and User type: Dict
  """
  token = bearer_token
  cached_token = get_key(f"cache::{token}")
  if cached_token is None:
    decoded_token = verify_token(token)
    cache_token = set_key(f"cache::{token}", decoded_token, 1800)
    Logger.info(f"Id Token caching status: {cache_token}")
  else:
    decoded_token = cached_token

  final_data = {**decoded_token}
  user = TempUser.find_by_email(decoded_token["email"])
  if user is not None:
    user_fields = user.get_fields(reformat_datetime=True)
    if user_fields.get("status") == "inactive":
      raise UnauthorizedUserError("Unauthorized")
    final_data["access_api_docs"] = False if user_fields.get(
        "access_api_docs") is None else user_fields.get("access_api_docs")
    final_data["user_type"] = user_fields.get("user_type")
  else:
    raise UnauthorizedUserError("Unauthorized")
  return final_data
