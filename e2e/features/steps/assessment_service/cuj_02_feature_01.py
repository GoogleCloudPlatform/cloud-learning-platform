"""
Feature 01 - CRUD for managing Assessment model in Assessment items
"""

import sys
import os
import json
import behave

sys.path.append("../")
from e2e.setup import post_method, get_method, put_method, delete_method
from e2e.test_object_schemas import TEST_PRACTICE_ASSESSMENT, BASIC_HUMAN_GRADED_ASSESSMENT_EXAMPLE, TEST_SKILL
from e2e.test_config import API_URL_ASSESSMENT_SERVICE, TESTING_OBJECTS_PATH
from common.models import Skill, Assessment

API_URL = API_URL_ASSESSMENT_SERVICE


#-------------------------------CREATE------------------------------------------
# --- Positive Scenario ---
@behave.given(
    "that a LXE  has access to Assessment Service and need to create an Assessment"
)
def step_impl_1(context):
  test_assessment = {**TEST_PRACTICE_ASSESSMENT}
  context.assessment_dict = test_assessment
  context.url = f"{API_URL}/assessment"


@behave.when(
    "API request is sent to create an Assessment with correct request payload"
)
def step_impl_2(context):
  context.res = post_method(
      url=context.url, request_body=context.assessment_dict)
  context.res_data = context.res.json()


@behave.then("that Assessment object will be created in the database")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the assessment"
  assessment_uuid = context.res_data["data"]["uuid"]
  url = f"{API_URL}/assessment/{assessment_uuid}"
  get_resp = get_method(url)
  resp_json = get_resp.json()
  assert get_resp.status_code == 200
  assert resp_json["message"] == "Successfully fetched the assessment"


# --- Negative Scenario ---
@behave.given(
    "that a LXE has access to Assessment Service and need to create an Assessment"
)
def step_impl_1(context):
  context.payload = {
      "child_nodes": {},
      "assessment_reference":
          "/learnosity/bf3793a4-39dd-4b0c-b82b-a624489d4e25",
  }
  context.url = f"{API_URL}/assessment"


@behave.when(
    "API request is sent to create Assessment with incorrect request payload"
)
def step_impl_2(context):
  context.res = post_method(url=context.url, request_body=context.payload)
  context.res_data = context.res.json()


@behave.then(
    "Assessment object will not be created and Assessment Service will throw a Validation error"
)
def step_impl_3(context):
  assert context.res.status_code == 422
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Validation Failed"
  assert context.res_data["data"][0]["msg"] == "field required"
  assert context.res_data["data"][0]["type"] == "value_error.missing"


#-------------------------------GET---------------------------------------------
# --- Positive Scenario ---
@behave.given(
    "that a LXE has access to Assessment Service and need to fetch an Assessment"
)
def step_impl_1(context):
  context.test_assessment = {**TEST_PRACTICE_ASSESSMENT}
  url = f"{API_URL}/assessment"
  post_res = post_method(url=url, request_body=context.test_assessment)
  post_res_data = post_res.json()
  assessment_uuid = post_res_data["data"]["uuid"]
  context.url = f"{API_URL}/assessment/{assessment_uuid}"


@behave.when(
    "API request is sent to fetch the Assessment with correct Assessment id"
)
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then(
    "the Assessment Service will serve up the requested Assessment")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data[
      "message"] == "Successfully fetched the assessment"



# --- Read a particular Assessment and fetch all its child nodes using correct Assessment id
@behave.given(
    "that a LXE has access to Assessment Service and need to fetch an Assessment and all of its child nodes"
)
def step_impl_1(context):
  context.test_assessment = {**BASIC_HUMAN_GRADED_ASSESSMENT_EXAMPLE}
  url = f"{API_URL}/assessment/human-graded"
  post_res = post_method(url=url, request_body=context.test_assessment)
  post_res_data = post_res.json()
  assessment_uuid = post_res_data["data"]["uuid"]
  context.url = f"{API_URL}/assessment/{assessment_uuid}?fetch_tree=True"


@behave.when(
    "API request is sent to fetch the Assessment and its child nodes with correct Assessment id"
)
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()["data"]


@behave.then(
    "the Assessment Service will serve up the requested Assessment and its child nodes")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["name"] == context.test_assessment["name"]
  assert context.res_data["child_nodes"]["rubrics"][0]["name"] == \
    context.test_assessment["child_nodes"]["rubrics"][0]["name"]
  assert context.res_data["child_nodes"]["rubrics"][0]["child_nodes"]["rubric_criteria"][0]["name"] == \
    context.test_assessment["child_nodes"]["rubrics"][0]["child_nodes"]["rubric_criteria"][0]["name"]

# --- Negative Scenario ---
@behave.given(
    "that LXE has access to Assessment Service and need to fetch an Assessment"
)
def step_impl_1(context):
  invalid_assessment_uuid = "random_id"
  context.url = f"{API_URL}/assessment/{invalid_assessment_uuid}"


@behave.when(
    "API request is sent to fetch the Assessment with incorrect Assessment id"
)
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then(
    "the Assessment will not be fetched and Assessment Service will throw ResourceNotFound error"
)
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False, "Success is not False"
  assert context.res_data[
      "message"] == "Assessment with uuid random_id not found", "Expected message not returned"


#-------------------------------GET ALL-----------------------------------------
# --- Positive Scenario ---
@behave.given(
    "that a LXE has access to Assessment Service and needs to fetch all Assessment"
)
def step_impl_1(context):
  # Create a skill
  basic_skill = TEST_SKILL
  new_skill = Skill()
  new_skill = new_skill.from_dict(basic_skill)
  new_skill.uuid = ""
  new_skill.save()
  new_skill.uuid = new_skill.id
  new_skill.update()
  context.skill_data = [{"uuid": new_skill.uuid, "name": new_skill.name}]

  # Create assessments
  json_file_path = os.path.join(TESTING_OBJECTS_PATH, "assessment.json")
  assert os.path.exists(json_file_path)
  url = f"{API_URL}/assessment/import/json"
  with open(json_file_path, encoding="UTF-8") as assessment_json_file:
    post_res = post_method(url, files={"json_file": assessment_json_file})
    post_res_data = post_res.json()
    context.imported_assessment_ids = post_res_data["data"]
  context.url = f"{API_URL}/assessments"
  for assessment_id in context.imported_assessment_ids:
    assessment = Assessment.find_by_uuid(assessment_id)
    assessment.references = {"skills": context.skill_data}
    assessment.update()
  context.params = {"performance_indicators": [new_skill.uuid]}


@behave.when(
    "API request is sent to fetch all Assessment with correct query parameters"
)
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params={"is_autogradable": True})
  context.res_data = context.res.json()


@behave.then("the Assessment Service will show all the Assessment")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data[
      "message"] == "Successfully fetched the assessments"
  fetched_uuids = [i.get("uuid") for i in context.res_data.get("data")["records"]]
  assert set(context.imported_assessment_ids).intersection(set(fetched_uuids)) \
    == set(context.imported_assessment_ids), "all data not retrieved"
  for assessment in context.res_data.get("data")["records"]:
    assert assessment.get("references", {}).get("skills") == context.skill_data


# --- Negative Scenario ---
@behave.given(
    "that a LXE can access Assessment Service and needs to fetch all Assessment"
)
def step_impl_1(context):
  context.url = f"{API_URL}/assessments"
  context.params = {"skip": "-1", "limit": "10"}


@behave.when(
    "API request is sent to fetch all Assessment with incorrect query parameters"
)
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()


@behave.then(
    "the Assessment will not be fetched and Assessment Service will throw a Validation error"
)
def step_impl_3(context):
  assert context.res.status_code == 422, "Status not 422"
  assert context.res_data.get("message") == \
    "Validation Failed", \
    "unknown response received"


#-------------------------------UPDATE------------------------------------------
# --- Positive Scenario ---
@behave.given(
    "that a LXE has access to Assessment Service and needs to update an Assessment"
)
def step_impl_1(context):
  context.test_assessment = {**TEST_PRACTICE_ASSESSMENT}
  url = f"{API_URL}/assessment"
  post_res = post_method(url=url, request_body=context.test_assessment)
  post_res_data = post_res.json()
  assessment_uuid = post_res_data["data"]["uuid"]
  context.url = f"{API_URL}/assessment/{assessment_uuid}"


@behave.when(
    "API request is sent to update the Assessment with correct request payload"
)
def step_impl_2(context):
  updated_data = context.test_assessment
  updated_data["name"] = "test_update"
  context.res = put_method(url=context.url, request_body=updated_data)
  context.res_data = context.res.json()


@behave.then("that Assessment will be updated in the database")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data[
      "message"] == "Successfully updated the assessment"
  assert context.res_data["data"]["name"] == "test_update"


# --- Negative Scenario ---
@behave.given(
    "that a LXE can access Assessment Service and needs to update an Assessment"
)
def step_impl_1(context):
  invalid_assessment_uuid = "random_id"
  context.url = f"{API_URL}/assessment/{invalid_assessment_uuid}"


@behave.when(
    "API request is sent to update the Assessment with incorrect Assessment id"
)
def step_impl_2(context):
  correct_payload = {"name": "test update1"}
  context.res = put_method(url=context.url, request_body=correct_payload)
  context.res_data = context.res.json()


@behave.then(
    "the Assessment will not be updated and Assessment Service will throw ResourceNotFound error"
)
def step_impl_3(context):
  context.res_data = context.res.json()
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data[
      "message"] == "Assessment with uuid random_id not found"


#-------------------------------DELETE------------------------------------------
# --- Positive Scenario ---
@behave.given(
    "that a LXE has access to Assessment Service and needs to delete an Assessment"
)
def step_impl_1(context):
  context.test_assessment = {**TEST_PRACTICE_ASSESSMENT}
  url = f"{API_URL}/assessment"
  post_res = post_method(url=url, request_body=context.test_assessment)
  post_res_data = post_res.json()
  assessment_uuid = post_res_data["data"]["uuid"]
  context.url = f"{API_URL}/assessment/{assessment_uuid}"


@behave.when(
    "API request is sent to delete the Assessment with correct Assessment id"
)
def step_impl_2(context):
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("that Assessment will be deleted from the database")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data[
      "message"] == "Successfully deleted the assessment"
  get_resp = get_method(url=context.url)
  assert get_resp.status_code == 404, "Assessment not deleted"


# --- Negative Scenario ---
@behave.given(
    "that a LXE can access Assessment Service and needs to delete an Assessment"
)
def step_impl_1(context):
  invalid_assessment_uuid = "random_id"
  context.url = f"{API_URL}/assessment/{invalid_assessment_uuid}"


@behave.when(
    "API request is sent to delete the Assessment with incorrect Assessment id"
)
def step_impl_2(context):
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()


@behave.then(
    "the Assessment will not be deleted and Assessment Service will throw ResourceNotFound error"
)
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data[
      "message"] == "Assessment with uuid random_id not found"


#-------------------------------IMPORT------------------------------------------
# --- Positive Scenario ---
@behave.given(
    "that a LXE has access to Assessment Service and needs to import Assessment from JSON file"
)
def step_impl_1(context):
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH,
                                        "assessment.json")
  assert os.path.exists(context.json_file_path)
  context.url = f"{API_URL}/assessment/import/json"


@behave.when(
    "the Assessment are imported from correct JSON in request payload")
def step_impl_2(context):
  with open(
      context.json_file_path, encoding="UTF-8") as assessment_json_file:
    context.res = post_method(
        context.url, files={"json_file": assessment_json_file})
    context.res_data = context.res.json()


@behave.then("those Assessment will be added in the database")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data[
      "message"] == "Successfully created the assessment"
  get_assessment_url = f"{API_URL}/assessment/{context.res_data['data'][0]}"
  get_res = get_method(get_assessment_url)
  get_res_data = get_res.json()
  assert get_res_data["data"]["uuid"] == context.res_data['data'][0], "Data not created successfully"


# --- Negative Scenario ---
@behave.given(
    "that a LXE can access Assessment Service and needs to import Assessment from JSON file"
)
def step_impl_1(context):
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH,
                                        "assessment_invalid.json")
  assert os.path.exists(context.json_file_path)
  context.url = f"{API_URL}/assessment/import/json"


@behave.when(
    "the Assessment are imported from incorrect JSON in request payload")
def step_impl_2(context):
  with open(
      context.json_file_path, encoding="UTF-8") as assessment_json_file:
    context.res = post_method(
        context.url, files={"json_file": assessment_json_file})
    context.res_data = context.res.json()


@behave.then(
    "the Assessment will not be imported and Assessment Service will throw Validation error"
)
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False, "Success is not True"
