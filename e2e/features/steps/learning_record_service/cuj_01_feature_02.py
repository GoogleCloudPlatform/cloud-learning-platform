"""
Feature 02 - CRUD API Test for managing Verb data in Learning Record Service
"""
import behave
import sys
import os
sys.path.append("../")
from e2e.setup import post_method, get_method, put_method, delete_method, set_cache, get_cache
from copy import deepcopy
from e2e.test_object_schemas import TEST_VERB
from e2e.test_config import API_URL_LEARNING_RECORD_SERVICE, TESTING_OBJECTS_PATH


#-------------------------------CREATE VERB-------------------------------------
# --- Positive Scenario ---
@behave.given("A user has access to Learning Record Service and needs to create a verb")
def step_impl_1(context):
  test_verb = deepcopy(TEST_VERB)
  test_verb["name"] = "verb name"
  context.verb_dict = test_verb
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/verb"

@behave.when("API request is sent to create verb with correct request payload")
def step_impl_2(context):
  context.res = post_method(url=context.url, request_body=context.verb_dict)
  context.res_data = context.res.json()
  set_cache(key="verb_id", value=context.res_data["data"]["uuid"])

@behave.then("Verb object will be created successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["message"] == "Successfully created the verb"
  verb_uuid = context.res_data["data"]["uuid"]
  url = f"{API_URL_LEARNING_RECORD_SERVICE}/verb/{verb_uuid}"
  request = get_method(url)
  opdata = request.json()
  assert request.status_code == 200
  assert opdata["message"] ==  "Successfully fetched the verb"
  assert opdata["data"]["name"] == context.verb_dict["name"]
  assert opdata["data"]["url"] == context.verb_dict["url"]


# --- Negative Scenario ---
@behave.given("A user has access privileges to Learning Record Service and needs to create a verb")
def step_impl_1(context):
  context.payload= {
      "verb": "Test Verb Name",
      "url": "Test Verb URL",
      "canonical_data": {}
  }
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/verb"

@behave.when("API request is sent to create verb with incorrect request payload")
def step_impl_2(context):
  context.res = post_method(url=context.url, request_body=context.payload)
  context.res_data = context.res.json()

@behave.then("verb object will not be created and Learning Record Service will throw a validation error")
def step_impl_3(context):
  assert context.res.status_code == 422
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Validation Failed"
  assert context.res_data["data"][0]["msg"] == "field required"
  assert context.res_data["data"][0]["type"] == "value_error.missing"



#-------------------------------GET VERB-------------------------------------
# --- Positive Scenario ---
@behave.given("A user has access to Learning Record Service and needs to fetch a verb")
def step_impl_1(context):
  context.test_verb = deepcopy(TEST_VERB)
  verb_uuid = get_cache(key="verb_id")
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/verb/{verb_uuid}"

@behave.when("API request is sent to fetch verb by providing correct uuid")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Verb object corresponding to given uuid will be returned successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully fetched the verb"
  assert context.res_data["data"]["name"] == "verb name"
  assert context.res_data["data"]["url"] == context.test_verb["url"]


# --- Negative Scenario ---
@behave.given("A user has access privileges to Learning Record Service and needs to fetch a verb")
def step_impl_1(context):
  invalid_verb_uuid = "random_id"
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/verb/{invalid_verb_uuid}"

@behave.when("API request is sent to fetch verb by providing invalid uuid")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("verb object will not be returned and Resource not found error will be thrown by Learning Record Service")
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False, "success not False"
  assert context.res_data["message"] == "Verb with uuid random_id not found", "Expected message not returned"



#-------------------------------GET ALL VERBS-----------------------------------
# --- Positive Scenario ---
@behave.given("A user has access to Learning Record Service and needs to fetch all verbs")
def step_impl_1(context):
  json_file_path = os.path.join(TESTING_OBJECTS_PATH, "verbs.json")
  assert os.path.exists(json_file_path)
  url = f"{API_URL_LEARNING_RECORD_SERVICE}/verb/import/json"
  with open(json_file_path, encoding="UTF-8") as verbs_json_file:
    post_res = post_method(url, files={"json_file": verbs_json_file})
    post_res_data = post_res.json()
    context.imported_verb_ids = post_res_data["data"]
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/verbs"

@behave.when("API request is sent to fetch all verbs")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Learning Record Service will return all existing verb objects successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Data fetched successfully"
  fetched_uuids = [i.get("uuid") for i in context.res_data.get(
    "data")["records"]]
  assert set(context.imported_verb_ids).intersection(set(fetched_uuids)) \
    == set(context.imported_verb_ids), "all data not retrieved"


# --- Negative Scenario ---
@behave.given("A user can access Learning Record Service and needs to fetch all verbs")
def step_impl_1(context):
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/verbs"
  context.params = params = {"skip": "-1", "limit": "10"}

@behave.when("API request is sent to fetch all verbs with incorrect request payload")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("The verbs will not be fetched and Learning Record Service will throw a Validation error")
def step_impl_3(context):
  assert context.res.status_code == 422, "Status not 422"
  assert context.res_data.get("message") == \
    "Validation Failed", \
    "unknown response received"


#-------------------------------UPDATE VERB-------------------------------------
# --- Positive Scenario ---
@behave.given("A user has access to Learning Record Service and needs to update a verb")
def step_impl_1(context):
  context.test_verb = deepcopy(TEST_VERB)
  verb_uuid = get_cache(key="verb_id")
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/verb/{verb_uuid}"

@behave.when("API request is sent to update verb with correct request payload")
def step_impl_2(context):
  updated_data = context.test_verb
  updated_data["name"] = "Random Updated Name"
  context.res = put_method(url=context.url, request_body=updated_data)
  context.res_data = context.res.json()

@behave.then("Verb object will be updated successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully updated the verb"
  assert context.res_data["data"]["name"] == "Random Updated Name"


# --- Negative Scenario ---
@behave.given("A user has access privileges to Learning Record Service and needs to update a verb")
def step_impl_1(context):
  invalid_verb_uuid = "random_id"
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/verb/{invalid_verb_uuid}"

@behave.when("API request is sent to update verb by providing invalid uuid")
def step_impl_2(context):
  correct_payload = {
      "name": "Test Verb Name",
      "url": "Test Verb URL",
      "canonical_data": {}
  }
  context.res = put_method(url=context.url, request_body=correct_payload)
  context.res_data = context.res.json()

@behave.then("verb object will not be updated and Learning Record Service will throw a resource not found error")
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Verb with uuid random_id not found"



#-------------------------------DELETE VERB-------------------------------------
# --- Positive Scenario ---
@behave.given("A user has access to Learning Record Service and needs to delete a verb")
def step_impl_1(context):
  verb_uuid = get_cache(key="verb_id")
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/verb/{verb_uuid}"

@behave.when("API request is sent to delete verb by providing correct uuid")
def step_impl_2(context):
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Verb object will be deleted successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully deleted the verb"


# --- Negative Scenario ---
@behave.given("A user has access privileges to Learning Record Service and needs to delete a verb")
def step_impl_1(context):
  invalid_verb_uuid = "random_id"
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/verb/{invalid_verb_uuid}"

@behave.when("API request is sent to delete verb by providing invalid uuid")
def step_impl_2(context):
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("verb object will not be deleted and Learning Record Service will throw a resource not found error")
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Verb with uuid random_id not found"



#-------------------------------IMPORT VERBS-----------------------------------
# --- Positive Scenario ---
@behave.given("We have access to raw data in json format for verb")
def step_impl_1(context):
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "verbs.json")
  assert os.path.exists(context.json_file_path)
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/verb/import/json"

@behave.when("Learning Record Service accesses this verb json data with correct payload request")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as verbs_json_file:
    context.res = post_method(context.url, files={"json_file": verbs_json_file})
    context.res_data = context.res.json()

@behave.then("verb json data will be imported into Learning Record Service")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully created the verbs"
  imported_verb_ids = context.res_data["data"]

  get_verbs_url = f"{API_URL_LEARNING_RECORD_SERVICE}/verbs"
  get_res = get_method(get_verbs_url)
  get_res_data = get_res.json()
  fetched_uuids = [i.get("uuid") for i in get_res_data.get(
    "data")["records"]]
  assert set(imported_verb_ids).intersection(set(fetched_uuids)) \
    == set(imported_verb_ids), "all data not retrieved"


# --- Negative Scenario 1---
@behave.given("We have access to raw data of json type with invalid json schema for verb")
def step_impl_1(context):
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "verbs_invalid.json")
  assert os.path.exists(context.json_file_path)
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/verb/import/json"

@behave.when("Learning Record Service accesses this verb json data with invalid json schema")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as verbs_json_file:
    context.res = post_method(context.url, files={"json_file": verbs_json_file})
    context.res_data = context.res.json()

@behave.then("verb data from given json file will not get imported and Learning Record Service will throw a validation error")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False, "Success is not True"
  assert context.res_data["message"] == "Missing required fields - 'name'"


# --- Negative Scenario 2---
@behave.given("We have access to raw data for verb in csv format")
def step_impl_1(context):
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "sample_csv_file.csv")
  assert os.path.exists(context.json_file_path)
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/verb/import/json"

@behave.when("Learning Record Service accesses this verb data in csv format instead of JSON")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as verbs_json_file:
    context.res = post_method(context.url, files={"json_file": verbs_json_file})
    context.res_data = context.res.json()

@behave.then("verb data from given csv file will not get imported and Learning Record Service will throw a validation error")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False, "Success is not True"
  assert context.res_data["message"] == "Valid JSON file type is supported"
