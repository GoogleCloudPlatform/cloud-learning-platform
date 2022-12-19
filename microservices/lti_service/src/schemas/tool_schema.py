"""
Pydantic Model for Tool API's
"""
from pydantic import BaseModel
from typing import List, Optional
from typing_extensions import Literal
from schemas.schema_examples import (BASIC_TOOL_EXAMPLE, FULL_TOOL_EXAMPLE)
from config import ISSUER

ALLOWED_PUBLIC_KEY_TYPES = Literal["JWK URL", "Public Key"]


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


class FullToolModel(BasicToolModel):
  """Tool Model with uuid, created and last modified time"""
  uuid: str
  client_id: str
  deployment_id: str
  issuer: str = ISSUER
  platform_auth_url: str = f"{ISSUER}/lti-service/api/v1/authorize"
  platform_token_url: str = f"{ISSUER}/lti-service/api/v1/token"
  platform_keyset_url: str = f"{ISSUER}/lti-service/api/v1/jwks"
  is_archived: Optional[bool] = False
  created_timestamp: str
  last_updated_timestamp: str


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
  is_archived: Optional[bool]

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
