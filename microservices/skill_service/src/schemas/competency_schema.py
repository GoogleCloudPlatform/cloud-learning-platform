"""
Pydantic Model for Competency API's
"""
from typing import List, Dict, Optional
from pydantic import BaseModel
from schemas.schema_examples import (BASIC_COMPETENCY_MODEL_EXAMPLE,
                                     FULL_COMPETENCY_MODEL_EXAMPLE)
# pylint: disable=line-too-long


class Occupation(BaseModel):
  """Occupation Pydantic Model"""
  occupations_major_group: Optional[list] = []
  occupations_minor_group: Optional[list] = []
  broad_occupation: Optional[list] = []
  detailed_occupation: Optional[list] = []


class CompetencyAlignment(BaseModel):
  """Competency Alignment Pydantic Model"""
  standard_alignment: Optional[dict] = {}
  credential_alignment: Optional[dict] = {}
  skill_alignment: Optional[dict] = {}
  organizational_alignment: Optional[dict] = {}
  competency_alignment: Optional[dict] = {}
  o_net_alignment: Optional[dict] = {}


class ParentNodes(BaseModel):
  """Parent Nodes Pydantic Model"""
  categories: Optional[list] = []
  sub_domains: Optional[list] = []

class ChildNodes(BaseModel):
  """Parent Nodes Pydantic Model"""
  skills: Optional[list] = []

class BasicCompetencyModel(BaseModel):
  """Competency Skeleton Pydantic Model"""
  name: Optional[str] = ""
  description: str
  keywords: Optional[List[str]] = [""]
  level: Optional[str] = ""
  subject_code: Optional[str] = ""
  course_code: Optional[str] = ""
  course_title: Optional[str] = ""
  alignments: Optional[CompetencyAlignment] = None
  category: Optional[str] = None
  occupations: Optional[Occupation] = None
  parent_nodes: Optional[ParentNodes] = {}
  child_nodes: Optional[ChildNodes] = {}
  reference_id: Optional[str] = ""
  source_uri: Optional[str] = ""
  source_name: Optional[str] = ""


class FullCompetencyDataModel(BasicCompetencyModel):
  """Competency Skeleton Model with uuid, created and updated time"""
  uuid: str
  created_time: str
  last_modified_time: str


class CompetencyModel(BasicCompetencyModel):
  """Competency Input Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_COMPETENCY_MODEL_EXAMPLE}


class UpdateCompetencyModel(BasicCompetencyModel):
  """Update Competency Pydantic Model"""
  description: Optional[str]

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_COMPETENCY_MODEL_EXAMPLE}


class GetCompetencyResponseModel(BaseModel):
  """Competency Input Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the competency"
  data: Optional[FullCompetencyDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the competency",
            "data": FULL_COMPETENCY_MODEL_EXAMPLE
        }
    }


class PostCompetencyResponseModel(BaseModel):
  """Competency Input Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the competency"
  data: Optional[FullCompetencyDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the competency",
            "data": FULL_COMPETENCY_MODEL_EXAMPLE
        }
    }


class UpdateCompetencyResponseModel(BaseModel):
  """Competency Input Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the competency"
  data: Optional[FullCompetencyDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully updated the competency",
            "data": FULL_COMPETENCY_MODEL_EXAMPLE
        }
    }


class DeleteCompetency(BaseModel):
  """Delete Competency Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the competency"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the competency"
        }
    }


class AllCompetencyResponseModel(BaseModel):
  """Competency Input Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Data fetched successfully"
  data: Optional[List[FullCompetencyDataModel]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Data fetched successfully",
            "data": [FULL_COMPETENCY_MODEL_EXAMPLE]
        }
    }


class CompetencyImportJsonResponse(BaseModel):
  """Competency Import Json Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the competencies"
  data: Optional[List[str]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success":
                True,
            "message":
                "Successfully created the competencies",
            "data": [
                "44qxEpc35pVMb6AkZGbi", "00MPqUhCbyPe1BcevQDr",
                "lQRzcrRuDpJ9IoW8bCHu"
            ]
        }
    }


class ChildSkillsResponse(BaseModel):
  skill_name: str
  skill_id: str

class CompetenciesSkillsResponse(BaseModel):
  """Child Skills of Competencies Response Model"""
  success: Optional[bool] = True
  message: Optional[str] = \
    "Successfully fetched the child skills of competencies"
  data: Optional[Dict[str, List[ChildSkillsResponse]]]
