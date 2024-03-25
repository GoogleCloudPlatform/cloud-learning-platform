"""
Feature 15 - API Test Script For Fetching child nodes
"""

import behave
from time import sleep
import sys
import os
import json
from copy import deepcopy
sys.path.append("../")
from setup import get_method
from test_config import API_URL_SKILL_SERVICE
from test_object_schemas import TEST_SKILL, TEST_COMPETENCY
from uuid import uuid4
from common.models import Skill, SkillServiceCompetency


#----------------------------- Scenario 01 --------------------------------
@behave.given("that a user has access to Skill Service (via Competencies & Skill Management) and needs to fetch all the child skills of a list of valid competencies")
def step_impl1(context):

  # create a list of skills
  skill_dict = deepcopy(TEST_SKILL)
  context.skill_uuids = []
  for _ in range(3):
    skill = Skill.from_dict(skill_dict)
    skill.uuid = ""
    skill.save()
    skill.uuid = skill.id
    skill.update()
    context.skill_uuids.append(skill.uuid)

  # create a competency
  competency_dict = deepcopy(TEST_COMPETENCY)
  competency = SkillServiceCompetency.from_dict(competency_dict)
  competency.uuid = ""
  competency.child_nodes = {"skills": context.skill_uuids}
  competency.save()
  competency.uuid = competency.id
  competency.update()
  context.competency_id = competency.uuid

  context.url = f"{API_URL_SKILL_SERVICE}/competencies/fetch_skills"
  context.params = {"competencies": [competency.uuid]}

@behave.when("there is a request to fetch all the child skills of a list of valid competencies")
def step_impl_2(context):
  context.resp = get_method(context.url, query_params=context.params)
  context.resp_data = context.resp.json()


@behave.then("Skill Service will return all the child skill nodes associated to their respective competencies")
def step_impl_3(context):
  assert context.resp.status_code == 200, "Status code not 200"
  actual_skill_uuids = [skill.get("skill_id") for skill in context.resp_data
                        ["data"][context.competency_id]]
  assert set(actual_skill_uuids) == set(context.skill_uuids),\
      "All child skills for the parent competency are not fetched"


#----------------------------- Scenario 02 --------------------------------
@behave.given("that a user has access to Skill Service (via Competencies & Skill Management) and needs to fetch all the child skills of a list of invalid competencies")
def step_impl1(context):
  context.competency_id = str(uuid4())
  context.url = f"{API_URL_SKILL_SERVICE}/competencies/fetch_skills"
  context.params = {"competencies": [context.competency_id]}


@behave.when("there is a request to fetch all the child skills of a list of invalid competencies")
def step_impl_2(context):
  context.resp = get_method(context.url, query_params=context.params)
  context.resp_data = context.resp.json()


@behave.then("Skill Service will throw an error message for invalid competency")
def step_impl_3(context):
  assert context.resp.status_code == 404,\
      f"Competency with uuid: {context.competency_id} exists"
  assert not context.resp_data["success"], "Successfully fetched the skills"
  assert context.resp_data["message"] == \
    f"Competency with uuid {context.competency_id} not found",\
    f"Competency with uuid: {context.competency_id} exists"
