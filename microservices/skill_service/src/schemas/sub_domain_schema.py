"""
Pydantic Model for SubDomain API's
"""
from typing import List, Optional
from pydantic import BaseModel
from schemas.schema_examples import (BASIC_SUB_DOMAIN_MODEL_EXAMPLE,
                                     FULL_SUB_DOMAIN_MODEL_EXAMPLE)
# pylint: disable=line-too-long

class ChildNodes(BaseModel):
  """Child Nodes Pydantic Model"""
  categories: Optional[list] = []
  competencies: Optional[list] = []

class ParentNodes(BaseModel):
  """Parent Nodes Pydantic Model"""
  domains: Optional[list] = []

class BasicSubDomainModel(BaseModel):
  """Role Skeleton Pydantic Model"""
  name: str
  description: str
  keywords: Optional[List[str]] = [""]
  parent_nodes: Optional[ParentNodes] = {}
  child_nodes: Optional[ChildNodes] = {}
  reference_id: Optional[str] = ""
  source_uri: Optional[str] = ""
  source_name: Optional[str] = ""


class FullSubDomainDataModel(BasicSubDomainModel):
  """Role Skeleton Model with uuid, created and updated time"""
  uuid: str
  created_time: str
  last_modified_time: str


class SubDomainModel(BasicSubDomainModel):
  """SubDomain Input Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_SUB_DOMAIN_MODEL_EXAMPLE}


class UpdateSubDomainModel(BasicSubDomainModel):
  """Update SubDomain Pydantic Model"""
  name: Optional[str]
  description: Optional[str]

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_SUB_DOMAIN_MODEL_EXAMPLE}


class GetSubDomainResponseModel(BaseModel):
  """SubDomain Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the sub-domain"
  data: Optional[FullSubDomainDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the sub-domain",
            "data": FULL_SUB_DOMAIN_MODEL_EXAMPLE
        }
    }


class PostSubDomainResponseModel(BaseModel):
  """SubDomain Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the sub-domain"
  data: Optional[FullSubDomainDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the sub-domain",
            "data": FULL_SUB_DOMAIN_MODEL_EXAMPLE
        }
    }


class UpdateSubDomainResponseModel(BaseModel):
  """SubDomain Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the sub-domain"
  data: Optional[FullSubDomainDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully updated the sub-domain",
            "data": FULL_SUB_DOMAIN_MODEL_EXAMPLE
        }
    }


class DeleteSubDomain(BaseModel):
  """Delete Skill Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the sub-domain"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the sub-domain"
        }
    }


class AllSubDomainsResponseModel(BaseModel):
  """SubDomain Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Data fetched successfully"
  data: Optional[List[FullSubDomainDataModel]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Data fetched successfully",
            "data": [FULL_SUB_DOMAIN_MODEL_EXAMPLE]
        }
    }


class SubDomainImportJsonResponse(BaseModel):
  """SubDomain Import Json Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the sub-domains"
  data: Optional[List[str]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success":
                True,
            "message":
                "Successfully created the sub-domains",
            "data": [
                "44qxEpc35pVMb6AkZGbi", "00MPqUhCbyPe1BcevQDr",
                "lQRzcrRuDpJ9IoW8bCHu"
            ]
        }
    }
