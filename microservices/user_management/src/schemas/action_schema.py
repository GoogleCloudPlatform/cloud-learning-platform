"""
Pydantic Model for Action API's
"""
from typing import List, Optional
from typing_extensions import Literal
from pydantic import BaseModel, Extra
from schemas.schema_examples import (BASIC_ACTION_MODEL_EXAMPLE,
                                     FULL_ACTION_MODEL_EXAMPLE)

# pylint: disable=invalid-name
ALLOWED_ACTION_TYPES = Literal["main","other"]

class BasicActionModel(BaseModel):
  """Action Skeleton Pydantic Model"""
  # uuid: str
  name: str
  description: str
  action_type: ALLOWED_ACTION_TYPES


class FullActionDataModel(BasicActionModel):
  """Action Model with uuid, created and updated time"""
  uuid: str
  created_time: str
  last_modified_time: str


class ActionModel(BasicActionModel):
  """Action Input Pydantic Model"""

  class Config():
    orm_mode = True
    extra = Extra.forbid
    schema_extra = {"example": BASIC_ACTION_MODEL_EXAMPLE}


class UpdateActionModel(BaseModel):
  """Update Action Pydantic Request Model"""
  name: Optional[str]
  description: Optional[str]
  action_type: Optional[ALLOWED_ACTION_TYPES]

  class Config():
    orm_mode = True
    extra = Extra.forbid
    schema_extra = {"example": BASIC_ACTION_MODEL_EXAMPLE}


class GetActionResponseModel(BaseModel):
  """Action Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the action"
  data: Optional[FullActionDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the action",
            "data": FULL_ACTION_MODEL_EXAMPLE
        }
    }


class PostActionResponseModel(BaseModel):
  """Action Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the action"
  data: FullActionDataModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the action",
            "data": FULL_ACTION_MODEL_EXAMPLE
        }
    }


class UpdateActionResponseModel(BaseModel):
  """Action Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the action"
  data: Optional[FullActionDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully updated the action",
            "data": FULL_ACTION_MODEL_EXAMPLE
        }
    }


class DeleteAction(BaseModel):
  """Delete Action Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the action"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the action"
        }
    }


class AllActionResponseModel(BaseModel):
  """Action Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Data fetched successfully"
  data: Optional[List[FullActionDataModel]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Data fetched successfully",
            "data": [FULL_ACTION_MODEL_EXAMPLE]
        }
    }


class ActionImportJsonResponse(BaseModel):
  """Action Import Json Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the actions"
  data: Optional[List[str]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the actions",
            "data": [
                "44qxEpc35pVMb6AkZGbi", "00MPqUhCbyPe1BcevQDr",
                "lQRzcrRuDpJ9IoW8bCHu"
            ]
        }
    }
