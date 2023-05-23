"""
Feature 01 - CRUD for managing Activity State model in Learning Record Service
"""

import sys
import os
import behave
sys.path.append("../")
from common.models import ActivityState
from e2e.setup import post_method, get_method, put_method, delete_method
from e2e.test_object_schemas import TEST_ACTIVITY_STATE
from e2e.test_config import API_URL_LEARNING_RECORD_SERVICE, TESTING_OBJECTS_PATH

API_URL = API_URL_LEARNING_RECORD_SERVICE


#-------------------------------CREATE------------------------------------------
# --- Positive Scenario ---
@behave.given("A user has access to Learning Record Service and needs to create an Activity State")
def step_impl_1(context):
  test_activity_state = {**TEST_ACTIVITY_STATE}
  context.activity_state_dict = test_activity_state
  context.url = f"{API_URL}/activity-state"

@behave.when("API request is sent to create Activity State with correct request payload")
def step_impl_2(context):
  context.res = post_method(url=context.url, request_body=context.activity_state_dict)
  context.res_data = context.res.json()

@behave.then("that Activity State object will be created in the database")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["message"] == "Successfully created the activity state"
  activity_state_uuid = context.res_data["data"]["uuid"]
  url = f"{API_URL}/activity-state/{activity_state_uuid}"
  get_resp = get_method(url)
  resp_json = get_resp.json()
  assert get_resp.status_code == 200
  assert resp_json["message"] ==  "Successfully fetched the activity state"
  assert resp_json["data"]["agent_id"] == context.activity_state_dict["agent_id"]
  assert resp_json["data"]["activity_id"] == context.activity_state_dict["activity_id"]


# --- Negative Scenario ---
@behave.given("A user can access Learning Record Service and needs to create an Activity State")
def step_impl_1(context):
  context.payload= {
    "agent_id": "agent_id#1",
    "canonical_data": {}
  }
  context.url = f"{API_URL}/activity-state"

@behave.when("API request is sent to create Activity State with incorrect request payload")
def step_impl_2(context):
  context.res = post_method(url=context.url, request_body=context.payload)
  context.res_data = context.res.json()

@behave.then("Activity State object will not be created and Learning Record Service will throw a Validation error")
def step_impl_3(context):
  assert context.res.status_code == 422
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Validation Failed"
  assert context.res_data["data"][0]["msg"] == "field required"
  assert context.res_data["data"][0]["type"] == "value_error.missing"


#-------------------------------GET---------------------------------------------
# --- Positive Scenario ---
@behave.given("A user has access to Learning Record Service and needs to fetch an Activity State")
def step_impl_1(context):
  context.test_activity_state = {**TEST_ACTIVITY_STATE}
  url = f"{API_URL}/activity-state"
  post_res = post_method(url=url, request_body=context.test_activity_state)
  post_res_data = post_res.json()
  activity_state_uuid = post_res_data["data"]["uuid"]
  context.url = f"{API_URL}/activity-state/{activity_state_uuid}"

@behave.when("API request is sent to fetch the Activity State with correct Activity State id")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("the Learning Record Service will serve up the requested Activity State")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully fetched the activity state"
  assert context.res_data["data"]["agent_id"] == context.test_activity_state["agent_id"]
  assert context.res_data["data"]["activity_id"] == context.test_activity_state["activity_id"]


# --- Negative Scenario ---
@behave.given("A user can access Learning Record Service and needs to fetch an Activity State")
def step_impl_1(context):
  invalid_activity_state_uuid = "random_id"
  context.url = f"{API_URL}/activity-state/{invalid_activity_state_uuid}"

@behave.when("API request is sent to fetch the Activity State with incorrect Activity State id")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("The Activity State will not be fetched and Learning Record Service will throw ResourceNotFound error")
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False, "Success is not False"
  assert context.res_data["message"] == "Activity State with uuid random_id not found", "Expected message not returned"


#-------------------------------GET ALL-----------------------------------------
# --- Positive Scenario ---
@behave.given("A user has access to Learning Record Service and needs to fetch all Activity States")
def step_impl_1(context):
  json_file_path = os.path.join(TESTING_OBJECTS_PATH, "activity_states.json")
  assert os.path.exists(json_file_path)
  url = f"{API_URL}/activity-state/import/json"
  with open(json_file_path, encoding="UTF-8") as activity_states_json_file:
    post_res = post_method(url, files={"json_file": activity_states_json_file})
    post_res_data = post_res.json()
    context.imported_activity_state_ids = post_res_data["data"]
  context.url = f"{API_URL}/activity-states"

@behave.when("API request is sent to fetch all Activity States with correct request payload")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("the Learning Record Service will show all the Activity States")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully fetched the activity states"
  fetched_uuids = [i.get("uuid") for i in context.res_data.get("data")]
  assert set(context.imported_activity_state_ids).intersection(set(fetched_uuids)) \
    == set(context.imported_activity_state_ids), "all data not retrieved"


# --- Negative Scenario ---
@behave.given("A user can access Learning Record Service and needs to fetch all Activity States")
def step_impl_1(context):
  context.url = f"{API_URL}/activity-states"
  context.params = params = {"skip": "-1", "limit": "10"}

@behave.when("API request is sent to fetch all Activity States with incorrect request payload")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("The Activity States will not be fetched and Learning Record Service will throw a Validation error")
def step_impl_3(context):
  assert context.res.status_code == 422, "Status not 422"
  assert context.res_data.get("message") == \
    "Validation Failed", \
    "unknown response received"


#-------------------------------UPDATE------------------------------------------
# --- Positive Scenario ---
@behave.given("A user has access to Learning Record Service and needs to update an Activity State")
def step_impl_1(context):
  context.test_activity_state = {**TEST_ACTIVITY_STATE}
  url = f"{API_URL}/activity-state"
  post_res = post_method(url=url, request_body=context.test_activity_state)
  post_res_data = post_res.json()
  activity_state_uuid = post_res_data["data"]["uuid"]
  context.url = f"{API_URL}/activity-state/{activity_state_uuid}"

@behave.when("API request is sent to update the Activity State with correct request payload")
def step_impl_2(context):
  updated_data = context.test_activity_state
  updated_data["agent_id"] = "updated_agent_id"
  context.res = put_method(url=context.url, request_body=updated_data)
  context.res_data = context.res.json()

@behave.then("that Activity State will be updated in the database")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully updated the activity state"
  assert context.res_data["data"]["agent_id"] == "updated_agent_id"


# --- Negative Scenario ---
@behave.given("A user can access Learning Record Service and needs to update an Activity State")
def step_impl_1(context):
  invalid_activity_state_uuid = "random_id"
  context.url = f"{API_URL}/activity-state/{invalid_activity_state_uuid}"

@behave.when("API request is sent to update the Activity State with incorrect Activity State id")
def step_impl_2(context):
  correct_payload = {
      "agent_id": "updated_agent_id",
      "activity_id": "updated_activity_id",
      "canonical_data": {}
  }
  context.res = put_method(url=context.url, request_body=correct_payload)
  context.res_data = context.res.json()

@behave.then("The Activity State will not be updated and Learning Record Service will throw ResourceNotFound error")
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Activity State with uuid random_id not found"


#-------------------------------DELETE------------------------------------------
# --- Positive Scenario ---
@behave.given("A user has access to Learning Record Service and needs to delete an Activity State")
def step_impl_1(context):
  context.test_activity_state = {**TEST_ACTIVITY_STATE}
  url = f"{API_URL}/activity-state"
  post_res = post_method(url=url, request_body=context.test_activity_state)
  post_res_data = post_res.json()
  activity_state_uuid = post_res_data["data"]["uuid"]
  context.url = f"{API_URL}/activity-state/{activity_state_uuid}"

@behave.when("API request is sent to delete the Activity State with correct Activity State id")
def step_impl_2(context):
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("that Activity State will be deleted from the database")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully deleted the activity state"
  get_resp = get_method(url=context.url)
  assert get_resp.status_code == 404, "Activity State not deleted"


# --- Negative Scenario ---
@behave.given("A user can access Learning Record Service and needs to delete an Activity State")
def step_impl_1(context):
  invalid_activity_state_uuid = "random_id"
  context.url = f"{API_URL}/activity-state/{invalid_activity_state_uuid}"

@behave.when("API request is sent to delete the Activity State with incorrect Activity State id")
def step_impl_2(context):
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("The Activity State will not be deleted and Learning Record Service will throw ResourceNotFound error")
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Activity State with uuid random_id not found"


#-------------------------------IMPORT------------------------------------------
# --- Positive Scenario ---
@behave.given("A user has access to Learning Record Service and needs to import Activity State from JSON file")
def step_impl_1(context):
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "activity_states.json")
  assert os.path.exists(context.json_file_path)
  context.url = f"{API_URL}/activity-state/import/json"

@behave.when("the Activity States are imported from correct JSON in request payload")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as activity_states_json_file:
    context.res = post_method(context.url, files={"json_file": activity_states_json_file})
    context.res_data = context.res.json()

@behave.then("those Activity States will be added in the database")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully created the activity_states"
  imported_activity_state_ids = context.res_data["data"]

  get_activity_states_url = f"{API_URL}/activity-states"
  get_res = get_method(get_activity_states_url)
  get_res_data = get_res.json()
  fetched_uuids = [i.get("uuid") for i in get_res_data.get("data")]
  assert set(imported_activity_state_ids).intersection(set(fetched_uuids)) \
    == set(imported_activity_state_ids), "all data not retrieved"


# --- Negative Scenario ---
@behave.given("A user can access Learning Record Service and needs to import Activity State from JSON file")
def step_impl_1(context):
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "activity_states_invalid.json")
  assert os.path.exists(context.json_file_path)
  context.url = f"{API_URL}/activity-state/import/json"

@behave.when("the Activity States are imported from incorrect JSON in request payload")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as activity_states_json_file:
    context.res = post_method(context.url, files={"json_file": activity_states_json_file})
    context.res_data = context.res.json()

@behave.then("The Activity States will not be imported and Learning Record Service will throw Validation error")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False, "Success is not True"
  assert context.res_data["message"] == "Missing required fields - 'activity_id'"
