"""
Pydantic Model for Tool API's
"""
from typing import List, Optional
from pydantic import BaseModel
from typing_extensions import Literal
from schemas.schema_examples import (BASIC_TOOL_EXAMPLE, FULL_TOOL_EXAMPLE)
from config import LTI_ISSUER_DOMAIN

# pylint: disable = invalid-name
ALLOWED_PUBLIC_KEY_TYPES = Literal["JWK URL", "Public Key"]
ALLOWED_TOOL_TYPES = Literal["Allow once per context", "Not required",
                             "Allow everytime"]


class BasicToolModel(BaseModel):
  """Basic Tool Pydantic Model"""
  name: str
  description: Optional[str]
  tool_url: str
  tool_login_url: str
  public_key_type: ALLOWED_PUBLIC_KEY_TYPES
  tool_public_key: Optional[str]
  tool_keyset_url: Optional[str]
  content_selection_url: Optional[str]
  redirect_uris: list
  enable_grade_sync: Optional[bool] = False
  enable_nrps: Optional[bool] = False
  custom_params: Optional[str]
  validate_title_for_grade_sync: Optional[bool] = False
  deeplink_type: ALLOWED_TOOL_TYPES


class FullToolModel(BasicToolModel):
  """Tool Model with id, created and last modified time"""
  id: str
  client_id: str
  deployment_id: str
  issuer: str = LTI_ISSUER_DOMAIN
  platform_auth_url: str = f"{LTI_ISSUER_DOMAIN}/lti/api/v1/authorize"
  platform_token_url: str = f"{LTI_ISSUER_DOMAIN}/lti/api/v1/token"
  platform_keyset_url: str = f"{LTI_ISSUER_DOMAIN}/lti/api/v1/jwks"
  created_time: str
  last_modified_time: str


class ToolModel(BasicToolModel):
  """Tool Input Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_TOOL_EXAMPLE}
    extra = "forbid"


class UpdateToolModel(BaseModel):
  """Update Tool Pydantic Model"""
  name: Optional[str]
  description: Optional[str]
  tool_url: Optional[str]
  tool_login_url: Optional[str]
  public_key_type: ALLOWED_PUBLIC_KEY_TYPES
  tool_public_key: Optional[str]
  tool_keyset_url: Optional[str]
  content_selection_url: Optional[str]
  redirect_uris: Optional[list]
  enable_grade_sync: Optional[bool]
  enable_nrps: Optional[bool]
  custom_params: Optional[str]
  validate_title_for_grade_sync: Optional[bool]
  deeplink_type: ALLOWED_TOOL_TYPES

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_TOOL_EXAMPLE}
    extra = "forbid"


class ToolResponseModel(BaseModel):
  """Tool Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the tool"
  data: FullToolModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the tool",
            "data": FULL_TOOL_EXAMPLE
        }
    }


class DeleteTool(BaseModel):
  """Delete Tool Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the tool"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the tool"
        }
    }


class ToolSearchResponseModel(BaseModel):
  """Tool Search Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the tools"
  data: List[FullToolModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the tools",
            "data": [FULL_TOOL_EXAMPLE]
        }
    }


class AllToolsResponseModel(BaseModel):
  """Tool Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Data fetched successfully"
  data: List[FullToolModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Data fetched successfully",
            "data": [FULL_TOOL_EXAMPLE]
        }
    }
