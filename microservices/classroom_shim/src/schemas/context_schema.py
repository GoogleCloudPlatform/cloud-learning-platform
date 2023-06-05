"""
Pydantic Model for Context API's
"""
from typing import Optional, List
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


class ContextMembersModel(BaseModel):
  """Context Members Pydantic Model

  Args:
      BaseModel (_type_): _description_
  """
  user_id: str
  email: str
  user_type: str
  first_name: Optional[str]
  last_name: Optional[str]
  photo_url: Optional[str]
  status: Optional[str]
  enrollment_status: Optional[str]

  class Config():
    orm_mode = True
    schema_extra = {"example": CONTEXT_EXAMPLE}


class ContextMembersResponseModel(BaseModel):
  """Context Response model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the context details"
  data: Optional[List[ContextMembersModel]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the context details",
            "data": CONTEXT_EXAMPLE
        }
    }
