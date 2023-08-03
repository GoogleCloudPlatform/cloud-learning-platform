"""
  Sample Tests for Learning Record endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=nconsistent-quotes,unused-argument,redefined-outer-name,unused-import
import json
from fastapi import FastAPI
from fastapi.testclient import TestClient
from common.utils.http_exceptions import add_exception_handlers
from common.models import (Agent, LearningExperience, Verb, Activity, Session,
                           User, Learner, LearnerProfile)
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)

from testing.test_config import API_URL
from schemas.schema_examples import (
    ACTIVITY_XAPI_RESPONSE_EXAMPLE, BASIC_ACTIVITY_EXAMPLE,
    BASIC_AGENT_SCHEMA_EXAMPLE, BASIC_VERB_MODEL_EXAMPLE, BASIC_XAPI_STATEMENT,
    FULL_XAPI_STATEMENT, AGENT_XAPI_EXAMPLE, VERB_XAPI_EXAMPLE, TEST_USER,
    ACTIVITY_XAPI_EXAMPLE, BASIC_LEARNING_EXPERIENCE_EXAMPLE,
    BASIC_SESSION_EXAMPLE, BASIC_LEARNER_EXAMPLE, BASIC_LEARNER_PROFILE_EXAMPLE)
from routes.statement import router
import datetime

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/learning-record-service/api/v1")

client_with_emulator = TestClient(app)

api_url = f"{API_URL}"


def test_get_lrs_details():
  url = f"{api_url}/about"
  resp = client_with_emulator.get(url)
  resp_data = resp.json()

  assert resp.status_code == 200
  assert resp_data["success"] is True, "Success is not True"
  assert resp_data["message"] == "Successfully fetched the details about LRS"
  assert resp_data["data"]["version"], "LRS Version not returned"


def test_get_xapi_statement(mocker):
  expected_data = {**FULL_XAPI_STATEMENT}
  expected_data["uuid"] = "g91vvwkbey17vb7t1"
  uuid = "g91vvwkbey17vb7t1"
  url = f"{api_url}/statement/{uuid}"
  json_dict = [{
      "uuid":
          "g91vvwkbey17vb7t1",
      "actor":
          AGENT_XAPI_EXAMPLE,
      "verb": {
          **VERB_XAPI_EXAMPLE, "canonical_data": json.dumps({})
      },
      "object": {
          **ACTIVITY_XAPI_RESPONSE_EXAMPLE, "canonical_data":
              json.dumps(ACTIVITY_XAPI_RESPONSE_EXAMPLE["canonical_data"])
      },
      "session_id":
          expected_data["session_id"],
      "object_type":
          "activities",
      "result":
          json.dumps({}),
      "context":
          json.dumps({}),
      "timestamp":
          datetime.datetime(
              2022, 8, 26, 12, 29, 50, 1353, tzinfo=datetime.timezone.utc),
      "stored":
          datetime.datetime(
              2022, 8, 26, 12, 29, 50, 1353, tzinfo=datetime.timezone.utc),
      "authority":
          json.dumps({}),
      "attachments": [],
      "result_success":
          True,
      "result_completion":
          True,
      "result_score_raw":
          80,
      "result_score_min":
          0,
      "result_score_max":
          100
  }]
  mocker.patch(
      "routes.statement.fetch_data_using_query_from_bq", return_value=json_dict)
  resp = client_with_emulator.get(url)
  resp_data = resp.json()
  del resp_data["data"]["stored"]
  del resp_data["data"]["timestamp"]
  del expected_data["stored"]
  del expected_data["timestamp"]
  assert resp.status_code == 200, "Status code is not 200"
  assert resp_data["success"] is True, "Success is not True"
  assert resp_data["message"] == "Successfully fetched the statement"
  assert resp_data["data"] == expected_data


def test_get_xapi_statement_negative(mocker):
  uuid = "random_id"
  url = f"{api_url}/statement/{uuid}"
  mocker.patch(
      "routes.statement.fetch_data_using_query_from_bq", return_value=False)
  resp = client_with_emulator.get(url)
  resp_data = resp.json()
  assert resp.status_code == 404, "Status code is not 200"
  assert resp_data["success"] is False, "Success is not False"
  assert resp_data["message"] == "xAPI Statement with 'random_id' not found"


def test_get_all_xapi_statement(mocker):
  url = f"{api_url}/statements"
  expected_data = {**FULL_XAPI_STATEMENT}
  expected_data["uuid"] = "g91vvwkbey17vb7t1"
  query_params = {"skip": 0, "limit": 10}
  json_dict = [{
      "uuid":
          "g91vvwkbey17vb7t1",
      "actor":
          AGENT_XAPI_EXAMPLE,
      "verb": {
          **VERB_XAPI_EXAMPLE, "canonical_data": json.dumps({})
      },
      "object": {
          **ACTIVITY_XAPI_RESPONSE_EXAMPLE, "canonical_data":
              json.dumps(ACTIVITY_XAPI_RESPONSE_EXAMPLE["canonical_data"])
      },
      "session_id":
          expected_data["session_id"],
      "object_type":
          "activities",
      "result":
          json.dumps({}),
      "context":
          json.dumps({}),
      "timestamp":
          datetime.datetime(
              2022, 8, 26, 12, 29, 50, 1353, tzinfo=datetime.timezone.utc),
      "stored":
          datetime.datetime(
              2022, 8, 26, 12, 29, 50, 1353, tzinfo=datetime.timezone.utc),
      "authority":
          json.dumps({}),
      "attachments": [],
      "result_success":
          True,
      "result_completion":
          True,
      "result_score_raw":
          80,
      "result_score_min":
          0,
      "result_score_max":
          100
  }]
  mocker.patch(
      "routes.statement.fetch_data_using_query_from_bq", return_value=json_dict)
  resp = client_with_emulator.get(url, params=query_params)
  resp_data = resp.json()
  del resp_data["data"]["records"][0]["stored"]
  del resp_data["data"]["records"][0]["timestamp"]
  del expected_data["stored"]
  del expected_data["timestamp"]
  assert resp.status_code == 200, "Status code is not 200"
  assert resp_data["success"] is True, "Success is not True"
  assert resp_data["message"] == "Successfully fetched the statements"
  assert expected_data in resp_data["data"]["records"]


def test_get_all_xapi_statement_negative(mocker):
  url = f"{api_url}/statements"
  query_params = {"skip": -1, "limit": 10}
  mocker.patch(
      "routes.statement.fetch_data_using_query_from_bq", return_value=[])
  resp = client_with_emulator.get(url, params=query_params)
  resp_data = resp.json()
  assert resp.status_code == 422, "Status not 422"
  assert resp_data.get(
    "message"
  ) == "Validation Failed", \
    "unknown response received"


def test_post_xapi_statements(mocker, firestore_emulator, clean_firestore):

  test_learner = Learner()
  test_learner = test_learner.from_dict(BASIC_LEARNER_EXAMPLE)
  test_learner.uuid = "test_learner"
  test_learner.save()

  test_learner_profile = LearnerProfile()
  test_learner_profile = test_learner_profile\
    .from_dict(BASIC_LEARNER_PROFILE_EXAMPLE)
  test_learner_profile.uuid = "test_learner_profile"
  test_learner_profile.learner_id = "test_learner"
  test_learner_profile.save()

  test_user = User()
  test_user = test_user.from_dict(TEST_USER)
  test_user.user_id = "2ivy523v5y6ynefn7a"
  test_user.user_type_ref = "test_learner"
  test_user.save()

  test_agent = Agent()
  test_agent = test_agent.from_dict(BASIC_AGENT_SCHEMA_EXAMPLE)
  test_agent.uuid = "2ivy523v5y6ynefn7a"
  test_agent.save()

  test_verb = Verb()
  test_verb = test_verb.from_dict(BASIC_VERB_MODEL_EXAMPLE)
  test_verb.uuid = "test_verb_id"
  test_verb.save()

  test_activity = Activity()
  test_activity = test_activity.from_dict(ACTIVITY_XAPI_EXAMPLE)
  test_activity.save()

  test_learning_experience = LearningExperience()
  test_learning_experience = test_learning_experience.from_dict(
      BASIC_LEARNING_EXPERIENCE_EXAMPLE)
  test_learning_experience.uuid = "oTkwe45fsrdfjhin"
  test_learning_experience.save()

  test_session = Session()
  test_session = test_session.from_dict(BASIC_SESSION_EXAMPLE)
  test_session.session_id = ""
  test_session.save()
  test_session.session_id = test_session.id
  test_session.update()
  session_id = test_session.id

  input_statement = {**BASIC_XAPI_STATEMENT}
  input_statement["session_id"] = session_id
  input_statements_list = [input_statement]
  url = f"{api_url}/statements"
  mocker.patch("routes.statement.insert_data_to_bq", return_value=True)
  resp = client_with_emulator.post(url, json=input_statements_list)
  resp_data = resp.json()
  assert resp.status_code == 200, "Status code is not 200"
  assert resp_data["success"] is True, "Success is not True"
  assert resp_data["message"] == "Successfully added the given statement/s"
  assert resp_data["data"][0], "No statement created"


def test_post_statements_negative():
  input_statement = {**BASIC_XAPI_STATEMENT}
  del input_statement["actor"]
  input_statements_list = [input_statement]
  url = f"{api_url}/statements"
  resp = client_with_emulator.post(url, json=input_statements_list)
  assert resp.status_code == 422
