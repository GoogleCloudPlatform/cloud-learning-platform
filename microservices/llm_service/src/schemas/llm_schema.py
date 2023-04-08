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
Pydantic Model for Grade API's
"""
from typing import Optional
from pydantic import BaseModel
from schemas.schema_examples import LLM_GENERATE_EXAMPLE, USER_LLM_MODEL_EXAMPLE

class LLMGenerateModel(BaseModel):
  """LLM Generate model"""
  prompt: str
  llm_type: Optional[str] = None
  context: Optional[str] = ""
  primer: Optional[list[str]] = []

  class Config():
    orm_mode = True
    schema_extra = {
        "example": LLM_GENERATE_EXAMPLE
    }


class UserLLMModel(BaseModel):
  """User LLM model"""
  prompt: str
  llm_type: Optional[str] = ""
  context: Optional[str] = ""
  primer: Optional[list[str]] = []
  history: Optional[list[str]] = []
  memory: Optional[str] = ""

  class Config():
    orm_mode = True
    schema_extra = {
        "example": USER_LLM_MODEL_EXAMPLE
    }

class LLMGenerateResponse(BaseModel):
  """LLM Generate Response model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully generated text"
  content: Optional[str] = ""

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully generated text",
            "content": None
        }
    }
