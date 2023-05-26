"""
Pydantic Model for Learning Experience API's
"""
from typing import List, Optional
from pydantic import BaseModel
from schemas.schema_examples import (BASIC_LEARNING_EXPERIENCE_EXAMPLE,
                                     FULL_LEARNING_EXPERIENCE_EXAMPLE)
from config import ALLOWED_THEMES, LE_TYPES, LE_ALIASES


class DesignConfig(BaseModel):
  """DesignConfig Pydantic Model"""
  theme: Optional[ALLOWED_THEMES] = ""
  illustration: Optional[str] = ""

class MetaData(BaseModel):
  """Metadata Pydantic Model"""
  design_config: Optional[DesignConfig] = {}

class LOSNodes(BaseModel):
  """Parent Nodes Pydantic Model"""
  curriculum_pathways: Optional[List[str]] = []
  learning_experiences: Optional[List[str]] = []
  learning_objects: Optional[List[str]] = []
  learning_resources: Optional[List[str]] = []
  assessments: Optional[List[str]] = []


class Reference(BaseModel):
  """Reference Pydantic Model"""
  competencies: Optional[list] = []
  skills: Optional[list] = []


class Alignment(BaseModel):
  """Alignment Pydantic Model"""
  competency_alignments: Optional[list] = []
  skill_alignments: Optional[list] = []


class ChildNodes(BaseModel):
  """Child Nodes Pydantic Model"""
  learning_objects: Optional[list] = []
  assessments: Optional[list] = []

class ParentNodes(BaseModel):
  """Parent Nodes Pydantic Model"""
  learning_opportunities: Optional[list] = []
  curriculum_pathways: Optional[list] = []


class UpdateAlignment(BaseModel):
  """Update Alignment Pydantic Model"""
  competency_alignments: list
  skill_alignments: list


class UpdateChildNodes(BaseModel):
  """Update Child Nodes Pydantic Model"""
  learning_objects: Optional[list]
  assessments: Optional[list]

  class Config():
    orm_mode = True
    extra = "forbid"


class UpdateParentNodes(BaseModel):
  """Update Parent Nodes Pydantic Model"""
  learning_opportunities: Optional[list]
  curriculum_pathways: Optional[list]

  class Config():
    orm_mode = True
    extra = "forbid"


class BasicLearningExperienceModel(BaseModel):
  """Learning Experience Pydantic Model"""
  name: str
  display_name: Optional[str]
  description: Optional[str] = ""
  author: Optional[str] = ""
  alignments: Optional[Alignment] = {}
  references: Optional[Reference] = {}
  child_nodes: Optional[ChildNodes] = {}
  parent_nodes: Optional[ParentNodes] = {}
  metadata: Optional[MetaData] = {}
  achievements: Optional[list] = []
  is_optional: Optional[bool] = False
  completion_criteria: Optional[LOSNodes] = {}
  prerequisites: Optional[LOSNodes] = {}
  is_locked: Optional[bool] = False
  is_hidden: Optional[bool] = False
  equivalent_credits: Optional[int] = 0
  duration: Optional[int] = 0
  alias: Optional[LE_ALIASES]
  order: Optional[int]
  type: Optional[LE_TYPES]
  resource_path: Optional[str] = ""
  srl_resource_path: Optional[str] = ""


class FullLearningExperienceModel(BasicLearningExperienceModel):
  """Learning Experience Model with uuid, created and updated time"""
  uuid: str
  version: Optional[int] = 1
  is_archived: Optional[bool] = False
  parent_version_uuid: Optional[str] = ""
  root_version_uuid: Optional[str] = ""
  created_time: str
  last_modified_time: str


class LearningExperienceModel(BasicLearningExperienceModel):
  """Learning Experience Input Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_LEARNING_EXPERIENCE_EXAMPLE}
    extra = "forbid"


class UpdateLearningExperienceModel(BaseModel):
  """Update Learning Experience Pydantic Model"""
  name: Optional[str]
  display_name: Optional[str]
  description: Optional[str]
  author: Optional[str]
  alignments: Optional[UpdateAlignment]
  references: Optional[Reference]
  child_nodes: Optional[UpdateChildNodes]
  is_optional: Optional[bool]
  parent_nodes: Optional[UpdateParentNodes]
  is_archived: Optional[bool]
  metadata: Optional[MetaData]
  is_locked: Optional[bool]
  is_hidden: Optional[bool]
  achievements: Optional[list]
  completion_criteria: Optional[LOSNodes]
  prerequisites: Optional[LOSNodes]
  duration: Optional[int]
  equivalent_credits: Optional[int]
  alias: Optional[LE_ALIASES]
  order: Optional[int]
  type: Optional[LE_TYPES]
  # TODO: Disable update for following fields post Alpha
  resource_path: Optional[str]
  srl_resource_path: Optional[str]

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_LEARNING_EXPERIENCE_EXAMPLE}
    extra = "forbid"


class LearningExperienceResponseModel(BaseModel):
  """Learning Experience Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the learning experience"
  data: FullLearningExperienceModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the learning experience",
            "data": FULL_LEARNING_EXPERIENCE_EXAMPLE
        }
    }


class DeleteLearningExperience(BaseModel):
  """Delete Learning Experience Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the learning experience"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the learning experience"
        }
    }


class LearningExperienceSearchResponseModel(BaseModel):
  """Learning Experience Search Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the learning experiences"
  data: List[FullLearningExperienceModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the learning experiences",
            "data": [FULL_LEARNING_EXPERIENCE_EXAMPLE]
        }
    }


class AllLearningExperiencesResponseModel(BaseModel):
  """Learning Experience Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Data fetched successfully"
  data: List[FullLearningExperienceModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Data fetched successfully",
            "data": [FULL_LEARNING_EXPERIENCE_EXAMPLE]
        }
    }


class LearningExperienceImportJsonResponse(BaseModel):
  """Learning Experience Import Json Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the learning experiences"
  data: List[str]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success":
                True,
            "message":
                "Successfully created the learning experiences",
            "data": [
                "44qxEpc35pVMb6AkZGbi", "00MPqUhCbyPe1BcevQDr",
                "lQRzcrRuDpJ9IoW8bCHu"
            ]
        }
    }


class CopyLearningExperienceModel(BaseModel):
  """Learning Experience Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the learning experience"
  data: FullLearningExperienceModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the learning experience",
            "data": FULL_LEARNING_EXPERIENCE_EXAMPLE
        }
    }
