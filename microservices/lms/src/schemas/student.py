"""
Pydantic Model for copy course API's
"""
from typing import Optional
from pydantic import BaseModel, constr
from schemas.schema_examples import TEMP_USER,GET_STUDENT_EXAMPLE

class AddStudentResponseModel(BaseModel):
  """Add Student Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully Added the Student"
  data: Optional[dict] = None
  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully Added the Student",
            "data": {"course_enrollment_id":"2xBnBjqm2X3eRgVxE6Bv",
            "student_email":"test_user@gmail",
            "section_id":"fake-section-id",
            "cohort_id":"fake-cohort-id",
            "classroom_id":"123453333",
            "classroom_url":"https://classroom.google.com/c/NTYzMhjhjrx"}
        }
    }

class AddStudentToCohortModel(BaseModel):
  """Input Model to add student in section"""
  email: constr(min_length=7, max_length=128,
                regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
                to_lower=True)
  access_token:str
  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "email": "email@gmail.com",
            "access_token":"test_token"
        }
    }

class GetStudentDetailsResponseModel(BaseModel):
  """Get Student Details Model"""
  success: Optional[bool] = True
  data: Optional[dict] = None
  class Config():
    orm_mode = True
    schema_extra = {
        "example":GET_STUDENT_EXAMPLE
    }

class GetProgressPercentageResponseModel(BaseModel):
  """Get Progress Percentage"""
  success: Optional[bool] = True
  data: int = None
class GetProgressPercentageCohortResponseModel(BaseModel):
  """Get Progress Percentage"""
  success: Optional[bool] = True
  data: list = None
  