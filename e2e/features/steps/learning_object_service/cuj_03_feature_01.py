"""
Integration with 3rd Party Tool | Frost (learning experience storage)
"""
import behave
import sys
from copy import copy

sys.path.append("../")
from setup import post_method, get_method, put_method
from test_config import API_URL_LEARNING_OBJECT_SERVICE, DEL_KEYS
from test_object_schemas import (TEST_LEARNING_OBJECT, TEST_LEARNING_EXPERIENCE,
                                TEST_LEARNING_RESOURCE)

API_URL = API_URL_LEARNING_OBJECT_SERVICE

#FILTER LEARNING OBJECT POSITIVE----------------------------------------------------

@behave.given("that an LXE or CD has access to the content authoring tool to filter learning objects with correct parameters")
def step_impl_1(context):
  #Creating a learning experience uuid
  context.le_payload = TEST_LEARNING_EXPERIENCE
  context.le_url= f"{API_URL}/learning-experience"
  context.le_res = post_method(url=context.le_url, request_body=context.le_payload)
  le_data = context.le_res.json()
  LE_UUID = le_data["data"]["uuid"]

  #creating learning object
  NEW_LO= copy(TEST_LEARNING_OBJECT)
  NEW_LO["parent_nodes"]["learning_experiences"].append(LE_UUID)
  context.payload = NEW_LO
  context.url= f"{API_URL}/learning-object"
  context.res = post_method(url=context.url, request_body=context.payload)
  
  context.url= f"{API_URL}/learning-objects"
  context.params = {"skip":0, "limit":30, "learning_experience": LE_UUID}

@behave.when("they filter for learning objects within that tool with correct parameters")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("LOS will serve up the most relevant search results based on the filter")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["message"] == "Data fetched successfully"
  fetched_los = context.res_data["data"]
  for lo in fetched_los:
    assert context.params["learning_experience"] in lo["parent_nodes"]["learning_experiences"]


#FILTER NEGATIVE
@behave.given("that an LXE or CD has access to the content authoring tool to filter learning objects with multiple parent/child node parameters")
def step_impl_1(context):
  context.params = {"skip":0, "limit":30, " learning_experience": "LE_UUID", "learning_resource": "LR_UUID"}
  context.url= f"{API_URL}/learning-objects"

@behave.when("they filter for learning objects within that tool with multiple parameters on parent/child nodes")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("LOS will throw Internal Server Error when filtering for learning objects")
def step_impl_3(context):
  assert context.res.status_code == 500


#FILTER LEARNING EXPERIENCE POSITIVE----------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool to filter learning experiences with correct parameters")
def step_impl_1(context):
  context.payload = TEST_LEARNING_EXPERIENCE
  context.url= f"{API_URL}/learning-experience"
  context.res = post_method(url=context.url, request_body=context.payload)
  create_data = context.res.json()
  context.req_id = create_data["data"]["uuid"]
  
  #Creating Learning object
  context.lo_payload = TEST_LEARNING_OBJECT
  context.lo_url= f"{API_URL}/learning-object"
  context.lo_res = post_method(url=context.lo_url, request_body=context.lo_payload)
  lo_data = context.lo_res.json()
  LO_UUID = lo_data["data"]["uuid"]
  
  #creating parent lo_uuid
  context.url= f"{API_URL}/learning-experiences"
  context.params = {"skip":0, "limit":30, "learning_object": LO_UUID}

@behave.when("they filter for learning experiences within that tool with correct parameters")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("LOS will serve up the most relevant learning experiences based on the filter")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["message"] == "Data fetched successfully"
  fetched_los = context.res_data["data"]
  for lo in fetched_los:
    assert context.params["learning_object"] in lo["child_nodes"]["learning_objects"]

#FILTER NEGATIVE
@behave.given("that an LXE or CD has access to the content authoring tool to filter learning experiences with multiple parent/child node parameters")
def step_impl_1(context):
  context.params = {"curriculum_pathway": "CP_UUID", "learning_resource": "LR_UUID",
  "author": "TestUser", "version": 1, "learning_opportunity": "LO_UUID"}
  context.url= f"{API_URL}/learning-experiences"

@behave.when("they filter for learning experiences within that tool with multiple parameters on parent/child nodes")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("LOS will throw Validation Failed when filtering for learning experiences")
def step_impl_3(context):
  assert context.res.status_code == 422


#FILTER LEARNING RESOURCE POSITIVE----------------------------------------

@behave.given("that an LXE or CD has access to the content authoring tool to filter learning resources with correct parameters")
def step_impl_1(context):
  context.payload = {**TEST_LEARNING_RESOURCE}
  context.url= f"{API_URL}/learning-resource"
  for key in DEL_KEYS:
    if key in context.payload:
      del context.payload[key]
  context.res = post_method(url=context.url, request_body=context.payload)
  
  context.url= f"{API_URL}/learning-resources"
  context.params = {
    "skip": 0, "limit": 30, 
    "concept": "concept_UUID",
    "version": 1,
    "is_archived": "true",
    "title": "title",
    "type": "testing type"
  }

@behave.when("they filter for learning resources within that tool with correct parameters")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("LOS will serve up the most relevant learning resources based on the filter")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["message"] == "Data fetched successfully"
  fetched_lrs = context.res_data["data"]
  for lr in fetched_lrs:
    assert context.params["concept"] in lr["child_nodes"]["concepts"]
    assert context.params["version"] == lr["version"]
    assert bool(context.params["is_archived"] == "true") == lr["is_archived"]
    assert context.params["title"] == lr["title"]
    assert context.params["type"] == lr["type"]


#FILTER NEGATIVE

@behave.given("that an LXE or CD has access to the content authoring tool to filter learning resources with multiple parent/child node parameters")
def step_impl_1(context):
  context.params = {
    "learning_object": "LO_UUID",
    "course_category": "Calculus",
    "version": 1
  }
  context.url= f"{API_URL}/learning-resources"

@behave.when("they filter for learning resources within that tool with multiple parameters on parent/child nodes")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("LOS will throw Validation Failed when filtering for learning resources")
def step_impl_3(context):
  assert context.res.status_code == 422
