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
from common.models import UserLLM
from common.utils.logging_handler import Logger
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from schemas.llm_schema import (LLMGenerateModel, UserLLMModel, LLMGenerateResponse)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from services.json_import import json_import
from services.langchain_service import langchain_llm_generate
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES, OPENAI_LLM_TYPE

router = APIRouter(prefix="/llm", tags=["LLMs"], responses=ERROR_RESPONSES)

# pylint: disable = broad-except

@router.post("/generate", response_model=LLMGenerateResponse)
async def generate(gen_config: LLMGenerateModel):
  """
  Generate text with an LLM

  Args:
      prompt(str): Input prompt for model

  Returns:
      LLMGenerateResponse: 
  """
  genconfig_dict = {**gen_config.dict()}

  prompt = genconfig_dict.get("prompt")

  # default to openai LLM
  llm_type = genconfig_dict.get("llm_type")
  if llm_type is None:
    llm_type = OPENAI_LLM_TYPE

  try:
    if prompt is not None:
      result = await langchain_llm_generate(prompt, llm_type)      

      return {
          "success": True,
          "message": "Successfully generated text",
          "content": result
      }
    else:
      return BadRequest("Missing or invalid payload parameters")
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post("/{userid}/generate", response_model=LLMGenerateResponse)
async def generate_user(userid: str, gen_config: UserLLMModel):
  """
  Generate text with an user specific LLM

  Args:
      prompt(str): Input prompt for model

  Returns:
      LLMGenerateResponse: 
  """
  genconfig_dict = {**gen_config.dict()}

  result = []
  user_llm = None

  prompt = genconfig_dict.get("prompt")

  # default to openai LLM
  llm_type = genconfig_dict.get("llm_type", OPENAI_LLM_TYPE)

  try:
    user_llm = UserLLM.find_by_userid(userid, llm_type)
    if user_llm is None:
      raise ResourceNotFoundException(f"LLM not found for {userid}")

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
