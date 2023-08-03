"""
Pydantic Model for xAPI Statement API's
"""
from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel
from schemas.schema_examples import (BASIC_XAPI_STATEMENT, FULL_XAPI_STATEMENT)
from typing_extensions import Literal
from common.utils.schema_validator import BaseConfigModel
# pylint: disable=line-too-long


class AgentModel(BaseModel):
  """Agent(Actor) Pydantic Model"""
  uuid: str
  object_type: Literal["agent", "group"]
  name: str
  mbox: Optional[str] = ""
  mbox_sha1sum: Optional[str] = ""
  open_id: Optional[str] = ""
  account_homepage: Optional[str] = ""
  account_name: Optional[str] = ""
  members: Optional[list] = []
  user_id: Optional[str] = ""


class VerbModel(BaseModel):
  """Verb Pydantic Model"""
  uuid: str
  name: str
  url: str
  canonical_data: Optional[dict] = {}



Type = Literal[
  "learning_experiences",
  "curriculum_pathways",
  "learning_objects",
  "learning_resources",
  "assessment_items"]


class Hierarchy(BaseModel):
  curriculum_pathways: Optional[List[PathwayModel]]


class LearningObjectChildNodes(BaseModel):
  """Learning Object Child Nodes Pydantic Model"""
  learning_objects: Optional[List[LearningObjectModel]] = []


class LearningObjectModel(BaseModel):
  """Learning Object Pydantic Model"""
  name: str
  uuid: str
  child_nodes: Optional[LearningObjectChildNodes] = {}


class LearningExperienceChildNodes(BaseModel):
  """Learning Experience Child Nodes Pydantic Model"""
  learning_objects: Optional[List[LearningObjectModel]] = []


class LearningExperienceModel(BaseModel):
  """Learning Experience Pydantic Model"""
  name: Optional[str]
  uuid: str
  child_nodes: Optional[LearningExperienceChildNodes] = {}


class ChildNodes(BaseModel):
  """Child Nodes Pydantic Model"""
  learning_experiences: Optional[List[LearningExperienceModel]] = []
  curriculum_pathways: Optional[List[PathwayModel]] = []


class PathwayModel(BaseModel):
  """UploadPathwayModel Pydantic Model"""
  name: Optional[str]
  uuid: Optional[str]
  child_nodes: Optional[ChildNodes] = {}


class ObjectDetails(BaseModel):
  name: Optional[str]
  type: Optional[Type]
  uuid: Optional[str]
  hierarchy: Optional[Hierarchy]
  existing_document: Optional[dict]


class ActivityModel(BaseModel):
  """Activity(Object) Pydantic Model"""
  uuid: str
  name: str
  authority: Optional[str] = ""
  canonical_data: Optional[dict] = {}


class BasicStatementModel(BaseConfigModel):
  """Basic xAPI Statement Pydantic Model"""
  actor: AgentModel
  verb: VerbModel
  object: ActivityModel
  object_type: Literal["activities", "agents",
  "learning_experiences",
  "curriculum_pathways",
  "learning_objects",
  "learning_resources",
  "assessments",
  "submitted_assessments"]
  session_id: str
  result: Optional[dict] = {}
  context: Optional[dict] = {}
  timestamp: Optional[str]
  authority: Optional[dict] = {}
  attachments: Optional[list] = []
  result_success: Optional[bool]
  result_completion: Optional[bool]
  result_score_raw: Optional[float]
  result_score_min: Optional[float]
  result_score_max: Optional[float]


class LRSDetailsModel(BaseModel):
  """Info about LRS"""
  version: str


class LRSDetailsResponseModel(BaseModel):
  """LRS about info response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the details about LRS"
  data: LRSDetailsModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the details about LRS",
            "data": {
                "version": "1.0.3"
            }
        }
    }


class InputStatementsModel(BasicStatementModel):
  """Input Statements Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_XAPI_STATEMENT}


class FullStatementModel(BasicStatementModel):
  """Full xAPI Statements Pydantic Model"""
  uuid: str
  stored: str


class PostStatementsResponseModel(BaseModel):
  """xAPI Statement Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully added the given statement/s"
  data: List[str]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully added the given statement/s",
            "data": ["qiw1vb7t1qwicubo", "pb0vpvb1y32r1vp0"]
        }
    }


class GetStatementResponseModel(BaseModel):
  """Get Statement Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the statement"
  data: FullStatementModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the statement",
            "data": FULL_XAPI_STATEMENT
        }
    }

class TotalCountResponseModel(BaseModel):
  records: Optional[List[FullStatementModel]]
  total_count: int

class GetAllStatementsResponseModel(BaseModel):
  """Get all Statements Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the statements"
  data: TotalCountResponseModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the statements",
            "data": {
                      "records":[FULL_XAPI_STATEMENT],
                      "total_count": 50
                    }
        }
    }


Hierarchy.update_forward_refs()

ChildNodes.update_forward_refs()
LearningObjectChildNodes.update_forward_refs()
