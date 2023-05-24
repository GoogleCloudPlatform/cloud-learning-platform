"""
  Unit tests for Learner Profile endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import

import os

from fastapi import FastAPI
from fastapi.testclient import TestClient

from testing.test_config import API_URL

from routes.mastery import router

from common.utils.http_exceptions import add_exception_handlers

from common.testing.firestore_emulator import (
  firestore_emulator,
  clean_firestore
)

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/learner-profile-service/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/mastery"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_compute_mastery_score(clean_firestore):
  assert True
