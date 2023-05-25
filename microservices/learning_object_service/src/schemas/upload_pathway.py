"""
Pydantic Model for Bulk Upload Pathway API's
"""
from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel
from config import (CP_TYPES, LE_TYPES, LO_TYPES,
                    ASSESSMENT_TYPES, LR_TYPES,
                    CP_ALIASES, LE_ALIASES, LO_ALIASES,
                    ASSESSMENT_ALIASES, LR_ALIASES,
                    ALLOWED_THEMES, ALLOWED_RESOURCE_STATUS)
from typing_extensions import Literal
SOURCE = Literal["learnosity"]

class DesignConfig(BaseModel):
  """DesignConfig Pydantic Model"""
  theme: Optional[ALLOWED_THEMES] = ""
  illustration: Optional[str] = ""

class MetaData(BaseModel):
  """Metadata Pydantic Model"""
  design_config: Optional[DesignConfig] = {}

class AssessmentReference(BaseModel):
  activity_template_id: Optional[str] = ""
  source: Optional[SOURCE] = "learnosity"


class LOSNodes(BaseModel):
  """Parent Nodes Pydantic Model"""
  curriculum_pathways: Optional[List[str]] = []
  learning_experiences: Optional[List[str]] = []
  learning_objects: Optional[List[str]] = []
  learning_resources: Optional[List[str]] = []
  assessments: Optional[List[str]] = []


class SkillParentNodes(BaseModel):
  """Parent Nodes Pydantic Model"""
  competencies: Optional[list] = []


class SkillModel(BaseModel):
  """Skill Skeleton Pydantic Model"""
  name: str
  description: str
  keywords: Optional[List] = None
  author: Optional[str] = ""
  creator: Optional[str] = ""
  alignments: Optional[dict] = {}
  organizations: Optional[List[str]] = [""]
  certifications: Optional[List[str]] = [""]
  occupations: Optional[dict] = {}
  onet_job: Optional[str] = ""
  type: Optional[dict] = {}
  parent_nodes: Optional[SkillParentNodes] = {}
  reference_id: Optional[str] = ""
  source_uri: Optional[str] = ""
  source_name: Optional[str] = ""


class CompetencyParentNodes(BaseModel):
  """Competency Parent Nodes Pydantic Model"""
  categories: Optional[list] = []
  sub_domains: Optional[list] = []


class CompetencyChildNodes(BaseModel):
  """Competency Child Nodes Pydantic Model"""
  skills: Optional[list] = []


class CompetencyModel(BaseModel):
  """Competency Skeleton Pydantic Model"""
  name: Optional[str] = ""
  description: str
  keywords: Optional[List[str]] = [""]
  level: Optional[str] = ""
  subject_code: Optional[str] = ""
  course_code: Optional[str] = ""
  course_title: Optional[str] = ""
  alignments: Optional[dict] = {}
  occupations: Optional[dict] = {}
  parent_nodes: Optional[CompetencyParentNodes] = {}
  child_nodes: Optional[CompetencyChildNodes] = {}
  reference_id: Optional[str] = ""
  source_uri: Optional[str] = ""
  source_name: Optional[str] = ""


class Reference(BaseModel):
  """Reference Pydantic Model"""
  competencies: Optional[List[CompetencyModel]] = []
  skills: Optional[List[SkillModel]] = []


class AssessmentAlignments(BaseModel):
  competency_alignments: Optional[list] = []
  skill_alignments: Optional[list] = []
  learning_resource_alignment: Optional[list] = []
  rubric_alignment: Optional[list] = []


class AssessmentModel(BaseModel):
  """Assessment Skeleton Pydantic Model"""
  name: str
  display_name: Optional[str] = ""
  type: ASSESSMENT_TYPES
  author_id: Optional[str] = ""
  instructor_id: Optional[str] = ""
  assessor_id: Optional[str] = ""
  assessment_reference: Optional[AssessmentReference] = {}
  max_attempts: Optional[int]
  pass_threshold: Optional[float] = 0.7
  is_optional: Optional[bool] = False
  is_locked: Optional[bool] = False
  is_hidden: Optional[bool] = False
  achievements: Optional[list] = []
  alignments: Optional[AssessmentAlignments] = {}
  references: Optional[Reference] = {}
  parent_nodes: Optional[dict] = {}
  child_nodes: Optional[dict] = {}
  prerequisites: Optional[LOSNodes] = {}
  metadata: Optional[MetaData] = {}
  # FIXME: tags should be Literal
  tags: Optional[dict]
  order: Optional[int] = 1
  alias: Optional[ASSESSMENT_ALIASES]


class Alignment(BaseModel):
  """Alignment Pydantic Model"""
  competency_alignments: Optional[list] = []
  skill_alignments: Optional[list] = []


class LearningResourceChildNodes(BaseModel):
  """Learning Resource Child Nodes Pydantic Model"""
  concepts: Optional[list] = []


class LearningResourceParentNodes(BaseModel):
  """Learning Resource Parent Nodes Pydantic Model"""
  learning_objects: Optional[List[LearningObjectModel]] = []


class LearningResourceModel(BaseModel):
  """Learning Resource Pydantic Model"""
  name: Optional[str]
  display_name: Optional[str]
  description: Optional[str] = ""
  type: Optional[LR_TYPES] = ""
  resource_path: Optional[str] = ""
  lti_content_item_id: Optional[str] = ""
  course_category: Optional[list] = []
  alignments: Optional[Alignment] = {}
  is_optional: Optional[bool] = False
  is_locked: Optional[bool] = False
  is_hidden: Optional[bool] = False
  references: Optional[Reference]
  achievements: Optional[list] = []
  completion_criteria: Optional[LOSNodes] = {}
  child_nodes: Optional[LearningResourceChildNodes] = {}
  parent_nodes: Optional[LearningResourceParentNodes] = {}
  status: Optional[ALLOWED_RESOURCE_STATUS] = "initial"
  current_content_version: Optional[str] = ""
  metadata: Optional[MetaData]
  alias: Optional[LR_ALIASES]
  order: Optional[int] = 1
  duration: Optional[int] = 15

class LearningObjectChildNodes(BaseModel):
  """Learning Object Child Nodes Pydantic Model"""
  learning_objects: Optional[List[LearningObjectModel]] = []
  learning_resources: Optional[List[LearningResourceModel]] = []
  assessments: Optional[List[AssessmentModel]] = []


class LearningObjectParentNodes(BaseModel):
  """Learning Object Parent Nodes Pydantic Model"""
  learning_experiences: Optional[List[LearningExperienceModel]] = []


class LearningObjectModel(BaseModel):
  """Learning Object Pydantic Model"""
  name: Optional[str]
  display_name: Optional[str]
  description: Optional[str] = ""
  author: Optional[str] = ""
  alignments: Optional[Alignment] = {}
  is_optional: Optional[bool] = False
  is_locked: Optional[bool] = False
  is_hidden: Optional[bool] = False
  references: Optional[Reference]
  achievements: Optional[list] = []
  completion_criteria: Optional[LOSNodes] = {}
  child_nodes: Optional[LearningObjectChildNodes] = {}
  parent_nodes: Optional[LearningObjectParentNodes] = {}
  metadata: Optional[MetaData]
  alias: Optional[LO_ALIASES]
  order: Optional[int] = 1
  type: Optional[LO_TYPES]
  duration: Optional[int] = 15
  equivalent_credits: Optional[int] = 0


class LearningExperienceChildNodes(BaseModel):
  """Learning Experience Child Nodes Pydantic Model"""
  learning_objects: Optional[List[LearningObjectModel]] = []
  assessments: Optional[List[AssessmentModel]] = []


class LearningExperienceParentNodes(BaseModel):
  """Learning Experience Parent Nodes Pydantic Model"""
  learning_opportunities: Optional[list] = []
  curriculum_pathways: Optional[List[UploadPathwayModel]] = []


class LearningExperienceModel(BaseModel):
  """Learning Experience Pydantic Model"""
  name: Optional[str]
  display_name: Optional[str]
  description: Optional[str] = ""
  author: Optional[str] = ""
  alignments: Optional[Alignment] = {}
  is_optional: Optional[bool] = False
  is_locked: Optional[bool] = False
  is_hidden: Optional[bool] = False
  references: Optional[Reference]
  achievements: Optional[list] = []
  completion_criteria: Optional[LOSNodes] = {}
  child_nodes: Optional[LearningExperienceChildNodes] = {}
  parent_nodes: Optional[LearningExperienceParentNodes] = {}
  metadata: Optional[MetaData]
  alias: Optional[LE_ALIASES]
  type: Optional[LE_TYPES]
  order: Optional[int] = 1
  equivalent_credits: Optional[int] = 0
  duration: Optional[int] = 15
  resource_path: Optional[str] = ""


class ChildNodes(BaseModel):
  """Child Nodes Pydantic Model"""
  learning_experiences: Optional[List[LearningExperienceModel]] = []
  curriculum_pathways: Optional[List[UploadPathwayModel]] = []


class ParentNodes(BaseModel):
  """Parent Nodes Pydantic Model"""
  learning_opportunities: Optional[list] = []
  curriculum_pathways: Optional[UploadPathwayModel] = []


class UploadPathwayModel(BaseModel):
  """UploadPathwayModel Pydantic Model"""
  name: Optional[str]
  display_name: Optional[str] = ""
  description: Optional[str] = ""
  author: Optional[str] = ""
  alignments: Optional[Alignment] = {}
  is_optional: Optional[bool] = False
  is_locked: Optional[bool] = False
  is_active: Optional[bool] = False
  is_hidden: Optional[bool] = False
  references: Optional[Reference]
  child_nodes: Optional[ChildNodes] = {}
  parent_nodes: Optional[ParentNodes] = {}
  metadata: Optional[MetaData]
  achievements: Optional[list] = []
  completion_criteria: Optional[LOSNodes] = {}
  alias: Optional[CP_ALIASES]
  type: Optional[CP_TYPES]
  order: Optional[int] = 1
  equivalent_credits: Optional[int] = 0
  duration: Optional[int] = 15


class PathwayImportJsonResponse(BaseModel):
  """Learning Hierarchy Import Json Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully inserted the Learning Hierarchy"
  data: Optional[List[str]] = []

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully inserted the Learning Hierarchy",
            "data": ["jmFNsNRc0He4m22dxEUc"]
        }
    }


LearningExperienceParentNodes.update_forward_refs()
ChildNodes.update_forward_refs()
ParentNodes.update_forward_refs()
LearningObjectChildNodes.update_forward_refs()
LearningResourceParentNodes.update_forward_refs()
LearningObjectParentNodes.update_forward_refs()
