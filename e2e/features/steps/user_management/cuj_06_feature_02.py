"""
E2E API test for permission module filters
"""

import sys

from behave import *
from behave.runner import Context
from uuid import uuid4
from copy import deepcopy

sys.path.append("../")
from e2e.test_object_schemas import TEST_PERMISSION, TEST_ACTION, TEST_MODULE, \
  TEST_APPLICATION, TEST_USER_GROUP
from e2e.test_config import API_URL_USER_MANAGEMENT as UM_API_URL
from e2e.setup import post_method, get_method

group_name = uuid4()

@given("Retrieve all unique applications, modules, actions and user groups from permission collection")
def step_impl_1(context):
  action_dict = {**TEST_ACTION, "name": f"action-{uuid4()}"}
  action_res = post_method(url=f"{UM_API_URL}/action", request_body=action_dict)
  assert action_res.status_code == 200
  context.action_id = action_res.json().get("data").get("uuid")

  module_dict = {
    **TEST_MODULE,
    "name": f"module-{uuid4()}",
    "actions": [context.action_id]}
  module_res = post_method(url=f"{UM_API_URL}/module", request_body=module_dict)
  assert module_res.status_code == 200
  context.module_id = module_res.json().get("data").get("uuid")

  application_dict = {**TEST_APPLICATION, "modules": [context.module_id]}
  application_dict["name"] = str(uuid4())
  application_res = post_method(
    url=f"{UM_API_URL}/application", request_body=application_dict)
  assert application_res.status_code == 200
  context.application_id = application_res.json().get("data").get("uuid")

  user_group_dict = {**TEST_USER_GROUP, "name": f"{uuid4()}"}
  user_group_url = f"{UM_API_URL}/user-group"
  user_group_res = post_method(url=user_group_url,
                                    request_body=user_group_dict)
  assert user_group_res.status_code == 200
  context.user_group_id = user_group_res.json().get("data").get("uuid")


  permission_url = f"{UM_API_URL}/permission"
  permission_dict = deepcopy(TEST_PERMISSION)
  permission_dict["application_id"] = context.application_id
  permission_dict["module_id"] = context.module_id
  permission_dict["action_id"] = context.action_id
  del permission_dict["user_groups"]
  post_permission = post_method(
    url=permission_url,
    request_body=permission_dict
  )
  assert post_permission.status_code == 200

@when("API request is sent to fetch unique records from permission collection")
def step_impl_2(context):
  url = f"{UM_API_URL}/permission_filter/unique"
  unique_records = get_method(url)
  context.unique_records_res = unique_records.json()

@then("Object will be returned with unique values from permission collection")
def step_impl_3(context):
  assert context.unique_records_res["success"] is True
  assert context.unique_records_res["message"] == "Successfully fetched the unique values for applications, modules, actions and user_groups."
  assert len(context.unique_records_res["data"]["applications"]) >= 1

@given("Retrieve all unique applications, modules, actions and user groups matching query params")
def step_impl_1(context):
  action_dict = {**TEST_ACTION, "name": f"action-{uuid4()}"}
  action_res = post_method(
    url=f"{UM_API_URL}/action", request_body=action_dict)
  assert action_res.status_code == 200
  context.action_id = action_res.json().get("data").get("uuid")

  module_dict = {
    **TEST_MODULE,
    "name": f"module-{uuid4()}",
    "actions": [context.action_id]}
  module_res = post_method(
    url=f"{UM_API_URL}/module", request_body=module_dict)
  assert module_res.status_code == 200
  context.module_id = module_res.json().get("data").get("uuid")

  application_dict = {**TEST_APPLICATION, "modules": [context.module_id]}
  application_dict["name"] = str(uuid4())
  application_res = post_method(
    url=f"{UM_API_URL}/application", request_body=application_dict)
  assert application_res.status_code == 200
  context.application_id = application_res.json().get("data").get("uuid")

  user_group_dict = {**TEST_USER_GROUP, "name": f"{uuid4()}"}
  user_group_url = f"{UM_API_URL}/user-group"
  user_group_res = post_method(url=user_group_url,
                                    request_body=user_group_dict)
  assert user_group_res.status_code == 200

  permission_url = f"{UM_API_URL}/permission"
  permission_dict = deepcopy(TEST_PERMISSION)
  permission_dict["application_id"] = context.application_id
  permission_dict["module_id"] = context.module_id
  permission_dict["action_id"] = context.action_id
  del permission_dict["user_groups"]
  post_permission = post_method(
    url=permission_url,
    request_body=permission_dict
  )
  assert post_permission.status_code == 200

@when("API request is sent to fetch unique records from permission collection matching query params")
def step_impl_2(context):
  url = f"{UM_API_URL}/permission_filter/unique?application={context.application_id}"
  unique_records = get_method(url)
  context.unique_records_res = unique_records.json()

@then("Object will be returned with unique values from permission collection matching query params")
def step_impl_3(context):
  assert context.unique_records_res["success"] is True
  assert len(context.unique_records_res["data"]["applications"]) == 1


@given("Retrieve all unique applications, modules, actions and user groups matching invalid query params")
def step_impl_1(context):
  pass

@when("API request is sent to fetch unique records from permission collection matching invalid query params")
def step_impl_2(context):
  url = f"{UM_API_URL}/permission_filter/unique?application=some_random_application_uuid"
  unique_records = get_method(url)
  context.unique_records_res = unique_records.json()

@then("Object will be returned with empty filter data")
def step_impl_3(context):
  assert context.unique_records_res["success"] is True
  assert context.unique_records_res["data"]["applications"] == []
