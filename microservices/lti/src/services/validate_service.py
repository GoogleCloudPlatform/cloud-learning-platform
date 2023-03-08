"""Validate Service"""
from functools import wraps
from fastapi import Depends
from fastapi.security import HTTPBearer
from common.models import Tool
from common.utils.errors import InvalidTokenError
from common.utils.http_exceptions import Unauthenticated
from services.keys_manager import get_platform_public_keyset
from services.lti_token import decode_token, get_unverified_token_claims
from jose.exceptions import JWSError, ExpiredSignatureError, JWTError

auth_scheme = HTTPBearer(auto_error=False)


def validate_and_decode_token(token):
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
    return decoded_token
  else:
    raise InvalidTokenError("Token is missing")


def validate_access(allowed_scopes):
  """Validate token and provide access based on the scope of the API"""

  def decorator(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
      try:
        token = kwargs.get("token")
        # if token is None:
        #   raise InvalidTokenError("Token is missing")
        # token_dict = dict(token)

        # access_token = token_dict.get("credentials")
        # if access_token:
        #   unverified_claims = get_unverified_token_claims(token=access_token)
        #   decoded_token = decode_token(
        #       access_token,
        #       get_platform_public_keyset().get("public_keyset"),
        #       unverified_claims.get("aud"))
        decoded_token = validate_and_decode_token(token)

        user_scopes = decoded_token["scope"].split(" ")
        for scope in allowed_scopes:
          if scope in user_scopes:
            return func(*args, **kwargs)
        raise InvalidTokenError("Unauthorized due to invalid scope")

      except (InvalidTokenError, JWSError, ExpiredSignatureError,
              JWTError) as e:
        raise Unauthenticated(str(e)) from e

    return wrapper

  return decorator


def get_tool_info(token: auth_scheme = Depends()):
  decoded_token = validate_and_decode_token(token)
  print("dec tok sub", decoded_token.get("sub"))
  tool_config = Tool.find_by_client_id(decoded_token.get("sub"))
  print("tool_config", tool_config)
  return tool_config