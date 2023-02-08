"""
Pydantic Model for LTI Content Item API's
"""
from pydantic import BaseModel
from typing import List, Optional
from schemas.schema_examples import (BASIC_CONTENT_ITEM_EXAMPLE,
                                     FULL_CONTENT_ITEM_EXAMPLE)


class BasicLTIContentItemModel(BaseModel):
  """Basic Content Item Pydantic Model"""
  tool_id: str
  content_item_type: str
  content_item_info: dict


class FullLTIContentItemModel(BasicLTIContentItemModel):
  """Content Item Model with id, created and last modified time"""
  id: str
  created_time: str
  last_modified_time: str


class LTIContentItemModel(BasicLTIContentItemModel):
  """Content Item Input Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_CONTENT_ITEM_EXAMPLE}
    extra = "forbid"


class UpdateLTIContentItemModel(BaseModel):
  """Update Content Item Pydantic Model"""
  tool_id: Optional[str]
  content_item_type: Optional[str]
  content_item_info: Optional[dict]

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_CONTENT_ITEM_EXAMPLE}
    extra = "forbid"


class LTIContentItemResponseModel(BaseModel):
  """Content Item Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the content item"
  data: FullLTIContentItemModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the content item",
            "data": FULL_CONTENT_ITEM_EXAMPLE
        }
    }


class DeleteLTIContentItem(BaseModel):
  """Delete Content Item Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the content item"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the content item"
        }
    }


class LTIContentItemSearchResponseModel(BaseModel):
  """Content Item Search Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the content items"
  data: List[FullLTIContentItemModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the content items",
            "data": [FULL_CONTENT_ITEM_EXAMPLE]
        }
    }


class AllLTIContentItemsResponseModel(BaseModel):
  """Content Item Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Data fetched successfully"
  data: List[FullLTIContentItemModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Data fetched successfully",
            "data": [FULL_CONTENT_ITEM_EXAMPLE]
        }
    }
