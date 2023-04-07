"""
Pydantic Model for Admin Results API's
"""
from pydantic import BaseModel
from typing import List, Optional
from schemas.schema_examples import (BASIC_RESULT_EXAMPLE,
                                     FULL_RESULT_WITH_TIMESTAMPS_EXAMPLE)
# pylint: disable = invalid-name


class BasicResultModel(BaseModel):
  """Basic Result Pydantic Model"""
  userId: str
  resultScore: Optional[float]
  resultMaximum: Optional[float]
  comment: Optional[str]
  scoreOf: str
  lineItemId: str
  isGradeSyncCompleted: bool = False

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_RESULT_EXAMPLE}


class FullResultModel(BaseModel):
  """Full Result Pydantic Model"""
  id: str
  userId: str
  resultScore: Optional[float]
  resultMaximum: Optional[float]
  comment: Optional[str]
  scoreOf: str
  lineItemId: str
  isGradeSyncCompleted: Optional[bool]
  created_time: str
  last_modified_time: str


class GetAllResultsResponseModel(BaseModel):
  """Get all results pydantic model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched results"
  data: List[FullResultModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched results",
            "data": [FULL_RESULT_WITH_TIMESTAMPS_EXAMPLE]
        }
    }


class ResultResponseModel(BaseModel):
  """Result Response Pydantic model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched results"
  data: FullResultModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched results",
            "data": FULL_RESULT_WITH_TIMESTAMPS_EXAMPLE
        }
    }


class UpdateResultModel(BaseModel):
  """Update Result Request Model"""
  isGradeSyncCompleted: bool

  class Config():
    orm_mode = True
    schema_extra = {"example": {"isGradeSyncCompleted": False}}
    extra = "forbid"
