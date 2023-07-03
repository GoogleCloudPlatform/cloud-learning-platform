"""
Pydantic Model for Agent API's
"""
from typing import List, Optional
from pydantic import BaseModel
from typing_extensions import Literal
from schemas.schema_examples import (BASIC_AGENT_SCHEMA_EXAMPLE,
                                     FULL_AGENT_SCHEMA_EXAMPLE,
                                     UPDATE_AGENT_SCHEMA_EXAMPLE)


class BasicAgentModel(BaseModel):
  """Agent Pydantic Model"""
  object_type: Literal["agent", "group"]
  name: str
  mbox: Optional[str] = ""
  mbox_sha1sum: Optional[str] = ""
  open_id: Optional[str] = ""
  account_homepage: str
  account_name: Optional[str] = ""
  members: Optional[list] = []
  user_id: str


class FullAgentDataModel(BasicAgentModel):
  """Agent Model with uuid, created and updated time"""
  uuid: str
  created_time: str
  last_modified_time: str
  # FIXME: remove optional after all docs get this field
  is_deleted: Optional[bool] = False


class AgentModel(BasicAgentModel):
  """Agent Input Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_AGENT_SCHEMA_EXAMPLE}
    extra = "forbid"


class UpdateAgentModel(BaseModel):
  """Update Agent Pydantic Model"""
  object_type: Optional[Literal["agent", "group"]]
  name: Optional[str]
  mbox: Optional[str]
  mbox_sha1sum: Optional[str]
  open_id: Optional[str]
  account_homepage: Optional[str]
  account_name: Optional[str]
  members: Optional[list]
  user_id: Optional[str]

  class Config():
    orm_mode = True
    schema_extra = {"example": UPDATE_AGENT_SCHEMA_EXAMPLE}
    extra = "forbid"


class GetAgentModelResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the agent"
  data: FullAgentDataModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the agent",
            "data": FULL_AGENT_SCHEMA_EXAMPLE
        }
    }


class PostAgentModelResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the agent"
  data: FullAgentDataModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the agent",
            "data": FULL_AGENT_SCHEMA_EXAMPLE
        }
    }


class UpdateAgentModelResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the agent"
  data: FullAgentDataModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully updated the agent",
            "data": FULL_AGENT_SCHEMA_EXAMPLE
        }
    }


class AllAgentModelResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the agents"
  data: List[FullAgentDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the agents",
            "data": [FULL_AGENT_SCHEMA_EXAMPLE]
        }
    }


class DeleteAgent(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the agent"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the agent"
        }
    }


class AgentSearchModelResponse(BaseModel):
  """Agent Search Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the agents"
  data: List[FullAgentDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the agents",
            "data": [FULL_AGENT_SCHEMA_EXAMPLE]
        }
    }


class AgentImportJsonResponse(BaseModel):
  """Agent Import Json Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the agents"
  data: List[str]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the agents",
            "data": [
                "44qxEpc35pVMb6AkZGbi", "00MPqUhCbyPe1BcevQDr",
                "lQRzcrRuDpJ9IoW8bCHu"
            ]
        }
    }
