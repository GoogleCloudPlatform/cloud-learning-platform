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

from common.models import UserChat
from common.utils.errors import ResourceNotFoundException
from common.utils.http_exceptions import InternalServerError
from common.utils.logging_handler import Logger
from services.langchain_service import langchain_llm_generate
from typing import Optional
from config import (LANGCHAIN_LLM, GOOGLE_LLM,
                    OPENAI_LLM_TYPE_GPT3_5, VERTEX_LLM_TYPE_BISON_TEXT,
                    CHAT_LLM_TYPES)
from vertexai.preview.language_models import (ChatModel,
    TextGenerationModel)

async def llm_generate(prompt: str, llm_type: str,
                       user_chat: Optional[UserChat] = None):
  """
  Generate text with an LLM given a prompt.  This is
    always done asychronously, and so must be used in a route defined with
    async def.

  Args:
    prompt: the text prompt to pass to the LLM

    llm_type: the type of LLM to use (default to openai)

    user_chat (optional): a user chat to use for context

  Returns:
    the text result.
  """
  # default to openai LLM
  if llm_type is None:
    llm_type = OPENAI_LLM_TYPE_GPT3_5

  Logger.info(f"generating text with llm_type {llm_type}")
  try:
    if llm_type in LANGCHAIN_LLM.keys():
      result = await langchain_llm_generate(prompt, llm_type, user_chat)
    elif llm_type in GOOGLE_LLM.keys():
      google_llm = GOOGLE_LLM.get(llm_type, VERTEX_LLM_TYPE_BISON_TEXT)
      is_chat = llm_type in CHAT_LLM_TYPES
      result = await google_llm_predict(prompt, is_chat, google_llm)
    else:
      raise ResourceNotFoundException(f"Cannot find llm type '{llm_type}'")

    return result
  except Exception as e:
    raise InternalServerError(str(e)) from e

async def google_llm_predict(prompt, is_chat, google_llm):
  """
  Generate text with a Google LLM given a prompt.

  Args:
    prompt: the text prompt to pass to the LLM
    is_chat: true if the model is a chat model
    google_llm: name of the vertex llm model

  Returns:
    the text result.
  """

  # Temperature controls the degree of randomness in token selection.
  # Token limit determines the maximum amount of text output.
  # Tokens are selected from most probable to least until the sum of
  #  their probabilities equals the top_p value.
  # top_k of 1 means the selected token is the most probable among all tokens.

  parameters = {
    "temperature": 0.2,
    "max_output_tokens": 1024,
    "top_p": 0.95,
    "top_k": 40,
  }

  try:
    if is_chat:
      chat_model = ChatModel.from_pretrained(google_llm)
      chat = chat_model.start_chat()
      response = chat.send_message(prompt, **parameters)
    else:
      text_model = TextGenerationModel.from_pretrained(google_llm)
      response = text_model.predict(
          prompt,
          **parameters,
      )

  except Exception as e:
    raise InternalServerError(str(e)) from e

  Logger.info(f"Response from Model: {response.text}")
  result = response.text

  return result
