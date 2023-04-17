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

# pylint: disable = broad-except,unused-import

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
from schemas.llm_schema import (LLMGenerateModel, UserLLMModel,
                                LLMGetResponse, LLMGenerateResponse)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from services.llm_generate import llm_generate
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES, LLM_TYPES

router = APIRouter(prefix="/llm", tags=["LLMs"], responses=ERROR_RESPONSES)


@router.get("", response_model=LLMGetResponse)
def get_llm_list():
  """
  Get available LLMs

  Returns:
      LLMGetResponse
  """
  try:
    return {
      "success": True,
      "message": "Successfully retrieved llm types",
      "data": LLM_TYPES
    }
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post("/generate", response_model=LLMGenerateResponse)
async def generate(gen_config: LLMGenerateModel):
  """
  Generate text with an LLM

  Args:
      prompt(str): Input prompt for model

  Returns:
      LLMGenerateResponse
  """
  genconfig_dict = {**gen_config.dict()}

  prompt = genconfig_dict.get("prompt")
  if prompt is None or prompt == "":
    return BadRequest("Missing or invalid payload parameters")

  llm_type = genconfig_dict.get("llm_type")

  try:
    result = await llm_generate(prompt, llm_type)

    return {
        "success": True,
        "message": "Successfully generated text",
        "content": result
    }
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post("/{userid}/generate", response_model=LLMGenerateResponse)
async def generate_user(userid: str, gen_config: UserLLMModel):
  """
  Generate text and track history for user

  Args:
      prompt(str): Input prompt for model

  Returns:
      LLMGenerateResponse
  """
  genconfig_dict = {**gen_config.dict()}

  result = []
  user_llm = None

  prompt = genconfig_dict.get("prompt")
  if prompt is None or prompt == "":
    return BadRequest("Missing or invalid payload parameters")

  llm_type = genconfig_dict.get("llm_type")

  user_llm = UserLLM.find_by_userid(userid, llm_type)
  if user_llm is None:
    raise ResourceNotFoundException(f"LLM not found for {userid}")

  try:
    result = await llm_generate(prompt, llm_type, user_llm)

    return {
        "success": True,
        "message": "Successfully generated text",
        "content": result
    }
  except Exception as e:
    raise InternalServerError(str(e)) from e
