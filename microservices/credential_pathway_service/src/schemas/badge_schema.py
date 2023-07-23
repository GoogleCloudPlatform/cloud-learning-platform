"""
Pydantic models for BadgeClass
"""
from pydantic import BaseModel
from typing import Optional, List
from typing_extensions import Literal
from schemas.schema_examples import BASIC_BADGE_EXAMPLE

# pylint: disable=invalid-name
ALLOWED_ACHIEVEMENT_TYPES = Literal["Achievement", "Assessment", "Assignment",
                                    "Award", "Badge", "Certificate",
                                    "Certification", "Course",
                                    "CommunityService", "Competency",
                                    "Co-Curricular", "Degree", "Diploma",
                                    "Fieldwork", "License", "Membership"]


class BasicBadgeModel(BaseModel):
  """Basic Badge Pydantic Model"""
  entity_type: str
  entity_id: str
  open_badge_id: str
  created_by: Optional[str]
  issuer: Optional[str]
  issuer_open_badge_id: Optional[str]
  name: Optional[str]
  image: Optional[str]
  description: Optional[str]
  achievement_type: Optional[ALLOWED_ACHIEVEMENT_TYPES]
  criteria_url: Optional[str]
  criteria_narrative: Optional[str]
  alignments: Optional[dict]
  tags: Optional[List[str]] = []
  expires: Optional[dict]
  extensions: Optional[str]


class BadgeModel(BasicBadgeModel):
  """Badge Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_BADGE_EXAMPLE}


class FullBadgeModel(BasicBadgeModel):
  """Badge Model with uuid, created and updated time"""
  uuid: str
  created_time: str
  last_modified_time: str


class BadgeResponseModel(BaseModel):
  """BadgeResponse Pydantic Model"""
  success: Optional[bool]
  message: Optional[str]
  data: Optional[FullBadgeModel]

  class Config():
    orm_mode = True


class AllBadgeResponseModel(BaseModel):
  """AllBadgeResponse Pydantic Model"""
  success: Optional[bool]
  message: Optional[str]
  data: Optional[List[FullBadgeModel]]

  class Config():
    orm_mode = True


class DeleteBadge(BaseModel):
  """DeleteBadge Pydantic Model"""
  success: Optional[bool]
  message: Optional[str]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully delete the badge"
        }
    }


class BadgeImportJsonResponse(BaseModel):
  """BadgeImportJsonResponse Pydantic Model"""
  success: Optional[bool]
  message: Optional[str]
  data: Optional[List[str]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success":
                True,
            "message":
                "Successfully created the badges",
            "data": [
                "44qxEpc35pVMb6AkZGbi", "00MPqUhCbyPe1BcevQDr",
                "lQRzcrRuDpJ9IoW8bCHu"
            ]
        }
    }
