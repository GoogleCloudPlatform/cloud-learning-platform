"""
Feature: To fetch Inspace token
"""

# pylint: disable=line-too-long, wrong-import-position
import behave
from uuid import uuid4
from copy import deepcopy
import sys

sys.path.append("../")
from e2e.test_config import (API_URL_AUTHENTICATION_SERVICE,
                        API_URL_USER_MANAGEMENT)
from e2e.test_object_schemas import (TEST_SIGN_UP, TEST_USER)
from common.models import User
from common.utils.inspace import delete_inspace_user_helper
from e2e.setup import post_method, get_method, get_cache, set_cache

API_URL = API_URL_AUTHENTICATION_SERVICE
UM_API_URL = API_URL_USER_MANAGEMENT

# Scenario: Fetch inpsace token for extisting inspace user
@behave.given("The inspace user already exists")
def step_1_1(context):
  user_dict = deepcopy(TEST_USER)
  user_dict["email"] = f"{uuid4()}@gmail.com"
  param = { "create_inspace_user" : True }

  post_user_url = f"{UM_API_URL}/user"
  post_user_res = post_method(
    url= post_user_url,
    request_body= user_dict,
    query_params= param
  )
  assert post_user_res.status_code == 200
  context.uuid = post_user_res.json()["data"]["user_id"]

  context.req_body = deepcopy({
      **TEST_SIGN_UP, "email": user_dict["email"]
  })
  sign_up_url = f"{API_URL}/sign-up/credentials"
  context.res_signup = post_method(url=sign_up_url, request_body=context.req_body)
  assert context.res_signup.status_code == 200
  context.res_data = context.res_signup.json()
  set_cache(key="authToken", value=context.res_data["data"]["idToken"])

@behave.when("API request is sent to fetch the inspace token")
def step_impl_2(context):
  get_token_url = f"{API_URL}/inspace/token/{context.uuid}"
  context.get_token_res = get_method(url= get_token_url,
                                  token=context.res_data["data"]["idToken"])

@behave.then("The inspace token for existing user is returned")
def step_impl_3(context):
  assert context.get_token_res.status_code == 200
  assert context.get_token_res.json()["message"] == "Successfully fetched the inspace token"

  # Clean up inspace user
  user = User.find_by_uuid(context.uuid)
  result = delete_inspace_user_helper(user)
  assert result is True

# Scenario: Fetch inpsace token for when inspace_user is false
@behave.given("The inspace user does not exists")
def step_1_1(context):
  user_dict = deepcopy(TEST_USER)
  user_dict["email"] = f"{uuid4()}@gmail.com"
  param = { "create_inspace_user" : False }

  post_user_url = f"{UM_API_URL}/user"
  post_user_res = post_method(
    url= post_user_url,
    request_body= user_dict,
    query_params= param
  )

  assert post_user_res.status_code == 200
  context.uuid = post_user_res.json()["data"]["user_id"]

@behave.when("API request is sent to retrieve the inspace token")
def step_impl_2(context):
  authToken = get_cache(key="authToken")
  get_token_url = f"{API_URL}/inspace/token/{context.uuid}"
  context.get_token_res = get_method(url= get_token_url, token=authToken)

@behave.then("Error in creating inpsace token message will be returned")
def step_impl_3(context):
  assert context.get_token_res.status_code == 500
