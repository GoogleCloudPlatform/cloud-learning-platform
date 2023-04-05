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

from common.utils.http_exceptions import InternalServerError
from typing import Optional
from langchain.llms.base import LLM
from config import LANGCHAIN_LLM, OPENAI_LLM_TYPE

async def langchain_llm_generate(prompt: str, llm_type: str,
                                 llm: Optional[LLM] = None):
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
  try:
    if llm is None:
      llm = LANGCHAIN_LLM.get(llm_type, OPENAI_LLM_TYPE)

    # we always use await for LLM calls
    result = await llm.agenerate(prompt)

    return result
  except Exception as e:
    raise InternalServerError(str(e)) from e
