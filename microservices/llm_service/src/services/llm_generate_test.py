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

"""
  Unit tests for Langchain Service endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import,unused-variable,ungrouped-imports
import os
import pytest
from unittest import mock
from vertexai.preview.language_models import TextGenerationResponse
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.models import User, UserChat
from services.langchain_service_test import (FAKE_GENERATE_RESULT,
                                             FAKE_CHAT_RESULT,
                                             FAKE_GENERATE_RESPONSE)
from schemas.schema_examples import (CHAT_EXAMPLE, USER_EXAMPLE)
from services.llm_generate import llm_generate, llm_chat

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"
os.environ["OPENAI_API_KEY"] = "fake-key"
os.environ["COHERE_API_KEY"] = "fake-key"

with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  with mock.patch("langchain.chat_models.ChatOpenAI"):
    with mock.patch("langchain.llms.Cohere"):
      from config import (COHERE_LLM_TYPE,
                          OPENAI_LLM_TYPE_GPT3_5,
                          VERTEX_LLM_TYPE_BISON_TEXT,
                          VERTEX_LLM_TYPE_BISON_CHAT)

FAKE_GOOGLE_RESPONSE = TextGenerationResponse(text=FAKE_GENERATE_RESPONSE,
                                              _prediction_response={})

FAKE_PROMPT = "test prompt"

@pytest.fixture
def create_user(clean_firestore):
  user_dict = USER_EXAMPLE
  user = User.from_dict(user_dict)
  user.save()

@pytest.fixture
def test_chat(clean_firestore):
  chat_dict = CHAT_EXAMPLE
  chat = UserChat.from_dict(chat_dict)
  chat.save()
  return chat

@pytest.mark.asyncio
async def test_llm_generate(clean_firestore):
  with mock.patch("langchain.llms.Cohere.agenerate",
                  return_value = FAKE_GENERATE_RESULT):
    response = await llm_generate(FAKE_PROMPT, COHERE_LLM_TYPE)

  assert response == FAKE_GENERATE_RESPONSE

@pytest.mark.asyncio
async def test_llm_chat(clean_firestore, test_chat):
  with mock.patch("langchain.chat_models.ChatOpenAI.agenerate",
                  return_value = FAKE_CHAT_RESULT):
    response = await llm_chat(FAKE_PROMPT, OPENAI_LLM_TYPE_GPT3_5)

  assert response == FAKE_GENERATE_RESPONSE

@pytest.mark.asyncio
async def test_llm_generate_google(clean_firestore):
  with mock.patch(
      "vertexai.preview.language_models.TextGenerationModel.predict",
      return_value = FAKE_GOOGLE_RESPONSE):
    response = await llm_generate(FAKE_PROMPT, VERTEX_LLM_TYPE_BISON_TEXT)

  assert response == FAKE_GENERATE_RESPONSE

@pytest.mark.asyncio
async def test_llm_chat_google(clean_firestore, test_chat):
  with mock.patch("vertexai.preview.language_models.ChatSession.send_message",
                  return_value = FAKE_GOOGLE_RESPONSE):
    response = await llm_chat(FAKE_PROMPT, VERTEX_LLM_TYPE_BISON_CHAT)

  assert response == FAKE_GENERATE_RESPONSE
