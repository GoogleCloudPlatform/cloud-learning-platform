"""
E2E API for action module
"""

import sys

from behave import *
from behave.runner import Context
from uuid import uuid4

sys.path.append("../")
from e2e.test_object_schemas import TEST_ACTION
from e2e.test_config import API_URL_USER_MANAGEMENT as UM_API_URL
from e2e.setup import post_method, get_method, put_method, delete_method


@given("user wants to create action in user management with correct "
       "request payload")
def step_impl_1(context: Context) -> None:
  """
  Construct the request payload to create action
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """
  context.action_dict = {**TEST_ACTION}
  context.action_dict["name"] = f"Action - {uuid4()}"


@when("API request is sent to create action with correct request payload")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to create action
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """
  context.url = f"{UM_API_URL}/action"
  context.res = post_method(url=context.url,
                            request_body=context.action_dict)
  context.res_data = context.res.json()


@then("the action has been created successfully")
def step_impl_3(context: Context) -> None:
  """
  Assert the action Response
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """
  assert context.res.status_code == 200
  assert context.res_data["message"] == "Successfully created the action"


@given("user wants to create action in user management with incorrect "
       "request payload")
def step_impl_1(context: Context) -> None:
  """
  Construct incorrect request payload to create action
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  context.action_dict = {**TEST_ACTION}
  del context.action_dict["name"]


@when("API request is sent to create action with incorrect request payload")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to create action
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """
  context.url = f"{UM_API_URL}/action"
  context.res = post_method(url=context.url,
                            request_body=context.action_dict)
  context.res_data = context.res.json()


@then("the action has been failed to create for incorrect request payload")
def step_impl_3(context: Context) -> None:
  """
  Assert the action Response
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

@given("A user wants to create an action with name already existing in database")
def step_impl_1(context):
  context.action_dict = {**TEST_ACTION}
  context.action_dict["name"] = f"Action - {uuid4()}"
  context.url=f"{UM_API_URL}/action"

  post_action = post_method(
      url=context.url, request_body=context.action_dict)
  post_action_data = post_action.json()
  context.action_name = post_action_data["data"]["name"]
  assert post_action.status_code == 200

@when("API request is sent to create action with name already existing in database")
def step_impl_2(context):
  context.res = post_method(url=context.url, request_body=context.action_dict)
  context.res_data = context.res.json()


@then("action object will not be created and a conflict error is thrown")
def step_impl_3(context):
  assert context.res.status_code == 500
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == \
    f"Action with the given name: {context.action_name} already exists"


@given("user want to update their action with correct action ID")
def step_impl_1(context: Context) -> None:
  """
  Construct the request payload and query param to update the action
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  context.action_dict = {**TEST_ACTION}
  context.action_dict["name"] = f"Action - {uuid4()}"
  post_url = f"{UM_API_URL}/action"
  post_action = post_method(url=post_url,
                            request_body=context.action_dict)
  context.action_id = post_action.json()["data"]["uuid"]

  assert post_action.status_code == 200


@when("API request is sent to update action with correct action ID")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to update the action with correct action ID
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """
  context.action_dict["name"] = f"Action - {uuid4()}"
  context.url = f"{UM_API_URL}/action/{context.action_id}"
  context.res = put_method(url=context.url,
                           request_body=context.action_dict)


@then("the action has been updated successfully with correct action ID")
def step_impl_3(context: Context) -> None:
  """
  Assert the Updated action Response
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  assert context.res.status_code == 200
  assert context.res.json()["success"] is True
  assert context.res.json()["message"] == "Successfully updated the action"
  assert context.res.json()["data"]["name"] == context.action_dict["name"]


@given("user try to update their action with incorrect action ID")
def step_impl_1(context: Context) -> None:
  """
  Construct the request payload and incorrect query param to update the
  action
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  context.action_dict = {**TEST_ACTION}
  context.action_id = "12322121we3"


@when("API request is sent to update the action for incorrect action "
      "ID")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to update the action with incorrect action ID
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """
  context.action_dict["name"] = f"Action - {uuid4()}"
  context.url = f"{UM_API_URL}/action/{context.action_id}"
  context.res = put_method(url=context.url,
                           request_body=context.action_dict)


@then("the action has been failed to update with incorrect action ID")
def step_impl_3(context: Context) -> None:
  """
  Assert the Updated action Response
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  assert context.res.status_code == 404
  assert context.res.json()["success"] is False
  assert context.res.json()["message"] == f"Action with uuid " \
                                          f"{context.action_id} not found"
  assert context.res.json()["data"] is None


@given("action is fetch from the datastore with correct action ID")
def step_impl_1(context: Context) -> None:
  """
  Construct query param to fetch action details
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  context.action_dict = {**TEST_ACTION}
  context.action_dict["name"] = f"Action - {uuid4()}"
  post_url = f"{UM_API_URL}/action"
  post_action = post_method(url=post_url,
                            request_body=context.action_dict)
  context.action_id = post_action.json()["data"]["uuid"]

  assert post_action.status_code == 200


@when("API request is sent to fetch the action details with correct "
      "action ID")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to fetch action Based on action ID
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  context.url = f"{UM_API_URL}/action/{context.action_id}"
  context.res = get_method(url=context.url)


@then("the action is fetched successfully with correct action ID")
def step_impl_3(context: Context) -> None:
  """
  Assert the fetch action details
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  assert context.res.status_code == 200
  assert context.res.json()["success"] is True
  assert context.res.json()["message"] == "Successfully fetched the action"
  assert context.res.json()["data"]["uuid"] == context.action_id


@given("User try to fetch their action with incorrect action ID")
def step_impl_1(context: Context) -> None:
  """
  Construct query param to fetch action details
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  context.action_id = "121212314324jjj3r345"


@when("API request is sent to fetch the action with incorrect action "
      "ID")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to fetch action Based on action ID
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  context.url = f"{UM_API_URL}/action/{context.action_id}"
  context.res = get_method(url=context.url)


@then("the action details is failed to fetch for incorrect action ID")
def step_impl_3(context: Context) -> None:
  """
  Assert the fetch action details
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  assert context.res.status_code == 404
  assert context.res.json()["success"] is False
  assert context.res.json()["message"] == f"Action with uuid " \
                                          f"{context.action_id} not found"
  assert context.res.json()["data"] is None


@given("fetch all the actions from the datastore")
def step_impl_1(context: Context) -> None:
  """
  Construct query param to fetch action details
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """
  context.action_dict = {**TEST_ACTION}
  context.action_dict["name"] = f"Action - {uuid4()}"
  post_url = f"{UM_API_URL}/action"
  post_action = post_method(url=post_url,
                            request_body=context.action_dict)

  assert post_action.status_code == 200


@when("API request is sent to fetch all the actions")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to fetch actions
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """
  context.url = f"{UM_API_URL}/actions"
  context.query_params = {"skip": "0", "limit": "10"}
  context.res = get_method(url=context.url, query_params=context.query_params)


@then("the actions is fetched successfully")
def step_impl_3(context: Context) -> None:
  """
  Assert the fetch actions details
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
  assert type(context.res.json()["data"]["records"]) is list


@given("fetch all the actions for incorrect query params")
def step_impl_1(context: Context) -> None:
  """
  Construct query param to fetch actions details
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  context.url = f"{UM_API_URL}/actions"
  context.query_params = {"skip": "-1", "limit": "10"}


@when("API request is sent for fetch all the actions with incorrect query "
      "params")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to fetch actions
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  context.res = get_method(url=context.url, query_params=context.query_params)


@then("the actions is failed to fetch for incorrect query params")
def step_impl_3(context: Context) -> None:
  """
  Assert the fetch actions details
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
