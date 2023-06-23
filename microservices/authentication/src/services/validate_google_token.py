"""Method to validate google auth token"""
from google.oauth2 import id_token
from google.auth.transport import requests
from common.utils.errors import InvalidTokenError
from common.utils.http_exceptions import InternalServerError, Unauthenticated


def validate_google_oauth_token(token):
  try:
    # If the ID token is valid. Get the user's Google Account ID from the
    # decoded token.
    return id_token.verify_oauth2_token(token, requests.Request())
  except (ValueError, InvalidTokenError) as e:
    raise Unauthenticated(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
