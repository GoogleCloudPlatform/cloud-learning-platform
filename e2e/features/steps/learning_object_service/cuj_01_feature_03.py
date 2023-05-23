"""
Integration with 3rd Party Tool | Frost (Clone Functionality)
"""

import time
import behave
from copy import copy

import sys 
sys.path.append("../")
from e2e.setup import get_method, post_method
from e2e.test_config import API_URL_LEARNING_OBJECT_SERVICE, DEL_KEYS
from e2e.test_object_schemas import (TEST_LEARNING_OBJECT, TEST_LEARNING_EXPERIENCE, TEST_LEARNING_RESOURCE)
from common.models import LearningResource

API_URL = API_URL_LEARNING_OBJECT_SERVICE

@behave.given("that an LXE or CD has access to the content authoring tool and needs to copy a learning experience")
def step_impl_1(context):
  lx_dict = copy(TEST_LEARNING_EXPERIENCE)
  for key in DEL_KEYS:
    if key in lx_dict:
      del lx_dict[key]
  context.url = f"{API_URL}/learning-experience"
  context.res = post_method(url=context.url, request_body=lx_dict)
  context.res_data = context.res.json()
  context.le_id = context.res_data["data"]["uuid"]
  context.url = f"{API_URL}/learning-experience/copy/{context.le_id}"
  
@behave.when("there is a request to copy a particular learning experience with correct id")
def step_impl_2(context):
  context.res = post_method(url = context.url)
  context.res_data = context.res.json()

@behave.then("a copy of the requested learning experience will be returned")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True

  #fetch original learning experience
  retrieve_url = f"{API_URL}/learning-experience/{context.le_id}"
  response = get_method(url = retrieve_url)
  assert response.status_code == 200, "retrieval failed"
  response_data = response.json()

  #drop irrelevant fields
  del context.res_data["data"]["uuid"]
  del context.res_data["data"]["created_time"]
  del context.res_data["data"]["last_modified_time"]
  del context.res_data["data"]["root_version_uuid"]
  del response_data["data"]["uuid"]
  del response_data["data"]["created_time"]
  del response_data["data"]["last_modified_time"]
  del response_data["data"]["root_version_uuid"]
  assert context.res_data["data"] == response_data["data"]



@behave.given("an LXE or CD has access to the content authoring tool and needs to copy a learning experience")
def step_impl_1(context):
  context.le_id = "random_id"
  context.url = f"{API_URL}/learning-experience/copy/{context.le_id}"

@behave.when("there is a request to copy a particular learning experience with incorrect id")
def step_impl_2(context):
  context.res = post_method(url = context.url)
  context.res_data = context.res.json()

@behave.then("Learning Object Service will fail to copy the learning experience due to invalid learning experience id")
def step_impl_3(context):
  time.sleep(20)
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data["data"] is None



@behave.given("that an LXE or CD has access to the content authoring tool and needs to copy a learning object")
def step_impl_1(context):
  lx_dict = copy(TEST_LEARNING_OBJECT)
  for key in DEL_KEYS:
    if key in lx_dict:
      del lx_dict[key]
  context.url = f"{API_URL}/learning-object"
  context.res = post_method(url=context.url, request_body=lx_dict)
  context.res_data = context.res.json()
  context.lo_id = context.res_data["data"]["uuid"]
  context.url = f"{API_URL}/learning-object/copy/{context.lo_id}"

@behave.when("there is a request to copy a particular learning object with correct id")
def step_impl_2(context):
  context.res = post_method(url = context.url)
  context.res_data = context.res.json()
  
@behave.then("a copy of the requested learning object will be returned")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True

  #fetch original learning experience
  retrieve_url = f"{API_URL}/learning-object/{context.lo_id}"
  response = get_method(url = retrieve_url)
  assert response.status_code == 200, "retrieval failed"
  response_data = response.json()

  #drop irrelevant fields
  del context.res_data["data"]["uuid"]
  del context.res_data["data"]["created_time"]
  del context.res_data["data"]["last_modified_time"]
  del context.res_data["data"]["root_version_uuid"]
  del response_data["data"]["uuid"]
  del response_data["data"]["created_time"]
  del response_data["data"]["last_modified_time"]
  del response_data["data"]["root_version_uuid"]
  assert context.res_data["data"] == response_data["data"]



@behave.given("an LXE or CD has access to the content authoring tool and needs to copy a learning object")
def step_impl_1(context):
  context.lo_id = "random_id"
  context.url = f"{API_URL}/learning-object/copy/{context.lo_id}"

@behave.when("there is a request to copy a particular learning object with incorrect id")
def step_impl_2(context):
  context.res = post_method(url = context.url)
  context.res_data = context.res.json()

@behave.then("Learning Object Service will fail to copy the learning experience due to invalid learning object id")
def step_impl_3(context):
  time.sleep(20)
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data["data"] is None

@behave.given("that an LXE or CD has access to the content authoring tool and needs to copy a learning resource with correct uuid")
def step_impl_1_1(context):
  context.lr_dict = TEST_LEARNING_RESOURCE
  lr = LearningResource.from_dict(context.lr_dict)
  lr.uuid = ""
  lr.save()
  lr.uuid = lr.id
  lr.update()
  context.lr_dict["uuid"] = lr.id
  context.uuid = lr.id
  context.url = f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-resource/copy/{context.uuid}"

@behave.when("there is a request to copy a particular learning resource with correct uuid")
def step_imp_1_2(context):
  context.res = post_method(url = context.url)
  context.res_data = context.res.json()

@behave.then("a copy of the requested learning resource will be returned along with associated data")
def step_impl_1_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] != context.uuid, "Creating a learning resource with the same uuid"
  assert context.res_data["message"] == "Successfully copied the learning resource", "Failed in copying the learning resource"
  assert context.res_data["data"]["name"] == "name" , "Title mismatch"
  assert context.res_data["data"]["display_name"] == "display_name" , "Title mismatch"
  assert context.res_data["data"]["description"] == "description", "Description mismatch"


@behave.given("that an LXE or CD has access to the content authoring tool and needs to create a copy of a learning resource with an incorrect uuid")
def step_impl_1_1(context):
  context.lr_dict = TEST_LEARNING_RESOURCE
  lr = LearningResource.from_dict(context.lr_dict)
  lr.uuid = ""
  lr.save()
  lr.uuid = lr.id
  lr.update()
  context.lr_dict["uuid"] = lr.id
  context.uuid = "wrong"
  context.url = f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-resource/copy/{context.uuid}"

@behave.when("there is a request to copy a particular the learning resource with incorrect uuid")
def step_imp_1_2(context):
  context.res = post_method(url = context.url)
  context.res_data = context.res.json()

@behave.then("user fails to create the clone of the LR and gets an error message")
def step_impl_1_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  err_msg = f"Learning Resource with uuid {context.uuid} not found"
  assert context.res_data["message"] == err_msg, "Created the learning resource with the wrong uuid"
