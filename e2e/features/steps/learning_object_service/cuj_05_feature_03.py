"""
Integration with 3rd Party Tool | Frost (Clone Functionality)
"""

import time
import behave
from copy import copy

import sys 
sys.path.append("../")
from setup import get_method, post_method
from test_config import API_URL_LEARNING_OBJECT_SERVICE, DEL_KEYS
from test_object_schemas import TEST_CURRICULUM_PATHWAY

API_URL = API_URL_LEARNING_OBJECT_SERVICE

@behave.given("that an LXE or CD has access to the content authoring tool and needs to copy a curriculum pathway")
def step_impl_1(context):
  cp_dict = copy(TEST_CURRICULUM_PATHWAY)
  for key in DEL_KEYS:
    if key in cp_dict:
      del cp_dict[key]
  context.url = f"{API_URL}/curriculum-pathway"
  context.res = post_method(url=context.url, request_body=cp_dict)
  context.res_data = context.res.json()
  context.cp_id = context.res_data["data"]["uuid"]
  context.url = f"{API_URL}/curriculum-pathway/copy/{context.cp_id}"
  
@behave.when("there is a request to copy a particular curriculum pathway with correct id")
def step_impl_2(context):
  context.res = post_method(url = context.url)
  context.res_data = context.res.json()

@behave.then("a copy of the requested curriculum pathway will be returned")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True

  #fetch original curriculum pathway
  context.params = {"fetch_tree": False, "frontend_response": False}
  retrieve_url = f"{API_URL}/curriculum-pathway/{context.cp_id}"
  response = get_method(url = retrieve_url, query_params=context.params)
  assert response.status_code == 200, "retrieval failed"
  response_data = response.json()

  #drop irrelevant fields
  for key in DEL_KEYS:
    if key in context.res_data["data"]:
      del context.res_data["data"][key]
    if key in response_data["data"]:
      del response_data["data"][key]
  assert context.res_data["data"] == response_data["data"]



@behave.given("an LXE or CD has access to the content authoring tool and needs to copy a curriculum pathway")
def step_impl_1(context):
  context.cp_id = "random_id"
  context.url = f"{API_URL}/curriculum-pathway/copy/{context.cp_id}"

@behave.when("there is a request to copy a particular curriculum pathway with incorrect id")
def step_impl_2(context):
  context.res = post_method(url = context.url)
  context.res_data = context.res.json()

@behave.then("Learning Object Service will fail to copy the curriculum pathway due to invalid curriculum pathway id")
def step_impl_3(context):
  time.sleep(20)
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data["data"] is None
