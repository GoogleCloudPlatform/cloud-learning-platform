"""
  Unit tests for Assessment endpoints
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
app.include_router(router, prefix="/assessment-service/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/assessment"
ASSESSMENT_DATA_TESTDATA_FILENAME = os.path.join(TESTING_FOLDER_PATH,
                                                 "assessment.json")

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_get_assessment(clean_firestore):
  assessment_dict = {**BASIC_ASSESSMENT_EXAMPLE}
  assessment_dict["name"] = "CLP TEST"
  assessment = Assessment.from_dict(assessment_dict)
  assessment.uuid = ""
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()
  assessment_dict["uuid"] = assessment.id

  url = f"{api_url}/{assessment_dict['uuid']}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 200, "Status is not 200"
  assert json_response.get("data").get("uuid") == assessment_dict["uuid"]


def test_search_assessment(clean_firestore):
  assessment_dict = {**BASIC_ASSESSMENT_EXAMPLE}
  assessment_dict["name"] = "Language Test"
  assessment = Assessment.from_dict(assessment_dict)
  assessment.uuid = ""
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()
  assessment_dict["uuid"] = assessment.id

  params = {"name": "Language Test"}

  url = f"{api_url}/search"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status is not 200"
  assert json_response.get("data")[0].get("name") == assessment_dict.get(
      "name"), "Response received"


def test_get_assessments(clean_firestore):
  assessment_dict = {**BASIC_ASSESSMENT_EXAMPLE}
  assessment_dict["name"] = "Questionnaire"
  assessment = Assessment.from_dict(assessment_dict)
  assessment.uuid = ""
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()
  params = {"skip": 0, "limit": "30"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  saved_names = [i.get("name") for i in json_response.get("data")]
  assert assessment_dict["name"] in saved_names, "all data not retrived"

def test_get_assessments_negative(clean_firestore):
  assessment_dict = {**BASIC_ASSESSMENT_EXAMPLE}
  assessment_dict["name"] = "Questionnaire"
  assessment = Assessment.from_dict(assessment_dict)
  assessment.uuid = ""
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()
  params = {"skip": 0, "limit": "101"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422, "Status not 422"
  assert json_response.get(
    "message"
  ) == "Validation Failed", \
    "unknown response received"

def test_post_assessment(clean_firestore):
  input_assessment = BASIC_ASSESSMENT_EXAMPLE
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_assessment)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  post_json_response = post_resp.json()
  del post_json_response["data"]["created_time"]
  del post_json_response["data"]["last_modified_time"]

  uuid = post_json_response.get("data").get("uuid")
  # now see if GET endpoint returns same data
  url = f"{api_url}/{uuid}"
  get_resp = client_with_emulator.get(url)
  get_json_response = get_resp.json()
  del get_json_response["data"]["created_time"]
  del get_json_response["data"]["last_modified_time"]
  assert get_json_response.get("data") == post_json_response.get("data")


def test_delete_assessment(clean_firestore):
  assessment_dict = BASIC_ASSESSMENT_EXAMPLE
  assessment = Assessment.from_dict(assessment_dict)
  assessment.uuid = ""
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()
  assessment_dict["uuid"] = assessment.id

  uuid = assessment.uuid
  assessment_dict["uuid"] = uuid

  url = f"{api_url}/{uuid}"
  resp = client_with_emulator.delete(url)
  del_json_response = resp.json()

  expected_data = {
      "success": True,
      "message": "Successfully deleted the assessment"
  }
  assert resp.status_code == 200, "Status code not 200"
  assert del_json_response == expected_data, "Expected response not same"


def test_delete_assessment_negative(clean_firestore):
  assessment_uuid = "ASS345Dl3Ayg0PWudzhI"
  url = f"{api_url}/{assessment_uuid}"
  response = {
      "success": False,
      "message": "Assessment with uuid ASS345Dl3Ayg0PWudzhI not found",
      "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_import_assessment(clean_firestore):
  url = f"{api_url}/import/json"
  with open(
      ASSESSMENT_DATA_TESTDATA_FILENAME,
      encoding="UTF-8") as assessment_json_file:
    resp = client_with_emulator.post(
        url, files={"json_file": assessment_json_file})

  json_response = resp.json()
  assert resp.status_code == 200, "Status code not 200"
  assert isinstance(json_response.get("data"), list), "Response is not a list"
  assert len(json_response.get("data")) > 0, "Empty list returned"
