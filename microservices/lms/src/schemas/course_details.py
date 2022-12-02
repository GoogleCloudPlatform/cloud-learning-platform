"""
Pydantic Model for copy course API's
"""
from pydantic import BaseModel


class CourseDetails(BaseModel):
  """Course Detail model"""
  course_id: str
