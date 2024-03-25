"""
Pydantic Model for CSV upload from Google Cloud Storage
"""
from typing import Optional
from pydantic import BaseModel


class GCSBucketInfoModel(BaseModel):
  """GCS Bucket blob Pydantic Model"""
  competency_uri: Optional[str] = None
  skill_uri: Optional[str] = None

  class Config():
    schema_extra = {
        "example": {
            "competency_uri":
                "gs://bucket-name/path-to-competency-file-name.csv",
            "skill_uri":
                "gs://bucket-name/path-to-skill-file-name.csv"
        }
    }
