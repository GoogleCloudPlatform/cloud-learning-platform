"""Behave Test for Feature: SNHU Reigstrar can view and maintain a learner's academic record"""

import sys
from e2e.setup import post_method, get_method, delete_method
import behave
import uuid

sys.path.append("../")
from copy import copy
from e2e.test_object_schemas import LEARNER_OBJECT_TEMPLATE, ACHIEVEMENT_OBJECT_TEMPLATE, LEARNER_PROFILE_TEMPLATE
from e2e.test_config import API_URL_LEARNER_PROFILE_SERVICE


API_URL = API_URL_LEARNER_PROFILE_SERVICE

# Scenario 1
"""SNHU Registrar can access learner academic records"""


@behave.given("A learner is having some academic records")
def step_impl_1(context):
  """Defining the payload required for creating a Learner
      and then creating an Achievement"""
  achievement_dict = copy(ACHIEVEMENT_OBJECT_TEMPLATE)
  achievement_url = f"{API_URL}/achievement"
  achievement_post_res = post_method(url=achievement_url,
                                        request_body=achievement_dict)
  achievement_post_res_data = achievement_post_res.json()
  context.achievement_id = achievement_post_res_data["data"]["uuid"]
  assert achievement_post_res.status_code == 200, "Status code not 200"

  learner_dict = copy(LEARNER_OBJECT_TEMPLATE)
  learner_dict["email_address"] = "jondoe_c2f2s1@gmail.com"
  context.learner_url = f"{API_URL}/learner"
  learner_post_res = post_method(url=context.learner_url,
                                request_body=learner_dict)
  learner_post_res_data = learner_post_res.json()
  context.learner_id = learner_post_res_data["data"]["uuid"]
  assert learner_post_res.status_code == 200, "Status code not 200"

  learner_profile_dict = copy(LEARNER_PROFILE_TEMPLATE)
  learner_profile_dict["achievements"] = [context.achievement_id]
  context.learner_profile_url = f"{API_URL}/learner/{context.learner_id}/learner-profile"
  learner_profile_post_res = post_method(url=context.learner_profile_url,
                                    request_body=learner_profile_dict)
  assert learner_profile_post_res.status_code == 200, "Status code not 200"


@behave.when(
    "SNHU Registrar wants to access academic records of a particular learner")
def step_impl_2(context):
  """Fetching academic records of a learner"""
  context.learner_profile_get_res = get_method(url=context.learner_profile_url)
  context.learner_profile_get_res_data = context.learner_profile_get_res.json()


@behave.then(
    "SLP should return the academic records of the particular learner to SNHU Reigstrar"
)
def step_impl_3(context):
  """fetching a learner profile"""
  assert context.learner_profile_get_res.status_code == 200
  assert context.learner_profile_get_res_data["success"] is True
  assert context.learner_profile_get_res_data["data"]["learner_id"] == context.learner_id
  assert context.achievement_id in context.learner_profile_get_res_data["data"]["achievements"]

  # delete learner
  delete_method(url=context.learner_url + "/" + context.learner_id)

# --------------------------- Negative ----------------------------------

@behave.given("A learner is enrolled is having some academic records")
def step_impl_1(context):
  """Defining the payload required for creating a Learner
      and then creating an Achievement"""
  achievement_dict = copy(ACHIEVEMENT_OBJECT_TEMPLATE)
  achievement_url = f"{API_URL}/achievement"
  achievement_post_res = post_method(url=achievement_url,
                                        request_body=achievement_dict)
  achievement_post_res_data = achievement_post_res.json()
  achievement_id = achievement_post_res_data["data"]["uuid"]
  assert achievement_post_res.status_code == 200, "Status code not 200"

  learner_dict = copy(LEARNER_OBJECT_TEMPLATE)
  learner_dict["email_address"] = "jondoe_c2f2s2@gmail.com"
  context.learner_url = f"{API_URL}/learner"
  learner_post_res = post_method(url=context.learner_url,
                                request_body=learner_dict)
  learner_post_res_data = learner_post_res.json()
  context.learner_id = learner_post_res_data["data"]["uuid"]
  assert learner_post_res.status_code == 200, "Status code not 200"

  learner_profile_dict = copy(LEARNER_PROFILE_TEMPLATE)
  learner_profile_dict["achievements"] = [achievement_id]
  learner_profile_url = f"{API_URL}/learner/{context.learner_id}/learner-profile"
  learner_profile_post_res = post_method(url=learner_profile_url,
                                    request_body=learner_profile_dict)
  assert learner_profile_post_res.status_code == 200, "Status code not 200"


@behave.when(
    "SNHU Registrar wants to access academic records of a learner with invalid ID")
def step_impl_2(context):
  """Fetching academic records of a learner"""
  invalid_learner_id = "random_learner_id"
  learner_profile_url = f"{API_URL}/learner/{invalid_learner_id}/learner-profile"
  context.learner_profile_get_res = get_method(learner_profile_url)
  context.learner_profile_get_res_data = context.learner_profile_get_res.json()


@behave.then(
    "SLP should return error message to SNHU Registrar"
)
def step_impl_3(context):
  """fetching a learner profile"""
  assert context.learner_profile_get_res.status_code == 404
  assert context.learner_profile_get_res_data["success"] is False
  assert context.learner_profile_get_res_data["message"] == "Learner with uuid random_learner_id not found"

  # delete learner
  delete_method(url=context.learner_url + "/" + context.learner_id)
