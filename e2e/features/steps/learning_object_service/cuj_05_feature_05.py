"""
Integration with 3rd Party Tool | Filter on Curriculum Pathways
"""
import behave
import sys
from copy import copy

sys.path.append("../")
from e2e.setup import post_method, get_method, put_method
from e2e.test_config import API_URL_LEARNING_OBJECT_SERVICE, DEL_KEYS
from e2e.test_object_schemas import (TEST_CURRICULUM_PATHWAY, TEST_LEARNING_EXPERIENCE)

API_URL = API_URL_LEARNING_OBJECT_SERVICE

#FILTER CURRICULUM PATHWAY POSITIVE----------------------------------------

@behave.given("that an LXE or CD has access to the content authoring tool to filter curriculum pathways with correct parameters")
def step_impl_1(context):
  context.payload = TEST_CURRICULUM_PATHWAY
  context.url= f"{API_URL}/curriculum-pathway"
  context.res = post_method(url=context.url, request_body=context.payload)
  create_data = context.res.json()
  context.req_id = create_data["data"]["uuid"]
  
  #Creating Learning Experience
  context.le_payload = TEST_LEARNING_EXPERIENCE
  context.le_url= f"{API_URL}/learning-experience"
  context.le_res = post_method(url=context.le_url, request_body=context.le_payload)
  le_data = context.le_res.json()
  LE_UUID = le_data["data"]["uuid"]
  
  #creating parent le_uuid
  context.url= f"{API_URL}/curriculum-pathways"
  context.params = {"skip":0, "limit":30, "learning_experience": LE_UUID}

@behave.when("they filter for curriculum pathways within that tool with correct parameters")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("LOS will serve up the most relevant curriculum pathways based on the filter")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["message"] == "Data fetched successfully"
  fetched_cps = context.res_data["data"]
  for lo in fetched_cps:
    assert context.params["learning_experience"] in lo["child_nodes"]["learning_experiences"]

#FILTER NEGATIVE
@behave.given("that an LXE or CD has access to the content authoring tool to filter curriculum pathways with multiple parent/child node parameters")
def step_impl_1(context):
  context.params = {"learning_experience": "LE_UUID",
  "author": "TestUser", "version": 1, "learning_opportunity": "LE_UUID"}
  context.url= f"{API_URL}/curriculum-pathways"

@behave.when("they filter for curriculum pathways within that tool with multiple parameters on parent/child nodes")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("LOS will throw Validation Failed when filtering for curriculum pathways")
def step_impl_3(context):
  assert context.res.status_code == 422


#FILTER ARCHIVED CURRICULUM PATHWAY POSITIVE----------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool to filter archived curriculum pathways with correct parameters")
def step_impl_1(context):

  CP = copy(TEST_CURRICULUM_PATHWAY)
  context.payload = TEST_CURRICULUM_PATHWAY
  context.url= f"{API_URL}/curriculum-pathway"
  for key in DEL_KEYS:
    if key in context.payload:
      del context.payload[key]
  context.res = post_method(url=context.url, request_body=context.payload)
  create_data = context.res.json()
  context.req_id = create_data["data"]["uuid"]

  #archiving the created curriculum pathway using put method
  context.update_params = {"is_archived": True}
  context.update_url = f"{API_URL}/curriculum-pathway/{context.req_id}"
  context.update_res = put_method(url=context.update_url, query_params=context.update_params,
              request_body=CP)

  context.url= f"{API_URL}/curriculum-pathways"
  context.params = {"skip":0, "limit":30, "fetch_archive": True}

@behave.when("they filter for archived curriculum pathways within that tool with correct parameters")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("LOS will serve up the most relevant archived curriculum pathways based on the filter")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["message"] == "Data fetched successfully"
  fetched_cps = context.res_data["data"]
  for lo in fetched_cps:
    assert lo["is_archived"] is True

#FILTER UNARCHIVED CURRICULUM PATHWAY POSITIVE----------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool to filter unarchived curriculum pathways with correct parameters")
def step_impl_1(context):

  #Creating unarchived Curriculum Pathway
  context.payload = TEST_CURRICULUM_PATHWAY
  for key in DEL_KEYS:
    if key in context.payload:
      del context.payload[key]
  context.url= f"{API_URL}/curriculum-pathway"
  context.res = post_method(url=context.url, request_body=context.payload)
  create_data = context.res.json()
  context.req_id = create_data["data"]["uuid"]
  
  context.url= f"{API_URL}/curriculum-pathways"
  context.params = {"skip":0, "limit":30,"fetch_archive": False}

@behave.when("they filter for unarchived curriculum pathways within that tool with correct parameters")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("LOS will serve up only the unarchived curriculum pathways based on the filter")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["message"] == "Data fetched successfully"
  fetched_cps = context.res_data["data"]
  for cp in fetched_cps:
    assert cp["is_archived"] is False
