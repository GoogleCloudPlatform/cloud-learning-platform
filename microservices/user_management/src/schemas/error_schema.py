"""
Pydantic models for different status codes
"""
from typing import Optional
from pydantic import BaseModel


class NotFoundErrorResponseModel(BaseModel):
  success: bool = False
  message: Optional[str] = None
  data: Optional[dict] = {}

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": False,
            "message": "Resource with uuid o1nv13n6sbu0ny not found",
            "data": {}
        }
    }


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


class ConflictResponseModel(BaseModel):
  success: bool = False
  message: Optional[str] = "Conflict"
  data: Optional[dict] = {}

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": False,
            "message": "Conflict",
            "data": {}
        }
    }


class UnauthorizedResponseModel(BaseModel):
  success: bool = False
  message: Optional[str] = "Unauthorized"
  data: Optional[dict] = {}

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": False,
            "message": "Unauthorized",
            "data": {}
        }
    }


class PayloadTooLargeResponseModel(BaseModel):
  success: bool = False
  message: Optional[str] = ""
  data: Optional[dict] = {}

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": False,
            "message": "Content too large",
            "data": {}
        }
    }
