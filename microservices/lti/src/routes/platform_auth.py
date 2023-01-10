"""LTI Platform Auth endpoints"""
from copy import deepcopy
from datetime import datetime
from config import ERROR_RESPONSES, ISSUER, TOKEN_TTL
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from common.utils.errors import (ResourceNotFoundException, ValidationError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound)
from common.models import Tool
from services.keys_manager import get_platform_public_keyset, get_remote_keyset
from services.lti_token import (lti_claim_field, generate_token_claims,
                                encode_token, decode_token,
                                get_unverified_token_claims)
from schemas.error_schema import NotFoundErrorResponseModel
# pylint: disable=too-many-function-args
# pylint: disable=line-too-long
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


@router.post(
    "/authorize",
    name="POST method for Authorization Endpoint",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def post_authorize(request: Request,
                   client_id: str = Form(),
                   login_hint: str = Form(),
                   lti_message_hint: str = Form(),
                   redirect_uri: str = Form(),
                   nonce: str = Form(),
                   state: str = Form(),
                   scope: str = Form(default="openid"),
                   response_type: str = Form(default="id_token"),
                   response_mode: str = Form(default="form_post"),
                   prompt: str = Form(default="none")):
  """
    Generate a LTI Message (jwt token) which is encoded using a private rsa key
    of platform and return it back to provided redirect_uri
  """
  return authorize(
      request=request,
      client_id=client_id,
      login_hint=login_hint,
      lti_message_hint=lti_message_hint,
      redirect_uri=redirect_uri,
      nonce=nonce,
      state=state,
      scope=scope,
      response_type=response_type,
      response_mode=response_mode,
      prompt=prompt)


@router.get(
    "/authorize",
    name="GET method for Authorization Endpoint",
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
      if token_claims.get(lti_claim_field("claim", "target_link_uri")):
        redirect_uri = token_claims.get(
            lti_claim_field("claim", "target_link_uri"))

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
def generate_token(
    grant_type: str = Form(default="client_credentials"),
    client_assertion_type: str = Form(
        default="urn:ietf:params:oauth:client-assertion-type:jwt-bearer"),
    client_assertion: str = Form(),
    scope: str = Form()):
  """The generate token endpoint will be used to generate the id token"""
  try:
    valid_scopes = [
        lti_claim_field("scope", "lineitem", "ags"),
        lti_claim_field("scope", "lineitem.readonly", "ags"),
        lti_claim_field("scope", "result.readonly", "ags"),
        lti_claim_field("scope", "score", "ags")
    ]
    scopes = scope.split(" ")
    required_scopes = []
    for received_scope in scopes:
      if received_scope in valid_scopes:
        required_scopes.append(received_scope)

    if grant_type != "client_credentials":
      raise ValidationError("Invalid grant_type")
    if client_assertion_type != "urn:ietf:params:oauth:client-assertion-type:jwt-bearer":
      raise ValidationError("Invalid client_assertion_type")

    if len(required_scopes) == 0:
      raise ValidationError("Invalid scope")
    # client_assertion jwt should consist of following claims when requesting
    # for token
    # iss :- Issuer (Domain of the application which requests the access token)
    # iat :- Token generated time
    # exp :- Token expiration time
    # aud :- Audience (endpoint URL of this access token api [/token])
    # sub :- Client ID (client ID provided by the platform after the external
    # tool creation)

    unverified_claims = get_unverified_token_claims(token=client_assertion)
    tool_config = Tool.find_by_client_id(unverified_claims.get("sub"))

    if tool_config.public_key_type == "JWK URL":
      key = get_remote_keyset(tool_config.tool_keyset_url)
    elif tool_config.public_key_type == "Public Key":
      key = tool_config.tool_public_key

    claims = decode_token(
        token=client_assertion, key=key, audience=unverified_claims.get("aud"))

    required_scopes_str = " ".join(required_scopes)
    token_claims = {
        "iss": ISSUER,
        "aud": claims.get("sub"),
        "iat": int(datetime.now().timestamp()),
        "exp": int(datetime.now().timestamp()) + TOKEN_TTL,
        "sub": claims.get("sub"),
        "scope": required_scopes_str
    }

    return {
        "access_token": encode_token(token_claims),
        "token_type": "bearer",
        "expires_in": 3600,
        "scope": required_scopes_str
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
