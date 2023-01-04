"""
Pydantic Model for Line item API's
"""
from pydantic import BaseModel
from typing import Optional
from schemas.schema_examples import (BASIC_LINE_ITEM_EXAMPLE,
                                     UPDATE_LINE_ITEM_EXAMPLE,
                                     FULL_LINE_ITEM_EXAMPLE,
                                     BASIC_SCORE_EXAMPLE, FULL_SCORE_EXAMPLE,
                                     BASIC_RESULT_EXAMPLE, FULL_RESULT_EXAMPLE)


# pylint: disable = invalid-name
class BasicScoreModel(BaseModel):
  """Basic Score Pydantic Model"""
  userId: str
  activityProgress: str
  gradingProgress: str
  timestamp: str
  scoreGiven: Optional[int]
  scoreMaximum: Optional[int]
  comment: Optional[str]

  class Config():
    orm_mode = True
    schem_extra = {"example": BASIC_SCORE_EXAMPLE}


class ScoreResponseModel(BaseModel):
  """Score Response Model"""
  uuid: str
  userId: str
  scoreGiven: int
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

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_RESULT_EXAMPLE}


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
  scoreMaximum: int
  label: str
  resourceId: Optional[str]
  tag: Optional[str]
  resourceLinkId: Optional[str]
  startDateTime: Optional[str]
  endDateTime: Optional[str]


class FullLineItemModel(BasicLineItemModel):
  """Full Line Item Model"""
  id: str
  uuid: str

  class Config():
    orm_mode = True
    schema_extra = {"example": FULL_LINE_ITEM_EXAMPLE}


class LineItemModel(BasicLineItemModel):
  """Line Item Input Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_LINE_ITEM_EXAMPLE}


class UpdateLineItemModel(BaseModel):
  """Update Line Item Pydantic Model"""
  scoreMaximum: int
  label: str
  startDateTime: str
  endDateTime: str

  class Config():
    orm_mode = True
    schema_extra = {"example": UPDATE_LINE_ITEM_EXAMPLE}


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
