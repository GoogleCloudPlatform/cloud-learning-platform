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
Pydantic Models for Batch Job API's
"""
from typing import Optional
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
