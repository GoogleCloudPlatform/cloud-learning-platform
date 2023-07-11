"""
Pydantic Model for Upload API
"""
from typing import List, Optional
from pydantic import BaseModel

class UploadResponseModel(BaseModel):
  """Upload Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully uploaded the transcripts"
  data: Optional[List[str]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully uploaded the transcripts",
            "data": [
              "gs://gcp-project/pla/user-transcripts/course1.pdf",
              "gs://gcp-project/pla/user-transcripts/course2.jpeg"
            ]
        }
    }
