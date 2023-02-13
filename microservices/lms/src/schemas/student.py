"""
Pydantic Model for copy course API's
"""
from typing import Optional
from pydantic import BaseModel

class AddStudentResponseModel(BaseModel):
  """Add Student Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully Added the Student"
  data: Optional[str] = None

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully Added the Student",
            "data": {"course_enrollment_id":"2xBnBjqm2X3eRgVxE6Bv",
            "user_id":"2xBnBjqm2X3eRgVxE6Bv"}
        }
    }

class AddStudentToSectionModel(BaseModel):
  """Input Model to add student in section"""
  email: str
  access_token:str
  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "email": "email@gmail.com",
            "access_token":"test_token"
        }
    }

