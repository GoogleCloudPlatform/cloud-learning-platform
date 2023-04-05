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
from typing import Optional
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
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES, OPENAI_LLM_TYPE

router = APIRouter(tags=["LLMs"], responses=ERROR_RESPONSES)

# pylint: disable = broad-except

@router.post("/llm/generate", response_model=LLMGenerateResponse)
async def generate(gen_config: LLMModel):
  """
  Generate text with an LLM

  Args:
      prompt(str): Input prompt for model

  Returns:
      LLMGenerateResponse: 
  """
  genconfig_dict = {**gen_config.dict()}

  result = []
  user_llm = None
  userid = None

  # default to openai LLM
  llm_type = OPENAI_LLM_TYPE

  prompt = genconfig_dict.get("prompt")
  llm_type = genconfig_dict.get("llm_type", OPENAI_LLM_TYPE)
  userid = genconfig_dict.get("userid")

  try:
    #if userid is not None:
    #  user_llm = LLMModel.find(userid, llm_type)

    prompt = await langchain_llm_generate(prompt, llm_type, user_llm)

    if prompt:
      result = {"result": prompt}

      return {
          "success": True,
          "message": "Successfully generated text",
          "data": result
      }
    else:
      return BadRequest("Missing or invalid request parameters")
  except Exception as e:
    raise InternalServerError(str(e)) from e
