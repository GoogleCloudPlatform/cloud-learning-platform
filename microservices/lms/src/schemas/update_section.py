"""
Pydantic Model for copy course API's
"""
from pydantic import BaseModel


class UpdateSection(BaseModel):
  """Course Detail model"""
  id: str
  course_id: str
  section_name: str
  description: str
  course_state: str
