"""
Pydantic Model for Assessment Item API's
"""
from typing import List, Optional
from typing_extensions import Literal
from pydantic import BaseModel, constr
from schemas.schema_examples import (BASIC_ASSESSMENT_ITEM_EXAMPLE,
                                     FULL_ASSESSMENT_ITEM_EXAMPLE,
                                     UPDATE_ASSESSMENT_ITEM_EXAMPLE)

# pylint: disable=line-too-long

SOURCE = Literal["learnosity"]


class AssessmentReference(BaseModel):
  activity_id: Optional[str] = ""
  activity_template_id: Optional[str] = ""
  source: Optional[SOURCE] = "learnosity"


class Reference(BaseModel):
  """Reference Pydantic Model"""
  competencies: Optional[list] = []
  skills: Optional[list] = []


class ParentNodes(BaseModel):
  learning_objects: Optional[list] = []
  assessments: Optional[list] = []


class Alignment(BaseModel):
  competency_alignments: Optional[list] = []
  skill_alignments: Optional[list] = []
  learning_resource_alignment: Optional[list] = []
  rubric_alignment: Optional[list] = []


class BasicAssessmentItemModel(BaseModel):
  """AssessmentItem Skeleton Pydantic Model"""
  name: str
  question: Optional[str] = ""
  answer: Optional[str] = ""
  context: Optional[str] = ""
  options: Optional[list] = []
  question_type: Optional[str] = ""
  assessment_type: Optional[str] = ""
  use_type: Optional[str] = ""
  metadata: Optional[dict] = {}
  author: Optional[str] = ""
  difficulty: Optional[float] = 0
  alignments: Optional[Alignment] = {}
  references: Optional[Reference] = {}
  parent_nodes: Optional[ParentNodes] = {}
  child_nodes: Optional[dict] = {}
  assessment_reference: Optional[AssessmentReference] = {}
  achievements: Optional[list] = []
  pass_threshold: Optional[int] = 1
  is_flagged: Optional[bool]
  comments: Optional[constr(max_length=300)]


class FullAssessmentItemDataModel(BasicAssessmentItemModel):
  """AssessmentItem Skeleton Model with uuid, created and updated time"""
  uuid: str
  created_time: str
  last_modified_time: str


class AssessmentItemModel(BasicAssessmentItemModel):
  """AssessmentItem Input Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_ASSESSMENT_ITEM_EXAMPLE}


class UpdateAssessmentItemModel(BaseModel):
  """Update AssessmentItem Pydantic Model"""
  name: Optional[str]
  question: Optional[str]
  answer: Optional[str]
  context: Optional[str]
  options: Optional[list]
  question_type: Optional[str]
  assessment_type: Optional[str]
  use_type: Optional[str]
  metadata: Optional[dict]
  author: Optional[str]
  difficulty: Optional[float]
  alignments: Optional[Alignment]
  references: Optional[Reference]
  parent_nodes: Optional[ParentNodes]
  child_nodes: Optional[dict]
  assessment_reference: Optional[AssessmentReference]
  achievements: Optional[list]
  pass_threshold: Optional[int]
  is_flagged: Optional[bool]
  comments: Optional[constr(max_length=300)]

  class Config():
    orm_mode = True
    schema_extra = {"example": UPDATE_ASSESSMENT_ITEM_EXAMPLE}


class AssessmentItemModelResponse(BaseModel):
  """AssessmentItem Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the assessment_item"
  data: Optional[FullAssessmentItemDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the assessment_item",
            "data": FULL_ASSESSMENT_ITEM_EXAMPLE
        }
    }


class DeleteAssessmentItem(BaseModel):
  """Delete AssessmentItem Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the assessment_item"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the assessment_item"
        }
    }


class AssessmentItemSearchModelResponse(BaseModel):
  """AssessmentItem Search Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the assessment_items"
  data: Optional[List[FullAssessmentItemDataModel]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the assessment_items",
            "data": [FULL_ASSESSMENT_ITEM_EXAMPLE]
        }
    }

class TotalCountResponseModel(BaseModel):
  records: Optional[List[FullAssessmentItemDataModel]]
  total_count: int

class AllAssessmentItemsModelResponse(BaseModel):
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
                      "records":[FULL_ASSESSMENT_ITEM_EXAMPLE],
                      "total_count": 50
                    }
        }
    }


class AssessmentItemsImportJsonResponse(BaseModel):
  """Assessment Items Import Json Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the assessment item"
  data: List[str]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the assessment item",
            "data": [
                "44qxEpc35pVMb6AkZGbi", "00MPqUhCbyPe1BcevQDr",
                "lQRzcrRuDpJ9IoW8bCHu"
            ]
        }
    }
