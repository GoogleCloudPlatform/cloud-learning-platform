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
from common.models import User, UserChat
from common.utils.auth_service import validate_token
from common.utils.logging_handler import Logger
from common.utils.errors import (ResourceNotFoundException,
                                 ValidationError,
                                 PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from schemas.llm_schema import (ChatModel, ChatUpdateModel,
                                LLMGenerateModel,
                                LLMGenerateResponse,
                                LLMUserChatResponse,
                                LLMUserAllChatsResponse)
from services.llm_generate import llm_chat
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES, LLM_TYPES

router = APIRouter(prefix="/chat", tags=["LLMs"], responses=ERROR_RESPONSES)


@router.get(
    "",
    name="Get all user chats",
    response_model=LLMUserAllChatsResponse)
def get_chat_list(skip: int = 0, limit: int = 20,
                  user_data: dict = Depends(validate_token)):
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

    user = User.find_by_email(user_data.get("email"))
    user_chats = UserChat.find_by_user(user.user_id)

    chat_list = []
    for i in user_chats:
      chat_data = i.get_fields(reformat_datetime=True)
      chat_data["id"] = i.id
      # don't inculde chat history to slim return payload
      del chat_data["history"]
      chat_list.append(chat_data)

    return {
      "success": True,
      "message": f"Successfully retrieved user chats for user {user.user_id}",
      "data": chat_list
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/{chat_id}",
    name="Get user chat",
    response_model=LLMUserChatResponse)
def get_chat(chat_id: str):
  """
  Get a specific user chat by id

  Returns:
      LLMUserChatResponse
  """
  try:
    user_chat = UserChat.find_by_id(chat_id)
    chat_data = user_chat.get_fields(reformat_datetime=True)
    chat_data["id"] = user_chat.id

    return {
      "success": True,
      "message": f"Successfully retrieved user chat {chat_id}",
      "data": chat_data
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
  "/{chat_id}",
  name="Update user chat"
)
def update_chat(chat_id: str, input_chat: ChatUpdateModel):
  """Update a user chat

  Args:
    input_chat (ChatUpdateModel): fields in body of chat to update.
      The only field that can be updated is the title.

  Raises:
    ResourceNotFoundException: If the Chat does not exist
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: {'success': 'True'} if the chat is updated,
    NotFoundErrorResponseModel if the chat not found,
    InternalServerErrorResponseModel if the chat update raises an exception
  """
  try:
    input_chat_dict = {**input_chat.dict()}

    existing_chat = UserChat.find_by_id(chat_id)
    for key in input_chat_dict:
      if input_chat_dict.get(key) is not None:
        setattr(existing_chat, key, input_chat_dict.get(key))
    existing_chat.update()

    return {
      "success": True,
      "message": f"Successfully updated user chat {chat_id}",
    }
  except ResourceNotFoundException as re:
    raise ResourceNotFound(str(re)) from re
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.delete(
  "/{chat_id}",
  name="Delete user chat"
)
def delete_chat(chat_id: str):
  """Delete a user chat.

  Args:
    chat_id: id of user chat to delete.  We do a soft delete.

  Raises:
    ResourceNotFoundException: If the Chat does not exist
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: {'success': 'True'} if the chat is deleted,
    NotFoundErrorResponseModel if the chat not found,
    InternalServerErrorResponseModel if the chat deletion raises an exception
  """
  try:
    UserChat.soft_delete_by_id(chat_id)

    return {
      "success": True,
      "message": f"Successfully deleted user chat {chat_id}",
    }
  except ResourceNotFoundException as re:
    raise ResourceNotFound(str(re)) from re
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.post(
    "",
    name="Create new chat",
    response_model=LLMUserChatResponse)
async def create_user_chat(gen_config: LLMGenerateModel,
                           user_data: dict = Depends(validate_token)):
  """
  Create new chat for authentcated user

  Args:
      prompt(str): Input prompt for model
      llm_type(str): LLM type

  Returns:
      LLMUserChatResponse
  """
  genconfig_dict = {**gen_config.dict()}

  response = []

  prompt = genconfig_dict.get("prompt")
  if prompt is None or prompt == "":
    return BadRequest("Missing or invalid payload parameters")

  llm_type = genconfig_dict.get("llm_type")

  try:
    user = User.find_by_email(user_data.get("email"))

    # generate text from prompt
    response = await llm_chat(prompt, llm_type)

    # create new chat for user
    user_chat = UserChat(user_id=user.user_id, llm_type=llm_type)
    history = UserChat.get_history_entry(prompt, response)
    user_chat.history = history
    user_chat.save()

    chat_data = user_chat.get_fields(reformat_datetime=True)
    chat_data["id"] = user_chat.id

    return {
        "success": True,
        "message": "Successfully created chat",
        "data": chat_data
    }
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/{chat_id}/generate",
    name="Generate new chat response",
    response_model=LLMUserChatResponse)
async def user_chat_generate(chat_id: str, gen_config: LLMGenerateModel):
  """
  Continue chat based on context of user chat

  Args:
      prompt(str): Input prompt for model

  Returns:
      LLMUserChatResponse
  """
  genconfig_dict = {**gen_config.dict()}

  response = []

  prompt = genconfig_dict.get("prompt")
  if prompt is None or prompt == "":
    return BadRequest("Missing or invalid payload parameters")

  # fetch user chat
  user_chat = UserChat.find_by_id(chat_id)
  if user_chat is None:
    raise ResourceNotFoundException(f"Chat {chat_id} not found ")
  llm_type = user_chat.llm_type

  try:
    response = await llm_chat(prompt, llm_type, user_chat)

    # save chat history
    user_chat.update_history(prompt, response)

    chat_data = user_chat.get_fields(reformat_datetime=True)
    chat_data["id"] = user_chat.id

    return {
        "success": True,
        "message": "Successfully generated text",
        "data": chat_data
    }
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
