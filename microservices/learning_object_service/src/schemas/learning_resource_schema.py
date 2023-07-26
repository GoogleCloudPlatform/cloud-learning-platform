"""
Pydantic Model for Learning Resource API"s
"""
from pydantic import BaseModel
from typing import List, Optional
from config import (ALLOWED_THEMES, LR_TYPES, ALLOWED_RESOURCE_STATUS,
                    LR_ALIASES)
from schemas.schema_examples import (BASIC_LEARNING_RESOURCE_EXAMPLE,
                                     UPDATE_LEARNING_RESOURCE_EXAMPLE,
                                     FULL_LEARNING_RESOURCE_EXAMPLE)


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
  assessment_items: Optional[List[str]] = []
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
  concepts: Optional[list] = []


class ParentNodes(BaseModel):
  """Parent Nodes Pydantic Model"""
  learning_objects: Optional[list] = []


class UpdateAlignment(BaseModel):
  """Update Alignment Pydantic Model"""
  competency_alignments: list
  skill_alignments: list


class UpdateChildNodes(BaseModel):
  """Update Child Nodes Pydantic Model"""
  concepts: list


class UpdateParentNodes(BaseModel):
  """Update Parent Nodes Pydantic Model"""
  learning_objects: list

class BasicLearningResourceModel(BaseModel):
  """Learning Resource Pydantic Model"""
  name: str
  display_name: Optional[str]
  description: Optional[str] = ""
  type: Optional[LR_TYPES] = ""
  resource_path: Optional[str] = ""
  lti_content_item_id: Optional[str] = ""
  course_category: Optional[list] = []
  alignments: Optional[Alignment] = {}
  references: Optional[Reference] = {}
  child_nodes: Optional[ChildNodes] = {}
  parent_nodes: Optional[ParentNodes] = {}
  metadata: Optional[MetaData] = {}
  achievements: Optional[list] = []
  completion_criteria: Optional[LOSNodes] = {}
  prerequisites: Optional[LOSNodes] = {}
  is_locked: Optional[bool] = False
  is_optional: Optional[bool] = False
  is_hidden: Optional[bool] = False
  status: Optional[ALLOWED_RESOURCE_STATUS] = "initial"
  current_content_version: Optional[str] = ""
  alias: Optional[LR_ALIASES]
  order: Optional[int]
  duration: Optional[int] = 15


class FullLearningResourceDataModel(BasicLearningResourceModel):
  """Learning Resource Skeleton Model with uuid, created and updated time"""
  uuid: str
  version: Optional[int] = 1
  parent_version_uuid: Optional[str] = ""
  root_version_uuid: Optional[str] = ""
  is_archived: Optional[bool] = False
  created_time: str
  last_modified_time: str
  is_locked: Optional[bool]
  last_published_on: Optional[str]
  alias: Optional[str] = "lesson"
  status: Optional[ALLOWED_RESOURCE_STATUS] = "initial"
  is_implicit: Optional[bool]=False

  def __init__(self, **kwargs):
    if kwargs["status"] == "initial":
      kwargs["status"] = "draft"
    super().__init__(**kwargs)

class LearningResourceModel(BasicLearningResourceModel):
  """Learning Resource Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_LEARNING_RESOURCE_EXAMPLE}
    extra = "forbid"


class UpdateLearningResourceModel(BaseModel):
  """Update Learning Resource Pydantic Model"""
  name: Optional[str]
  display_name: Optional[str]
  description: Optional[str]
  author: Optional[str]
  type: Optional[LR_TYPES]
  resource_path: Optional[str]
  lti_content_item_id: Optional[str]
  course_category: Optional[list]
  alignments: Optional[UpdateAlignment]
  references: Optional[Reference]
  child_nodes: Optional[UpdateChildNodes]
  parent_nodes: Optional[UpdateParentNodes]
  is_archived: Optional[bool]
  metadata: Optional[MetaData]
  is_locked: Optional[bool]
  achievements: Optional[list] = []
  completion_criteria: Optional[LOSNodes]
  prerequisites: Optional[LOSNodes]
  is_optional: Optional[bool]
  is_hidden: Optional[bool]
  status: Optional[ALLOWED_RESOURCE_STATUS]
  current_content_version: Optional[str]
  alias: Optional[LR_ALIASES]
  order: Optional[int]
  duration: Optional[int]

  class Config():
    orm_mode = True
    schema_extra = {"example": UPDATE_LEARNING_RESOURCE_EXAMPLE}
    extra = "forbid"


class GetLearningResourceModelResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the learning resource"
  data: FullLearningResourceDataModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the learning resource",
            "data": FULL_LEARNING_RESOURCE_EXAMPLE
        }
    }


class PostLearningResourceModelResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the learning resource"
  data: FullLearningResourceDataModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the learning resource",
            "data": FULL_LEARNING_RESOURCE_EXAMPLE
        }
    }


class UpdateLearningResourceModelResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the learning resource"
  data: FullLearningResourceDataModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully updated the learning resource",
            "data": FULL_LEARNING_RESOURCE_EXAMPLE
        }
    }

class TotalCountResponseModel(BaseModel):
  records: Optional[List[FullLearningResourceDataModel]]
  total_count: int

class AllLearningResourcesModelResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the learning resources"
  data: TotalCountResponseModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the learning resources",
            "data": {
                      "records":[FULL_LEARNING_RESOURCE_EXAMPLE],
                      "total_count": 50
                    }
        }
    }


class DeleteLearningResource(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the learning resource"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the learning resource"
        }
    }


class LearningResourceSearchModelResponse(BaseModel):
  """Learning Resource Search Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the learning resources"
  data: List[FullLearningResourceDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the learning resources",
            "data": [FULL_LEARNING_RESOURCE_EXAMPLE]
        }
    }


class LearningResourceImportJsonResponse(BaseModel):
  """Learning Resource Import Json Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the learning resources"
  data: List[str]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the learning resources",
            "data": [
                "44qxEpc35pVMb6AkZGbi", "00MPqUhCbyPe1BcevQDr",
                "lQRzcrRuDpJ9IoW8bCHu"
            ]
        }
    }


class CopyLearningResourceModel(BaseModel):
  """Learning Resource Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully copied the learning experience"
  data: FullLearningResourceDataModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully copied the learning experience",
            "data": FULL_LEARNING_RESOURCE_EXAMPLE
        }
    }
