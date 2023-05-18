"""
Feature: CRUD for managing Staff in user management
"""
import os
import behave
import sys
from copy import deepcopy
from uuid import uuid4

sys.path.append("../")
from test_object_schemas import TEST_STAFF
from test_config import API_URL_USER_MANAGEMENT, TESTING_OBJECTS_PATH
from setup import post_method, get_method, put_method, delete_method

API_URL = f"{API_URL_USER_MANAGEMENT}/staff"

# ---------------------------------CREATE---------------------------------------

# --- Positive Scenario ---

# Scenario: Create a Staff with correct request payload

@behave.given("A user has permission to user management and wants to create a Staff with correct request payload")
def step_impl_1(context):
  staff_dict = deepcopy(TEST_STAFF)
  staff_dict["email"] = f"{uuid4()}@gmail.com"
  staff_dict["first_name"] = "Post"
  staff_dict["last_name"] = "Positive"
  context.request_body = staff_dict

@behave.when("API request is sent to create Staff with correct request payload")
def step_impl_2(context):
  context.url = f"{API_URL}"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()

@behave.then("Staff object will be created in the database as per given request payload")
def step_impl_3(context):
  assert context.res.status_code == 200, \
    f"Status is {context.res.status_code}"
  assert context.res_data["message"] == "Successfully created staff"
  staff_uuid = context.res_data["data"]["uuid"]
  url = f"{API_URL}/{staff_uuid}"
  request = get_method(url)
  resp = request.json()
  assert request.status_code == 200
  assert resp["success"] is True
  assert resp["data"]["first_name"] == context.request_body["first_name"]


# --- Negative Scenario ---

# Scenario: Create a Staff with incorrect request payload

@behave.given("A user has permission to user management and wants to create a Staff with incorrect request payload")
def step_impl_1(context):
  staff_dict = deepcopy(TEST_STAFF)
  staff_dict["phone_number"] = ["0000110011"]
  staff_dict["email"] = f"{uuid4()}@gmail.com"
  context.request_body = staff_dict

@behave.when("API request is sent to create Staff with incorrect request payload")
def step_impl_2(context):
  context.url = f"{API_URL}"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()

@behave.then("Staff object will not be created in the database and a ValidationError will be thrown")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["message"] == "Validation Failed"


# ---------------------------------SEARCH---------------------------------------

# Scenario: Search a Staff with correct request payload

@behave.given("A user has permission to user management and wants to search a Staff with correct request payload")
def step_impl_1(context):
  staff_dict = deepcopy(TEST_STAFF)
  staff_dict["email"] = f"{uuid4()}@gmail.com"
  context.staff_dict = staff_dict
  context.res = post_method(url=API_URL, request_body=staff_dict)

@behave.when("API request is sent to search Staff with correct request payload")
def step_impl_2(context):
  context.url = f"{API_URL}/search"
  context.params = params = {"email": context.staff_dict["email"]}
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("Staff object will be retrieved from the database as per given request payload")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["message"] == "Successfully fetched the staff"
  for data in context.res_data["data"]:
    assert data["email"] == context.staff_dict["email"]


@behave.given("A user has permission to user management and wants to search a "
              "Staff with incorrect request payload")
def step_impl_1(context):
  context.url = f"{API_URL}/search"
  context.params = {"email": "test.staff"}


@behave.when("API request is sent to search Staff with incorrect request "
             "payload")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()


@behave.then("Invalid payload error response raised")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False
  assert context.res_data["data"] is None

# -----------------------------------GET----------------------------------------

# --- Positive Scenario ---

# Scenario: Retrieve the Staff with correct uuid

@behave.given("A user has permission to user management and wants to retrieve the Staff with correct uuid")
def step_impl_1(context):
  staff_dict = deepcopy(TEST_STAFF)
  staff_dict["first_name"] = "Get"
  staff_dict["last_name"] =  "Positive"
  staff_dict["email"] = f"{uuid4()}@gmail.com"
  context.post_res = post_method(url=API_URL, request_body=staff_dict)
  assert context.post_res.status_code == 200
  context.post_res_json = context.post_res.json()
  context.uuid = context.post_res_json["data"]["uuid"]

@behave.when("API request is sent to retrieve the Staff with correct uuid")
def step_impl_2(context):
  context.url = f"{API_URL}/{context.uuid}"
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Staff object will be retrieved from the database as per given uuid")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["message"] == "Successfully fetched the staff"
  assert context.res_data["data"]["uuid"] == context.uuid


# --- Negative Scenario ---

# Scenario: Retrieve the Staff with incorrect uuid

@behave.given("A user has permission to user management and wants to retrieve the Staff with incorrect uuid")
def step_impl_1(context):
  context.uuid = "random_uuid"

@behave.when("API request is sent to retrieve the Staff with incorrect uuid")
def step_impl_2(context):
  context.url = f"{API_URL}/{context.uuid}"
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Staff object will not be retrieved from the database and a ResourceNotFoundException will be thrown")
def step_impl_3(context):
  assert context.res.status_code == 404
  assert context.res_data["message"] == "Staff with uuid random_uuid not found"


# ----------------------------------GET ALL-------------------------------------

# --- Positive Scenario ---

# Scenario: Retrieve all Staff with correct request payload

@behave.given("A user has permission to user management and wants to retrieve all Staff with correct request payload")
def step_impl_1(context):
  staff_dict = deepcopy(TEST_STAFF)
  staff_dict["email"] = f"{uuid4()}@gmail.com"
  context.payload = staff_dict

  post_staff = post_method(url=API_URL, request_body=context.payload)
  context.post_staff_data = post_staff.json()
  context.staff_uuid = context.post_staff_data["data"]["uuid"]
  assert post_staff.status_code == 200
  context.url = f"{API_URL}s"

@behave.when("API request is sent to retrieve all Staff with correct request payload")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("All Staff objects will be retrieved from the database")
def step_impl_3(context):
  assert context.res.status_code == 200, \
    f"Status is {context.res.status_code}"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Data fetched successfully"
  fetched_uuids = [i.get("uuid") for i in context.res_data.get(
    "data")["records"]]
  assert context.staff_uuid in fetched_uuids


# --- Negative Scenario ---

# Scenario: Retrieve all Staff with incorrect request payload

@behave.given("A user has permission to user management and wants to retrieve all Staff with incorrect request payload")
def step_impl_1(context):
  context.url = f"{API_URL}s"
  context.params = params = {"skip": "-1", "limit": "10"}

@behave.when("API request is sent to retrieve all Staff with incorrect request payload")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("Staff objects will not be retrieved from the database and a ValidationError will be thrown")
def step_impl_3(context):
  assert context.res.status_code == 422, "Status not 422"
  assert context.res_data.get("message") == \
    "Validation Failed"


# ----------------------------------UPDATE--------------------------------------

# --- Positive Scenario ---

# Scenario: Update a Staff with correct request payload

@behave.given("A user has permission to user management and wants to update a Staff with correct request payload")
def step_impl_1(context):
  staff_dict = deepcopy(TEST_STAFF)
  staff_dict["first_name"] = "PUT"
  staff_dict["last_name"] = "Positive"
  staff_dict["email"] = f"{uuid4()}@gmail.com"
  context.payload = staff_dict

  post_staff = post_method(url=API_URL, request_body=context.payload)
  context.post_staff_data = post_staff.json()
  context.staff_uuid = context.post_staff_data["data"]["uuid"]
  assert post_staff.status_code == 200

@behave.when("API request is sent to update a Staff with correct request payload")
def step_impl_2(context):
  context.url = f"{API_URL}/{context.staff_uuid}"
  updated_data = {"bio": "new and updated bio"}
  context.staff_bio = updated_data["bio"]
  context.res = put_method(url=context.url, request_body=updated_data)
  context.res_data = context.res.json()

@behave.then("Staff object will be updated in the database")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully updated the staff"
  assert context.res_data["data"]["bio"] == context.staff_bio


# --- Negative Scenario ---

# Scenario: Update a Staff with incorrect request payload

@behave.given("A user has permission to user management and wants to update a Staff with incorrect request payload")
def step_impl_1(context):
  invalid_staff_uuid = "random_id"
  context.url = f"{API_URL}/{invalid_staff_uuid}"

@behave.when("API request is sent to update a Staff with incorrect request payload")
def step_impl_2(context):
  staff_dict = {
    "phone_number": "1111111111"
  }
  context.res = put_method(url=context.url, request_body=staff_dict)
  context.res_data = context.res.json()

@behave.then("Staff object will not be updated in the database and a ValidationError will be thrown")
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Staff with uuid random_id not found"


# ----------------------------------DELETE--------------------------------------

# --- Positive Scenario ---

# Scenario: Delete a Staff with correct request payload

@behave.given("A user has permission to user management and wants to delete a Staff with correct request payload")
def step_impl_1(context):
  staff_dict = deepcopy(TEST_STAFF)
  staff_dict["email"] = f"{uuid4()}@gmail.com"
  context.payload = staff_dict

  post_staff = post_method(url=API_URL, request_body=context.payload)
  context.post_staff_data = post_staff.json()
  context.staff_uuid = context.post_staff_data["data"]["uuid"]
  assert post_staff.status_code == 200

@behave.when("API request is sent to delete a Staff with correct request payload")
def step_impl_2(context):
  context.url = f"{API_URL}/{context.staff_uuid}"
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Staff object will be deleted from the database")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully deleted the staff"
  get_res = get_method(url=context.url)
  assert get_res.status_code == 404


# --- Negative Scenario ---

# Scenario: Delete a Staff with incorrect uuid

@behave.given("A user has permission to user management and wants to delete a Staff with incorrect uuid")
def step_impl_1(context):
  invalid_staff_uuid = "random_id"
  context.url = f"{API_URL}/{invalid_staff_uuid}"

@behave.when("API request is sent to delete a Staff with incorrect uuid")
def step_impl_2(context):
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Staff object will not be deleted from the database and a ResourceNotFoundException will be thrown")
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Staff with uuid random_id not found"


# ----------------------------------IMPORT--------------------------------------

# --- Positive Scenario ---

# Scenario: Import Staffs from a JSON file with correct request payload

@behave.given("A user has permission to user management and wants to import Staffs from JSON file with correct request payload")
def step_impl_1(context):
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "staffs.json")
  assert os.path.exists(context.json_file_path)
  context.url = f"{API_URL}/import/json"

@behave.when("API request is sent to import Staffs with correct request payload")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as staff_json_file:
    context.res = post_method(context.url, files={"json_file": staff_json_file})
    context.res_data = context.res.json()

@behave.then("All the Staff objects in the JSON file will be created and added in the database")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully created the staffs"
  imported_staff_ids = context.res_data["data"]

  for uuid in imported_staff_ids:
    get_res = get_method(f"{API_URL}/{uuid}")
    assert get_res.status_code == 200


# --- Negative Scenario ---

# Scenario: Import Staffs from an invalid JSON file

@behave.given("A user has permission to user management and wants to import Staffs from an invalid JSON file")
def step_impl_1(context):
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "staffs_invalid.json")
  assert os.path.exists(context.json_file_path)
  context.url = f"{API_URL}/import/json"

@behave.when("API request is sent to import Staffs from invalid JSON file")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as staffs_json_file:
    context.res = post_method(context.url, files={"json_file": staffs_json_file})
    context.res_data = context.res.json()

@behave.then("Staff objects will not be imported and a ValidationError will be thrown")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False, "Success is not True"
  assert context.res_data["message"] == "Missing required fields - 'email'"
