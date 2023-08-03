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
from testing.test_config import API_URL
from schemas.schema_examples import BATCHJOB_EXAMPLE
from common.models import BatchJobModel, JobStatus
from common.utils.config import JOB_TYPE_QUERY_ENGINE_BUILD
from common.utils.auth_service import validate_user, validate_token
from common.utils.http_exceptions import add_exception_handlers
from common.testing.firestore_emulator import firestore_emulator, clean_firestore

with mock.patch("common.utils.kf_job_app.kube_delete_job"):
  from common.utils import batch_jobs

from config import JOB_TYPES

# assigning url
api_url = f"{API_URL}/jobs"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  from routes.jobs import router

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/jobs-service/api/v1")

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

  app.dependency_overrides[validate_user] = mock_validate_user
  app.dependency_overrides[validate_token] = mock_validate_token
  test_client = TestClient(app)
  yield test_client

@pytest.fixture
def create_job(client_with_emulator):
  batchjob_dict = BATCHJOB_EXAMPLE
  job = BatchJobModel.from_dict(batchjob_dict)
  job.save()


def test_get_job_status(create_job, client_with_emulator):
  job = BatchJobModel.find_by_name(BATCHJOB_EXAMPLE["name"])
  job_name = job.name
  url = f"{api_url}/{job.type}/{job_name}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  job_data = json_response.get("data")
  assert job_data["id"] == BATCHJOB_EXAMPLE["id"], "all data not retrieved"


def test_get_all_jobs(create_job, client_with_emulator):
  url = f"{api_url}/{JOB_TYPE_QUERY_ENGINE_BUILD}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  saved_ids = [i.get("id") for i in json_response.get("data")]
  assert BATCHJOB_EXAMPLE["id"] in saved_ids, "all data not retrieved"


def test_delete_job(create_job, client_with_emulator):
  job = BatchJobModel.find_by_name(BATCHJOB_EXAMPLE["name"])
  job_name = job.name
  url = f"{api_url}/{job.type}/{job_name}"
  resp = client_with_emulator.delete(url)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  job = BatchJobModel.find_by_name(BATCHJOB_EXAMPLE["name"])
  assert job is None, "batch job model not deleted"


def test_update_job(create_job, client_with_emulator):
  job = BatchJobModel.find_by_name(BATCHJOB_EXAMPLE["name"])
  job_name = job.name
  url = f"{api_url}/{job.type}/{job_name}"
  resp = client_with_emulator.put(url)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  job = BatchJobModel.find_by_name(BATCHJOB_EXAMPLE["name"])
  assert job.status == JobStatus.JOB_STATUS_ABORTED.value, \
      "all data not retrieved"
