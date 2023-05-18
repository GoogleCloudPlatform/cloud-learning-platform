"""
Feature: CRUD for managing UserGroup in user management
"""
import behave
import sys
from copy import deepcopy
from uuid import uuid4

sys.path.append("../")
from test_object_schemas import TEST_USER, TEST_USER_GROUP
from test_config import (API_URL_USER_MANAGEMENT as UM_API_URL)
from setup import post_method, get_method, put_method, delete_method
'''
Scenario: Create UserGroup with correct request payload
'''


@behave.given(
    "A user has permission to user management and wants to create a UserGroup")
def step_impl_1(context):

    context.group_dict = {**TEST_USER_GROUP, "name": f"{uuid4()}"}


@behave.when("API request is sent to create UserGroup with correct request payload")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/user-group"

  context.res = post_method(url=context.url, request_body=context.group_dict)
  context.res_data = context.res.json()


@behave.then("that UserGroup object will be created in the database")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["message"] == "Successfully created the user group"
  group_uuid = context.res_data["data"]["uuid"]
  url = f"{UM_API_URL}/user-group/{group_uuid}"
  request = get_method(url)
  group_data = request.json()
  assert request.status_code == 200
  assert group_data["message"] == "Successfully fetched the user group"
  assert group_data["data"]["name"] == context.group_dict["name"]


# --- Negative Scenario ---
@behave.given(
    "A user has permission to user management and wants to create a UserGroup with incorrect payload"
)
def step_impl_1(context):
  context.payload = {**TEST_USER_GROUP}
  del context.payload["name"]
  context.url = f"{UM_API_URL}/user-group"


@behave.when(
    "API request is sent to create UserGroup with incorrect request payload")
def step_impl_2(context):
    context.res = post_method(url=context.url, request_body=context.payload)
    context.res_data = context.res.json()


@behave.then(
    "that UserGroup object will not be created and a validation error is thrown")
def step_impl_3(context):
    assert context.res.status_code == 422
    context.res_data = context.res.json()
    assert context.res_data["success"] is False
    assert context.res_data["message"] == "Validation Failed"
    assert context.res_data["data"][0]["msg"] == "field required"
    assert context.res_data["data"][0]["type"] == "value_error.missing"


# -------------------------------GET GROUP-------------------------------------
# --- Positive Scenario ---
@behave.given(
    "A user has access privileges to User management and needs to fetch a UserGroup"
)
def step_impl_1(context):
    context.group_dict = {**TEST_USER_GROUP, "name": f"{uuid4()}"}

    post_group = post_method(
      url=f"{UM_API_URL}/user-group", request_body=context.group_dict)
    context.post_group_data = post_group.json()
    context.group_uuid = context.post_group_data["data"]["uuid"]
    assert post_group.status_code == 200


@behave.when("API request is sent to fetch UserGroup by providing correct uuid")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/user-group/{context.group_uuid}"
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then(
    "UserGroup object corresponding to given uuid will be returned successfully")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_data["success"] is True, "Success is not True"
    assert context.res_data["message"] == "Successfully fetched the user group"
    assert context.res_data["data"] == context.post_group_data["data"]


# --- Negative Scenario ---
@behave.given("A user has access to User management and needs to fetch a UserGroup")
def step_impl_1(context):
  invalid_group_uuid = "random_id"
  context.url = f"{UM_API_URL}/user-group/{invalid_group_uuid}"


@behave.when("API request is sent to fetch UserGroup by providing invalid uuid")
def step_impl_2(context):
    context.res = get_method(url=context.url)
    context.res_data = context.res.json()


@behave.then(
    "UserGroup object will not be returned and Resource not found error will be thrown by User management"
)
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False, "success not False"
  assert context.res_data[
      "message"] == "UserGroup with uuid random_id not found", "Expected message not returned"


# -------------------------------GET ALL GROUPS-----------------------------------
# --- Positive Scenario ---
@behave.given(
    "A user has access to User management and needs to fetch all UserGroups")
def step_impl_1(context):
    context.group_dict = {**TEST_USER_GROUP, "name": f"{uuid4()}"}

    post_group = post_method(
        url=f"{UM_API_URL}/user-group", request_body=context.group_dict)
    context.post_group_data = post_group.json()
    context.group_uuid = context.post_group_data["data"]["uuid"]
    assert post_group.status_code == 200
    context.url = f"{UM_API_URL}/user-groups"

@behave.when("API request is sent to fetch all UserGroups")
def step_impl_2(context):
    context.res = get_method(url=context.url)
    context.res_data = context.res.json()


@behave.then(
    "User management will return all existing UserGroup objects successfully")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_data["success"] is True, "Success is not True"
    assert context.res_data["message"] == "Successfully fetched user groups"
    fetched_uuids = [i.get("uuid") for i in context.res_data.get("data")["records"]]
    assert context.group_uuid in fetched_uuids


# --- Negative Scenario ---
@behave.given("A user can access User management and needs to fetch all UserGroups")
def step_impl_1(context):
  context.url = f"{UM_API_URL}/user-groups"
  context.params = params = {"skip": "-1", "limit": "10"}


@behave.when(
    "API request is sent to fetch all UserGroups with incorrect request payload")
def step_impl_2(context):
    context.res = get_method(url=context.url, query_params=context.params)
    context.res_data = context.res.json()


@behave.then(
    "The UserGroups will not be fetched and User management will throw a Validation error"
)
def step_impl_3(context):
  assert context.res.status_code == 422, "Status not 422"
  assert context.res_data.get("message") == \
    "Validation Failed", \
    "unknown response received"


# -------------------------------UPDATE GROUP-------------------------------------
# --- Positive Scenario ---
@behave.given("A user has access to User management and needs to update a UserGroup"
              )
def step_impl_1(context):
    context.group_dict = {**TEST_USER_GROUP, "name": f"{uuid4()}"}
    post_group = post_method(
        url=f"{UM_API_URL}/user-group", request_body=context.group_dict)
    context.post_group_data = post_group.json()
    context.group_uuid = context.post_group_data["data"]["uuid"]
    assert post_group.status_code == 200


@behave.when("API request is sent to update UserGroup with correct request payload")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/user-group/{context.group_uuid}"
  updated_data = {"description": "updated description"}
  context.res = put_method(url=context.url, request_body=updated_data)
  context.res_data = context.res.json()


@behave.then("UserGroup object will be updated successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully updated the user group"
  assert context.res_data["data"]["description"] == "updated description"





# --- Negative Scenario ---
@behave.given(
    "A user has access privileges to User management and needs to update a UserGroup"
)
def step_impl_1(context):
  invalid_group_uuid = "random_id"
  context.url = f"{UM_API_URL}/user-group/{invalid_group_uuid}"
  context.payload = {}


@behave.when("API request is sent to update UserGroup by providing invalid uuid")
def step_impl_2(context):
    context.res = put_method(url=context.url, request_body=context.payload)
    context.res_data = context.res.json()


@behave.then(
    "UserGroup object will not be updated and User management will throw a resource not found error"
)
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "UserGroup with uuid random_id not found"


# -------------------------------DELETE GROUP-------------------------------------
# --- Positive Scenario ---
@behave.given("A user has access to User management and needs to delete a UserGroup")
def step_impl_1(context):
  context.group_dict = {
      **TEST_USER_GROUP, "name": f"{uuid4()}"
  }

  post_group = post_method(
      url=f"{UM_API_URL}/user-group", request_body=context.group_dict)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

  user_dict = deepcopy({**TEST_USER})
  user_dict["email"] = f"{uuid4()}@gmail.com"
  user_dict["user_type"] = "instructor"
  post_user_url = f"{UM_API_URL}/user"
  post_user_res = post_method(url=post_user_url, request_body=user_dict)
  assert post_user_res.status_code == 200
  context.user_id = post_user_res.json()["data"]["user_id"]

  update_user_dict = {"user_groups": [context.group_uuid]}
  put_user_res = put_method(url=f"{UM_API_URL}/user/{context.user_id}", request_body=update_user_dict)
  assert put_user_res.status_code == 200



@behave.when("API request is sent to delete UserGroup by providing correct uuid")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/user-group/{context.group_uuid}"
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("UserGroup object will be deleted successfully")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_data["success"] is True, "Success is not True"
    assert context.res_data["message"] == "Successfully deleted the user group"


@behave.then("And the deleted UserGroup is unassigned from all the users and permissions")
def step_impl_3(context):
    get_user_res = get_method(url=f"{UM_API_URL}/user/{context.user_id}")
    get_user_res_data = get_user_res.json()
    assert get_user_res.status_code == 200
    assert get_user_res_data["data"]["user_groups"] == []


# --- Negative Scenario ---
@behave.given(
    "A user has access privileges to User management and needs to delete a UserGroup"
)
def step_impl_1(context):
  invalid_group_uuid = "random_id"
  context.url = f"{UM_API_URL}/user-group/{invalid_group_uuid}"


@behave.when("API request is sent to delete UserGroup by providing invalid uuid")
def step_impl_2(context):
    context.res = delete_method(url=context.url)
    context.res_data = context.res.json()


@behave.then(
    "UserGroup object will not be deleted and User management will throw a resource not found error"
)
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "UserGroup with uuid random_id not found"


# -------------------------------ADD USERS TO GROUP-------------------------------------
# --- Positive Scenario ---
@behave.given(
    "A user has access to User management and needs to add users to UserGroup")
def step_impl_1(context):
  user_dict = deepcopy(TEST_USER)
  user_dict["email"] = f"{uuid4()}@gmail.com"
  user_dict["user_type"] = "learner"
  post_user_url = f"{UM_API_URL}/user"
  post_user_res = post_method(url=post_user_url, request_body=user_dict)
  assert post_user_res.status_code == 200
  context.user_id = post_user_res.json()["data"]["user_id"]
  context.group_dict = {**TEST_USER_GROUP, "name": f"{uuid4()}"}

  post_group = post_method(
      url=f"{UM_API_URL}/user-group", request_body=context.group_dict)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200


@behave.when("API request is sent to add users to UserGroup")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/user-group/{context.group_uuid}/users/add"
  context.res = post_method(
      url=context.url, request_body={"user_ids": [context.user_id]})
  context.res_data = context.res.json()


@behave.then("The users are added to UserGroup")
def step_impl_3(context):

    assert context.res.status_code == 200
    assert context.res_data["success"] is True, "Success is not True"
    assert context.res_data["message"] == "Successfully added users to user group"
    assert context.res_data["data"]["users"] == [context.user_id]


@behave.then("the UserGroup is assigned to the users in request")
def step_impl_3(context):
    get_user_res = get_method(url=f"{UM_API_URL}/user/{context.user_id}")
    get_user_res_data = get_user_res.json()
    assert get_user_res.status_code == 200
    assert get_user_res_data["data"]["user_groups"] == [context.group_uuid]


# -------------------------------REMOVES USERS FROM GROUP-------------------------------------
# --- Positive Scenario ---
@behave.given(
    "A user has access to User management and needs to remove users from UserGroup")
def step_impl_1(context):
  user_dict = deepcopy(TEST_USER)
  user_dict["email"] = f"{uuid4()}@gmail.com"
  user_dict["user_type"] = "learner"
  post_user_url = f"{UM_API_URL}/user"
  post_user_res = post_method(url=post_user_url, request_body=user_dict)
  assert post_user_res.status_code == 200
  context.user_id = post_user_res.json()["data"]["user_id"]
  context.group_dict = {
      **TEST_USER_GROUP, "name": f"{uuid4()}"
  }

  post_group = post_method(
      url=f"{UM_API_URL}/user-group", request_body=context.group_dict)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

  updated_user_data = {"user_groups": [context.group_uuid]}
  update_user = put_method(
      url=f"{UM_API_URL}/user/{context.user_id}",
      request_body=updated_user_data)
  print(update_user.json())
  assert update_user.status_code == 200


@behave.when("API request is sent to remove users to UserGroup")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/user-group/{context.group_uuid}/user/remove"
  context.res = post_method(
      url=context.url, request_body={"user_id": context.user_id})
  context.res_data = context.res.json()


@behave.then("The users are removed from the UserGroup")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_data["success"] is True, "Success is not True"
    assert context.res_data[
        "message"] == "Successfully removed user from user group"
    assert context.res_data["data"]["users"] == []


@behave.then("the UserGroup is unassigned from the users in request")
def step_impl_3(context):
  get_user_res = get_method(url=f"{UM_API_URL}/user/{context.user_id}")
  get_user_res_data = get_user_res.json()
  assert get_user_res.status_code == 200
  assert get_user_res_data["data"]["user_groups"] == []

#-------------------------------SEARCH GROUP-------------------------------------
# --- Positive Scenario ---
@behave.given(
    "A user has access privileges to User management and needs to search for a UserGroup"
)
def step_impl_1(context):
  context.group_dict = {**TEST_USER_GROUP,  "name": f"{uuid4()}"}

  post_group = post_method(
      url=f"{UM_API_URL}/user-group", request_body=context.group_dict)
  context.post_group_data = post_group.json()
  assert post_group.status_code == 200


@behave.when("API request is sent to search UserGroup by providing correct name")
def step_impl_2(context):
  context.query_params = {
    "name": context.group_dict['name']
  }
  context.url = f"{UM_API_URL}/user-group/search"
  context.res = get_method(url=context.url, query_params=context.query_params)
  context.res_data = context.res.json()


@behave.then(
    "UserGroups corresponding to given name will be returned successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is True"
  assert context.res_data["message"] == "Successfully fetched the user group"
  assert context.res_data["data"][0]["name"] == context.post_group_data["data"]["name"]

# --- Negative Scenario ---
@behave.given(
    "A user has access to User management and needs to search for a UserGroup"
)
def step_impl_1(context):
  context.group_dict = {**TEST_USER_GROUP, "name": f"{uuid4()}"}

  post_group = post_method(
      url=f"{UM_API_URL}/user-group", request_body=context.group_dict)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200


@behave.when("API request is sent to search UserGroup by providing invalid name")
def step_impl_2(context):
  context.query_params = {
    "name": 1
  }
  context.url = f"{UM_API_URL}/user-group/search"
  context.res = get_method(url=context.url, query_params=context.query_params)
  context.res_data = context.res.json()


@behave.then(
    "An empty list would be returned for the search")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"] == []


#-------------------------------FETCH USERS FOR USERGROUP-------------------------------------
# --- Positive Scenario ---
@behave.given("A user has access to User management and needs to retrieve users that can be added to a UserGroup")
def step_impl_1(context):
  # create user
  user_dict = deepcopy(TEST_USER)
  user_dict["email"] = f"{uuid4()}@gmail.com"
  user_dict["user_type"] = "learner"
  post_user_url = f"{UM_API_URL}/user"
  post_user_res = post_method(url=post_user_url, request_body=user_dict)
  print("User Data")
  print(post_user_res.json().get("data"))
  assert post_user_res.status_code == 200

  # create user group
  context.group_dict = {**TEST_USER_GROUP,  "name": f"{uuid4()}"}
  post_group = post_method(
      url=f"{UM_API_URL}/user-group", request_body=context.group_dict)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  print("User Group Data")
  print(context.post_group_data)
  assert post_group.status_code == 200


@behave.when("API request is sent to fetch users by providing valid UserGroup uuid")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/user-group/{context.group_uuid}/addable-users"
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("List of users that can be added to provided UserGroup will be returned")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["message"] == "Successfully fetched users that can be added to user group"


# --- Negative Scenario ---
@behave.given("A user has access to User management and needs to retrieve users that can be added to a UserGroup which does not exist")
def step_impl_1(context):
  context.group_dict = {**TEST_USER_GROUP, "name": f"{uuid4()}"}

  post_group = post_method(
      url=f"{UM_API_URL}/user-group", request_body=context.group_dict)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200


@behave.when("API request is sent to fetch users by providing invalid UserGroup uuid")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/user-group/random_id/addable-users"
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Resource not Found error will be thrown for providing invalid UserGroup uuid")
def step_impl_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "UserGroup with uuid random_id not found"
  assert context.res_data["data"] is None
