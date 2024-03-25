"""
  Tests for syntactic-search endpoint
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
import os
from unittest import mock
from fastapi import FastAPI
from fastapi.testclient import TestClient
with mock.patch(
    "google.cloud.logging.Client", side_effect=mock.MagicMock()) as mok:
  from routes.syntactic_search import router
from testing.test_config import API_URL
from schemas.schema_examples import BASIC_SKILL_MODEL_EXAMPLE
from common.models import Skill
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/skill-service/api/v1")

client_with_emulator = TestClient(app)

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_search_skill_name(clean_firestore):
  skill_dict = BASIC_SKILL_MODEL_EXAMPLE
  skill = Skill.from_dict(skill_dict)
  skill.uuid = ""
  skill.save()
  skill.uuid = skill.id
  skill.update()

  req_body = {"name": "Regression Analysis"}

  url = f"{API_URL}/syntactic-search"
  resp = client_with_emulator.post(url, json=req_body)
  json_response = resp.json()
  print(json_response)
  assert resp.status_code == 200, "Status 200"
  assert json_response.get("data")["skill"][0].get(
      "name") == BASIC_SKILL_MODEL_EXAMPLE.get("name"), "Response received"


def test_search_skill_keywords(clean_firestore):
  skill_dict = BASIC_SKILL_MODEL_EXAMPLE
  skill = Skill.from_dict(skill_dict)
  skill.uuid = ""
  skill.save()
  skill.uuid = skill.id
  skill.update()
  skill_dict["uuid"] = skill.id

  req_body = {"keyword": "analysis"}

  url = f"{API_URL}/syntactic-search"
  resp = client_with_emulator.post(url, json=req_body)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert req_body.get("keyword") in json_response.get(
      "data")["skill"][0]["keywords"], "Response received"


def test_search_skill_negative(clean_firestore):
  skill_dict = BASIC_SKILL_MODEL_EXAMPLE
  skill = Skill.from_dict(skill_dict)
  skill.uuid = ""
  skill.save()
  skill.uuid = skill.id
  skill.update()
  skill_dict["uuid"] = skill.id

  req_body = {"name": "test name", "keyword": "test keyword"}

  url = f"{API_URL}/syntactic-search"
  resp = client_with_emulator.post(url, json=req_body)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  assert json_response.get("data") == {
      "domain": [],
      "sub_domain": [],
      "category": [],
      "competency": [],
      "skill": []
  }, "Response received"
