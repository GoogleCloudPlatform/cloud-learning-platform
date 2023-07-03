"""
Pydantic models for Issuer
"""
from pydantic import BaseModel
from typing import Optional, List
from schemas.schema_examples import BASIC_ISSUER_EXAMPLE


class BasicIssuerModel(BaseModel):
  """BasicIssuer Pydantic Model"""
  entity_type: Optional[str]
  entity_id: Optional[str]
  open_badge_id: Optional[str]
  name: str
  image: Optional[str]
  email: str
  description: Optional[str]
  url: str
  staff: Optional[List[dict]]
  extensions: Optional[str]
  badgr_domain: Optional[str]


class IssuerModel(BasicIssuerModel):
  """Issuer Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_ISSUER_EXAMPLE}


class FullIssuerModel(BasicIssuerModel):
  """Issuer Model with uuid, created and updated time"""
  uuid: str
  created_time: str
  last_modified_time: str


class IssuerResponseModel(BaseModel):
  """IssuerResponseModel Pydantic Model"""
  success: Optional[bool]
  message: Optional[str]
  data: Optional[FullIssuerModel]

  class Config():
    orm_mode = True


class AllIssuerResponseModel(BaseModel):
  """AllIssuerResponseModel Pydantic Model"""
  success: Optional[bool]
  message: Optional[str]
  data: Optional[List[FullIssuerModel]]

  class Config():
    orm_mode = True


class DeleteIssuer(BaseModel):
  """DeleteIssuer Pydantic Model"""
  success: Optional[bool]
  message: Optional[str]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the Issuer"
        }
    }


class IssuerImportJsonResponse(BaseModel):
  """DeleteIssuer Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the Issuers"
  data: Optional[List[str]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success":
                True,
            "message":
                "Successfully created the issuer",
            "data": [
                "44qxEpc35pVMb6AkZGbi", "00MPqUhCbyPe1BcevQDr",
                "lQRzcrRuDpJ9IoW8bCHu"
            ]
        }
    }
