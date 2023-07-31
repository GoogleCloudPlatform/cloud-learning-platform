"""
  Unit tests for Assessment endpoints
"""
import os
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest import mock
from copy import deepcopy

with mock.patch(
  "google.cloud.secretmanager.SecretManagerServiceClient",
  side_effect=mock.MagicMock()) as mok:
  from routes.assessment import router
from testing.test_config import API_URL, TESTING_FOLDER_PATH
from schemas.schema_examples import BASIC_ASSESSMENT_EXAMPLE,\
  BASIC_HUMAN_GRADED_ASSESSMENT_EXAMPLE,BASIC_LEARNING_OBJECT_EXAMPLE,\
  BASIC_SKILL_EXAMPLE
from common.models import Assessment,LearningObject, Skill
from common.utils.http_exceptions import add_exception_handlers
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from config import DATABASE_PREFIX
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

def mocked_requests_put(**kwargs):
  class MockResponse:
    def __init__(self, json_data, status_code):
      self.json_data = json_data
      self.status_code = status_code
    def json(self):
      return self.json_data
  return MockResponse({"success":True}, 200)

def test_get_assessment(clean_firestore, mocker):

  assessment_dict = deepcopy(BASIC_HUMAN_GRADED_ASSESSMENT_EXAMPLE)
  url = f"{api_url}/human-graded"
  mocker.patch(
    "routes.assessment.attach_files_to_assessment",
    return_value=assessment_dict["resource_paths"]
  )
  post_resp = client_with_emulator.post(url, json=assessment_dict)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  url = f"{api_url}/{post_resp_json['data']['uuid']}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 200, "Status is not 200"
  assert json_response.get("data").get("uuid") == post_resp_json["data"]["uuid"]

  url = f"{api_url}/{post_resp_json['data']['uuid']}?fetch_tree=True"
  resp = client_with_emulator.get(url)
  json_response = resp.json()["data"]
  assert resp.status_code == 200, "Status is not 200"
  assert json_response["name"] == assessment_dict["name"], \
    f"""Ingested Assessment = {json_response["name"]}"""
  assert json_response["child_nodes"]["rubrics"][0]["name"] == \
  assessment_dict["child_nodes"]["rubrics"][0]["name"], \
  f"""Ingested Rubric = {json_response["child_nodes"][
    "rubrics"][0]["name"]}"""
  assert json_response["child_nodes"]["rubrics"][0][
    "child_nodes"]["rubric_criteria"][0]["name"] == \
      assessment_dict["child_nodes"]["rubrics"][0][
        "child_nodes"]["rubric_criteria"][0]["name"], \
  f"""Ingested RubricCriteria = {json_response[
    "child_nodes"]["rubrics"][0]["name"]}"""


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


def test_get_assessment_types(clean_firestore):
  url = f"{api_url}/types"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 200, "Status is not 200"
  assert json_response.get("data") == {
    "static_srl": "SRL",
    "practice": "Formative",
    "project": "Summative"
  }


def test_get_assessments(clean_firestore):
  basic_skill = BASIC_SKILL_EXAMPLE
  new_skill = Skill()
  new_skill = new_skill.from_dict(basic_skill)
  new_skill.uuid = ""
  new_skill.save()
  new_skill.uuid = new_skill.id
  new_skill.update()
  assessment_dict = {**BASIC_ASSESSMENT_EXAMPLE}
  assessment_dict["name"] = "Questionnaire"
  assessment = Assessment.from_dict(assessment_dict)
  assessment.uuid = ""

  skill_data = [{"uuid": new_skill.uuid, "name": new_skill.name}]
  assessment.references = {"skills": skill_data}
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()
  params = {"skip": 0, "limit": "30",
            "performance_indicators": [new_skill.uuid]}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  saved_names = [i.get("name") for i in json_response.get("data")["records"]]
  assert assessment.name in saved_names, "all data not retrived"
  assert assessment.references.get("skills") == skill_data


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


def test_sort_assessments(clean_firestore):
  assessment_dict = {**BASIC_ASSESSMENT_EXAMPLE, "name": "Questionnaire"}
  assessment = Assessment.from_dict(assessment_dict)
  assessment.uuid = ""
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()
  params = {"skip": 0, "limit": "30", "sort_by": "name",
            "sort_order": "ascending"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  saved_names = [i.get("name") for i in json_response.get("data")["records"]]
  assert assessment_dict["name"] in saved_names, "all data not retrived"


def test_sort_assessments_negative(clean_firestore):
  params = {"skip": 0, "limit": "30", "sort_by": "name",
            "sort_order": "asc"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422
  assert json_response["success"] is False


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
    "message": f"{DATABASE_PREFIX}assessments with id "+\
      "ASS345Dl3Ayg0PWudzhI is not found",
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


def test_create_human_graded_assessment(mocker, clean_firestore):
  input_human_graded_assessment = deepcopy(
    BASIC_HUMAN_GRADED_ASSESSMENT_EXAMPLE)
  mocker.patch(
    "routes.assessment.attach_files_to_assessment",
    return_value=input_human_graded_assessment["resource_paths"]
  )
  basic_skill = BASIC_SKILL_EXAMPLE
  new_skill = Skill()
  new_skill = new_skill.from_dict(basic_skill)
  new_skill.uuid = ""
  new_skill.save()
  new_skill.uuid = new_skill.id
  new_skill.update()
  input_human_graded_assessment["child_nodes"]["rubrics"][0][
    "child_nodes"]["rubric_criteria"][0][
      "performance_indicators"] = [new_skill.id]

  url = f"{api_url}/human-graded"
  post_resp = client_with_emulator.post(url, json=input_human_graded_assessment)
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


@mock.patch(
    "routes.assessment.requests.put",side_effect=mocked_requests_put)
def test_replace_old_assessment(mock_token_res,clean_firestore):
  parent_lo_dict= {**BASIC_LEARNING_OBJECT_EXAMPLE}
  parent_lo= LearningObject.from_dict(parent_lo_dict)
  parent_lo.uuid=""
  parent_lo.save()
  parent_lo.uuid = parent_lo.id
  parent_lo.update()

  assessment_example= deepcopy(BASIC_ASSESSMENT_EXAMPLE)
  assessment_dict = {**assessment_example}
  assessment_dict["name"] = "Placeholder Assessment"
  assessment = Assessment.from_dict(assessment_dict)
  assessment.uuid = ""
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()
  assessment_dict["uuid"] = assessment.uuid

  old_assessment_id = assessment.uuid

  #Parent LO assessment linking
  parent_lo.child_nodes = {"assessments": [old_assessment_id]}
  assessment.parent_nodes = {"learning_objects": [parent_lo.uuid]}
  parent_lo.update()
  assessment.update()

  authored_assessment_example= deepcopy(BASIC_ASSESSMENT_EXAMPLE)
  authored_assessment_dict = {**authored_assessment_example}
  authored_assessment_dict["name"] = "Authored Assessment"
  authored_assessment = Assessment.from_dict(authored_assessment_dict)
  authored_assessment.uuid = ""
  authored_assessment.save()
  authored_assessment.uuid = authored_assessment.id
  authored_assessment.update()
  authored_assessment_dict["uuid"] = authored_assessment.id

  new_assessment_id = authored_assessment.uuid

  #pylint: disable=line-too-long
  url =\
    f"{api_url}/replace/{old_assessment_id}?new_assessment_id={new_assessment_id}"
  resp = client_with_emulator.put(url)
  json_response = resp.json()
  print(json_response)
  assert resp.status_code == 200, "Status is not 200"
  assert json_response["data"]["parent_nodes"]["learning_objects"][0] ==\
    parent_lo.uuid, "The assessment isn't linked in the heirarchy"
  assert json_response["data"]["uuid"] == new_assessment_id
  assert json_response["data"]["name"] == authored_assessment_dict["name"]

def test_update_human_graded_assessment(mocker, clean_firestore):

  input_human_graded_assessment = deepcopy(
    BASIC_HUMAN_GRADED_ASSESSMENT_EXAMPLE)
  mocker.patch(
    "routes.assessment.attach_files_to_assessment",
    return_value=input_human_graded_assessment["resource_paths"]
  )
  basic_skill = BASIC_SKILL_EXAMPLE
  new_skill = Skill()
  new_skill = new_skill.from_dict(basic_skill)
  new_skill.uuid = ""
  new_skill.save()
  new_skill.uuid = new_skill.id
  new_skill.update()
  input_human_graded_assessment["child_nodes"]["rubrics"][0][
    "child_nodes"]["rubric_criteria"][0][
      "performance_indicators"] = [new_skill.id]

  url = f"{api_url}/human-graded"
  post_resp = client_with_emulator.post(url, json=input_human_graded_assessment)
  post_resp_json = post_resp.json()
  assert post_resp.status_code == 200, "Creation Status not 200"

  assessment_uuid = post_resp_json["data"]["uuid"]

  update_request = {
  "name": "Assessment 22",
  "type": "practice",
  "order": 3,
  "author_id": "sme authore",
  "instructor_id": "sme",
  "assessor_id": "assessor_id",
  "alias": "assessment"
}
  update_url = f"{api_url}/human-graded/{assessment_uuid}"
  put_resp = client_with_emulator.put(update_url, json=update_request)
  update_json_response = put_resp.json()

  assert put_resp.status_code == 200, "Status code not 200"
  assert update_json_response["success"], "Success is False"
  assert update_json_response["data"]["name"] == update_request["name"], \
    "Assessment Item not updated properly."
  assert update_json_response["data"]["order"] == 3, \
  "Assessment order not updated properly"
