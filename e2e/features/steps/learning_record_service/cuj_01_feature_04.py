"""
Feature 04 - CRUD API Test for managing Agent data in Learning Record Service
"""
import behave
import sys
import os
from uuid import uuid4
sys.path.append("../")
from setup import post_method, get_method, put_method, delete_method, set_cache, get_cache
from copy import deepcopy
from common.models import User
from test_object_schemas import TEST_AGENT, TEST_USER
from test_config import API_URL_LEARNING_RECORD_SERVICE, API_URL_USER_MANAGEMENT, TESTING_OBJECTS_PATH

#-------------------------------CREATE AGENT-------------------------------------
# --- Positive Scenario ---
@behave.given("A user has access to Learning Record Service and needs to create a Agent")
def step_impl_1(context):
  input_user = {**TEST_USER, "email": f"{uuid4()}@gmail.com"}
  user = User.from_dict(input_user)
  user.user_type_ref = ""
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  context.test_user_id= user.id
  set_cache(key="test_user_id", value=user.id)
  test_agent = deepcopy({**TEST_AGENT, "user_id":context.test_user_id})
  context.agent_dict = test_agent
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/agent"

@behave.when("API request is sent to create Agent with correct request payload")
def step_impl_2(context):
  context.res = post_method(url=context.url,
  request_body=context.agent_dict)
  context.res_data = context.res.json()
  set_cache(key="agent_id", value=context.res_data["data"]["uuid"])

@behave.then("Agent object will be created successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  created_agent_uuid = context.res_data["data"]["uuid"]
  url = f"{API_URL_LEARNING_RECORD_SERVICE}/agent/{created_agent_uuid}"
  request = get_method(url)
  opdata = request.json()
  assert request.status_code == 200
  assert opdata["message"] ==  "Successfully fetched the agent"
  assert opdata["data"]["user_id"] == context.agent_dict["user_id"]

# --- Negative Scenario ---
@behave.given("A user has access privileges to Learning Record Service and needs to create a Agent")
def step_impl_1(context):
  context.payload= {
    "account_name": "test_account_name",
    "account_homepage": "hp1",
    "members": [],
    "user_id": "user_id_1"
  }
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/agent"

@behave.when("API request is sent to create Agent with incorrect request payload")
def step_impl_2(context):
  context.res = post_method(url=context.url, request_body=context.payload)
  context.res_data = context.res.json()

@behave.then("Agent object will not be created and Learning Record Service will throw a validation error")
def step_impl_3(context):
  assert context.res.status_code == 422
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Validation Failed"
  assert context.res_data["data"][0]["msg"] == "field required"
  assert context.res_data["data"][0]["type"] == "value_error.missing"

#-------------------------------GET AGENT-------------------------------------
# --- Positive Scenario ---
@behave.given("A user has access to Learning Record Service and needs to fetch a Agent")
def step_impl_1(context):
  test_user_id=get_cache(key="test_user_id")
  context.test_agent = deepcopy({**TEST_AGENT, "user_id":test_user_id})
  created_agent_uuid = get_cache(key="agent_id")
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/agent/{created_agent_uuid}"

@behave.when("API request is sent to fetch Agent by providing correct uuid")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Agent object corresponding to given uuid will be returned successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully fetched the agent"
  assert context.res_data["data"]["user_id"] == get_cache(key="test_user_id")

# --- Negative Scenario ---
@behave.given("A user has access privileges to Learning Record Service and needs to fetch a Agent")
def step_impl_1(context):
  invalid_agent_uuid = "random_id"
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/agent/{invalid_agent_uuid}"

@behave.when("API request is sent to fetch Agent by providing invalid uuid")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Agent object will not be returned and Resource not found error will be thrown by Learning Record Service")
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False, "success not False"
  assert context.res_data["message"] == "Agent with uuid random_id not found", "Expected message not returned"


#------------------------GET AGENT BY USER ------------------------------
# --- Positive Scenario ---
@behave.given("A user has access to Learning Record Service and needs to fetch Agent associated with a User")
def step_impl_1(context):
  test_user_id=get_cache(key="test_user_id")
  context.test_agent = deepcopy({**TEST_AGENT, "user_id":test_user_id})
  created_agent_uuid = get_cache(key="agent_id")
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/agents"
  context.params = {"user_id" : test_user_id}

@behave.when("API request is sent to fetch Agent by providing user id associated with that agent")
def step_impl_2(context):
  context.res = get_method(url=context.url,query_params=context.params)
  context.res_data = context.res.json()

@behave.then("Agent object corresponding to given user id will be returned successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Data fetched successfully"
  assert context.res_data["data"][0]["user_id"] == get_cache(key="test_user_id")

#-------------------------------GET ALL AGENTS-----------------------------------
# --- Positive Scenario ---
@behave.given("A user has access to Learning Record Service and needs to fetch all Agents")
def step_impl_1(context):

  json_file_path = os.path.join(TESTING_OBJECTS_PATH, "agents.json")
  assert os.path.exists(json_file_path)
  url = f"{API_URL_LEARNING_RECORD_SERVICE}/agent/import/json"
  with open(json_file_path, encoding="UTF-8") as agents_json_file:
    post_res = post_method(url, files={"json_file": agents_json_file})
    post_res_data = post_res.json()
    context.imported_agent_ids = post_res_data["data"]
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/agents"

@behave.when("API request is sent to fetch all agents")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Learning Record Service will return all existing Agent objects successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Data fetched successfully"
  fetched_uuids = [i.get("uuid") for i in context.res_data.get("data")]
  assert set(context.imported_agent_ids).intersection(set(fetched_uuids)) \
    == set(context.imported_agent_ids), "all data not retrieved"


#-------------------------------UPDATE AGENT-------------------------------------
# --- Positive Scenario ---
@behave.given("A user has access to Learning Record Service and needs to update a Agent")
def step_impl_1(context):
  test_user_id=get_cache(key="test_user_id")
  context.test_agent = deepcopy({**TEST_AGENT, "user_id":test_user_id})
  created_agent_uuid = get_cache(key="agent_id")
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/agent/{created_agent_uuid}"

@behave.when("API request is sent to update Agent with correct request payload")
def step_impl_2(context):
  updated_data = context.test_agent
  updated_data["name"] = "Random Updated Name"
  context.res = put_method(url=context.url, request_body=updated_data)
  context.res_data = context.res.json()

@behave.then("Agent object will be updated successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully updated the agent"
  assert context.res_data["data"]["name"] == "Random Updated Name"

# --- Negative Scenario 1 ---
@behave.given("A user has access privileges to Learning Record Service and needs to update an already existing Agent")
def step_impl_1(context):
  test_user_id=get_cache(key="test_user_id")
  context.test_agent = deepcopy({**TEST_AGENT, "user_id":test_user_id})
  created_agent_uuid = get_cache(key="agent_id")
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/agent/{created_agent_uuid}"

@behave.when("API request is sent to update agent with incorrect request payload")
def step_impl_2(context):
  incorrect_payload= {
      "agent_name": "Test Agent Name",
      "account_homepage": "Test Agent HP URL",
      "members": []
  }
  context.res = put_method(url=context.url, request_body=incorrect_payload)
  context.res_data = context.res.json()

@behave.then("Agent object will not be updated and Learning Record Service will throw a validation error")
def step_impl_3(context):
  assert context.res.status_code == 422
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Validation Failed"
  assert context.res_data["data"][0]["msg"] == "extra fields not permitted"
  assert context.res_data["data"][0]["type"] == "value_error.extra"

# --- Negative Scenario 2 ---
@behave.given("A user has access privileges to Learning Record Service and needs to update a Agent")
def step_impl_1(context):
  invalid_agent_uuid = "random_id"
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/agent/{invalid_agent_uuid}"

@behave.when("API request is sent to update Agent by providing invalid uuid")
def step_impl_2(context):
  correct_payload = {
      "name": "Test Agent Name",
      "account_homepage": "Test Agent HP URL"
  }
  context.res = put_method(url=context.url, request_body=correct_payload)
  context.res_data = context.res.json()

@behave.then("Agent object will not be updated and Learning Record Service will throw a resource not found error")
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Agent with uuid random_id not found"

#-------------------------------DELETE AGENT-------------------------------------
# --- Positive Scenario ---
@behave.given("A user has access to Learning Record Service and needs to delete a Agent")
def step_impl_1(context):
  test_user_id = get_cache(key="test_user_id")
  context.test_agent = deepcopy({**TEST_AGENT, "user_id":test_user_id})
  created_agent_uuid = get_cache(key="agent_id")
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/agent/{created_agent_uuid}"

@behave.when("API request is sent to delete Agent by providing correct uuid")
def step_impl_2(context):
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Agent object will be deleted successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully deleted the agent"

# --- Negative Scenario ---
@behave.given("A user has access privileges to Learning Record Service and needs to delete a Agent")
def step_impl_1(context):
  invalid_agent_uuid = "random_id"
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/agent/{invalid_agent_uuid}"

@behave.when("API request is sent to delete Agent by providing invalid uuid")
def step_impl_2(context):
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Agent object will not be deleted and Learning Record Service will throw a resource not found error")
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Agent with uuid random_id not found"


#-------------------------------IMPORT AGENTS-----------------------------------
# --- Positive Scenario ---
@behave.given("We have access to raw data in json format for agent")
def step_impl_1(context):
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "agents.json")
  assert os.path.exists(context.json_file_path)
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/agent/import/json"

@behave.when("Learning Record Service accesses this agent json data with correct payload request")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as agents_json_file:
    context.res = post_method(context.url, files={"json_file": agents_json_file})
    context.res_data = context.res.json()

@behave.then("Agent json data will be imported into Learning Record Service")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully created the agents"
  imported_agent_ids = context.res_data["data"]

  get_agents_url = f"{API_URL_LEARNING_RECORD_SERVICE}/agents"
  get_res = get_method(get_agents_url)
  get_res_data = get_res.json()
  fetched_uuids = [i.get("uuid") for i in get_res_data.get("data")]
  assert set(imported_agent_ids).intersection(set(fetched_uuids)) \
    == set(imported_agent_ids), "all data not retrieved"

# --- Negative Scenario 1---
@behave.given("We have access to raw data of json type with invalid json schema for Agent")
def step_impl_1(context):
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "agents_invalid.json")
  assert os.path.exists(context.json_file_path)
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/agent/import/json"

@behave.when("Learning Record Service accesses this Agent json data with invalid json schema")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as agents_json_file:
    context.res = post_method(context.url, files={"json_file": agents_json_file})
    context.res_data = context.res.json()

@behave.then("Agent data from given json file will not get imported and Learning Record Service will throw a validation error")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False, "Success is not True"
  assert context.res_data["message"] == "Missing required fields - 'name'"
