"""
Feature 10 - API Test Script For Skill to Knowledge Alignment
"""

import behave
import sys
import os
import pandas as pd
from copy import copy
from time import sleep
from common.models import Skill
sys.path.append("../")
from setup import post_method, set_cache, get_cache, get_method, put_method, delete_method
from test_config import API_URL_SKILL_SERVICE, TESTING_OBJECTS_PATH
from test_object_schemas import SKILL_OBJ_TEMPLATE

TEST_E2E_SKILLS_PATH = os.path.join(TESTING_OBJECTS_PATH, "test_e2e_skills.csv")

# Setting up skills to perform Skill to Knowledge alignment:
INSERTED_SKILL_IDS = []
test_skills = pd.read_csv(TEST_E2E_SKILLS_PATH)
test_skills["description"] = test_skills["description"].fillna("")
for _, row in test_skills.iterrows():
  skill_dict = copy(SKILL_OBJ_TEMPLATE)
  skill_dict["name"] = row["name"]
  skill_dict["description"] = row["description"]
  skill_dict["reference_id"] = row["id"]
  skill_dict["source_name"] = "e2e_test"
  skill_dict["uuid"] = row["id"]
  skill_dict["source_uri"] = f"https://e2e/resources/{row['id']}"
  skill = Skill.from_dict(skill_dict)
  skill.save()
  INSERTED_SKILL_IDS.append(skill.id)


@behave.given("That a user has access to align and update knowledge nodes to skills by triggering batch job via Skill Management")
def step_impl1(context):
  context.req_body = {
      "source_name": ["e2e_test"],
      "input_type": "skill",
      "top_k": 5,
      "output_alignment_sources": {
        "skill_sources": [],
        "learning_resource_ids": [context.learning_resource_id]
      },
      "update_alignments": "true"
    }
  context.url = f"{API_URL_SKILL_SERVICE}/unified-alignment/batch"


@behave.when("The mechanism to update skills for given source name with aligned knowledge nodes by triggering a batch job is applied")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will create a batch job to align and update relevant knowledge nodes to skills belonging to given source name")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("data"), "Incorrect response"
  assert context.res_data.get("data").get("status") == "active", "Expected response not same"

  # checking the status of job
  job_name = context.res_data["data"]["job_name"]
  url = f"{API_URL_SKILL_SERVICE}/jobs/unified_alignment/{job_name}"
  for _ in range(60):
    res = get_method(url=url)
    data = res.json()
    if data["data"]["status"] in ["succeeded", "failed"]:
      break
    sleep(10)
  assert data["data"]["status"] == "succeeded"

  # checking if knowledge were updated in the skill document
  skill_list = [Skill.find_by_id(id) for id in INSERTED_SKILL_IDS]
  for skill in skill_list:
    knowledge_alignments = skill.alignments["knowledge_alignment"]
    assert "suggested" in knowledge_alignments, "suggested alignments missing in knowledge alignment"


@behave.given("That a user can access functionality to align and update knowledge nodes to skills by triggering batch job via Skill Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        "bc94f026-c485-11ec-9d64-0242ac120002"
      ],
      "input_type": "skill",
      "top_k": 5,
      "output_alignment_sources": {
        "skill_sources": [],
        "learning_resource_ids": [context.learning_resource_id]
      }
    }
  context.url = f"{API_URL_SKILL_SERVICE}/unified-alignment/batch"


@behave.when("The mechanism to update skills for given ids with aligned knowledge nodes by triggering a batch job is applied")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will create a batch job to align and update relevant knowledge nodes to skills for given ids")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("data"), "Incorrect response"
  assert context.res_data.get("data").get("status") == "active", "Expected response not same"

  # checking the status of job
  job_name = context.res_data["data"]["job_name"]
  url = f"{API_URL_SKILL_SERVICE}/jobs/unified_alignment/{job_name}"
  for _ in range(60):
    res = get_method(url=url)
    data = res.json()
    if data["data"]["status"] in ["succeeded", "failed"]:
      break
    sleep(10)
  assert data["data"]["status"] == "succeeded"

  # checking if knowledge nodes were updated in the skill document
  skill = Skill.find_by_uuid(context.req_body["ids"][0])
  knowledge_alignments = skill.alignments["knowledge_alignment"]
  assert "suggested" in knowledge_alignments, "suggested alignments missing in knowledge alignment"



@behave.given("That a user can align and update knowledge nodes to skills by triggering batch job via Skill Management")
def step_impl1(context):
  context.req_body = {
      "ids": ["bc94f026-c485-11ec-9d64-0242ac120002"],
      "source_name": ["e2e"],
      "input_type": "skill",
      "top_k": 5,
      "output_alignment_sources": {
        "skill_sources": [],
        "learning_resource_ids": [context.learning_resource_id]
      },
      "update_alignments": "true"
    }
  context.url = f"{API_URL_SKILL_SERVICE}/unified-alignment/batch"


@behave.when("The mechanism to update skills with aligned knowledge nodes is applied by giving both source name and skill ids")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw an internal error as both source name and skill ids were given and batch job will not be triggered")
def step_impl3(context):
  assert context.res.status_code == 500, "Status is not 500"
  assert context.res_data["success"] is False, "Success is not False"



@behave.given("That a user can update aligned knowledge nodes to skills by triggering batch job via Skill Management")
def step_impl1(context):
  context.req_body = {
      "input_type": "skill",
      "top_k": 5,
      "output_alignment_sources": {
        "skill_sources": [],
        "learning_resource_ids": [context.learning_resource_id]
      },
      "update_alignments": "true"
    }
  context.url = f"{API_URL_SKILL_SERVICE}/unified-alignment/batch"


@behave.when("The mechanism to update skills with aligned knowledge nodes is applied without giving both source name and skill ids")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw an internal error as both source name and skill ids are missing and batch job will not be triggered")
def step_impl3(context):
  assert context.res.status_code == 500, "Status is not 500"
  assert context.res_data["success"] is False, "Success is not False"



@behave.given("That a user has access to update aligned knowledge nodes to skills by triggering batch job via Skill Management")
def step_impl1(context):
  context.req_body = {
      "source_name": [
        "invalid_source"
      ],
      "input_type": "skill",
      "top_k": 5,
      "output_alignment_sources": {
        "skill_sources": [],
        "learning_resource_ids": [context.learning_resource_id]
      },
      "update_alignments": "true"
    }
  context.url = f"{API_URL_SKILL_SERVICE}/unified-alignment/batch"


@behave.when("The mechanism to update skills with aligned knowledge nodes is applied by providing an invalid source name")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw an internal error as invalid source name was given and batch job will not be triggered")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data["success"] is False, "Success is not False"


@behave.given("That a user has access to update knowledge nodes to skills by triggering batch job via Skill Management")
def step_impl1(context):
  context.req_body = {
      "ids": ["invalid_skill_id"],
      "input_type": "skill",
      "top_k": 5,
      "output_alignment_sources": {
        "skill_sources": [],
        "learning_resource_ids": [context.learning_resource_id]
      }
    }
  context.url = f"{API_URL_SKILL_SERVICE}/unified-alignment/batch"


@behave.when("The mechanism to update skills with aligned knowledge nodes is applied by providing an invalid skill id")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw an internal error as invalid skill id was given and batch job will not be triggered")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["success"] is False, "Success is not False"
  assert context.res_data["message"] == "Skill with uuid invalid_skill_id not found"


@behave.given("That a user is privileged to update aligned knowledge nodes to skills by triggering batch job via Skill Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        "bc94f026-c485-11ec-9d64-0242ac120002"
      ],
      "input_type": "skill",
      "top_k": 5,
      "output_alignment_sources": {
        "skill_sources": ["e2e"]
      },
      "update_alignments": "true"
    }
  context.url = f"{API_URL_SKILL_SERVICE}/unified-alignment/batch"


@behave.when("The mechanism to update skills with aligned knowledge nodes is applied without providing learning resource id key")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw an internal error as learning resource id key is missing and batch job will not be triggered")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data["success"] is False, "Success is not False"
  assert context.res_data["message"] == "{'learning_resource_ids'} missing in output_alignment_sources"


@behave.given("That a user is privileged to update knowledge nodes to skills by triggering batch job via Skill Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        "bc94f026-c485-11ec-9d64-0242ac120002"
      ],
      "input_type": "skill",
      "top_k": 5,
      "output_alignment_sources": {
        "skill_sources": [],
        "learning_resource_ids": ["invalid_learning_resourcce"]
      },
      "update_alignments": "true"
    }
  context.url = f"{API_URL_SKILL_SERVICE}/unified-alignment/batch"


@behave.when("The mechanism to update skills with aligned knowledge nodes is applied by providing invalid learning resource id")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw an internal error as invalid learning resource id was given and batch job will not be triggered")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["success"] is False, "Success is not False"
  assert context.res_data["message"] == "Invalid KnowledgeServiceLearningContent ID: invalid_learning_resourcce"


@behave.given("That a user can access functionality update aligned knowledge nodes to skills by triggering batch job via Skill Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        "bc94f026-c485-11ec-9d64-0242ac120002"
      ],
      "input_type": "skill",
      "top_k": 5,
      "output_alignment_sources": {
        "skill_sources": [
          "e2e"
        ],
        "learning_resource_ids": [
          context.learning_resource_id
        ],
        "random_alignment": []
      },
      "update_alignments": "true"
    }
  context.url = f"{API_URL_SKILL_SERVICE}/unified-alignment/batch"


@behave.when("The mechanism to update skills with aligned knowledge nodes is applied with invalid output alignment source key")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("the batch job will not get triggered and Skill Service will throw an internal error as invalid output alignment source key was given")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data["success"] is False, "Success is not False"



@behave.given("That a user can align knowledge nodes to skill by query via Skill Management")
def step_impl1(context):
  context.req_body = {
      "name": "Operating Systems",
      "description": "An operating system (OS) is system software that manages computer hardware, software resources, and provides common services for computer programs.",
      "input_type": "skill",
      "top_k": 3,
      "output_alignment_sources": {
        "skill_sources": [],
        "learning_resource_ids": [context.learning_resource_id]
      }
    }
  context.url = f"{API_URL_SKILL_SERVICE}/unified-alignment/query"


@behave.when("The mechanism to align knowledge nodes to skills is applied with skill name & description")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will align and return knowledge nodes that are relevant to the given skill name and description")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("data").get("aligned_knowledge").get(context.learning_resource_id), "aligned_knowledge not found"



@behave.given("That a user is able to align knowledge nodes to skill by query via Skill Management")
def step_impl1(context):
  context.req_body = {
      "name": "Operating Systems",
      "description": "",
      "input_type": "skill",
      "top_k": 3,
      "output_alignment_sources": {
        "skill_sources": [],
        "learning_resource_ids": [context.learning_resource_id]
      }
    }
  context.url = f"{API_URL_SKILL_SERVICE}/unified-alignment/query"


@behave.when("The mechanism to align knowledge nodes to skill is applied with skill name only")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will align and return knowledge nodes that are relevant to the given skill name")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("data").get("aligned_knowledge").get(context.learning_resource_id), "aligned_knowledge not found"



@behave.given("That a user is allowed to align knowledge nodes to skill by query via Skill Management")
def step_impl1(context):
  context.req_body = {
      "name": "",
      "description": "An operating system (OS) is system software that manages computer hardware, software resources, and provides common services for computer programs.",
      "input_type": "skill",
      "top_k": 3,
      "output_alignment_sources": {
        "skill_sources": [],
        "learning_resource_ids": [context.learning_resource_id]
      }
    }
  context.url = f"{API_URL_SKILL_SERVICE}/unified-alignment/query"


@behave.when("The mechanism to align knowledge nodes to skill is applied with skill description only")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will align and return knowledge nodes that are relevant to the given skill description")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("data").get("aligned_knowledge").get(context.learning_resource_id), "aligned_knowledge not found"



@behave.given("That a user has the ability to align knowledge nodes to skill by query via Skill Management")
def step_impl1(context):
  context.req_body = {
      "name": "",
      "description": "",
      "input_type": "skill",
      "top_k": 3,
      "output_alignment_sources": {
        "skill_sources": [],
        "learning_resource_ids": [context.learning_resource_id]
      }
    }
  context.url = f"{API_URL_SKILL_SERVICE}/unified-alignment/query"


@behave.when("The mechanism to align knowledge nodes to skill is applied when both skill name and description is missing")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw an internal error while aligning knowledge nodes as both name and description are empty strings")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data["success"] is False, "Success is not False"



@behave.given("That a user has access to align knowledge nodes to skill by query via Skill Management")
def step_impl1(context):
  context.req_body = {
      "name": "Expert",
      "description": "Diagnose small engines used to power sporting equipment.",
      "input_type": "skill",
      "top_k": 3,
      "output_alignment_sources": {
        "skill_sources": [],
        "learning_resource_ids": ["invalid_learning_resource"]
      }
    }
  context.url = f"{API_URL_SKILL_SERVICE}/unified-alignment/query"


@behave.when("The mechanism to align knowledge nodes to skill is applied by providing invalid learning resource id")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw an internal error while aligning knowledge nodes as invalid learning resource id was given")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["success"] is False, "Success is not False"
  assert context.res_data["message"] == "Invalid KnowledgeServiceLearningContent ID: invalid_learning_resource"


@behave.given("That a user can align knowledge nodes to skill by id via Skill Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        "bc94f026-c485-11ec-9d64-0242ac120002"
      ],
      "input_type": "skill",
      "top_k": 3,
      "output_alignment_sources": {
        "skill_sources": [],
        "learning_resource_ids": [context.learning_resource_id]
      }
    }
  context.url = f"{API_URL_SKILL_SERVICE}/unified-alignment/id"


@behave.when("The mechanism to align knowledge nodes to skills is applied with correct request payload")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will align and return knowledge nodes that are relevant to the skill corresponding given skill id")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("data").get(context.req_body["ids"][0]).get(
    "aligned_knowledge").get(context.learning_resource_id), "aligned_knowledge not found"



@behave.given("That a user has access to align knowledge nodes to skill by id via Skill Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        "invalid_id",
      ],
      "input_type": "skill",
      "top_k": 3,
      "output_alignment_sources": {
        "skill_sources": [],
        "learning_resource_ids": [context.learning_resource_id]
      }
    }
  context.url = f"{API_URL_SKILL_SERVICE}/unified-alignment/id"


@behave.when("The mechanism to align knowledge nodes to skill by id is applied by providing invalid skill id")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw an internal error while aligning knowledge nodes as invalid skill id was given")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["success"] is False, "Success is not False"
  assert context.res_data["message"] == "Skill with uuid invalid_id not found"



@behave.given("That a user has the ability to align knowledge nodes to skill by id via Skill Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        "bc94f026-c485-11ec-9d64-0242ac120002",
      ],
      "input_type": "skill",
      "top_k": 3,
      "output_alignment_sources": {
        "skill_sources": [],
        "learning_resource_ids": [context.learning_resource_id],
        "another_source": ["some_source"]
      }
    }
  context.url = f"{API_URL_SKILL_SERVICE}/unified-alignment/id"


@behave.when("The mechanism to align knowledge nodes to skill by id is applied by providing invalid output alignment source")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw an internal error while aligning knowledge nodes as invalid output alignment source was given")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data["success"] is False, "Success is not False"



@behave.given("That a user has the access to align knowledge nodes to skill by id via Skill Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        "bc94f026-c485-11ec-9d64-0242ac120002",
      ],
      "input_type": "skill",
      "top_k": 3,
      "output_alignment_sources": {
        "skill_sources": ["e2e"]
      }
    }
  context.url = f"{API_URL_SKILL_SERVICE}/unified-alignment/id"


@behave.when("The mechanism to align knowledge nodes to skill by id is applied with missing learning resource id")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw an internal error while aligning knowledge nodes as learning resource id was missing")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data["success"] is False, "Success is not False"
  assert context.res_data["message"] == "{'learning_resource_ids'} missing in output_alignment_sources"



@behave.given("That a user is allowed to align knowledge nodes to skill by id via Skill Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        "bc94f026-c485-11ec-9d64-0242ac120002",
      ],
      "input_type": "skill",
      "top_k": 3,
      "output_alignment_sources": {
        "skill_sources": [],
        "learning_resource_ids": ["invalid_id"]
      }
    }
  context.url = f"{API_URL_SKILL_SERVICE}/unified-alignment/id"


@behave.when("The mechanism to align knowledge nodes to skill by id is applied by providing invalid learning resource id")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw an internal error while aligning knowledge nodes by id as invalid learning resource id was given")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["success"] is False, "Success is not False"
  assert context.res_data["message"] == "Invalid KnowledgeServiceLearningContent ID: invalid_id"



@behave.given("That a user has privileges to align knowledge nodes to skill by id via Skill Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        "bc94f026-c485-11ec-9d64-0242ac120002",
      ],
      "input_type": "skill",
      "top_k": 3,
      "output_alignment_sources": {
        "skill_sources": [],
        "learning_resource_ids": ["*"]
      }
    }
  context.url = f"{API_URL_SKILL_SERVICE}/unified-alignment/id"


@behave.when("The mechanism to align knowledge nodes to skill by id is applied by providing asterisk as value for learning resource id")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw an internal error while aligning knowledge nodes as asterisk was given as value for learning resource id")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data["success"] is False, "Success is not False"
  assert context.res_data["message"] == '"*" is not allowed as value in "output_alignment_sources". Please use specific source(s) as value.'
