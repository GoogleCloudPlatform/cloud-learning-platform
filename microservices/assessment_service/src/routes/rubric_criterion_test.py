"""
  Unit tests for Rubric Criterion endpoints
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
  from routes.rubric_criterion import router
from testing.test_config import API_URL
from schemas.schema_examples import BASIC_RUBRIC_CRITERION_EXAMPLE
from common.models import RubricCriterion
from common.utils.http_exceptions import add_exception_handlers
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/assessment-service/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/rubric-criterion"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_get_rubric_criterion(clean_firestore):
  assert True


def test_search_rubric_criterion(clean_firestore):
  rubric_criterion_dict = BASIC_RUBRIC_CRITERION_EXAMPLE
  rubric_criterion_dict["name"] = "Writing and Grammar"
  rubric_criterion = RubricCriterion.from_dict(rubric_criterion_dict)
  rubric_criterion.uuid = ""
  rubric_criterion.save()
  rubric_criterion.uuid = rubric_criterion.id
  rubric_criterion.update()
  rubric_criterion_dict["uuid"] = rubric_criterion.id

  params = {"name": "Writing and Grammar"}

  url = f"{api_url}/search"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert json_response.get("data")[0].get("name") == rubric_criterion_dict.get(
      "name"), "Response received"


def test_get_rubric_criterions(clean_firestore):
  rubric_criterion_dict = BASIC_RUBRIC_CRITERION_EXAMPLE
  rubric_criterion_dict["name"] = "Spelling"
  rubric_criterion = RubricCriterion.from_dict(rubric_criterion_dict)
  rubric_criterion.uuid = ""
  rubric_criterion.save()
  rubric_criterion.uuid = rubric_criterion.id
  rubric_criterion.update()
  params = {"skip": 0, "limit": "30"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  saved_names = [i.get("name") for i in json_response.get("data")["records"]]
  assert rubric_criterion_dict["name"] in saved_names, "all data not retrived"

def test_get_rubric_criterions_negative(clean_firestore):
  rubric_criterion_dict = BASIC_RUBRIC_CRITERION_EXAMPLE
  rubric_criterion_dict["name"] = "Spelling"
  rubric_criterion = RubricCriterion.from_dict(rubric_criterion_dict)
  rubric_criterion.uuid = ""
  rubric_criterion.save()
  rubric_criterion.uuid = rubric_criterion.id
  rubric_criterion.update()
  params = {"skip": 0, "limit": "101"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422, "Status 422"
  assert json_response.get(
    "message"
  ) == "Validation Failed", \
    "unknown response received"
