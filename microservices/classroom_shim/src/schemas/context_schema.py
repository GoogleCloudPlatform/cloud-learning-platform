"""
Pydantic Model for Context API's
"""
from typing import Optional
from pydantic import BaseModel
from schemas.schema_examples import CONTEXT_EXAMPLE


class ContextModel(BaseModel):
  """Context Pydantic Model

  Args:
      BaseModel (_type_): _description_
  """
  id: str
  name: Optional[str]
  description: Optional[str]

  class Config():
    orm_mode = True
    schema_extra = {"example": CONTEXT_EXAMPLE}


class ContextResponseModel(BaseModel):
  """Context Response model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the context details"
  data: Optional[ContextModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the context details",
            "data": CONTEXT_EXAMPLE
        }
    }
