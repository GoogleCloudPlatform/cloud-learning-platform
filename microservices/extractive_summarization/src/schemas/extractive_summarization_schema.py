"""Pydantic models for Extractive Summarization APIs"""
from pydantic import BaseModel, Field
from typing import Optional

class RequestModel(BaseModel):
  """Extractive Summarization request pydantic model"""
  data: str = Field(min_length=1)
  ratio: Optional[int] = 0.2
  min_length: Optional[int] = 25
  max_length: Optional[int] = 500


  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "data": "Social science is any branch of academic study or science "
        "that deals with human behaviour in its social and cultural aspects.",
        "ratio": 0.3
      }
    }


class ResponseModel(BaseModel):
  """Extractive Summarization response pydantic model"""
  success: bool
  message: str
  data: Optional[dict]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
    "success": True,
    "message": "All good",
    "data": {
      "summary": "Social science is any branch of academic study or science "
      "that deals with human behaviour in its social and cultural aspects."
    }
      }
    }
