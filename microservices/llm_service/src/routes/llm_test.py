"""
  Unit tests for LLM Service endpoints
"""
import os
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest import mock
with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  from routes.assessment import router
from testing.test_config import API_URL, TESTING_FOLDER_PATH
from schemas.schema_examples import BASIC_ASSESSMENT_EXAMPLE
from common.models import Assessment
from common.utils.http_exceptions import add_exception_handlers
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/llm-service/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/llm"
LLM_TESTDATA_FILENAME = os.path.join(TESTING_FOLDER_PATH,
                                        "llm_generate.json")

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"



def test_llm_generate(clean_firestore):
  assessment_dict = {**BASIC_ASSESSMENT_EXAMPLE}
  assessment_dict["name"] = "Language Test"
  assessment = Assessment.from_dict(assessment_dict)
  assessment.uuid = ""
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()
  assessment_dict["uuid"] = assessment.id

  params = {"name": "LLM Test"}

  url = f"{api_url}/generate"
  resp = client_with_emulator.post(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status is not 200"
  assert json_response.get("data")[0].get("name") == assessment_dict.get(
      "name"), "Response received"


