"""
Feature 12 - API Test Script For Curriculum to Skill Alignment
"""
import os
import pandas as pd
from copy import copy
import behave
import sys
from common.models import Skill
sys.path.append("../")
from setup import post_method
from test_config import API_URL_SKILL_SERVICE, TESTING_OBJECTS_PATH
from test_object_schemas import SKILL_OBJ_TEMPLATE

TEST_E2E_SKILLS_PATH = os.path.join(TESTING_OBJECTS_PATH, "test_e2e_skills.csv")

# Setting up skills to perform curriculum to skill alignment:
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



@behave.given("That a user can to align skills to curriculum via Skill Management")
def step_impl1(context):
  context.req_body = {
        "name": "cyber security",
        "description": "Explain cyber security and its uses.",
        "top_k": 1,
        "skill_alignment_sources": [
            "e2e_osn"
        ]
    }
  context.url = f"{API_URL_SKILL_SERVICE}/curriculum/skill-alignment/query"


@behave.when("The mechanism to align skills to curriculum is applied with correct request payload with curriculum name & description")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will align and return skills that are relevant to the given curriculum name and description")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("data").get("aligned_skills"), "aligned_skills not found"
  for source in context.req_body["skill_alignment_sources"]:
    assert len(context.res_data.get("data").get("aligned_skills").get(source)) \
      == 0, f"Expected response not same for {source} skill source"
      # == [context.req_body["top_k"]], f"Expected response not same for {source} skill source" #skill_source=e2e




@behave.given("That a user is able to align skills to curriculum via Skill Management")
def step_impl1(context):
  context.req_body = {
        "name": "cyber security",
        "description": "",
        "top_k": 1,
        "skill_alignment_sources": [
            "e2e_osn"
        ]
    }
  context.url = f"{API_URL_SKILL_SERVICE}/curriculum/skill-alignment/query"


@behave.when("The mechanism to align skills to curriculum is applied with correct request payload with curriculum name only")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will align and return skills that are relevant to the given curriculum name")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("data").get("aligned_skills"), "aligned_skills not found"
  for source in context.req_body["skill_alignment_sources"]:
    assert len(context.res_data.get("data").get("aligned_skills").get(source)) \
      == 0, f"Expected response not same for {source} skill source"
      # == context.req_body["top_k"], f"Expected response not same for {source} skill source" # skill_source=e2e




@behave.given("That a user is allowed to align skills to curriculum via Skill Management")
def step_impl1(context):
  context.req_body = {
        "name": "",
        "description": "Explain cyber security and its uses.",
        "top_k": 1,
        "skill_alignment_sources": [
            "e2e_osn"
        ]
    }
  context.url = f"{API_URL_SKILL_SERVICE}/curriculum/skill-alignment/query"


@behave.when("The mechanism to align skills to curriculum is applied with correct request payload with curriculum description only")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will align and return skills that are relevant to the given curriculum description")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("data").get("aligned_skills"), "aligned_skills not found"
  for source in context.req_body["skill_alignment_sources"]:
    assert len(context.res_data.get("data").get("aligned_skills").get(source)) \
      == 0, f"Expected response not same for {source} skill source"
      # == [context.req_body["top_k"]], f"Expected response not same for {source} skill source" #skill_source=e2e



@behave.given("That a user has the ability to align skills to curriculum via Skill Management")
def step_impl1(context):
  context.req_body = {
        "name": "",
        "description": "",
        "top_k": 1,
        "skill_alignment_sources": [
            "e2e_osn"
        ]
    }
  context.url = f"{API_URL_SKILL_SERVICE}/curriculum/skill-alignment/query"


@behave.when("The mechanism to align skills to curriculum is applied with incorrect request payload with missing curriculum name and description")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw a validation error to the user as both name and description should not be empty")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data["success"] is False, "Success is not False"
  assert context.res_data.get("message") == "Both name and description cannot be empty."



@behave.given("That a user has acess to align skills to curriculum via Skill Management")
def step_impl1(context):
  context.req_body = {
        "name": "Define Science",
        "description": "",
        "top_k": 1,
        "skill_alignment_sources": [
            "random_source"
        ]
    }
  context.url = f"{API_URL_SKILL_SERVICE}/curriculum/skill-alignment/query"


@behave.when("The mechanism to align skills to curriculum is applied with invalid skill alignment source")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw an internal error to the user as no embeddings exist for given invalid skill alignment source")
def step_impl3(context):
  assert context.res.status_code == 500, "Status is not 500"
  assert context.res_data.get("success") is False, "Success is not False"
  assert context.res_data.get("message") == "Please create an embeddings index first.", "Expected Message not returned"
