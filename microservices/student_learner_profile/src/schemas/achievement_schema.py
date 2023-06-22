"""
Pydantic Model for Achievement API's
"""
# pylint: disable=invalid-name

from pydantic import BaseModel
from typing import List, Optional
from typing_extensions import Literal

from schemas.schema_examples import (
  FULL_ACHIEVEMENT_EXAMPLE,
  UPDATE_ACHIEVEMENT_EXAMPLE,
  POST_ACHIEVEMENT_EXAMPLE,
  LEARNER_ACHIEVEMENTS
)

ALLOWED_ACHIEVEMENT_TYPES = Literal["course equate", "competency", "level"]


class Alignments(BaseModel):
  """
  Alignments Pydantic Model
  """
  competency_alignments: Optional[list] = []
  skill_alignments: Optional[list] = []


class UpdateAlignments(BaseModel):
  """
  Update Alignments Pydantic Model
  """
  competency_alignments: Optional[list]
  skill_alignments: Optional[list]

class DesignConfig(BaseModel):
  """
  DesignConfig Pydantic Model
  """
  theme: Optional[str] = ""
  illustration: Optional[str] = ""
  shape: Optional[str] = ""

class MetaData(BaseModel):
  """
  Metadata Pydantic Model
  """
  design_config: Optional[DesignConfig] = {}


class UpdateAssociations(BaseModel):
  """
  Update Associations Pydantic Model
  """
  exact_match_of: Optional[list]
  exemplar: Optional[list]
  has_skill_level: Optional[list]
  is_child_of: Optional[list]
  is_parent_of: Optional[list]
  is_part_of: Optional[list]
  is_peer_of: Optional[list]
  is_related_to: Optional[list]
  precedes: Optional[list]
  replaced_by: Optional[list]


class Associations(BaseModel):
  """
  Associations Pydantic Model
  """
  exact_match_of: Optional[list] = []
  exemplar: Optional[list] = []
  has_skill_level: Optional[list] = []
  is_child_of: Optional[list] = []
  is_parent_of: Optional[list] = []
  is_part_of: Optional[list] = []
  is_peer_of: Optional[list] = []
  is_related_to: Optional[list] = []
  precedes: Optional[list] = []
  replaced_by: Optional[list] = []


class BasicAchievementModel(BaseModel):
  """
  Achievement Skeleton Pydantic Model
  """
  type: ALLOWED_ACHIEVEMENT_TYPES
  name: str
  description: Optional[str]
  alignments: Optional[Alignments] = {}
  associations: Optional[Associations] = {}
  credits_available: Optional[float]
  field_of_study: Optional[str]
  metadata: Optional[MetaData] = {}
  image: Optional[str]
  result_descriptions: Optional[List[str]]
  tags: Optional[List[str]]
  timestamp: Optional[str]


class FullAchievementDataModel(BasicAchievementModel):
  """
  Achievement Skeleton Model with uuid, created and updated time
  """
  uuid: str
  is_archived: bool
  created_time: str
  last_modified_time: str


class AllAchievementsResponseModel(BaseModel):
  """
  All Achievements Response Pydantic Model
  """
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the achievements"
  data: Optional[List[FullAchievementDataModel]]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully fetched the achievements",
        "data": [FULL_ACHIEVEMENT_EXAMPLE]
      }
    }


class PostAchievementModel(BaseModel):
  """
  Post Achievement Pydantic Model
  """
  type: ALLOWED_ACHIEVEMENT_TYPES
  name: str
  description: Optional[str]
  #   skill_ids: Optional[list]
  #   competency_ids: Optional[list]
  alignments: Optional[Alignments] = {}
  associations: Optional[Associations] = {}
  credits_available: Optional[float]
  field_of_study: Optional[str]
  metadata: Optional[dict] = {}
  image: Optional[str]
  result_descriptions: Optional[List[str]]
  tags: Optional[List[str]]
  timestamp: Optional[str]

  class Config():
    orm_mode = True
    schema_extra = {"example": POST_ACHIEVEMENT_EXAMPLE}


class UpdateAchievementModel(BaseModel):
  """
  Update Achievement Pydantic Model
  """
  type: Optional[str]
  name: Optional[str]
  description: Optional[str]
  alignments: Optional[UpdateAlignments]
  associations: Optional[UpdateAssociations]
  credits_available: Optional[float]
  field_of_study: Optional[str]
  metadata: Optional[dict] = {}
  image: Optional[str]
  result_descriptions: Optional[List[str]]
  tags: Optional[List[str]]
  timestamp: Optional[str]
  is_archived: Optional[bool]

  class Config():
    orm_mode = True
    extra = "forbid"
    schema_extra = {"example": UPDATE_ACHIEVEMENT_EXAMPLE}


class GetAchievementResponseModel(BaseModel):
  """
  Get Achievement Response Pydantic Model
  """
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the achievement"
  data: Optional[FullAchievementDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully fetched the achievement",
        "data": FULL_ACHIEVEMENT_EXAMPLE
      }
    }


class PostAchievementResponseModel(BaseModel):
  """
  Post Achievement Response Pydantic Model
  """
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the achievement"
  data: Optional[FullAchievementDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully created the achievement",
        "data": FULL_ACHIEVEMENT_EXAMPLE
      }
    }


class UpdateAchievementResponseModel(BaseModel):
  """
  Update Achievement Response Pydantic Model
  """
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the achievement"
  data: Optional[FullAchievementDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully updated the achievement",
        "data": FULL_ACHIEVEMENT_EXAMPLE
      }
    }


class DeleteAchievement(BaseModel):
  """
  Delete Achievement Pydantic Model
  """
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the achievement"

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully deleted the achievement"
      }
    }


class AchievementSearchResponseModel(BaseModel):
  """
  Achievement Search Response Pydantic Model
  """
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the achievements"
  data: Optional[List[FullAchievementDataModel]]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully fetched the achievements",
        "data": [FULL_ACHIEVEMENT_EXAMPLE]
      }
    }


class AchievementImportJsonResponse(BaseModel):
  """
  Achievement Import Json Response Pydantic Model
  """
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the achievements"
  data: Optional[List[str]]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully created the achievements",
        "data": [
          "44qxEpc35pVMb6AkZGbi", "00MPqUhCbyPe1BcevQDr",
          "lQRzcrRuDpJ9IoW8bCHu"
        ]
      }
    }

class LearnerAchievementModel(FullAchievementDataModel):
  """
  LearnerAchievement Pydantic Model
  """
  status: Optional[str]
  parent_node: Optional[dict] = {}
  child_achievements: Optional[List] = []

class LearnerAchievementResponseModel(BaseModel):
  """
  LearnerAchievement Response Pydantic Model
  """
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the learner achievements for"
  " the given pathway"
  data: Optional[List[LearnerAchievementModel]]
  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully fetched the learner "
                   "achievements for the given pathway",
        "data": LEARNER_ACHIEVEMENTS
      }
    }
