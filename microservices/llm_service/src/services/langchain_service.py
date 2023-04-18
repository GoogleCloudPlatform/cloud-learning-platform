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

""" Langchain service """

from common.utils.errors import ResourceNotFoundException
from common.utils.http_exceptions import InternalServerError
from common.utils.logging_handler import Logger
from typing import Optional
from common.models import UserLLM
from langchain.schema import HumanMessage

from config import LANGCHAIN_LLM, CHAT_LLM_TYPES, COHERE_LLM_TYPES

async def langchain_llm_generate(prompt: str, llm_type: str,
                                 user_llm: Optional[UserLLM] = None):
  """
  Use langchain to generate text with an LLM given a prompt.  This is
    always done asychronously, and so must be used in a route defined with
    async def.

  Args:
    prompt: the text prompt to pass to the LLM

    llm_type: the type of LLM to use (default to openai)

    llm (optional): a langchain llm object to use, perhaps specific to
      a user

  Returns:
    the text result.
  """
  Logger.info(f"generating text with langchain llm_type {llm_type}")
  try:
    if user_llm is not None:
      pass
    llm = LANGCHAIN_LLM.get(llm_type)
    if llm is None:
      raise ResourceNotFoundException(f"Cannot find llm type '{llm_type}'")

    result_text = ""
    if llm_type in CHAT_LLM_TYPES:
      # use langchain chat interface for openai
      msg = [HumanMessage(content=prompt)]
      Logger.info(f"generating text for [{prompt}]")
      result = await llm.agenerate([msg])
      result_text = result.generations[0][0].message.content
      Logger.info(f"result {result.generations[0][0].message.content}")
    elif llm_type in COHERE_LLM_TYPES:
      result = llm.generate([prompt])
      result_text = result.generations[0][0].text
    else:
      # we always use await for LLM calls if we can
      result = await llm.agenerate([prompt])
      result_text = result.generations[0][0].message.content
    
    return result_text
  except Exception as e:
    raise InternalServerError(str(e)) from e
