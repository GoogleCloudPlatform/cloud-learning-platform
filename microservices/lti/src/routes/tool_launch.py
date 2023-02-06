""" Launch endpoints for LTI as a tool """
import json
from copy import deepcopy
from config import ERROR_RESPONSES, LTI_ISSUER_DOMAIN
from services.lti_token import lti_claim_field, get_unverified_token_claims
from fastapi import APIRouter, Request, Form
from fastapi.security import HTTPBearer
from fastapi.templating import Jinja2Templates
# pylint: disable = line-too-long

ERROR_RESPONSE_DICT = deepcopy(ERROR_RESPONSES)
del ERROR_RESPONSE_DICT[401]

auth_scheme = HTTPBearer(auto_error=False)
templates = Jinja2Templates(directory="templates")

router = APIRouter(
    tags=["Launch Endpoints for LTI Service as a Tool"],
    responses=ERROR_RESPONSE_DICT)


@router.post(
    "/content-selection-launch", name="Content Selection Launch Endpoint")
def content_selection_launch(request: Request,
                             id_token: str = Form(),
                             state: str = Form()):
  """
    This endpoint will accept DeepLinkingRequest and will accordingly redirect
    to requested User Interface.
  """
  # TODO: verify id_token using platform_config.jwks url
  # TODO: research a way to verify state and nonce for mitigating replay attacks
  # and csrf attacks
  # TODO: add a check for the message type claim to be LtiDeepLinkingRequest
  unverified_claims = get_unverified_token_claims(token=id_token)
  unverified_claims_dict = json.loads(unverified_claims)

  deep_link_return_url = unverified_claims_dict.get(
      lti_claim_field("claim", "deep_linking_settings",
                      "dl")).get("deep_link_return_url")

  content_return_url = LTI_ISSUER_DOMAIN + "/lti/api/v1/content-selection-response"
  # decoded_token = jwt.decode(token=id_token, algorithms="RS256")
  # decoded_token = decode_token(id_token, key)
  return templates.TemplateResponse(
      "tool.html", {
          "request": request,
          "id_token": id_token,
          "state": state,
          "content_return_url": content_return_url,
          "deep_link_return_url": deep_link_return_url
      })


@router.post(
    "/content-selection-response", name="Content Selection Response Endpoint")
def content_selection_response():
  """
    This endpoint will provide DeepLinkingResponse to
    platforms DeepLinkingRequest
  """
  # TODO: Generate a DeepLinkingResponse token to send back to
  # deep-link-return-url sent by the platform
  # Input -> resource info, deep_link_return_url, encode token
  return True


@router.post("/resource-launch", name="Resource launch Endpoint")
def resource_launch():
  """
    This endpoint will launch the requested resource from the
    LtiResourceLinkRequest message
  """
  # TODO: verify id_token using platform_config jwks url
  # TODO: research a way to verify state and nonce for mitigating replay attacks
  # and csrf attacks
  # TODO: add a check for the message type claim to be LtiResourceLinkRequest
  return True
