"""Behave Test for Feature: Student Experience Staff can
  access a specific learner's personal information and academic records"""

from e2e.setup import post_method, get_method, delete_method
import behave
import uuid
import sys

sys.path.append("../")
from copy import copy
from e2e.test_object_schemas import LEARNER_OBJECT_TEMPLATE, ACHIEVEMENT_OBJECT_TEMPLATE, LEARNER_PROFILE_TEMPLATE
from e2e.test_config import API_URL_LEARNER_PROFILE_SERVICE

API_URL = API_URL_LEARNER_PROFILE_SERVICE

# Scenario 1
"""Student Experience Staff can access learner personal
  information and academic records"""


@behave.given(
    "A learner is enrolled in a Learning Experience and has some academic records"
)
def step_impl_1(context):
  """Defining the payload required for creating a Learner
      and then creating a Achievement"""
  achievement_url = f"{API_URL}/achievement"
  context.achievement_payload = copy(ACHIEVEMENT_OBJECT_TEMPLATE)
  achievement_post_res = post_method(
      url=achievement_url, request_body=context.achievement_payload)
  achievement_post_res_data = achievement_post_res.json()
  context.achievement_id = achievement_post_res_data["data"]["uuid"]

  learner_dict = copy(LEARNER_OBJECT_TEMPLATE)
  learner_dict["email_address"] = "jondoe_c2f1s1@gmail.com"
  context.learner_payload = learner_dict
  context.learner_url = f"{API_URL}/learner"

  context.learner_profile_payload = copy(LEARNER_PROFILE_TEMPLATE)
  context.learner_profile_payload["achievements"] = [context.achievement_id]

  context.learner_post_res = post_method(
      url=context.learner_url, request_body=context.learner_payload)

  context.learner_post_res_data = context.learner_post_res.json()
  learner_id = context.achievement_payload["learner_id"] =\
    context.learner_post_res_data["data"]["uuid"]

  context.learner_profile_post_res = post_method(
      url=context.learner_url + "/" +
      context.learner_post_res_data["data"]["uuid"] + "/learner-profile",
      request_body=context.learner_profile_payload)


@behave.when(
    "Student Experience Staff wants to access learner's personal information and academic records")
def step_impl_2(context):
  """Fetching learner info and learner profile of a particular person"""

  context.learner_get_res = get_method(
    url= context.learner_url + "/" +\
      context.learner_post_res_data["data"]["uuid"])

  context.learner_profile_get_res = get_method(
    url= context.learner_url + "/" +\
      context.learner_post_res_data["data"]["uuid"] +\
        "/learner-profile")

  context.learner_get_res_data = context.learner_get_res.json()
  context.learner_profile_get_res_data = context.learner_profile_get_res.json()



@behave.then("SLP should return the personal data and academic records of the particular learner")
def step_impl_4(context):
  """Checking learner and learner profile data"""

  assert context.learner_get_res.status_code == 200
  assert context.learner_get_res_data.get("success") is True
  assert context.learner_get_res_data.get(
      "message") == "Successfully fetched the learner"

  assert context.learner_profile_get_res.status_code == 200
  assert context.learner_profile_get_res_data.get("success") is True
  assert context.learner_profile_get_res_data.get(
      "message") == "Successfully fetched the learner profile"

  assert context.achievement_id in context.learner_profile_get_res_data[
                      "data"]["achievements"]


  # delete learner
  delete_method(url=context.learner_url + "/" +
                context.learner_post_res_data["data"]["uuid"])


# --------------------------- Negative ----------------------------------

@behave.given(
    "A learner is enrolled in Learning Experience and has some academic records"
)
def step_impl_1(context):
  """Defining the payload required for creating a Learner
      and then creating a Achievement"""
  achievement_url = f"{API_URL}/achievement"
  context.achievement_payload = copy(ACHIEVEMENT_OBJECT_TEMPLATE)
  achievement_post_res = post_method(
      url=achievement_url, request_body=context.achievement_payload)
  achievement_post_res_data = achievement_post_res.json()
  context.achievement_id = achievement_post_res_data["data"]["uuid"]

  learner_dict = copy(LEARNER_OBJECT_TEMPLATE)
  learner_dict["email_address"] = "jondoe_c2f1s2@gmail.com"
  context.learner_payload = learner_dict
  context.learner_url = f"{API_URL}/learner"

  context.learner_profile_payload = copy(LEARNER_PROFILE_TEMPLATE)
  context.learner_profile_payload["achievements"] = [context.achievement_id]

  context.learner_post_res = post_method(
      url=context.learner_url, request_body=context.learner_payload)

  context.learner_post_res_data = context.learner_post_res.json()
  learner_id = context.achievement_payload["learner_id"] =\
    context.learner_post_res_data["data"]["uuid"]

  context.learner_profile_post_res = post_method(
      url=context.learner_url + "/" +
      context.learner_post_res_data["data"]["uuid"] + "/learner-profile",
      request_body=context.learner_profile_payload)


@behave.when(
    "Student Experience Staff wants to access learner's personal information and academic records with invalid student id"
)
def step_impl_2(context):
  """Fetching learner info and learner profile of a particular person"""

  context.invalid_id = str(uuid.uuid4())

  context.learner_get_res = get_method(
      url=f"{context.learner_url}/{context.invalid_id}")

  context.learner_profile_get_res = get_method(
      url=f"{context.learner_url}/{context.invalid_id}/learner-profile")

  context.learner_get_res_data = context.learner_get_res.json()
  context.learner_profile_get_res_data = context.learner_profile_get_res.json()


@behave.then("SLP should return the error message to Student Experience Staff")
def step_impl_4(context):
  """Checking learner and learner profile data"""

  assert context.learner_get_res.status_code == 404
  assert context.learner_get_res_data.get("success") is False
  assert context.learner_get_res_data.get(
      "message") == f"Learner with uuid {context.invalid_id} not found"

  assert context.learner_profile_get_res.status_code == 404
  assert context.learner_profile_get_res_data.get("success") is False
  assert context.learner_profile_get_res_data.get(
      "message") == f"Learner with uuid {context.invalid_id} not found"

  # delete learner
  delete_method(url=context.learner_url + "/" +
                context.learner_post_res_data["data"]["uuid"])
