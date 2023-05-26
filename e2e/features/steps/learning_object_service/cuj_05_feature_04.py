"""
Parent-Child relationship between curriculum pathway and curriculum pathway
"""
import behave
import sys
import uuid
from copy import deepcopy

sys.path.append("../")
from e2e.setup import post_method, get_method, put_method
from e2e.test_config import API_URL_LEARNING_OBJECT_SERVICE
from e2e.test_object_schemas import TEST_CURRICULUM_PATHWAY, TEST_LEARNING_EXPERIENCE

API_URL = API_URL_LEARNING_OBJECT_SERVICE


@behave.given("that LXE or CD has access to the content authoring tool")
def step_1_1(context):
  context.curriculum_pathway_req_body = deepcopy(TEST_CURRICULUM_PATHWAY)
  context.curriculum_pathway_url = f"{API_URL}/curriculum-pathway"

  context.learning_experience_req_body = deepcopy(TEST_LEARNING_EXPERIENCE)
  context.learning_experience_url = f"{API_URL}/learning-experience"


@behave.when(
    "they design the curriculum pathway and the learning experience using a third-party tool"
)
def step_1_2(context):
  context.curriculum_pathway_response = post_method(
      url=context.curriculum_pathway_url,
      request_body=context.curriculum_pathway_req_body)
  context.test_curriculum_pathway = context.curriculum_pathway_response.json()
  context.curriculum_pathway_uuid = context.test_curriculum_pathway["data"][
      "uuid"]

  context.learning_experience_req_body["parent_nodes"][
      "curriculum_pathways"].append(context.curriculum_pathway_uuid)
  context.learning_experience_response = post_method(
      url=context.learning_experience_url,
      request_body=context.learning_experience_req_body)
  context.test_learning_experience = context.learning_experience_response.json()

  context.learning_experience_get_response = get_method(
      url=context.curriculum_pathway_url + "/" +
      context.curriculum_pathway_uuid)
  context.learning_experience_get_object = context.learning_experience_get_response.json(
  )


@behave.then(
    "the curriculum pathway and the learning experience will be created in a third-party tool"
)
def step_1_3(context):
  assert context.curriculum_pathway_response.status_code == 200
  assert context.test_curriculum_pathway["success"] is True
  assert "uuid" in context.test_curriculum_pathway["data"]
  assert "created_time" in context.test_curriculum_pathway["data"]
  assert "last_modified_time" in context.test_curriculum_pathway["data"]

  assert context.learning_experience_response.status_code == 200
  assert context.test_learning_experience["success"] is True
  assert "uuid" in context.test_learning_experience["data"]
  assert "created_time" in context.test_learning_experience["data"]
  assert "last_modified_time" in context.test_learning_experience["data"]


@behave.then("the learning experience gets associated with the curriculum pathway")
def step_1_4(context):
  assert context.curriculum_pathway_uuid in context.test_learning_experience[
      "data"]["parent_nodes"]["curriculum_pathways"]

  assert context.test_learning_experience["data"][
      "uuid"] in context.learning_experience_get_object["data"][
          "child_nodes"]["learning_experiences"]


@behave.given(
    "that an LXE or CD wants to create a learning experience providing the reference of the given curriculum pathway with incorrect uuid"
)
def step_2_1(context):
  context.curriculum_pathway_req_body = deepcopy(TEST_CURRICULUM_PATHWAY)
  context.curriculum_pathway_url = f"{API_URL}/curriculum-pathway"

  context.learning_experience_req_body = deepcopy(TEST_LEARNING_EXPERIENCE)
  context.learning_experience_url = f"{API_URL}/learning-experience"


@behave.when("they design the learning experience using a third-party tool")
def step_2_2(context):
  context.curriculum_pathway_response = post_method(
      url=context.curriculum_pathway_url,
      request_body=context.curriculum_pathway_req_body)
  context.test_curriculum_pathway = context.curriculum_pathway_response.json()
  context.curriculum_pathway_uuid = context.test_curriculum_pathway["data"][
      "uuid"]

  context.uuid = str(uuid.uuid4())
  context.learning_experience_req_body["parent_nodes"][
      "curriculum_pathways"].append(context.uuid)
  context.learning_experience_response = post_method(
      url=context.learning_experience_url,
      request_body=context.learning_experience_req_body)
  context.test_learning_experience = context.learning_experience_response.json()


@behave.then(
    "the user will get an error message of not found the reference to the curriculum pathway"
)
def step_2_3(context):
  assert context.curriculum_pathway_response.status_code == 200
  assert context.test_curriculum_pathway["success"] is True
  assert "uuid" in context.test_curriculum_pathway["data"]
  assert "created_time" in context.test_curriculum_pathway["data"]
  assert "last_modified_time" in context.test_curriculum_pathway["data"]

  assert context.learning_experience_response.status_code == 404
  assert context.test_learning_experience[
      "message"] == f"Curriculum Pathway with uuid {context.uuid} not found"


@behave.given(
    "that an LXE or CD wants to add the reference of curriculum pathway in the learning experience"
)
def step_3_1(context):
  context.curriculum_pathway_req_body = deepcopy(TEST_CURRICULUM_PATHWAY)
  context.curriculum_pathway_url = f"{API_URL}/curriculum-pathway"

  context.learning_experience_req_body = deepcopy(TEST_LEARNING_EXPERIENCE)
  context.learning_experience_url = f"{API_URL}/learning-experience"


@behave.when(
    "they design the multiple curriculum pathways and the single learning experience using a third-party tool"
)
def step_3_2(context):
  context.curriculum_pathway_response_1 = post_method(
      url=context.curriculum_pathway_url,
      request_body=context.curriculum_pathway_req_body)
  context.test_curriculum_pathway_1 = context.curriculum_pathway_response_1.json(
  )
  context.curriculum_pathway_uuid_1 = context.test_curriculum_pathway_1[
      "data"]["uuid"]

  context.curriculum_pathway_response_2 = post_method(
      url=context.curriculum_pathway_url,
      request_body=context.curriculum_pathway_req_body)
  context.test_curriculum_pathway_2 = context.curriculum_pathway_response_2.json(
  )
  context.curriculum_pathway_uuid_2 = context.test_curriculum_pathway_2[
      "data"]["uuid"]

  curriculum_pathway_uuid = [
      context.curriculum_pathway_uuid_1, context.curriculum_pathway_uuid_2
  ]
  context.learning_experience_req_body["parent_nodes"][
      "curriculum_pathways"].extend(curriculum_pathway_uuid)
  context.learning_experience_response = post_method(
      url=context.learning_experience_url,
      request_body=context.learning_experience_req_body)
  context.test_learning_experience = context.learning_experience_response.json()

  context.learning_experience_get_response_1 = get_method(
      url=context.curriculum_pathway_url + "/" +
      context.curriculum_pathway_uuid_1)
  context.learning_experience_get_object_1 = context.learning_experience_get_response_1.json(
  )

  context.learning_experience_get_response_2 = get_method(
      url=context.curriculum_pathway_url + "/" +
      context.curriculum_pathway_uuid_2)
  context.learning_experience_get_object_2 = context.learning_experience_get_response_2.json(
  )


@behave.then(
    "the multiple curriculum pathways and the learning experience will be created in a third-party tool"
)
def step_3_3(context):
  assert context.curriculum_pathway_response_1.status_code == 200
  assert context.test_curriculum_pathway_1["success"] is True
  assert "uuid" in context.test_curriculum_pathway_1["data"]
  assert "created_time" in context.test_curriculum_pathway_1["data"]
  assert "last_modified_time" in context.test_curriculum_pathway_1["data"]

  assert context.curriculum_pathway_response_2.status_code == 200
  assert context.test_curriculum_pathway_2["success"] is True
  assert "uuid" in context.test_curriculum_pathway_2["data"]
  assert "created_time" in context.test_curriculum_pathway_2["data"]
  assert "last_modified_time" in context.test_curriculum_pathway_2["data"]

  assert context.learning_experience_response.status_code == 200
  assert context.test_learning_experience["success"] is True
  assert "uuid" in context.test_learning_experience["data"]
  assert "created_time" in context.test_learning_experience["data"]
  assert "last_modified_time" in context.test_learning_experience["data"]


@behave.then(
    "the learning experience gets associated with the multiple curriculum pathways"
)
def step_3_4(context):
  assert context.curriculum_pathway_uuid_1 in context.test_learning_experience[
      "data"]["parent_nodes"]["curriculum_pathways"]
  assert context.curriculum_pathway_uuid_2 in context.test_learning_experience[
      "data"]["parent_nodes"]["curriculum_pathways"]

  assert context.test_learning_experience["data"][
      "uuid"] in context.learning_experience_get_object_1["data"][
          "child_nodes"]["learning_experiences"]
  assert context.test_learning_experience["data"][
      "uuid"] in context.learning_experience_get_object_2["data"][
          "child_nodes"]["learning_experiences"]


@behave.given(
    "that an LXE or CD wants to add the reference of a single curriculum pathway in the multiple learning experiences"
)
def step_4_1(context):
  context.curriculum_pathway_req_body = deepcopy(TEST_CURRICULUM_PATHWAY)
  context.curriculum_pathway_url = f"{API_URL}/curriculum-pathway"

  context.learning_experience_req_body = deepcopy(TEST_LEARNING_EXPERIENCE)
  context.learning_experience_url = f"{API_URL}/learning-experience"


@behave.when(
    "they design the multiple learning experiences using a third-party tool")
def step_4_2(context):
  context.curriculum_pathway_response = post_method(
      url=context.curriculum_pathway_url,
      request_body=context.curriculum_pathway_req_body)
  context.test_curriculum_pathway = context.curriculum_pathway_response.json()
  context.curriculum_pathway_uuid = context.test_curriculum_pathway["data"][
      "uuid"]

  context.learning_experience_req_body["parent_nodes"]["curriculum_pathways"] = [
      context.curriculum_pathway_uuid
  ]

  context.learning_experience_response_1 = post_method(
      url=context.learning_experience_url,
      request_body=context.learning_experience_req_body)
  context.test_learning_experience_1 = context.learning_experience_response_1.json()

  context.learning_experience_response_2 = post_method(
      url=context.learning_experience_url,
      request_body=context.learning_experience_req_body)
  context.test_learning_experience_2 = context.learning_experience_response_2.json()

  context.learning_experience_get_response = get_method(
      url=context.curriculum_pathway_url + "/" +
      context.curriculum_pathway_uuid)
  context.learning_experience_get_object = context.learning_experience_get_response.json(
  )


@behave.then("the multiple learning experiences will be created in a third-party tool")
def step_4_3(context):
  assert context.curriculum_pathway_response.status_code == 200
  assert context.test_curriculum_pathway["success"] is True
  assert "uuid" in context.test_curriculum_pathway["data"]
  assert "created_time" in context.test_curriculum_pathway["data"]
  assert "last_modified_time" in context.test_curriculum_pathway["data"]

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


@behave.then(
    "all the learning experiences gets associated with the given curriculum pathways"
)
def step_4_4(context):
  assert context.curriculum_pathway_uuid in context.test_learning_experience_1[
      "data"]["parent_nodes"]["curriculum_pathways"]
  assert context.curriculum_pathway_uuid in context.test_learning_experience_2[
      "data"]["parent_nodes"]["curriculum_pathways"]

  assert context.test_learning_experience_1["data"][
      "uuid"] in context.learning_experience_get_object["data"][
          "child_nodes"]["learning_experiences"]
  assert context.test_learning_experience_2["data"][
      "uuid"] in context.learning_experience_get_object["data"][
          "child_nodes"]["learning_experiences"]


@behave.given(
    "that an LXE or CD wants to replace an old reference of the curriculum pathway with a new reference in the learning experience"
)
def step_5_1(context):
  context.curriculum_pathway_req_body = deepcopy(TEST_CURRICULUM_PATHWAY)
  context.curriculum_pathway_url = f"{API_URL}/curriculum-pathway"

  context.learning_experience_req_body = deepcopy(TEST_LEARNING_EXPERIENCE)
  context.learning_experience_url = f"{API_URL}/learning-experience"


@behave.when("they update the new curriculum pathway using a third-party tool")
def step_5_2(context):
  context.curriculum_pathway_response_old = post_method(
      url=context.curriculum_pathway_url,
      request_body=context.curriculum_pathway_req_body)
  context.test_curriculum_pathway_old = context.curriculum_pathway_response_old.json(
  )
  context.curriculum_pathway_uuid_old = context.test_curriculum_pathway_old[
      "data"]["uuid"]

  context.learning_experience_req_body["parent_nodes"]["curriculum_pathways"] = [
      context.curriculum_pathway_uuid_old
  ]
  context.learning_experience_response_old = post_method(
      url=context.learning_experience_url,
      request_body=context.learning_experience_req_body)
  context.test_learning_experience_old = context.learning_experience_response_old.json()

  context.curriculum_pathway_response_new = post_method(
      url=context.curriculum_pathway_url,
      request_body=context.curriculum_pathway_req_body)
  context.test_curriculum_pathway_new = context.curriculum_pathway_response_new.json(
  )
  context.curriculum_pathway_uuid_new = context.test_curriculum_pathway_new[
      "data"]["uuid"]

  context.learning_experience_req_body["parent_nodes"]["curriculum_pathways"] = [
      context.curriculum_pathway_uuid_new
  ]
  context.learning_experience_req_body["is_archived"] = False

  context.learning_experience_response_updated = put_method(
      url=context.learning_experience_url + "/" +
      context.test_learning_experience_old["data"]["uuid"],
      request_body=context.learning_experience_req_body)
  context.test_learning_experience_updated = context.learning_experience_response_updated.json(
  )

  context.learning_experience_get_response_old = get_method(
      url=context.curriculum_pathway_url + "/" +
      context.curriculum_pathway_uuid_old)
  context.learning_experience_get_object_old = context.learning_experience_get_response_old.json(
  )

  context.learning_experience_get_response_new = get_method(
      url=context.curriculum_pathway_url + "/" +
      context.curriculum_pathway_uuid_new)
  context.learning_experience_get_object_new = context.learning_experience_get_response_new.json(
  )


@behave.then(
    "the learning experience gets associated with the new curriculum pathway")
def step_5_3(context):
  assert context.curriculum_pathway_response_new.status_code == 200
  assert context.test_curriculum_pathway_new["success"] is True

  assert context.curriculum_pathway_uuid_new in context.test_learning_experience_updated[
      "data"]["parent_nodes"]["curriculum_pathways"]
  assert context.curriculum_pathway_uuid_old not in context.test_learning_experience_updated[
      "data"]["parent_nodes"]["curriculum_pathways"]

  assert context.test_learning_experience_updated["data"][
      "uuid"] not in context.learning_experience_get_object_old["data"][
          "child_nodes"]["learning_experiences"]
  assert context.test_learning_experience_updated["data"][
      "uuid"] in context.learning_experience_get_object_new["data"][
          "child_nodes"]["learning_experiences"]


@behave.given(
    "that an LXE or CD wants to add a reference to one more curriculum pathway in the learning experience"
)
def step_6_1(context):
  context.curriculum_pathway_req_body = deepcopy(TEST_CURRICULUM_PATHWAY)
  context.curriculum_pathway_url = f"{API_URL}/curriculum-pathway"

  context.learning_experience_req_body = deepcopy(TEST_LEARNING_EXPERIENCE)
  context.learning_experience_url = f"{API_URL}/learning-experience"


@behave.when("they update the learning experience using a third-party tool by adding incorrect reference of the curriculum pathway")
def step_6_2(context):
  context.curriculum_pathway_response = post_method(
      url=context.curriculum_pathway_url,
      request_body=context.curriculum_pathway_req_body)
  context.test_curriculum_pathway = context.curriculum_pathway_response.json()
  context.curriculum_pathway_uuid = context.test_curriculum_pathway["data"][
      "uuid"]

  context.learning_experience_response = post_method(
      url=context.learning_experience_url,
      request_body=context.learning_experience_req_body)
  context.test_learning_experience = context.learning_experience_response.json()

  context.uuid = str(uuid.uuid4())
  context.learning_experience_req_body["parent_nodes"]["curriculum_pathways"] = [
      context.uuid
  ]
  context.learning_experience_req_body["is_archived"] = False

  context.learning_experience_response_updated = put_method(
      url=context.learning_experience_url + "/" +
      context.test_learning_experience["data"]["uuid"],
      request_body=context.learning_experience_req_body)
  context.test_learning_experience_updated = context.learning_experience_response_updated.json(
  )


@behave.then(
    "the user gets an error message of not found the reference to the curriculum pathway"
)
def step_6_3(context):
  assert context.curriculum_pathway_response.status_code == 200
  assert context.test_curriculum_pathway["success"] is True

  assert context.learning_experience_response_updated.status_code == 404
  assert context.test_learning_experience_updated[
      "message"] == f"Curriculum Pathway with uuid {context.uuid} not found"


@behave.given(
    "that an LXE or CD wants to update the reference of the learning experience in the curriculum pathway"
)
def step_7_1(context):
  context.curriculum_pathway_req_body = deepcopy(TEST_CURRICULUM_PATHWAY)
  context.curriculum_pathway_url = f"{API_URL}/curriculum-pathway"

  context.learning_experience_req_body = deepcopy(TEST_LEARNING_EXPERIENCE)
  context.learning_experience_url = f"{API_URL}/learning-experience"


@behave.when(
    "they add the new reference and delete the old reference of the learning experience using a third-party tool"
)
def step_7_2(context):
  context.curriculum_pathway_response = post_method(
      url=context.curriculum_pathway_url,
      request_body=context.curriculum_pathway_req_body)
  context.test_curriculum_pathway = context.curriculum_pathway_response.json()
  context.curriculum_pathway_uuid = context.test_curriculum_pathway["data"][
      "uuid"]

  context.learning_experience_req_body["parent_nodes"]["curriculum_pathways"] = [
      context.curriculum_pathway_uuid
  ]

  context.learning_experience_response_1 = post_method(
      url=context.learning_experience_url,
      request_body=context.learning_experience_req_body)
  context.test_learning_experience_1 = context.learning_experience_response_1.json()

  context.learning_experience_response_2 = post_method(
      url=context.learning_experience_url,
      request_body=context.learning_experience_req_body)
  context.test_learning_experience_2 = context.learning_experience_response_2.json()

  context.learning_experience_req_body["parent_nodes"]["curriculum_pathways"] = []
  context.learning_experience_req_body["is_archived"] = False
  context.learning_experience_response_updated_1 = put_method(
      url=context.learning_experience_url + "/" +
      context.test_learning_experience_2["data"]["uuid"],
      request_body=context.learning_experience_req_body)
  context.test_learning_experience_updated_1 = context.learning_experience_response_updated_1.json(
  )

  context.learning_experience_req_body["parent_nodes"]["curriculum_pathways"] = [
      context.curriculum_pathway_uuid
  ]

  context.learning_experience_response_3 = post_method(
      url=context.learning_experience_url,
      request_body=context.learning_experience_req_body)
  context.test_learning_experience_3 = context.learning_experience_response_1.json()

  context.learning_experience_get_response = get_method(
      url=context.curriculum_pathway_url + "/" +
      context.curriculum_pathway_uuid)
  context.learning_experience_get_object = context.learning_experience_get_response.json(
  )


@behave.then(
    "the old learning experience will get untagged and the new learning experience will get tagged to the curriculum pathway"
)
def step_7_3(context):
  assert context.test_learning_experience_1["data"][
      "uuid"] in context.learning_experience_get_object["data"][
          "child_nodes"]["learning_experiences"]
  assert context.test_learning_experience_2["data"][
      "uuid"] not in context.learning_experience_get_object["data"][
          "child_nodes"]["learning_experiences"]
  assert context.test_learning_experience_3["data"][
      "uuid"] in context.learning_experience_get_object["data"][
          "child_nodes"]["learning_experiences"]


@behave.given("that LXE or CD has access to the content authoring tool to associate the child curriculum pathway with the parent curriculum pathway")
def step_8_1(context):
  context.parent_curriculum_pathway_req_body = deepcopy(TEST_CURRICULUM_PATHWAY)
  context.child_curriculum_pathway_req_body = deepcopy(TEST_CURRICULUM_PATHWAY)
  context.curriculum_pathway_url = f"{API_URL}/curriculum-pathway"


@behave.when(
    "they design the parent curriculum pathway and the child curriculum pathway using a third-party tool"
)
def step_8_2(context):
  context.parent_curriculum_pathway_response = post_method(
      url=context.curriculum_pathway_url,
      request_body=context.parent_curriculum_pathway_req_body)
  context.test_parent_curriculum_pathway = context.parent_curriculum_pathway_response.json()
  context.parent_curriculum_pathway_uuid = context.test_parent_curriculum_pathway["data"][
      "uuid"]

  context.child_curriculum_pathway_req_body["parent_nodes"][
      "curriculum_pathways"].append(context.parent_curriculum_pathway_uuid)
  context.child_curriculum_pathway_response = post_method(
      url=context.curriculum_pathway_url,
      request_body=context.child_curriculum_pathway_req_body)
  context.test_child_curriculum_pathway = context.child_curriculum_pathway_response.json()

  context.child_curriculum_pathway_get_response = get_method(
      url=context.curriculum_pathway_url + "/" +
      context.parent_curriculum_pathway_uuid)
  context.child_curriculum_pathway_get_object = context.child_curriculum_pathway_get_response.json(
  )


@behave.then(
    "the parent curriculum pathway and the child curriculum pathway will be created in a third-party tool"
)
def step_8_3(context):
  assert context.parent_curriculum_pathway_response.status_code == 200
  assert context.test_parent_curriculum_pathway["success"] is True
  assert "uuid" in context.test_parent_curriculum_pathway["data"]
  assert "created_time" in context.test_parent_curriculum_pathway["data"]
  assert "last_modified_time" in context.test_parent_curriculum_pathway["data"]

  assert context.child_curriculum_pathway_response.status_code == 200
  assert context.test_child_curriculum_pathway["success"] is True
  assert "uuid" in context.test_child_curriculum_pathway["data"]
  assert "created_time" in context.test_child_curriculum_pathway["data"]
  assert "last_modified_time" in context.test_child_curriculum_pathway["data"]


@behave.then("the child curriculum pathway gets associated with the parent curriculum pathway")
def step_8_4(context):
  assert context.parent_curriculum_pathway_uuid in context.test_child_curriculum_pathway[
      "data"]["parent_nodes"]["curriculum_pathways"]

  assert context.test_child_curriculum_pathway["data"][
      "uuid"] in context.child_curriculum_pathway_get_object["data"][
          "child_nodes"]["curriculum_pathways"]


@behave.given(
    "that an LXE or CD wants to create a child curriculum pathway providing the reference of the given parent curriculum pathway with incorrect uuid"
)
def step_9_1(context):
  context.parent_curriculum_pathway_req_body = deepcopy(TEST_CURRICULUM_PATHWAY)
  context.child_curriculum_pathway_req_body = deepcopy(TEST_CURRICULUM_PATHWAY)
  context.curriculum_pathway_url = f"{API_URL}/curriculum-pathway"


@behave.when("they design the child curriculum pathway using a third-party tool")
def step_9_2(context):
  context.parent_curriculum_pathway_response = post_method(
      url=context.curriculum_pathway_url,
      request_body=context.parent_curriculum_pathway_req_body)
  context.test_parent_curriculum_pathway = context.parent_curriculum_pathway_response.json()
  context.parent_curriculum_pathway_uuid = context.test_parent_curriculum_pathway["data"][
      "uuid"]

  context.uuid = str(uuid.uuid4())
  context.child_curriculum_pathway_req_body["parent_nodes"][
      "curriculum_pathways"].append(context.uuid)
  context.child_curriculum_pathway_response = post_method(
      url=context.curriculum_pathway_url,
      request_body=context.child_curriculum_pathway_req_body)
  context.test_child_curriculum_pathway = context.child_curriculum_pathway_response.json()


@behave.then(
    "the user will get an error message of not found the reference to the parent curriculum pathway"
)
def step_9_3(context):
  assert context.parent_curriculum_pathway_response.status_code == 200
  assert context.test_parent_curriculum_pathway["success"] is True
  assert "uuid" in context.test_parent_curriculum_pathway["data"]
  assert "created_time" in context.test_parent_curriculum_pathway["data"]
  assert "last_modified_time" in context.test_parent_curriculum_pathway["data"]

  assert context.child_curriculum_pathway_response.status_code == 404
  assert context.test_child_curriculum_pathway[
      "message"] == f"Curriculum Pathway with uuid {context.uuid} not found"


@behave.given(
    "that an LXE or CD wants to add the reference of parent curriculum pathway in the child curriculum pathway"
)
def step_10_1(context):
  context.parent_curriculum_pathway_req_body = deepcopy(TEST_CURRICULUM_PATHWAY)
  context.child_curriculum_pathway_req_body = deepcopy(TEST_CURRICULUM_PATHWAY)
  context.curriculum_pathway_url = f"{API_URL}/curriculum-pathway"


@behave.when(
    "they design the multiple parent curriculum pathways and the single child curriculum pathway using a third-party tool"
)
def step_10_2(context):
  context.parent_curriculum_pathway_response_1 = post_method(
      url=context.curriculum_pathway_url,
      request_body=context.parent_curriculum_pathway_req_body)
  context.test_parent_curriculum_pathway_1 = context.parent_curriculum_pathway_response_1.json(
  )
  context.parent_curriculum_pathway_uuid_1 = context.test_parent_curriculum_pathway_1[
      "data"]["uuid"]

  context.parent_curriculum_pathway_response_2 = post_method(
      url=context.curriculum_pathway_url,
      request_body=context.parent_curriculum_pathway_req_body)
  context.test_parent_curriculum_pathway_2 = context.parent_curriculum_pathway_response_2.json(
  )
  context.parent_curriculum_pathway_uuid_2 = context.test_parent_curriculum_pathway_2[
      "data"]["uuid"]

  parent_curriculum_pathway_uuid = [
      context.parent_curriculum_pathway_uuid_1, context.parent_curriculum_pathway_uuid_2
  ]
  context.child_curriculum_pathway_req_body["parent_nodes"][
      "curriculum_pathways"].extend(parent_curriculum_pathway_uuid)
  context.child_curriculum_pathway_response = post_method(
      url=context.curriculum_pathway_url,
      request_body=context.child_curriculum_pathway_req_body)
  context.test_child_curriculum_pathway = context.child_curriculum_pathway_response.json()

  context.child_curriculum_pathway_get_response_1 = get_method(
      url=context.curriculum_pathway_url + "/" +
      context.parent_curriculum_pathway_uuid_1)
  context.child_curriculum_pathway_get_object_1 = context.child_curriculum_pathway_get_response_1.json(
  )

  context.child_curriculum_pathway_get_response_2 = get_method(
      url=context.curriculum_pathway_url + "/" +
      context.parent_curriculum_pathway_uuid_2)
  context.child_curriculum_pathway_get_object_2 = context.child_curriculum_pathway_get_response_2.json(
  )


@behave.then(
    "the multiple parent curriculum pathways and the child curriculum pathway will be created in a third-party tool"
)
def step_10_3(context):
  assert context.parent_curriculum_pathway_response_1.status_code == 200
  assert context.test_parent_curriculum_pathway_1["success"] is True
  assert "uuid" in context.test_parent_curriculum_pathway_1["data"]
  assert "created_time" in context.test_parent_curriculum_pathway_1["data"]
  assert "last_modified_time" in context.test_parent_curriculum_pathway_1["data"]

  assert context.parent_curriculum_pathway_response_2.status_code == 200
  assert context.test_parent_curriculum_pathway_2["success"] is True
  assert "uuid" in context.test_parent_curriculum_pathway_2["data"]
  assert "created_time" in context.test_parent_curriculum_pathway_2["data"]
  assert "last_modified_time" in context.test_parent_curriculum_pathway_2["data"]

  assert context.child_curriculum_pathway_response.status_code == 200
  assert context.test_child_curriculum_pathway["success"] is True
  assert "uuid" in context.test_child_curriculum_pathway["data"]
  assert "created_time" in context.test_child_curriculum_pathway["data"]
  assert "last_modified_time" in context.test_child_curriculum_pathway["data"]


@behave.then(
    "the child curriculum pathway gets associated with the multiple parent curriculum pathways"
)
def step_10_4(context):
  assert context.parent_curriculum_pathway_uuid_1 in context.test_child_curriculum_pathway[
      "data"]["parent_nodes"]["curriculum_pathways"]
  assert context.parent_curriculum_pathway_uuid_2 in context.test_child_curriculum_pathway[
      "data"]["parent_nodes"]["curriculum_pathways"]

  assert context.test_child_curriculum_pathway["data"][
      "uuid"] in context.child_curriculum_pathway_get_object_1["data"][
          "child_nodes"]["curriculum_pathways"]
  assert context.test_child_curriculum_pathway["data"][
      "uuid"] in context.child_curriculum_pathway_get_object_2["data"][
          "child_nodes"]["curriculum_pathways"]
