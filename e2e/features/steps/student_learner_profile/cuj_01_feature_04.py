"""
Faculty should be able to archive/un-archive a Learner.
"""

from e2e.setup import post_method, get_method, put_method, delete_method
from e2e.test_config import API_URL_LEARNER_PROFILE_SERVICE
from e2e.test_object_schemas import (LEARNER_OBJECT_TEMPLATE,
                                LEARNER_PROFILE_TEMPLATE,
                                ACHIEVEMENT_OBJECT_TEMPLATE)
import behave
import sys
from uuid import uuid4
sys.path.append("../")


API_URL = API_URL_LEARNER_PROFILE_SERVICE

#Scenario 1

@behave.given("A Learner is present with Learner Profile and Achievements.")
def step_1_1(context):

  # Adding a learner
  learner_dict = {**LEARNER_OBJECT_TEMPLATE}
  learner_dict["email_address"] = f"{uuid4()}@gmail.com"
  context.learner_payload = learner_dict
  context.learner_url = f"{API_URL}/learner"
  context.learner_post_res = post_method(
      url=context.learner_url, request_body=context.learner_payload)
  context.learner_post_res_data = context.learner_post_res.json()
  assert context.learner_post_res.status_code == 200, "status not 200"
  assert context.learner_post_res_data.get("success") is True, \
      "success not true"
  context.learner_id = context.learner_post_res_data["data"]["uuid"]

  # Adding a Learner Profile
  learner_profile_dict = {**LEARNER_PROFILE_TEMPLATE}
  learner_profile_dict["learner_id"] = context.learner_id
  context.learner_profile_payload = learner_profile_dict
  context.learner_profile_url = \
      f"{API_URL}/learner/{context.learner_id}/learner-profile"
  context.learner_profile_post_res = post_method(
      url=context.learner_profile_url,
      request_body=context.learner_profile_payload)
  context.learner_profile_post_res_data = \
      context.learner_profile_post_res.json()
  assert context.learner_profile_post_res.status_code == 200, "status not 200"
  assert context.learner_profile_post_res_data.get("success") is True, \
      "success not true"
  context.learner_profile_id = \
      context.learner_profile_post_res_data["data"]["uuid"]

  # Adding an Achievement
  achievement_dict = {**ACHIEVEMENT_OBJECT_TEMPLATE}
  context.achievement_payload = achievement_dict
  context.achievement_url = f"{API_URL}/achievement"
  context.achievement_post_res = post_method(
      url=context.achievement_url,
      request_body=context.achievement_payload)
  context.achievement_post_res_data = \
      context.achievement_post_res.json()
  assert context.achievement_post_res.status_code == 200, "status not 200"
  assert context.achievement_post_res_data.get("success") is True, \
      "success not true"
  context.achievement_id = \
      context.achievement_post_res_data["data"]["uuid"]


@behave.when("Faculty archives the Learner with correct payload.")
def step_1_2(context):
  context.url = f"{context.learner_url}/{context.learner_id}"

  archive_learner_dict = {}
  archive_learner_dict["is_archived"] = True
  context.updated_learner = archive_learner_dict

  # put request
  response = put_method(url=context.url, request_body=archive_learner_dict)
  response_data = response.json()
  assert response.status_code == 200, "Status not 200"
  assert response_data.get("data").get("is_archived") is True, \
      "is_archived not working"


@behave.then("Learner gets archived")
def step_1_3(context):
  response = get_method(url=context.url)
  response_data = response.json()

  assert response.status_code == 200, "Status not 200"
  assert response_data.get("success") is True, "Success not true"
  assert response_data.get("message") == \
    "Successfully fetched the learner", "Expected response not same"
  assert response_data.get("data").get(
      "is_archived") is True, "Expected response not same"


@behave.then("Learner Profile associated with Learner gets archived")
def step_1_4(context):
  url = context.learner_profile_url
  response = get_method(url=url)
  response_data = response.json()

  assert response.status_code == 200, "Status not 200"
  assert response_data.get("success") is True, "Success not true"
  assert response_data.get("message") == \
    "Successfully fetched the learner profile", "Expected response not same"
  assert response_data.get("data").get(
      "is_archived") is True, "Expected response not same"

  #delete learner
  delete_method(url=context.url)


# Scenario 2

@behave.given(
    "An archived Learner is present with Learner Profile and Achievements.")
def step_2_1(context):

  # Adding a learner
  learner_dict = {**LEARNER_OBJECT_TEMPLATE}
  learner_dict["email_address"] = f"{uuid4()}@gmail.com"
  learner_dict["is_archived"] = True
  context.learner_payload = learner_dict
  context.learner_url = f"{API_URL}/learner"
  context.learner_post_res = post_method(
      url=context.learner_url, request_body=context.learner_payload)
  context.learner_post_res_data = context.learner_post_res.json()
  assert context.learner_post_res.status_code == 200, "status not 200"
  assert context.learner_post_res_data.get("success") is True, \
      "success not true"
  context.learner_id = context.learner_post_res_data["data"]["uuid"]

  # Adding a Learner Profile
  learner_profile_dict = {**LEARNER_PROFILE_TEMPLATE}
  learner_profile_dict["learner_id"] = context.learner_id
  learner_profile_dict["is_archived"] = True
  context.learner_profile_payload = learner_profile_dict
  context.learner_profile_url = \
      f"{API_URL}/learner/{context.learner_id}/learner-profile"
  context.learner_profile_post_res = post_method(
      url=context.learner_profile_url,
      request_body=context.learner_profile_payload)
  context.learner_profile_post_res_data = \
      context.learner_profile_post_res.json()

  assert context.learner_profile_post_res.status_code == 200, "status not 200"
  assert context.learner_profile_post_res_data.get("success") is True, \
      "success not true"
  context.learner_profile_id = \
      context.learner_profile_post_res_data["data"]["uuid"]

  # Adding an Achievement
  achievement_dict = {**ACHIEVEMENT_OBJECT_TEMPLATE}
  achievement_dict["is_archived"] = True
  context.achievement_payload = achievement_dict
  context.achievement_url = f"{API_URL}/achievement"
  context.achievement_post_res = post_method(
      url=context.achievement_url,
      request_body=context.achievement_payload)
  context.achievement_post_res_data = \
      context.achievement_post_res.json()

  assert context.achievement_post_res.status_code == 200, "status not 200"
  assert context.achievement_post_res_data.get("success") is True, \
      "success not true"
  context.achievement_id = \
      context.achievement_post_res_data["data"]["uuid"]


@behave.when("Faculty un-archives the Learner with correct payload.")
def step_2_2(context):
  context.url = f"{context.learner_url}/{context.learner_id}"

  archive_learner_dict = {}
  archive_learner_dict["is_archived"] = False
  context.updated_learner = archive_learner_dict

  # put request
  response = put_method(url=context.url, request_body=archive_learner_dict)
  response_data = response.json()
  assert response.status_code == 200, "Status not 200"
  assert response_data.get("data").get("is_archived") is False, \
      "is_archived not working"


@behave.then("Learner gets un-archived")
def step_2_3(context):
  response = get_method(url=context.url)
  response_data = response.json()

  assert response.status_code == 200, "Status not 200"
  assert response_data.get("success") is True, "Success not true"
  assert response_data.get("message") == \
    "Successfully fetched the learner", "Expected response not same"
  assert response_data.get("data").get(
      "is_archived") is False, "Expected response not same"


@behave.then("Learner Profile associated with Learner gets un-archived")
def step_2_4(context):
  url = f"{context.learner_profile_url}/{context.learner_profile_id}"
  response = get_method(url=url)
  response_data = response.json()

  assert response.status_code == 200, "Status not 200"
  assert response_data.get("success") is True, "Success not true"
  assert response_data.get("message") == \
    "Successfully fetched the learner profile", "Expected response not same"
  assert response_data.get("data").get(
      "is_archived") is False, "Expected response not same"

  #delete learner
  delete_method(url=context.url)
