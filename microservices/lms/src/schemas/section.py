"""
Pydantic Model for copy course API's
"""
from typing import Optional
from pydantic import BaseModel

class SectionDetails(BaseModel):
    """Course Detail model"""
    name:str
    description:str
    course_template:str
    cohort:str
    teachers_list:list

class SectionResponseModel(BaseModel):
  """Delete Course Template Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the course template"
  data: Optional[str] = None

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the course template",
            "data": None
        }
    }
