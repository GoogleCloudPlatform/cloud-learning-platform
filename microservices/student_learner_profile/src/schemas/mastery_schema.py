"""
Pydantic Model for Mastery APIs
"""
from typing import List, Optional
from pydantic import BaseModel


class MasteryScores(BaseModel):
  """Mastery Scores Pydantic Model"""
  pass

  class Config():
    orm_mode = True
    schema_extra = {"example": []}


class MasteryScoresResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the mastery scores"
  data: Optional[List[MasteryScores]]

  class Config():
    orm_mode = True
    schema_extra = {"example": []}
