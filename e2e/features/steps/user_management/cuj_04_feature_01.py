"""
Feature 04 - CRUD APIs for managing Sessions data in User Management
"""

import behave
import sys
from copy import copy
from uuid import uuid4
sys.path.append("../")
from setup import post_method, get_method, put_method, set_cache, get_cache
from test_config import API_URL_USER_MANAGEMENT
from test_object_schemas import (BASIC_SESSION_DATA, TEST_USER)

# Create Session for a valid User with the correct request payload
@behave.given("A User has access to User Management and wants to create a Session with the correct request payload")
def step_impl1(context):
  user_dict = copy(TEST_USER)
  user_dict["email"] = f"{uuid4()}@gmail.com"
  created_user = post_method(url=f"{API_URL_USER_MANAGEMENT}/user", request_body=user_dict)
  created_user_data = created_user.json()
  print(created_user_data)
  assert created_user.status_code == 200, "User creation failed"
  context.user_id=created_user_data["data"]["user_id"]
  set_cache(key="user_id", value=context.user_id)
  context.url = f"{API_URL_USER_MANAGEMENT}/session"
  context.req_body = { **BASIC_SESSION_DATA, "user_id": context.user_id}

@behave.when("A valid User sends a API request to create a Session with the correct request payload")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()

@behave.then("The User Management will create a Session for the User")
def step_impl3(context):
  set_cache(key="session_id", value=context.res_data["data"]["session_id"])
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success not True"
  assert context.res_data["message"] == "Successfully created the session", "Expected message not returned"
  assert context.res_data["data"]["user_id"] == context.user_id


# Create Session for an invalid User
@behave.given("A Invalid User wants to create a Session")
def step_impl1(context):
  context.user_id="random_invalid_uuid"
  context.url = f"{API_URL_USER_MANAGEMENT}/session"
  context.req_body = { **BASIC_SESSION_DATA, "user_id": context.user_id}

@behave.when("A Invalid User sends a API request to create a Session")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("The User Management will not create a Session and returns a ResourceNotFound Exception")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["success"] is False, "Success not False"
  assert context.res_data["message"] == f"User with user_id {context.user_id} not found", "Expected message not returned"

# Create Session for a valid User with an incorrect request payload
@behave.given("A User has access to User Management and wants to create a Session with an incorrect request payload")
def step_impl1(context):
  context.url = f"{API_URL_USER_MANAGEMENT}/session"
  context.req_body ={ }

@behave.when("A valid User sends a API request to create a Session with an incorrect request payload")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()

@behave.then("The User Management will not create a Session for the User and throws a Validation error")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 200"
  assert context.res_data["success"] is False, "Success not True"
  assert context.res_data["message"] == "Validation Failed", "Expected message not returned"

# User wants to fetch a session by providing a valid Session Id
@behave.given("User has the privilege to access User Management service and wants to get his/her Session by providing correct Session Id")
def step_impl1(context):
  context.user_id= get_cache(key="user_id")
  context.session_id = get_cache(key="session_id")
  context.url = f"{API_URL_USER_MANAGEMENT}/session/{context.session_id}"

@behave.when("User sends a API request to User Management to get a Session by sending a valid Session Id")
def step_impl2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("User Management service will return the requested Session Object in response")
def step_impl3(context):
  del context.res_data["data"]["created_time"]
  del context.res_data["data"]["last_modified_time"]

  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success not True"
  assert context.res_data["message"] == "Successfully fetched the session", "Expected message not returned"
  print(context.res_data["data"])
  print( { **BASIC_SESSION_DATA, "user_id": context.user_id, "session_id": context.session_id })
  assert context.res_data["data"] == { **BASIC_SESSION_DATA, "user_id": context.user_id, "session_id": context.session_id }

# User wants to fetch a session by providing a Invalid Session Id
@behave.given("User has the privilege to access User Management service and wants to get his/her Session by providing Incorrect Session Id")
def step_impl1(context):
  context.session_id = "invalid_session_id"
  context.url = f"{API_URL_USER_MANAGEMENT}/session/{context.session_id}"

@behave.when("User sends a API request to User Management to get a Session by sending a Invalid Session Id")
def step_impl2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("User Management service will return ResourceNotFound Exception")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["success"] is False, "Success not False"
  assert context.res_data["message"] == f"Session with session_id {context.session_id} not found", "Expected message not returned"

# A User wants to fetch all sessions or filter sessions related to his/her User Id, Node Id, and Session Id
@behave.given("A User has access to User Management and wants to fetch all sessions or filter sessions related to his/her User Id, Node Id, and Session Id")
def step_impl1(context):
  context.user_id = get_cache(key="user_id")
  session_id1 = get_cache(key = "session_id")
  session_2 = post_method(url=f"{API_URL_USER_MANAGEMENT}/session", request_body={ **BASIC_SESSION_DATA, "user_id": context.user_id})
  session_2_data = session_2.json()
  context.session_ids = [session_2_data["data"]["session_id"],session_id1]
  context.url = f"{API_URL_USER_MANAGEMENT}/session"

@behave.when("A valid User sends a API request to fetch all sessions related to his/her User Id, Node Id, and Session Id")
def step_impl2(context):
  context.res = get_method(url=context.url, query_params={"user_id": context.user_id})
  context.res_data = context.res.json()

@behave.then("The User Management will return the requested sessions")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success not True"
  assert context.res_data["message"] == "Successfully fetched the sessions", "Expected message not returned"
  assert len(context.res_data["data"]) > 0
  assert len([ session["user_id"] for session in context.res_data["data"] if session["user_id"] != context.user_id]) == 0

# A User wants to fetch the latest session related to his/her User Id
@behave.given("A User has access to User Management and needs to fetch the latest Session related to his/her User Id")
def step_impl1(context):
  context.user_id= get_cache(key="user_id")
  context.session_id = get_cache(key="session_id")
  latest_session = post_method(url=f"{API_URL_USER_MANAGEMENT}/session", request_body={ **BASIC_SESSION_DATA, "user_id": context.user_id})
  latest_session_data = latest_session.json()
  context.latest_session_id = latest_session_data["data"]["session_id"]
  context.url = f"{API_URL_USER_MANAGEMENT}/session/latest"

@behave.when("A valid User sends a API request to fetch the latest session related to his/her User Id")
def step_impl2(context):
  context.res = get_method(url=context.url, query_params={"user_id": context.user_id})
  context.res_data = context.res.json()


@behave.then("The User Management will return the latest session related to User Id")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success not True"
  assert context.res_data["message"] == "Successfully fetched latest session", "Expected message not returned"
  assert context.res_data["data"]["session_id"] == context.latest_session_id

# Rules Engine wants to update session details by providing Session and correct request payload
@behave.given("Rules Engine has access to User Management and wants to update Session using session Id and by sending the correct request payload")
def step_impl1(context):
  context.session_id = get_cache(key = "session_id")
  context.user_id= get_cache(key ="user_id")
  context.url = f"{API_URL_USER_MANAGEMENT}/session/{context.session_id}"
  context.req_body ={
    "session_data": { **BASIC_SESSION_DATA, "user_id": context.user_id, "node_type":"assessment_items" }
  }

@behave.when("Rules Engine sends a API request to update the session with the correct request Payload")
def step_impl2(context):
  context.res = put_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()
  print(context.res_data)

@behave.then("The User Management will update the session and returns the updated session")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success not True"
  assert context.res_data["message"] == "Successfully updated the session", "Expected message not returned"
  assert context.res_data["data"]["user_id"] == context.user_id

# Rules Engine wants to update non existing Session
@behave.given("Rules Engine has access to User Management and wants to update a non existing Session")
def step_impl1(context):
  context.session_id = "randon_session_id"
  context.url = f"{API_URL_USER_MANAGEMENT}/session/{context.session_id}"
  context.req_body ={
    "session_data": { **BASIC_SESSION_DATA, "node_type":"assessment_items" }
  }

@behave.when("Rules Engine sends a API request to update the session with the invalid Session Id")
def step_impl2(context):
  context.res = put_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()

@behave.then("The User Management will return ResourceNotFound Exception")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 200"
  assert context.res_data["success"] is False, "Success not True"
  assert context.res_data["message"] == f"Session with session_id {context.session_id} not found", "Expected message not returned"
