"""
Pydantic Model for FAQ API's
"""
from typing import Optional, List
from typing_extensions import Literal
from pydantic import BaseModel, constr
from schemas.schema_examples import BASIC_FAQ_CONTENT_EXAMPLE, FULL_FAQ_CONTENT_EXAMPLE

#pylint: disable=invalid-name
ALLOWED_FAQ_TYPES = Literal["faq_item", "faq_group"]


class BasicFAQModel(BaseModel):
  """FAQ Content Pydantic model"""
  resource_path: Optional[str]
  name: Optional[constr(max_length=100)]
  curriculum_pathway_id: Optional[str]

class FullFAQModel(BasicFAQModel):
  """FAQ Skeleton Model with uuid, created and updated time"""
  uuid: str
  is_archived: Optional[bool] = False
  is_deleted: Optional[bool] = False
  created_time: str
  last_modified_time: str


class FAQModel(BasicFAQModel):
  """FAQ Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_FAQ_CONTENT_EXAMPLE}
    extra = "forbid"


class GetFAQResponseModel(BaseModel):
  """Batch Job Response Pydantic Model"""
  success: bool
  message: str
  data: FullFAQModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched FAQ by UUID",
            "data": {
                **FULL_FAQ_CONTENT_EXAMPLE
            }
        }
    }


class TotalCountResponseModel(BaseModel):
  records: Optional[List[FullFAQModel]]
  total_count: int

class SearchFAQResponseModel(BaseModel):
  """Search FAQ Response Pydantic Model"""
  success: bool
  message: str
  data: TotalCountResponseModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched FAQs",
            "data": {
                      "records":[FULL_FAQ_CONTENT_EXAMPLE],
                      "total_count": 50
                    }
        }
    }


class CreateFAQResponseModel(BaseModel):
  """Create FAQ Response Pydantic Model"""
  success: bool
  message: str
  data: FullFAQModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created FAQ",
            "data": FULL_FAQ_CONTENT_EXAMPLE
        }
    }


class UpdateFAQResponseModel(BaseModel):
  """Update FAQ Response Pydantic Model"""
  success: bool
  message: str
  data: FullFAQModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully updated FAQ",
            "data": FULL_FAQ_CONTENT_EXAMPLE
        }
    }


class DeleteFAQResponseModel(BaseModel):
  """Delete FAQ Response Pydantic Model"""
  success: bool
  message: str

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted FAQ"
        }
    }
