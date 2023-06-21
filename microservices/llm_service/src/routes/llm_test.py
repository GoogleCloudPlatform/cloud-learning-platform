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
  Unit tests for LLM Service endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import,unused-variable,ungrouped-imports
import os
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest import mock
from testing.test_config import API_URL, TESTING_FOLDER_PATH
from schemas.schema_examples import (LLM_GENERATE_EXAMPLE, CHAT_EXAMPLE,
                                     USER_EXAMPLE)
from common.models import UserChat, User
from common.utils.http_exceptions import add_exception_handlers
with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  with mock.patch("langchain.chat_models.ChatOpenAI"):
    with mock.patch("langchain.llms.Cohere"):
      from common.testing.client_with_emulator import client_with_emulator
from common.testing.firestore_emulator import firestore_emulator, clean_firestore

with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  with mock.patch("langchain.chat_models.ChatOpenAI"):
    with mock.patch("langchain.llms.Cohere"):
      from config import LLM_TYPES

# assigning url
api_url = f"{API_URL}/llm"
LLM_TESTDATA_FILENAME = os.path.join(TESTING_FOLDER_PATH,
                                        "llm_generate.json")

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"
os.environ["OPENAI_API_KEY"] = "fake-key"
os.environ["COHERE_API_KEY"] = "fake-key"

with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  from routes.llm import router

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/llm-service/api/v1")

FAKE_GENERATE_PARAMS = {
    "llm_type": "LLM Test",
    "prompt": "test prompt"
  }

FAKE_GENERATE_RESPONSE = "test generation"

@pytest.fixture
def create_user(client_with_emulator):
  user_dict = USER_EXAMPLE
  user = User.from_dict(user_dict)
  user.save()


def test_get_llm_list(client_with_emulator):
  url = f"{api_url}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert json_response.get("data") == LLM_TYPES


def test_llm_generate(client_with_emulator):
  url = f"{api_url}/generate"

  with mock.patch("routes.llm.llm_generate",
                  return_value = FAKE_GENERATE_RESPONSE):
    resp = client_with_emulator.post(url, json=FAKE_GENERATE_PARAMS)

  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert json_response.get("content") == FAKE_GENERATE_RESPONSE, \
    "returned generated text"


def test_create_chat(create_user, client_with_emulator):
  userid = CHAT_EXAMPLE["user_id"]
  url = f"{api_url}/chat"

  with mock.patch("routes.llm.llm_generate",
                  return_value = FAKE_GENERATE_RESPONSE):
    resp = client_with_emulator.post(url, json=FAKE_GENERATE_PARAMS)

  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  chat_data = json_response.get("data")
  assert chat_data["history"][0] == FAKE_GENERATE_PARAMS["prompt"], \
    "returned chat data prompt"
  assert chat_data["history"][1] == FAKE_GENERATE_RESPONSE, \
    "returned chat data generated text"

  user_chats = UserChat.find_by_user(userid)
  assert len(user_chats) == 1, "retreieved new user chat"
  user_chat = user_chats[0]
  assert user_chat.history[0] == FAKE_GENERATE_PARAMS["prompt"], \
    "retrieved user chat prompt"
  assert user_chat.history[1] == FAKE_GENERATE_RESPONSE, \
    "retrieved user chat response"


def test_chat_generate(client_with_emulator):
  chat_dict = {**CHAT_EXAMPLE}
  chat = UserChat.from_dict(chat_dict)
  chat.save()

  chatid = chat.id

  url = f"{api_url}/chat/{chatid}/generate"

  with mock.patch("routes.llm.llm_generate",
                  return_value = FAKE_GENERATE_RESPONSE):
    resp = client_with_emulator.post(url, json=FAKE_GENERATE_PARAMS)

  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  chat_data = json_response.get("data")
  assert chat_data["history"][0] == CHAT_EXAMPLE["history"][0], \
    "returned chat history 0"
  assert chat_data["history"][1] == CHAT_EXAMPLE["history"][1], \
    "returned chat history 1"
  assert chat_data["history"][-2] == FAKE_GENERATE_PARAMS["prompt"], \
    "returned chat data prompt"
  assert chat_data["history"][-1] == FAKE_GENERATE_RESPONSE, \
    "returned chat data generated text"

  user_chat = UserChat.find_by_id(chatid)
  assert user_chat is not None, "retrieved user chat"
  assert len(user_chat.history) == len(chat.history) + 2, \
    "user chat history updated"
  assert user_chat.history[-2] == FAKE_GENERATE_PARAMS["prompt"], \
    "retrieved user chat prompt"
  assert user_chat.history[-1] == FAKE_GENERATE_RESPONSE, \
    "retrieved user chat response"


def test_get_chats(create_user, client_with_emulator):
  chat_dict = {**CHAT_EXAMPLE}
  chat = UserChat.from_dict(chat_dict)
  chat.save()

  userid = chat.user_id
  params = {"skip": 0, "limit": "30"}
  url = f"{api_url}/chat"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  saved_ids = [i.get("id") for i in json_response.get("data")]
  assert chat_dict["id"] in saved_ids, "all data not retrieved"
