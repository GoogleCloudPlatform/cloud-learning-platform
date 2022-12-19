"""LTI Platform Auth endpoints"""
from copy import deepcopy
from config import ERROR_RESPONSES
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from common.utils.errors import (ResourceNotFoundException, ValidationError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, APINotImplemented)
from services.keys_manager import get_platform_public_keyset
from services.lti_token import generate_token_claims, encode_token
from schemas.error_schema import NotFoundErrorResponseModel

# pylint: disable=too-many-function-args
ERROR_RESPONSE_DICT = deepcopy(ERROR_RESPONSES)
del ERROR_RESPONSE_DICT[401]
templates = Jinja2Templates(directory="templates")

router = APIRouter(
    tags=["Authentication Endpoints for LTI service as a Platform"],
    responses=ERROR_RESPONSE_DICT)


@router.get("/jwks", name="Platform JWKS Endpoint")
def platform_jwks():
  """Get the public keys of the platform"""
  key_set = get_platform_public_keyset()
  return key_set.get("public_keyset")


# TODO: add post method for /authorize endpoint(optional)
@router.get(
    "/authorize",
    name="Authorization Endpoint",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def authorize(request: Request,
              client_id: str,
              login_hint: str,
              lti_message_hint: str,
              redirect_uri: str,
              nonce: str,
              state: str,
              scope: str = "openid",
              response_type: str = "id_token",
              response_mode: str = "form_post",
              prompt: str = "none"):
  """
    Generate a LTI Message (jwt token) which is encoded using a private rsa key
    of platform and return it back to provided redirect_uri
  """
  try:
    if scope != "openid":
      raise ValidationError("Invalid scope provided")
    if response_type != "id_token":
      raise ValidationError("Invalid response_type provided")
    if prompt != "none":
      raise ValidationError("Invalid prompt provided")

    if lti_message_hint == "deep_link":  # this is DeepLinkingRequest
      token_claims = generate_token_claims("deep_link", client_id, login_hint,
                                           lti_message_hint, nonce,
                                           redirect_uri)
    else:  # this is ResourceLinkRequest
      token_claims = generate_token_claims("resource_link", client_id,
                                           login_hint, lti_message_hint, nonce,
                                           redirect_uri)

    token = encode_token(token_claims)

    if response_mode == "form_post":
      return templates.TemplateResponse(
          "auth.html", {
              "request": request,
              "id_token": token,
              "state": state,
              "redirect_uri": redirect_uri
          })
    else:
      return {
          "success": True,
          "message": "Generated token successfully",
          "data": {
              "id_token": token,
              "state": state,
              "redirect_uri": redirect_uri
          }
      }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post("/token", name="Token Endpoint")
def generate_token():
  """The generate token endpoint will be used to generate the id token
  APINotImplemented: The API is not yet implemented
  """
  raise APINotImplemented()
