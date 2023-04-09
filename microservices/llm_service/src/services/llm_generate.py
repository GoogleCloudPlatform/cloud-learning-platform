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

""" LLM Generation Service """

from common.models import UserLLM
from common.utils.errors import ResourceNotFoundException
from common.utils.http_exceptions import InternalServerError
from common.utils.logging_handler import Logger
from services.langchain_service import langchain_llm_generate
from typing import Optional

from config import LANGCHAIN_LLM, GOOGLE_LLM, OPENAI_LLM_TYPE_GPT3_5

async def llm_generate(prompt: str, llm_type: str,
                       user_llm: Optional[UserLLM] = None):
  """
  Generate text with an LLM given a prompt.  This is 
    always done asychronously, and so must be used in a route defined with 
    async def.

  Args:
    prompt: the text prompt to pass to the LLM

    llm_type: the type of LLM to use (default to openai)

    llm (optional): an user llm model

  Returns:
    the text result.
  """
  # default to openai LLM
  if llm_type is None:
    llm_type = OPENAI_LLM_TYPE_GPT3_5

  Logger.info(f"generating text with llm_type {llm_type}")
  try:
    if llm_type in LANGCHAIN_LLM.keys():
      result = await langchain_llm_generate(prompt, llm_type, user_llm)
    elif llm_type in GOOGLE_LLM.keys():
      google_llm = GOOGLE_LLM.get(llm_type)
      result = await google_llm.predict(prompt)
    else:
      raise ResourceNotFoundException(f"Cannot find llm type '{llm_type}'")

    return result
  except Exception as e:
    raise InternalServerError(str(e)) from e
