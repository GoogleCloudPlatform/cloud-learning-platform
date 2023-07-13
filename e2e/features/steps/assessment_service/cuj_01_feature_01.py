"""
Feature 01 - CRUD for managing Assessment Item model in Assessment items
"""

import sys
import os
import json
import behave

sys.path.append("../")
from e2e.setup import post_method, get_method, put_method, delete_method
from e2e.test_object_schemas import TEST_ASSESSMENT_ITEM
from e2e.test_config import API_URL_ASSESSMENT_SERVICE, TESTING_OBJECTS_PATH

API_URL = API_URL_ASSESSMENT_SERVICE


#-------------------------------CREATE------------------------------------------
# --- Positive Scenario ---
@behave.given(
    "that a LXE  has access to Assessment Service and need to create an Assessment Item"
)
def step_impl_1(context):
  test_assessment_item = {**TEST_ASSESSMENT_ITEM}
  context.assessment_item_dict = test_assessment_item
  context.url = f"{API_URL}/assessment-item"


@behave.when(
    "API request is sent to create an Assessment Item with correct request payload"
)
def step_impl_2(context):
  context.res = post_method(
      url=context.url, request_body=context.assessment_item_dict)
  context.res_data = context.res.json()


@behave.then("that Assessment Item object will be created in the database")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the assessment item"
  assessment_item_uuid = context.res_data["data"]["uuid"]
  url = f"{API_URL}/assessment-item/{assessment_item_uuid}"
  get_resp = get_method(url)
  resp_json = get_resp.json()
  assert get_resp.status_code == 200
  assert resp_json["message"] == "Successfully fetched the assessment item"


# --- Negative Scenario ---
@behave.given(
    "that a LXE has access to Assessment Service and need to create an Assessment Item"
)
def step_impl_1(context):
  context.payload = {
      "child_nodes": {},
      "assessment_reference":
          "/learnosity/bf3793a4-39dd-4b0c-b82b-a624489d4e25",
  }
  context.url = f"{API_URL}/assessment-item"


@behave.when(
    "API request is sent to create Assessment Item with incorrect request payload"
)
def step_impl_2(context):
  context.res = post_method(url=context.url, request_body=context.payload)
  context.res_data = context.res.json()


@behave.then(
    "Assessment Item object will not be created and Assessment Service will throw a Validation error"
)
def step_impl_3(context):
  assert context.res.status_code == 422
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Validation Failed"
  assert context.res_data["data"][0]["msg"] == "field required"
  assert context.res_data["data"][0]["type"] == "value_error.missing"


#-------------------------------GET---------------------------------------------
# --- Positive Scenario ---
@behave.given(
    "that a LXE has access to Assessment Service and need to fetch an Assessment Item"
)
def step_impl_1(context):
  context.test_assessment_item = {**TEST_ASSESSMENT_ITEM}
  url = f"{API_URL}/assessment-item"
  post_res = post_method(url=url, request_body=context.test_assessment_item)
  post_res_data = post_res.json()
  assessment_item_uuid = post_res_data["data"]["uuid"]
  context.url = f"{API_URL}/assessment-item/{assessment_item_uuid}"


@behave.when(
    "API request is sent to fetch the Assessment Item with correct Assessment Item id"
)
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then(
    "the Assessment Service will serve up the requested Assessment Item")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data[
      "message"] == "Successfully fetched the assessment item"


# --- Negative Scenario ---
@behave.given(
    "that LXE has access to Assessment Service and need to fetch an Assessment Item"
)
def step_impl_1(context):
  invalid_assessment_item_uuid = "random_id"
  context.url = f"{API_URL}/assessment-item/{invalid_assessment_item_uuid}"


@behave.when(
    "API request is sent to fetch the Assessment Item with incorrect Assessment Item id"
)
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then(
    "the Assessment Item will not be fetched and Assessment Service will throw ResourceNotFound error"
)
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False, "Success is not False"
  assert context.res_data[
      "message"] == "Assessment Item with uuid random_id not found", "Expected message not returned"


#-------------------------------GET ALL-----------------------------------------
# --- Positive Scenario ---
@behave.given(
    "that a LXE has access to Assessment Service and needs to fetch all Assessment Item"
)
def step_impl_1(context):
  json_file_path = os.path.join(TESTING_OBJECTS_PATH, "assessment_item.json")
  assert os.path.exists(json_file_path)
  url = f"{API_URL}/assessment-item/import/json"
  with open(json_file_path, encoding="UTF-8") as assessment_item_json_file:
    post_res = post_method(url, files={"json_file": assessment_item_json_file})
    post_res_data = post_res.json()
    context.imported_assessment_item_ids = post_res_data["data"]
  context.url = f"{API_URL}/assessment-items"


@behave.when(
    "API request is sent to fetch all Assessment Item with correct request payload"
)
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("the Assessment Service will show all the Assessment Item")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data[
      "message"] == "Successfully fetched the assessment items"
  fetched_uuids = [i.get("uuid") for i in context.res_data.get("data")["records"]]
  assert set(context.imported_assessment_item_ids).intersection(set(fetched_uuids)) \
    == set(context.imported_assessment_item_ids), "all data not retrieved"


# --- Negative Scenario ---
@behave.given(
    "that a LXE can access Assessment Service and needs to fetch all Assessment Item"
)
def step_impl_1(context):
  context.url = f"{API_URL}/assessment-items"
  context.params = {"skip": "-1", "limit": "10"}


@behave.when(
    "API request is sent to fetch all Assessment Item with incorrect request payload"
)
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()


@behave.then(
    "the Assessment Item will not be fetched and Assessment Service will throw a Validation error"
)
def step_impl_3(context):
  assert context.res.status_code == 422, "Status not 422"
  assert context.res_data.get("message") == \
    "Validation Failed", \
    "unknown response received"


#-------------------------------UPDATE------------------------------------------
# --- Positive Scenario ---
@behave.given(
    "that a LXE has access to Assessment Service and needs to update an Assessment Item"
)
def step_impl_1(context):
  context.test_assessment_item = {**TEST_ASSESSMENT_ITEM}
  url = f"{API_URL}/assessment-item"
  post_res = post_method(url=url, request_body=context.test_assessment_item)
  post_res_data = post_res.json()
  assessment_item_uuid = post_res_data["data"]["uuid"]
  context.url = f"{API_URL}/assessment-item/{assessment_item_uuid}"


@behave.when(
    "API request is sent to update the Assessment Item with correct request payload"
)
def step_impl_2(context):
  updated_data = context.test_assessment_item
  updated_data["name"] = "test_update"
  context.res = put_method(url=context.url, request_body=updated_data)
  context.res_data = context.res.json()


@behave.then("that Assessment Item will be updated in the database")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data[
      "message"] == "Successfully updated the assessment item"
  assert context.res_data["data"]["name"] == "test_update"


# --- Negative Scenario ---
@behave.given(
    "that a LXE can access Assessment Service and needs to update an Assessment Item"
)
def step_impl_1(context):
  invalid_assessment_item_uuid = "random_id"
  context.url = f"{API_URL}/assessment-item/{invalid_assessment_item_uuid}"


@behave.when(
    "API request is sent to update the Assessment Item with incorrect Assessment Item id"
)
def step_impl_2(context):
  correct_payload = {"name": "test update1"}
  context.res = put_method(url=context.url, request_body=correct_payload)
  context.res_data = context.res.json()


@behave.then(
    "the Assessment Item will not be updated and Assessment Service will throw ResourceNotFound error"
)
def step_impl_3(context):
  context.res_data = context.res.json()
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data[
      "message"] == "Assessment Item with uuid random_id not found"


#-------------------------------DELETE------------------------------------------
# --- Positive Scenario ---
@behave.given(
    "that a LXE has access to Assessment Service and needs to delete an Assessment Item"
)
def step_impl_1(context):
  context.test_assessment_item = {**TEST_ASSESSMENT_ITEM}
  url = f"{API_URL}/assessment-item"
  post_res = post_method(url=url, request_body=context.test_assessment_item)
  post_res_data = post_res.json()
  assessment_item_uuid = post_res_data["data"]["uuid"]
  context.url = f"{API_URL}/assessment-item/{assessment_item_uuid}"


@behave.when(
    "API request is sent to delete the Assessment Item with correct Assessment Item id"
)
def step_impl_2(context):
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("that Assessment Item will be deleted from the database")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data[
      "message"] == "Successfully deleted the assessment item"
  get_resp = get_method(url=context.url)
  assert get_resp.status_code == 404, "Assessment Item not deleted"


# --- Negative Scenario ---
@behave.given(
    "that a LXE can access Assessment Service and needs to delete an Assessment Item"
)
def step_impl_1(context):
  invalid_assessment_item_uuid = "random_id"
  context.url = f"{API_URL}/assessment-item/{invalid_assessment_item_uuid}"


@behave.when(
    "API request is sent to delete the Assessment Item with incorrect Assessment Item id"
)
def step_impl_2(context):
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()


@behave.then(
    "the Assessment Item will not be deleted and Assessment Service will throw ResourceNotFound error"
)
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data[
      "message"] == "Assessment Item with uuid random_id not found"


#-------------------------------IMPORT------------------------------------------
# --- Positive Scenario ---
@behave.given(
    "that a LXE has access to Assessment Service and needs to import Assessment Item from JSON file"
)
def step_impl_1(context):
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH,
                                        "assessment_item.json")
  assert os.path.exists(context.json_file_path)
  context.url = f"{API_URL}/assessment-item/import/json"


@behave.when(
    "the Assessment Item are imported from correct JSON in request payload")
def step_impl_2(context):
  with open(
      context.json_file_path, encoding="UTF-8") as assessment_item_json_file:
    context.res = post_method(
        context.url, files={"json_file": assessment_item_json_file})
    context.res_data = context.res.json()


@behave.then("those Assessment Item will be added in the database")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data[
      "message"] == "Successfully created the assessment item"
  imported_assessment_item_ids = context.res_data["data"]

  get_assessment_item_url = f"{API_URL}/assessment-items"
  get_res = get_method(get_assessment_item_url)
  get_res_data = get_res.json()

  fetched_uuids = [i.get("uuid") for i in get_res_data.get("data")["records"]]
  assert set(imported_assessment_item_ids).intersection(set(fetched_uuids)) \
    == set(imported_assessment_item_ids), "all data not retrieved"


# --- Negative Scenario ---
@behave.given(
    "that a LXE can access Assessment Service and needs to import Assessment Item from JSON file"
)
def step_impl_1(context):
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH,
                                        "assessment_item_invalid.json")
  assert os.path.exists(context.json_file_path)
  context.url = f"{API_URL}/assessment-item/import/json"


@behave.when(
    "the Assessment Item are imported from incorrect JSON in request payload")
def step_impl_2(context):
  with open(
      context.json_file_path, encoding="UTF-8") as assessment_item_json_file:
    context.res = post_method(
        context.url, files={"json_file": assessment_item_json_file})
    context.res_data = context.res.json()


@behave.then(
    "the Assessment Item will not be imported and Assessment Service will throw Validation error"
)
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False, "Success is not True"
