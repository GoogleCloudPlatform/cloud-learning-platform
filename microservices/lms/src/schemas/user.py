# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Pydantic Model for User API's
"""
from typing import Optional
from pydantic import BaseModel
from schemas.schema_examples import USER_EXAMPLE

class UserModel(BaseModel):
  """User Pydantic Model"""
  uuid:Optional[str]=None
  auth_id: str
  email: str
  role: Optional[str]=None


  class Config():
    orm_mode = True
    schema_extra = {
        "example": USER_EXAMPLE
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
