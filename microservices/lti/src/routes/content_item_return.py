"""Content Item  Return endpoint for LTI Service as Platform"""
from copy import deepcopy
from config import ERROR_RESPONSES
from fastapi import APIRouter, Form
from common.models import Tool
from common.utils.errors import (ResourceNotFoundException)
from common.utils.http_exceptions import (InternalServerError, ResourceNotFound)
from schemas.error_schema import NotFoundErrorResponseModel
from services.keys_manager import get_remote_keyset
from services.lti_token import decode_token, lti_claim_field, get_unverified_token_claims

# pylint: disable=invalid-name

ERROR_RESPONSE_DICT = deepcopy(ERROR_RESPONSES)
del ERROR_RESPONSE_DICT[401]

router = APIRouter(
    tags=["Content Item Return Endpoint"], responses=ERROR_RESPONSE_DICT)


@router.get(
    "/content-item-return",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }},
    name="DeepLinking Response API for Content Item")
def content_item_return(JWT: str = Form()):
  """
    This endpoint which will be used by tool for sending deeplinking response
    for content selection.
    Args:
      JWT: jwt token encoded using private key of tool

    After this endpoint is triggered by tool, Platform should process the
    content that is received in the jwt token
  """
  try:
    # decode token to fetch claims without token verification
    unverified_claims = get_unverified_token_claims(token=JWT)

    tool_config = Tool.find_by_client_id(unverified_claims.get("iss"))

    if tool_config.get("public_key_type") == "JWK URL":
      key = get_remote_keyset(tool_config.get("tool_keyset_url"))
    elif tool_config.get("public_key_type") == "Public Key":
      key = tool_config.get("tool_public_key")

    decoded_data = decode_token(JWT, key)
    content_item_key = lti_claim_field("claim", "content_items", "dl")
    content_item_data = decoded_data[content_item_key]
    # TODO: Once the content-item datamodel is implemented, save the
    # decoded_data[content_item_key] in it and link it to the learning resource.
    return {
        "success": True,
        "message": "Successfully received and decoded content item",
        "data": content_item_data
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
