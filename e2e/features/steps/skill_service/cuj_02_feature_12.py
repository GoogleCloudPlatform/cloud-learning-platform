"""
Feature 11 - API Test Script For EmploymentRole to Skill Alignment
"""

import behave
import sys
from time import sleep
import os
import pandas as pd
from copy import copy
from common.models import EmploymentRole
sys.path.append("../")
from setup import post_method
from test_config import API_URL_SKILL_SERVICE, TESTING_OBJECTS_PATH
from test_object_schemas import ROLE_OBJ_TEMPLATE


TEST_ROLES_PATH = os.path.join(TESTING_OBJECTS_PATH, "test_e2e_roles.csv")

# Setting up EmploymentRoles to perform EmploymentRole to skill alignment:
test_roles = pd.read_csv(TEST_ROLES_PATH)
test_roles["description"] = test_roles["description"].fillna("")
for _, row in test_roles.iterrows():
  role_dict = copy(ROLE_OBJ_TEMPLATE)
  role_dict["id"] = row["id"]
  role_dict["uuid"] = row["id"]
  role_dict["title"] = row["name"]
  role_dict["description"] = row["description"]
  role_dict["source_uri"] = f"https://e2e/resources/{row['id']}"
  role = EmploymentRole.from_dict(role_dict)
  role.save()


@behave.given("That a user can align skills to role via Skill Management")
def step_impl1(context):
  context.req_body = {
        "name": "Software Developer",
        "description": "Research, design, and develop computer and network "
            "software or specialized utility programs. Analyze user needs "
            "and develop software solutions, applying principles and techniques "
            "of computer science, engineering, and mathematical analysis.",
        "top_k": 5,
        "skill_alignment_sources": [
            "e2e_osn"
        ]
    }
  context.url = f"{API_URL_SKILL_SERVICE}/role/skill-alignment/query"


@behave.when("The mechanism to align skills to role is applied with correct request payload with role name & description")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will align and return skills that are relevant to the given role name and description")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("data").get("aligned_skills"), "aligned_skills not found"
  for source in context.req_body["skill_alignment_sources"]:
    assert len(context.res_data.get("data").get("aligned_skills").get(source)) \
      == context.req_body["top_k"], f"Expected response not same for {source} skill source"




@behave.given("That a user is able to align skills to role via Skill Management")
def step_impl1(context):
  context.req_body = {
        "name": "Software Developer",
        "description": "",
        "top_k": 5,
        "skill_alignment_sources": [
            "e2e_osn"
        ]
    }
  context.url = f"{API_URL_SKILL_SERVICE}/role/skill-alignment/query"


@behave.when("The mechanism to align skills to role is applied with correct request payload with role name only")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will align and return skills that are relevant to the given role name")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("data").get("aligned_skills"), "aligned_skills not found"



@behave.given("That a user is allowed to align skills to role via Skill Management")
def step_impl1(context):
  context.req_body = {
        "name": "",
        "description": "Research, design, and develop computer and network "
            "software or specialized utility programs. Analyze user needs "
            "and develop software solutions, applying principles and techniques "
            "of computer science, engineering, and mathematical analysis.",
        "top_k": 5,
        "skill_alignment_sources": [
            "e2e_osn"
        ]
    }
  context.url = f"{API_URL_SKILL_SERVICE}/role/skill-alignment/query"


@behave.when("The mechanism to align skills to role is applied with correct request payload with role description only")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will align and return skills that are relevant to the given role description")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("data").get("aligned_skills"), "aligned_skills not found"
  for source in context.req_body["skill_alignment_sources"]:
    assert len(context.res_data.get("data").get("aligned_skills").get(source)) \
      == context.req_body["top_k"], f"Expected response not same for {source} skill source"



@behave.given("That a user has the ability to align skills to role via Skill Management")
def step_impl1(context):
  context.req_body = {
        "name": "",
        "description": "",
        "top_k": 5,
        "skill_alignment_sources": [
            "e2e_osn"
        ]
    }
  context.url = f"{API_URL_SKILL_SERVICE}/role/skill-alignment/query"


@behave.when("The mechanism to align skills to role is applied with incorrect request payload with missing role name and description")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw an internal error to the user while trying to align roles to skills")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data["success"] is False, "Success is not False"
  assert context.res_data["message"] == "Both name and description cannot be empty."



@behave.given("That a user has acess to align skills to role via Skill Management")
def step_impl1(context):
  context.req_body = {
        "name": "",
        "description": "",
        "top_k": 5,
        "skill_alignment_sources": [
            "random_source"
        ]
    }
  context.url = f"{API_URL_SKILL_SERVICE}/role/skill-alignment/query"


@behave.when("The mechanism to align skills to role is applied with invalid skill alignment source")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw a validation error to the user while trying to align roles to skills")
def step_impl3(context):
  assert context.res.status_code == 500, "Status is not 500"
  assert context.res_data["success"] is False, "Success is not False"



@behave.given("That a user can align skills to role by given role id via Skill Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        "44b47ef4-c701-11ec-9d64-0242ac120002",
      ],
      "top_k": 5,
      "skill_alignment_sources": [
        "e2e_osn"
      ]
    }
  context.url = f"{API_URL_SKILL_SERVICE}/role/skill-alignment/id"


@behave.when("The mechanism to align skills to role by id is applied with correct request payload (a valid role ID)")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will align and return skills that are relevant to the role corresponding to given role ID")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("data").get("aligned_skills"), "aligned_skills not found"
  assert len(context.res_data.get("data").get("aligned_skills")) == \
      len(context.req_body["ids"]), \
        "mismatch between number of skill ids from request and response bodies"
  for id in context.req_body["ids"]:
    for source in context.req_body["skill_alignment_sources"]:
      assert len(context.res_data.get("data").get("aligned_skills").get(id).get(source)) \
        == context.req_body["top_k"], \
          f"Expected response not same for skill id: {id} and skill source: {source}"



@behave.given("That a user has access to align skills to role by given role id via Skill Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        "random_id",
      ],
      "top_k": 5,
      "skill_alignment_sources": [
        "e2e_osn"
      ]
    }
  context.url = f"{API_URL_SKILL_SERVICE}/role/skill-alignment/id"


@behave.when("The mechanism to align skills to role by id is applied with incorrect request payload (invalid role ID)")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw an internal error to the user while trying to align roles to skills by ID")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["success"] is False, "Success is not False"
  assert context.res_data["message"]  == "EmploymentRole with uuid random_id not found"



@behave.given("That a user has privileges to align skills to role by given role id via Skill Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        "44b47ef4-c701-11ec-9d64-0242ac120002",
      ],
      "top_k": 5,
      "skill_alignment_sources": [
        "random_source"
      ]
    }
  context.url = f"{API_URL_SKILL_SERVICE}/role/skill-alignment/id"


@behave.when("The mechanism to align skills to role by id is applied with incorrect request payload (invalid skill alignment source)")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw an internal error to the user while aligning roles to skills by ID")
def step_impl3(context):
  assert context.res.status_code == 500, "Status is not 500"
  assert context.res_data["success"] is False, "Success is not False"



@behave.given("That a user can update aligned skills to role for given role id by triggering batch job via Skill Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        "44b47ef4-c701-11ec-9d64-0242ac120002",
      ],
      "source_name": ["e2e"],
      "top_k": 5,
      "skill_alignment_sources": [
        "e2e_osn"
      ],
      "update_alignments": True
    }
  context.url = f"{API_URL_SKILL_SERVICE}/role/skill-alignment/batch"


@behave.when("The mechanism to update aligned skills to role by triggering a batch job is applied with correct request payload")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will create a batch job to align and update skills that are relevant to the role")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("data"), "Incorrect response"
  assert context.res_data.get("data").get("status") == "active", "Expected response not same"

  # checking the status of job
  job_name = context.res_data["data"]["job_name"]
  url = f"{API_URL_SKILL_SERVICE}/jobs/role_skill_alignment/{job_name}"
  for _ in range(60):
    res = get_method(url=url)
    data = res.json()
    if data["data"]["status"] in ["succeeded", "failed"]:
      break
    sleep(10)
  assert data["data"]["status"] == "succeeded"

  # checking if skills were updated in the role document
  role = EmploymentRole.find_by_id(context.req_body["ids"][0])
  updated_alignments = role.alignments["skill_alignment"]
  assert updated_alignments["e2e_osn"]["suggested"], "suggested alignments missing"
  assert len(updated_alignments["e2e_osn"]["suggested"]) == context.req_body["top_k"], "suggested alignments missing"



@behave.given("That a user can update aligned skills to role for given role id in request body with missing source name field via Skill Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        "44b47ef4-c701-11ec-9d64-0242ac120002",
      ],
      "top_k": 5,
      "skill_alignment_sources": ["e2e_osn"],
      "update_alignments": True
    }
  context.url = f"{API_URL_SKILL_SERVICE}/role/skill-alignment/batch"


@behave.when("The mechanism to update aligned skills to role by triggering a batch job is applied with missing source name field")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will create a batch job to align and update skills from all sources that are relevant to the role")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("data"), "Incorrect response"
  assert context.res_data.get("data").get("status") == "active", "Expected response not same"

  # checking the status of job
  job_name = context.res_data["data"]["job_name"]
  url = f"{API_URL_SKILL_SERVICE}/jobs/role_skill_alignment/{job_name}"
  for _ in range(60):
    res = get_method(url=url)
    data = res.json()
    if data["data"]["status"] in ["succeeded", "failed"]:
      break
    sleep(10)
  assert data["data"]["status"] == "succeeded"

  # checking if skills were updated in the role document
  role = EmploymentRole.find_by_id(context.req_body["ids"][0])
  updated_alignments = role.alignments["skill_alignment"]
  assert updated_alignments["e2e_osn"]["suggested"], "suggested alignments missing"
  assert len(updated_alignments["e2e_osn"]["suggested"]) == context.req_body["top_k"], "suggested alignments missing"



@behave.given("That a user can update aligned skills to role for given role id in request body with invalid role ID via Skill Management")
def step_impl1(context):
  context.req_body = {
      "ids": [
        "random_id",
      ],
      "source_name": ["e2e"],
      "top_k": 5,
      "skill_alignment_sources": [
        "e2e_osn"
      ],
      "update_alignments": True
    }
  context.url = f"{API_URL_SKILL_SERVICE}/role/skill-alignment/batch"


@behave.when("The mechanism to update aligned skills to role by triggering a batch job is applied with invalid role ID")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("the batch job triggered by Skill Service will fail as role ID given is invalid")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["success"] is False, "Success is not False"
  assert context.res_data["message"] == "Invalid EmploymentRole ID: random_id"
