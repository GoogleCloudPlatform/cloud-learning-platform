"""
Pydantic Model for lms job API's
"""
import datetime
from typing import Optional
from pydantic import BaseModel
from schemas.schema_examples import LMS_JOB_EXAMPLE


class LmsJobModel(BaseModel):
  """LMS job Pydantic Model

  Args:
      BaseModel (_type_): _description_
  """
  id: str
  job_type: str
  status: str
  logs: dict
  input_data: dict
  section_id: Optional[str]
  classroom_id: Optional[str]
  created_time: Optional[datetime.datetime]
  start_time: Optional[datetime.datetime]
  end_time: Optional[datetime.datetime]

  class Config():
    "Pydantic Config Class"
    orm_mode = True
    schema_extra = {"example": LMS_JOB_EXAMPLE}


class LmsJobResponseModel(BaseModel):
  """LMS job List Response model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the LMS job details"
  data: Optional[LmsJobModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the LMS job details",
            "data": [LMS_JOB_EXAMPLE]
        }
    }


class LmsJobsListResponseModel(BaseModel):
  """LMS job List Response model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the LMS job list"
  data: Optional[list[LmsJobModel]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the LMS job list",
            "data": [LMS_JOB_EXAMPLE]
        }
    }
