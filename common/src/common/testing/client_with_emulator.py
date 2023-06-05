# Copyright 2022 Google LLC
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
  Pytest Fixture for getting testclient from fastapi

  NOTE: this assumes you are executing this in a FastAPI service
  where you can run run `from main import app`
"""

# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import

import pytest
from fastapi.testclient import TestClient
from main import app, api
from common.testing.firestore_emulator import clean_firestore
from common.utils.auth_service import validate_user
from common.utils.auth_service import validate_token

FAKE_USER_DATA = {
    "id": "fake-user-id",
    "user_id": "fake-user-id",
    "auth_id": "fake-user-id",
    "email": "user@gmail.com",
    "role": "Admin"
}

@pytest.fixture
def client_with_emulator(clean_firestore, scope="module"):
  """ Create FastAPI test client with clean firestore emulator """
  def mock_validate_user():
    return True

  def mock_validate_token():
    return FAKE_USER_DATA

  api.dependency_overrides[validate_user] = mock_validate_user
  api.dependency_overrides[validate_token] = mock_validate_token
  test_client = TestClient(app)
  yield test_client
