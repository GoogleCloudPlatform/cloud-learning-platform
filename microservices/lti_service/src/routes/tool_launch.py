""" Launch endpoints for LTI as a tool """
from copy import deepcopy
from config import ERROR_RESPONSES
from fastapi import APIRouter, Request, Form
from fastapi.security import HTTPBearer
from fastapi.templating import Jinja2Templates

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
  return templates.TemplateResponse("tool.html", {
      "request": request,
      "id_token": id_token,
      "state": state
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
  return True
