"""
Pydantic Model for copy course API's
"""
from pydantic import BaseModel, constr
from schemas.schema_examples import UPDATE_SECTION


class UpdateSection(BaseModel):
  """Course Detail model"""
  id: str
  course_id: str
  section_name: str
  description: str
  teachers: list[constr(min_length=7, max_length=128,
    regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    to_lower=True)]

  class Config():
    orm_mode = True
    schema_extra = {"example": UPDATE_SECTION}
