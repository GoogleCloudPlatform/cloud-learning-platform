"""
Feature: A user with appropriate permissions wants to get user account details
"""
import behave
import sys
from copy import deepcopy
from uuid import uuid4

sys.path.append("../")
from e2e.test_object_schemas import TEST_USER

from e2e.test_config import (API_URL_USER_MANAGEMENT,
                        API_URL_LEARNER_PROFILE_SERVICE,
                        API_URL_LEARNING_RECORD_SERVICE)
from e2e.setup import post_method, get_method

UM_API_URL = API_URL_USER_MANAGEMENT
LRS_API_URL = API_URL_LEARNING_RECORD_SERVICE
SLP_API_URL = API_URL_LEARNER_PROFILE_SERVICE

'''
Scenario: User information is to be fetched for a single user with correct uuid
'''


@behave.given("Required User already exists in the database and correct uuid "
              "will be used to find user")
def step_impl_1(context):
  user_dict = deepcopy(TEST_USER)
  user_dict["user_type"] = "learner"
  user_dict["email"] = f"{uuid4()}@gmail.com"

  post_user_url = f"{UM_API_URL}/user"
  post_user_res = post_method(
    url=post_user_url,
    request_body=user_dict
  )

  assert post_user_res.status_code == 200
  context.uuid = post_user_res.json()["data"]["user_id"]


@behave.when(
  "A GET api call is made to the User Management Service with correct uuid")
def step_impl_2(context):
  get_user_url = f"{UM_API_URL}/user/{context.uuid}"
  context.get_user_res = get_method(url=get_user_url)


@behave.then("The User data is correctly fetched")
def step_impl_3(context):
  assert context.get_user_res.status_code == 200
  assert context.get_user_res.json()["data"]["user_id"] == context.uuid


'''
Scenario: User information is to be fetched for a single user with incorrect uuid
'''


@behave.given("Required User does not exists in the database and incorrect "
              "uuid will be used to find the user")
def step_impl_1(context):
  context.uuid = "some_random_uuid"
  context.get_user_url = f"{UM_API_URL}/user/{context.uuid}"


@behave.when(
  "A GET api call is made to the User Management Service with incorrect uuid")
def step_impl_2(context):
  context.get_user_res = get_method(url=context.get_user_url)


@behave.then("The User Not Found error response is returned")
def step_impl_3(context):
  assert context.get_user_res.status_code == 404
  assert context.get_user_res.json()[
           "message"] == f"User with user_id {context.uuid} not found"


'''
Scenario: User information is to be searched with user email
'''


@behave.given("Required User already exists in the database and correct email "
              "address will be used for query")
def step_impl_1(context):
  context.email = f"{uuid4()}@gmail.com"

  user_dict = deepcopy(TEST_USER)
  user_dict["email"] = context.email

  post_user_url = f"{UM_API_URL}/user"
  post_user_res = post_method(
    url=post_user_url,
    request_body=user_dict
  )

  assert post_user_res.status_code == 200
  context.uuid = post_user_res.json()["data"]["user_id"]


@behave.when(
  "A GET api call is made to the User Management Service with correct email")
def step_impl_2(context):
  get_user_url = f"{UM_API_URL}/user/search/email"
  context.get_user_res = get_method(url=get_user_url,
                                    query_params={"email": context.email})


@behave.then("A list of matching users is returned")
def step_impl_3(context):
  assert context.get_user_res.status_code == 200
  assert context.get_user_res.json()["data"][0]["email"] == context.email


@behave.given("Required User already exists in the database and incorrect "
              "email address will be used for query")
def step_impl_1(context):
  context.get_user_url = f"{UM_API_URL}/user/search/email"
  context.query_params = {"email": "test.email"}


@behave.when("A GET api call is made to the User Management Service with "
             "incorrect email")
def step_impl_2(context):
  context.get_user_res = get_method(url=context.get_user_url,
                                    query_params=context.query_params)


@behave.then("Invalid email error response raised")
def step_impl_3(context):
  assert context.get_user_res.status_code == 422
  assert context.get_user_res.json()["success"] is False
  assert context.get_user_res.json()["data"] is None


'''
Scenario: User information is to be fetched for all users
'''


@behave.given("Users already exist in the database")
def step_impl_1(context):
  user_dict = deepcopy(TEST_USER)
  user_dict["email"] = f"{uuid4()}@gmail.com"

  post_user_url = f"{UM_API_URL}/user"
  post_user_res = post_method(
    url=post_user_url,
    request_body=user_dict
  )
  assert post_user_res.status_code == 200
  context.uuid = post_user_res.json()["data"]["user_id"]


@behave.when(
  "A GET api call is made to the User Management Service to fetch all")
def step_impl_2(context):
  get_user_url = f"{UM_API_URL}/users"
  context.get_user_res = get_method(url=get_user_url)


@behave.then("A list of users is returned")
def step_impl_3(context):
  assert context.get_user_res.status_code == 200
  assert len(context.get_user_res.json()["data"]["records"]) > 0


'''
Scenario: User information is to be searched for the given filter
'''


@behave.given("A user has access to User management and needs to fetch users")
def step_impl_1(context):
  context.email = f"{uuid4()}@gmail.com"

  user_dict = deepcopy(TEST_USER)
  user_dict["email"] = context.email
  context.firstname = user_dict["first_name"]

  post_user_url = f"{UM_API_URL}/user"
  post_user_res = post_method(
    url=post_user_url,
    request_body=user_dict
  )
  assert post_user_res.status_code == 200
  context.uuid = post_user_res.json()["data"]["user_id"]


@behave.when("API request is sent to fetch users along with a filter")
def step_impl_2(context):
  get_user_url = f"{UM_API_URL}/user/search"
  context.get_user_res = get_method(url=get_user_url,
                                    query_params={
                                      "search_query": context.firstname})


@behave.then(
  "User management will successfully return users for the given filter")
def step_impl_3(context):
  assert context.get_user_res.status_code == 200
  assert context.get_user_res.json()["data"][0][
           "first_name"] == context.firstname


@behave.given("A user has access to User management and needs to fetch users "
              "on a specific sort order by email")
def step_impl_1(context):
  context.email = f"{uuid4()}@gmail.com"

  user_dict = deepcopy(TEST_USER)
  user_dict["email"] = context.email
  context.firstname = user_dict["first_name"]

  post_user_url = f"{UM_API_URL}/user"
  post_user_res = post_method(
    url=post_user_url,
    request_body=user_dict
  )
  assert post_user_res.status_code == 200
  context.uuid = post_user_res.json()["data"]["user_id"]


@behave.when(
  "API request is sent to fetch users along with a sort order by email")
def step_impl_2(context):
  get_user_url = f"{UM_API_URL}/users"
  context.get_user_res = get_method(url=get_user_url,
                                    query_params={"sort_by": "email"})


@behave.then("User management will successfully return users for the given "
             "sort order by email")
def step_impl_3(context):
  assert context.get_user_res.status_code == 200


@behave.given("A user has access to User management and needs to fetch users "
              "on a specific firstname sort order")
def step_impl_1(context):
  context.email = f"{uuid4()}@gmail.com"

  user_dict = deepcopy(TEST_USER)
  user_dict["email"] = context.email
  context.firstname = user_dict["first_name"]

  post_user_url = f"{UM_API_URL}/user"
  post_user_res = post_method(
    url=post_user_url,
    request_body=user_dict
  )
  assert post_user_res.status_code == 200
  context.uuid = post_user_res.json()["data"]["user_id"]


@behave.when("API request is sent to fetch users along with a sort order "
             "by firstname")
def step_impl_2(context):
  get_user_url = f"{UM_API_URL}/users"
  context.get_user_res = get_method(url=get_user_url,
                                    query_params={"sort_by": "first_name"})


@behave.then("User management will successfully return users for the given "
             "sort order by firstname")
def step_impl_3(context):
  assert context.get_user_res.status_code == 200


@behave.given("A user has access to User management and needs to fetch users "
              "on a specific lastname sort order")
def step_impl_1(context):
  context.email = f"{uuid4()}@gmail.com"

  user_dict = deepcopy(TEST_USER)
  user_dict["email"] = context.email
  context.firstname = user_dict["first_name"]

  post_user_url = f"{UM_API_URL}/user"
  post_user_res = post_method(
    url=post_user_url,
    request_body=user_dict
  )
  assert post_user_res.status_code == 200
  context.uuid = post_user_res.json()["data"]["user_id"]


@behave.when(
    "API request is sent to fetch users along with a sort order by lastname")
def step_impl_2(context):
  get_user_url = f"{UM_API_URL}/users"
  context.get_user_res = get_method(url=get_user_url,
                                    query_params={"sort_by": "last_name"})


@behave.then("User management will successfully return users for the given "
             "sort order by lastname")
def step_impl_3(context):
  assert context.get_user_res.status_code == 200


@behave.given("A user has access to User management and needs to fetch users "
              "on a specific sort order by email in ascending")
def step_impl_1(context):
  context.email = f"{uuid4()}@gmail.com"

  user_dict = deepcopy(TEST_USER)
  user_dict["email"] = context.email
  context.firstname = user_dict["first_name"]

  post_user_url = f"{UM_API_URL}/user"
  post_user_res = post_method(
    url=post_user_url,
    request_body=user_dict
  )
  assert post_user_res.status_code == 200
  context.uuid = post_user_res.json()["data"]["user_id"]


@behave.when("API request is sent to fetch users along with a sort order by "
             "email in ascending")
def step_impl_2(context):
  get_user_url = f"{UM_API_URL}/users"
  context.get_user_res = get_method(url=get_user_url,
                                    query_params={"sort_by": "email",
                                                  "sort_order": "ascending"})


@behave.then("User management will successfully return users for the given "
             "sort order by email in ascending")
def step_impl_3(context):
  assert context.get_user_res.status_code == 200


@behave.given("A user has access to User management and needs to fetch users "
              "on a specific firstname sort order in ascending")
def step_impl_1(context):
  context.email = f"{uuid4()}@gmail.com"

  user_dict = deepcopy(TEST_USER)
  user_dict["email"] = context.email
  context.firstname = user_dict["first_name"]

  post_user_url = f"{UM_API_URL}/user"
  post_user_res = post_method(
    url=post_user_url,
    request_body=user_dict
  )
  assert post_user_res.status_code == 200
  context.uuid = post_user_res.json()["data"]["user_id"]


@behave.when("API request is sent to fetch users along with a sort order by "
             "firstname in ascending")
def step_impl_2(context):
  get_user_url = f"{UM_API_URL}/users"
  context.get_user_res = get_method(url=get_user_url,
                                    query_params={"sort_by": "first_name",
                                                  "sort_order": "ascending"})


@behave.then("User management will successfully return users for the given "
             "sort order by firstname in ascending")
def step_impl_3(context):
  assert context.get_user_res.status_code == 200


@behave.given("A user has access to User management and needs to fetch users "
              "on a specific lastname sort order in ascending")
def step_impl_1(context):
  context.email = f"{uuid4()}@gmail.com"

  user_dict = deepcopy(TEST_USER)
  user_dict["email"] = context.email
  context.firstname = user_dict["first_name"]

  post_user_url = f"{UM_API_URL}/user"
  post_user_res = post_method(
    url=post_user_url,
    request_body=user_dict
  )
  assert post_user_res.status_code == 200
  context.uuid = post_user_res.json()["data"]["user_id"]


@behave.when("API request is sent to fetch users along with a sort order by "
             "lastname in ascending")
def step_impl_2(context):
  get_user_url = f"{UM_API_URL}/users"
  context.get_user_res = get_method(url=get_user_url,
                                    query_params={"sort_by": "last_name",
                                                  "sort_order": "ascending"})


@behave.then("User management will successfully return users for the given "
             "sort order by lastname in ascending")
def step_impl_3(context):
  assert context.get_user_res.status_code == 200
