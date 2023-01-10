"""
Pydantic Model for copy course API's
"""
from pydantic import BaseModel
from typing import Literal, Optional


class CourseDetails(BaseModel):
  """Course Detail model"""
  course_id: str


class RegistrationDetails(BaseModel):
  """Registration API Details Model"""
  feed_type: Literal["COURSE_WORK_CHANGES", "COURSE_ROSTER_CHANGES"]
  course_id: str


class RegistrationResponse(BaseModel):
  """Registration API Response Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully registered the course"
  data: Optional[dict] = None

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully registered the course",
            "data": None
        }
    }
