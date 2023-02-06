""" Launch endpoints for LTI as a platform """
from copy import deepcopy
from config import ERROR_RESPONSES, LTI_ISSUER_DOMAIN
from fastapi import APIRouter
from fastapi.security import HTTPBearer
from fastapi.templating import Jinja2Templates
from common.models import Tool, LTIContentItem
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 TokenNotFoundError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound)
from urllib.parse import urlparse, urlunparse, urlencode, parse_qsl
from schemas.error_schema import NotFoundErrorResponseModel

ERROR_RESPONSE_DICT = deepcopy(ERROR_RESPONSES)
del ERROR_RESPONSE_DICT[401]

auth_scheme = HTTPBearer(auto_error=False)
templates = Jinja2Templates(directory="templates")

router = APIRouter(
    tags=["Launch Endpoints for LTI Service as a Platform"],
    responses=ERROR_RESPONSE_DICT)


@router.get(
    "/resource-launch-init",
    name="Resource launch endpoint for LTI initiation",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def resource_launch_init(lti_content_item_id: str, user_id: str):
  """The resource launch init endpoint will initiate the process to
  fetch a content item and then redirect the request to the tool login url.
  ### Args:
  lti_content_item_id: `str`
    UUID of the content item <br/>
  user_id: `str`
    UUID of the User <br/>
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
      if tool:
        tool_data = tool.get_fields(reformat_datetime=True)
        # """Redirect request to tool login endpoint"""
        # using client_id and deployment_id, fetch tool_login_url
        login_url = urlparse(tool_data.get("tool_login_url"))
        query_params = parse_qsl(login_url.query)
        query_params.extend([("login_hint", user_id),
                             ("lti_message_hint", lti_content_item_id),
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
    raise InternalServerError(str(e)) from e


@router.get(
    "/content-selection-launch-init",
    name="Content selection launch endpoint for LTI initiation",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def content_selection_launch_init(tool_id: str, user_id: str):
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

      query_params = parse_qsl(login_url.query)
      query_params.extend([("login_hint", user_id),
                           ("lti_message_hint", "deep_link"), ("iss", LTI_ISSUER_DOMAIN),
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
    raise InternalServerError(str(e)) from e
