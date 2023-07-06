"""
Establishing a relationship between the Assessment and Learning Experience
"""

import behave
import sys
import uuid
from copy import deepcopy

sys.path.append("../")
from e2e.setup import post_method, get_method, put_method
from e2e.test_config import API_URL_ASSESSMENT_SERVICE, API_URL_LEARNING_OBJECT_SERVICE, DEL_KEYS
from e2e.test_object_schemas import (TEST_PRACTICE_ASSESSMENT, TEST_LEARNING_EXPERIENCE)


# --- Positive Scenario ---
@behave.given(
    "that a LXE has access Learning Object Service and Assessment Service to establish relationship with LE")
def step_1_1(context):
  context.learning_experience_req_body = deepcopy(TEST_LEARNING_EXPERIENCE)
  context.assessment_req_body = deepcopy(TEST_PRACTICE_ASSESSMENT)
  for key in DEL_KEYS:
    if key in context.learning_experience_req_body:
      del context.learning_experience_req_body[key]
    if key in context.assessment_req_body:
      del context.assessment_req_body[key]

  context.learning_experience_url = f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-experience"
  context.assessment_url = f"{API_URL_ASSESSMENT_SERVICE}/assessment"


@behave.when(
    "API request is sent to create Assessment and Learning Experience with correct request payload"
)
def step_1_2(context):
  context.learning_experience_response = post_method(
      url=context.learning_experience_url,
      request_body=context.learning_experience_req_body)
  context.test_learning_experience = context.learning_experience_response.json()
  context.learning_experience_uuid = context.test_learning_experience['data']["uuid"]

  context.assessment_req_body["parent_nodes"]["learning_experiences"].append(
      context.learning_experience_uuid)
  context.assessment_response = post_method(
      url=context.assessment_url,
      request_body=context.assessment_req_body)
  context.test_assessment = context.assessment_response.json()

  context.learning_experience_get_response = get_method(
      url=context.learning_experience_url + "/" + context.learning_experience_uuid)
  context.learning_experience_get_object = context.learning_experience_get_response.json(
  )


@behave.then(
    "Assessment and Learning Experience will be created in the database")
def step_1_3(context):
  assert context.learning_experience_response.status_code == 200
  assert context.test_learning_experience["success"] is True
  assert "uuid" in context.test_learning_experience["data"]
  assert "created_time" in context.test_learning_experience["data"]
  assert "last_modified_time" in context.test_learning_experience["data"]
  assert context.assessment_response.status_code == 200
  assert context.test_assessment["success"] is True
  assert "uuid" in context.test_assessment["data"]
  assert "created_time" in context.test_assessment["data"]
  assert "last_modified_time" in context.test_assessment["data"]


@behave.then("Assessment gets associated with Learning Experience")
def step_1_4(context):
  assert context.learning_experience_uuid in context.test_assessment["data"][
      "parent_nodes"]["learning_experiences"]

  assert context.test_assessment["data"][
      "uuid"] in context.learning_experience_get_object["data"]["child_nodes"][
          "assessments"]


# --- Negative Scenario ---
@behave.given(
    "that an LXE create a Assessment providing the reference of the given Learning Experience with incorrect uuid"
)
def step_2_1(context):
  context.learning_experience_req_body = deepcopy(TEST_LEARNING_EXPERIENCE)
  context.assessment_req_body = deepcopy(TEST_PRACTICE_ASSESSMENT)
  for key in DEL_KEYS:
    if key in context.learning_experience_req_body:
      del context.learning_experience_req_body[key]
    if key in context.assessment_req_body:
      del context.assessment_req_body[key]

  context.learning_experience_url = f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-experience"
  context.assessment_url = f"{API_URL_ASSESSMENT_SERVICE}/assessment"


@behave.when("API request is sent to create Assessment and LE with incorrect reference")
def step_2_2(context):
  context.learning_experience_response = post_method(
      url=context.learning_experience_url,
      request_body=context.learning_experience_req_body)
  context.test_learning_experience = context.learning_experience_response.json()
  context.learning_experience_uuid = context.test_learning_experience['data']["uuid"]

  context.uuid = str(uuid.uuid4())
  context.assessment_req_body["parent_nodes"]["learning_experiences"].append(
      context.uuid)
  context.assessment_response = post_method(
      url=context.assessment_url,
      request_body=context.assessment_req_body)
  context.test_assessment = context.assessment_response.json()


@behave.then(
    "LXE will get an error message for the Learning Experience not found"
)
def step_2_3(context):
  assert context.learning_experience_response.status_code == 200
  assert context.test_learning_experience["success"] is True
  assert "uuid" in context.test_learning_experience["data"]
  assert "created_time" in context.test_learning_experience["data"]
  assert "last_modified_time" in context.test_learning_experience["data"]
  assert context.assessment_response.status_code == 404
  assert context.test_assessment[
      "message"] == f"Learning Experience with uuid {context.uuid} not found"


# --- Positive Scenario ---


@behave.given(
    "that an LXE  wants to replace an old reference of the Learning Experience with a new reference in the Assessment"
)
def step_3_1(context):
  context.learning_experience_req_body = deepcopy(TEST_LEARNING_EXPERIENCE)
  context.assessment_req_body = deepcopy(TEST_PRACTICE_ASSESSMENT)
  for key in DEL_KEYS:
    if key in context.learning_experience_req_body:
      del context.learning_experience_req_body[key]
    if key in context.assessment_req_body:
      del context.assessment_req_body[key]

  context.learning_experience_url = f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-experience"
  context.assessment_url = f"{API_URL_ASSESSMENT_SERVICE}/assessment"


@behave.when(
    "API request is sent to update the Assessment with new reference of Learning Experience"
)
def step_3_2(context):
  context.learning_experience_response_old = post_method(
      url=context.learning_experience_url,
      request_body=context.learning_experience_req_body)
  context.test_learning_experience_old = context.learning_experience_response_old.json()
  context.learning_experience_uuid_old = context.test_learning_experience_old['data'][
      "uuid"]

  context.assessment_req_body["parent_nodes"]["learning_experiences"] = [
      context.learning_experience_uuid_old
  ]
  context.assessment_response_old = post_method(
      url=context.assessment_url,
      request_body=context.assessment_req_body)
  context.test_assessment_old = context.assessment_response_old.json()

  context.learning_experience_response_new = post_method(
      url=context.learning_experience_url,
      request_body=context.learning_experience_req_body)
  context.test_learning_experience_new = context.learning_experience_response_new.json()
  context.learning_experience_uuid_new = context.test_learning_experience_new['data'][
      "uuid"]
  context.assessment_req_body["parent_nodes"]["learning_experiences"] = [
      context.learning_experience_uuid_new
  ]

  context.assessment_response_updated = put_method(
      url=context.assessment_url + "/" +
      context.test_assessment_old["data"]["uuid"],
      request_body=context.assessment_req_body)
  context.test_assessment_updated = context.assessment_response_updated.json(
  )
  context.learning_experience_get_response_old = get_method(
      url=context.learning_experience_url + "/" + context.learning_experience_uuid_old)
  context.learning_experience_get_object_old = context.learning_experience_get_response_old.json(
  )

  context.learning_experience_get_response_new = get_method(
      url=context.learning_experience_url + "/" + context.learning_experience_uuid_new)
  context.learning_experience_get_object_new = context.learning_experience_get_response_new.json(
  )


@behave.then("the Assessment gets associated with the new Learning Experience")
def step_3_3(context):
  assert context.learning_experience_response_new.status_code == 200
  assert context.test_learning_experience_new["success"] is True
  assert context.learning_experience_uuid_new in context.test_assessment_updated[
      "data"]["parent_nodes"]["learning_experiences"]
  assert context.learning_experience_uuid_old not in context.test_assessment_updated[
      "data"]["parent_nodes"]["learning_experiences"]

  assert context.test_assessment_updated["data"][
      "uuid"] not in context.learning_experience_get_object_old["data"][
          "child_nodes"]["assessments"]
  assert context.test_assessment_updated["data"][
      "uuid"] in context.learning_experience_get_object_new["data"]["child_nodes"][
          "assessments"]


# --- Negative Scenario ---


@behave.given(
    "that an LXE wants to add a reference to one more Learning Experience in the Assessment"
)
def step_4_1(context):
  context.learning_experience_req_body = deepcopy(TEST_LEARNING_EXPERIENCE)
  context.assessment_req_body = deepcopy(TEST_PRACTICE_ASSESSMENT)
  for key in DEL_KEYS:
    if key in context.learning_experience_req_body:
      del context.learning_experience_req_body[key]
    if key in context.assessment_req_body:
      del context.assessment_req_body[key]

  context.learning_experience_url = f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-experience"
  context.assessment_url = f"{API_URL_ASSESSMENT_SERVICE}/assessment"


@behave.when(
    "API request is sent to update the Assessment with incorrect reference of Learning Experience"
)
def step_4_2(context):
  context.learning_experience_response = post_method(
      url=context.learning_experience_url,
      request_body=context.learning_experience_req_body)
  context.test_learning_experience = context.learning_experience_response.json()
  context.learning_experience_uuid = context.test_learning_experience['data']["uuid"]

  context.assessment_response = post_method(
      url=context.assessment_url,
      request_body=context.assessment_req_body)
  context.test_assessment = context.assessment_response.json()

  context.uuid = str(uuid.uuid4())
  context.assessment_req_body["parent_nodes"]["learning_experiences"] = [
      context.uuid
  ]

  context.assessment_response_updated = put_method(
      url=context.assessment_url + "/" +
      context.test_assessment["data"]["uuid"],
      request_body=context.assessment_req_body)
  context.test_assessment_updated = context.assessment_response_updated.json(
  )


@behave.then(
    "the user gets error message of not found for the reference to the Learning Experience"
)
def step_4_3(context):
  assert context.learning_experience_response.status_code == 200
  assert context.test_learning_experience["success"] is True

  assert context.assessment_response_updated.status_code == 404
  assert context.test_assessment_updated[
      "message"] == f"Learning Experience with uuid {context.uuid} not found"


# --- Positive Scenario ---
@behave.given(
    "that an LXE or CD wants to update the reference of the Assessment in the Learning Experience"
)
def step_5_1(context):
  context.learning_experience_req_body = deepcopy(TEST_LEARNING_EXPERIENCE)
  context.assessment_req_body = deepcopy(TEST_PRACTICE_ASSESSMENT)
  for key in DEL_KEYS:
    if key in context.learning_experience_req_body:
      del context.learning_experience_req_body[key]
    if key in context.assessment_req_body:
      del context.assessment_req_body[key]

  context.learning_experience_url = f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-experience"
  context.assessment_url = f"{API_URL_ASSESSMENT_SERVICE}/assessment"


@behave.when(
    "they add the new reference and delete the old reference of the Assessment using an API request to Assessment Service"
)
def step_5_2(context):
  context.learning_experience_response = post_method(
      url=context.learning_experience_url,
      request_body=context.learning_experience_req_body)
  context.test_learning_experience = context.learning_experience_response.json()
  context.learning_experience_uuid = context.test_learning_experience['data']["uuid"]

  context.assessment_req_body["parent_nodes"]["learning_experiences"] = [
      context.learning_experience_uuid
  ]

  context.assessment_response_1 = post_method(
      url=context.assessment_url,
      request_body=context.assessment_req_body)
  context.test_assessment_1 = context.assessment_response_1.json()

  context.assessment_response_2 = post_method(
      url=context.assessment_url,
      request_body=context.assessment_req_body)
  context.test_assessment_2 = context.assessment_response_2.json()

  context.assessment_req_body["parent_nodes"]["learning_experiences"] = []
  context.assessment_response_updated_1 = put_method(
      url=context.assessment_url + "/" +
      context.test_assessment_2["data"]["uuid"],
      request_body=context.assessment_req_body)
  context.test_assessment_updated_1 = context.assessment_response_updated_1.json(
  )

  context.assessment_req_body["parent_nodes"]["learning_experiences"] = [
      context.learning_experience_uuid
  ]

  for key in DEL_KEYS:
    if key in context.assessment_req_body:
      del context.assessment_req_body[key]
  context.assessment_response_3 = post_method(
      url=context.assessment_url,
      request_body=context.assessment_req_body)
  context.test_assessment_3 = context.assessment_response_3.json()

  context.learning_experience_get_response = get_method(
      url=context.learning_experience_url + "/" + context.learning_experience_uuid)
  context.learning_experience_get_object = context.learning_experience_get_response.json(
  )


@behave.then(
    "the old Assessment will get untagged and the new Assessment will get tagged to the Learning Experience"
)
def step_5_3(context):
  assert context.test_assessment_1["data"][
      "uuid"] in context.learning_experience_get_object["data"]["child_nodes"][
          "assessments"]
  assert context.test_assessment_2["data"][
      "uuid"] not in context.learning_experience_get_object["data"]["child_nodes"][
          "assessments"]
  assert context.test_assessment_3["data"][
      "uuid"] in context.learning_experience_get_object["data"]["child_nodes"][
          "assessments"]
