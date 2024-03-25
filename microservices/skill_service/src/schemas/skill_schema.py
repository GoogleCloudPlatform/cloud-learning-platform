"""
Pydantic Models for Skill API's
"""
from typing import Optional, List
from pydantic import BaseModel
from schemas.schema_examples import (BASIC_SKILL_MODEL_EXAMPLE,
                                     FULL_SKILL_MODEL_EXAMPLE)
# pylint: disable = line-too-long


class AlignedSuggested(BaseModel):
  """Aligned Suggested Pydantic Model"""
  aligned: Optional[List[dict]] = []
  suggested: Optional[List[dict]] = []


class AlignedSuggestedStr(BaseModel):
  """Aligned Suggested Pydantic Model"""
  aligned: Optional[List[str]] = []
  suggested: Optional[List[str]] = []


class SkillAlignment(BaseModel):
  """Skill Alignment Pydantic Model"""
  emsi: Optional[AlignedSuggested] = {}
  snhu: Optional[AlignedSuggested] = {}
  osn: Optional[AlignedSuggested] = {}
  e2e_osn: Optional[AlignedSuggested] = {}


class KnowledgeAlignment(BaseModel):
  """Knowledge Alignment Pydantic Model"""
  knowledge_nodes: Optional[AlignedSuggested] = {}
  learning_resource_ids: Optional[AlignedSuggestedStr] = {}
  learning_unit_ids: Optional[AlignedSuggestedStr] = {}


class RoleAlignment(BaseModel):
  """Role Alignment Pydantic Model"""
  onet: Optional[AlignedSuggested] = {}


class Alignment(BaseModel):
  """Alignment Pydantic Model"""
  standard_alignment: Optional[dict] = {}
  credential_alignment: Optional[dict] = {}
  skill_alignment: Optional[SkillAlignment] = {}
  knowledge_alignment: Optional[KnowledgeAlignment] = {}
  role_alignment: Optional[RoleAlignment] = {}
  organizational_alignment: Optional[dict] = {}


class Occupation(BaseModel):
  """Skill Occupation Pydantic Model"""
  occupations_major_group: Optional[list] = []
  occupations_minor_group: Optional[list] = []
  broad_occupation: Optional[list] = []
  detailed_occupation: Optional[list] = []


class Type(BaseModel):
  """Skill Type Pydantic Model"""
  id: Optional[str] = ""
  name: Optional[str] = ""

class ParentNodes(BaseModel):
  """Parent Nodes Pydantic Model"""
  competencies: Optional[list] = []

class ChildNodes(BaseModel):
  skills: Optional[list] = []

class BasicSkillModel(BaseModel):
  """Skill Skeleton Pydantic Model"""
  name: str
  description: str
  keywords: Optional[List] = None
  author: Optional[str] = ""
  creator: Optional[str] = ""
  alignments: Optional[Alignment] = None
  organizations: Optional[List[str]] = [""]
  certifications: Optional[List[str]] = [""]
  occupations: Optional[Occupation] = None
  onet_job: Optional[str] = ""
  type: Optional[Type] = None
  parent_nodes: Optional[ParentNodes] = {}
  child_nodes: Optional[ChildNodes] = {}
  reference_id: Optional[str] = ""
  source_uri: Optional[str] = ""
  source_name: Optional[str] = ""


class FullSkillDataModel(BasicSkillModel):
  """Skill Skeleton Model with uuid, created and updated time"""
  uuid: str
  created_time: str
  last_modified_time: str


class SkillModel(BasicSkillModel):
  """Skill Input Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_SKILL_MODEL_EXAMPLE}


class UpdateSkillModel(BasicSkillModel):
  """Update Skill Pydantic Model"""
  name: Optional[str]
  description: Optional[str]

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_SKILL_MODEL_EXAMPLE}


class GetSkillResponseModel(BaseModel):
  """Skill Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the skill"
  data: Optional[FullSkillDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the skill",
            "data": FULL_SKILL_MODEL_EXAMPLE
        }
    }


class PostSkillResponseModel(BaseModel):
  """Skill Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the skill"
  data: Optional[FullSkillDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the skill",
            "data": FULL_SKILL_MODEL_EXAMPLE
        }
    }


class UpdateSkillResponseModel(BaseModel):
  """Skill Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the skill"
  data: Optional[FullSkillDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully updated the skill",
            "data": FULL_SKILL_MODEL_EXAMPLE
        }
    }


class DeleteSkill(BaseModel):
  """Delete Skill Pydantic Model"""
  success: bool = True
  message: str = "Successfully deleted the skill"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the skill"
        }
    }


class AllSkillsResponseModel(BaseModel):
  """Skill Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Data fetched successfully"
  data: Optional[List[FullSkillDataModel]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Data fetched successfully",
            "data": [FULL_SKILL_MODEL_EXAMPLE]
        }
    }


class SkillImportJsonResponse(BaseModel):
  """Skill Import Json Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the skills"
  data: Optional[List[str]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success":
                True,
            "message":
                "Successfully created the skills",
            "data": [
                "44qxEpc35pVMb6AkZGbi", "00MPqUhCbyPe1BcevQDr",
                "lQRzcrRuDpJ9IoW8bCHu"
            ]
        }
    }
