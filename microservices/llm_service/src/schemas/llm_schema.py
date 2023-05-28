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
Pydantic Model for LLM API's
"""
from typing import List, Optional
from pydantic import BaseModel
from schemas.schema_examples import LLM_GENERATE_EXAMPLE

class ChatModel(BaseModel):
  id: str
  user_id: str
  llm_type: str
  history: List[str] = []
  created_time: str
  last_modified_time: str

class LLMGetTypesResponse(BaseModel):
  """LLM Get types model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully retrieved llm types"
  data: Optional[list[str]] = []

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully retrieved llm types",
            "data": []
        }
    }

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

class LLMUserChatResponse(BaseModel):
  """LLM User Create Chat Response model"""
  chatid: str
  success: Optional[bool] = True
  message: Optional[str] = "Successfully generated text"
  content: Optional[str] = ""

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully generated text",
            "content": None,
            "chatid": None
        }
    }

class LLMUserAllChatsResponse(BaseModel):
  """LLM Get User All Chats Response model"""
  data: List[ChatModel] = []
  success: Optional[bool] = True
  message: Optional[str] = "Successfully retrieved user chats"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully generated text",
            "data": None
        }
    }
