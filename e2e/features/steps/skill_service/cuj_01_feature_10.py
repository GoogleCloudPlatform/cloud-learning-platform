"""
Feature 10 - API Test Script For Creating LUs from LOs in Knowledge service
"""

import behave
from time import sleep
import sys
import pandas as pd
import os
from common.models import KnowledgeServiceLearningUnit, SubConcept
sys.path.append("../")
from setup import post_method, set_cache, get_cache, get_method, put_method, delete_method
from test_config import API_URL_KNOWLEDGE_SERVICE, TESTING_OBJECTS_PATH
from test_object_schemas import TEST_KG_SUBCONCEPT


TEST_E2E_LOS_PATH = os.path.join(TESTING_OBJECTS_PATH, "test_e2e_los.csv")


#----------------------------- Scenario 01 --------------------------------

@behave.given("User has access to create LUs from LOs via Competency Management and LO from which LUs are to be created exists")
def step_impl1(context):
  # Create parent sub-concept before creating LO
  sub_concept_dict = TEST_KG_SUBCONCEPT
  subconcept = SubConcept.from_dict(sub_concept_dict)
  subconcept.uuid = ""
  subconcept.save()
  subconcept.uuid = subconcept.id
  subconcept.update()

  # Create LO from which LUs need to be created
  test_los = pd.read_csv(TEST_E2E_LOS_PATH).to_dict(orient="records")
  TEST_LEARNING_OBJECTIVE = test_los[0]
  TEST_LEARNING_OBJECTIVE["text"] = TEST_LEARNING_OBJECTIVE["text"].split(
      "<p>")
  create_lo_url = f"{API_URL_KNOWLEDGE_SERVICE}/sub-concept/{subconcept.uuid}/learning-objective"
  create_lo_res = post_method(url=create_lo_url, request_body=TEST_LEARNING_OBJECTIVE)
  create_lo_res_data = create_lo_res.json()

  assert create_lo_res.status_code == 200, "Status not 200"
  assert create_lo_res_data.get("success") is True, "Success not true"
  assert create_lo_res_data.get(
    "message") == "Successfully created the learning objective",\
    "Expected response not same"
  assert create_lo_res_data.get("data").get(
      "title") == TEST_LEARNING_OBJECTIVE.get(
          "title"), "Expected response not same"
  global LEARNING_OBJECTIVE_ID
  LEARNING_OBJECTIVE_ID = create_lo_res_data["data"]["uuid"]
  context.learning_objective_id = LEARNING_OBJECTIVE_ID

  # URL & Request payload to be used to create LUs from LO
  context.req_body = {
      "created_by": "XYZ-e2e",
      "last_modified_by": "ABC-e2e"
    }
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-objective/{LEARNING_OBJECTIVE_ID}/learning_unit/tree"


@behave.when("API to create Learning Units from Learning Objectives is called by providing correct request payload")
def step_impl2(context):
  # POST to Request Create LUs from LOs
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Knowledge Service will trigger a batch job to create Learning Units from given Learning Objectives successfully")
def step_impl3(context):
  # Check if batch job triggered successfully
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("data"), "Incorrect response"
  assert context.res_data.get("data").get("status") == "active", "Status not Active"

  # checking the status of job
  job_name = context.res_data["data"]["job_name"]
  url = f"{API_URL_KNOWLEDGE_SERVICE}/jobs/course-ingestion_learning-units/{job_name}"
  for _ in range(60):
    res = get_method(url=url)
    data = res.json()
    if data["data"]["status"] in ["succeeded", "failed"]:
      break
    sleep(10)
  assert data["data"]["status"] == "succeeded"
  print(data)

  # checking if lus are generated in the LU collection
  lus = KnowledgeServiceLearningUnit.collection.filter(
      parent_nodes={"learning_objectives": [context.learning_objective_id]}).fetch()
  global LEARNING_UNIT_IDS
  LEARNING_UNIT_IDS = [lu.id for lu in lus]
  assert LEARNING_UNIT_IDS, "LUs not generated for the LO"


#----------------------------- Scenario 02 --------------------------------

@behave.given("User has privilege to create Learning Units from Learning Objectives via Competency Management")
def step_impl1(context):
  context.req_body = {
    "created_by": "XYZ-e2e",
    "last_modified_by": "ABC-e2e"
    }
  random_lo_id = "random_id"
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-objective/{random_lo_id}/learning_unit/tree"


@behave.when("API to create Learning Units from Learning Objectives is called by providing incorrect LO ID in request payload")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Knowledge Service will throw ResourceNotFoundException for the invalid Learning Objective")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["success"] is False, "Success is not False"
  assert context.res_data["data"] is None
  assert context.res_data["message"] == "Learning Objective with uuid random_id not found"
