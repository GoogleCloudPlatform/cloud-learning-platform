"""
Pydantic Model for Admin Results API's
"""
from pydantic import BaseModel
from typing import Optional
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


class ResultResponseModel(BaseModel):
  """Result Response Model"""
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

  class Config():
    orm_mode = True
    schema_extra = {"example": FULL_RESULT_WITH_TIMESTAMPS_EXAMPLE}


class UpdateResultModel(BaseModel):
  """Result Response Model"""
  isGradeSyncCompleted: bool

  class Config():
    orm_mode = True
    schema_extra = {"example": {"isGradeSyncCompleted": False}}
    extra = "forbid"
