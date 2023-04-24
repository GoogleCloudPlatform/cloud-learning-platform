""" Launch endpoints for LTI as a platform """
import traceback
from copy import deepcopy
from typing import Optional
from config import ERROR_RESPONSES, LTI_ISSUER_DOMAIN
from fastapi import APIRouter
from fastapi.security import HTTPBearer
from fastapi.templating import Jinja2Templates
from common.models import Tool, LTIContentItem
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 TokenNotFoundError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound)
from common.utils.logging_handler import Logger
from urllib.parse import urlparse, urlunparse, urlencode, parse_qsl
from schemas.error_schema import NotFoundErrorResponseModel
from services.lti_token import encode_token

# pylint: disable=dangerous-default-value

ERROR_RESPONSE_DICT = deepcopy(ERROR_RESPONSES)
del ERROR_RESPONSE_DICT[401]

auth_scheme = HTTPBearer(auto_error=False)
templates = Jinja2Templates(directory="templates")

router = APIRouter(
    tags=["Launch Endpoints for LTI Service as a Platform"],
    responses=ERROR_RESPONSE_DICT)


@router.post(
    "/resource-launch-init",
    name="Resource launch endpoint for LTI initiation",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def post_resource_launch_init(lti_content_item_id: str,
                              user_id: str,
                              context_id: str,
                              custom_params: Optional[dict] = {}):
  """Post method for the resource launch init endpoint"""
  return get_resource_launch_init(lti_content_item_id, user_id, context_id,
                                  custom_params)


@router.get(
    "/resource-launch-init",
    name="Resource launch endpoint for LTI initiation",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_resource_launch_init(lti_content_item_id: str,
                             user_id: str,
                             context_id: str,
                             custom_params: Optional[dict] = {}):
  """The resource launch init endpoint will initiate the process to
  fetch a content item and then redirect the request to the tool login url.
  ### Args:
  lti_content_item_id: `str`
    UUID of the content item <br/>
  user_id: `str`
    UUID of the User <br/>
  context_id: `str`
    ID of the context of the given resource <br/>
  ### Raises:
  ResourceNotFoundException:
    If the LTI content item or tool does not exist. <br/>
  TokenNotFoundError:
    If the bearer token is not provided <br/>
  Internal Server Error:
     Raised if something went wrong <br/>
  """
  try:
    lti_content_item = LTIContentItem.find_by_id(lti_content_item_id)

    if lti_content_item:
      tool = Tool.find_by_id(lti_content_item.tool_id)
      final_lti_message_hint_dict = {
          "lti_request_type":
              "resource_link",
          "custom_params_for_substitution":
              custom_params.get("custom_params_for_substitution"),
          "lti_content_item_id":
              lti_content_item_id,
          "context_id":
              context_id,
          "context_type":
              custom_params.get("context_type")
      }
      lti_message_hint = encode_token(final_lti_message_hint_dict)

      if tool:
        tool_data = tool.get_fields(reformat_datetime=True)
        # build a url for tool login endpoint
        login_url = urlparse(tool_data.get("tool_login_url"))
        query_params = parse_qsl(login_url.query)
        query_params.extend([("login_hint", user_id),
                             ("lti_message_hint", lti_message_hint),
                             ("iss", LTI_ISSUER_DOMAIN),
                             ("target_link_uri", tool_data.get("tool_url")),
                             ("client_id", tool_data.get("client_id")),
                             ("lti_deployment_id",
                              tool_data.get("deployment_id"))])

        redirect_url = urlunparse(
            (login_url.scheme, login_url.netloc, login_url.path,
             login_url.params, urlencode(query_params), login_url.fragment))

        return {"url": redirect_url}
      else:
        raise ResourceNotFoundException(
            "Tool for the requested resource is not available")

    else:
      raise ResourceNotFoundException("Requested resource is not available")

  except ValidationError as e:
    raise BadRequest(str(e), data=e.data) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except TokenNotFoundError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
    "/content-selection-launch-init",
    name="Content selection launch endpoint for LTI initiation",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def content_selection_launch_init(tool_id: str, user_id: str, context_id: str):
  """The content selection launch init endpoint is used to initiate
  the process to choose the content from the selected external tool
  and then redirect the request to the tool login url.
  ### Args:
  tool_id: `str`
    UUID of the tool <br/>
  user_id: `str`
    UUID of the User <br/>
  ### Raises:
  ResourceNotFoundException:
    If the tool does not exist. <br/>
  TokenNotFoundError:
    If the bearer token is not provided <br/>
  Internal Server Error:
    Raised if something went wrong
  ### Returns:
  Redirect Request to the tool endpoint : `RedirectResponse`
  """
  try:
    tool = Tool.find_by_id(tool_id)

    if tool:
      tool_data = tool.get_fields(reformat_datetime=True)
      # Redirect request to tool login endpoint
      login_url = urlparse(tool_data.get("tool_login_url"))

      if tool_data.get("content_selection_url"):
        target_link_uri = tool_data.get("content_selection_url")
      else:
        target_link_uri = tool_data.get("tool_url")

      lti_message_hint_dict = {
          "lti_request_type": "deep_link",
          "context_id": context_id
      }

      lti_message_hint = encode_token(lti_message_hint_dict)

      query_params = parse_qsl(login_url.query)
      query_params.extend([("login_hint", user_id),
                           ("lti_message_hint", lti_message_hint),
                           ("iss", LTI_ISSUER_DOMAIN),
                           ("target_link_uri", target_link_uri),
                           ("client_id", tool_data.get("client_id")),
                           ("lti_deployment_id", tool_data.get("deployment_id"))
                          ])

      redirect_url = urlunparse(
          (login_url.scheme, login_url.netloc, login_url.path, login_url.params,
           urlencode(query_params), login_url.fragment))

      return {"url": redirect_url}

  except ValidationError as e:
    raise BadRequest(str(e), data=e.data) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except TokenNotFoundError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
