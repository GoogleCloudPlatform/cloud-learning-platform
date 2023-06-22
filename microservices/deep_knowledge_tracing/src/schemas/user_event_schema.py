"""
  Pydantic schemas for Bulk Upload API's
"""
from pydantic import BaseModel

class BulkUploadResponse(BaseModel):
  success: bool
  message: str
  num_user_events: int
  course_ids: list

  class Config:
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the user events",
            "num_user_events": 100,
            "course_ids": ["sadasasfa", "afafasfas"]
        }
    }

class DeleteResponse(BaseModel):
  success: bool
  message: str
  deleted_user_events: list

  class Config:
    orm_mode = True
    schema_extra={
      "example": {
        "success": True,
        "message": "Successfully deleted the user events",
        "deleted_user_events" : ["uuid1", "uuid2"]
      }
    }

class SyntheticDataCreate(BaseModel):
  success: bool
  message: str
  gcs_path: str

  class Config:
    orm_mode = True
    schema_extra={
      "example": {
        "success": True,
        "message": "Successfully created the synthetic data in a csv",
        "gcs_path" : "gs:bucket_name/file_name.csv"
      }
    }
