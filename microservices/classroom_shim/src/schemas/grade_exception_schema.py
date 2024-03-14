"""
Pydantic Model for LTI Assignment API's
"""
from typing import Optional
from pydantic import BaseModel


class GradeExceptionInputModel(BaseModel):
  """Pydantic Model

  Args:
      BaseModel (_type_): _description_
  """
  email_id: str
  user_id: str
  tool_id: str
  allow_exception: Optional[bool] = True

  class Config():
    "Pydantic Config Class"
    orm_mode = True
    schema_extra = {
        "example": {
            "email_id": "Kv57BaY2uqE23N",
            "user_id": "N49q6vGt29oBvn8gt",
            "tool_id": "Z3bV9qJ7p41uCX",
            "allow_exception": True
        }
    }
