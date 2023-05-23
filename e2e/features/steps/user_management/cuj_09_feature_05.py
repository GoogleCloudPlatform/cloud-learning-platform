"""
Feature: CRUD for managing Association Group in user management
"""
import behave
import sys
from copy import deepcopy
from uuid import uuid4

sys.path.append("../")
from e2e.test_object_schemas import TEST_ASSOCIATION_GROUP, TEST_USER
from e2e.test_config import API_URL_USER_MANAGEMENT
from e2e.setup import post_method, get_method, put_method, delete_method

UM_API_URL = f"{API_URL_USER_MANAGEMENT}"

#-------------------------------GET ASSOCIATION-GROUP------------------------------------
# --- Positive Scenario ---
# fix limit - update limit to 30 post alpha
@behave.given("A user has access to User management and needs to search Association Group")
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Association Group - {uuid4()}"

  context.payload = association_group_dict
  context.name = association_group_dict["name"]

  post_group = post_method(
      url=f"{UM_API_URL}/association-groups/discipline-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  context.association_group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200


@behave.when("API request is sent to fetch Association Group by providing valid name")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/association-groups/search"
  params = {"search_query": context.name}
  context.res = get_method(url=context.url, query_params=params)
  context.res_data = context.res.json()


@behave.then("A list of Association Group objects corresponding to given name will be returned")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully fetched the association group"
  assert context.res_data[
     "data"]["records"][0]["name"] == context.name


# --- Negative Scenario---
@behave.given("A user has access to User management and needs to fetch a Association Group")
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/association-groups/discipline-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  context.association_group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

@behave.when("API request is sent to fetch Association Group by providing invalid name")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/association-groups/search"
  params = {"search_query": "example"}
  context.res = get_method(url=context.url, query_params=params)
  context.res_data = context.res.json()


@behave.then("An empty list will be returned for the search")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully fetched the association group"
  assert context.res_data["data"]["records"] == []


# --- Fetch Association Groups from User management by searching with empty search_query--
@behave.given("A user has access to User management and wants to search Association Group")
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/association-groups/discipline-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  context.association_group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

@behave.when("API request is sent to fetch Association Group by providing empty search_query")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/association-groups/search"
  params = {"search_query": ""}
  context.res = get_method(url=context.url, query_params=params)
  context.res_data = context.res.json()


@behave.then("A ValidationError will be thrown")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False, "Success is not False"
  assert context.res_data["message"] == "search_query cannot be empty"


# --- Get Association Group with correct request payload--
@behave.given("A user has permission to user management and wants to retrieve Association Group")
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Association Group - {uuid4()}"
  context.payload = association_group_dict
  post_group = post_method(
      url=f"{UM_API_URL}/association-groups/discipline-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  assert post_group.status_code == 200


@behave.when("API request is sent to retrieve Association Group with correct request payload")
def step_impl_2(context):
  context.url = f"{UM_API_URL}"
  params = {"skip": 0, "limit": 10}
  context.res = get_method(url=context.url, query_params=params)
  context.res_data = context.res.json()


@behave.then("A list of Association Group will be retrieved from the database as per given request payload")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully fetched the association groups"

# ---Get Association Group with incorrect request payload---
@behave.given("A user has permission to user management and wants to fetch Association Group")
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/association-groups/discipline-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  context.association_group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

@behave.when("API request is sent to retrieve Association Group with incorrect request payload")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/association-groups"
  params = {"skip": -1, "limit": 10}
  context.res = get_method(url=context.url, query_params=params)
  context.res_data = context.res.json()


@behave.then("A list of Association Group will be not retrieved and a validation error is thrown")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False, "Success is not True"
  assert context.res_data["message"] == "Validation Failed"

'''
Scenario: Retrieve Users addable to an assocation group for a given user type
'''
@behave.given("A user has access to fetch users for a given user type")
def step_impl_1(context):
    user_dict = deepcopy(TEST_USER)
    user_dict["email"] = f"{uuid4()}@gmail.com"
    user_dict["user_type"] = "coach"

    post_user_url = f"{UM_API_URL}/user"
    post_user_res = post_method(
        url= post_user_url,
        request_body= user_dict
    )

    assert post_user_res.status_code == 200
    context.uuid = post_user_res.json()["data"]["user_id"]

    # create an learner association group
    association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
    association_group_dict["name"] = str(uuid4())
    association_request_body = association_group_dict
    association_url = f"{UM_API_URL}/association-groups/learner-association"
    association_res = post_method(url=association_url, request_body=association_request_body)
    association_res_data = association_res.json()
    assert association_res.status_code == 200
    context.association_uuid = association_res_data["data"]["uuid"]


@behave.when("A GET api call is made to the User Management Service to fetch users")
def step_impl_2(context):
    get_user_url = f"{UM_API_URL}/association-groups/{context.association_uuid}/addable-users"
    context.get_user_res = get_method(url= get_user_url,
        query_params={"user_type":"coach"})

@behave.then("A list of users for the given user type is returned")
def step_impl_3(context):
    assert context.get_user_res.status_code == 200

'''
Scenario: Retrieve Users for type learner which are already associated with learner assocation groups
'''
@behave.given("A user has access to to fetch users of type learner which are already associated with learner assocation groups")
def step_impl_1(context):
    user_dict = deepcopy(TEST_USER)
    user_dict["email"] = f"{uuid4()}@gmail.com"
    user_dict["user_type"] = "learner"

    post_user_url = f"{UM_API_URL}/user"
    post_user_res = post_method(
        url= post_user_url,
        request_body= user_dict
    )

    assert post_user_res.status_code == 200
    context.uuid = post_user_res.json()["data"]["user_id"]

    association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
    association_group_dict["name"] = str(uuid4())
    association_request_body = association_group_dict
    association_url = f"{UM_API_URL}/association-groups/learner-association"
    association_res = post_method(url=association_url, request_body=association_request_body)
    association_res_data = association_res.json()
    assert association_res.status_code == 200
    context.association_uuid = association_res_data["data"]["uuid"]

    association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
    association_group_dict["name"] = str(uuid4())
    association_request_body = association_group_dict
    association_url = f"{UM_API_URL}/association-groups/learner-association"
    association_res = post_method(url=association_url, request_body=association_request_body)
    association_res_data = association_res.json()
    assert association_res.status_code == 200
    association_uuid_with_user = association_res_data["data"]["uuid"]

    add_users = {"users": [context.uuid], "status": "active"}
    context.url = f"{UM_API_URL}/association-groups/learner-association/{association_uuid_with_user}/users/add"
    context.res = post_method(url=context.url, request_body=add_users)
    assert context.res.status_code == 200

@behave.when("A GET api call is made to the User Management Service to fetch users of type learner")
def step_impl_2(context):
    get_user_url = f"{UM_API_URL}/association-groups/{context.association_uuid}/addable-users"
    context.get_user_res = get_method(url= get_user_url,
        query_params={"user_type":"coach"})

@behave.then("A empty list of users for user type learner is returned")
def step_impl_3(context):
    assert context.get_user_res.status_code == 200
    assert  context.uuid not in context.get_user_res.json()["data"]
