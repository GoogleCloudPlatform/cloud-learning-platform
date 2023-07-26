"""
Pydantic Model for Learning Object API's
"""
from typing import List, Optional
from pydantic import BaseModel
from schemas.schema_examples import (BASIC_LEARNING_OBJECT_EXAMPLE,
                                     FULL_LEARNING_OBJECT_EXAMPLE)
from config import ALLOWED_THEMES, LO_TYPES, LO_ALIASES


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
  learning_resources: Optional[list] = []
  assessments: Optional[list] = []


class ParentNodes(BaseModel):
  """Parent Nodes Pydantic Model"""
  learning_experiences: Optional[list] = []
  learning_objects: Optional[list] = []


class UpdateAlignment(BaseModel):
  """Update Alignment Pydantic Model"""
  competency_alignments: list
  skill_alignments: list


class UpdateChildNodes(BaseModel):
  """Update Child Nodes Pydantic Model"""
  learning_objects: Optional[list]
  learning_resources: Optional[list]
  assessments: Optional[list]


class UpdateParentNodes(BaseModel):
  """Update Parent Nodes Pydantic Model"""
  learning_experiences: Optional[list]
  learning_objects: Optional[list]


class BasicLearningObjectModel(BaseModel):
  """Learning Object Pydantic Model"""
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
  completion_criteria: Optional[LOSNodes] = {}
  prerequisites: Optional[LOSNodes] = {}
  is_optional: Optional[bool] = False
  is_locked: Optional[bool] = False
  is_hidden: Optional[bool] = False
  equivalent_credits: Optional[int] = 0
  duration: Optional[int] = 0
  alias: Optional[LO_ALIASES]
  order: Optional[int] = 1
  type: Optional[LO_TYPES]


class FullLearningObjectModel(BasicLearningObjectModel):
  """Learning Object Model with uuid, created and updated time"""
  uuid: str
  version: Optional[int] = 1
  parent_version_uuid: Optional[str] = ""
  root_version_uuid: Optional[str] = ""
  is_archived: Optional[bool] = False
  created_time: str
  last_modified_time: str


class LearningObjectModel(BasicLearningObjectModel):
  """Learning Object Input Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_LEARNING_OBJECT_EXAMPLE}
    extra = "forbid"


class UpdateLearningObjectModel(BaseModel):
  """Update Learning Object Pydantic Model"""
  name: Optional[str]
  display_name: Optional[str]
  description: Optional[str]
  author: Optional[str]
  alignments: Optional[UpdateAlignment]
  references: Optional[Reference]
  child_nodes: Optional[UpdateChildNodes]
  parent_nodes: Optional[UpdateParentNodes]
  is_archived: Optional[bool]
  metadata: Optional[MetaData]
  is_locked: Optional[bool]
  is_optional: Optional[bool]
  is_hidden: Optional[bool]
  achievements: Optional[list]
  completion_criteria: Optional[LOSNodes]
  prerequisites: Optional[LOSNodes]
  duration: Optional[int]
  equivalent_credits: Optional[int]
  alias: Optional[LO_ALIASES]
  order: Optional[int]
  type: Optional[LO_TYPES]

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_LEARNING_OBJECT_EXAMPLE}
    extra = "forbid"


class LearningObjectResponseModel(BaseModel):
  """Learning Object Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the learning object"
  data: FullLearningObjectModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the learning object",
            "data": FULL_LEARNING_OBJECT_EXAMPLE
        }
    }


class DeleteLearningObject(BaseModel):
  """Delete Learning Object Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the learning object"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the learning object"
        }
    }


class LearningObjectSearchResponseModel(BaseModel):
  """Learning Object Search Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the learning objects"
  data: List[FullLearningObjectModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the learning objects",
            "data": [FULL_LEARNING_OBJECT_EXAMPLE]
        }
    }

class TotalCountResponseModel(BaseModel):
  records: Optional[List[FullLearningObjectModel]]
  total_count: int

class AllLearningObjectsResponseModel(BaseModel):
  """Learning Object Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Data fetched successfully"
  data: TotalCountResponseModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Data fetched successfully",
            "data": {
                      "records":[FULL_LEARNING_OBJECT_EXAMPLE],
                      "total_count": 50
                    }
        }
    }


class LearningObjectImportJsonResponse(BaseModel):
  """Learning Object Import Json Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the learning objects"
  data: List[str]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success":
                True,
            "message":
                "Successfully created the learning objects",
            "data": [
                "44qxEpc35pVMb6AkZGbi", "00MPqUhCbyPe1BcevQDr",
                "lQRzcrRuDpJ9IoW8bCHu"
            ]
        }
    }


class CopyLearningObjectModel(BaseModel):
  """Learning Object Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully copied the learning object"
  data: FullLearningObjectModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully copied the learning object",
            "data": FULL_LEARNING_OBJECT_EXAMPLE
        }
    }
