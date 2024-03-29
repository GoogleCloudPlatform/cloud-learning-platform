"""
Pydantic Model for copy course API's
"""
from pydantic import BaseModel
from schemas.schema_examples import UPDATE_SECTION


class UpdateSection(BaseModel):
  """Course Detail model"""
  id: str
  course_id: str
  section_name: str
  description: str
  max_students : int

  class Config():
    orm_mode = True
    schema_extra = {"example": UPDATE_SECTION}
