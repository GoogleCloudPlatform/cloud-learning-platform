"""
Pydantic Models for Batch Job API's
"""
from typing import Optional, List
from pydantic import BaseModel


# pylint: disable = line-too-long
class Data(BaseModel):
  job_name: Optional[str]
  status: Optional[str]


class BatchJobModel(BaseModel):
  """Batch Job Response Pydantic Model"""
  success: bool
  message: str
  data: Optional[Data]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully initiated the job with type 'emsi_ingestion'. Please use the job name to track the job status",
            "data": {
                "job_name": "abcd-ajdf-sdfk-sdff",
                "status": "active"
            }
        }
    }
