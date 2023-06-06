"""
Pydantic Model for RubricCriterion API's
"""
from typing import List, Optional
from pydantic import BaseModel
from schemas.schema_examples import (BASIC_RUBRIC_CRITERION_EXAMPLE,
                                     FULL_RUBRIC_CRITERION_EXAMPLE,
                                     UPDATE_RUBRIC_CRITERION_EXAMPLE)
# pylint: disable=line-too-long


class ParentNodes(BaseModel):
  rubrics: Optional[list] = []


class BasicRubricCriterionModel(BaseModel):
  """RubricCriterion Skeleton Pydantic Model"""
  name: str
  description: str
  author: Optional[str] = ""
  parent_nodes: Optional[ParentNodes] = {}
  performance_indicators: Optional[list] = []


class FullRubricCriterionDataModel(BasicRubricCriterionModel):
  """RubricCriterion Skeleton Model with uuid, created and updated time"""
  uuid: str
  created_time: str
  last_modified_time: str


class RubricCriterionModel(BasicRubricCriterionModel):
  """RubricCriterion Input Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_RUBRIC_CRITERION_EXAMPLE}


class UpdateRubricCriterionModel(BasicRubricCriterionModel):
  """Update RubricCriterion Pydantic Model"""
  uuid: str

  class Config():
    orm_mode = True
    schema_extra = {"example": UPDATE_RUBRIC_CRITERION_EXAMPLE}


class RubricCriterionModelResponse(BaseModel):
  """RubricCriterion Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the rubric criterion"
  data: Optional[FullRubricCriterionDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the rubric criterion",
            "data": FULL_RUBRIC_CRITERION_EXAMPLE
        }
    }


class DeleteRubricCriterion(BaseModel):
  """Delete RubricCriterion Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the rubric criterion"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the rubric criterion"
        }
    }


class RubricCriterionSearchModelResponse(BaseModel):
  """RubricCriterion Search Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the rubric criterions"
  data: Optional[List[FullRubricCriterionDataModel]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the rubric criterions",
            "data": [FULL_RUBRIC_CRITERION_EXAMPLE]
        }
    }

class TotalCountResponseModel(BaseModel):
  records: Optional[List[FullRubricCriterionDataModel]]
  total_count: int

class AllRubricCriterionsModelResponse(BaseModel):
  """Rubric Criterion Response Pydantic Model"""
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
                      "records":[FULL_RUBRIC_CRITERION_EXAMPLE],
                      "total_count": 50
                  }
        }
    }
