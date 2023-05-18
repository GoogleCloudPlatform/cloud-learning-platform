"""
Feature: Relationship between User and Group
"""
import behave
import sys
from copy import deepcopy
from uuid import uuid4

sys.path.append("../")
from common.models import UserGroup
from test_object_schemas import TEST_USER, TEST_USER_GROUP
from environment import TEST_USER_MANAGEMENT_PATH
from test_config import (API_URL_USER_MANAGEMENT as UM_API_URL,
                         API_URL_LEARNER_PROFILE_SERVICE as SLP_API_URL,
                         API_URL_LEARNING_RECORD_SERVICE as LRS_API_URL)
from setup import post_method, get_method, put_method, delete_method
'''
Scenario: Add new user to the group within User management 
'''


@behave.given(
    "A user has privilege to create a user and wants to assign Group to the new user during creation"
)
def step_impl_1(context):
  #create group
  group_dict = {**TEST_USER_GROUP, "name": "learner"}
  post_group = post_method(url=f"{UM_API_URL}/user-group/immutable", request_body=group_dict)
  post_group_data = post_group.json()
  assert post_group.status_code in [200, 409]
  if post_group.status_code == 200:
    context.group_uuid = post_group_data["data"]["uuid"]
  if post_group.status_code == 409:
    user_group = UserGroup.find_by_name(group_dict["name"])
    user_group.is_immutable = True
    user_group.update()
    context.group_uuid = user_group.id

  context.user_dict = deepcopy({
      **TEST_USER, "user_groups": [context.group_uuid]
  })
  context.user_dict["email"] = f"{uuid4()}@gmail.com"

  context.url = f"{UM_API_URL}/user"


@behave.when("A API request to create user is sent to User management")
def step_impl_2(context):

  context.post_user_res = post_method(
      url=context.url, request_body=context.user_dict)


@behave.then("the new user is successfully created by user management")
def step_impl_3(context):
  assert context.post_user_res.status_code == 200
  context.post_user_res_dict = context.post_user_res.json()["data"]
  context.user_id = context.post_user_res_dict.get("user_id", "")


@behave.then("the new user is added to the assigned groups")
def step_impl_3(context):
  get_group_res = get_method(url=f"{UM_API_URL}/user-group/{context.group_uuid}")
  assert get_group_res.status_code == 200
  get_group_res_dict = get_group_res.json()["data"]
  assert context.user_id in get_group_res_dict.get("users", [])


'''
Scenario: Update groups of a existing user within User management 
'''


@behave.given(
    "A user has privilege to update a user and wants to update groups of a user"
)
def step_impl_1(context):
  #create group 1
  group_dict = {**TEST_USER_GROUP, "name": "coach"}
  post_group_1 = post_method(url=f"{UM_API_URL}/user-group/immutable", request_body=group_dict)
  #create group 2
  group_dict_2 = {**TEST_USER_GROUP, "name": f"{uuid4()}"}
  post_group_2 = post_method(url=f"{UM_API_URL}/user-group", request_body=group_dict_2)
  post_group_data_1 = post_group_1.json()
  post_group_data_2 = post_group_2.json()
  # context.group_uuid = post_group_data_2["data"]["uuid"]
  assert post_group_1.status_code in [200, 409]
  if post_group_1.status_code == 200:
    context.group_uuid_1 = post_group_data_1["data"]["uuid"]
  if post_group_1.status_code == 409:
    user_group1 = UserGroup.find_by_name(group_dict["name"])
    user_group1.is_immutable = True
    user_group1.update()
    context.group_uuid_1 = user_group1.id

  assert post_group_2.status_code in [200, 409]
  if post_group_2.status_code == 200:
    context.group_uuid_2 = post_group_data_2["data"]["uuid"]
  if post_group_2.status_code == 409:
    user_group2 = UserGroup.find_by_name(group_dict_2["name"])
    context.group_uuid_2 = user_group2.id
  #create user
  context.user_dict = deepcopy({
      **TEST_USER, "user_groups": [context.group_uuid_1], "user_type": "coach",
      "email": f"{str(uuid4())}@gmail.com",
  })
  context.user_dict["email"] = f"{uuid4()}@gmail.com"
  context.post_user_res = post_method(
      url=f"{UM_API_URL}/user", request_body=context.user_dict)
  assert context.post_user_res.status_code == 200
  post_user_res_dict = context.post_user_res.json()["data"]
  context.user_id = post_user_res_dict.get("user_id", "")
  context.url = f"{UM_API_URL}/user/{context.user_id}"


@behave.when("A API request to update user is sent to User management")
def step_impl_2(context):
  context.updated_user_data = {
    "user_groups": [context.group_uuid_2]
  }
  context.updated_user_res = put_method(
      url=context.url, request_body=context.updated_user_data)


@behave.then("the groups of the user are successfully updated")
def step_impl_3(context):
  assert context.updated_user_res.status_code == 200
  context.updated_user_res_dict = context.updated_user_res.json()["data"]
  assert context.updated_user_res_dict[
      "user_groups"] == context.updated_user_data["user_groups"]


@behave.then(
    "the user is added to the assigned groups and removed from the unassiged groups"
)
def step_impl_3(context):
  get_group_res = get_method(url=f"{UM_API_URL}/user-group/{context.group_uuid_2}")
  assert get_group_res.status_code == 200
  get_group_res_dict = get_group_res.json()["data"]
  assert context.user_id in get_group_res_dict.get("users", [])


'''
Scenario: Update Group documents when a user is deleted 
'''


@behave.given("A user has privilege to delete a user and wants to delete a user"
             )
def step_impl_1(context):
  #create group
  group_dict = {**TEST_USER_GROUP, "name": "admin"}
  post_group = post_method(url=f"{UM_API_URL}/user-group/immutable", request_body=group_dict)
  post_group_data = post_group.json()
  assert post_group.status_code in [200, 409]
  if post_group.status_code == 200:
    context.group_uuid = post_group_data["data"]["uuid"]
  if post_group.status_code == 409:
    user_group = UserGroup.find_by_name(group_dict["name"])
    context.group_uuid = user_group.id

  

  #create user
  context.user_dict = deepcopy({
      **TEST_USER, "user_groups": [context.group_uuid], "user_type": "admin"
  })
  context.user_dict["email"] = f"{uuid4()}@gmail.com"
  context.post_user_res = post_method(
      url=f"{UM_API_URL}/user", request_body=context.user_dict)
  assert context.post_user_res.status_code == 200
  post_user_res_dict = context.post_user_res.json()["data"]
  context.user_id = post_user_res_dict.get("user_id", "")
  context.url = f"{UM_API_URL}/user/{context.user_id}"


@behave.when("A API request to delete a user is sent to User management")
def step_impl_2(context):
  context.delete_user_res = delete_method(url=context.url)


@behave.then("the user is successfully deleted by the user management")
def step_impl_3(context):
  assert context.delete_user_res.status_code == 200
  assert context.delete_user_res.json(
  )["message"] == "Successfully deleted the user and associated agent, learner/faculty"


@behave.then("the user should be removed from all the assigned groups")
def step_impl_3(context):
  get_group_res = get_method(url=f"{UM_API_URL}/user-group/{context.group_uuid}")
  assert get_group_res.status_code == 200
  get_group_res_dict = get_group_res.json()["data"]
  assert not context.user_id in get_group_res_dict.get("users", [])


'''
Scenario: Update the status of a user to inactive
'''


@behave.given("A Admin wants deactivate a user")
def step_impl_1(context):
  #create group
  group_dict = {**TEST_USER_GROUP, "name": "assessor"}
  post_group = post_method(url=f"{UM_API_URL}/user-group/immutable", request_body=group_dict)
  post_group_data = post_group.json()
  assert post_group.status_code in [200, 409]
  if post_group.status_code == 200:
    context.group_uuid = post_group_data["data"]["uuid"]
  if post_group.status_code == 409:
    user_group = UserGroup.find_by_name(group_dict["name"])
    context.group_uuid = user_group.id

  #create user
  context.user_dict = deepcopy({
      **TEST_USER, "user_groups": [context.group_uuid], "user_type": "assessor"
  })
  context.user_dict["email"] = f"{uuid4()}@gmail.com"
  context.post_user_res = post_method(
      url=f"{UM_API_URL}/user", request_body=context.user_dict)
  assert context.post_user_res.status_code == 200
  post_user_res_dict = context.post_user_res.json()["data"]
  context.user_id = post_user_res_dict.get("user_id", "")
  context.url = f"{UM_API_URL}/user/{context.user_id}/status"


@behave.when("A API request to deactivate a user is sent to User management")
def step_impl_2(context):
  context.updated_user_res = put_method(
      url=context.url, request_body={"status": "inactive"})


@behave.then("the user should be deactivated")
def step_impl_3(context):
  assert context.updated_user_res.status_code == 200
  context.updated_user_res_dict = context.updated_user_res.json()["data"]
  assert context.updated_user_res_dict["status"] == "inactive"
  assert context.updated_user_res_dict["user_groups"] == []


@behave.then("the user should be removed from all the groups")
def step_impl_3(context):
  get_group_res = get_method(url=f"{UM_API_URL}/user-group/{context.group_uuid}")
  assert get_group_res.status_code == 200
  get_group_res_dict = get_group_res.json()["data"]
  assert not context.user_id in get_group_res_dict.get("users", [])
