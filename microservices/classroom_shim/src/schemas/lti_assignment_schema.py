"""
Pydantic Model for LTI Assignment API's
"""
import datetime
from typing import Optional, List
from typing_extensions import Literal
from pydantic import BaseModel
from schemas.schema_examples import (LTI_ASSIGNMENT_EXAMPLE,
                                     INSERT_LTI_ASSIGNMENT_EXAMPLE,
                                     UPDATE_LTI_ASSIGNMENT_EXAMPLE)


class LTIAssignmentModel(BaseModel):
  """LTI Assignment Pydantic Model

  Args:
      BaseModel (_type_): _description_
  """
  id: str
  context_id: str
  context_type: Literal["section", "course_template"] = "section"
  lti_assignment_title: Optional[str]
  lti_content_item_id: Optional[str]
  tool_id: Optional[str]
  course_work_id: Optional[str]
  max_points: Optional[float]
  start_date: Optional[datetime.datetime]
  end_date: Optional[datetime.datetime]
  due_date: Optional[datetime.datetime]

  class Config():
    "Pydantic Config Class"
    orm_mode = True
    schema_extra = {"example": LTI_ASSIGNMENT_EXAMPLE}


class UpdateLTIAssignmentModel(BaseModel):
  """Update LTI Assignment Pydantic Model

  Args:
      BaseModel (_type_): _description_
  """
  context_id: Optional[str]
  context_type: Literal["section", "course_template"] = "section"
  lti_assignment_title: Optional[str]
  lti_content_item_id: Optional[str]
  tool_id: Optional[str]
  course_work_id: Optional[str]
  max_points: Optional[float]
  start_date: Optional[datetime.datetime]
  end_date: Optional[datetime.datetime]
  due_date: Optional[datetime.datetime]

  class Config():
    orm_mode = True
    schema_extra = {"example": UPDATE_LTI_ASSIGNMENT_EXAMPLE}


class LTIAssignmentListResponseModel(BaseModel):
  """LTI Assignment List Response model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the LTI Assignment list"
  data: Optional[List[LTIAssignmentModel]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the LTI Assignment list",
            "data": [LTI_ASSIGNMENT_EXAMPLE]
        }
    }


class GetLTIAssignmentResponseModel(BaseModel):
  """Get LTI Assignment Response model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the LTI Assignment"
  data: Optional[LTIAssignmentModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the LTI Assignment",
            "data": LTI_ASSIGNMENT_EXAMPLE
        }
    }


class CreateLTIAssignmentResponseModel(BaseModel):
  """Create LTI Assignment Response Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the LTI Assignment"
  data: Optional[LTIAssignmentModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the LTI Assignment",
            "data": LTI_ASSIGNMENT_EXAMPLE
        }
    }


class InputLTIAssignmentModel(BaseModel):
  """Pydantic Input LTI Assignment Model

  Args:
      BaseModel (_type_): _description_
  """
  context_id: str
  context_type: Literal["section", "course_template"]
  lti_content_item_id: Optional[str]
  lti_assignment_title: Optional[str]
  tool_id: Optional[str]
  course_work_id: Optional[str]
  max_points: Optional[float]
  start_date: Optional[datetime.datetime]
  end_date: Optional[datetime.datetime]
  due_date: Optional[datetime.datetime]

  class Config():
    orm_mode = True
    schema_extra = {"example": INSERT_LTI_ASSIGNMENT_EXAMPLE}


class UpdateLTIAssignmentResponseModel(BaseModel):
  """Update LTI Assignment response Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the LTI Assignment"
  data: Optional[LTIAssignmentModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully updated the LTI Assignment",
            "data": LTI_ASSIGNMENT_EXAMPLE
        }
    }


class DeleteLTIAssignmentResponseModel(BaseModel):
  """Delete LTI Assignment Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the LTI Assignment"
  data: Optional[str] = None

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the LTI Assignment",
            "data": None
        }
    }


class InputCopyLTIAssignmentModel(BaseModel):
  """Pydantic Input LTI Assignment Model

  Args:
      BaseModel (_type_): _description_
  """
  lti_assignment_id: str
  context_id: str

  class Config():
    orm_mode = True
