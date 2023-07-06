"""
Establishing a relationship between the Assessment and Learning Object
"""

import behave
import sys
import uuid
from copy import deepcopy

sys.path.append("../")
from e2e.setup import post_method, get_method, put_method
from e2e.test_config import API_URL_ASSESSMENT_SERVICE, API_URL_LEARNING_OBJECT_SERVICE, DEL_KEYS
from e2e.test_object_schemas import (TEST_PRACTICE_ASSESSMENT, TEST_LEARNING_OBJECT,TEST_LEARNING_RESOURCE,
                                 BASIC_HUMAN_GRADED_ASSESSMENT_EXAMPLE)


# --- Positive Scenario ---
@behave.given(
    "that a LXE has access Learning Object Service and Assessment Service")
def step_1_1(context):
  context.learning_object_req_body = deepcopy(TEST_LEARNING_OBJECT)
  context.assessment_req_body = deepcopy(TEST_PRACTICE_ASSESSMENT)
  for key in DEL_KEYS:
    if key in context.learning_object_req_body:
      del context.learning_object_req_body[key]
    if key in context.assessment_req_body:
      del context.assessment_req_body[key]

  context.learning_object_url = f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-object"
  context.assessment_url = f"{API_URL_ASSESSMENT_SERVICE}/assessment"


@behave.when(
    "API request is sent to create Assessment and Learning Object with correct request payload"
)
def step_1_2(context):
  context.learning_object_response = post_method(
      url=context.learning_object_url,
      request_body=context.learning_object_req_body)
  context.test_learning_object = context.learning_object_response.json()
  context.learning_object_uuid = context.test_learning_object['data']["uuid"]

  context.assessment_req_body["parent_nodes"]["learning_objects"].append(
      context.learning_object_uuid)
  context.assessment_response = post_method(
      url=context.assessment_url,
      request_body=context.assessment_req_body)
  context.test_assessment = context.assessment_response.json()

  context.learning_object_get_response = get_method(
      url=context.learning_object_url + "/" + context.learning_object_uuid)
  context.learning_object_get_object = context.learning_object_get_response.json(
  )


@behave.then(
    "Assessment and Learning Object will be created in the database")
def step_1_3(context):
  assert context.learning_object_response.status_code == 200
  assert context.test_learning_object["success"] is True
  assert "uuid" in context.test_learning_object["data"]
  assert "created_time" in context.test_learning_object["data"]
  assert "last_modified_time" in context.test_learning_object["data"]
  assert context.assessment_response.status_code == 200
  assert context.test_assessment["success"] is True
  assert "uuid" in context.test_assessment["data"]
  assert "created_time" in context.test_assessment["data"]
  assert "last_modified_time" in context.test_assessment["data"]


@behave.then("Assessment gets associated with Learning Object")
def step_1_4(context):
  assert context.learning_object_uuid in context.test_assessment["data"][
      "parent_nodes"]["learning_objects"]

  assert context.test_assessment["data"][
      "uuid"] in context.learning_object_get_object["data"]["child_nodes"][
          "assessments"]


# --- Negative Scenario ---
@behave.given(
    "that an LXE create a Assessment providing the reference of the given Learning Object with incorrect uuid"
)
def step_2_1(context):
  context.learning_object_req_body = deepcopy(TEST_LEARNING_OBJECT)
  context.assessment_req_body = deepcopy(TEST_PRACTICE_ASSESSMENT)
  for key in DEL_KEYS:
    if key in context.learning_object_req_body:
      del context.learning_object_req_body[key]
    if key in context.assessment_req_body:
      del context.assessment_req_body[key]

  context.learning_object_url = f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-object"
  context.assessment_url = f"{API_URL_ASSESSMENT_SERVICE}/assessment"


@behave.when("API request is sent to create Assessment")
def step_2_2(context):
  context.learning_object_response = post_method(
      url=context.learning_object_url,
      request_body=context.learning_object_req_body)
  context.test_learning_object = context.learning_object_response.json()
  context.learning_object_uuid = context.test_learning_object['data']["uuid"]

  context.uuid = str(uuid.uuid4())
  context.assessment_req_body["parent_nodes"]["learning_objects"].append(
      context.uuid)
  context.assessment_response = post_method(
      url=context.assessment_url,
      request_body=context.assessment_req_body)
  context.test_assessment = context.assessment_response.json()


@behave.then(
    "the LXE will get an error message of not found the reference to the Learning Object"
)
def step_2_3(context):
  assert context.learning_object_response.status_code == 200
  assert context.test_learning_object["success"] is True
  assert "uuid" in context.test_learning_object["data"]
  assert "created_time" in context.test_learning_object["data"]
  assert "last_modified_time" in context.test_learning_object["data"]

  assert context.assessment_response.status_code == 404
  assert context.test_assessment[
      "message"] == f"Learning Object with uuid {context.uuid} not found"


# --- Positive Scenario ---


@behave.given(
    "that an LXE  wants to replace an old reference of the Learning Object with a new reference in the Assessment"
)
def step_3_1(context):
  context.learning_object_req_body = deepcopy(TEST_LEARNING_OBJECT)
  context.assessment_req_body = deepcopy(TEST_PRACTICE_ASSESSMENT)
  for key in DEL_KEYS:
    if key in context.learning_object_req_body:
      del context.learning_object_req_body[key]
    if key in context.assessment_req_body:
      del context.assessment_req_body[key]

  context.learning_object_url = f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-object"
  context.assessment_url = f"{API_URL_ASSESSMENT_SERVICE}/assessment"


@behave.when(
    "API request is sent to update the Assessment with new reference of Learning Object"
)
def step_3_2(context):
  context.learning_object_response_old = post_method(
      url=context.learning_object_url,
      request_body=context.learning_object_req_body)
  context.test_learning_object_old = context.learning_object_response_old.json()
  context.learning_object_uuid_old = context.test_learning_object_old['data'][
      "uuid"]

  context.assessment_req_body["parent_nodes"]["learning_objects"] = [
      context.learning_object_uuid_old
  ]
  context.assessment_response_old = post_method(
      url=context.assessment_url,
      request_body=context.assessment_req_body)
  context.test_assessment_old = context.assessment_response_old.json()

  context.learning_object_response_new = post_method(
      url=context.learning_object_url,
      request_body=context.learning_object_req_body)
  context.test_learning_object_new = context.learning_object_response_new.json()
  context.learning_object_uuid_new = context.test_learning_object_new['data'][
      "uuid"]
  context.assessment_req_body["parent_nodes"]["learning_objects"] = [
      context.learning_object_uuid_new
  ]

  context.assessment_response_updated = put_method(
      url=context.assessment_url + "/" +
      context.test_assessment_old["data"]["uuid"],
      request_body=context.assessment_req_body)
  context.test_assessment_updated = context.assessment_response_updated.json(
  )
  context.learning_object_get_response_old = get_method(
      url=context.learning_object_url + "/" + context.learning_object_uuid_old)
  context.learning_object_get_object_old = context.learning_object_get_response_old.json(
  )

  context.learning_object_get_response_new = get_method(
      url=context.learning_object_url + "/" + context.learning_object_uuid_new)
  context.learning_object_get_object_new = context.learning_object_get_response_new.json(
  )


@behave.then("the Assessment gets associated with the new Learning Object")
def step_3_3(context):
  assert context.learning_object_response_new.status_code == 200
  assert context.test_learning_object_new["success"] is True
  assert context.learning_object_uuid_new in context.test_assessment_updated[
      "data"]["parent_nodes"]["learning_objects"]
  assert context.learning_object_uuid_old not in context.test_assessment_updated[
      "data"]["parent_nodes"]["learning_objects"]

  assert context.test_assessment_updated["data"][
      "uuid"] not in context.learning_object_get_object_old["data"][
          "child_nodes"]["assessments"]
  assert context.test_assessment_updated["data"][
      "uuid"] in context.learning_object_get_object_new["data"]["child_nodes"][
          "assessments"]


# --- Negative Scenario ---


@behave.given(
    "that an LXE wants to add a reference to one more Learning Object in the Assessment"
)
def step_4_1(context):
  context.learning_object_req_body = deepcopy(TEST_LEARNING_OBJECT)
  context.assessment_req_body = deepcopy(TEST_PRACTICE_ASSESSMENT)
  for key in DEL_KEYS:
    if key in context.learning_object_req_body:
      del context.learning_object_req_body[key]
    if key in context.assessment_req_body:
      del context.assessment_req_body[key]

  context.learning_object_url = f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-object"
  context.assessment_url = f"{API_URL_ASSESSMENT_SERVICE}/assessment"


@behave.when(
    "API request is sent to update the Assessment with incorrect reference of Learning Object"
)
def step_4_2(context):
  context.learning_object_response = post_method(
      url=context.learning_object_url,
      request_body=context.learning_object_req_body)
  context.test_learning_object = context.learning_object_response.json()
  context.learning_object_uuid = context.test_learning_object['data']["uuid"]

  context.assessment_response = post_method(
      url=context.assessment_url,
      request_body=context.assessment_req_body)
  context.test_assessment = context.assessment_response.json()

  context.uuid = str(uuid.uuid4())
  context.assessment_req_body["parent_nodes"]["learning_objects"] = [
      context.uuid
  ]

  context.assessment_response_updated = put_method(
      url=context.assessment_url + "/" +
      context.test_assessment["data"]["uuid"],
      request_body=context.assessment_req_body)
  context.test_assessment_updated = context.assessment_response_updated.json(
  )


@behave.then(
    "the user gets error message of not found the reference to the Learning Object"
)
def step_4_3(context):
  assert context.learning_object_response.status_code == 200
  assert context.test_learning_object["success"] is True

  assert context.assessment_response_updated.status_code == 404
  assert context.test_assessment_updated[
      "message"] == f"Learning Object with uuid {context.uuid} not found"


# --- Positive Scenario ---
@behave.given(
    "that an LXE or CD wants to update the reference of the Assessment in the Learning Object"
)
def step_5_1(context):
  context.learning_object_req_body = deepcopy(TEST_LEARNING_OBJECT)
  context.assessment_req_body = deepcopy(TEST_PRACTICE_ASSESSMENT)
  for key in DEL_KEYS:
    if key in context.learning_object_req_body:
      del context.learning_object_req_body[key]
    if key in context.assessment_req_body:
      del context.assessment_req_body[key]

  context.learning_object_url = f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-object"
  context.assessment_url = f"{API_URL_ASSESSMENT_SERVICE}/assessment"


@behave.when(
    "they add the new reference and delete the old reference of the Assessment using an API request"
)
def step_5_2(context):
  context.learning_object_response = post_method(
      url=context.learning_object_url,
      request_body=context.learning_object_req_body)
  context.test_learning_object = context.learning_object_response.json()
  context.learning_object_uuid = context.test_learning_object['data']["uuid"]

  context.assessment_req_body["parent_nodes"]["learning_objects"] = [
      context.learning_object_uuid
  ]

  context.assessment_response_1 = post_method(
      url=context.assessment_url,
      request_body=context.assessment_req_body)
  context.test_assessment_1 = context.assessment_response_1.json()

  context.assessment_response_2 = post_method(
      url=context.assessment_url,
      request_body=context.assessment_req_body)
  context.test_assessment_2 = context.assessment_response_2.json()

  context.assessment_req_body["parent_nodes"]["learning_objects"] = []
  context.assessment_response_updated_1 = put_method(
      url=context.assessment_url + "/" +
      context.test_assessment_2["data"]["uuid"],
      request_body=context.assessment_req_body)
  context.test_assessment_updated_1 = context.assessment_response_updated_1.json(
  )

  context.assessment_req_body["parent_nodes"]["learning_objects"] = [
      context.learning_object_uuid
  ]

  for key in DEL_KEYS:
    if key in context.assessment_req_body:
      del context.assessment_req_body[key]
  context.assessment_response_3 = post_method(
      url=context.assessment_url,
      request_body=context.assessment_req_body)
  context.test_assessment_3 = context.assessment_response_3.json()

  context.learning_object_get_response = get_method(
      url=context.learning_object_url + "/" + context.learning_object_uuid)
  context.learning_object_get_object = context.learning_object_get_response.json(
  )


@behave.then(
    "the old Assessment will get untagged and the new Assessment will get tagged to the Learning Object"
)
def step_5_3(context):
  assert context.test_assessment_1["data"][
      "uuid"] in context.learning_object_get_object["data"]["child_nodes"][
          "assessments"]
  assert context.test_assessment_2["data"][
      "uuid"] not in context.learning_object_get_object["data"]["child_nodes"][
          "assessments"]
  assert context.test_assessment_3["data"][
      "uuid"] in context.learning_object_get_object["data"]["child_nodes"][
          "assessments"]


# Scenario: LXE wants to link an authored assessment to a placeholder assessment in the heirarchy
@behave.given(
  "there exists a learning heirarchy with a placeholder assessment and a new authored assessment has been created")
def step_6_1(context):
  context.learning_object_req_body = deepcopy(TEST_LEARNING_OBJECT)
  context.assessment_req_body = deepcopy(TEST_PRACTICE_ASSESSMENT)
  context.learning_resource_req_body = deepcopy(TEST_LEARNING_RESOURCE)
  context.human_graded_assessment_req_body = deepcopy(BASIC_HUMAN_GRADED_ASSESSMENT_EXAMPLE)

  for key in DEL_KEYS:
    if key in context.learning_object_req_body:
      del context.learning_object_req_body[key]
    if key in context.assessment_req_body:
      del context.assessment_req_body[key]
    if key in context.learning_resource_req_body:
      del context.learning_resource_req_body[key]

  context.learning_object_url = f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-object"
  context.assessment_url = f"{API_URL_ASSESSMENT_SERVICE}/assessment"
  context.learning_resource_url = f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-resource"
  context.human_graded_assessment_url = f"{API_URL_ASSESSMENT_SERVICE}/assessment/human-graded"
  
  #Creating the parent learning object
  context.learning_object_response = post_method(
    url=context.learning_object_url,
    request_body=context.learning_object_req_body)
  context.test_learning_object = context.learning_object_response.json()
  context.learning_object_uuid = context.test_learning_object['data']["uuid"]

  #Creating the child nodes
  #Creating order 1 LR
  context.learning_resource_req_body["parent_nodes"]["learning_objects"].append(
    context.learning_object_uuid)
  context.learning_resource_req_body["order"] = 1
  
  context.learning_resource_response = post_method(
    url=context.learning_resource_url,
    request_body=context.learning_resource_req_body)
  context.learning_resource_1 = context.learning_resource_response.json()
  context.learning_resource_1_uuid = context.learning_resource_1['data']["uuid"]
  
  #Creating order 2 placeholder assessment
  context.assessment_req_body["parent_nodes"]["learning_objects"].append(
    context.learning_object_uuid)
  context.assessment_req_body["order"] = 2
  context.assessment_req_body["prerequisites"]["learning_resources"].append(context.learning_resource_1_uuid)

  context.placeholder_assessment_response = post_method(
    url=context.assessment_url,
    request_body=context.assessment_req_body)
  context.placeholder_assessment = context.placeholder_assessment_response.json()
  context.placeholder_assessment_uuid = context.placeholder_assessment['data']["uuid"]

  #Creating order 3 learning resource
  context.learning_resource_2_req_body = deepcopy(context.learning_resource_req_body)
  context.learning_resource_2_req_body["parent_nodes"]["learning_objects"].append(
    context.learning_object_uuid)
  context.learning_resource_2_req_body["order"] = 3
  context.learning_resource_2_req_body["prerequisites"]["assessments"].append(context.placeholder_assessment_uuid)
  
  context.learning_resource_2_response = post_method(
    url=context.learning_resource_url,
    request_body=context.learning_resource_2_req_body)
  context.learning_resource_2 = context.learning_resource_2_response.json()
  context.learning_resource_2_uuid = context.learning_resource_2['data']["uuid"]

  #Creating order 3 assessment
  context.assessment_2_req_body = deepcopy(context.assessment_req_body)
  context.assessment_2_req_body["parent_nodes"]["learning_objects"].append(
    context.learning_object_uuid)
  context.assessment_2_req_body["order"] = 3
  context.assessment_2_req_body["prerequisites"]["assessments"].append(context.placeholder_assessment_uuid)

  context.assessment_2_response = post_method(
    url=context.assessment_url,
    request_body=context.assessment_2_req_body)
  context.assessment_2 = context.assessment_2_response.json()
  context.assessment_2_uuid = context.assessment_2['data']["uuid"]

  #Create an authored assessment
  context.authored_assessment_req_body = deepcopy(context.human_graded_assessment_req_body)
  context.authored_assessment_req_body["name"] = "Authored Assessment"

  context.authored_assessment_response = post_method(
    url=context.human_graded_assessment_url,
    request_body=context.authored_assessment_req_body)
  print(context.authored_assessment_response)
  context.authored_assessment = context.authored_assessment_response.json()
  print(context.authored_assessment)
  context.authored_assessment_uuid = context.authored_assessment['data']["uuid"]

@behave.when("the LXE wants to link the authored assessment to the placeholder and ingest it into the hierarchy")
def step_6_2(context):
  new_assessment_id = context.authored_assessment_uuid
  old_assessment_id = context.placeholder_assessment_uuid
  linking_url = f"{API_URL_ASSESSMENT_SERVICE}/assessment/replace/{old_assessment_id}"
  query_params={"new_assessment_id":new_assessment_id}
  linking_response = put_method(linking_url,query_params=query_params,request_body={})
  context.linking_response_obj = linking_response.json()
  assert linking_response.status_code == 200, "Linking API Failed"

@behave.then("the authored assessment gets ingested and linked into the hierarchy")
def step_6_3(context):
  assert context.linking_response_obj['data']["name"] == "Authored Assessment", "Authored assessment not updated"
  assert context.linking_response_obj['data']["parent_nodes"]["learning_objects"][0] == context.learning_object_uuid, "Authored assessment not ingested in the hierarchy"
  assert context.linking_response_obj['data']["order"] == context.assessment_req_body["order"], "Authored assessment not ingested in the right order"
  assert context.linking_response_obj['data']["prerequisites"]["learning_resources"][0] == context.learning_resource_1_uuid, "Authored assessment pre-reqs not updated correctly"

@behave.then("the pre-reqs for subsequent nodes in the hierarchy are also updated")
def step_6_4(context):

  #Validating the updates to the subsequent nodes in the hierarchy
  context.learning_resource_get_response = get_method(
      url=context.learning_resource_url + "/" + context.learning_resource_2_uuid)
  
  context.learning_resource_get_object = context.learning_resource_get_response.json()
  assert context.learning_resource_get_object['data']["prerequisites"]["assessments"][0] == context.authored_assessment_uuid, "Dependent LRs not updated"

  context.assessment_get_response = get_method(
      url=context.assessment_url + "/" + context.assessment_2_uuid)
  context.assessment_get_object = context.assessment_get_response.json()
  assert context.learning_resource_get_object['data']["prerequisites"]["assessments"][0] == context.authored_assessment_uuid, "Dependent assessments no updated"


@behave.then("the placeholder assessment is delinked from the hierarchy")
def ste_6_5(context):
  #Validating the delinking of the placeholder assessment from the hierarchy
  context.placeholder_assessment_get_response = get_method(
      url=context.assessment_url + "/" + context.placeholder_assessment_uuid)
  context.placeholder_assessment_get_object = context.placeholder_assessment_get_response.json()
  assert context.placeholder_assessment_get_object['data']["parent_nodes"]["learning_objects"] == [], "Delinking of placeholder assessment not succesful"