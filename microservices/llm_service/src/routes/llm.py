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
from common.models import UserChat
from common.utils.logging_handler import Logger
from common.utils.errors import (ResourceNotFoundException,
                                 ValidationError,
                                 PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from schemas.llm_schema import (LLMGenerateModel, UserLLMModel,
                                LLMGetResponse, LLMGenerateResponse,
                                LLMUserGenerateResponse,
                                LLMGetUserChatResponse)
from services.llm_generate import llm_generate
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES, LLM_TYPES

router = APIRouter(prefix="/llm", tags=["LLMs"], responses=ERROR_RESPONSES)


@router.get(
    "",
    name="Get all LLM types",
    response_model=LLMGetResponse)
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


@router.get(
    "/user/{userid}/chat",
    name="Get all user chats",
    response_model=LLMGetUserChatResponse)
def get_chat_list(userid: str, skip: int = 0, limit: int = 20):
  """
  Get user chats

  Args:
    skip: `int`
      Number of tools to be skipped <br/>
    limit: `int`
      Size of tools array to be returned <br/>

  Returns:
      LLMGetUserChatResponse
  """
  try:
    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")

    if limit < 1:
      raise ValidationError("Invalid value passed to \"limit\" query parameter")

    user_chats = UserChat.find_by_user(userid)

    chat_list = []
    for i in user_chats:
      chat_data = i.get_fields(reformat_datetime=True)
      chat_data["id"] = i.id
      chat_list.append(chat_data)

    return {
      "success": True,
      "message": f"Successfully retrieved user chats for user {userid}",
      "data": chat_list
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/generate",
    name="Generate text from LLM",
    response_model=LLMGenerateResponse)
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

  if len(prompt) > PAYLOAD_FILE_SIZE:
    return PayloadTooLargeError(
      f"Prompt must be less than {PAYLOAD_FILE_SIZE}")

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


@router.post(
    "/user/{userid}/chat",
    name="Create new chat",
    response_model=LLMGenerateResponse)
async def create_user_chat(userid: str, gen_config: LLMGenerateModel):
  """
  Create new chat for user with text response

  Args:
      prompt(str): Input prompt for model
      llm_type(str): LLM type

  Returns:
      LLMUserGenerateResponse
  """
  genconfig_dict = {**gen_config.dict()}

  result = []

  prompt = genconfig_dict.get("prompt")
  if prompt is None or prompt == "":
    return BadRequest("Missing or invalid payload parameters")

  llm_type = genconfig_dict.get("llm_type")

  try:
    # generate text from prompt
    result = await llm_generate(prompt, llm_type)

    # create new chat for user
    user_chat = UserChat(userid=userid, llm_type=llm_type)
    user_chat.history = [result]
    user_chat.save()

    return {
        "success": True,
        "message": "Successfully generated text",
        "content": result,
        "chatid": user_chat.id
    }
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/chat/{chatid}/generate",
    name="Generate new chat response",
    response_model=LLMGenerateResponse)
async def user_chat_generate(chatid: str, gen_config: LLMGenerateModel):
  """
  Continue chat based on context of user chat

  Args:
      prompt(str): Input prompt for model
      llm_type(str): LLM type

  Returns:
      LLMUserGenerateResponse
  """
  genconfig_dict = {**gen_config.dict()}

  result = []

  prompt = genconfig_dict.get("prompt")
  if prompt is None or prompt == "":
    return BadRequest("Missing or invalid payload parameters")

  llm_type = genconfig_dict.get("llm_type")

  # fetch user chat
  user_chat = UserChat.find_by_id(chatid)
  if user_chat is None:
    raise ResourceNotFoundException(f"Chat {chatid} not found ")

  try:
    result = await llm_generate(prompt, llm_type, user_chat)

    # save chat history
    user_chat.history.append(result)
    user_chat.save()

    return {
        "success": True,
        "message": "Successfully generated text",
        "content": result
    }
  except Exception as e:
    raise InternalServerError(str(e)) from e
