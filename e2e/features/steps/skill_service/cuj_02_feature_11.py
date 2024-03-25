"""
Feature 11 - API Test Script For Knowledge to Skill Alignment
"""

import behave
from time import sleep
import sys
import os
from copy import copy
import pandas as pd
from common.models import KnowledgeServiceLearningUnit
sys.path.append("../")
from setup import post_method, set_cache, get_cache, get_method, put_method, delete_method
from test_config import API_URL_KNOWLEDGE_SERVICE, TESTING_OBJECTS_PATH
from test_object_schemas import LEARNING_UNIT_OBJ_TEMPLATE


TEST_LEARNING_UNITS_PATH = os.path.join(TESTING_OBJECTS_PATH, "test_e2e_learning_units.csv")

# Setting up Learning Units to perform Knowledge to skill alignment:
test_learning_unit = pd.read_csv(TEST_LEARNING_UNITS_PATH).iloc[4]
learning_unit_dict = copy(LEARNING_UNIT_OBJ_TEMPLATE)
learning_unit_dict["title"] = test_learning_unit["title"]
learning_unit_dict["description"] = test_learning_unit["text"]
learning_unit = KnowledgeServiceLearningUnit.from_dict(learning_unit_dict)
learning_unit.save()
LEARNING_UNIT_ID = learning_unit.id

#----------------------------- Scenario 01 --------------------------------

@behave.given("That a user can fetch skills that align with given knowledge node by id via Competency Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        LEARNING_UNIT_ID,
      ],
      "top_k": 4,
      "alignment_sources": [
        "e2e_osn"
      ],
      "knowledge_level": "learning_units"
    }
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/knowledge/skill-alignment/id"


@behave.when("The mechanism to align skills to knowledge node is applied with correct request payload")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Knowledge service will align and return skills that are relevant to the knowledge node corresponding to given knowledge node id")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("data").get(context.req_body["ids"][0]).get(
    "aligned_skills"), "aligned_skills not found"
  assert len(context.res_data.get("data")) == len(context.req_body["ids"]), \
    "mismatch between number of skill ids from request and response bodies"
  for id in context.req_body["ids"]:
    for source in context.req_body["alignment_sources"]:
      assert len(context.res_data.get("data").get(id).get("aligned_skills").get(source)) \
        == context.req_body["top_k"], f"Expected response not same"


#----------------------------- Scenario 02 --------------------------------

@behave.given("That a user has access to fetch skills that align with given knowledge node by id via Competency Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        "random_id",
      ],
      "top_k": 5,
      "alignment_sources": [
        "e2e_osn"
      ],
      "knowledge_level": "learning_units"
    }
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/knowledge/skill-alignment/id"


@behave.when("The mechanism to align skills to knowledge node is applied with invalid knowledge node id")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Knowledge service will throw an internal error while aligning skills to knowledge node as invalid knowledge node id was given")
def step_impl3(context):
  assert context.res.status_code == 500, "Status is not 500"
  assert context.res_data["success"] is False, "Success is not False"


#----------------------------- Scenario 03 --------------------------------

@behave.given("That a user is allowed to fetch skills that align with given knowledge node by id via Competency Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        LEARNING_UNIT_ID,
      ],
      "top_k": 5,
      "alignment_sources": [
        "random_source"
      ],
      "knowledge_level": "learning_units"
    }
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/knowledge/skill-alignment/id"


@behave.when("The mechanism to align skills to knowledge node is applied with invalid skill alignment source")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)


@behave.then("Knowledge service will throw an internal error while aligning skills to knowledge node as invalid skill alignment source was given")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"



#----------------------------- Scenario 04 --------------------------------

@behave.given("That a user is privileged to fetch skills that align with given knowledge node by id via Competency Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        LEARNING_UNIT_ID,
      ],
      "top_k": 5,
      "alignment_sources": [
        "e2e_osn"
      ],
      "knowledge_level": "random_level"
    }
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/knowledge/skill-alignment/id"


@behave.when("The mechanism to align skills to knowledge node is applied with invalid knowledge level")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)


@behave.then("Knowledge service will throw an internal error while aligning skills to knowledge node as invalid knowledge level was given")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"


#----------------------------- Scenario 05 --------------------------------

@behave.given("That a user has privilege to fetch skills that align with given knowledge node by id via Competency Management")
def step_impl1(context):
  context.req_body = {
      "top_k": 5,
      "alignment_sources": [
        "e2e_osn"
      ],
      "knowledge_level": "learning_units"
    }
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/knowledge/skill-alignment/id"


@behave.when("The mechanism to align skills to knowledge node is applied with missing knowledge node id")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)


@behave.then("Knowledge service will throw a validation error while aligning skills to knowledge node as knowledge node id is missing")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"


#----------------------------- Scenario 06 --------------------------------

@behave.given("That a user has privileges to fetch skills that align with given knowledge node by id via Competency Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        LEARNING_UNIT_ID,
      ],
      "top_k": 5,
      "knowledge_level": "learning_units"
    }
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/knowledge/skill-alignment/id"


@behave.when("The mechanism to align skills to knowledge node is applied with missing skill alignment source")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)


@behave.then("Knowledge service will throw a validation error while aligning skills to knowledge node as skill alignment source is missing")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"


#----------------------------- Scenario 07 --------------------------------

@behave.given("That a user has access privileges to fetch skills that align with given knowledge node by id via Competency Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        LEARNING_UNIT_ID,
      ],
      "top_k": 5,
      "alignment_sources": [
        "e2e_osn"
      ]
    }
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/knowledge/skill-alignment/id"


@behave.when("The mechanism to align skills to knowledge node is applied with missing knowledge level")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)


@behave.then("Knowledge service will throw a validation error while aligning skills to knowledge node as knowledge level is missing")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"


#----------------------------- Scenario 08 --------------------------------

@behave.given("That a user has access to align and update knowledge nodes with relevant skills by triggering batch job via Competency Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        LEARNING_UNIT_ID,
      ],
      "top_k": 5,
      "alignment_sources": [
        "e2e_osn"
      ],
      "knowledge_level": "learning_units"
    }
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/knowledge/skill-alignment/batch"


@behave.when("The mechanism to trigger a batch job to update knowledge nodes for given node ids with aligned skills is applied")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Knowledge service will create a batch job to align relevant skills to given knowledge node ids and update the same on firestore")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("data"), "Incorrect response"
  assert context.res_data.get("data").get("status") == "active", "Expected response not same"

  # checking the status of job
  job_name = context.res_data["data"]["job_name"]
  url = f"{API_URL_KNOWLEDGE_SERVICE}/jobs/skill_alignment/{job_name}"
  for _ in range(60):
    res = get_method(url=url)
    data = res.json()
    if data["data"]["status"] in ["succeeded", "failed"]:
      break
    sleep(10)
  assert data["data"]["status"] == "succeeded"

  # checking if knowledge nodes were updated in the skill document
  lu_object = KnowledgeServiceLearningUnit.find_by_id(context.req_body["ids"][0])
  skill_alignments = lu_object.alignments["skill_alignment"]
  assert "suggested" in skill_alignments["e2e_osn"], "suggested alignments missing in skill alignment"


#----------------------------- Scenario 09 --------------------------------

@behave.given("That a user has access to update skills that align with given knowledge node by triggering a batch job via Competency Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        "random_id",
      ],
      "top_k": 5,
      "alignment_sources": [
        "e2e_osn"
      ],
      "knowledge_level": "learning_units"
    }
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/knowledge/skill-alignment/batch"


@behave.when("The mechanism to trigger a batch job to align and align skills to knowledge node is applied with invalid knowledge node id")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Knowledge service will throw an internal error and batch job will not be triggered as invalid knowledge node id was given")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["success"] is False, "Success is not False"


#----------------------------- Scenario 10 --------------------------------

@behave.given("That a user is allowed to update skills that align with given knowledge node by triggering a batch job via Competency Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        LEARNING_UNIT_ID,
      ],
      "top_k": 5,
      "skill_alignment_sources": [
        "random_source"
      ],
      "knowledge_level": "learning_units"
    }
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/knowledge/skill-alignment/batch"


@behave.when("The mechanism to trigger a batch job to align and update skills to knowledge node is applied with invalid alignment source")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)


@behave.then("Knowledge service will throw an internal error and batch job will not be triggered as invalid alignment source was given")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"


#----------------------------- Scenario 11 --------------------------------

@behave.given("That a user is privileged to update skills that align with given knowledge node by triggering a batch via Competency Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        LEARNING_UNIT_ID,
      ],
      "top_k": 5,
      "skill_alignment_sources": [
        "e2e_osn"
      ],
      "knowledge_level": "random_level"
    }
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/knowledge/skill-alignment/batch"


@behave.when("The mechanism to trigger a batch job to align and update skills to knowledge node is applied with invalid knowledge level")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)


@behave.then("Knowledge service will throw an internal error and batch job will not be triggered as invalid knowledge level was given")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"



#----------------------------- Scenario 12 --------------------------------

@behave.given("That a user has privilege to update skills that align with given knowledge node by triggering a batch via Competency Management")
def step_impl1(context):
  context.req_body = {
      "top_k": 5,
      "alignment_sources": [
        "e2e_osn"
      ],
      "knowledge_level": "learning_units"
    }
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/knowledge/skill-alignment/batch"


@behave.when("The mechanism to trigger a batch job to align and update skills to knowledge node is applied with missing knowledge node id")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()

@behave.then("Knowledge service will throw a validation error and batch job will not be triggered as knowledge node id is missing")
def step_impl3(context):
  assert context.res.status_code == 500, "Status is not 500"
  assert context.res_data["success"] is False, "Success is not False"


#----------------------------- Scenario 13 --------------------------------
@behave.given("That a user has privileges to update skills that align with given knowledge node by triggering a batch via Competency Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        LEARNING_UNIT_ID,
      ],
      "top_k": 5,
      "knowledge_level": "learning_units"
    }
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/knowledge/skill-alignment/batch"


@behave.when("The mechanism to trigger a batch job to align and update skills to knowledge node is applied with missing alignment source")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)


@behave.then("Knowledge service will throw a validation error and batch job will not be triggered as alignment source is missing")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"



#----------------------------- Scenario 14 --------------------------------

@behave.given("That a user has access privileges to update skills that align with given knowledge node by triggering a batch via Competency Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        LEARNING_UNIT_ID,
      ],
      "top_k": 5,
      "skill_alignment_sources": [
        "e2e_osn"
      ]
    }
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/knowledge/skill-alignment/batch"


@behave.when("The mechanism to trigger a batch job to align and update skills to knowledge node is applied with missing knowledge level")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)


@behave.then("Knowledge service will throw a validation error and batch job will not be triggered as knowledge level is missing")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"
