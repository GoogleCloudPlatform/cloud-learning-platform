"""
Integration with 3rd Party Tool | Frost (curriculum pathway storage)
"""

import time
import behave
from copy import copy
import sys
import uuid
sys.path.append("../")
from setup import get_method, post_method
from test_config import API_URL_LEARNING_OBJECT_SERVICE, DEL_KEYS
from test_object_schemas import TEST_CURRICULUM_PATHWAY

API_URL = API_URL_LEARNING_OBJECT_SERVICE

@behave.given("that an LXE or CD has access to the content authoring tool and needs to view the curriculum pathway")
def step_impl_1(context):
  cp_dict = copy(TEST_CURRICULUM_PATHWAY)
  context.url = f"{API_URL}/curriculum-pathway"
  for key in DEL_KEYS:
    if key in cp_dict:
      del cp_dict[key]
  context.res = post_method(url=context.url, request_body=cp_dict)
  context.res_data = context.res.json()
  context.cp_id = context.res_data["data"]["uuid"]
  context.url = f"{API_URL}/curriculum-pathway/{context.cp_id}"
  context.params = {"fetch_tree": False, "frontend_response": False}
  
@behave.when("there is a request to view a particular curriculum pathway with correct id")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("the requested curriculum pathway will be retrieved")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.cp_id


@behave.given("that an LXE or CD has access to the content authoring tool and needs to view all versions of the curriculum pathway")
def step_impl_1(context):
  cp_dict = copy(TEST_CURRICULUM_PATHWAY)
  context.url = f"{API_URL}/curriculum-pathway"
  for key in DEL_KEYS:
    if key in cp_dict:
      del cp_dict[key]
  context.res = post_method(url=context.url, request_body=cp_dict)
  context.res_data = context.res.json()
  context.cp_id = context.res_data["data"]["uuid"]
  context.params = {"fetch_all": True}
  context.url = f"{API_URL}/curriculum-pathway/{context.cp_id}"

@behave.when("there is a request to view all versions of curriculum pathway with correct id")
def step_impl_2(context):
  context.res = get_method(url = context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("all the versions of the requested curriculum pathway will be retrieved")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.cp_id

@behave.given("that an LXE or CD has access to the content authoring tool and needs to view a specific version of the curriculum pathway")
def step_impl_1(context):
  cp_dict = copy(TEST_CURRICULUM_PATHWAY)
  context.url = f"{API_URL}/curriculum-pathway"
  for key in DEL_KEYS:
    if key in cp_dict:
      del cp_dict[key]
  context.res = post_method(url=context.url, request_body=cp_dict)
  context.res_data = context.res.json()
  context.cp_id = context.res_data["data"]["uuid"]
  context.params = {"version": 1}
  context.url = f"{API_URL}/curriculum-pathway/{context.cp_id}"

@behave.when("there is a request to view a particular version of the curriculum pathway with correct id")
def step_impl_2(context):
  context.res = get_method(url = context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("the requested version of the curriculum pathway will be retrieved")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.cp_id

@behave.given("an LXE or CD has access to the content authoring tool and needs to view the curriculum pathway")
def step_impl_1(context):
  context.cp_id = "random_id"
  context.url = f"{API_URL}/curriculum-pathway/{context.cp_id}"

@behave.when("there is a request to view a particular curriculum pathway with incorrect id")
def step_impl_2(context):
  context.res = get_method(url = context.url)
  context.res_data = context.res.json()

@behave.then("Learning Object Service will throw an error message for accessing invalid curriculum pathway")
def step_impl_3(context):
  time.sleep(20)
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data["data"] is None
