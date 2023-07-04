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
from schemas.schema_examples import (LLM_GENERATE_EXAMPLE, QUERY_EXAMPLE,
                                     USER_EXAMPLE, query data)
from common.models import UserQuery, QueryEngine, User
from common.models.llm import CHAT_HUMAN, CHAT_AI
from common.utils.http_exceptions import add_exception_handlers
from common.utils.auth_service import validate_user
from common.utils.auth_service import validate_token
from common.testing.firestore_emulator import firestore_emulator, clean_firestore

QUERY_HUMAN
QUERY_AI_RESPONSE
QUERY_AI_REFERENCES


with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  with mock.patch("langchain.chat_models.ChatOpenAI"):
    with mock.patch("langchain.llms.Cohere"):
      from config import LLM_TYPES

# assigning url
api_url = f"{API_URL}/query"
LLM_TESTDATA_FILENAME = os.path.join(TESTING_FOLDER_PATH,
                                        "llm_generate.json")

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"
os.environ["GCP_PROJECT"] = "fake-project"
os.environ["OPENAI_API_KEY"] = "fake-key"
os.environ["COHERE_API_KEY"] = "fake-key"

with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  with mock.patch("kubernetes.config.load_incluster_config"):
    from routes.query import router

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/llm-service/api/v1")

FAKE_USER_DATA = {
    "id": "fake-user-id",
    "user_id": "fake-user-id",
    "auth_id": "fake-user-id",
    "email": "user@gmail.com",
    "role": "Admin"
}

FAKE_QE_BUILD_RESPONSE = {
  "success": True,
  "message": f"job created",
  "data": {
    "job_name": "fake_job_name",
    "status": "fake_job_status"
  }
}

FAKE_GENERATE_RESPONSE = "test generation"

FAKE_QUERY_PARAMS = {
    "prompt": "test prompt"
}


@pytest.fixture
def client_with_emulator(clean_firestore, scope="module"):
  """ Create FastAPI test client with clean firestore emulator """
  def mock_validate_user():
    return True

  def mock_validate_token():
    return FAKE_USER_DATA

  app.dependency_overrides[validate_user] = mock_validate_user
  app.dependency_overrides[validate_token] = mock_validate_token
  test_client = TestClient(app)
  yield test_client

@pytest.fixquery data(client_with_emulator):
  user_dict = USER_EXAMPLE
  user = User.from_dict(user_dict)
  user.save()


def test_get_query_engine_list(client_with_emulator):
  query_engine_dict = {**QUERY_ENGINE_EXAMPLE}
  q_engine = QueryEngine.from_dict(query_engine_dict)
  q_engine.save()
  
  url = f"{api_url}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  saved_ids = [i.get("id") for i query data("data")]
  assert query_engine_dict["id"] in saved_ids, "all data not retrieved"


def test_create_query_engine(create_user, client_with_emulator):
  url = f"{api_url}"
  params = QUERY_ENGINE_EXAMPLE
  del params["id"]
  with mock.patch("routes.query.initiate_batch_job",
                  return_value = FAKE_QE_BUILD_RESPONSE):
    resp = client_with_emulator.post(url, json=params)

  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  query_engine_data = json_response.get("data")
  assert query_engine_data == FAKE_QE_BUILD_RESPONSE


def test_query(client_with_emulator):
  query_engine_dict = {**QUERY_ENGINE_EXAMPLE}
  q_engine = QueryEngine.from_dict(query_engine_dict)
  q_engine.save()

  url = f"{api_url}/engine/{q_engine.id}"

  with mock.patch("routes.query.query_generate",
                  return_value = FAKE_GENERATE_RESPONSE):
    resp = client_with_emulator.post(url, json=FAKE_QUERY_PARAMS)

  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  query_data = json_response.get("data")
  assert query_data["history"][0] == QUERY_EXAMPLE["history"][0], \
    "returned query history 0"
  assert query_data["history"][1] == QUERY_EXAMPLE["history"][1], \
    "returned query history 1"

  user_queries = UserQuery.find_by_user(userid)
  assert len(user_queries) == 1, "retreieved new user query"
  user_query = user_queries[0]
  assert user_query.history[0] == \
    {CHAT_HUMAN: FAKE_GENERATE_PARAMS["prompt"]}, \
    "retrieved user query prompt"
  assert user_query.history[1] == \
    {CHAT_AI: FAKE_GENERATE_RESPONSE}, \
    "retrieved user query response"


def test_query_generate(client_with_emulator):
  query_dict = {**QUERY_EXAMPLE}
  query = UserQuery.from_dict(query_dict)
  query.save()

  queryid = query.id

  url = f"{api_url}/query/{queryid}/generate"

  with mock.patch("routes.query.query_generate",
                  return_value = FAKE_GENERATE_RESPONSE):
    resp = client_with_emulator.post(url, json=FAKE_QUERY_PARAMS)

  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  query_data = json_response.get("data")
  assert query_data["history"][0] == QUERY_EXAMPLE["history"][0], \
    "returned query history 0"
  assert query_data["history"][1] == QUERY_EXAMPLE["history"][1], \
    "returned query history 1"
  assert query_data["history"][-2] == FAKE_QUERY_PARAMS["prompt"], \
    "returned query data prompt"
  assert query_data["history"][-1] == FAKE_GENERATE_RESPONSE, \
    "returned query data generated text"

  user_query = UserQuery.find_by_id(queryid)
  assert user_query is not None, "retrieved user query"
  assert len(user_query.history) == len(chat.history) + 2, \
    "user query history updated"
  assert user_query.history[-2] == FAKE_QUERY_PARAMS["prompt"], \
    "retrieved user chat prompt"
  assert user_query.history[-1] == FAKE_GENERATE_RESPONSE, \
    "retrieved user chat response"


def test_get_query(create_user, client_with_emulator):
  query_dict = {**QUERY_EXAMPLE}
  query = UserQuery.from_dict(query_dict)
  query.save()

  url = f"{api_url}/{query.id}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  saved_id = json_response.get("data").get("id")
  assert query.id == saved_id, "all data not retrieved"


def test_get_queries(create_user, client_with_emulator):
  query_dict = {**QUERY_EXAMPLE}
  query = UserQuery.from_dict(query_dict)
  query.save()

  userid = query.user_id
  url = f"{api_url}/user/{userid}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  saved_ids = [i.get("id") for i in json_response.get("data")]
  assert query_dict["id"] in saved_ids, "all data not retrieved"
