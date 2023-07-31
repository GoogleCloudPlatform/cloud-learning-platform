"""
Pydantic Model for Goal API's
"""
from typing import List, Optional
from pydantic import BaseModel
from schemas.schema_examples import (BASIC_GOAL_EXAMPLE, FULL_GOAL_EXAMPLE,
                                     UPDATE_GOAL_EXAMPLE)


class BasicGoalModel(BaseModel):
  """Goal Skeleton Pydantic Model"""
  name: str
  description: Optional[str] = ""
  type: str = ""
  aligned_skills: Optional[list] = []
  aligned_workforces: Optional[list] = []
  aligned_credentials: Optional[list] = []
  aligned_learning_experiences: Optional[list] = []


class FullGoalDataModel(BasicGoalModel):
  """Goal Skeleton Model with uuid, created and updated time"""
  uuid: str
  is_archived: bool
  created_time: str
  last_modified_time: str


class GoalModel(BasicGoalModel):
  """Goal Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_GOAL_EXAMPLE}


class UpdateGoalModel(BaseModel):
  """Update Goal Pydantic Model"""
  name: Optional[str]
  description: Optional[str]
  type: Optional[str]
  aligned_skills: Optional[list]
  aligned_workforces: Optional[list]
  aligned_credentials: Optional[list]
  aligned_learning_experiences: Optional[list]
  is_archived: Optional[bool]

  class Config():
    orm_mode = True
    extra = "forbid"
    schema_extra = {"example": UPDATE_GOAL_EXAMPLE}


class TotalCountResponseModel(BaseModel):
  records: Optional[List[FullGoalDataModel]]
  total_count: int


class GetAllGoalsResponseModel(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the goal"
  data: Optional[TotalCountResponseModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the goal",
            "data": {
                      "records":[FULL_GOAL_EXAMPLE],
                      "total_count": 50
                    }
        }
    }


class GetGoalResponseModel(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the goal"
  data: Optional[FullGoalDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the goal",
            "data": FULL_GOAL_EXAMPLE
        }
    }


class PostGoalResponseModel(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the goal"
  data: Optional[FullGoalDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the goal",
            "data": FULL_GOAL_EXAMPLE
        }
    }


class UpdateGoalResponseModel(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the goal"
  data: Optional[FullGoalDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully updated the goal",
            "data": FULL_GOAL_EXAMPLE
        }
    }


class DeleteGoal(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the goal"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the goal"
        }
    }


class GoalSearchResponseModel(BaseModel):
  """Goal Search Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the goals"
  data: Optional[List[FullGoalDataModel]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the goals",
            "data": [FULL_GOAL_EXAMPLE]
        }
    }


class GoalImportJsonResponse(BaseModel):
  """Goal Import Json Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the goals"
  data: Optional[List[str]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success":
                True,
            "message":
                "Successfully created the goals",
            "data": [
                "44qxEpc35pVMb6AkZGbi", "00MPqUhCbyPe1BcevQDr",
                "lQRzcrRuDpJ9IoW8bCHu"
            ]
        }
    }
