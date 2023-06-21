"""
Create Activities
"""

import os
import behave
import sys
from uuid import uuid4
sys.path.append("../")
from e2e.setup import post_method, get_method, put_method, delete_method
from copy import deepcopy
from e2e.test_config import API_URL_LEARNING_RECORD_SERVICE

from e2e.test_object_schemas import TEST_ACTIVITY
from e2e.test_config import API_URL_LEARNING_RECORD_SERVICE, TESTING_OBJECTS_PATH

#-----------------------------------------CREATE ACTIVITY----------------------------------------------------------
# --- Positive Scenario ---
@behave.given("User has the ability to create activity and tries to create activity with correct payload")
def step_impl_1(context):
    """ Defining activity item for creation"""
    test_activity = deepcopy(TEST_ACTIVITY)
    context.activity_name = test_activity["name"] = str(uuid4())
    context.activity_dict = test_activity
    context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/activity"


@behave.when("API request is sent to create Activity with correct request payload")
def step_impl_2(context):
    """Creating the required node as per the input """
    context.res = post_method(url=context.url, request_body=context.activity_dict)
    context.res_data = context.res.json()

@behave.then("That activity is created successfully with the given request payload")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_data["message"] == "Successfully created the activity"
    id = context.res_data["data"]["uuid"]
    context.activity_id=id
    url = f"{API_URL_LEARNING_RECORD_SERVICE}/activity/{id}"
    request = get_method(url)
    opdata = request.json()
    assert request.status_code == 200
    assert opdata["message"] ==  "Successfully fetched the activity"
    assert opdata["data"]["name"] == context.activity_name
    # delete activity
    delete_method(url=url)


# --- Negative Scenario ---
@behave.given("User has the ability to create activity and tries to create activity with incorrect payload")
def step_impl_1(context):
    """ Defining an incorrect activity item for creation"""

    context.payload= {
        "canonical_data":{},
        "authority":"test authority"
    }
    context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/activity"

@behave.when("API request is sent to create Activity with incorrect request payload")
def step_impl_2(context):
    """Passing the query with incorrect params """
    context.res = post_method(url=context.url, request_body=context.payload)
    context.res_data = context.res.json()

@behave.then("Learning Record Service doesn't create Activity and throws validation error")
def step_impl_3(context):
    assert context.res.status_code == 422
    context.res_data = context.res.json()
    assert context.res_data["success"] is False
    assert context.res_data["message"] == "Validation Failed"
    assert context.res_data["data"][0]["msg"] == "field required"
    assert context.res_data["data"][0]["type"] == "value_error.missing"

#-----------------------------------------READ ACTIVITY----------------------------------------------------------
# --- Positive Scenario ---
@behave.given("User has access to learning record service and needs to view a particular activity using correct activity uuid")
def step_impl_1(context):
  context.test_activity = deepcopy(TEST_ACTIVITY)
  context.test_activity["name"] = str(uuid4())
  url = f"{API_URL_LEARNING_RECORD_SERVICE}/activity"
  post_res = post_method(url=url, request_body=context.test_activity)
  post_res_data = post_res.json()
  created_activity_uuid = post_res_data["data"]["uuid"]
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/activity/{created_activity_uuid}"

@behave.when("API request is sent to get Activity with correct activity uuid")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Learning record Service will serve up the requested activity")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully fetched the activity"
  assert context.res_data["data"]["name"] == context.test_activity["name"]
  # delete activity
  delete_method(url=context.url)

# --- Negative Scenario ---
@behave.given("User has access to learning record service and needs to view a particular activity using incorrect activity uuid")
def step_impl_1(context):
  context.uuid = "random_id"
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/activity/{context.uuid}"

@behave.when("API request is sent to get Activity with incorrect activity uuid")
def step_impl_1(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Learning Record Service will return resource not found")
def step_impl_1(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False, "success not False"
  assert context.res_data["message"] == "Activity with uuid random_id not found", "Expected message not returned"

#-----------------------------------------READ ALL ACTIVITIES----------------------------------------------------------
# --- Positive Scenario ---
@behave.given("User has the ability to get list of activities with correct request parameters")
def step_impl_1(context):
  json_file_path = os.path.join(TESTING_OBJECTS_PATH, "activities.json")
  assert os.path.exists(json_file_path)
  url = f"{API_URL_LEARNING_RECORD_SERVICE}/activity/import/json"
  with open(json_file_path, encoding="UTF-8") as activities_json_file:
    post_res = post_method(url, files={"json_file": activities_json_file})
    post_res_data = post_res.json()
    context.imported_activities_ids = post_res_data["data"]
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/activities"

@behave.when("API request is sent to get Activities with correct activity parameters")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Learning Record Service will serve list of activities based on correct request params")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Data fetched successfully"
  fetched_uuids = [i.get("uuid") for i in context.res_data.get("data")]
  assert set(context.imported_activities_ids).intersection(set(fetched_uuids)) \
    == set(context.imported_activities_ids), "all data not retrieved"

# --- Negative Scenario ---
@behave.given("User has the ability to get list of activities but provided incorrect parameters")
def step_impl_1(context):
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/activities"
  context.params = params = {"skip": "-1", "limit": "10"}

@behave.when("API request is sent to get Activities with incorrect activity parameters")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("Learning Record Service will throw validation error for incorrect paramaters")
def step_impl_3(context):
  assert context.res.status_code == 422, "Status not 422"
  assert context.res_data.get("message") == \
    "Validation Failed", \
    "unknown response received"
#-----------------------------------------UPDATE ACTIVITY----------------------------------------------------------
# --- Positive scenario ---
@behave.given("User has access to learning record Service and needs to update a activity")
def step_impl_1(context):
  context.test_activity = deepcopy(TEST_ACTIVITY)
  context.test_activity["name"] = str(uuid4())
  url = f"{API_URL_LEARNING_RECORD_SERVICE}/activity"
  post_res = post_method(url=url, request_body=context.test_activity)
  post_res_data = post_res.json()
  created_activity_uuid = post_res_data["data"]["uuid"]
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/activity/{created_activity_uuid}"

@behave.when("Api request is sent to update activity with correct request payload")
def step_impl_2(context):
  updated_data = context.test_activity
  updated_data["name"] = "Random Updated Name"
  context.res = put_method(url=context.url, request_body=updated_data)
  context.res_data = context.res.json()

@behave.then("that activity should be updated successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully updated the activity"
  assert context.res_data["data"]["name"] == "Random Updated Name"
  # delete activity
  delete_method(url=context.url)

# --- Negative Scenario ---
@behave.given("User has access to Learning Record Service and needs to update a activity using invalid uuid")
def step_impl_1(context):
  invalid_activity_uuid = "random_id"
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/activity/{invalid_activity_uuid}"

@behave.when("API request is sent to update activity by providing invalid uuid")
def step_impl_2(context):
  correct_payload = {
      "name": f"{uuid4()} activity",
      "authority": "Test Authority",
      "canonical_data": {}
  }
  context.res = put_method(url=context.url, request_body=correct_payload)
  context.res_data = context.res.json()

@behave.then("Activity is not updated and Learning Record Service will throw a resource not found error")
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Activity with uuid random_id not found"

#-----------------------------------------DELETE ACTIVITY----------------------------------------------------------
# --- Positive Scenario ---
@behave.given("User has access to Learning Record Service and needs to delete a activity")
def step_impl_1(context):
  context.test_activity = deepcopy(TEST_ACTIVITY)
  context.test_activity["name"] = str(uuid4())
  url = f"{API_URL_LEARNING_RECORD_SERVICE}/activity"
  post_res = post_method(url=url, request_body=context.test_activity)
  post_res_data = post_res.json()
  created_activity_uuid = post_res_data["data"]["uuid"]
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/activity/{created_activity_uuid}"

@behave.when("API request is sent to delete activity by providing correct uuid")
def step_impl_2(context):
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Activity object will be deleted successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully deleted the Activity"
  # delete activity
  delete_method(url=context.url)

# --- Negative Scenario ---
@behave.given("User has access to Learning Record Service and needs to delete a activity using incorrect uuid")
def step_impl_1(context):
  invalid_activity_uuid = "random_id"
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/activity/{invalid_activity_uuid}"

@behave.when("API request is sent to delete activity by providing incorrect uuid")
def step_impl_2(context):
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Activity object will not be deleted and Learning Record Service will throw a resource not found error")
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Activity with uuid random_id not found"

#-----------------------------------------IMPORT ACTIVITIES----------------------------------------------------------
# --- Positive Scenario ---
@behave.given("We have access to raw data in json format for activity")
def step_impl_1(context):
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "activities.json")
  assert os.path.exists(context.json_file_path)
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/activity/import/json"

@behave.when("Learning Record Service accesses this activity json data with correct payload request")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as activity_json_file:
    context.res = post_method(context.url, files={"json_file": activity_json_file})
    context.res_data = context.res.json()

@behave.then("activity json data will be imported into Learning Record Service")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully created the activities"
  imported_activity_ids = context.res_data["data"]

  get_activities_url = f"{API_URL_LEARNING_RECORD_SERVICE}/activities"
  get_res = get_method(get_activities_url)
  get_res_data = get_res.json()
  fetched_uuids = [i.get("uuid") for i in get_res_data.get("data")]
  assert set(imported_activity_ids).intersection(set(fetched_uuids)) \
    == set(imported_activity_ids), "all data not retrieved"


# --- Negative Scenario --- 1
@behave.given("We have access to raw data of json type with invalid json schema for activity")
def step_impl_1(context):
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "activities_invalid.json")
  assert os.path.exists(context.json_file_path)
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/activity/import/json"

@behave.when("Learning Record Service accesses this activity json data with invalid json schema")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as activities_json_file:
    context.res = post_method(context.url, files={"json_file": activities_json_file})
    context.res_data = context.res.json()

@behave.then("activity data from given json file will not get imported and Learning Record Service will throw a validation error")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False, "Success is not True"
  assert context.res_data["message"] == "Missing required fields - 'name'"


# --- Negative Scenario --- 2
@behave.given("We have access to raw data for activity in csv format")
def step_impl_1(context):
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "sample_csv_file.csv")
  assert os.path.exists(context.json_file_path)
  context.url = f"{API_URL_LEARNING_RECORD_SERVICE}/activity/import/json"

@behave.when("Learning Record Service accesses this activity data in csv format instead of JSON")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as activities_json_file:
    context.res = post_method(context.url, files={"json_file": activities_json_file})
    context.res_data = context.res.json()

@behave.then("activity data from given csv file will not get imported and Learning Record Service will throw a validation error")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False, "Success is not True"
  assert context.res_data["message"] == "Valid JSON file type is supported"
