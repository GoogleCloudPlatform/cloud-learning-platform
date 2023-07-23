"""
  Unit Tests for Upload endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
import os
import mock
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from testing.test_config import API_URL, TESTING_FOLDER_PATH
from routes.upload import router
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers
from config import ALLOWED_TRANSCRIPT_TYPES

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/prior-learning-assessment/api/v1")

client_with_emulator = TestClient(app)

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_upload_transcripts(mocker):
  mocker.patch("routes.upload.upload_file_to_bucket",
    return_value="gs://gcp-project/pla/user-transcripts/test.pdf")
  url = f"{API_URL}/upload"
  test_file_path = os.path.join(TESTING_FOLDER_PATH, "test.pdf")
  with open(test_file_path, "rb") as file:
    resp = client_with_emulator.post(url, files={"files": file})

  json_response = resp.json()
  assert resp.status_code == 200, "Status not 200"
  assert isinstance(json_response.get("data"), list), "Response is not a list"
  assert json_response.get("data") == \
    ["gs://gcp-project/pla/user-transcripts/test.pdf"]


def test_upload_transcripts_negative():
  url = f"{API_URL}/upload"
  test_file_path = os.path.join(TESTING_FOLDER_PATH, "prior_experiences.json")
  with open(test_file_path, "rb") as file:
    resp = client_with_emulator.post(url, files={"files": file})

  json_response = resp.json()
  assert resp.status_code == 422, "Status not 422"
  assert json_response.get("message") == \
  f"Invalid document type. Allowed types are: {ALLOWED_TRANSCRIPT_TYPES}"
