"""
Pydantic Model for batch job API's
"""
from typing import Optional
from pydantic import BaseModel
from schemas.schema_examples import BATCH_JOB_EXAMPLE


class BatchJobModel(BaseModel):
  """Batch job Pydantic Model

  Args:
      BaseModel (_type_): _description_
  """
  id: str
  type: str
  status: str
  logs: dict
  input_data: dict
  section_id: Optional[str]
  classroom_id: Optional[str]

  class Config():
    "Pydantic Config Class"
    orm_mode = True
    schema_extra = {"example": BATCH_JOB_EXAMPLE}


class BatchJobsListResponseModel(BaseModel):
  """Batch job List Response model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully get the Batch job list"
  data: Optional[list[BatchJobModel]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully get the Batch job list",
            "data": [BATCH_JOB_EXAMPLE]
        }
    }
