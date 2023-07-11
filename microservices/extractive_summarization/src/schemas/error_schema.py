"""
Pydantic models for different status codes
"""
from typing import Optional
from pydantic import BaseModel

class InternalServerErrorResponseModel(BaseModel):
  success: bool = False
  message: Optional[str] = "Internal Server Error"
  data: Optional[dict] = {}

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": False,
            "message": "Internal server error",
            "data": {}
        }
    }


class ValidationErrorResponseModel(BaseModel):
  success: bool = False
  message: Optional[str] = "Validation Failed"
  data: Optional[dict] = {}

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": False,
            "message": "Validation Failed",
            "data": []
        }
    }
