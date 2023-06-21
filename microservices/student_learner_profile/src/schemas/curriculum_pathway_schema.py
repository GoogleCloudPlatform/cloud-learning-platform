"""
Pydantic Model for Curriculum Pathway APIs
"""
from typing import List, Optional
from pydantic import BaseModel
from schemas.schema_examples import BASIC_CURRICULUM_PATHWAY_EXAMPLE


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
  metadata: Optional[dict] = {}
  achievements: Optional[list] = []
  completion_criteria: Optional[LOSNodes] = {}
  prerequisites: Optional[LOSNodes] = {}
  is_locked: Optional[bool] = False
  equivalent_credits: Optional[int] = 0
  duration: Optional[int] = 0


class LearningHierarchyModel(BasicCurriculumPathwayModel):
  """Curriculum Pathway Model with uuid, created and updated time"""
  uuid: str
  version: Optional[int] = 1
  is_archived: Optional[bool] = False
  parent_version_uuid: Optional[str] = ""
  root_version_uuid: Optional[str] = ""
  created_time: str
  last_modified_time: str
  is_locked: Optional[bool]
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


class NewLearningHierarchyResponseModel(BaseModel):
  label: str
  type: str
  data: LearningHierarchyModel
  children: list
