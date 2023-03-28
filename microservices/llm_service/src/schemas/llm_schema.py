"""
Pydantic Model for Grade API's
"""
from typing import Optional
from pydantic import BaseModel
from schemas.schema_examples import LLM_MODEL_EXAMPLE


class LLMModel(BaseModel):
  """LLM model"""
  userid: str
  llm_type: str
  context: Optional[str] = ""
  primer: Optional[list[str]] = ""
  history: Optional[list[str]] = []
  memory: Optional[str] = ""

  class Config():
    orm_mode = True
    schema_extra = {
        "example": LLM_MODEL_EXAMPLE
    }

class LLMGenerateResponse(BaseModel):
  """LLM Generate Response model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully generated text"
  data: Optional[str] = ""

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully generated text",
            "data": None
        }
    }
