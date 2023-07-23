"""
For the given learner get the curriculum pathway
"""

from e2e.setup import post_method, get_method, delete_method, put_method
from copy import copy, deepcopy
from e2e.test_config import DEL_KEYS, API_URL_LEARNER_PROFILE_SERVICE, API_URL_LEARNING_OBJECT_SERVICE, API_URL_USER_MANAGEMENT as UM_API_URL
from e2e.test_object_schemas import (TEST_USER, TEST_CURRICULUM_PATHWAY,
                                 TEST_ASSOCIATION_GROUP)
import behave
import sys
from uuid import uuid4

sys.path.append("../")


#Scenario: Get the curriculum pathway for a learner with correct uuid
@behave.given(
    "learner was already created, this learner should be present in the learner association group and curriculum pathway is also exists in the database"
)
def step_1_1(context):

  # Create the pathway
  context.req_body = {**TEST_CURRICULUM_PATHWAY, "alias": "program",
                      "is_active": True}
  for key in DEL_KEYS:
    if key in context.req_body:
      del context.req_body[key]
  context.url = f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway"
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  context.curriculum_pathway_id = context.res_data["data"]["uuid"]

  context.res = put_method(
      url=f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway/{context.curriculum_pathway_id}",
      request_body = {"is_active": True}
  )
  assert context.res.status_code == 200

  # create an learner association group and add learner to it
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = str(uuid4())
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/association-groups/learner-association"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  context.learner_association_uuid = context.res_data["data"]["uuid"]
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the association group"

  # create a user of learner type and add to the learner group
  context.user_dict = deepcopy(TEST_USER)
  context.user_dict["email"] = f"{uuid4()}@gmail.com"
  context.url = f"{UM_API_URL}/user"
  context.post_user_res = post_method(
      url=context.url, request_body=context.user_dict)
  assert context.post_user_res.status_code == 200
  context.user_id = context.post_user_res.json()["data"]["user_id"]
  context.learner_id = context.post_user_res.json()["data"]["user_type_ref"]

  # add learner to the learner association group
  add_users = {"users": [context.user_id], "status": "active"}
  context.url = f"{UM_API_URL}/association-groups/learner-association/{context.learner_association_uuid}/users/add"
  context.res = post_method(url=context.url, request_body=add_users)
  context.res_data = context.res.json()
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully added the users to the learner association group"


@behave.when(
    "an API request sent to get the pathway for the given learner with correct uuid"
)
def step_impl_1_2(context):
  context.learner_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner"
  context.url = f"{context.learner_url}/{context.learner_id}/curriculum-pathway"
  context.response = get_method(url=context.url)
  context.response_data = context.response.json()


@behave.then("the pathway detail correctly fetched")
def step_impl_1_3(context):
  context.response_data = context.response.json()
  assert context.response.status_code == 200
  assert context.response_data[
      "message"] == "Successfully fetch the curriculum pathway for the learner"
  curriculum_pathway_id = context.response_data["data"]["curriculum_pathway_id"]
  context.url = f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway/{curriculum_pathway_id}"
  context.response = delete_method(context.url)
  assert context.response.status_code == 200


# Scenario: Get the curriculum pathway for learner with correct uuid
@behave.given(
    "learner was already created, this learner should be present in the learner association group and curriculum pathway is not exist in the database"
)
def step_1_1(context):

  # create an learner association group and add learner to it
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = str(uuid4())
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/association-groups/learner-association"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  context.learner_association_uuid = context.res_data["data"]["uuid"]
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the association group"

  # create a user of learner type and add to the learner group
  context.user_dict = deepcopy(TEST_USER)
  context.user_dict["email"] = f"{uuid4()}@gmail.com"
  context.url = f"{UM_API_URL}/user"
  context.post_user_res = post_method(
      url=context.url, request_body=context.user_dict)
  assert context.post_user_res.status_code == 200
  context.user_id = context.post_user_res.json()["data"]["user_id"]
  context.learner_id = context.post_user_res.json()["data"]["user_type_ref"]

  # add learner to the learner association group
  add_users = {"users": [context.user_id], "status": "active"}
  context.url = f"{UM_API_URL}/association-groups/learner-association/{context.learner_association_uuid}/users/add"
  context.res = post_method(url=context.url, request_body=add_users)
  context.res_data = context.res.json()
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully added the users to the learner association group"


@behave.when(
    "an API request is sent to get the pathway for the given learner with correct uuid"
)
def step_impl_1_2(context):
  context.learner_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner"
  context.url = f"{context.learner_url}/{context.learner_id}/curriculum-pathway"
  context.response = get_method(url=context.url)


@behave.then("error response returned")
def step_impl_1_3(context):
  context.response_data = context.response.json()
  assert context.response.status_code == 404
  assert context.response_data[
      "message"] == f"Given Learner with uuid {context.learner_id} no pathway found"


# Scenario: Get the curriculum pathway for the learner with correct uuid
@behave.given(
    "learner was already created, this learner is not be present in any of the learner association group and curriculum pathway is not exist in the database"
)
def step_1_1(context):

  # create an learner association group and add learner to it
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = str(uuid4())
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/association-groups/learner-association"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  context.learner_association_uuid = context.res_data["data"]["uuid"]
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the association group"

  # create a user of learner type and add to the learner group
  context.user_dict = deepcopy(TEST_USER)
  context.user_dict["email"] = f"{uuid4()}@gmail.com"
  context.url = f"{UM_API_URL}/user"
  context.post_user_res = post_method(
      url=context.url, request_body=context.user_dict)
  assert context.post_user_res.status_code == 200
  context.user_id = context.post_user_res.json()["data"]["user_id"]
  context.learner_id = context.post_user_res.json()["data"]["user_type_ref"]


@behave.when(
    "an API request is sent to get pathway for the given learner with correct uuid"
)
def step_impl_1_2(context):
  context.learner_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner"
  context.url = f"{context.learner_url}/{context.learner_id}/curriculum-pathway"
  context.response = get_method(url=context.url)


@behave.then("error response is returned")
def step_impl_1_3(context):
  context.response_data = context.response.json()
  assert context.response.status_code == 404
  assert context.response_data[
      "message"] == f"Given Learner with uuid {context.learner_id} is not present in any of the learner association group"


# Scenario: Get the curriculum pathway for a learner with incorrect uuid
@behave.given(
    "learner is already created, this learner should be present in the learner association group"
)
def step_1_1(context):

  # create an learner association group and add learner to it
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = str(uuid4())
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/association-groups/learner-association"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  context.learner_association_uuid = context.res_data["data"]["uuid"]
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the association group"

  # create a user of learner type and add to the learner group
  context.user_dict = deepcopy(TEST_USER)
  context.user_dict["email"] = f"{uuid4()}@gmail.com"
  context.url = f"{UM_API_URL}/user"
  context.post_user_res = post_method(
      url=context.url, request_body=context.user_dict)
  assert context.post_user_res.status_code == 200
  context.user_id = context.post_user_res.json()["data"]["user_id"]
  context.learner_id = context.post_user_res.json()["data"]["user_type_ref"]

  # add learner to the learner association group
  add_users = {"users": [context.user_id], "status": "active"}
  context.url = f"{UM_API_URL}/association-groups/learner-association/{context.learner_association_uuid}/users/add"
  context.res = post_method(url=context.url, request_body=add_users)
  context.res_data = context.res.json()
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully added the users to the learner association group"


@behave.when(
    "an API request sent to get pathway for the given learner with incorrect uuid"
)
def step_impl_1_2(context):
  context.learner_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner"
  context.url = f"{context.learner_url}/learner_id/curriculum-pathway"
  context.response = get_method(url=context.url)


@behave.then("error response is return")
def step_impl_1_3(context):
  context.response_data = context.response.json()
  assert context.response.status_code == 404
  assert context.response_data[
      "message"] == "Learner with uuid learner_id not found"
