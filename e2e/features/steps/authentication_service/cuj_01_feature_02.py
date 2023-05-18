"""
Users want to get access to backend APIs using email and password authentication
"""

# pylint: disable=line-too-long, wrong-import-position
import behave
from uuid import uuid4
from copy import deepcopy
import sys

sys.path.append("../")
from setup import post_method, set_cache, get_cache
from test_config import (API_URL_AUTHENTICATION_SERVICE,
                         API_URL_USER_MANAGEMENT)
from test_object_schemas import (TEST_SIGN_UP, TEST_USER)

API_URL = API_URL_AUTHENTICATION_SERVICE

# ---- The user wants to set password to the backend using sign-up api with valid email-id ----


@behave.given(
    "the user email id already exists in the backend firestore database")
def step_1_1(context):
  context.user_data = {**TEST_USER, "email": f"{uuid4()}@gmail.com"}

  # create a user
  created_user = post_method(
      url=f"{API_URL_USER_MANAGEMENT}/user", request_body=context.user_data)

  assert created_user.status_code == 200, "not able to create user"

  context.req_body = deepcopy({
      **TEST_SIGN_UP, "email": context.user_data["email"]
  })
  set_cache(key="authentication_credentials", value=context.req_body)


@behave.when(
    "API request is sent to sign up with backend with valid email in the request body"
)
def step_1_2(context):
  sign_up_url = f"{API_URL}/sign-up/credentials"
  context.res = post_method(url=sign_up_url, request_body=context.req_body)
  context.res_data = context.res.json()
  print("API request is sent to sign up with backend with valid email in the request body")
  print(context.res)
  print(context.res_data)


@behave.then(
    "the Authentication service successfully signs up the user with the backend"
)
def step_1_3(context):
  assert context.res.status_code == 200, "signup api failed"
  assert context.res_data["success"] is True, "signup success status not true"
  assert "idToken" in context.res_data[
      "data"], "id token not present in response"
  assert context.res_data["data"]["email"] == context.user_data[
      "email"], "unknown email"


@behave.then(
    "the user can sign in to the backend using correct email and password")
def step_1_4(context):
  sign_in_url = f"{API_URL}/sign-in/credentials"
  sign_in_res = post_method(url=sign_in_url, request_body=context.req_body)
  assert sign_in_res.status_code == 200, "user sign-in failed"


# ---- The user wants to set password to the backend using sign-up api with invalid email-id ----
@behave.given(
    "the user email id doesn't exists in the backend firestore database")
def step_2_1(context):
  # change email is of unknown user
  context.req_body = deepcopy({
      **TEST_SIGN_UP, "email": "invalid_user@gmail.com"
  })


@behave.when(
    "API request is sent to set the password with invalid email in the request body"
)
def step_2_2(context):
  sign_up_url = f"{API_URL}/sign-up/credentials"
  context.res = post_method(url=sign_up_url, request_body=context.req_body)
  context.res_data = context.res.json()
  print("API request is sent to set the password with invalid email in the request body")
  print(context.res)
  print(context.res_data)


@behave.then(
    "the Authentication service will not sign up the user instead throws Unauthorized user"
)
def step_2_3(context):
  assert context.res.status_code == 401, "signup api failed to return 401 status code on unknown email"
  assert context.res_data[
      "success"] is False, "signup api success not false for unknown email"
  assert context.res_data[
      "message"] == "Unauthorized", "unexpected message received from signup api"


# ---- The user wants to sign-in in to the backend with correct email-id and password ----


@behave.given("the user have already signed up with the backend")
def step_3_1(context):
  signed_up_user = get_cache(key="authentication_credentials")
  context.req_body = signed_up_user


@behave.when("API request is sent to sign in with correct request body")
def step_3_2(context):
  sign_in_url = f"{API_URL}/sign-in/credentials"
  context.res = post_method(url=sign_in_url, request_body=context.req_body)
  context.res_data = context.res.json()
  print("API request is sent to sign in with correct request body")
  print(context.res)
  print(context.res_data)


@behave.then(
    "the user successfully logs in to backend and receives response that contains a valid id-token of the backend project"
)
def step_3_3(context):
  assert context.res.status_code == 200, "user sign-in failed"
  assert context.res_data["success"] is True, "user sign-in failed"
  assert context.res_data[
      "message"] == "Successfully signed in", "user sign-in failed"
  assert context.res_data["data"]["email"] == context.req_body[
      "email"], "user sign-in failed"


# ---- The user wants to sign-in in to the backend with incorrect email-id and password ----


@behave.given("the user is not already signed up with the backend")
def step_4_1(context):
  context.req_body = deepcopy({
      **TEST_SIGN_UP, "email": "invalid_user@gmail.com"
  })
  context.url = f"{API_URL}/sign-in/credentials"


@behave.when("In Valid User sends API request to sign in to the backend")
def step_4_2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()
  print("In Valid User sends API request to sign in to the backend")
  print(context.res)
  print(context.res_data)

@behave.then("the Authentication service throws Unauthorized user")
def step_4_3(context):
  assert context.res.status_code == 401
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Unauthorized"


# ---- The user tries to sign-in in to the backend with correct email-id and wrong password ----


@behave.given("the user is already a signed up user of backend")
def step_5_1(context):
  signed_up_user = get_cache(key="authentication_credentials")
  context.req_body = {**signed_up_user, "password": "wrong_password"}
  context.url = f"{API_URL}/sign-in/credentials"


@behave.when("API request is sent to sign in with wrong password")
def step_5_2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()
  print("API request is sent to sign in with wrong password")
  print(context.res)
  print(context.res_data)


@behave.then(
    "the Authentication service returns error response invalid credentials")
def step_5_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "INVALID_PASSWORD"


# ---- The user wants to change sign in password of backend using valid id-token ----


@behave.given(
    "the user already signs in to the backend and has a valid id-token")
def step_6_1(context):
  signed_up_user = get_cache(key="authentication_credentials")
  sign_in_url = f"{API_URL}/sign-in/credentials"
  context.sign_in = post_method(url=sign_in_url, request_body=signed_up_user)
  context.sign_in_data = context.sign_in.json()
  context.req_body = deepcopy({
      **signed_up_user, "password": "changed_password"
  })
  set_cache(key="authentication_credentials", value=context.req_body)
  context.url = f"{API_URL}/change-password"


@behave.when(
    "API request with valid Id token is sent to Authentication service to change sign in password"
)
def step_6_2(context):
  context.res = post_method(
      url=context.url,
      request_body=context.req_body,
      token=context.sign_in_data["data"]["idToken"])
  context.res_data = context.res.json()
  print("API request with valid Id token is sent to Authentication service to change sign in password")
  print(context.res)
  print(context.res_data)


@behave.then(
    "the Authentication service successfully changes users sign in password and return successfully changed password message in response"
)
def step_6_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["message"] == "Successfully changed the password"


@behave.then("the user can sign in to the backend using changed password")
def step_6_4(context):
  sign_in_url = f"{API_URL}/sign-in/credentials"
  sign_in_res = post_method(url=sign_in_url, request_body=context.req_body)
  assert sign_in_res.status_code == 200


# ---- The user wants to change sign in password of backend using Invalid id-token ----


@behave.given("the user already signs in to the backend")
def step_7_1(context):
  signed_up_user = get_cache(key="authentication_credentials")
  context.url = f"{API_URL}/sign-in/credentials"
  context.sign_in = post_method(url=context.url, request_body=signed_up_user)

  assert context.sign_in.status_code == 200
  context.sign_in_data = context.sign_in.json()

  context.change_password_url = f"{API_URL}/change-password"
  context.req_body = deepcopy({
      **signed_up_user, "password": "changed_password"
  })


@behave.when(
    "API request with invalid Id token is sent to Authentication service to change sign in password"
)
def step_7_2(context):
  context.res = post_method(
      url=context.change_password_url,
      request_body=context.req_body,
      token="invalid_token")
  context.res_data = context.res.json()
  print("API request with invalid Id token is sent to Authentication service to change sign in password")
  print(context.res)
  print(context.res_data)


@behave.then(
    "the Authentication service returns an error response invalid token")
def step_7_3(context):
  assert context.res.status_code == 401
  assert context.res_data["success"] is False
