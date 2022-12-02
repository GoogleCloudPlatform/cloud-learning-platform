"""
Pydantic Model for copy course API's
"""
from typing import Optional
from pydantic import BaseModel


class CourseDetails(BaseModel):
  """Course Detail model"""
  course_id: str
