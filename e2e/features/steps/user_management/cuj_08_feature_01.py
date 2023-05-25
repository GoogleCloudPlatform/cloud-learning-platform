"""
E2E API for module module
"""

import sys

from behave import *
from behave.runner import Context
from uuid import uuid4

sys.path.append("../")
from common.models import Action
from e2e.test_object_schemas import TEST_MODULE, TEST_ACTION
from e2e.test_config import API_URL_USER_MANAGEMENT as UM_API_URL
from e2e.setup import post_method, get_method, put_method, delete_method


@given("user wants to create module in user management with correct "
       "request payload")
def step_impl_1(context: Context) -> None:
  """
  Construct the request payload to create module
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """
  action_dict = {**TEST_ACTION}
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()
  action_dict["uuid"] = action.id

  context.module_dict = {**TEST_MODULE, "name": f"Module - {uuid4()}",
                         "actions": [action.id]}


@when("API request is sent to create module with correct request payload")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to create module
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """
  context.url = f"{UM_API_URL}/module"
  context.res = post_method(url=context.url,
                            request_body=context.module_dict)
  context.res_data = context.res.json()


@then("the module has been created successfully")
def step_impl_3(context: Context) -> None:
  """
  Assert the module Responsethreadpool
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """
  assert context.res.status_code == 200
  assert context.res_data["message"] == "Successfully created the module"


@given("user wants to create module in user management with incorrect "
       "request payload")
def step_impl_1(context: Context) -> None:
  """
  Construct incorrect request payload to create module
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  context.module_dict = {**TEST_MODULE}
  del context.module_dict["name"]


@when("API request is sent to create module with incorrect request payload")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to create module
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """
  context.url = f"{UM_API_URL}/module"
  context.res = post_method(url=context.url,
                            request_body=context.module_dict)
  context.res_data = context.res.json()


@then("the module has been failed to create for incorrect request payload")
def step_impl_3(context: Context) -> None:
  """
  Assert the module Response
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  assert context.res.status_code == 422
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Validation Failed"
  assert context.res_data["data"] == [{
    "loc": ["body", "name"],
    "msg": "field required",
    "type": "value_error.missing"
  }]

@given("A user wants to create an module with name already existing in database")
def step_impl_1(context):
  context.module_dict = {**TEST_MODULE}
  context.module_dict["name"] = f"Module - {uuid4()}"
  context.url=f"{UM_API_URL}/module"

  post_module = post_method(
      url=context.url, request_body=context.module_dict)
  post_module_data = post_module.json()
  context.module_name = post_module_data["data"]["name"]
  assert post_module.status_code == 200

@when("API request is sent to create module with name already existing in database")
def step_impl_2(context):
  context.res = post_method(url=context.url, request_body=context.module_dict)
  context.res_data = context.res.json()


@then("module object will not be created and a conflict error is thrown")
def step_impl_3(context):
  assert context.res.status_code == 500
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == \
    f"Module with the given name: {context.module_name} already exists"

@given("user want to update their module with correct module ID")
def step_impl_1(context: Context) -> None:
  """
  Construct the request payload and query param to update the module
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  action_dict = {**TEST_ACTION}
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()
  action_dict["uuid"] = action.id

  context.module_dict = {**TEST_MODULE, "name": f"Module - {uuid4()}",
                         "actions": [action.id]}
  post_url = f"{UM_API_URL}/module"
  post_module = post_method(url=post_url,
                            request_body=context.module_dict)
  context.module_id = post_module.json()["data"]["uuid"]

  assert post_module.status_code == 200


@when("API request is sent to update module with correct module ID")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to update the module with correct module ID
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """
  context.module_dict["name"] = f"Module - {uuid4()}"
  context.url = f"{UM_API_URL}/module/{context.module_id}"
  context.res = put_method(url=context.url,
                           request_body=context.module_dict)


@then("the module has been updated successfully with correct module ID")
def step_impl_3(context: Context) -> None:
  """
  Assert the Updated module Response
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  assert context.res.status_code == 200
  assert context.res.json()["success"] is True
  assert context.res.json()["message"] == "Successfully updated the module"
  assert context.res.json()["data"]["name"] == context.module_dict["name"]


@given("user try to update their module with incorrect module ID")
def step_impl_1(context: Context) -> None:
  """
  Construct the request payload and incorrect query param to update the
  module
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  context.module_dict = {**TEST_MODULE}
  context.module_id = "12322121we3"


@when("API request is sent to update the module for incorrect module "
      "ID")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to update the module with incorrect module ID
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """
  context.module_dict["name"] = f"Module - {uuid4()}"
  context.url = f"{UM_API_URL}/module/{context.module_id}"
  context.res = put_method(url=context.url,
                           request_body=context.module_dict)


@then("the module has been failed to update with incorrect module ID")
def step_impl_3(context: Context) -> None:
  """
  Assert the Updated module Response
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  assert context.res.status_code == 404
  assert context.res.json()["success"] is False
  assert context.res.json()["message"] == f"Module with uuid " \
                                          f"{context.module_id} not found"
  assert context.res.json()["data"] is None


@given("module is fetch from the datastore with correct module ID")
def step_impl_1(context: Context) -> None:
  """
  Construct query param to fetch module details
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  context.module_dict = {**TEST_MODULE}
  context.module_dict["name"] = f"Module - {uuid4()}"
  post_url = f"{UM_API_URL}/module"
  post_module = post_method(url=post_url,
                            request_body=context.module_dict)
  context.module_id = post_module.json()["data"]["uuid"]

  assert post_module.status_code == 200


@when("API request is sent to fetch the module details with correct "
      "module ID")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to fetch module Based on module ID
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  context.url = f"{UM_API_URL}/module/{context.module_id}"
  context.res = get_method(url=context.url)


@then("the module is fetched successfully with correct module ID")
def step_impl_3(context: Context) -> None:
  """
  Assert the fetch module details
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  assert context.res.status_code == 200
  assert context.res.json()["success"] is True
  assert context.res.json()["message"] == "Successfully fetched the module"
  assert context.res.json()["data"]["uuid"] == context.module_id


@given("User try to fetch their module with incorrect module ID")
def step_impl_1(context: Context) -> None:
  """
  Construct query param to fetch module details
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  context.module_id = "121212314324jjj3r345"


@when("API request is sent to fetch the module with incorrect module "
      "ID")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to fetch module Based on module ID
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  context.url = f"{UM_API_URL}/module/{context.module_id}"
  context.res = get_method(url=context.url)


@then("the module details is failed to fetch for incorrect module ID")
def step_impl_3(context: Context) -> None:
  """
  Assert the fetch module details
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  assert context.res.status_code == 404
  assert context.res.json()["success"] is False
  assert context.res.json()["message"] == f"Module with uuid " \
                                          f"{context.module_id} not found"
  assert context.res.json()["data"] is None


@given("fetch all the modules from the datastore")
def step_impl_1(context: Context) -> None:
  """
  Construct query param to fetch module details
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """
  context.module_dict = {**TEST_MODULE}
  context.module_dict["name"] = f"Module - {uuid4()}"
  post_url = f"{UM_API_URL}/module"
  post_module = post_method(url=post_url,
                            request_body=context.module_dict)

  assert post_module.status_code == 200


@when("API request is sent to fetch all the modules")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to fetch modules
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """
  context.url = f"{UM_API_URL}/modules"
  context.query_params = {"skip": "0", "limit": "10"}
  context.res = get_method(url=context.url, query_params=context.query_params)


@then("the modules is fetched successfully")
def step_impl_3(context: Context) -> None:
  """
  Assert the fetch modules details
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  assert context.res.status_code == 200
  assert context.res.json()["success"] is True
  assert context.res.json()["message"] == "Data fetched successfully"
  assert type(context.res.json()["data"]) is list


@given("fetch all the modules for incorrect query params")
def step_impl_1(context: Context) -> None:
  """
  Construct query param to fetch modules details
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  context.url = f"{UM_API_URL}/modules"
  context.query_params = {"skip": "-1", "limit": "10"}


@when("API request is sent for fetch all the modules with incorrect query "
      "params")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to fetch modules
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  context.res = get_method(url=context.url, query_params=context.query_params)


@then("the modules is failed to fetch for incorrect query params")
def step_impl_3(context: Context) -> None:
  """
  Assert the fetch modules details
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """
  assert context.res.status_code == 422
  assert context.res.json()["success"] is False
  assert context.res.json()["message"] == "Validation Failed"
