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
  Unit tests for Jobs Service endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import,unused-variable,ungrouped-imports
import os
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest import mock
from testing.test_config import API_URL, TESTING_FOLDER_PATH
from schemas.schema_examples import USER_EXAMPLE
from common.models import UserChat, User
from common.utils.http_exceptions import add_exception_handlers
from common.testing.client_with_emulator import client_with_emulator
from common.testing.firestore_emulator import firestore_emulator, clean_firestore

from config import JOB_TYPES

# assigning url
api_url = f"{API_URL}/chat"
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
app.include_router(router, prefix="/jobs-service/api/v1")

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

