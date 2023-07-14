"""
Pydantic Model for Approved Experience API's
"""
from typing import List, Optional
from pydantic import BaseModel
from schemas.schema_examples import (BASIC_APPROVED_EXPERIENCE_MODEL_EXAMPLE,
                                     FULL_APPROVED_EXPERIENCE_MODEL_EXAMPLE)
from config import EXPERIENCE_TYPES, STUDENT_TYPES, CLASS_LEVEL, STATUS_AP


class BasicApprovedExperienceModel(BaseModel):
  """ApprovedExperience Skeleton Pydantic Model"""
  organization: Optional[str]
  title: Optional[str]
  description: Optional[str]
  type: Optional[EXPERIENCE_TYPES]
  student_type: Optional[STUDENT_TYPES]
  class_level: Optional[CLASS_LEVEL]
  credits_range: Optional[dict] = {}
  status: Optional[STATUS_AP]
  metadata: Optional[dict] = {}


class ApprovedExperienceModel(BasicApprovedExperienceModel):
  """ApprovedExperience Input Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_APPROVED_EXPERIENCE_MODEL_EXAMPLE}


class UpdateApprovedExperienceModel(BasicApprovedExperienceModel):
  """Update ApprovedExperience Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_APPROVED_EXPERIENCE_MODEL_EXAMPLE}


class FullApprovedExperienceDataModel(BasicApprovedExperienceModel):
  """ApprovedExperience Skeleton Model with uuid, created and updated time"""
  uuid: str
  created_time: str
  last_modified_time: str


class GetApprovedExperienceResponseModel(BaseModel):
  """ApprovedExperience Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the approved experience"
  data: Optional[FullApprovedExperienceDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the approved experience",
            "data": FULL_APPROVED_EXPERIENCE_MODEL_EXAMPLE
        }
    }

class TotalCountResponseModel(BaseModel):
  records: Optional[List[FullApprovedExperienceDataModel]]
  total_count: int

class AllApprovedExperienceResponseModel(BaseModel):
  """ApprovedExperience Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the approved experiences"
  data: Optional[TotalCountResponseModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the approved experiences",
            "data": {
                      "records":[FULL_APPROVED_EXPERIENCE_MODEL_EXAMPLE],
                      "total_count": 50
                    }
        }
    }


class PostApprovedExperienceResponseModel(BaseModel):
  """ApprovedExperience Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the approved experience"
  data: Optional[FullApprovedExperienceDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the approved experience",
            "data": FULL_APPROVED_EXPERIENCE_MODEL_EXAMPLE
        }
    }


class UpdateApprovedExperienceResponseModel(BaseModel):
  """ApprovedExperience Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the approved experience"
  data: Optional[FullApprovedExperienceDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully updated the approved experience",
        "data": FULL_APPROVED_EXPERIENCE_MODEL_EXAMPLE
      }
    }


class DeleteApprovedExperienceModel(BaseModel):
  """Delete ApprovedExperience Pydantic Model"""
  success: bool = True
  message: str = "Successfully deleted the approved experience"

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully deleted the approved experience"
      }
    }


class ApprovedExperienceImportJsonResponse(BaseModel):
  """ApprovedExperience Import Json Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the approved experiences"
  data: Optional[List[str]]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully created the approved experiences",
        "data": [
          "44qxEpc35pVMb6AkZGbi",
          "00MPqUhCbyPe1BcevQDr",
          "lQRzcrRuDpJ9IoW8bCHu"
        ]
      }
    }

class AllApprovedOrganisationResponseModel(BaseModel):
  """ApprovedOgranisations Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the unique list of\
    approved organisation"
  data: Optional[List[str]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message":\
              "Successfully fetched the unique list of approved organisation",
            "data": ["org1", "org2", "org3", "org4"]
        }
    }
