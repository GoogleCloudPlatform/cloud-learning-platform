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
from fastapi import APIRouter, Depends
from common.models import UserChat
from common.utils.auth_service import validate_token, get_user_data
from common.utils.logging_handler import Logger
from common.utils.errors import (ResourceNotFoundException,
                                 ValidationError,
                                 PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from schemas.llm_schema import (LLMGenerateModel, LLMGetTypesResponse,
                                LLMGenerateResponse,
                                LLMUserChatResponse,
                                LLMUserAllChatsResponse)
from services.llm_generate import llm_generate
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES, LLM_TYPES, auth_client

router = APIRouter(prefix="/llm", tags=["LLMs"], responses=ERROR_RESPONSES)


@router.get(
    "",
    name="Get all LLM types",
    response_model=LLMGetTypesResponse)
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
    "/chat",
    name="Get all user chats",
    response_model=LLMUserAllChatsResponse)
def get_chat_list(skip: int = 0, limit: int = 20,
                  user_details: dict = Depends(validate_token)):
  """
  Get user chats for authenticated user.  Chat data does not include
  chat history to slim payload.  To retrieve chat history use the
  get single chat endpoint.

  Args:
    skip: `int`
      Number of tools to be skipped <br/>
    limit: `int`
      Size of tools array to be returned <br/>

  Returns:
      LLMUserAllChatsResponse
  """
  try:
    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")

    if limit < 1:
      raise ValidationError("Invalid value passed to \"limit\" query parameter")

    user_data = get_user_data(user_details, auth_client)
    userid = user_data.get("user_id")
    user_chats = UserChat.find_by_user(userid)

    chat_list = []
    for i in user_chats:
      chat_data = i.get_fields(reformat_datetime=True)
      chat_data["id"] = i.id
      # don't inculde chat history to slim return payload
      del chat_data["history"]
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


@router.get(
    "/chat/{chatid}",
    name="Get user chat",
    response_model=LLMUserChatResponse)
def get_chat(chatid: str):
  """
  Get a specific user chat by id

  Returns:
      LLMUserChatResponse
  """
  try:
    user_chat = UserChat.find_by_id(chatid)
    chat_data = user_chat.get_fields(reformat_datetime=True)
    chat_data["id"] = user_chat.id

    return {
      "success": True,
      "message": f"Successfully retrieved user chat {chatid}",
      "data": chat_data
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
    "/chat",
    name="Create new chat",
    response_model=LLMUserChatResponse)
async def create_user_chat(gen_config: LLMGenerateModel,
                           user_details: dict = Depends(validate_token)):
  """
  Create new chat for authentcated user

  Args:
      prompt(str): Input prompt for model
      llm_type(str): LLM type

  Returns:
      LLMUserChatResponse
  """
  genconfig_dict = {**gen_config.dict()}

  result = []

  prompt = genconfig_dict.get("prompt")
  if prompt is None or prompt == "":
    return BadRequest("Missing or invalid payload parameters")

  llm_type = genconfig_dict.get("llm_type")

  try:
    user_data = get_user_data(user_details, auth_client)
    userid = user_data.get("user_id")

    # generate text from prompt
    result = await llm_generate(prompt, llm_type)

    # create new chat for user
    user_chat = UserChat(user_id=userid, llm_type=llm_type)
    user_chat.history = [prompt, result]
    user_chat.save()

    chat_data = user_chat.get_fields(reformat_datetime=True)
    chat_data["id"] = user_chat.id

    return {
        "success": True,
        "message": "Successfully created chat",
        "chat": chat_data
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
    user_chat.history.append(prompt)
    user_chat.history.append(result)
    user_chat.save()

    return {
        "success": True,
        "message": "Successfully generated text",
        "content": result
    }
  except Exception as e:
    raise InternalServerError(str(e)) from e
