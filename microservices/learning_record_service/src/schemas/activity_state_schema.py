"""
Pydantic Models for ActivityState API's
"""
from typing import Optional, List
from pydantic import BaseModel
from schemas.schema_examples import (BASIC_ACTIVITY_STATE_MODEL_EXAMPLE,
                                     FULL_ACTIVITY_STATE_MODEL_EXAMPLE)
from common.utils.schema_validator import BaseConfigModel

class BasicActivityStateModel(BaseConfigModel):
  """ActivityState Skeleton Pydantic Model"""
  agent_id: str
  activity_id: str
  canonical_data: Optional[dict]


class FullActivityStateDataModel(BasicActivityStateModel):
  """ActivityState Skeleton Model with uuid, created and updated time"""
  uuid: str
  created_time: str
  last_modified_time: str


class ActivityStateModel(BasicActivityStateModel):
  """ActivityState Input Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_ACTIVITY_STATE_MODEL_EXAMPLE}


class UpdateActivityStateModel(BasicActivityStateModel):
  """Update ActivityState Pydantic Model"""
  agent_id: Optional[str]
  activity_id: Optional[str]

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_ACTIVITY_STATE_MODEL_EXAMPLE}


class GetActivityStateResponseModel(BaseModel):
  """Skill Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the activity state"
  data: Optional[FullActivityStateDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the activity state",
            "data": FULL_ACTIVITY_STATE_MODEL_EXAMPLE
        }
    }


class PostActivityStateResponseModel(BaseModel):
  """ActivityState Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the activity state"
  data: Optional[FullActivityStateDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the activity state",
            "data": FULL_ACTIVITY_STATE_MODEL_EXAMPLE
        }
    }


class UpdateActivityStateResponseModel(BaseModel):
  """ActivityState Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the activity state"
  data: Optional[FullActivityStateDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully updated the activity state",
            "data": FULL_ACTIVITY_STATE_MODEL_EXAMPLE
        }
    }


class DeleteActivityState(BaseModel):
  """Delete ActivityState Pydantic Model"""
  success: bool = True
  message: str = "Successfully deleted the activity state"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the activity state"
        }
    }

class TotalCountResponseModel(BaseModel):
  records: Optional[List[FullActivityStateDataModel]]
  total_count: int

class AllActivityStateResponseModel(BaseModel):
  """ActivityState Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Data fetched successfully"
  data: TotalCountResponseModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Data fetched successfully",
            "data": {
                      "records":[FULL_ACTIVITY_STATE_MODEL_EXAMPLE],
                      "total_count": 50
                    }
        }
    }


class ActivityStateImportJsonResponse(BaseModel):
  """ActivityState Import Json Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the activity states"
  data: Optional[List[str]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success":
                True,
            "message":
                "Successfully created the activity states",
            "data": [
                "44qxEpc35pVMb6AkZGbi", "00MPqUhCbyPe1BcevQDr",
                "lQRzcrRuDpJ9IoW8bCHu"
            ]
        }
    }
