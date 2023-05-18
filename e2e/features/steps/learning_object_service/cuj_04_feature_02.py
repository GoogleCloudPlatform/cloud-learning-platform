"""
Parent-Child relationship between learning object and learning resource
"""

import behave
import sys
import uuid
from copy import deepcopy

sys.path.append("../")
from setup import post_method, get_method, put_method
from test_object_schemas import (TEST_LEARNING_OBJECT, TEST_LEARNING_RESOURCE)
from test_config import API_URL_LEARNING_OBJECT_SERVICE, DEL_KEYS

API_URL = API_URL_LEARNING_OBJECT_SERVICE


@behave.given("that LXE or CD has access of the content authoring tool")
def step_1_1(context):
  context.learning_object_req_body = deepcopy(TEST_LEARNING_OBJECT)
  context.learning_object_url = f"{API_URL}/learning-object"

  context.learning_resource_req_body = deepcopy(TEST_LEARNING_RESOURCE)

  for key in DEL_KEYS:
    if key in context.learning_resource_req_body:
      del context.learning_resource_req_body[key]

  context.learning_resource_url = f"{API_URL}/learning-resource"


@behave.when(
    "they design the learning object and the learning resource using a third-party tool"
)
def step_1_2(context):
  context.learning_object_response = post_method(
      url=context.learning_object_url,
      request_body=context.learning_object_req_body)
  context.test_learning_object = context.learning_object_response.json()
  context.learning_object_uuid = context.test_learning_object['data']["uuid"]
  context.learning_resource_req_body["parent_nodes"]["learning_objects"].append(
      context.learning_object_uuid)

  context.learning_resource_response = post_method(
      url=context.learning_resource_url,
      request_body=context.learning_resource_req_body)
  context.test_learning_resource = context.learning_resource_response.json()

  context.learning_object_get_response = get_method(
      url=context.learning_object_url + "/" + context.learning_object_uuid)
  context.learning_object_get_resource = context.learning_object_get_response.json(
  )


@behave.then(
    "the learning object and the learning resource will be created in a third-party tool"
)
def step_1_3(context):
  assert context.learning_object_response.status_code == 200
  assert context.test_learning_object["success"] is True
  assert "uuid" in context.test_learning_object["data"]
  assert "created_time" in context.test_learning_object["data"]
  assert "last_modified_time" in context.test_learning_object["data"]

  assert context.learning_resource_response.status_code == 200
  assert context.test_learning_resource["success"] is True
  assert "uuid" in context.test_learning_resource["data"]
  assert "created_time" in context.test_learning_resource["data"]
  assert "last_modified_time" in context.test_learning_resource["data"]


@behave.then("the learning resource gets associated with the learning object")
def step_1_4(context):
  assert context.learning_object_uuid in context.test_learning_resource["data"][
      "parent_nodes"]["learning_objects"]

  assert context.test_learning_resource["data"][
      "uuid"] in context.learning_object_get_resource["data"]["child_nodes"][
          "learning_resources"]


@behave.given(
    "that an LXE or CD wants to create a learning resource providing the reference of the given learning object"
)
def step_2_1(context):
  context.learning_object_req_body = deepcopy(TEST_LEARNING_OBJECT)
  context.learning_object_url = f"{API_URL}/learning-object"

  context.learning_resource_req_body = deepcopy(TEST_LEARNING_RESOURCE)

  for key in DEL_KEYS:
    if key in context.learning_resource_req_body:
      del context.learning_resource_req_body[key]

  context.learning_resource_url = f"{API_URL}/learning-resource"


@behave.when("they design the learning resource using a third-party tool")
def step_2_2(context):
  context.learning_object_response = post_method(
      url=context.learning_object_url,
      request_body=context.learning_object_req_body)
  context.test_learning_object = context.learning_object_response.json()
  context.learning_object_uuid = context.test_learning_object["data"]["uuid"]

  context.uuid = str(uuid.uuid4())
  context.learning_resource_req_body["parent_nodes"]["learning_objects"].append(
      context.uuid)
  context.learning_resource_response = post_method(
      url=context.learning_resource_url,
      request_body=context.learning_resource_req_body)
  context.test_learning_resource = context.learning_resource_response.json()


@behave.then(
    "the user will get an error message of not found the reference to the learning object"
)
def step_2_3(context):
  assert context.learning_object_response.status_code == 200
  assert context.test_learning_object["success"] is True
  assert "uuid" in context.test_learning_object["data"]
  assert "created_time" in context.test_learning_object["data"]
  assert "last_modified_time" in context.test_learning_object["data"]

  assert context.learning_resource_response.status_code == 404
  assert context.test_learning_resource[
      "message"] == f"Learning Object with uuid {context.uuid} not found"


@behave.given(
    "that an LXE or CD wants to add the reference of learning object in the learning resource"
)
def step_3_1(context):
  context.learning_object_req_body = deepcopy(TEST_LEARNING_OBJECT)
  context.learning_object_url = f"{API_URL}/learning-object"

  context.learning_resource_req_body = deepcopy(TEST_LEARNING_RESOURCE)
  for key in DEL_KEYS:
    if key in context.learning_resource_req_body:
      del context.learning_resource_req_body[key]
  context.learning_resource_url = f"{API_URL}/learning-resource"


@behave.when(
    "they design the multiple learning object and the single learning resource using a third-party tool"
)
def step_3_2(context):
  context.learning_object_response_1 = post_method(
      url=context.learning_object_url,
      request_body=context.learning_object_req_body)
  context.test_learning_object_1 = context.learning_object_response_1.json()
  context.learning_object_uuid_1 = context.test_learning_object_1["data"][
      "uuid"]

  context.learning_object_response_2 = post_method(
      url=context.learning_object_url,
      request_body=context.learning_object_req_body)
  context.test_learning_object_2 = context.learning_object_response_2.json()
  context.learning_object_uuid_2 = context.test_learning_object_2['data'][
      "uuid"]

  learning_object_uuid = [
      context.learning_object_uuid_1, context.learning_object_uuid_2
  ]
  context.learning_resource_req_body["parent_nodes"]["learning_objects"].extend(
      learning_object_uuid)
  context.learning_resource_response = post_method(
      url=context.learning_resource_url,
      request_body=context.learning_resource_req_body)
  context.test_learning_resource = context.learning_resource_response.json()

  context.learning_object_get_response_1 = get_method(
      url=context.learning_object_url + "/" + context.learning_object_uuid_1)
  context.learning_object_get_resource_1 = context.learning_object_get_response_1.json(
  )

  context.learning_object_get_response_2 = get_method(
      url=context.learning_object_url + "/" + context.learning_object_uuid_2)
  context.learning_object_get_resource_2 = context.learning_object_get_response_2.json(
  )


@behave.then(
    "the multiple learning object and the learning resource will be created in a third-party tool"
)
def step_3_3(context):
  assert context.learning_object_response_1.status_code == 200
  assert context.test_learning_object_1["success"] is True
  assert "uuid" in context.test_learning_object_1["data"]
  assert "created_time" in context.test_learning_object_1["data"]
  assert "last_modified_time" in context.test_learning_object_1["data"]

  assert context.learning_object_response_2.status_code == 200
  assert context.test_learning_object_2["success"] is True
  assert "uuid" in context.test_learning_object_2["data"]
  assert "created_time" in context.test_learning_object_2["data"]
  assert "last_modified_time" in context.test_learning_object_2["data"]

  assert context.learning_resource_response.status_code == 200
  assert context.test_learning_resource["success"] is True
  assert "uuid" in context.test_learning_resource["data"]
  assert "created_time" in context.test_learning_resource["data"]
  assert "last_modified_time" in context.test_learning_resource["data"]


@behave.then(
    "the learning resource gets associated with the multiple learning object")
def step_3_4(context):
  assert context.learning_object_uuid_1 in context.test_learning_resource[
      "data"]["parent_nodes"]["learning_objects"]
  assert context.learning_object_uuid_2 in context.test_learning_resource[
      "data"]["parent_nodes"]["learning_objects"]

  assert context.test_learning_resource["data"][
      "uuid"] in context.learning_object_get_resource_1["data"]["child_nodes"][
          "learning_resources"]
  assert context.test_learning_resource["data"][
      "uuid"] in context.learning_object_get_resource_2["data"]["child_nodes"][
          "learning_resources"]


@behave.given(
    "that an LXE or CD wants to add the reference of a single learning object in the multiple learning resource"
)
def step_4_1(context):
  context.learning_object_req_body = deepcopy(TEST_LEARNING_OBJECT)
  context.learning_object_url = f"{API_URL}/learning-object"

  context.learning_resource_req_body = deepcopy(TEST_LEARNING_RESOURCE)

  for key in DEL_KEYS:
    if key in context.learning_resource_req_body:
      del context.learning_resource_req_body[key]

  context.learning_resource_url = f"{API_URL}/learning-resource"


@behave.when(
    "they design the multiple learning resource using a third-party tool")
def step_4_2(context):
  context.learning_object_response = post_method(
      url=context.learning_object_url,
      request_body=context.learning_object_req_body)
  context.test_learning_object = context.learning_object_response.json()
  context.learning_object_uuid = context.test_learning_object["data"]["uuid"]

  context.learning_resource_req_body["parent_nodes"]["learning_objects"] = [
      context.learning_object_uuid
  ]

  context.learning_resource_response_1 = post_method(
      url=context.learning_resource_url,
      request_body=context.learning_resource_req_body)
  context.test_learning_resource_1 = context.learning_resource_response_1.json()

  context.learning_resource_response_2 = post_method(
      url=context.learning_resource_url,
      request_body=context.learning_resource_req_body)
  context.test_learning_resource_2 = context.learning_resource_response_2.json()

  context.learning_object_get_response = get_method(
      url=context.learning_object_url + "/" + context.learning_object_uuid)
  context.learning_object_get_resource = context.learning_object_get_response.json(
  )


@behave.then("the learning object will be created in a third-party tool")
def step_4_3(context):
  assert context.learning_object_response.status_code == 200
  assert context.test_learning_object["success"] is True
  assert "uuid" in context.test_learning_object["data"]
  assert "created_time" in context.test_learning_object["data"]
  assert "last_modified_time" in context.test_learning_object["data"]

  assert context.learning_resource_response_1.status_code == 200
  assert context.test_learning_resource_1["success"] is True
  assert "uuid" in context.test_learning_resource_1["data"]
  assert "created_time" in context.test_learning_resource_1["data"]
  assert "last_modified_time" in context.test_learning_resource_1["data"]

  assert context.learning_resource_response_2.status_code == 200
  assert context.test_learning_resource_2["success"] is True
  assert "uuid" in context.test_learning_resource_2["data"]
  assert "created_time" in context.test_learning_resource_2["data"]
  assert "last_modified_time" in context.test_learning_resource_2["data"]


@behave.then(
    "all the learning resource gets associated with the given learning object")
def step_4_4(context):
  assert context.learning_object_uuid in context.test_learning_resource_1[
      "data"]["parent_nodes"]["learning_objects"]
  assert context.learning_object_uuid in context.test_learning_resource_2[
      "data"]["parent_nodes"]["learning_objects"]

  assert context.test_learning_resource_1["data"][
      "uuid"] in context.learning_object_get_resource["data"]["child_nodes"][
          "learning_resources"]
  assert context.test_learning_resource_2["data"][
      "uuid"] in context.learning_object_get_resource["data"]["child_nodes"][
          "learning_resources"]


@behave.given(
    "that an LXE or CD wants to replace an old reference of the learning object with a new reference in the learning resource"
)
def step_5_1(context):
  context.learning_object_req_body = deepcopy(TEST_LEARNING_OBJECT)
  context.learning_object_url = f"{API_URL}/learning-object"

  context.learning_resource_req_body = deepcopy(TEST_LEARNING_RESOURCE)
  for key in DEL_KEYS:
    if key in context.learning_resource_req_body:
      del context.learning_resource_req_body[key]
  context.learning_resource_url = f"{API_URL}/learning-resource"


@behave.when("they update the new learning object using a third-party tool")
def step_5_2(context):
  context.learning_object_response_old = post_method(
      url=context.learning_object_url,
      request_body=context.learning_object_req_body)
  context.test_learning_object_old = context.learning_object_response_old.json()
  context.learning_object_uuid_old = context.test_learning_object_old["data"][
      "uuid"]

  context.learning_resource_req_body["parent_nodes"]["learning_objects"] = [
      context.learning_object_uuid_old
  ]
  context.learning_resource_response_old = post_method(
      url=context.learning_resource_url,
      request_body=context.learning_resource_req_body)
  context.test_learning_resource_old = context.learning_resource_response_old.json(
  )

  context.learning_object_response_new = post_method(
      url=context.learning_object_url,
      request_body=context.learning_object_req_body)
  context.test_learning_object_new = context.learning_object_response_new.json()
  context.learning_object_uuid_new = context.test_learning_object_new['data'][
      "uuid"]

  context.learning_resource_req_body["parent_nodes"]["learning_objects"] = [
      context.learning_object_uuid_new
  ]
  context.learning_resource_req_body["is_archived"] = False

  context.learning_resource_response_updated = put_method(
      url=context.learning_resource_url + "/" +
      context.test_learning_resource_old["data"]["uuid"],
      request_body=context.learning_resource_req_body)
  context.test_learning_resource_updated = context.learning_resource_response_updated.json(
  )

  context.learning_object_get_response_old = get_method(
      url=context.learning_object_url + "/" + context.learning_object_uuid_old)
  context.learning_object_get_resource_old = context.learning_object_get_response_old.json(
  )

  context.learning_object_get_response_new = get_method(
      url=context.learning_object_url + "/" + context.learning_object_uuid_new)
  context.learning_object_get_resource_new = context.learning_object_get_response_new.json(
  )


@behave.then(
    "the learning resource gets associated with the new learning object")
def step_5_3(context):
  assert context.learning_object_response_new.status_code == 200
  assert context.test_learning_object_new["success"] is True

  assert context.learning_object_uuid_new in context.test_learning_resource_updated[
      "data"]["parent_nodes"]["learning_objects"]
  assert context.learning_object_uuid_old not in context.test_learning_resource_updated[
      "data"]["parent_nodes"]["learning_objects"]

  assert context.test_learning_resource_updated["data"][
      "uuid"] not in context.learning_object_get_resource_old["data"][
          "child_nodes"]["learning_resources"]
  assert context.test_learning_resource_updated["data"][
      "uuid"] in context.learning_object_get_resource_new["data"][
          "child_nodes"]["learning_resources"]


@behave.given(
    "that an LXE or CD wants to add a reference to one more learning object in the learning resource"
)
def step_6_1(context):
  context.learning_object_req_body = deepcopy(TEST_LEARNING_OBJECT)
  context.learning_object_url = f"{API_URL}/learning-object"

  context.learning_resource_req_body = deepcopy(TEST_LEARNING_RESOURCE)
  for key in DEL_KEYS:
    if key in context.learning_resource_req_body:
      del context.learning_resource_req_body[key]
  context.learning_resource_url = f"{API_URL}/learning-resource"


@behave.when("they update the learning resource using a third-party tool")
def step_6_2(context):
  context.learning_object_response = post_method(
      url=context.learning_object_url,
      request_body=context.learning_object_req_body)
  context.test_learning_object = context.learning_object_response.json()
  context.learning_object_uuid = context.test_learning_object["data"]["uuid"]

  context.learning_resource_response = post_method(
      url=context.learning_resource_url,
      request_body=context.learning_resource_req_body)
  context.test_learning_resource = context.learning_resource_response.json()

  context.uuid = str(uuid.uuid4())
  context.learning_resource_req_body["parent_nodes"]["learning_objects"] = [
      context.uuid
  ]
  context.learning_resource_req_body["is_archived"] = False

  context.learning_resource_response_updated = put_method(
      url=context.learning_resource_url + "/" +
      context.test_learning_resource["data"]["uuid"],
      request_body=context.learning_resource_req_body)
  context.test_learning_resource_updated = context.learning_resource_response_updated.json(
  )


@behave.then(
    "the user gets an error message of not found the reference to the learning object"
)
def step_6_3(context):
  assert context.learning_object_response.status_code == 200
  assert context.test_learning_object["success"] is True

  assert context.learning_resource_response_updated.status_code == 404
  assert context.test_learning_resource_updated[
      "message"] == f"Learning Object with uuid {context.uuid} not found"


@behave.given(
    "that an LXE or CD wants to update the reference of the learning resource in the learning object"
)
def step_7_1(context):
  context.learning_object_req_body = deepcopy(TEST_LEARNING_OBJECT)
  context.learning_object_url = f"{API_URL}/learning-object"

  context.learning_resource_req_body = deepcopy(TEST_LEARNING_RESOURCE)
  for key in DEL_KEYS:
    if key in context.learning_resource_req_body:
      del context.learning_resource_req_body[key]
  context.learning_resource_url = f"{API_URL}/learning-resource"


@behave.when(
    "they add the new reference and delete the old reference of the learning resource using a third-party tool"
)
def step_7_2(context):
  context.learning_object_response = post_method(
      url=context.learning_object_url,
      request_body=context.learning_object_req_body)
  context.test_learning_object = context.learning_object_response.json()
  context.learning_object_uuid = context.test_learning_object["data"]["uuid"]

  context.learning_resource_req_body["parent_nodes"]["learning_objects"] = [
      context.learning_object_uuid
  ]

  context.learning_resource_response_1 = post_method(
      url=context.learning_resource_url,
      request_body=context.learning_resource_req_body)
  context.test_learning_resource_1 = context.learning_resource_response_1.json()

  context.learning_resource_response_2 = post_method(
      url=context.learning_resource_url,
      request_body=context.learning_resource_req_body)
  context.test_learning_resource_2 = context.learning_resource_response_2.json()

  context.learning_resource_req_body["parent_nodes"]["learning_objects"] = []
  context.learning_resource_req_body["is_archived"] = False
  context.learning_resource_response_updated_1 = put_method(
      url=context.learning_resource_url + "/" +
      context.test_learning_resource_2["data"]["uuid"],
      request_body=context.learning_resource_req_body)
  context.test_learning_resource_updated_1 = context.learning_resource_response_updated_1.json(
  )

  context.learning_resource_req_body["parent_nodes"]["learning_objects"] = [
      context.learning_object_uuid
  ]

  context.learning_resource_response_3 = post_method(
      url=context.learning_resource_url,
      request_body=context.learning_resource_req_body)
  context.test_learning_resource_3 = context.learning_resource_response_1.json()

  context.learning_object_get_response = get_method(
      url=context.learning_object_url + "/" + context.learning_object_uuid)
  context.learning_object_get_resource = context.learning_object_get_response.json(
  )


@behave.then(
    "the old learning resource will get untagged and the new learning resource will get tagged to the learning object"
)
def step_7_3(context):
  assert context.test_learning_resource_1["data"][
      "uuid"] in context.learning_object_get_resource["data"]["child_nodes"][
          "learning_resources"]
  assert context.test_learning_resource_2["data"][
      "uuid"] not in context.learning_object_get_resource["data"][
          "child_nodes"]["learning_resources"]
  assert context.test_learning_resource_3["data"][
      "uuid"] in context.learning_object_get_resource["data"]["child_nodes"][
          "learning_resources"]
