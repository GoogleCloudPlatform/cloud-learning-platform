"""
Pydantic Model for Activity API's
"""
from typing import List, Optional
from pydantic import BaseModel
from schemas.schema_examples import BASIC_ACTIVITY_EXAMPLE, FULL_ACTIVITY_EXAMPLE
from common.utils.schema_validator import BaseConfigModel


class BasicActivityModel(BaseConfigModel):
  """Activity Pydantic Model"""
  name: str
  authority: Optional[str] = None
  canonical_data: Optional[dict] = {}

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_ACTIVITY_EXAMPLE}

class UpdateActivityModel(BaseConfigModel):
  """Update Activity Pydantic Model"""
  canonical_data: Optional[dict]
  name: Optional[str]
  authority: Optional[str]

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_ACTIVITY_EXAMPLE}


class FullActivityDataModel(BasicActivityModel):
  """Activity Skeleton Model with uuid, created and updated time"""
  uuid: str
  created_time: str
  last_modified_time: str

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the activity",
            "data": FULL_ACTIVITY_EXAMPLE
        }
    }

class TotalCountResponseModel(BaseModel):
  records: Optional[List[FullActivityDataModel]]
  total_count: int

class AllActivitiesResponseModel(BaseModel):
  """Activity Response Pydantic Model"""
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
                      "records":[FULL_ACTIVITY_EXAMPLE],
                      "total_count": 50
                    }
        }
    }


class GetActivityResponseModel(BaseModel):
  """Activity Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the activity"
  data: Optional[FullActivityDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the activity",
            "data": FULL_ACTIVITY_EXAMPLE
        }
    }


class PostActivityResponseModel(BaseModel):
  """Activity Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the activity"
  data: Optional[FullActivityDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the activity",
            "data": FULL_ACTIVITY_EXAMPLE
        }
    }


class UpdateActivityResponseModel(BaseModel):
  """Activity Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the activity"
  data: Optional[FullActivityDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully updated the activity",
            "data": FULL_ACTIVITY_EXAMPLE
        }
    }


class DeleteActivity(BaseModel):
  """Delete Activity Pydantic Model"""
  success: bool = True
  message: str = "Successfully deleted the activity"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the activity"
        }
    }


class ActivityImportJsonResponse(BaseModel):
  """Activity Import Json Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the activities"
  data: Optional[List[str]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success":
                True,
            "message":
                "Successfully created the activities",
            "data": [
                "44qxEpc35pVMb6AkZGbi", "00MPqUhCbyPe1BcevQDr",
                "lQRzcrRuDpJ9IoW8bCHu"
            ]
        }
    }
