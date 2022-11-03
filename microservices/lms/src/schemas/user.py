"""
Pydantic Model for User API's
"""
from typing import Optional
from pydantic import BaseModel

class UserModel(BaseModel):
  """User Pydantic Model"""
  uuid:Optional[str]=None
  auth_id: str
  email: str
  role: Optional[str]=None


  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
        "uuid":"fake-user-id",
        "auth_id" : "fake-user-id",
        "email" : "user@gmail.com",
        "role" : "Admin"
      }
    }


class GcsBucketInfoModel(BaseModel):
  """Gcs Bucket blob Pydantic Model"""
  bucket_name: str
  file_name: str

  class Config():
    schema_extra = {
        "example": {
            "bucket_name": "client-users-data",
            "file_name": "all-users.csv"
        }
    }
