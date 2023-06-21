"""
Pydantic Model for Assessment Item API's
"""
from typing import Dict, List, Optional
from typing_extensions import Literal
from pydantic import BaseModel
from schemas.schema_examples import (BASIC_ASSESSMENT_EXAMPLE,
                                     FULL_ASSESSMENT_EXAMPLE,
                                     UPDATE_ASSESSMENT_EXAMPLE,
                                     BASIC_HUMAN_GRADED_ASSESSMENT_EXAMPLE,
                                     UPDATE_HUMAN_GRADED_ASSESSMENT_EXAMPLE)
from config import (ALLOWED_THEMES, ASSESSMENT_TYPES,
                    ASSESSMENT_ALIASES)


SOURCE = Literal["learnosity"]

class Empty(BaseModel):
  class Config():
    extra = "forbid"

class DesignConfig(BaseModel):
  """DesignConfig Pydantic Model"""
  theme: Optional[ALLOWED_THEMES]
  illustration: Optional[str] = ""

class Items(BaseModel):
  """DesignConfig Pydantic Model"""
  skill: Optional[str] = ""
  competency: Optional[str] = ""

class MetaData(BaseModel):
  """Metadata Pydantic Model"""
  design_config: Optional[DesignConfig] = {}
  items: Optional[Dict[str, Items]] = {}

class AssessmentReference(BaseModel):
  activity_template_id: Optional[str] = ""
  source: Optional[SOURCE] = "learnosity"


class Reference(BaseModel):
  """Reference Pydantic Model"""
  competencies: Optional[list] = []
  skills: Optional[list] = []


class LOSNodes(BaseModel):
  """Parent Nodes Pydantic Model"""
  curriculum_pathways: Optional[List[str]] = []
  learning_experiences: Optional[List[str]] = []
  learning_objects: Optional[List[str]] = []
  learning_resources: Optional[List[str]] = []
  assessments: Optional[List[str]] = []


class ParentNodes(BaseModel):
  learning_objects: Optional[list] = []
  learning_experiences: Optional[list] = []


class ChildNodes(BaseModel):
  rubrics: Optional[list] = []


class Alignment(BaseModel):
  competency_alignments: Optional[list] = []
  skill_alignments: Optional[list] = []
  learning_resource_alignment: Optional[list] = []
  rubric_alignment: Optional[list] = []


class BasicAssessmentModel(BaseModel):
  """Assessment Skeleton Pydantic Model"""
  name: str
  display_name: Optional[str] = ""
  type: ASSESSMENT_TYPES
  order: Optional[int]
  author_id: Optional[str] = ""
  instructor_id: Optional[str] = ""
  assessment_reference: Optional[AssessmentReference] = {}
  max_attempts: Optional[int]
  pass_threshold: Optional[float]
  is_archived: Optional[bool] = False
  is_optional: Optional[bool] = False
  is_locked: Optional[bool] = False
  is_hidden: Optional[bool] = False
  achievements: Optional[list] = []
  alignments: Optional[Alignment] = {}
  references: Optional[Reference] = {}
  parent_nodes: Optional[ParentNodes] = {}
  child_nodes: Optional[ChildNodes] = {}
  prerequisites: Optional[LOSNodes] = {}
  metadata: Optional[MetaData] = {}
  alias: Optional[ASSESSMENT_ALIASES]
  is_autogradable: Optional[bool] = False
  resource_paths: Optional[List[str]] = []
  instructions: Optional[dict]


class FullAssessmentDataModel(BasicAssessmentModel):
  """Assessment Skeleton Model with uuid, created and updated time"""
  uuid: str
  created_time: str
  last_modified_time: str

class HumanGradedFullAssessmentDataModel(BasicAssessmentModel):
  """Human Graded Assessment Skeleton Model with uuid, created
     and updated time"""
  uuid: str
  created_time: str
  last_modified_time: str
  assessment_reference: Empty


class AssessmentModel(BasicAssessmentModel):
  """Assessment Input Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_ASSESSMENT_EXAMPLE}

class HumanGradedAssessmentModel(BasicAssessmentModel):
  """Assessment Input Pydantic Model"""
  assessment_reference: Empty

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_HUMAN_GRADED_ASSESSMENT_EXAMPLE}


class UpdateAssessmentModel(BaseModel):
  """Update Assessment Pydantic Model"""
  name: Optional[str]
  display_name: Optional[str]
  type: Optional[ASSESSMENT_TYPES]
  order: Optional[int]
  author_id: Optional[str]
  instructor_id: Optional[str]
  assessment_reference: Optional[AssessmentReference]
  max_attempts: Optional[int]
  pass_threshold: Optional[float]
  achievements: Optional[list]
  alignments: Optional[Alignment]
  references: Optional[Reference]
  parent_nodes: Optional[ParentNodes]
  child_nodes: Optional[ChildNodes]
  prerequisites: Optional[LOSNodes]
  metadata: Optional[MetaData]
  alias: Optional[ASSESSMENT_ALIASES]
  is_locked: Optional[bool]
  is_hidden: Optional[bool]
  is_optional: Optional[bool]
  is_archived: Optional[bool]
  resource_paths: Optional[List[str]]
  instructions: Optional[dict]
  is_autogradable: Optional[bool]

  class Config():
    orm_mode = True
    schema_extra = {"example": UPDATE_ASSESSMENT_EXAMPLE}

class UpdateHumanGradedAssessmentModel(UpdateAssessmentModel):
  """Update Input Pydantic Human graded Assessment Model"""
  assessment_reference: Optional[Empty] = {}

  class Config():
    orm_mode = True
    schema_extra = {"example": UPDATE_HUMAN_GRADED_ASSESSMENT_EXAMPLE}


class AssessmentModelResponse(BaseModel):
  """Assessment Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the assessment"
  data: Optional[FullAssessmentDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the assessment",
            "data": FULL_ASSESSMENT_EXAMPLE
        }
    }

class HumanGradedAssessmentResponse(BaseModel):
  """Assessment Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the assessment"
  data: Optional[HumanGradedFullAssessmentDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the assessment",
            "data": FULL_ASSESSMENT_EXAMPLE
        }
    }


class DeleteAssessment(BaseModel):
  """Delete Assessment Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the assessment"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the assessment"
        }
    }


class AssessmentSearchModelResponse(BaseModel):
  """Assessment Search Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the assessments"
  data: Optional[List[FullAssessmentDataModel]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the assessments",
            "data": [FULL_ASSESSMENT_EXAMPLE]
        }
    }

class AssessmentTypesResponse(BaseModel):
  """Assessment Search Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the assessment types"
  data: Optional[dict]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the assessment types",
            "data": {
              "static_srl": "SRL",
              "practice": "Formative",
              "project": "Summative"
            }
        }
    }


class TotalCountResponseModel(BaseModel):
  records: Optional[List[FullAssessmentDataModel]]
  total_count: int

class AllAssessmentsModelResponse(BaseModel):
  """Assessment Item Response Pydantic Model"""
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
                      "records":[FULL_ASSESSMENT_EXAMPLE],
                      "total_count": 50
                    }
        }
    }


class AssessmentsImportJsonResponse(BaseModel):
  """Assessment Items Import Json Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the assessment"
  data: List[str]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the assessment",
            "data": [
                "44qxEpc35pVMb6AkZGbi", "00MPqUhCbyPe1BcevQDr",
                "lQRzcrRuDpJ9IoW8bCHu"
            ]
        }
    }

class AssessmentLinkResponse(BaseModel):
  """Assessment Linking Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully linked the assessment"
  data: Optional[FullAssessmentDataModel]
  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully linked the assessment",
            "data": FULL_ASSESSMENT_EXAMPLE
        }
    }
