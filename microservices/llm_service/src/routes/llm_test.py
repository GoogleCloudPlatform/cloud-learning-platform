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
from schemas.schema_examples import LLM_GENERATE_EXAMPLE, CHAT_EXAMPLE
from common.models import UserChat
from common.utils.http_exceptions import add_exception_handlers
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
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

client_with_emulator = TestClient(app)


def test_get_llm_list(clean_firestore):
  pass


def test_llm_generate(clean_firestore):
  params = {
    "llm_type": "LLM Test",
    "prompt": "test"
  }
  url = f"{api_url}/generate"
  #with mock.patch("routes.llm.Logger"):
  #  with mock.patch("routes.llm.llm_generate"):
  #    resp = client_with_emulator.post(url, params=params)
  #assert resp.status_code == 200, "Status is not 200"


def test_get_chats(clean_firestore):
  chat_dict = {**CHAT_EXAMPLE}
  chat = UserChat.from_dict(chat_dict)
  chat.save()

  userid = chat.user_id
  params = {"skip": 0, "limit": "30"}
  url = f"{api_url}/user/{userid}/chat"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  
  assert resp.status_code == 200, "Status 200"
  saved_ids = [i.get("id") for i in json_response.get("data")]
  assert chat_dict["id"] in saved_ids, "all data not retrived"
