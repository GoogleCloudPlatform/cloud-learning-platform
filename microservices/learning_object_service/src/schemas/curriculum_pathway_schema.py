"""
Pydantic Model for Curriculum Pathway API's
"""
from typing import List, Optional
from pydantic import BaseModel
from schemas.schema_examples import (BASIC_CURRICULUM_PATHWAY_EXAMPLE,
                                     FULL_CURRICULUM_PATHWAY_EXAMPLE,
                                     CURRICULUM_PATHWAY_BY_ALIAS_EXAMPLE)
from config import ALLOWED_THEMES, CP_ALIASES, CP_TYPES
# pylint: disable=line-too-long

class DesignConfig(BaseModel):
  """DesignConfig Pydantic Model"""
  theme: Optional[ALLOWED_THEMES] = ""
  illustration: Optional[str] = ""

class MetaData(BaseModel):
  """Metadata Pydantic Model"""
  design_config: Optional[DesignConfig] = {}

class LOSNodes(BaseModel):
  """Parent Nodes Pydantic Model"""
  curriculum_pathways: Optional[list] = []
  learning_experiences: Optional[list] = []
  learning_objects: Optional[list] = []
  learning_resources: Optional[list] = []
  assessments: Optional[list] = []

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
  learning_experiences: Optional[list] = []
  curriculum_pathways: Optional[list] = []


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
  learning_experiences: Optional[list]
  curriculum_pathways: Optional[list]

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


class BasicCurriculumPathwayModel(BaseModel):
  """Curriculum Pathway Pydantic Model"""
  name: str
  display_name: Optional[str] = ""
  description: Optional[str] = ""
  author: Optional[str] = ""
  alignments: Optional[Alignment] = {}
  references: Optional[Reference]
  child_nodes: Optional[ChildNodes] = {}
  parent_nodes: Optional[ParentNodes] = {}
  metadata: Optional[MetaData] = {}
  achievements: Optional[list] = []
  completion_criteria: Optional[LOSNodes] = {}
  prerequisites: Optional[LOSNodes] = {}
  is_locked: Optional[bool] = False
  equivalent_credits: Optional[int] = 0
  duration: Optional[int] = 0
  is_optional: Optional[bool] = False
  is_hidden: Optional[bool] = False
  is_active: Optional[bool] = False
  alias: Optional[CP_ALIASES] = "unit"
  type: Optional[CP_TYPES]
  order: Optional[int]


class FullCurriculumPathwayModel(BasicCurriculumPathwayModel):
  """Curriculum Pathway Model with uuid, created and updated time"""
  uuid: str
  version: Optional[int] = 1
  is_archived: Optional[bool] = False
  parent_version_uuid: Optional[str] = ""
  root_version_uuid: Optional[str] = ""
  created_time: str
  last_modified_time: str


class LearningHierarchyModel(BasicCurriculumPathwayModel):
  """Curriculum Pathway Model with uuid, created and updated time"""
  uuid: str
  version: Optional[int] = 1
  is_archived: Optional[bool] = False
  parent_version_uuid: Optional[str] = ""
  root_version_uuid: Optional[str] = ""
  created_time: str
  last_modified_time: str
  progress: Optional[float]
  status: Optional[str]
  earned_achievements: Optional[List]
  child_nodes_count: Optional[int]
  completed_child_nodes_count: Optional[int]


class CurriculumPathwayModel(BasicCurriculumPathwayModel):
  """Curriculum Pathway Input Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_CURRICULUM_PATHWAY_EXAMPLE}
    extra = "forbid"


class UpdateCurriculumPathwayModel(BaseModel):
  """Update Curriculum Pathway Pydantic Model"""
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
  achievements: Optional[list]
  is_optional: Optional[bool]
  is_hidden: Optional[bool]
  is_active: Optional[bool]
  completion_criteria: Optional[LOSNodes]
  prerequisites: Optional[LOSNodes]
  duration: Optional[int]
  equivalent_credits: Optional[int]
  alias: Optional[CP_ALIASES]
  type: Optional[CP_TYPES]
  order: Optional[int]

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_CURRICULUM_PATHWAY_EXAMPLE}
    extra = "forbid"


class CurriculumPathwayResponseModel(BaseModel):
  """Curriculum Pathway Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the curriculum pathway"
  data: LearningHierarchyModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the curriculum pathway",
            "data": FULL_CURRICULUM_PATHWAY_EXAMPLE
        }
    }


class NewLearningHierarchyResponseModel(BaseModel):
  label: str
  type: str
  data: LearningHierarchyModel
  children: list


class CurriculumPathwayResponseModel2(BaseModel):
  """Learning Experience Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the curriculum pathway"
  data: List[NewLearningHierarchyResponseModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the curriculum pathway",
            "data": []
        }
    }


class DeleteCurriculumPathway(BaseModel):
  """Delete Curriculum Pathway Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the curriculum pathway"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the curriculum pathway"
        }
    }


class DeleteLearningPathway(BaseModel):
  """Delete Learning Pathway Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the learning hierarchy"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the learning hierarchy"
        }
    }


class CurriculumPathwaySearchResponseModel(BaseModel):
  """Curriculum Pathway Search Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the curriculum pathways"
  data: List[FullCurriculumPathwayModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the curriculum pathways",
            "data": [FULL_CURRICULUM_PATHWAY_EXAMPLE]
        }
    }


class CurriculumPathwayAliasModel(BaseModel):
  """Fetch Curriculum Pathway by Alias Response Pydantic Model"""
  uuid: str
  name: str
  alias: str

class GetCurriculumPathwayAliasResponseModel(BaseModel):
  """Fetch Curriculum Pathway by Alias Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the nodes"
  data: List[CurriculumPathwayAliasModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the nodes",
            "data": [CURRICULUM_PATHWAY_BY_ALIAS_EXAMPLE]
        }
    }

class AllCurriculumPathwaysResponseModel(BaseModel):
  """Curriculum Pathway Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Data fetched successfully"
  data: List[FullCurriculumPathwayModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Data fetched successfully",
            "data": [FULL_CURRICULUM_PATHWAY_EXAMPLE]
        }
    }


class CurriculumPathwayImportJsonResponse(BaseModel):
  """Curriculum Pathway Import Json Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the curriculum pathways"
  data: List[str]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the curriculum pathways",
            "data": [
                "44qxEpc35pVMb6AkZGbi", "00MPqUhCbyPe1BcevQDr",
                "lQRzcrRuDpJ9IoW8bCHu"
            ]
        }
    }


class CopyCurriculumPathwayModel(BaseModel):
  """Curriculum Pathway Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the curriculum pathway"
  data: FullCurriculumPathwayModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the curriculum pathway",
            "data": FULL_CURRICULUM_PATHWAY_EXAMPLE
        }
    }
