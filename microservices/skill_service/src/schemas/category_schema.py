"""
Pydantic Model for Category API's
"""
from typing import List, Optional
from pydantic import BaseModel
from schemas.schema_examples import (BASIC_CATEGORY_MODEL_EXAMPLE,
                                     FULL_CATEGORY_MODEL_EXAMPLE)
# pylint: disable=line-too-long

class ParentNodes(BaseModel):
  """Child Nodes Pydantic Model"""
  sub_domains: Optional[list] = []

class ChildNodes(BaseModel):
  """Child Nodes Pydantic Model"""
  competencies: Optional[list] = []

class BasicCategoryModel(BaseModel):
  """Category Skeleton Pydantic Model"""
  name: str
  description: str
  keywords: Optional[List[str]] = [""]
  parent_nodes: Optional[ParentNodes] = {}
  child_nodes: Optional[ChildNodes] = {}
  reference_id: Optional[str] = ""
  source_uri: Optional[str] = ""
  source_name: Optional[str] = ""


class FullCategoryDataModel(BasicCategoryModel):
  """Category Skeleton Model with uuid, created and updated time"""
  uuid: str
  created_time: str
  last_modified_time: str


class CategoryModel(BasicCategoryModel):
  """Category Input Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_CATEGORY_MODEL_EXAMPLE}


class UpdateCategoryModel(BasicCategoryModel):
  """Update Category Pydantic Model"""
  name: Optional[str]
  description: Optional[str]

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_CATEGORY_MODEL_EXAMPLE}


class GetCategoryResponseModel(BaseModel):
  """Category Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the category"
  data: Optional[FullCategoryDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the category",
            "data": FULL_CATEGORY_MODEL_EXAMPLE
        }
    }


class PostCategoryResponseModel(BaseModel):
  """Category Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the category"
  data: Optional[FullCategoryDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the category",
            "data": FULL_CATEGORY_MODEL_EXAMPLE
        }
    }


class UpdateCategoryResponseModel(BaseModel):
  """Category Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the category"
  data: Optional[FullCategoryDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully updated the category",
            "data": FULL_CATEGORY_MODEL_EXAMPLE
        }
    }


class DeleteCategory(BaseModel):
  """Delete Category Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the category"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the category"
        }
    }


class AllCategoryResponseModel(BaseModel):
  """Category Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the category"
  data: Optional[List[FullCategoryDataModel]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the category",
            "data": [FULL_CATEGORY_MODEL_EXAMPLE]
        }
    }


class CategoryImportJsonResponse(BaseModel):
  """Category Import Json Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the categories"
  data: Optional[List[str]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success":
                True,
            "message":
                "Successfully created the categories",
            "data": [
                "44qxEpc35pVMb6AkZGbi", "00MPqUhCbyPe1BcevQDr",
                "lQRzcrRuDpJ9IoW8bCHu"
            ]
        }
    }
