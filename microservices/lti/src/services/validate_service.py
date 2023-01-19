"""Validate Service"""
from functools import wraps
from fastapi.security import HTTPBearer
from common.utils.errors import InvalidTokenError
from services.keys_manager import get_platform_public_keyset
from services.lti_token import decode_token, get_unverified_token_claims

auth_scheme = HTTPBearer(auto_error=False)


def validate_access(allowed_scopes):
  """Validate token and provide access based on the scope of the API"""

  def decorator(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
      token = kwargs.get("token")
      if token is None:
        raise InvalidTokenError("Token is missing")
      token_dict = dict(token)

      access_token = token_dict.get("credentials")
      if access_token:
        unverified_claims = get_unverified_token_claims(token=access_token)
        decoded_token = decode_token(
            access_token,
            get_platform_public_keyset().get("public_keyset"),
            unverified_claims.get("aud"))

        user_scopes = decoded_token["scope"].split(" ")
        for scope in allowed_scopes:
          if scope in user_scopes:
            return func(*args, **kwargs)

      raise InvalidTokenError("Unauthorized due to invalid scope")

    return wrapper

  return decorator
