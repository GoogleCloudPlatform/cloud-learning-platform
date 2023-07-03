"""
Pydantic Model for Rubric API's
"""
from typing import List, Optional
from pydantic import BaseModel
from schemas.schema_examples import (BASIC_RUBRIC_EXAMPLE, FULL_RUBRIC_EXAMPLE,
                                     UPDATE_RUBRIC_EXAMPLE)
# pylint: disable=line-too-long


class ParentNodes(BaseModel):
  assessments: Optional[list] = []


class ChildNodes(BaseModel):
  rubric_criteria: Optional[list] = []


class BasicRubricModel(BaseModel):
  """Rubric Skeleton Pydantic Model"""
  name: Optional[str]
  description: Optional[str]
  author: Optional[str] = ""
  evaluation_criteria: Optional[dict] = {
    "0": "Exemplary",
    "1": "Proficient",
    "2": "Needs Improvement",
    "3": "Not Evident"
  }
  parent_nodes: Optional[ParentNodes] = {}
  child_nodes: Optional[ChildNodes] = {}


class FullRubricDataModel(BasicRubricModel):
  """Rubric Skeleton Model with uuid, created and updated time"""
  uuid: str
  created_time: str
  last_modified_time: str


class RubricModel(BasicRubricModel):
  """Rubric Input Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_RUBRIC_EXAMPLE}


class UpdateRubricModel(BasicRubricModel):
  """Update Rubric Pydantic Model"""
  uuid: str

  class Config():
    orm_mode = True
    schema_extra = {"example": UPDATE_RUBRIC_EXAMPLE}


class RubricModelResponse(BaseModel):
  """Rubric Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the rubric"
  data: Optional[FullRubricDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the rubric",
            "data": FULL_RUBRIC_EXAMPLE
        }
    }


class DeleteRubric(BaseModel):
  """Delete Rubric Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the rubric"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the rubric"
        }
    }


class RubricSearchModelResponse(BaseModel):
  """Rubric Search Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the rubrics"
  data: Optional[List[FullRubricDataModel]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the rubrics",
            "data": [FULL_RUBRIC_EXAMPLE]
        }
    }

class TotalCountResponseModel(BaseModel):
  records: Optional[List[FullRubricDataModel]]
  total_count: int

class AllRubricsModelResponse(BaseModel):
  """Rubric Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Data fetched successfully"
  data: Optional[TotalCountResponseModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Data fetched successfully",
            "data": {
                      "records":[FULL_RUBRIC_EXAMPLE],
                      "total_count": 50
                    }
        }
    }
