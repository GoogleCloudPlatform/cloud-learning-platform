"""Schema for ability tree"""

from pydantic import BaseModel
from enum import Enum


# pylint: disable=invalid-name
class LevelEnum(str, Enum):
  course = "course"
  competency = "competency"
  sub_competenccy = "sub_competency"
  learning_objective = "learning_objective"
  learning_unit = "learning_unit"

class AbilityRequest(BaseModel):
  user_id: str
  level: LevelEnum
  doc_id: str

  class Config:
    orm_mode = True
    schema_extra = {
        "example": {
            "user_id": "kfda435jkdsfka",
            "level": "learning_objective",
            "doc_id": "asdf3dsfaafd4trq"
        }
    }
