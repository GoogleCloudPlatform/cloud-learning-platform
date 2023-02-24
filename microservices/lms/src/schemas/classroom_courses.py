"""
Pydantic Model for copy course API's
"""
from pydantic import BaseModel
from typing import  Optional


class CourseDetails(BaseModel):
  """Course Detail model"""
  course_id: str

class EnableNotificationsResponse(BaseModel):
  """Enable Notifications API Response Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully registered the course"
  data: Optional[list[dict]] = None

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully registered the course",
            "data": []
        }
    }

class CopyCourseResponse(BaseModel):
  """Copy Course Response Model"""
  success: Optional[bool] = True
  message: Optional[str]="Successfully Copied the course"
  data: Optional[dict]=None

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully Copied the course",
            "data": {}
        }
    }


class ClassroomCourseListResponseModel(BaseModel):
  """Get a list of Classroom Courses"""
  success: Optional[bool] = True
  message: Optional[str] = "Success list"
  data: Optional[list] = []

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Success",
            "data": []
        }
    }
