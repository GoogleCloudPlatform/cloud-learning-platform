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

class UnauthorizedUserErrorResponseModel(BaseModel):
  success: bool = False
  message: Optional[str] = "User is not authorized"
  data: Optional[dict] = {}

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": False,
            "message": "User is not authorized",
            "data": []
        }
    }

class ConnectionTimeoutErrorResponseModel(BaseModel):
  success: bool = False
  message: Optional[str] = "Request Timed-out"
  data: Optional[dict] = {}

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": False,
            "message": "Request Timed-out",
            "data": {}
        }
    }


class ConnectionErrorResponseModel(BaseModel):
  success: bool = False
  message: Optional[str] = "Connection Error"
  data: Optional[dict] = {}

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": False,
            "message": "Connection Error",
            "data": {}
        }
    }
