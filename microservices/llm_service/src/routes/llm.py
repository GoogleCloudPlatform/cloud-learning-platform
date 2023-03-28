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
""" LLM endpoints """
import traceback
from typing import Required, Optional
from fastapi import APIRouter
from common.utils.logging_handler import Logger
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from schemas.llm_schema import (LLMModel, LLMGenerateResponse)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from services.json_import import json_import
from services.langchain_service import langchain_llm_generate
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES

router = APIRouter(tags=["LLMs"], responses=ERROR_RESPONSES)

# pylint: disable = broad-except

@router.post("/llm/generate", response_model=LLMGenerateResponse)
def generate(prompt: Required[str] = "", config: Optional[dict] = None):
  """
  Generate text with an LLM

  Args:
      prompt(str): Input prompt for model

  Returns:
      LLMGenerateResponse: 
  """
  result = []
  user_llm = None
  if config is not None:
    llm_type = config.get("llm_type")
    userid = config.get("userid")
    user_llm = LLMModel.find(userid, llm_type)

  if user_llm is None:
    user_llm = LLMModel(userid=userid, llm_type=llm_type)

  prompt = langchain_llm_generate(user_llm, prompt)

  if prompt:
    result = {"result": prompt}

    return {
        "success": True,
        "message": "Successfully generated text",
        "data": result
    }
  else:
    return BadRequest("Missing or invalid request parameters")

