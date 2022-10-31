"""
Pydantic Model for User API's
"""
from typing import Optional
from pydantic import BaseModel

class UserModel(BaseModel):
  """User Pydantic Model"""
  user_id:str
  user_auth_id: str
  user_role: Optional[str]=None
  user_email: str


  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
        "user_id":"fake-user-id",
        "user_auth_id" : "fake-user-id",
        "user_email" : "user@gmail.com",
        "user_role" : "Admin"
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
