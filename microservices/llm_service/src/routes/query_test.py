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
                                     USER_QUERY_EXAMPLE,
                                     USER_EXAMPLE, QUERY_ENGINE_EXAMPLE,
                                     QUERY_RESULT_EXAMPLE)
from common.models import UserQuery, QueryResult, QueryEngine, User
from common.models.llm_query import QUERY_HUMAN, QUERY_AI_RESPONSE, QUERY_AI_REFERENCES
from common.utils.http_exceptions import add_exception_handlers
from common.utils.auth_service import validate_user
from common.utils.auth_service import validate_token
from common.testing.firestore_emulator import firestore_emulator, clean_firestore

with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  with mock.patch("langchain.chat_models.ChatOpenAI"):
    with mock.patch("langchain.llms.Cohere"):
      from config import DEFAULT_QUERY_CHAT_MODEL

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
  "message": "job created",
  "data": {
    "job_name": "fake_job_name",
    "status": "fake_job_status"
  }
}

FAKE_QUERY_ENGINE_BUILD = {
  "doc_url": "fake-url",
  "query_engine": "query-engine-test",
  "llm_type": DEFAULT_QUERY_CHAT_MODEL,
  "is_public": True
}

FAKE_REFERENCES = USER_QUERY_EXAMPLE["history"][1]["AIReferences"]

FAKE_GENERATE_RESPONSE = "test generation"

FAKE_QUERY_RESPONSE = (QUERY_RESULT_EXAMPLE, FAKE_REFERENCES)

FAKE_QUERY_PARAMS = QUERY_EXAMPLE


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

@pytest.fixture
def create_user(client_with_emulator):
  user_dict = USER_EXAMPLE
  user = User.from_dict(user_dict)
  user.save()

@pytest.fixture
def create_engine(client_with_emulator):
  query_engine_dict = QUERY_ENGINE_EXAMPLE
  q_engine = QueryEngine.from_dict(query_engine_dict)
  q_engine.save()

@pytest.fixture
def create_user_query(client_with_emulator):
  query_dict = USER_QUERY_EXAMPLE
  query = UserQuery.from_dict(query_dict)
  query.save()

@pytest.fixture
def create_query_result(client_with_emulator):
  query_result_dict = QUERY_RESULT_EXAMPLE
  query_result = QueryResult.from_dict(query_result_dict)
  query_result.save()


def test_get_query_engine_list(create_engine, client_with_emulator):
  url = f"{api_url}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  saved_ids = [i.get("id") for i in json_response.get("data")]
  assert QUERY_ENGINE_EXAMPLE["id"] in saved_ids, "all data not retrieved"


def test_create_query_engine(create_user, client_with_emulator):
  url = f"{api_url}/engine"
  params = FAKE_QUERY_ENGINE_BUILD
  with mock.patch("routes.query.initiate_batch_job",
                  return_value = FAKE_QE_BUILD_RESPONSE):
    resp = client_with_emulator.post(url, json=params)

  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  query_engine_data = json_response.get("data")
  assert query_engine_data == FAKE_QE_BUILD_RESPONSE["data"]


def test_query(create_user, create_engine,
               create_query_result, client_with_emulator):
  q_engine_id = QUERY_ENGINE_EXAMPLE["id"]
  url = f"{api_url}/engine/{q_engine_id}"

  query_result = QueryResult.find_by_id(QUERY_RESULT_EXAMPLE["id"])
  fake_query_response = (query_result, FAKE_REFERENCES)
  with mock.patch("routes.query.query_generate",
                  return_value = fake_query_response):
    resp = client_with_emulator.post(url, json=FAKE_QUERY_PARAMS)

  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  query_data = json_response.get("data")
  assert query_data["query_result"]["id"] == QUERY_RESULT_EXAMPLE.get("id"), \
    "returned query result"
  assert query_data["query_references"] == FAKE_REFERENCES, \
    "returned query references"


def test_query_generate(create_user, create_engine, create_user_query,
                        create_query_result, client_with_emulator):
  queryid = USER_QUERY_EXAMPLE["id"]

  url = f"{api_url}/{queryid}"

  query_result = QueryResult.find_by_id(QUERY_RESULT_EXAMPLE["id"])
  fake_query_response = (query_result, FAKE_REFERENCES)
  with mock.patch("routes.query.query_generate",
                  return_value = fake_query_response):
    resp = client_with_emulator.post(url, json=FAKE_QUERY_PARAMS)

  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  query_data = json_response.get("data")
  assert query_data["query_result"]["id"] == QUERY_RESULT_EXAMPLE.get("id"), \
    "returned query result"
  assert query_data["query_references"] == FAKE_REFERENCES, \
    "returned query references"


def test_get_query(create_user, create_engine, create_user_query,
                   client_with_emulator):
  queryid = USER_QUERY_EXAMPLE["id"]
  url = f"{api_url}/{queryid}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  saved_id = json_response.get("data").get("id")
  assert USER_QUERY_EXAMPLE["id"] == saved_id, "all data not retrieved"


def test_get_queries(create_user, create_user_query, client_with_emulator):
  userid = USER_EXAMPLE["id"]
  url = f"{api_url}/user/{userid}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  saved_ids = [i.get("id") for i in json_response.get("data")]
  assert USER_QUERY_EXAMPLE["id"] in saved_ids, "all data not retrieved"
