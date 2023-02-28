"""
Pydantic Model for Grade API's
"""
from typing import Optional
from pydantic import BaseModel
from schemas.schema_examples import LTI_POST_GRADE_MODEL


class PostGradeModel(BaseModel):
  """Post Grade Pydantic Model

  Args:
      BaseModel (_type_): _description_
  """
  user_id: str
  comment: str
  lti_content_item_id: str
  maximum_grade: Optional[float] = None
  assigned_grade: Optional[float] = None
  draft_grade: Optional[float] = None

  class Config():
    "Pydantic Config Class"
    orm_mode = True
    schema_extra = {"example": LTI_POST_GRADE_MODEL}


class PostGradeResponseModel(BaseModel):
  """Post Grade List Response model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the user grade in classroom"
  data: Optional[str] = None

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully updated the user grade in classroom",
            "data": None
        }
    }
