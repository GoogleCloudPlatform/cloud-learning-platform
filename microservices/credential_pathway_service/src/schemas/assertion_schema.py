"""
Pydantic models for Assertion
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from schemas.schema_examples import BASIC_ASSERTION_EXAMPLE


class BasicAssertionModel(BaseModel):
  """BasicAssertion Pydantic Model"""
  entity_type: Optional[str]
  entity_id: Optional[str]
  open_badge_id: Optional[str]
  created_by: Optional[str]
  badgeclass: Optional[str]
  badgeclass_open_badge_id: Optional[str]
  issuer: Optional[str]
  issuer_open_badge_id: Optional[str]
  image: Optional[str]
  recipient: Optional[dict]
  issued_on: Optional[str]
  narrative: Optional[str]
  evidence: Optional[List[dict]]
  revoked: Optional[bool] = False
  revocation_reason: Optional[str]
  acceptance: Optional[str]
  expires: Optional[datetime]
  extensions: Optional[str]
  badgeclass_name: Optional[str]


class AssertionModel(BasicAssertionModel):
  """AssertionModel Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_ASSERTION_EXAMPLE}


class FullAssertionModel(AssertionModel):
  """Assertion Model with uuid, created and updated time"""
  uuid: str
  created_time: str
  last_modified_time: str


class AssertionResponseModel(BaseModel):
  """AssertionResponseModel Pydantic Model"""
  success: Optional[bool]
  message: Optional[str]
  data: Optional[FullAssertionModel]

  class Config():
    orm_mode = True


class AllAssertionResponseModel(BaseModel):
  """AllAssertionResponseModel Pydantic Model"""
  success: Optional[bool]
  message: Optional[str]
  data: Optional[List[FullAssertionModel]]

  class Config():
    orm_mode = True


class DeleteAssertion(BaseModel):
  """DeleteAssertion Pydantic Model"""
  success: Optional[bool]
  message: Optional[str]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully delete the Assertion"
        }
    }


class AssertionImportJsonResponse(BaseModel):
  """AssertionImportJsonResponse Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the Assertions"
  data: Optional[List[str]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success":
                True,
            "message":
                "Successfully created the assertions",
            "data": [
                "44qxEpc35pVMb6AkZGbi", "00MPqUhCbyPe1BcevQDr",
                "lQRzcrRuDpJ9IoW8bCHu"
            ]
        }
    }
