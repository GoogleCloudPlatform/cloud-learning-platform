"""
Pydantic Model for Line item API's
"""
from pydantic import BaseModel
from typing import List, Optional
from schemas.schema_examples import (BASIC_LINE_ITEM_EXAMPLE,
                                     FULL_LINE_ITEM_EXAMPLE, FULL_SCORE_EXAMPLE,
                                     FULL_RESULT_EXAMPLE)


# pylint: disable = invalid-name
class BasicScoreModel(BaseModel):
  """Basic Score Pydantic Model"""
  userId: str
  scoreGiven: str
  scoreMaximum: int
  comment: str
  timestamp: str
  activityProgress: str
  gradingProgress: str


class ScoreResponseModel(BaseModel):
  """Score Response Model"""
  uuid: str
  userId: str
  scoreGiven: str
  scoreMaximum: int
  comment: str
  timestamp: str
  activityProgress: str
  gradingProgress: str

  class Config():
    orm_mode = True
    schema_extra = {"example": FULL_SCORE_EXAMPLE}


class BasicResultModel(BaseModel):
  """Basic Result Pydantic Model"""
  userId: str
  resultScore: str
  resultMaximum: str
  comment: str
  scoreOf: str


class ResultResponseModel(BaseModel):
  """Result Response Model"""
  uuid: str
  userId: str
  resultScore: str
  resultMaximum: str
  comment: str
  scoreOf: str

  class Config():
    orm_mode = True
    schema_extra = {"example": FULL_RESULT_EXAMPLE}


class BasicLineItemModel(BaseModel):
  """Basic Line Item Pydantic Model"""
  startDateTime: str
  endDateTime: str
  scoreMaximum: int
  label: str
  tag: str
  resourceId: str
  resourceLinkId: str


class FullLineItemModel(BasicLineItemModel):
  """Full Line Item Model"""
  uuid: str


class LineItemModel(BasicLineItemModel):
  """Line Item Input Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_LINE_ITEM_EXAMPLE}


class UpdateLineItemModel(BaseModel):
  """Update Line Item Pydantic Model"""
  startDateTime: str
  endDateTime: str
  scoreMaximum: int
  label: str
  tag: str
  resourceId: str
  resourceLinkId: str

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_LINE_ITEM_EXAMPLE}


class LineItemResponseModel(FullLineItemModel):
  """Line Item Response Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": FULL_LINE_ITEM_EXAMPLE}


class DeleteLineItem(BaseModel):
  """Delete Line Item Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the Line item"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the Line item"
        }
    }


class AllLineItemsResponseModel(BaseModel):
  """Line Item Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Data fetched successfully"
  data: List[FullLineItemModel]

  class Config():
    orm_mode = True
    schema_extra = {"example": [FULL_LINE_ITEM_EXAMPLE]}
