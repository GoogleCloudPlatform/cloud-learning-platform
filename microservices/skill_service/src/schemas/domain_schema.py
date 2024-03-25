"""
Pydantic Model for Domain API's
"""
from typing import List, Optional
from pydantic import BaseModel
from schemas.schema_examples import (BASIC_DOMAIN_MODEL_EXAMPLE,
                                     FULL_DOMAIN_MODEL_EXAMPLE)
# pylint: disable=line-too-long

class ChildNodes(BaseModel):
  """Child Nodes Pydantic Model"""
  sub_domains: Optional[list] = []

class BasicDomainModel(BaseModel):
  """Domain Skeleton Pydantic Model"""
  name: str
  description: str
  keywords: Optional[List[str]] = [""]
  reference_id: Optional[str] = ""
  source_uri: Optional[str] = ""
  source_name: Optional[str] = ""
  child_nodes: Optional[ChildNodes] = {}


class FullDomainDataModel(BasicDomainModel):
  """Domain Skeleton Model with uuid, created and updated time"""
  uuid: str
  created_time: str
  last_modified_time: str


class DomainModel(BasicDomainModel):
  """Domain Input Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_DOMAIN_MODEL_EXAMPLE}


class UpdateDomainModel(BasicDomainModel):
  """Update Domain Pydantic Model"""
  name: Optional[str]
  description: Optional[str]

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_DOMAIN_MODEL_EXAMPLE}


class GetDomainResponseModel(BaseModel):
  """Domain Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the domain"
  data: Optional[FullDomainDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the domain",
            "data": FULL_DOMAIN_MODEL_EXAMPLE
        }
    }


class PostDomainResponseModel(BaseModel):
  """Domain Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the domain"
  data: Optional[FullDomainDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the domain",
            "data": FULL_DOMAIN_MODEL_EXAMPLE
        }
    }


class UpdateDomainResponseModel(BaseModel):
  """Domain Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the domain"
  data: Optional[FullDomainDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully updated the domain",
            "data": FULL_DOMAIN_MODEL_EXAMPLE
        }
    }


class DeleteDomain(BaseModel):
  """Delete Domain Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the domain"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the domain"
        }
    }


class AllDomainResponseModel(BaseModel):
  """Domain Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Data fetched successfully"
  data: Optional[List[FullDomainDataModel]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Data fetched successfully",
            "data": [FULL_DOMAIN_MODEL_EXAMPLE]
        }
    }


class DomainImportJsonResponse(BaseModel):
  """Domain Import Json Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the domains"
  data: Optional[List[str]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success":
                True,
            "message":
                "Successfully created the domains",
            "data": [
                "44qxEpc35pVMb6AkZGbi", "00MPqUhCbyPe1BcevQDr",
                "lQRzcrRuDpJ9IoW8bCHu"
            ]
        }
    }
