"""
Pydantic Model for Prior Experience API's
"""
from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel
from schemas.schema_examples import (BASIC_PRIOR_EXPERIENCE_MODEL_EXAMPLE,
                                     FULL_PRIOR_EXPERIENCE_MODEL_EXAMPLE)


class CourseModel(BaseModel):
  """Course Skeleton Pydantic Model"""
  course_title: str
  course_code: str
  credits: str
  grade: str


class EndDateModel(BaseModel):
  """EndDate Skeleton Pydantic Model"""
  year: str
  month: str
  day: str


class TermModel(BaseModel):
  """Term Skeleton Pydantic Model"""
  end_date: EndDateModel
  transfer_courses: List[CourseModel]


class BasicPriorExperienceModel(BaseModel):
  """PriorExperience Skeleton Pydantic Model"""
  organization: Optional[str]
  experience_title: Optional[str]
  date_completed: Optional[datetime]
  credits_earned: Optional[int]
  description: Optional[str]
  url: Optional[str]
  competencies: Optional[List[str]]
  skills: Optional[List[str]]
  documents: Optional[List[str]]
  cpl: Optional[int]
  is_flagged: Optional[bool] = False
  metadata: Optional[dict] = {}
  alignments: Optional[dict] = {}
  type_of_experience: Optional[str]
  validation_type: Optional[Dict[str, str]]
  terms: Optional[List[TermModel]]


class PriorExperienceModel(BasicPriorExperienceModel):
  """PriorExperience Input Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_PRIOR_EXPERIENCE_MODEL_EXAMPLE}


class UpdatePriorExperienceModel(BasicPriorExperienceModel):
  """Update PriorExperience Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_PRIOR_EXPERIENCE_MODEL_EXAMPLE}


class FullPriorExperienceDataModel(BasicPriorExperienceModel):
  """PriorExperience Skeleton Model with uuid, created and updated time"""
  uuid: str
  created_time: str
  last_modified_time: str


class GetPriorExperienceResponseModel(BaseModel):
  """PriorExperience Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the prior experience"
  data: Optional[FullPriorExperienceDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the prior experience",
            "data": FULL_PRIOR_EXPERIENCE_MODEL_EXAMPLE
        }
    }

class TotalCountResponseModel(BaseModel):
  records: Optional[List[FullPriorExperienceDataModel]]
  total_count: int

class AllPriorExperienceResponseModel(BaseModel):
  """PriorExperience Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the prior experiences"
  data: Optional[TotalCountResponseModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the prior experiences",
            "data": {
                      "records":[FULL_PRIOR_EXPERIENCE_MODEL_EXAMPLE],
                      "total_count": 50
                    }
        }
    }


class PostPriorExperienceResponseModel(BaseModel):
  """PriorExperience Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the prior experience"
  data: Optional[FullPriorExperienceDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the prior experience",
            "data": FULL_PRIOR_EXPERIENCE_MODEL_EXAMPLE
        }
    }


class UpdatePriorExperienceResponseModel(BaseModel):
  """PriorExperience Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the prior experience"
  data: Optional[FullPriorExperienceDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully updated the prior experience",
        "data": FULL_PRIOR_EXPERIENCE_MODEL_EXAMPLE
      }
    }


class DeletePriorExperienceModel(BaseModel):
  """Delete PriorExperience Pydantic Model"""
  success: bool = True
  message: str = "Successfully deleted the prior experience"

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully deleted the prior experience"
      }
    }


class PriorExperienceImportJsonResponse(BaseModel):
  """PriorExperience Import Json Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the prior experiences"
  data: Optional[List[str]]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully created the prior experiences",
        "data": [
          "44qxEpc35pVMb6AkZGbi",
          "00MPqUhCbyPe1BcevQDr",
          "lQRzcrRuDpJ9IoW8bCHu"
        ]
      }
    }
