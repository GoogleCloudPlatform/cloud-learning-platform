"""
Feature 02 - Search achievement, goal, learner account and learner profile data based on various Student Learner Profile attributes
"""

import behave
from uuid import uuid4
import sys
from copy import copy
sys.path.append("../")
from e2e.setup import post_method, get_method
from e2e.test_config import API_URL_LEARNER_PROFILE_SERVICE, DEL_KEYS
from e2e.test_object_schemas import (LEARNER_OBJECT_TEMPLATE, GOAL_OBJECT_TEMPLATE,
                                ACHIEVEMENT_OBJECT_TEMPLATE, LEARNER_PROFILE_TEMPLATE)


# ----------------------------- Scenario 01 ---------------------------------

@behave.given("Administrator has access to SLP service to search learner by first name")
def step_impl_1(context):
  learner_dict = copy(LEARNER_OBJECT_TEMPLATE)
  learner_dict["email_address"] = f"{uuid4()}_test_cuj3_feature2_scenario01@gmail.com"
  learner_dict["first_name"] = "UniqueFirstName"
  del learner_dict["uuid"]
  context.learner_first_name = learner_dict["first_name"]
  
  # Create learner using post request:
  api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner"
  post_req = post_method(url=api_url, request_body=learner_dict)
  post_result = post_req.json()
  post_result_data = post_result.get("data")
  for key in DEL_KEYS:
    if key in post_result_data:
      del post_result_data[key]
    if key in learner_dict:
      del learner_dict[key]
  assert post_req.status_code == 200, "Learner not created successfully"
  assert post_result_data == learner_dict, "Learner created dosent match expectecd response"

  context.params ={
      "first_name": "UniqueFirstName"
      }
  context.url = f"{api_url}/search"


@behave.when("Administrator wants to search learner based on correct first name")
def step_impl_2(context):
  context.get_res = get_method(url=context.url, query_params=context.params)
  context.get_res_data = context.get_res.json()


@behave.then("the relevant learner corresponding to given first name is retrieved and returned to user")
def step_impl_3(context):
  assert context.get_res.status_code == 200, "Status is not 200"
  assert context.get_res_data.get("success") is True
  assert context.get_res_data.get("message") == "Successfully fetched the learners"
  search_result = context.get_res_data.get("data")[0]
  del search_result["uuid"]
  assert search_result.get("first_name") == context.learner_first_name, "Response received"



# ----------------------------- Scenario 02 ---------------------------------

@behave.given("Administrator has privilege to access SLP service to search learner by first name")
def step_impl_1(context):
  context.params ={
      "first_name": "Random Name xyz123123"
      }
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/search"


@behave.when("Administrator wants to search learner based on incorrect first name")
def step_impl_2(context):
  context.get_res = get_method(url=context.url, query_params=context.params)
  context.get_res_data = context.get_res.json()


@behave.then("SLP service will return empty response as no learner exists for given incorrect first name")
def step_impl_3(context):
  assert context.get_res.status_code == 200, "Status is not 200"
  assert context.get_res_data.get("success") is True
  assert context.get_res_data.get("message") == "Successfully fetched the learners"
  assert context.get_res_data.get("data") == []



# ----------------------------- Scenario 03 ---------------------------------

@behave.given("Administrator has access to SLP service to search learner by email address")
def step_impl_1(context):
  learner_dict = copy(LEARNER_OBJECT_TEMPLATE)
  learner_dict["email_address"] = f"{uuid4()}_test_cuj3_feature2_scenario03@gmail.com"
  learner_dict["first_name"] = "UniqueFirstName"
  del learner_dict["uuid"]
  context.learner_email_address = learner_dict["email_address"]

  # Create learner using post request:
  api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner"
  post_req = post_method(url=api_url, request_body=learner_dict)
  assert post_req.status_code == 200, "Learner not created successfully"
  post_result = post_req.json()
  post_result_data = post_result.get("data")
  for key in DEL_KEYS:
    if key in post_result_data:
      del post_result_data[key]
    if key in learner_dict:
      del learner_dict[key]
  assert post_result_data == learner_dict, "Learner created dosent match expectecd response"

  context.params ={
      "email_address": context.learner_email_address
      }
  context.url = f"{api_url}/search"


@behave.when("Administrator wants to search learner based on correct email address")
def step_impl_2(context):
  context.get_res = get_method(url=context.url, query_params=context.params)
  context.get_res_data = context.get_res.json()


@behave.then("the relevant learner corresponding to given email address is retrieved and returned to user")
def step_impl_3(context):
  assert context.get_res.status_code == 200, "Status is not 200"
  assert context.get_res_data.get("success") is True
  assert context.get_res_data.get("message") == "Successfully fetched the learners"
  search_result = context.get_res_data.get("data")[0]
  del search_result["uuid"]
  assert search_result.get("email_address") == context.learner_email_address, "Wrong response received"


@behave.given("Administrator has access to SLP service to search learner "
              "by incorrect email address format")
def step_impl_1(context):
  api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner"
  context.params = {"email_address": "test.learner"}
  context.url = f"{api_url}/search"


@behave.when("Administrator wants to search learner based on incorrect "
             "email address format")
def step_impl_2(context):
  context.get_res = get_method(url=context.url, query_params=context.params)
  context.get_res_data = context.get_res.json()


@behave.then("getting error response learner email invalid")
def step_impl_3(context):
  assert context.get_res.status_code == 422
  assert context.get_res_data.get("success") is False
  assert context.get_res_data.get("data") is None



# ----------------------------- Scenario 04 ---------------------------------

@behave.given("Administrator has privilege to access SLP service to search learner by email address")
def step_impl_1(context):
  context.params ={
      "email_address": "Random@Email.com"
      }
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/search"


@behave.when("Administrator wants to search learner based on incorrect email address")
def step_impl_2(context):
  context.get_res = get_method(url=context.url, query_params=context.params)
  context.get_res_data = context.get_res.json()


@behave.then("SLP service will return empty response as no learner exists for given incorrect email address")
def step_impl_3(context):
  assert context.get_res.status_code == 200, "Status is not 200"
  assert context.get_res_data.get("success") is True
  assert context.get_res_data.get("message") == "Successfully fetched the learners"
  assert context.get_res_data.get("data") == []



# ----------------------------- Scenario 05 ---------------------------------
@behave.given("Administrator has access to SLP service to search goal by goal name")
def step_impl_1(context):
  goal_dict = copy(GOAL_OBJECT_TEMPLATE)
  goal_dict["name"] = "A Unique Goal"
  context.goal_name = goal_dict["name"]
  
  # Create goal using post request:
  api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/goal"
  post_req = post_method(url=api_url, request_body=goal_dict)
  post_result = post_req.json()
  post_result_data = post_result.get("data")
  del post_result_data["uuid"]
  del post_result_data["created_time"]
  del post_result_data["last_modified_time"]
  assert post_req.status_code == 200, "Goal not created successfully"
  assert post_result_data == goal_dict, "Goal created dosent match expectecd response"

  context.params ={
      "name": "A Unique Goal"
      }
  context.url = f"{api_url}/search"


@behave.when("Administrator wants to search goal based on correct goal name")
def step_impl_2(context):
  context.get_res = get_method(url=context.url, query_params=context.params)
  context.get_res_data = context.get_res.json()


@behave.then("the relevant goal corresponding to given goal name is retrieved and returned to user")
def step_impl_3(context):
  assert context.get_res.status_code == 200, "Status is not 200"
  assert context.get_res_data.get("success") is True
  assert context.get_res_data.get("message") == "Successfully fetched the goals"
  search_result = context.get_res_data.get("data")[0]
  del search_result["uuid"]
  assert search_result.get("name") == context.goal_name, "Response received"



# ----------------------------- Scenario 06 ---------------------------------

@behave.given("Administrator has privilege to access SLP service to search goal by goal name")
def step_impl_1(context):
  context.params ={
      "name": "Random Name xyz123123"
      }
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/goal/search"


@behave.when("Administrator wants to search goal by providing an incorrect goal name")
def step_impl_2(context):
  context.get_res = get_method(url=context.url, query_params=context.params)
  context.get_res_data = context.get_res.json()


@behave.then("SLP service will return empty response as no goal exists for given incorrect goal name")
def step_impl_3(context):
  assert context.get_res.status_code == 200, "Status is not 200"
  assert context.get_res_data.get("success") is True
  assert context.get_res_data.get("message") == "Successfully fetched the goals"
  assert context.get_res_data.get("data") == []


# ----------------------------- Scenario 07 ---------------------------------
@behave.given("Administrator has access to SLP service to search achievements by achievement type")
def step_impl_1(context):
  # Create achievement using post request:
  achievement_dict = copy(ACHIEVEMENT_OBJECT_TEMPLATE)
  context.achievement_type = achievement_dict["type"]
  api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/achievement"
  post_req = post_method(url=api_url, request_body=achievement_dict)
  post_result = post_req.json()
  post_result_data = post_result.get("data")
  del post_result_data["uuid"]
  del post_result_data["created_time"]
  del post_result_data["last_modified_time"]
  assert post_req.status_code == 200, "Achievement not created successfully"
  assert post_result_data == achievement_dict, "Achievement created dosent match expectecd response"

  context.params ={
      "type": "course equate"
      }
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/achievement/search"


@behave.when("Administrator wants to search achievements based on correct achievement type")
def step_impl_2(context):
  context.get_res = get_method(url=context.url, query_params=context.params)
  context.get_res_data = context.get_res.json()


@behave.then("the relevant achievements corresponding to given achievement type is retrieved and returned to user")
def step_impl_3(context):
  assert context.get_res.status_code == 200, "Status is not 200"
  assert context.get_res_data.get("success") is True
  assert context.get_res_data.get("message") == "Successfully fetched the achievements"
  search_result = context.get_res_data.get("data")[0]
  del search_result["uuid"]
  assert search_result.get("type") == context.achievement_type, "Response received does not match expected response"



# ----------------------------- Scenario 08 ---------------------------------

@behave.given("Administrator has access to SLP service to search learner profile by learner_id")
def step_impl_1(context):
  learner_profile_dict = copy(LEARNER_PROFILE_TEMPLATE)
  context.learning_goals = learner_profile_dict["learning_goals"]
  learner_dict = copy(LEARNER_OBJECT_TEMPLATE)
  learner_dict["email_address"] = f"{uuid4()}@gmail.com"
  
  # Create learner using post request:
  api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner"
  post_req = post_method(url=api_url, request_body=learner_dict)
  assert post_req.status_code == 200, "Learner not created successfully"
  learner_post_response = post_req.json()
  learner_id = learner_post_response.get("data").get("uuid")
  learner_profile_dict["learner_id"] = learner_id


  # Create learner-profile using post request:
  api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{learner_id}/learner-profile"
  post_req = post_method(url=api_url, request_body=learner_profile_dict)
  post_result = post_req.json()
  post_result_data = post_result.get("data")
  del post_result_data["uuid"]
  del post_result_data["created_time"]
  del post_result_data["last_modified_time"]
  assert post_req.status_code == 200, "Learner profile not created successfully"

  context.params ={
      "learner_id": learner_id
      }
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner-profile/search"


@behave.when("Administrator wants to search learner profile based on correct learner_id")
def step_impl_2(context):
  context.get_res = get_method(url=context.url, query_params=context.params)
  context.get_res_data = context.get_res.json()


@behave.then("the relevant learner profile corresponding to given learner_id is retrieved and returned to user")
def step_impl_3(context):
  assert context.get_res.status_code == 200, "Status is not 200"
  assert context.get_res_data.get("success") is True
  assert context.get_res_data.get("message") == "Successfully fetched the learner profiles"
  search_result = context.get_res_data.get("data")[0]
  del search_result["uuid"]
  assert search_result.get("learning_goals") == context.learning_goals, "Response received does not match expected response"


# ----------------------------- Scenario 09 ---------------------------------

@behave.given("Administrator has privilege to access SLP service to search learner profile by learner_id")
def step_impl_1(context):
  context.params ={
      "learner_id": "Random_ID"
      }
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner-profile/search"


@behave.when("Administrator wants to search learner profile by providing an incorrect learner_id")
def step_impl_2(context):
  context.get_res = get_method(url=context.url, query_params=context.params)
  context.get_res_data = context.get_res.json()

@behave.then("SLP service will return empty response as no learner profile exists for given incorrect learner_id")
def step_impl_3(context):
  assert context.get_res.status_code == 404, "Status is not 404"
  assert context.get_res_data.get("success") is False
  assert context.get_res_data.get("message") == "Learner with uuid Random_ID not found"
