"""schema file for learner progress API"""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from enum import Enum
from pydantic import BaseModel
from schemas.schema_examples import (LEARNING_RESOURCE_PROGRESS_RESPONSE,
LEARNING_OBJECT_PROGRESS_RESPONSE,LEARNING_EXPERIENCE_PROGRESS_RESPONSE,
CURRICULUM_PATHWAY_PROGRESS_RESPONSE)

#pylint: disable=missing-class-docstring,line-too-long
class NodeTypeModel(str, Enum):
  curriculum_pathways = "curriculum_pathways"
  learning_experiences = "learning_experiences"
  learning_objects = "learning_objects"
  learning_resources = "learning_resources"

class LearningExperienceParentNodes(BaseModel):
  curriculum_pathways: List[str]


class References(BaseModel):
  skills: Optional[list]
  competencies: Optional[list]

class ChildNodes3(BaseModel):
  assessments: List[str]
  learning_resources: List[str]


class ParentNodes1(BaseModel):
  learning_experiences: List[str]


class RecentChildNode(BaseModel):
  uuid: str
  name: str
  display_name: str
  description: Optional[str] = ""
  author: Optional[str] = ""
  alignments: Dict[str, Any]
  references: Optional[References]
  child_nodes: Optional[ChildNodes3] = {}
  parent_nodes: Optional[ParentNodes1] = {}
  version: Optional[int] = 1
  parent_version_uuid: Optional[str] = ""
  root_version_uuid: Optional[str] = ""
  is_archived: Optional[bool] = False
  is_deleted: Optional[bool] = False
  metadata: Optional[dict] = {}
  achievements: Optional[list] = []
  completion_criteria: Dict[str, Any]
  prerequisites: Dict[str, Any]
  is_locked: bool
  is_optional: bool
  is_hidden: bool
  equivalent_credits: int
  duration: Optional[int]
  created_time: str
  last_modified_time: str
  created_by: str
  last_modified_by: str
  progress: int
  status: str
  last_attempted: Optional[str] = ""
  child_count: Optional[int] = 0
  completed_child_count: Optional[int] = 0
  alias: str
  type: str
  order: Optional[int] = 1


class LearningExperience(BaseModel):
  uuid: str
  name: str
  display_name: str
  description: Optional[str] = ""
  author: Optional[str] = ""
  alignments: Dict[str, Any]
  references: Dict[str, Any]
  parent_nodes: Optional[LearningExperienceParentNodes] = {}
  version: int
  parent_version_uuid: str
  root_version_uuid: str
  is_archived: bool
  is_deleted: bool
  metadata: Optional[dict] = {}
  achievements: Optional[list] = []
  completion_criteria: Dict[str, Any]
  prerequisites: Dict[str, Any]
  is_locked: bool
  is_optional: bool
  is_hidden: bool
  equivalent_credits: int
  duration: Optional[int]
  created_time: str
  last_modified_time: str
  created_by: str
  last_modified_by: str
  progress: int
  status: str
  last_attempted: Optional[str] = ""
  child_count: Optional[int] = 0
  completed_child_count: Optional[int] = 0
  recent_child_node: Optional[RecentChildNode] = {}
  alias: str
  type: str
  order: Optional[int]


class UnitCurriculumPathwayChildNodes(BaseModel):
  learning_experiences: Optional[List[LearningExperience]]


class CurriculumPathwayParentNodes(BaseModel):
  curriculum_pathways: Optional[List[str]]


class UnitCurriculumPathway(BaseModel):
  uuid: str
  name: str
  display_name: str
  description: Optional[str] = ""
  author: Optional[str] = ""
  alignments: Any
  references: Dict[str, Any]
  child_nodes: Optional[UnitCurriculumPathwayChildNodes] = {}
  parent_nodes: Optional[CurriculumPathwayParentNodes] = {}
  version: int
  parent_version_uuid: str
  root_version_uuid: str
  is_archived: bool
  is_deleted: bool
  metadata: Optional[dict] = {}
  achievements: Optional[list] = []
  completion_criteria: Dict[str, Any]
  prerequisites: Dict[str, Any]
  is_locked: bool
  is_optional: bool
  is_hidden: bool
  equivalent_credits: int
  duration: Optional[int]
  created_time: str
  last_modified_time: str
  created_by: str
  last_modified_by: str
  progress: int
  status: str
  last_attempted: Optional[str] = ""
  child_count: Optional[int] = 0
  completed_child_count: Optional[int] = 0
  earned_achievements: Optional[list] = []
  alias: str
  type: str
  order: Optional[int]


class LevelCurriculumPathwayChildNodes(BaseModel):
  curriculum_pathways: Optional[List[UnitCurriculumPathway]]


class LevelCurriculumPathway(BaseModel):
  uuid: str
  name: str
  display_name: str
  description: Optional[str] = ""
  author: Optional[str] = ""
  alignments: Any
  references: Dict[str, Any]
  child_nodes: Optional[LevelCurriculumPathwayChildNodes] = {}
  parent_nodes: Optional[CurriculumPathwayParentNodes] = {}
  version: int
  parent_version_uuid: str
  root_version_uuid: str
  is_archived: bool
  is_deleted: bool
  metadata: Optional[dict] = {}
  achievements: Optional[list] = []
  completion_criteria: Dict[str, Any]
  prerequisites: Dict[str, Any]
  is_locked: bool
  is_optional: bool
  is_hidden: bool
  equivalent_credits: int
  duration: Optional[int]
  created_time: str
  last_modified_time: str
  created_by: str
  last_modified_by: str
  progress: int
  status: str
  last_attempted: Optional[str] = ""
  child_count: Optional[int] = 0
  completed_child_count: Optional[int] = 0
  earned_achievements: Optional[list] = []
  alias: str
  type: str
  order: Optional[int]


class DisciplineCurriculumPathwayChildNodes(BaseModel):
  curriculum_pathways: Optional[List[LevelCurriculumPathway]]


class DisciplineCurriculumPathway(BaseModel):
  uuid: str
  name: str
  display_name: str
  description: Optional[str] = ""
  author: Optional[str] = ""
  alignments: Any
  references: Dict[str, Any]
  child_nodes: Optional[DisciplineCurriculumPathwayChildNodes] = {}
  parent_nodes: Optional[CurriculumPathwayParentNodes] = {}
  version: int
  parent_version_uuid: str
  root_version_uuid: str
  is_archived: bool
  is_deleted: bool
  metadata: Optional[dict] = {}
  achievements: Optional[list] = []
  completion_criteria: Dict[str, Any]
  prerequisites: Dict[str, Any]
  is_locked: bool
  is_optional: bool
  is_hidden: bool
  equivalent_credits: int
  duration: Optional[int]
  created_time: str
  last_modified_time: str
  created_by: str
  last_modified_by: str
  progress: int
  status: str
  last_attempted: Optional[str] = ""
  child_count: Optional[int] = 0
  completed_child_count: Optional[int] = 0
  earned_achievements: Optional[list] = []
  alias: str
  type: str
  order: Optional[int]

class ProgramCurriculumPathwayChildNodes(BaseModel):
  curriculum_pathways: Optional[List[DisciplineCurriculumPathway]]

class ProgramCurriculumPathway(BaseModel):
  uuid: str
  name: str
  display_name: str
  description: Optional[str] = ""
  author: Optional[str] = ""
  alignments: Any
  references: Dict[str, Any]
  child_nodes: Optional[ProgramCurriculumPathwayChildNodes] = {}
  parent_nodes: Dict[str, Any]
  version: int
  parent_version_uuid: str
  root_version_uuid: str
  is_archived: bool
  is_deleted: bool
  metadata: Optional[dict] = {}
  achievements: Optional[list] = []
  completion_criteria: Dict[str, Any]
  prerequisites: Dict[str, Any]
  is_locked: bool
  is_optional: bool
  is_hidden: bool
  equivalent_credits: int
  duration: Optional[int]
  created_time: str
  last_modified_time: str
  created_by: str
  last_modified_by: str
  progress: int
  status: str
  last_attempted: Optional[str] = ""
  child_count: Optional[int] = 0
  completed_child_count: Optional[int] = 0
  earned_achievements: Optional[list] = []
  alias: str
  type: str
  order: Optional[int]


class ParentNodes4(BaseModel):
  learning_objects: Optional[List[str]]


class LearningResourceProgress(BaseModel):
  uuid: str
  name: str
  display_name: Any
  description: Optional[str] = ""
  author: Optional[str] = ""
  type: Optional[str]
  resource_path: Any
  lti_content_item_id: Any
  course_category: List
  alignments: Dict[str, Any]
  references: Dict[str, Any]
  parent_nodes: Optional[ParentNodes4] = {}
  child_nodes: Dict[str, Any]
  version: int
  parent_version_uuid: str
  root_version_uuid: str
  is_archived: bool
  is_deleted: bool
  metadata: Optional[dict] = {}
  achievements: Optional[list] = []
  completion_criteria: Dict[str, Any]
  prerequisites: Dict[str, Any]
  is_locked: bool
  is_optional: bool
  is_hidden: bool
  status: str
  current_content_version: Any
  content_history: Dict[str, Any]
  publish_history: Dict[str, Any]
  created_time: str
  last_modified_time: str
  created_by: str
  last_modified_by: str
  progress: int
  last_attempted: Optional[str] = ""
  child_count: Optional[int] = 0
  completed_child_count: Optional[int] = 0
  alias: str
  type: str
  order: Optional[int]


class Prerequisites(BaseModel):
  learning_resources: List[str]


class Assessment(BaseModel):
  uuid: str
  name: str
  type: Optional[str]
  author_id: Any
  assessment_reference: Any
  instructor_id: Any
  assessor_id: Any
  parent_nodes: Optional[ParentNodes4] = {}
  child_nodes: Any
  pass_threshold: Any
  max_attempts: Any
  alignments: Any
  references: Any
  achievements: Optional[list] = []
  prerequisites: Prerequisites
  is_locked: bool
  is_optional: bool
  is_hidden: bool
  is_deleted: bool
  metadata: Any
  created_time: str
  last_modified_time: str
  created_by: str
  last_modified_by: str
  progress: int
  status: str
  last_attempted: Optional[str] = ""
  child_count: Optional[int] = 0
  completed_child_count: Optional[int] = 0
  alias: str
  type: str
  order: Optional[int]
  instruction_completed: Optional[bool] = False


class LearningResource(BaseModel):
  uuid: str
  name: str
  display_name: Any
  description: Optional[str] = ""
  author: Optional[str] = ""
  type: Optional[str]
  resource_path: Any
  lti_content_item_id: Any
  course_category: List
  alignments: Dict[str, Any]
  references: Dict[str, Any]
  parent_nodes: Optional[ParentNodes4] = {}
  child_nodes: Dict[str, Any]
  version: int
  parent_version_uuid: str
  root_version_uuid: str
  is_archived: bool
  is_deleted: bool
  metadata: Optional[dict] = {}
  achievements: Optional[list] = []
  completion_criteria: Dict[str, Any]
  prerequisites: Dict[str, Any]
  is_locked: bool
  is_optional: bool
  is_hidden: bool
  status: str
  current_content_version: Any
  content_history: Dict[str, Any]
  publish_history: Dict[str, Any]
  created_time: str
  last_modified_time: str
  created_by: str
  last_modified_by: str
  progress: int
  last_attempted: Optional[str] = ""
  child_count: Optional[int] = 0
  completed_child_count: Optional[int] = 0
  alias: str
  type: str
  order: Optional[int]


class ChildNodes4(BaseModel):
  assessments: Optional[list] = []
  learning_resources: Optional[list] = []
  learning_objects: Optional[list] = []


class ParentNodes7(BaseModel):
  learning_experiences: Optional[list]
  learning_objects: Optional[list]

class LearningObjectProgress(BaseModel):
  uuid: str
  name: str
  display_name: str
  description: Optional[str] = ""
  author: Optional[str] = ""
  alignments: Dict[str, Any]
  references: Optional[References] = {}
  child_nodes: Optional[ChildNodes4] = {}
  parent_nodes: Optional[ParentNodes7] = {}
  version: int
  parent_version_uuid: str
  root_version_uuid: str
  is_archived: bool
  is_deleted: bool
  metadata: Optional[dict] = {}
  achievements: Optional[list] = []
  completion_criteria: Dict[str, Any] = {}
  prerequisites: Dict[str, Any] = {}
  is_locked: bool
  is_optional: bool
  is_hidden: bool
  equivalent_credits: int
  duration: Optional[int]
  created_time: str
  last_modified_time: str
  created_by: str
  last_modified_by: str
  progress: int
  status: str
  last_attempted: Optional[str] = ""
  child_count: Optional[int] = 0
  completed_child_count: Optional[int] = 0
  alias: str
  type: str
  order: Optional[int] = 1
  recent_child_node: Optional[RecentChildNode] = {}


class ChildNodes6(BaseModel):
  learning_resources: Optional[List[str]]
  assessments: Optional[List[str]]


class LearningObject(BaseModel):
  uuid: str
  name: str
  display_name: str
  description: Optional[str] = ""
  author: Optional[str] = ""
  alignments: Dict[str, Any]
  references: Optional[References]
  child_nodes: Optional[ChildNodes6] = {}
  parent_nodes: Optional[ParentNodes7] = {}
  version: int
  parent_version_uuid: str
  root_version_uuid: str
  is_archived: bool
  is_deleted: bool
  metadata: Optional[dict] = {}
  achievements: Optional[list] = []
  completion_criteria: Dict[str, Any]
  prerequisites: Dict[str, Any]
  is_locked: bool
  is_optional: bool
  is_hidden: bool
  equivalent_credits: int
  duration: Optional[int]
  created_time: str
  last_modified_time: str
  created_by: str
  last_modified_by: str
  progress: int
  status: str
  last_attempted: Optional[str] = ""
  child_count: Optional[int] = 0
  completed_child_count: Optional[int] = 0
  alias: str
  type: str
  order: Optional[int] = 1


class ChildNodes5(BaseModel):
  learning_objects: Optional[List[LearningObject]]


class ParentNodes9(BaseModel):
  curriculum_pathways: Optional[List[str]]


class LearningExperienceProgress(BaseModel):
  uuid: str
  name: str
  display_name: str
  description: Optional[str] = ""
  author: Optional[str] = ""
  alignments: Dict[str, Any]
  references: Dict[str, Any]
  child_nodes: Optional[ChildNodes5] = {}
  parent_nodes: Optional[ParentNodes9] = {}
  version: int
  parent_version_uuid: str
  root_version_uuid: str
  is_archived: bool
  is_deleted: bool
  metadata: Optional[dict] = {}
  achievements: Optional[list] = []
  completion_criteria: Dict[str, Any]
  prerequisites: Dict[str, Any]
  is_locked: bool
  is_optional: bool
  is_hidden: bool
  equivalent_credits: int
  duration: Optional[int]
  created_time: str
  last_modified_time: str
  created_by: str
  last_modified_by: str
  progress: int
  status: str
  last_attempted: Optional[str] = ""
  child_count: Optional[int] = 0
  completed_child_count: Optional[int] = 0
  alias: str
  type: str
  order: Optional[int]
  recent_child_node: Optional[RecentChildNode] = {}

class CurriculumPathwayProgressResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the curriculum_pathways progress for the given learner"
  data: Union[Any, ProgramCurriculumPathway]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the curriculum_pathways progress for the given learner",
            "data": CURRICULUM_PATHWAY_PROGRESS_RESPONSE
        }
    }

class LearningExperienceProgressResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the learning_experiences progress for the given learner"
  data: LearningExperienceProgress

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the learning_experiences progress for the given learner",
            "data": LEARNING_EXPERIENCE_PROGRESS_RESPONSE
        }
    }

class LearningObjectProgressResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the learning_objects progress for the given learner"
  data: LearningObjectProgress

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the learning_objects progress for the given learner",
            "data": LEARNING_OBJECT_PROGRESS_RESPONSE
        }
    }

class LearningResourceProgressResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the learning_resources progress for the given learner"
  data: LearningResourceProgress

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the learning_resources progress for the given learner",
            "data": LEARNING_RESOURCE_PROGRESS_RESPONSE
        }
    }
