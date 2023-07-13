"""
Creation and authoring of Human Graded Assessments
"""

import sys
import copy
import behave
from uuid import uuid4

sys.path.append("../")
from e2e.setup import post_method, get_method, put_method
from e2e.test_object_schemas import (BASIC_HUMAN_GRADED_ASSESSMENT_EXAMPLE, TEST_USER,
                                TEST_SKILL,UPDATE_HUMAN_GRADED_ASSESSMENT_EXAMPLE)
from e2e.test_config import API_URL_ASSESSMENT_SERVICE
from common.models import Rubric, RubricCriterion, User, Skill
from environment import TEST_ASSESSMENT_SUBMISSION_FILE_PATH

API_URL = API_URL_ASSESSMENT_SERVICE

# CREATE A HUMAN GRADED ASSESSMENT
# POSTIVE SCENARIO

@behave.given(
    "that a LXE  has access to Assessment Service and need to create a Human Graded Assessment"
)
def step_impl_1(context):

  # Create a User for the LXE
  user_dict = {**TEST_USER}
  user_dict["email"] = f"{uuid4()}@gmail.com"
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.user_type_ref =  ""
  user.update()

  skill_dict = {**TEST_SKILL}
  skill = Skill.from_dict(skill_dict)
  skill.uuid = ""
  skill.save()
  skill.uuid = skill.id
  skill.update()
  context.skill_id = skill.id
  context.user_id = user.user_id

  # Upload an assessment resource file by that LXE
  content_file = open(TEST_ASSESSMENT_SUBMISSION_FILE_PATH,"rb")
  content_file_input_dict = {"content_file":
              ("sample_assessment_authoring.txt", content_file, "text/plain")}

  content_res = post_method(
            url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-authoring/upload-sync/{context.user_id}",
            files=content_file_input_dict,
            )
  res_json = content_res.json()
  status_code = content_res.status_code
  assert status_code == 200
  assert res_json["success"] is True
  assert res_json["message"] == "Successfully uploaded file"

  temporary_file_path = f"assessments/{context.user_id}"
  temporary_file_path+="/temp/sample_assessment_authoring.txt"

  assert res_json["data"]["resource_path"] == temporary_file_path

  test_human_graded_assessment = {**BASIC_HUMAN_GRADED_ASSESSMENT_EXAMPLE}
  test_human_graded_assessment["child_nodes"]["rubrics"][0]["child_nodes"]["rubric_criteria"][0]["performance_indicators"] = [context.skill_id]
  test_human_graded_assessment["resource_paths"] = [temporary_file_path]
  test_human_graded_assessment["author_id"] = context.user_id
  context.assessment_dict = test_human_graded_assessment
  context.url = f"{API_URL}/assessment/human-graded"

@behave.when(
    "API request is sent to create a HUman Graded Assessment with correct request payload"
)
def step_impl_2(context):
  context.res = post_method(
      url=context.url, request_body=context.assessment_dict)
  context.res_data = context.res.json()

@behave.then("that Human Graded Assessment object will be created in the database with skills updated from rubric_criteria")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the assessment"
  context.assessment_uuid = context.res_data["data"]["uuid"]
  url = f"{API_URL}/assessment/{context.assessment_uuid}"
  get_resp = get_method(url)
  context.resp_json = get_resp.json()
  assert get_resp.status_code == 200
  assert context.resp_json["data"]["references"]["skills"] == [context.skill_id]
  assert context.resp_json["message"] == "Successfully fetched the assessment"

@behave.then("the assessment resources are moved to a proper gcs path")
def step_impl_4(context):
  context.resource_paths = context.resp_json["data"]["resource_paths"]
  expected_file_path = f"assessments/{context.user_id}"
  expected_file_path+=\
      f"/{context.assessment_uuid}/sample_assessment_authoring.txt"
  assert context.resp_json["data"]["resource_paths"] == [expected_file_path]


@behave.then("the child Rubric would also also be created and linked")
def step_impl_5(context):
  context.rubric_uuid = context.resp_json["data"]["child_nodes"]["rubrics"][0]
  rubric=Rubric.find_by_uuid(context.rubric_uuid)
  context.rubric_fields = rubric.get_fields(reformat_datetime=True)
  print(context.rubric_fields)
  context.rubric_data = context.assessment_dict["child_nodes"]["rubrics"][0]
  assert context.rubric_fields["name"] == context.rubric_data["name"]
  assert context.rubric_fields["description"] == context.rubric_data["description"]
  assert context.rubric_fields["author"] == context.rubric_data["author"]
  assert context.rubric_fields["parent_nodes"]["assessments"][0] == context.res_data["data"]["uuid"]
  

@behave.then("the leaf Rubric criterion will also be created and updated")
def step_impl_6(context):
  rubric_criteria_uuid = context.rubric_fields["child_nodes"]["rubric_criteria"][0]
  rubric_criteria = RubricCriterion.find_by_uuid(rubric_criteria_uuid)
  rubric_criteria_fields = rubric_criteria.get_fields(reformat_datetime=True)
  assert rubric_criteria_fields["name"] == context.rubric_data["child_nodes"]["rubric_criteria"][0]["name"]
  assert rubric_criteria_fields["description"] == context.rubric_data["child_nodes"]["rubric_criteria"][0]["description"]
  assert rubric_criteria_fields["author"] == context.rubric_data["child_nodes"]["rubric_criteria"][0]["author"]
  assert rubric_criteria_fields["parent_nodes"]["rubrics"][0] == context.rubric_uuid

# NEGAITVE SCENARIO
@behave.given(
    "that a LXE has access to Assessment Service but has an incorrect payload to create a Human Graded Assessment"
)
def step_impl_1(context):
  context.payload = {
    "description": "Assessmetn description",
    "child_nodes": {}
  }
  context.url = f"{API_URL}/assessment/human-graded"


@behave.when(
  "API request is sent to create a Human Graded Assessment with incorrect payload"
)
def step_impl_2(context):
  context.res = post_method(url=context.url, request_body=context.payload)
  context.res_data = context.res.json()


@behave.then(
    "Human Graded Assessment object will not be created and will throw a validation error"
)
def step_impl_3(context):
  assert context.res.status_code == 422
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Validation Failed"
  assert context.res_data["data"][0]["msg"] == "field required"
  assert context.res_data["data"][0]["type"] == "value_error.missing"


# UPDATE A HUMAN GRADED ASSESSMENT
# POSTIVE SCENARIO

@behave.given(
    "that a LXE  has access to Assessment Service and has created a Human Graded Assessment"
)
def step_impl_1(context):

  # Create a User for the LXE
  user_dict = {**TEST_USER}
  user_dict["email"] = f"{uuid4()}@gmail.com"
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  context.user_id = user.user_id

  # Upload an assessment resource file by that LXE
  content_file = open(TEST_ASSESSMENT_SUBMISSION_FILE_PATH,"rb")
  content_file_input_dict = {"content_file":
              ("sample_assessment_authoring.txt", content_file, "text/plain")}

  content_res = post_method(
            url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-authoring/upload-sync/{context.user_id}",
            files=content_file_input_dict,
            )
  res_json = content_res.json()
  status_code = content_res.status_code
  assert status_code == 200
  assert res_json["success"] is True
  assert res_json["message"] == "Successfully uploaded file"

  temporary_file_path = f"assessments/{context.user_id}"
  temporary_file_path+="/temp/sample_assessment_authoring.txt"

  assert res_json["data"]["resource_path"] == temporary_file_path

  test_human_graded_assessment = {**BASIC_HUMAN_GRADED_ASSESSMENT_EXAMPLE}
  test_human_graded_assessment["resource_paths"] = [temporary_file_path]
  test_human_graded_assessment["author_id"] = context.user_id
  context.assessment_dict = test_human_graded_assessment
  context.url = f"{API_URL}/assessment/human-graded"

  context.res = post_method(
      url=context.url, request_body=context.assessment_dict)
  context.res_data = context.res.json()
  assert context.res.status_code == 200, "Creation status failed"

  #Update request
  context.update_request = {
  "name": "Assessment 22",
  "type": "practice",
  "order": 3,
  "author_id": "sme author",
  "instructor_id": "sme",
  "assessor_id": "assessor_id",
  "alias": "assessment"
}

@behave.when(
    "API request is sent to update a Human Graded Assessment with correct request payload"
)
def step_impl_2(context):
  assessment_uuid = context.res_data["data"]["uuid"]
  update_url = f"{API_URL}/assessment/human-graded/{assessment_uuid}"
  context.update_res = put_method(
      url=update_url, request_body=context.update_request)
  context.update_res_data = context.update_res.json()

@behave.then("that Human Graded Assessment object will be updated corrrectly in the database")
def step_impl_3(context):
  assert context.update_res.status_code == 200
  assert context.update_res_data["message"] == "Successfully updated the assessment"
  context.assessment_uuid = context.res_data["data"]["uuid"]

  #Fetch the updated assessment
  url = f"{API_URL}/assessment/{context.assessment_uuid}"
  get_resp = get_method(url)
  context.resp_json = get_resp.json()
  assert get_resp.status_code == 200
  assert context.resp_json["message"] == "Successfully fetched the assessment"

  assert context.resp_json["data"]["name"] == context.update_request["name"], "Name not updated successfully"
  assert context.resp_json["data"]["author_id"] == context.update_request["author_id"], "author_id not updated successfully"
  assert context.resp_json["data"]["instructor_id"] == context.update_request["instructor_id"], "instructor_id not updated successfully"


# UPDATE A HUMAN GRADED ASSESSMENT WITH RUBRIC AND RUBRIC_CRITERION UPDATE
# POSTIVE SCENARIO

@behave.given(
    "that a LXE  has access to Assessment Service and has created a Human Graded Assessment with rubric details"
)
def step_impl_1(context):

  # Create a User for the LXE
  user_dict = {**TEST_USER}
  user_dict["email"] = f"{uuid4()}@gmail.com"
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  context.user_id = user.user_id

  # Upload an assessment resource file by that LXE
  content_file = open(TEST_ASSESSMENT_SUBMISSION_FILE_PATH,"rb")
  content_file_input_dict = {"content_file":
              ("sample_assessment_authoring.txt", content_file, "text/plain")}

  content_res = post_method(
            url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-authoring/upload-sync/{context.user_id}",
            files=content_file_input_dict,
            )
  res_json = content_res.json()
  status_code = content_res.status_code
  assert status_code == 200
  assert res_json["success"] is True
  assert res_json["message"] == "Successfully uploaded file"

  temporary_file_path = f"assessments/{context.user_id}"
  temporary_file_path+="/temp/sample_assessment_authoring.txt"

  assert res_json["data"]["resource_path"] == temporary_file_path

  test_human_graded_assessment = {**BASIC_HUMAN_GRADED_ASSESSMENT_EXAMPLE}
  test_human_graded_assessment["resource_paths"] = [temporary_file_path]
  test_human_graded_assessment["author_id"] = context.user_id
  context.assessment_dict = test_human_graded_assessment
  context.url = f"{API_URL}/assessment/human-graded"

  context.res = post_method(
      url=context.url, request_body=context.assessment_dict)
  context.res_data = context.res.json()
  assert context.res.status_code == 200, "Creation status failed"
  context.existing_rubric_uuid = context.res_data["data"]["child_nodes"]["rubrics"][0]

  rubric_criteria_get_url = f"{API_URL}/rubric/{context.existing_rubric_uuid}"
  get_result = get_method(rubric_criteria_get_url)
  get_result_data = get_result.json()
  context.existing_rubric_criteria_uuid = get_result_data["data"]["child_nodes"]["rubric_criteria"][0]

  #Update request
  context.update_request = copy.deepcopy(UPDATE_HUMAN_GRADED_ASSESSMENT_EXAMPLE)
  context.update_request["child_nodes"]["rubrics"][0]["uuid"] = context.existing_rubric_uuid
  context.update_request["child_nodes"]["rubrics"][0]["child_nodes"]["rubric_criteria"][0]["uuid"] = context.existing_rubric_criteria_uuid

@behave.when(
    "API request is sent to update a Human Graded Assessment with updates to existing and new rubric and rubric_criteria"
)
def step_impl_2(context):
  assessment_uuid = context.res_data["data"]["uuid"]
  update_url = f"{API_URL}/assessment/human-graded/{assessment_uuid}"
  context.update_res = put_method(
      url=update_url, request_body=context.update_request)
  context.update_res_data = context.update_res.json()

@behave.then("that Human Graded Assessment object will be updated with the list of old and new rubrics")
def step_impl_3(context):
  assert context.existing_rubric_uuid in context.update_res_data["data"]["child_nodes"]["rubrics"], "Old rubric uuid has been removed"
  assert len(context.update_res_data["data"]["child_nodes"]["rubrics"]) == 2, "New rubric has been added"

@behave.then("the old rubrics will be updated and new rubrics will be created")
def step_imple_4(context):
  #Assertions for the old rubrics
  rubric_get_url = f"{API_URL}/rubric/{context.existing_rubric_uuid}"
  rubric_get = get_method(rubric_get_url)
  rubric_get_data = rubric_get.json()

  assert rubric_get_data["data"]["name"] == context.update_request["child_nodes"]["rubrics"][0]["name"]
  assert rubric_get_data["data"]["description"] == context.update_request["child_nodes"]["rubrics"][0]["description"]

  #Assertions for the new rubrics
  new_rubric_uuid = context.update_res_data["data"]["child_nodes"]["rubrics"][1]
  rubric_get_url = f"{API_URL}/rubric/{new_rubric_uuid}"
  rubric_get = get_method(rubric_get_url)
  rubric_get_data = rubric_get.json()

  assert rubric_get_data["data"]["name"] == context.update_request["child_nodes"]["rubrics"][1]["name"]
  assert rubric_get_data["data"]["description"] == context.update_request["child_nodes"]["rubrics"][1]["description"]
