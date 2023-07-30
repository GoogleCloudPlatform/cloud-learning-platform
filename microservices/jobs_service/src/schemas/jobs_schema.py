# Copyright 2023 Google LLC
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
Pydantic Model for Jobs Service API's
"""
from typing import List, Optional
from pydantic import BaseModel
from schemas.schema_examples import BATCHJOB_EXAMPLE

job_type = BATCHJOB_EXAMPLE["type"]

class JobGetStatusResponse(BaseModel):
  """LLM Get types model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully retrieved batch job"
  data: Optional[dict] = {}

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully retrieved batch job",
            "data": BATCHJOB_EXAMPLE
        }
    }


class AllJobsGetStatusResponse(BaseModel):
  """All Jobs Status Response model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched all the batch jobs"
  data: Optional[List[dict]] = []

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message":
      f"Successfully fetched all the batch jobs of type {job_type}",
            "data": [BATCHJOB_EXAMPLE]
        }
    }

class JobDeleteResponse(BaseModel):
  """Job Delete Response model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted job"
  data: Optional[str] = ""

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted batch job",
            "data": None
        }
    }
