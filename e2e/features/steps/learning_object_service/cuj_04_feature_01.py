"""
Parent-Child relationship between learning experience and learning object
"""
import behave
import sys
import uuid
from copy import deepcopy

sys.path.append("../")
from e2e.setup import post_method, get_method, put_method
from e2e.test_config import API_URL_LEARNING_OBJECT_SERVICE, DEL_KEYS
from e2e.test_object_schemas import (TEST_LEARNING_OBJECT, TEST_LEARNING_EXPERIENCE)

API_URL = API_URL_LEARNING_OBJECT_SERVICE


@behave.given("that LXE or CD has access to the content authoring tool to copy learning experience")
def step_1_1(context):
  context.learning_experience_req_body = deepcopy(TEST_LEARNING_EXPERIENCE)
  context.learning_object_req_body = deepcopy(TEST_LEARNING_OBJECT)
  for key in DEL_KEYS:
    if key in context.learning_experience_req_body:
      del context.learning_experience_req_body[key]
    if key in context.learning_object_req_body:
      del context.learning_object_req_body[key]

  context.learning_experience_url = f"{API_URL}/learning-experience"
  context.learning_object_url = f"{API_URL}/learning-object"


@behave.when(
    "they design the learning experience and the learning object using a third-party tool"
)
def step_1_2(context):
  context.learning_experience_response = post_method(
      url=context.learning_experience_url,
      request_body=context.learning_experience_req_body)
  context.test_learning_experience = context.learning_experience_response.json()
  context.learning_experience_uuid = context.test_learning_experience['data'][
      "uuid"]

  context.learning_object_req_body["parent_nodes"][
      "learning_experiences"].append(context.learning_experience_uuid)
  context.learning_object_response = post_method(
      url=context.learning_object_url,
      request_body=context.learning_object_req_body)
  context.test_learning_object = context.learning_object_response.json()

  context.learning_experience_get_response = get_method(
      url=context.learning_experience_url + "/" +
      context.learning_experience_uuid)
  context.learning_experience_get_object = context.learning_experience_get_response.json(
  )


@behave.then(
    "the learning experience and the learning object will be created in a third-party tool"
)
def step_1_3(context):
  assert context.learning_experience_response.status_code == 200
  assert context.test_learning_experience["success"] is True
  assert "uuid" in context.test_learning_experience["data"]
  assert "created_time" in context.test_learning_experience["data"]
  assert "last_modified_time" in context.test_learning_experience["data"]

  assert context.learning_object_response.status_code == 200
  assert context.test_learning_object["success"] is True
  assert "uuid" in context.test_learning_object["data"]
  assert "created_time" in context.test_learning_object["data"]
  assert "last_modified_time" in context.test_learning_object["data"]


@behave.then("the learning object gets associated with the learning experience")
def step_1_4(context):
  assert context.learning_experience_uuid in context.test_learning_object[
      "data"]["parent_nodes"]["learning_experiences"]

  assert context.test_learning_object["data"][
      "uuid"] in context.learning_experience_get_object["data"][
          "child_nodes"]["learning_objects"]


@behave.given(
    "that an LXE or CD wants to create a learning object providing the reference of the given learning experience"
)
def step_2_1(context):
  context.learning_experience_req_body = deepcopy(TEST_LEARNING_EXPERIENCE)
  context.learning_object_req_body = deepcopy(TEST_LEARNING_OBJECT)
  for key in DEL_KEYS:
    if key in context.learning_experience_req_body:
      del context.learning_experience_req_body[key]
    if key in context.learning_object_req_body:
      del context.learning_object_req_body[key]

  context.learning_experience_url = f"{API_URL}/learning-experience"
  context.learning_object_url = f"{API_URL}/learning-object"


@behave.when("they design the learning object using a third-party tool")
def step_2_2(context):
  context.learning_experience_response = post_method(
      url=context.learning_experience_url,
      request_body=context.learning_experience_req_body)
  context.test_learning_experience = context.learning_experience_response.json()
  context.learning_experience_uuid = context.test_learning_experience['data'][
      "uuid"]

  context.uuid = str(uuid.uuid4())
  context.learning_object_req_body["parent_nodes"][
      "learning_experiences"].append(context.uuid)
  context.learning_object_response = post_method(
      url=context.learning_object_url,
      request_body=context.learning_object_req_body)
  context.test_learning_object = context.learning_object_response.json()


@behave.then(
    "the user will get an error message of not found the reference to the learning experience"
)
def step_2_3(context):
  assert context.learning_experience_response.status_code == 200
  assert context.test_learning_experience["success"] is True
  assert "uuid" in context.test_learning_experience["data"]
  assert "created_time" in context.test_learning_experience["data"]
  assert "last_modified_time" in context.test_learning_experience["data"]

  assert context.learning_object_response.status_code == 404
  assert context.test_learning_object[
      "message"] == f"Learning Experience with uuid {context.uuid} not found"


@behave.given(
    "that an LXE or CD wants to add the reference of learning experience in the learning object"
)
def step_3_1(context):
  context.learning_experience_req_body = deepcopy(TEST_LEARNING_EXPERIENCE)
  context.learning_object_req_body = deepcopy(TEST_LEARNING_OBJECT)
  for key in DEL_KEYS:
    if key in context.learning_experience_req_body:
      del context.learning_experience_req_body[key]
    if key in context.learning_object_req_body:
      del context.learning_object_req_body[key]

  context.learning_experience_url = f"{API_URL}/learning-experience"
  context.learning_object_url = f"{API_URL}/learning-object"


@behave.when(
    "they design the multiple learning experiences and the single learning object using a third-party tool"
)
def step_3_2(context):
  context.learning_experience_response_1 = post_method(
      url=context.learning_experience_url,
      request_body=context.learning_experience_req_body)
  context.test_learning_experience_1 = context.learning_experience_response_1.json(
  )
  context.learning_experience_uuid_1 = context.test_learning_experience_1[
      'data']["uuid"]

  context.learning_experience_response_2 = post_method(
      url=context.learning_experience_url,
      request_body=context.learning_experience_req_body)
  context.test_learning_experience_2 = context.learning_experience_response_2.json(
  )
  context.learning_experience_uuid_2 = context.test_learning_experience_2[
      'data']["uuid"]

  learning_experience_uuid = [
      context.learning_experience_uuid_1, context.learning_experience_uuid_2
  ]
  context.learning_object_req_body["parent_nodes"][
      "learning_experiences"].extend(learning_experience_uuid)
  context.learning_object_response = post_method(
      url=context.learning_object_url,
      request_body=context.learning_object_req_body)
  context.test_learning_object = context.learning_object_response.json()

  context.learning_experience_get_response_1 = get_method(
      url=context.learning_experience_url + "/" +
      context.learning_experience_uuid_1)
  context.learning_experience_get_object_1 = context.learning_experience_get_response_1.json(
  )
  context.learning_experience_get_response_2 = get_method(
      url=context.learning_experience_url + "/" +
      context.learning_experience_uuid_2)
  context.learning_experience_get_object_2 = context.learning_experience_get_response_2.json(
  )


@behave.then(
    "the multiple learning experiences and the learning object will be created in a third-party tool"
)
def step_3_3(context):
  assert context.learning_experience_response_1.status_code == 200
  assert context.test_learning_experience_1["success"] is True
  assert "uuid" in context.test_learning_experience_1["data"]
  assert "created_time" in context.test_learning_experience_1["data"]
  assert "last_modified_time" in context.test_learning_experience_1["data"]

  assert context.learning_experience_response_2.status_code == 200
  assert context.test_learning_experience_2["success"] is True
  assert "uuid" in context.test_learning_experience_2["data"]
  assert "created_time" in context.test_learning_experience_2["data"]
  assert "last_modified_time" in context.test_learning_experience_2["data"]

  assert context.learning_object_response.status_code == 200
  assert context.test_learning_object["success"] is True
  assert "uuid" in context.test_learning_object["data"]
  assert "created_time" in context.test_learning_object["data"]
  assert "last_modified_time" in context.test_learning_object["data"]


@behave.then(
    "the learning object gets associated with the multiple learning experiences"
)
def step_3_4(context):
  assert context.learning_experience_uuid_1 in context.test_learning_object[
      "data"]["parent_nodes"]["learning_experiences"]
  assert context.learning_experience_uuid_2 in context.test_learning_object[
      "data"]["parent_nodes"]["learning_experiences"]

  assert context.test_learning_object["data"][
      "uuid"] in context.learning_experience_get_object_1["data"][
          "child_nodes"]["learning_objects"]
  assert context.test_learning_object["data"][
      "uuid"] in context.learning_experience_get_object_2["data"][
          "child_nodes"]["learning_objects"]


@behave.given(
    "that an LXE or CD wants to add the reference of a single learning experience in the multiple learning objects"
)
def step_4_1(context):
  context.learning_experience_req_body = deepcopy(TEST_LEARNING_EXPERIENCE)
  context.learning_object_req_body = deepcopy(TEST_LEARNING_OBJECT)
  for key in DEL_KEYS:
    if key in context.learning_experience_req_body:
      del context.learning_experience_req_body[key]
    if key in context.learning_object_req_body:
      del context.learning_object_req_body[key]

  context.learning_experience_url = f"{API_URL}/learning-experience"
  context.learning_object_url = f"{API_URL}/learning-object"


@behave.when(
    "they design the multiple learning objects using a third-party tool")
def step_4_2(context):
  context.learning_experience_response = post_method(
      url=context.learning_experience_url,
      request_body=context.learning_experience_req_body)
  context.test_learning_experience = context.learning_experience_response.json()
  context.learning_experience_uuid = context.test_learning_experience['data'][
      "uuid"]

  context.learning_object_req_body["parent_nodes"]["learning_experiences"] = [
      context.learning_experience_uuid
  ]

  context.learning_object_response_1 = post_method(
      url=context.learning_object_url,
      request_body=context.learning_object_req_body)
  context.test_learning_object_1 = context.learning_object_response_1.json()

  context.learning_object_response_2 = post_method(
      url=context.learning_object_url,
      request_body=context.learning_object_req_body)
  context.test_learning_object_2 = context.learning_object_response_2.json()

  context.learning_experience_get_response = get_method(
      url=context.learning_experience_url + "/" +
      context.learning_experience_uuid)
  context.learning_experience_get_object = context.learning_experience_get_response.json(
  )


@behave.then("the learning objects will be created in a third-party tool")
def step_4_3(context):
  assert context.learning_experience_response.status_code == 200
  assert context.test_learning_experience["success"] is True
  assert "uuid" in context.test_learning_experience["data"]
  assert "created_time" in context.test_learning_experience["data"]
  assert "last_modified_time" in context.test_learning_experience["data"]

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


@behave.then(
    "all the learning objects gets associated with the given learning experiences"
)
def step_4_4(context):
  assert context.learning_experience_uuid in context.test_learning_object_1[
      "data"]["parent_nodes"]["learning_experiences"]
  assert context.learning_experience_uuid in context.test_learning_object_2[
      "data"]["parent_nodes"]["learning_experiences"]

  assert context.test_learning_object_1["data"][
      "uuid"] in context.learning_experience_get_object["data"][
          "child_nodes"]["learning_objects"]
  assert context.test_learning_object_2["data"][
      "uuid"] in context.learning_experience_get_object["data"][
          "child_nodes"]["learning_objects"]


@behave.given(
    "that an LXE or CD wants to replace an old reference of the learning experience with a new reference in the learning object"
)
def step_5_1(context):
  context.learning_experience_req_body = deepcopy(TEST_LEARNING_EXPERIENCE)
  context.learning_object_req_body = deepcopy(TEST_LEARNING_OBJECT)
  for key in DEL_KEYS:
    if key in context.learning_experience_req_body:
      del context.learning_experience_req_body[key]
    if key in context.learning_object_req_body:
      del context.learning_object_req_body[key]

  context.learning_experience_url = f"{API_URL}/learning-experience"
  context.learning_object_url = f"{API_URL}/learning-object"


@behave.when("they update the new learning experience using a third-party tool")
def step_5_2(context):
  context.learning_experience_response_old = post_method(
      url=context.learning_experience_url,
      request_body=context.learning_experience_req_body)
  context.test_learning_experience_old = context.learning_experience_response_old.json(
  )
  context.learning_experience_uuid_old = context.test_learning_experience_old[
      'data']["uuid"]

  context.learning_object_req_body["parent_nodes"]["learning_experiences"] = [
      context.learning_experience_uuid_old
  ]
  context.learning_object_response_old = post_method(
      url=context.learning_object_url,
      request_body=context.learning_object_req_body)
  context.test_learning_object_old = context.learning_object_response_old.json()
  context.learning_experience_response_new = post_method(
      url=context.learning_experience_url,
      request_body=context.learning_experience_req_body)
  context.test_learning_experience_new = context.learning_experience_response_new.json(
  )
  context.learning_experience_uuid_new = context.test_learning_experience_new[
      'data']["uuid"]

  context.learning_object_req_body["parent_nodes"]["learning_experiences"] = [
      context.learning_experience_uuid_new
  ]
  context.learning_object_req_body["is_archived"] = False

  context.learning_object_response_updated = put_method(
      url=context.learning_object_url + "/" +
      context.test_learning_object_old["data"]["uuid"],
      request_body=context.learning_object_req_body)
  context.test_learning_object_updated = context.learning_object_response_updated.json(
  )

  context.learning_experience_get_response_old = get_method(
      url=context.learning_experience_url + "/" +
      context.learning_experience_uuid_old)
  context.learning_experience_get_object_old = context.learning_experience_get_response_old.json(
  )

  context.learning_experience_get_response_new = get_method(
      url=context.learning_experience_url + "/" +
      context.learning_experience_uuid_new)
  context.learning_experience_get_object_new = context.learning_experience_get_response_new.json(
  )


@behave.then(
    "the learning object gets associated with the new learning experience")
def step_5_3(context):
  assert context.learning_experience_response_new.status_code == 200
  assert context.test_learning_experience_new["success"] is True

  assert context.learning_experience_uuid_new in context.test_learning_object_updated[
      "data"]["parent_nodes"]["learning_experiences"]
  assert context.learning_experience_uuid_old not in context.test_learning_object_updated[
      "data"]["parent_nodes"]["learning_experiences"]

  assert context.test_learning_object_updated["data"][
      "uuid"] not in context.learning_experience_get_object_old["data"][
          "child_nodes"]["learning_objects"]
  assert context.test_learning_object_updated["data"][
      "uuid"] in context.learning_experience_get_object_new["data"][
          "child_nodes"]["learning_objects"]


@behave.given(
    "that an LXE or CD wants to add a reference to one more learning experience in the learning object"
)
def step_6_1(context):
  context.learning_experience_req_body = deepcopy(TEST_LEARNING_EXPERIENCE)
  context.learning_object_req_body = deepcopy(TEST_LEARNING_OBJECT)
  for key in DEL_KEYS:
    if key in context.learning_experience_req_body:
      del context.learning_experience_req_body[key]
    if key in context.learning_object_req_body:
      del context.learning_object_req_body[key]

  context.learning_experience_url = f"{API_URL}/learning-experience"
  context.learning_object_url = f"{API_URL}/learning-object"


@behave.when("they update the learning object using a third-party tool")
def step_6_2(context):
  context.learning_experience_response = post_method(
      url=context.learning_experience_url,
      request_body=context.learning_experience_req_body)
  context.test_learning_experience = context.learning_experience_response.json()
  context.learning_experience_uuid = context.test_learning_experience['data'][
      "uuid"]

  context.learning_object_response = post_method(
      url=context.learning_object_url,
      request_body=context.learning_object_req_body)
  context.test_learning_object = context.learning_object_response.json()

  context.uuid = str(uuid.uuid4())
  context.learning_object_req_body["parent_nodes"]["learning_experiences"] = [
      context.uuid
  ]
  context.learning_object_req_body["is_archived"] = False

  context.learning_object_response_updated = put_method(
      url=context.learning_object_url + "/" +
      context.test_learning_object["data"]["uuid"],
      request_body=context.learning_object_req_body)
  context.test_learning_object_updated = context.learning_object_response_updated.json(
  )


@behave.then(
    "the user gets an error message of not found the reference to the learning experience"
)
def step_6_3(context):
  assert context.learning_experience_response.status_code == 200
  assert context.test_learning_experience["success"] is True

  assert context.learning_object_response_updated.status_code == 404
  assert context.test_learning_object_updated[
      "message"] == f"Learning Experience with uuid {context.uuid} not found"


@behave.given(
    "that an LXE or CD wants to update the reference of the learning object in the learning experience"
)
def step_7_1(context):
  context.learning_experience_req_body = deepcopy(TEST_LEARNING_EXPERIENCE)
  context.learning_object_req_body = deepcopy(TEST_LEARNING_OBJECT)
  for key in DEL_KEYS:
    if key in context.learning_experience_req_body:
      del context.learning_experience_req_body[key]
    if key in context.learning_object_req_body:
      del context.learning_object_req_body[key]

  context.learning_experience_url = f"{API_URL}/learning-experience"
  context.learning_object_url = f"{API_URL}/learning-object"


@behave.when(
    "they add the new reference and delete the old reference of the learning object using a third-party tool"
)
def step_7_2(context):
  context.learning_experience_response = post_method(
      url=context.learning_experience_url,
      request_body=context.learning_experience_req_body)
  context.test_learning_experience = context.learning_experience_response.json()
  context.learning_experience_uuid = context.test_learning_experience['data'][
      "uuid"]

  context.learning_object_req_body["parent_nodes"]["learning_experiences"] = [
      context.learning_experience_uuid
  ]

  context.learning_object_response_1 = post_method(
      url=context.learning_object_url,
      request_body=context.learning_object_req_body)
  context.test_learning_object_1 = context.learning_object_response_1.json()

  context.learning_object_response_2 = post_method(
      url=context.learning_object_url,
      request_body=context.learning_object_req_body)
  context.test_learning_object_2 = context.learning_object_response_2.json()

  context.learning_object_req_body["parent_nodes"]["learning_experiences"] = []
  context.learning_object_req_body["is_archived"] = False
  context.learning_object_response_updated_1 = put_method(
      url=context.learning_object_url + "/" +
      context.test_learning_object_2["data"]["uuid"],
      request_body=context.learning_object_req_body)
  context.test_learning_object_updated_1 = context.learning_object_response_updated_1.json(
  )

  context.learning_object_req_body["parent_nodes"]["learning_experiences"] = [
      context.learning_experience_uuid
  ]

  for key in DEL_KEYS:
    if key in context.learning_object_req_body:
        del context.learning_object_req_body[key]
  context.learning_object_response_3 = post_method(
      url=context.learning_object_url,
      request_body=context.learning_object_req_body)
  context.test_learning_object_3 = context.learning_object_response_3.json()

  context.learning_experience_get_response = get_method(
      url=context.learning_experience_url + "/" +
      context.learning_experience_uuid)
  context.learning_experience_get_object = context.learning_experience_get_response.json(
  )


@behave.then(
    "the old learning object will get untagged and the new learning object will get tagged to the learning experience"
)
def step_7_3(context):
  assert context.test_learning_object_1["data"][
      "uuid"] in context.learning_experience_get_object["data"][
          "child_nodes"]["learning_objects"]
  assert context.test_learning_object_2["data"][
      "uuid"] not in context.learning_experience_get_object["data"][
          "child_nodes"]["learning_objects"]
  assert context.test_learning_object_3["data"][
      "uuid"] in context.learning_experience_get_object["data"][
          "child_nodes"]["learning_objects"]
