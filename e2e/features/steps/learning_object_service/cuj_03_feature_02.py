"""
Integration with 3rd Party Tool | Archival
"""
import behave
import sys
from copy import copy

sys.path.append("../")
from e2e.setup import post_method, get_method, put_method
from e2e.test_config import API_URL_LEARNING_OBJECT_SERVICE, DEL_KEYS
from e2e.test_object_schemas import (TEST_LEARNING_OBJECT, TEST_LEARNING_EXPERIENCE,
                                TEST_LEARNING_RESOURCE)

API_URL = API_URL_LEARNING_OBJECT_SERVICE

#FILTER ARCHIVED LEARNING OBJECT POSITIVE----------------------------------------------------

@behave.given("that an LXE or CD has access to the content authoring tool to filter archived learning objects with correct parameters")
def step_impl_1(context):
  
  #Creating a learning experience uuid
  context.le_payload = TEST_LEARNING_EXPERIENCE
  for key in DEL_KEYS:
    if key in context.le_payload:
      del context.le_payload[key]
  context.le_url= f"{API_URL}/learning-experience"
  context.le_res = post_method(url=context.le_url, request_body=context.le_payload)
  le_data = context.le_res.json()
  LE_UUID = le_data["data"]["uuid"]

  #Creating a learning object
  LRO = copy(TEST_LEARNING_OBJECT)
  LRO["parent_nodes"]["learning_experiences"].append(LE_UUID)
  context.payload = LRO
  for key in DEL_KEYS:
    if key in context.payload:
      del context.payload[key]
  context.url= f"{API_URL}/learning-object"
  context.res = post_method(url=context.url, request_body=context.payload)
  create_data = context.res.json()
  context.req_id = create_data["data"]["uuid"]

  #archiving the created object using put method
  context.update_params = {"is_archived": True}
  context.update_url = f"{API_URL}/learning-object/{context.req_id}"
  context.update_res = put_method(url=context.update_url, query_params=context.update_params,
              request_body=LRO)

  context.url= f"{API_URL}/learning-objects"
  context.params = {"skip":0, "limit":30,"fetch_archive":True}

@behave.when("they filter for archived learning objects within that tool with correct parameters")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("LOS will serve up the most relevant archived learning objects based on the filter")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["message"] == "Data fetched successfully"
  fetched_los = context.res_data["data"]["records"]
  for lo in fetched_los:
    assert lo["is_archived"] is True

#FILTER UNARCHIVED LEARNING OBJECT POSITIVE----------------------------------------------------

@behave.given("that an LXE or CD has access to the content authoring tool to filter unarchived learning objects with correct parameters")
def step_impl_1(context):
  
  #Creating a learning experience uuid
  context.le_payload = TEST_LEARNING_EXPERIENCE
  context.le_url= f"{API_URL}/learning-experience"
  for key in DEL_KEYS:
    if key in context.le_payload:
      del context.le_payload[key]
  context.le_res = post_method(url=context.le_url, request_body=context.le_payload)
  le_data = context.le_res.json()
  LE_UUID = le_data["data"]["uuid"]

  #Creating an unarchived learning object
  LRO = copy(TEST_LEARNING_OBJECT)
  LRO["parent_nodes"]["learning_experiences"].append(LE_UUID)
  context.payload = LRO
  context.url= f"{API_URL}/learning-object"
  for key in DEL_KEYS:
    if key in context.payload:
      del context.payload[key]
  context.res = post_method(url=context.url, request_body=context.payload)
  create_data = context.res.json()
  context.req_id = create_data["data"]["uuid"]

  context.url= f"{API_URL}/learning-objects"
  context.params = {"skip":0, "limit":30, "fetch_archive":False}


@behave.when("they filter for unarchived learning objects within that tool with correct parameters")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("LOS will serve up only the unarchived learning objects based on the filter")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["message"] == "Data fetched successfully"
  fetched_los = context.res_data["data"]["records"]
  for lo in fetched_los:
    assert lo["is_archived"] is False

#FILTER ARCHIVED LEARNING EXPERIENCE POSITIVE----------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool to filter archived learning experiences with correct parameters")
def step_impl_1(context):

  LRE = copy(TEST_LEARNING_EXPERIENCE)
  context.payload = TEST_LEARNING_EXPERIENCE
  context.url= f"{API_URL}/learning-experience"
  for key in DEL_KEYS:
    if key in context.payload:
      del context.payload[key]
  context.res = post_method(url=context.url, request_body=context.payload)
  create_data = context.res.json()
  context.req_id = create_data["data"]["uuid"]

  #archiving the created learning experience using put method
  context.update_params = {"is_archived": True}
  context.update_url = f"{API_URL}/learning-experience/{context.req_id}"
  context.update_res = put_method(url=context.update_url, query_params=context.update_params,
              request_body=LRE)
  
  #Creating Learning object
  context.lo_payload = TEST_LEARNING_OBJECT
  context.lo_url= f"{API_URL}/learning-object"
  for key in DEL_KEYS:
    if key in context.lo_payload:
      del context.lo_payload[key]
  context.lo_res = post_method(url=context.lo_url, request_body=context.lo_payload)
  lo_data = context.lo_res.json()
  LO_UUID = lo_data["data"]["uuid"]
  
  context.url= f"{API_URL}/learning-experiences"
  context.params = {"skip":0, "limit":30, "fetch_archive": True}

@behave.when("they filter for archived learning experiences within that tool with correct parameters")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("LOS will serve up the most relevant archived learning experiences based on the filter")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["message"] == "Data fetched successfully"
  fetched_los = context.res_data["data"]["records"]
  for lo in fetched_los:
    assert lo["is_archived"] is True

#FILTER UNARCHIVED LEARNING EXPERIENCE POSITIVE----------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool to filter unarchived learning experiences with correct parameters")
def step_impl_1(context):

  #Creating unarchived Learning experience
  LRE = copy(TEST_LEARNING_EXPERIENCE)
  context.payload = TEST_LEARNING_EXPERIENCE
  for key in DEL_KEYS:
    if key in context.payload:
      del context.payload[key]
  context.url= f"{API_URL}/learning-experience"
  context.res = post_method(url=context.url, request_body=context.payload)
  create_data = context.res.json()
  context.req_id = create_data["data"]["uuid"]
  
  #Creating Learning object
  context.lo_payload = TEST_LEARNING_OBJECT
  context.lo_url= f"{API_URL}/learning-object"
  for key in DEL_KEYS:
    if key in context.lo_payload:
      del context.lo_payload[key]
  context.lo_res = post_method(url=context.lo_url, request_body=context.lo_payload)
  lo_data = context.lo_res.json()
  LO_UUID = lo_data["data"]["uuid"]
  
  context.url= f"{API_URL}/learning-experiences"
  context.params = {"skip":0, "limit":30,"fetch_archive": False}

@behave.when("they filter for unarchived learning experiences within that tool with correct parameters")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("LOS will serve up only the unarchived learning experiences based on the filter")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["message"] == "Data fetched successfully"
  fetched_los = context.res_data["data"]["records"]
  for lo in fetched_los:
    assert lo["is_archived"] is False

#FILTER ARCHIVED LEARNING RESOURCE POSITIVE----------------------------------------------------

@behave.given("that an LXE or CD has access to the content authoring tool to filter archived learning resources with correct filter parameters")
def step_impl_1(context):
  
  #Creating Learning object
  context.lo_payload = TEST_LEARNING_OBJECT
  context.lo_url= f"{API_URL}/learning-object"
  for key in DEL_KEYS:
    if key in context.lo_payload:
      del context.lo_payload[key]
  context.lo_res = post_method(url=context.lo_url, request_body=context.lo_payload)
  lo_data = context.lo_res.json()
  LO_UUID = lo_data["data"]["uuid"]

  #Creating a learning resource
  LR = copy(TEST_LEARNING_RESOURCE)
  LR["parent_nodes"]["learning_objects"].append(LO_UUID)
  context.payload = LR
  context.url= f"{API_URL}/learning-resource"
  for key in DEL_KEYS:
    if key in context.payload:
      del context.payload[key]
  context.res = post_method(url=context.url, request_body=context.payload)
  create_data = context.res.json()
  context.req_id = create_data["data"]["uuid"]

  #archiving the created object using put method
  context.update_params = {"is_archived": True}
  context.update_url = f"{API_URL}/learning-resource/{context.req_id}"
  context.update_res = put_method(url=context.update_url, query_params=context.update_params,
              request_body=LR)
  assert context.update_res.status_code == 200
  context.url= f"{API_URL}/learning-resources"
  context.params = {"skip":0, "limit":1, "fetch_archive":True}

@behave.when("they filter for archived learning resources within that tool with correct filter parameters")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("LOS will serve up only the most relevant archived learning resources based on the filter")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["message"] == "Data fetched successfully"
  fetched_los = context.res_data["data"]["records"]
  for lo in fetched_los:
    assert lo["is_archived"] is True

#FILTER UNARCHIVED LEARNING RESOURCE POSITIVE----------------------------------------------------

@behave.given("that an LXE or CD has access to the content authoring tool to filter unarchived learning resources with correct filter parameters")
def step_impl_1(context):
  
  #Creating Learning object
  context.lo_payload = TEST_LEARNING_OBJECT
  context.lo_url= f"{API_URL}/learning-object"
  for key in DEL_KEYS:
    if key in context.lo_payload:
      del context.lo_payload[key]
  context.lo_res = post_method(url=context.lo_url, request_body=context.lo_payload)
  lo_data = context.lo_res.json()
  LO_UUID = lo_data["data"]["uuid"]

  #Creating a learning resource
  LR = copy(TEST_LEARNING_RESOURCE)
  LR["parent_nodes"]["learning_objects"].append(LO_UUID)
  context.payload = LR
  context.url= f"{API_URL}/learning-resource"
  for key in DEL_KEYS:
    if key in context.payload:
      del context.payload[key]
  context.res = post_method(url=context.url, request_body=context.payload)
  create_data = context.res.json()
  context.req_id = create_data["data"]["uuid"]

  context.url= f"{API_URL}/learning-resources"
  context.params = {"skip":0, "limit":30, "fetch_archive":False}

@behave.when("they filter for unarchived learning resources within that tool with correct filter parameters")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("LOS will serve up only the most relevant unarchived learning resources based on the filter")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["message"] == "Data fetched successfully"
  fetched_los = context.res_data["data"]["records"]
  for lo in fetched_los:
    assert lo["is_archived"] is False
