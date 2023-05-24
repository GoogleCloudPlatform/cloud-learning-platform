"""
Pydantic Models for Inspace Token API's
"""
from pydantic import BaseModel
from schemas.schema_examples import INSPACE_TOKEN_EXAMPLE

class TokenResponseModel(BaseModel):
  """Response token Skeleton Pydantic Model"""
  token: dict

class InspaceTokenModel(BaseModel):
  """token Skeleton Pydantic Model"""
  success: bool = True
  message: str = "Successfully fetched the inspace token"
  data: dict

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully fetched the inspace token",
        "data": INSPACE_TOKEN_EXAMPLE
      }
    }
