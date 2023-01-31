"""LTI Tool Auth endpoints"""
from uuid import uuid4
from copy import deepcopy
from config import ERROR_RESPONSES
from fastapi import APIRouter, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from common.models import Platform, LTISession
from common.utils.errors import (ResourceNotFoundException, ValidationError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound)
from schemas.error_schema import NotFoundErrorResponseModel
from services.keys_manager import get_tool_public_keyset
from urllib.parse import urlparse, urlunparse, urlencode, parse_qsl

ERROR_RESPONSE_DICT = deepcopy(ERROR_RESPONSES)
del ERROR_RESPONSE_DICT[401]

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    tags=["Authentication Endpoints for LTI service as a Tool"],
    responses=ERROR_RESPONSE_DICT)


@router.get(
    "/jwks/{platform_id}",
    name="Tool JWKS Endpoint",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def tool_jwks(platform_id: str):
  """Get the public keys of the tool.
  ### Path Params:
  platform_id: `str`
    The uuid of the platform
  ### Raises:
  ResourceNotFoundException:
    If the platform with given uuid does not exist <br/>
  Internal Server Error:
    Raised if something went wrong.
  ### Returns:
  JWKS: `JSON`
    Returns public key set JSON
  """
  try:
    Platform.find_by_id(platform_id)
    keyset = get_tool_public_keyset()
    return keyset.get("public_keyset")
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/oidc-login",
    name="OIDC Login Endpoint",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def oidc_login(iss: str = Form(),
               client_id: str = Form(),
               target_link_uri: str = Form(),
               login_hint: str = Form(),
               lti_message_hint: str = Form(None),
               lti_deployment_id: str = Form(None)):
  """
    Validates the issuer and initiate a login process with the platform
    ### Raises:
    ResourceNotFoundException:
      Raised if the platform with given issuer does not exist <br/>
    ValidationError:
      Raised if the platform details doesn't have provided client_id <br/>
    Internal Server Error:
      Raised if something went wrong.
  """
  try:
    # TODO: Currently the issuer should be unique. The combination of client_id
    # and issuer should be unique
    platform = Platform.find_by_issuer(iss)
    if platform is None:
      raise ResourceNotFoundException(f"Platform with issuer '{iss}' not found")
    platform_data = platform.get_fields(reformat_datetime=True)

    if client_id != platform_data.get("client_id"):
      raise ValidationError("Incorrect client ID")

    # TODO: Move the creation of state and nonce to services
    state = str(uuid4())
    nonce = str(uuid4())

    # save state and nonce in database
    new_lti_session = LTISession()
    new_lti_session.uuid = ""
    new_lti_session.state = state
    new_lti_session.nonce = nonce
    new_lti_session.user_id = login_hint
    new_lti_session.client_id = client_id
    new_lti_session.save()
    new_lti_session.uuid = new_lti_session.id
    new_lti_session.update()

    auth_url = urlparse(platform_data.get("platform_auth_url"))
    query_params = parse_qsl(auth_url.query)
    query_params.extend([("scope", "openid"), ("response_type", "id_token"),
                         ("response_mode", "form_post"), ("prompt", "none"),
                         ("client_id", client_id),
                         ("redirect_uri", target_link_uri),
                         ("login_hint", login_hint), ("state", state),
                         ("nonce", nonce)])
    if lti_message_hint:
      query_params.append(("lti_message_hint", lti_message_hint))
    if lti_deployment_id:
      query_params.append(("lti_deployment_id", lti_deployment_id))

    redirect_url = urlunparse(
        (auth_url.scheme, auth_url.netloc, auth_url.path, auth_url.params,
         urlencode(query_params), auth_url.fragment))
    return RedirectResponse(url=redirect_url, status_code=302)

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
