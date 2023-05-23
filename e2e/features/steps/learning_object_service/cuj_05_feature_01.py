"""
Create, Read, Update and Delete learning object and curriculum pathways
"""

import behave
import uuid
import os
from copy import copy
import sys

sys.path.append("../")
from e2e.setup import post_method, get_method, put_method, delete_method
from e2e.test_config import API_URL_LEARNING_OBJECT_SERVICE, TESTING_OBJECTS_PATH, DEL_KEYS
from e2e.test_object_schemas import (TEST_CURRICULUM_PATHWAY)


API_URL = API_URL_LEARNING_OBJECT_SERVICE
# ---------------------------- Creation (Positive) --------------------------------------

@behave.given("that a LXE or CD has access to the content authoring tool to create curriculum pathway")
def step_impl1(context):
  context.req_body = copy(TEST_CURRICULUM_PATHWAY)
  for key in DEL_KEYS:
    if key in context.req_body:
      del context.req_body[key]
  context.url = f"{API_URL}/curriculum-pathway"

@behave.when("they design the curriculum pathway using a third party tool")
def step_impl(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()

@behave.then("the curriculum pathways will be created in a third-party tool and stored inside LOS")
def step_impl(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert "uuid" in context.res_data["data"]
  assert "created_time" in context.res_data["data"]
  assert "last_modified_time" in context.res_data["data"]
  context.req_id = context.res_data["data"]["uuid"]

@behave.then("all metadata for curriculum pathway will be ingested and stored in learning object service")
def step_impl(context):
  url = f"{API_URL}/curriculum-pathway/{context.req_id}"
  context.params = {"fetch_tree": False, "frontend_response": False}
  res = get_method(url=url, query_params=context.params)
  context.get_data = res.json()
  assert res.status_code == 200

@behave.then("uuid for curriculum pathways will be stored in learning object service")
def step_impl(context):
  assert "uuid" in context.get_data["data"]
  assert context.get_data["data"]["uuid"] == context.req_id

# ---------------------------- Creation (Negative) --------------------------------------

@behave.given("that a LXE or CD has access to content authoring tool to create curriculum pathway with invalid request")
def step_2_1(context):
  context.req_body = copy(TEST_CURRICULUM_PATHWAY)
  context.req_body["title"] = "Title"
  context.url = f"{API_URL}/curriculum-pathway"

@behave.when("they design the curriculum pathway using a third party tool with invalid request")
def step_2_2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()

@behave.then("the curriculum pathways will not be created in learning object service")
def step_2_3(context):
  assert context.res.status_code == 422

# ---------------------------- Updation (Positive) --------------------------------------

@behave.given("that an LXE or CD has access to the content authoring tool to update the curriculum pathway with correct payload")
def step_3_1_1(context):
  cp_dict = copy(TEST_CURRICULUM_PATHWAY)
  context.url = f"{API_URL}/curriculum-pathway"
  for key in DEL_KEYS:
    if key in cp_dict:
      del cp_dict[key]
  context.res = post_method(url=context.url,request_body=cp_dict)
  context.res_data = context.res.json()
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  context.req_id = context.res_data["data"]["uuid"]


@behave.when("they update the curriculum pathway using a third-party tool")
def step_3_1_2(context):
  cp_dict = copy(TEST_CURRICULUM_PATHWAY)
  cp_dict["name"] = "Kubernetes Platform"
  cp_dict["description"] = "Kubernetes was developed by Google"
  for key in DEL_KEYS:
    if key in cp_dict:
      del cp_dict[key]
  context.request = cp_dict
  context.params = {"create_version": False}
  context.url = f"{API_URL}/curriculum-pathway/{context.req_id}"
  context.res = put_method(url=context.url, query_params=context.params,
            request_body=cp_dict)
  context.res_data = context.res.json()

@behave.then("the curriculum pathways will be updated in a third-party tool")
def step_3_1_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.req_id
  assert context.res_data["data"]["name"] == "Kubernetes Platform"
  assert context.res_data["data"]["description"] == "Kubernetes was developed by Google"
  assert context.res_data["data"]["is_archived"] == False


@behave.then("all metadata will be updated in learning object service for the curriculum pathway")
def step_3_1_4(context):
  url = f"{API_URL}/curriculum-pathway/{context.req_id}"
  context.params = {"fetch_tree": False, "frontend_response": False}
  res = get_method(url=url, query_params=context.params)
  context.get_data = res.json()
  assert res.status_code == 200
  assert context.get_data["data"]["metadata"] == context.request["metadata"]
  assert context.get_data["data"]["version"] == 1

# ---------------------------- Update and Create Version --------------------------------------

@behave.given("that an LXE or CD has access to the content authoring tool to create version of curriculum pathway")
def step_3_2_1(context):
  cp_dict = copy(TEST_CURRICULUM_PATHWAY)
  for key in DEL_KEYS:
    if key in cp_dict:
      del cp_dict[key]
  context.url = f"{API_URL}/curriculum-pathway"
  context.res = post_method(url=context.url,request_body=cp_dict)
  context.res_data = context.res.json()
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  context.req_id = context.res_data["data"]["uuid"]

@behave.when("they update the curriculum pathway using a third-party tool to create version")
def step_3_2_2(context):
  cp_dict = copy(TEST_CURRICULUM_PATHWAY)
  cp_dict["name"] = "Online Platform"
  cp_dict["description"] = "Online Platform was developed by Google"
  for key in DEL_KEYS:
    if key in cp_dict:
      del cp_dict[key]
  context.request = cp_dict
  context.params = {"create_version": True}
  context.url = f"{API_URL}/curriculum-pathway/{context.req_id}"
  context.res = put_method(url=context.url, query_params=context.params,
              request_body=cp_dict)
  context.res_data = context.res.json()
  context.updated_doc_id = context.res_data["data"]["uuid"]

@behave.then("a version of curriculum pathway will be created")
def step_3_2_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["name"] == "Online Platform"
  assert context.res_data["data"]["parent_version_uuid"] == context.req_id

@behave.then("all metadata for the curriculum pathway will be updated learning object service")
def step_3_2_4(context):
  url = f"{API_URL}/curriculum-pathway/{context.req_id}"
  context.params = {"fetch_tree": False, "frontend_response": False}
  res = get_method(url=url, query_params=context.params)
  context.get_data = res.json()
  assert res.status_code == 200
  assert context.get_data["data"]["metadata"] == context.request["metadata"]

@behave.then("a version document for the curriculum pathway will be created in learing object service")
def step_3_2_5(context):
  url = f"{API_URL}/curriculum-pathway/{context.req_id}"
  context.params = {"fetch_tree": False, "frontend_response": False}
  res = get_method(url=url, query_params=context.params)
  context.get_data = res.json()
  assert res.status_code == 200
  assert context.res_data["data"]["version"] != 1
  assert context.res_data["data"]["uuid"] != context.req_id

# ---------------------------- Updation (Negative 1) --------------------------------------

@behave.given("that an LXE or CD has access to content authoring tool with invalid uuid for the curriculum pathway")
def step_4_1(context):
  cp_dict = copy(TEST_CURRICULUM_PATHWAY)
  for key in DEL_KEYS:
    if key in cp_dict:
      del cp_dict[key]
  context.url = f"{API_URL}/curriculum-pathway"
  context.res = post_method(url=context.url,request_body=cp_dict)
  context.res_data = context.res.json()
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  context.req_id = context.res_data["data"]["uuid"]

@behave.when("they update the curriculum pathway using a third-party tool with invalid uuid")
def step_4_2(context):
  context.req_id = str(uuid.uuid4())
  cp_dict = copy(TEST_CURRICULUM_PATHWAY)
  cp_dict["name"] = "Kubernetes Platform"
  cp_dict["description"] = "Kubernetes was developed by Google"
  for key in DEL_KEYS:
    if key in cp_dict:
      del cp_dict[key]
  context.url = f"{API_URL}/curriculum-pathway/{context.req_id}"
  context.res = put_method(url=context.url, request_body=cp_dict)
  context.res_data = context.res.json()

@behave.then("the curriculum pathways will not be updated in learning object service")
def step_4_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data["message"] == f"Curriculum Pathway with uuid {context.req_id} not found"

# ---------------------------- Updation (Negative 2) --------------------------------------

@behave.given("that a LXE has access to content authoring tool with invalid request payload for the curriculum pathway")
def step_5_1(context):
  cp_dict = copy(TEST_CURRICULUM_PATHWAY)
  for key in DEL_KEYS:
    if key in cp_dict:
      del cp_dict[key]
  context.url = f"{API_URL}/curriculum-pathway"
  context.res = post_method(url=context.url,request_body=cp_dict)
  context.res_data = context.res.json()
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  context.req_id = context.res_data["data"]["uuid"]

@behave.when("they update the curriculum pathway using a third-party tool with invalid request")
def step_5_2(context):
  cp_dict = copy(TEST_CURRICULUM_PATHWAY)
  cp_dict["title"] = "Kubernetes was developed by Google"
  for key in DEL_KEYS:
    if key in cp_dict:
      del cp_dict[key]
  context.url = f"{API_URL}/curriculum-pathway/{context.req_id}"
  context.res = put_method(url=context.url, request_body=cp_dict)
  context.res_data = context.res.json()

@behave.then("the curriculum pathway will not be updated in learning object service")
def step_5_3(context):
  assert context.res.status_code == 422

# ---------------------------- Deletion (Positive) --------------------------------------

@behave.given("that an LXE has access to content authoring tool to delete curriculum pathway with correct payload")
def step_6_1(context):
  cp_dict = copy(TEST_CURRICULUM_PATHWAY)
  for key in DEL_KEYS:
    if key in cp_dict:
      del cp_dict[key]
  context.url = f"{API_URL}/curriculum-pathway"
  context.res = post_method(url=context.url,request_body=cp_dict)
  context.res_data = context.res.json()
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  context.req_id = context.res_data["data"]["uuid"]

@behave.when("they delete the curriculum pathway using a third-party tool")
def step_6_2(context):
  context.url = f"{API_URL}/curriculum-pathway/{context.req_id}"
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("the curriculum pathways will be deleted from a third-party tool")
def step_6_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["message"] == "Successfully deleted the curriculum pathway"

@behave.then("all metadata will be deleted from learning object service for the curriculum pathway")
def step_6_4(context):
  url = f"{API_URL}/curriculum-pathway/{context.req_id}"
  context.params = {"fetch_tree": False, "frontend_response": False}
  res = get_method(url=url, query_params=context.params)
  context.get_data = res.json()
  assert res.status_code == 404
  assert context.get_data["message"] == f"Curriculum Pathway with uuid {context.req_id} not found"

# ---------------------------- Deletion (Negative) --------------------------------------

@behave.given("that an LXE has access to the content authoring tool to delete curriculum pathway with incorrect uuid")
def step_7_1(context):
  cp_dict = copy(TEST_CURRICULUM_PATHWAY)
  for key in DEL_KEYS:
    if key in cp_dict:
      del cp_dict[key]
  context.url = f"{API_URL}/curriculum-pathway"
  context.res = post_method(url=context.url,request_body=cp_dict)
  context.res_data = context.res.json()
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  context.req_id = context.res_data["data"]["uuid"]

@behave.when("they delete the curriculum pathway using a third-party tool wiht incorrect uuid")
def step_7_2(context):
  context.req_id = str(uuid.uuid4())
  context.url = f"{API_URL}/curriculum-pathway/{context.req_id}"
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("the curriculum pathways will not be deleted from learning object service")
def step_7_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data["message"] == f"Curriculum Pathway with uuid {context.req_id} not found"

# ---------------------------- Ingestion (Positive) --------------------------------------

@behave.given("that an CD or LXE has access to the content authoring tool to import curriculum pathway with correct json")
def step_8_1(context):
  context.url = f"{API_URL}/curriculum-pathway/import/json"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH,
                                        "curriculum_pathways.json")
  assert os.path.exists(context.json_file_path)

@behave.when("Curriculum Pathway JSON data with correct payload request is imported")
def step_8_2(context):
  with open(context.json_file_path, encoding="UTF-8") as lx_json_file:
    context.res = post_method(context.url, files={"json_file": lx_json_file})
    context.res_data = context.res.json()

@behave.then("That Curriculum Pathway JSON data should be ingested into learning object service")
def step_8_3(context):
  assert context.res.status_code == 200, "Status not 200"
  assert isinstance(context.res_data.get("data"), list), "Response is not a list"
  assert len(
      context.res_data.get("data")) > 0, "Empty list returned in import json api"
  inserted_lx_uuids = context.res_data.get("data")
  api_url = f"{API_URL}/curriculum-pathways"
  params = {"skip": 0, "limit": 30}
  resp = get_method(api_url, query_params=params)
  resp_data = resp.json()
  assert resp.status_code == 200, "Status not 200"
  lx_uuids = [i.get("uuid") for i in resp_data.get("data")]
  assert set(inserted_lx_uuids).intersection(set(lx_uuids)) \
    == set(inserted_lx_uuids), "all data not retrieved"

# ---------------------------- Ingestion (Negative) --------------------------------------

@behave.given("that a CD or LXE has access to the content authoring tool to import curriculum pathway with incorrect json")
def step_9_1(context):
  context.url = f"{API_URL}/curriculum-pathway/import/json"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH,
                                        "curriculum_pathways_invalid.json")
  context.required_fields = "'name'"
  assert os.path.exists(context.json_file_path)

@behave.when("Curriculum Pathway JSON data with incorrect payload request is imported")
def step_9_2(context):
  with open(context.json_file_path, encoding="UTF-8") as lx_json_file:
    context.res = post_method(context.url, files={"json_file": lx_json_file})
    context.res_data = context.res.json()

@behave.then("ingestion of Curriculum Pathway JSON data into learning object service should fail")
def step_9_3(context):
  # JSON file without required fields
  assert context.res.status_code == 422, "Status should be 422 if required fields are missing"
  assert context.res_data.get(
      "message") == f"Missing required fields - {context.required_fields}", "Expected response message is not same"


# Scenario: Fetch all nodes under a Program for a given alias

@behave.given("that a CD or LXE wants to fetch all nodes of the given alias under a program")
def step_11_1(context):
  cp_dict_discipline = copy(TEST_CURRICULUM_PATHWAY)
  cp_dict_discipline["alias"] = "discipline"
  context.url = f"{API_URL}/curriculum-pathway"
  for key in DEL_KEYS:
    if key in cp_dict_discipline:
      del cp_dict_discipline[key]
  context.res = post_method(url=context.url,request_body=cp_dict_discipline)
  context.res_data = context.res.json()
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  context.cp_discpline_uuid = context.res_data["data"]["uuid"]

  cp_dict_level = copy(TEST_CURRICULUM_PATHWAY)
  cp_dict_level["alias"] = "level"
  cp_dict_level["child_nodes"] = {
    "curriculum_pathways": [context.cp_discpline_uuid]
  }
  for key in DEL_KEYS:
    if key in cp_dict_level:
      del cp_dict_level[key]
  context.res = post_method(url=context.url,request_body=cp_dict_level)
  context.res_data = context.res.json()
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  context.cp_level_uuid = context.res_data["data"]["uuid"]

  cp_dict_program = copy(TEST_CURRICULUM_PATHWAY)
  cp_dict_program["alias"] = "discipline"
  cp_dict_program["child_nodes"] = {
    "curriculum_pathways": [context.cp_level_uuid]
  }
  for key in DEL_KEYS:
    if key in cp_dict_program:
      del cp_dict_program[key]
  context.res = post_method(url=context.url,request_body=cp_dict_program)
  context.res_data = context.res.json()
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  context.req_id = context.res_data["data"]["uuid"]

@behave.when("API request is sent to fetch all nodes with alias and correct program id")
def step_11_2(context):
  context.params = {"alias": "level"}
  context.url = f"{API_URL}/curriculum-pathway/{context.req_id}/nodes"
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("All nodes of the given alias under that program will be fetched")
def step_11_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"][0]["uuid"] == context.cp_level_uuid
