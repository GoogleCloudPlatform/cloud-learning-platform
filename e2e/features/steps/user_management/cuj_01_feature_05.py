"""
Feature: CRUD on Inspace User alongwith backend user
"""
import behave
import sys
from copy import deepcopy
from uuid import uuid4

sys.path.append("../")
from e2e.test_object_schemas import TEST_USER
from e2e.test_config import API_URL_USER_MANAGEMENT as UM_API_URL
from common.models import User
from common.utils.inspace import (get_inspace_user_helper,delete_inspace_user_helper)
from e2e.setup import post_method, put_method, delete_method, set_cache, get_cache

# -----------------------------------------------------
# Scenario 1: An Inspace User account is to be created alongwith backend user
# -----------------------------------------------------
@behave.given("A user has access to the application and enters valid details for user creation")
def step_impl_1(context):
  context.user_dict = deepcopy(TEST_USER)
  context.user_dict["email"] = f"{uuid4()}@gmail.com"
  context.query_params = {"create_inspace_user": True}

@behave.when("An api call is made to the User Management Service with correct details for user creation")
def step_impl_2(context):
  url = f"{UM_API_URL}/user"
  post_user_res = post_method(
      url, request_body=context.user_dict, query_params=context.query_params)
  context.status_code = post_user_res.status_code
  context.post_user_res_json = post_user_res.json()

@behave.then("The User will be successfully created alongwith Inspace User")
def step_impl_3(context):
  assert context.status_code == 200
  assert context.post_user_res_json.get("success") == True
  assert context.post_user_res_json.get("data")["inspace_user"]["is_inspace_user"] == True
  assert context.post_user_res_json.get("data")["inspace_user"]["inspace_user_id"] != ""
  assert context.post_user_res_json.get("message") == "Successfully created new User, "\
                                                "corresponding agent and Inspace User"
  
  # Clean up inspace user
  user = User.find_by_uuid(context.post_user_res_json.get("data")["user_id"])
  result = delete_inspace_user_helper(user)
  assert result is True

# -----------------------------------------------------
# Scenario 2: No Inspace User account is to be created alongwith backend user
# -----------------------------------------------------
@behave.given("A user has access to the application and enters valid details for only backend user creation")
def step_impl_1(context):
  context.user_dict = deepcopy(TEST_USER)
  context.user_dict["email"] = f"{uuid4()}@gmail.com"


@behave.when("An api call is made to the User Management Service with correct details for backend user creation")
def step_impl_2(context):
  url = f"{UM_API_URL}/user"
  post_user_res = post_method(
      url, request_body=context.user_dict)
  context.status_code = post_user_res.status_code
  context.post_user_res_json = post_user_res.json()


@behave.then("The backend User will be successfully created")
def step_impl_3(context):
  assert context.status_code == 200
  assert context.post_user_res_json.get("success") == True
  assert context.post_user_res_json.get("data")["inspace_user"]["is_inspace_user"] == False
  assert context.post_user_res_json.get("data")["inspace_user"]["inspace_user_id"] == ""
  assert context.post_user_res_json.get("message") == "Successfully created User and corresponding agent"

# -----------------------------------------------------
# Scenario 3: An Inspace User info is to be updated along with backend user
# -----------------------------------------------------
@behave.given("A user has access to the application and enters valid details for user updation")
def step_impl_1(context):
  context.user_dict = deepcopy(TEST_USER)
  context.user_dict["email"] = f"{uuid4()}@gmail.com"
  context.query_params = {"create_inspace_user": True}

  url = f"{UM_API_URL}/user"
  post_user_res = post_method(
      url, request_body=context.user_dict, query_params=context.query_params)
  context.status_code = post_user_res.status_code
  context.post_user_res_json = post_user_res.json()

  assert context.post_user_res_json.get("success") == True
  assert context.post_user_res_json.get("data")["inspace_user"]["is_inspace_user"] == True
  assert context.post_user_res_json.get("data")["inspace_user"]["inspace_user_id"] != ""
  assert context.post_user_res_json.get("message") == "Successfully created new User, "\
                                                "corresponding agent and Inspace User"

  assert context.status_code == 200

  context.user_id = context.post_user_res_json.get("data")["user_id"]

  # Inspace API call
  user = User.find_by_uuid(context.user_id)
  status_code, inspace_user_res = get_inspace_user_helper(user)
  assert status_code == 200
  assert inspace_user_res["inspaceUser"]["firstName"] == user.first_name
  assert inspace_user_res["inspaceUser"]["lastName"] == user.last_name

@behave.when("An api call is made to the User Management Service with correct details for user updation")
def step_impl_2(context):
  url = f"{UM_API_URL}/user/{context.user_id}"

  context.request_body = {
    "first_name": "updated fname",
    "last_name": "updated lname"
  }
  query_params = {
    "update_inspace_user": True
  }
  context.res = put_method(url= url,request_body=context.request_body,query_params=query_params)
  context.res_json = context.res.json()

@behave.then("The User will be successfully updated alongwith Inspace User")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_json["success"] == True
  assert context.res_json["message"] == "Successfully updated the user and corresponding Inspace user"
  assert context.res_json["data"]["first_name"] == context.request_body["first_name"]
  assert context.res_json["data"]["last_name"] == context.request_body["last_name"]

  # Inspace API call
  user = User.find_by_uuid(context.user_id)
  status_code, inspace_user_res = get_inspace_user_helper(user)
  assert status_code == 200
  assert inspace_user_res["inspaceUser"]["firstName"] == context.request_body["first_name"]
  assert inspace_user_res["inspaceUser"]["lastName"] == context.request_body["last_name"]

  # Clean up inspace user
  user = User.find_by_uuid(context.user_id)
  result = delete_inspace_user_helper(user)
  assert result is True

# -----------------------------------------------------
# Scenario 4: An Inspace User info is to be deleted along with backend user
# -----------------------------------------------------
@behave.given("A user has access to the application and enters valid details for user deletion")
def step_impl_1(context):
  context.user_dict = deepcopy(TEST_USER)
  context.user_dict["email"] = f"{uuid4()}@gmail.com"
  context.query_params = {"create_inspace_user": True}

  url = f"{UM_API_URL}/user"
  post_user_res = post_method(
      url, request_body=context.user_dict, query_params=context.query_params)
  context.status_code = post_user_res.status_code
  context.post_user_res_json = post_user_res.json()

  assert context.post_user_res_json.get("success") == True
  assert context.post_user_res_json.get("data")["inspace_user"]["is_inspace_user"] == True
  assert context.post_user_res_json.get("data")["inspace_user"]["inspace_user_id"] != ""
  assert context.post_user_res_json.get("message") == "Successfully created new User, "\
                                                "corresponding agent and Inspace User"

  assert context.status_code == 200

  context.user_id = context.post_user_res_json.get("data")["user_id"]

  # Inspace API call
  user = User.find_by_uuid(context.user_id)
  status_code, inspace_user_res = get_inspace_user_helper(user)
  assert status_code == 200

@behave.when("An api call is made to the User Management Service with correct details for user deletion")
def step_impl_2(context):
  url = f"{UM_API_URL}/user/{context.user_id}"

  query_params = {
    "delete_inspace_user": True
  }
  context.res = delete_method(url= url,query_params=query_params)
  context.res_json = context.res.json()

@behave.then("The User will be successfully deleted alongwith Inspace User")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_json["success"] == True
  assert context.res_json["message"] == "Successfully deleted the user and associated agent, learner/faculty and Inspace User"

# -----------------------------------------------------
# Scenario 5: An Inspace User info is to be updated along with backend user but Inspace user does not exists
# -----------------------------------------------------
@behave.given("A user has access to the application and enters valid details for user updation but Inspace user does not exists")
def step_impl_1(context):
  context.user_dict = deepcopy(TEST_USER)
  context.user_dict["email"] = f"{uuid4()}@gmail.com"
  context.query_params = {"create_inspace_user": True}

  url = f"{UM_API_URL}/user"
  post_user_res = post_method(
      url, request_body=context.user_dict, query_params=context.query_params)
  context.status_code = post_user_res.status_code
  context.post_user_res_json = post_user_res.json()

  assert context.post_user_res_json.get("success") == True
  assert context.post_user_res_json.get("data")["inspace_user"]["is_inspace_user"] == True
  assert context.post_user_res_json.get("data")["inspace_user"]["inspace_user_id"] != ""
  assert context.post_user_res_json.get("message") == "Successfully created new User, "\
                                                "corresponding agent and Inspace User"

  assert context.status_code == 200

  context.user_id = context.post_user_res_json.get("data")["user_id"]

  # Inspace GET API call
  user = User.find_by_uuid(context.user_id)
  status_code, _ = get_inspace_user_helper(user)
  assert status_code == 200

  # Inspace DELETE API call
  result = delete_inspace_user_helper(user)
  assert result is True

@behave.when("An api call is made to the User Management Service with correct details for user updation but Inspace user does not exists")
def step_impl_2(context):
  url = f"{UM_API_URL}/user/{context.user_id}"

  context.request_body = {
    "first_name": "updated fname",
    "last_name": "updated lname"
  }

  query_params = {
    "update_inspace_user": True
  }
  context.res = put_method(url= url,request_body=context.request_body,query_params=query_params)
  context.res_json = context.res.json()

@behave.then("The User will not be updated alongwith Inspace User")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_json["success"] == True
  assert context.res_json["message"] == "Successfully updated the user but corresponding Inspace user couldn't be updated"
  assert context.res_json["data"]["first_name"] == context.request_body["first_name"]
  assert context.res_json["data"]["last_name"] == context.request_body["last_name"]

  # Inspace API call
  user = User.find_by_uuid(context.user_id)
  status_code, _ = get_inspace_user_helper(user)
  assert status_code == 404

# -----------------------------------------------------
# Scenario 6: An Inspace User info is to be deleted along with backend user
# -----------------------------------------------------
@behave.given("A user has access to the application and enters valid details for user deletion but Inspace user does not exists")
def step_impl_1(context):
  context.user_dict = deepcopy(TEST_USER)
  context.user_dict["email"] = f"{uuid4()}@gmail.com"
  context.query_params = {"create_inspace_user": True}

  url = f"{UM_API_URL}/user"
  post_user_res = post_method(
      url, request_body=context.user_dict, query_params=context.query_params)
  context.status_code = post_user_res.status_code
  context.post_user_res_json = post_user_res.json()

  assert context.post_user_res_json.get("success") == True
  assert context.post_user_res_json.get("data")["inspace_user"]["is_inspace_user"] == True
  assert context.post_user_res_json.get("data")["inspace_user"]["inspace_user_id"] != ""
  assert context.post_user_res_json.get("message") == "Successfully created new User, "\
                                                "corresponding agent and Inspace User"

  assert context.status_code == 200

  context.user_id = context.post_user_res_json.get("data")["user_id"]

  # Inspace GET API call
  user = User.find_by_uuid(context.user_id)
  status_code, _ = get_inspace_user_helper(user)
  assert status_code == 200

  # Inspace DELETE API call
  result = delete_inspace_user_helper(user)
  assert result is True

@behave.when("An api call is made to the User Management Service with correct details for user deletion but Inspace user does not exists")
def step_impl_2(context):
  url = f"{UM_API_URL}/user/{context.user_id}"

  query_params = {
    "delete_inspace_user": True
  }
  context.res = delete_method(url= url,query_params=query_params)
  context.res_json = context.res.json()

@behave.then("The User will not be deleted alongwith Inspace User")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_json["success"] == True
  assert context.res_json["message"] == "Successfully deleted the user and associated agent, learner/faculty but could not delete Inspace User"