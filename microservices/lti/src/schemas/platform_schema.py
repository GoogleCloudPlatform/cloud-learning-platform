"""
Pydantic Model for Platform API's
"""
from pydantic import BaseModel
from typing import List, Optional
from schemas.schema_examples import (BASIC_PLATFORM_EXAMPLE,
                                     FULL_PLATFORM_EXAMPLE)


class BasicPlatformModel(BaseModel):
  """Basic Platform Pydantic Model"""
  name: str
  description: Optional[str]
  issuer: str
  client_id: str
  platform_keyset_url: str
  platform_auth_url: str
  platform_token_url: str
  deployment_ids: List


class FullPlatformModel(BasicPlatformModel):
  """Platform Model with id, created and last modified time"""
  id: str
  tool_url: str
  tool_login_url: str
  tool_keyset_url: str
  created_time: str
  last_modified_time: str


class PlatformModel(BasicPlatformModel):
  """Platform Input Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_PLATFORM_EXAMPLE}
    extra = "forbid"


class UpdatePlatformModel(BaseModel):
  """Update Platform Pydantic Model"""
  name: Optional[str]
  description: Optional[str]
  issuer: Optional[str]
  client_id: Optional[str]
  platform_keyset_url: Optional[str]
  platform_auth_url: Optional[str]
  platform_token_url: Optional[str]
  deployment_ids: Optional[list]

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_PLATFORM_EXAMPLE}
    extra = "forbid"


class PlatformResponseModel(BaseModel):
  """Platform Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the platform"
  data: FullPlatformModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the platform",
            "data": FULL_PLATFORM_EXAMPLE
        }
    }


class DeletePlatform(BaseModel):
  """Delete Platform Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the platform"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the platform"
        }
    }


class PlatformSearchResponseModel(BaseModel):
  """Platform Search Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the platforms"
  data: List[FullPlatformModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the platforms",
            "data": [FULL_PLATFORM_EXAMPLE]
        }
    }


class AllPlatformsResponseModel(BaseModel):
  """Platform Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Data fetched successfully"
  data: List[FullPlatformModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Data fetched successfully",
            "data": [FULL_PLATFORM_EXAMPLE]
        }
    }
