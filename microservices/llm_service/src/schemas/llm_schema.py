"""
Pydantic Model for Grade API's
"""
from typing import Optional
from pydantic import BaseModel
from schemas.schema_examples import LLM_MODEL


class LLMModel(BaseModel):
  """LLM Pydantic Model

  Args:
      BaseModel (_type_): _description_
  """
  user_id: str
  lti_content_item_id: str
  comment: Optional[str]
  maximum_grade: Optional[float] = None
  assigned_grade: Optional[float] = None
  draft_grade: Optional[float] = None
  validate_title: Optional[bool] = False
  line_item_title: Optional[str] = None

  class Config():
    "Pydantic Config Class"
    orm_mode = True
    schema_extra = {"example": LLM_MODEL}


class LLMGenerateResponse(BaseModel):
  """LLM Generate Response model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully generated text"
  data: Optional[str] = None

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully generated text",
            "data": None
        }
    }
