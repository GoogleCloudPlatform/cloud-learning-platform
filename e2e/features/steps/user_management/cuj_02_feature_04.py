"""
Feature: Managing Immutable UserGroups in user management
"""
import behave
import sys
from uuid import uuid4

sys.path.append("../")
from test_object_schemas import TEST_USER, TEST_USER_GROUP
from test_config import (API_URL_USER_MANAGEMENT as UM_API_URL)
from setup import post_method, put_method, delete_method, get_method, create_immutable_user_groups
'''
Scenario: Update name of a Immutable UserGroup with correct request payload
'''

@behave.given("A user has permission to user management and wants to update name of a Immutable UserGroup")
def step_impl_1(context):    
  context.learner_user_group_uuid = create_immutable_user_groups("learner")


@behave.when("API request is sent to update Immutable UserGroup with correct request payload")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/user-group/{context.learner_user_group_uuid}"
  updated_data = {"name": "updated name"}
  context.res = put_method(url=context.url, request_body=updated_data)
  context.res_data = context.res.json()


@behave.then("UserGroup document will not be updated and user management service will throw a validation error")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False, "Success is Not False"
  assert context.res_data["message"] == f"Cannot update name of an immutable Usergroup with uuid:{context.learner_user_group_uuid}"


'''
Scenario: Add users to a Immutable UserGroup within User management
'''
@behave.given("A user has access to User management and needs to add users with comaptible user_type to a immutable UserGroup")
def step_impl_1(context):
    context.learner_user_group_uuid = create_immutable_user_groups("learner")

    user_dict = {**TEST_USER, "user_type":"learner", "email" : f"{uuid4()}@gmail.com"}
    post_user = post_method(
        url=f"{UM_API_URL}/user", request_body=user_dict)
    context.post_user_data = post_user.json()
    context.learner_user_id = context.post_user_data["data"]["user_id"]
    assert post_user.status_code == 200


@behave.when("API request is sent to add users with type learner to a immutable UserGroup with name learner")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/user-group/{context.learner_user_group_uuid}/users/add"
  context.res = post_method(
      url=context.url, request_body={"user_ids": [context.learner_user_id]})
  context.res_data = context.res.json()


@behave.then("The users are successfully added to the learner UserGroup")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not False"
  assert context.res_data["message"] == f"Successfully added users to user group"

'''
Scenario: Add users with incompatible user_type to a Immutable UserGroup within User management
'''
@behave.given("A user has access to User management and needs to add users with incompatible user_type to a immutable UserGroup")
def step_impl_1(context):
    context.learner_user_group_uuid = create_immutable_user_groups("learner")

    user_dict = {**TEST_USER, "user_type":"instructor", "email" : f"{uuid4()}@gmail.com"}
    post_user = post_method(
        url=f"{UM_API_URL}/user", request_body=user_dict)
    context.post_user_data = post_user.json()
    context.instructor_user_id = context.post_user_data["data"]["user_id"]
    assert post_user.status_code == 200


@behave.when("API request is sent to add users with user_type instructor to a immutable UserGroup with name learner")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/user-group/{context.learner_user_group_uuid}/users/add"
  context.res = post_method(
      url=context.url, request_body={"user_ids": [context.instructor_user_id]})
  context.res_data = context.res.json()


@behave.then("The users will not be added to UserGroup user management service will throw validation error")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False, "Success is not False"
  assert context.res_data["message"] == f"User with user_type instructor cannot be added to user group: learner"

'''
Scenario: A Immutable UserGroup cannot be deleted
'''

@behave.given("A user has access privileges to User management and wants to delete a immutable UserGroup")
def step_impl_1(context):
  context.learner_user_group_uuid = create_immutable_user_groups("learner")

@behave.when("API request is sent to delete UserGroup whose is_immutable field is true by providing uuid")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/user-group/{context.learner_user_group_uuid}"
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("UserGroup object will not be deleted and User management will throw a Validation error")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False, "Success is not False"
  assert context.res_data["message"] == f"Cannot delete an immutable Usergroup with uuid:{context.learner_user_group_uuid}"