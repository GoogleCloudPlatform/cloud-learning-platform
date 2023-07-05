"""
Integration with 3rd Party Tool | Frost (learning experience storage)
"""

import time
import behave
from copy import copy
import sys
import uuid
sys.path.append("../")
from e2e.setup import get_method, post_method
from e2e.test_config import API_URL_LEARNING_OBJECT_SERVICE, DEL_KEYS
from e2e.test_object_schemas import (TEST_LEARNING_OBJECT, TEST_LEARNING_EXPERIENCE, TEST_LEARNING_RESOURCE)

API_URL = API_URL_LEARNING_OBJECT_SERVICE

@behave.given("that an LXE or CD has access to the content authoring tool and needs to view the learning experience")
def step_impl_1(context):
  lx_dict = copy(TEST_LEARNING_EXPERIENCE)
  context.url = f"{API_URL}/learning-experience"
  for key in DEL_KEYS:
    if key in lx_dict:
      del lx_dict[key]
  context.res = post_method(url=context.url, request_body=lx_dict)
  context.res_data = context.res.json()
  context.le_id = context.res_data["data"]["uuid"]
  context.url = f"{API_URL}/learning-experience/{context.le_id}"
  
@behave.when("there is a request to view a particular learning experience with correct id")
def step_impl_2(context):
  context.res = get_method(url = context.url)
  context.res_data = context.res.json()

@behave.then("the requested learning experience will be retrieved")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.le_id


@behave.given("that an LXE or CD has access to the content authoring tool and needs to view all versions of the learning experience")
def step_impl_1(context):
  lx_dict = copy(TEST_LEARNING_EXPERIENCE)
  context.url = f"{API_URL}/learning-experience"
  for key in DEL_KEYS:
    if key in lx_dict:
      del lx_dict[key]
  context.res = post_method(url=context.url, request_body=lx_dict)
  context.res_data = context.res.json()
  context.le_id = context.res_data["data"]["uuid"]
  context.params = {"fetch_all": True}
  context.url = f"{API_URL}/learning-experience/{context.le_id}"

@behave.when("there is a request to view all versions of learning experience with correct id")
def step_impl_2(context):
  context.res = get_method(url = context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("all the versions of the requested learning experience will be retrieved")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.le_id

@behave.given("that an LXE or CD has access to the content authoring tool and needs to view a specific version of the learning experience")
def step_impl_1(context):
  lx_dict = copy(TEST_LEARNING_EXPERIENCE)
  context.url = f"{API_URL}/learning-experience"
  for key in DEL_KEYS:
    if key in lx_dict:
      del lx_dict[key]
  context.res = post_method(url=context.url, request_body=lx_dict)
  context.res_data = context.res.json()
  context.le_id = context.res_data["data"]["uuid"]
  context.params = {"version": 1}
  context.url = f"{API_URL}/learning-experience/{context.le_id}"

@behave.when("there is a request to view a particular version of the learning experience with correct id")
def step_impl_2(context):
  context.res = get_method(url = context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("the requested version of the learning experience will be retrieved")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.le_id

@behave.given("an LXE or CD has access to the content authoring tool and needs to view the learning experience")
def step_impl_1(context):
  context.le_id = "random_id"
  context.url = f"{API_URL}/learning-experience/{context.le_id}"

@behave.when("there is a request to view a particular learning experience with incorrect id")
def step_impl_2(context):
  context.res = get_method(url = context.url)
  context.res_data = context.res.json()

@behave.then("Learning Object Service will throw an error message for accessing invalid learning experience")
def step_impl_3(context):
  time.sleep(20)
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data["data"] is None


@behave.given("that an LXE or CD has access to the content authoring tool and needs to view the learning object")
def step_impl_1(context):
  lx_dict = copy(TEST_LEARNING_OBJECT)
  context.url = f"{API_URL}/learning-object"
  for key in DEL_KEYS:
    if key in lx_dict:
      del lx_dict[key]
  context.res = post_method(url=context.url, request_body=lx_dict)
  context.res_data = context.res.json()
  context.lo_id = context.res_data["data"]["uuid"]
  context.url = f"{API_URL}/learning-object/{context.lo_id}"

@behave.when("there is a request to view a particular learning object with correct id")
def step_impl_2(context):
  context.res = get_method(url = context.url)
  context.res_data = context.res.json()

@behave.then("the requested learning object will be retrieved")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.lo_id


@behave.given("that an LXE or CD has access to the content authoring tool and needs to view all versions of the learning object")
def step_impl_1(context):
  lx_dict = copy(TEST_LEARNING_OBJECT)
  context.url = f"{API_URL}/learning-object"
  for key in DEL_KEYS:
    if key in lx_dict:
      del lx_dict[key]
  context.res = post_method(url=context.url, request_body=lx_dict)
  context.res_data = context.res.json()
  context.lo_id = context.res_data["data"]["uuid"]
  context.url = f"{API_URL}/learning-object/{context.lo_id}"
  context.params = {"fetch_all": True}

@behave.when("there is a request to view all versions of the learning object with correct id")
def step_impl_2(context):
  context.res = get_method(url = context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("all the versions of the requested learning object will be retrieved")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.lo_id


@behave.given("that an LXE or CD has access to the content authoring tool and needs to view a specific version of the learning object")
def step_impl_1(context):
  lx_dict = copy(TEST_LEARNING_OBJECT)
  context.url = f"{API_URL}/learning-object"
  for key in DEL_KEYS:
    if key in lx_dict:
      del lx_dict[key]
  context.res = post_method(url=context.url, request_body=lx_dict)
  context.res_data = context.res.json()
  context.lo_id = context.res_data["data"]["uuid"]
  context.url = f"{API_URL}/learning-object/{context.lo_id}"
  context.params = {"version": 1}

@behave.when("there is a request to view a specific version of the learning object with correct id")
def step_impl_2(context):
  context.res = get_method(url = context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("the requested version of the learning object will be retrieved")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.lo_id


@behave.given("an LXE or CD has access to the content authoring tool and needs to view the learning object")
def step_impl_1(context):
  context.lo_id = "random_id"
  context.url = f"{API_URL}/learning-object/{context.lo_id}"

@behave.when("there is a request to view a particular learning object with incorrect id")
def step_impl_2(context):
  context.res = get_method(url = context.url)
  context.res_data = context.res.json()

@behave.then("Learning Object Service will throw an error message for accessing invalid learning object")
def step_impl_3(context):
  time.sleep(20)
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data["data"] is None

# -------------------------------------------------------------------------------------------------------------------------

@behave.given("that an LXE or CD has access to the content authoring tool and needs to view the learning resource with the correct id")
def step_9_1(context):
  lr_dict = copy(TEST_LEARNING_RESOURCE)
  context.url = f"{API_URL}/learning-resource"
  for key in DEL_KEYS:
    if key in lr_dict:
      del lr_dict[key]
  context.res = post_method(url=context.url, request_body=lr_dict)
  context.res_data = context.res.json()
  context.lr_id = context.res_data["data"]["uuid"]
  context.url = f"{API_URL}/learning-resource/{context.lr_id}"


@behave.when("there is a request to view a particular learning resource with correct id")
def step_9_2(context):
  context.res = get_method(url = context.url)
  context.res_data = context.res.json()


@behave.then("the requested learning resource will be retrieved")
def step_9_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.lr_id

# -------------------------------------------------------------------------------------------------------------------------

@behave.given("that an LXE or CD has access to the content authoring tool and needs to view the learning resource with the incorrect id")
def step_10_1(context):
  _id = uuid.uuid4()
  context.url = f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-resource/{_id}"


@behave.when("there is a request to view a particular learning resource with incorrect id")
def step_10_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Learning Object Service will throw an error message for accessing invalid learning resource")
def step_10_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data["data"] is None