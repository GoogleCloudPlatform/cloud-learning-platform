"""
E2E API test for permission module
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
from e2e.setup import post_method, get_method, put_method, delete_method

group_name = uuid4()


@given("user wants to create permission in user management with correct "
       "request payload")
def step_impl_1(context: Context) -> None:
  """
  Construct the request payload to create permission
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """
  action_dict = TEST_ACTION
  action_dict["name"] = f"Action - {uuid4()}"
  action_url = f"{UM_API_URL}/action"
  action_res = post_method(url=action_url, request_body=action_dict)
  action_data = action_res.json()["data"]
  action_id = action_data["uuid"]

  module_dict = TEST_MODULE
  module_dict["name"] = f"Module - {uuid4()}"
  module_dict["actions"] = [action_id]
  module_url = f"{UM_API_URL}/module"
  module_res = post_method(url=module_url, request_body=module_dict)
  module_id = module_res.json()["data"]["uuid"]

  app_dict = TEST_APPLICATION
  app_dict["name"] = f"Application - {uuid4()}"
  app_dict["modules"] = [module_id]
  app_url = f"{UM_API_URL}/application"
  app_res = post_method(url=app_url, request_body=app_dict)
  app_id = app_res.json()["data"]["uuid"]

  group_dict = {**TEST_USER_GROUP, "name": f"{group_name}"}
  post_group = post_method(url=f"{UM_API_URL}/user-group",
                           request_body=group_dict)
  post_group_data = post_group.json()
  context.group_uuid = post_group_data["data"]["uuid"]

  context.perm_dict = {**TEST_PERMISSION, "user_groups": [
    context.group_uuid], "application_id": app_id, "module_id": module_id,
    "action_id": action_id}
  del context.perm_dict["user_groups"]


@when("API request is sent to create permission with correct request payload")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to create Permission
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """
  context.url = f"{UM_API_URL}/permission"
  context.res = post_method(url=context.url, request_body=context.perm_dict)
  context.res_data = context.res.json()


@then("the permission has been created successfully")
def step_impl_3(context: Context) -> None:
  """
  Assert the permission Response
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """
  assert context.res.status_code == 200
  assert context.res_data["message"] == "Successfully created the permission"


@given("user wants to create permission in user management with incorrect "
       "request payload")
def step_impl_1(context: Context) -> None:
  """
  Construct incorrect request payload to create permission
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """

  context.permission_dict = {**TEST_PERMISSION}
  del context.permission_dict["name"]


@when("API request is sent to create permission with incorrect request payload")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to create permission
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """
  context.url = f"{UM_API_URL}/permission"
  context.res = post_method(url=context.url,
                            request_body=context.permission_dict)
  context.res_data = context.res.json()


@then("the permission has been failed to create for incorrect request payload")
def step_impl_3(context: Context) -> None:
  """
  Assert the permission Response
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


@given("fetch all the permissions for action name")
def step_impl_1(context: Context) -> None:
  """
  Construct query param to fetch permission details
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """
  fetch_url = f"{UM_API_URL}/permissions"
  query_params = {"skip": 0, "limit": 100}
  data = get_method(url=fetch_url, query_params=query_params)
  if data.status_code == 200:
    delete_url = f"{UM_API_URL}/permission"
    [delete_method(url=f"{delete_url}/{i['uuid']}") for i in data.json()["data"]
     if i["application_id"] == "1212122ed3d33d" or i["module_id"] == "wewewewedn3211"]
  context.url = f"{UM_API_URL}/permission/search"
  context.query_params = {"search_query": "create"}


@when("API request is sent for fetch all the permissions based on action name")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to fetch permissions
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """
  context.res = get_method(url=context.url, query_params=context.query_params)
  print(context.res)
  print(context.res.json())


@then("the permissions is failed to fetch for action name")
def step_impl_3(context: Context) -> None:
  """
  Assert the fetch permissions details
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """
  assert context.res.status_code == 200
  assert context.res.json()["success"] is True
  assert context.res.json()["message"] == "Successfully fetched the permissions"
  assert type(context.res.json()["data"]) is list


@given("fetch all the permissions for module name")
def step_impl_1(context: Context) -> None:
  """
  Construct query param to fetch permission details
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """

  context.url = f"{UM_API_URL}/permission/search"
  context.query_params = {"search_query": "admin"}


@when("API request is sent for fetch all the permissions based on module name")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to fetch permissions
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """
  context.res = get_method(url=context.url, query_params=context.query_params)


@then("the permissions is failed to fetch for module name")
def step_impl_3(context: Context) -> None:
  """
  Assert the fetch permissions details
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """
  assert context.res.status_code == 200
  assert context.res.json()["success"] is True
  assert context.res.json()[
    "message"] == "Successfully fetched the permissions"
  assert type(context.res.json()["data"]) is list


@given("fetch all the permissions for application name")
def step_impl_1(context: Context) -> None:
  """
  Construct query param to fetch permission details
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """

  context.url = f"{UM_API_URL}/permission/search"
  context.query_params = {"search_query": "random_name"}


@when("API request is sent for fetch all the permissions based on "
      "application name")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to fetch permissions
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """
  context.res = get_method(url=context.url, query_params=context.query_params)


@then("the permissions is failed to fetch for application name")
def step_impl_3(context: Context) -> None:
  """
  Assert the fetch permissions details
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """

  assert context.res.status_code == 200
  assert context.res.json()["success"] is True
  assert context.res.json()[
    "message"] == "Successfully fetched the permissions"
  assert type(context.res.json()["data"]) is list


@given("fetch all the permissions for permission name")
def step_impl_1(context: Context) -> None:
  """
  Construct query param to fetch permission details
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """
  context.url = f"{UM_API_URL}/permission/search"
  context.query_params = {"search_query": "admin"}


@when("API request is sent for fetch all the permissions based on "
      "permission name")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to fetch permissions
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """

  context.res = get_method(url=context.url, query_params=context.query_params)


@then("the permissions is failed to fetch for permission name")
def step_impl_3(context: Context) -> None:
  """
  Assert the fetch permissions details
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """

  assert context.res.status_code == 200
  assert context.res.json()["success"] is True
  assert context.res.json()[
    "message"] == "Successfully fetched the permissions"
  assert type(context.res.json()["data"]) is list


@given("fetch all the permissions for group name")
def step_impl_1(context: Context) -> None:
  """
  Construct query param to fetch permission details
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """

  context.url = f"{UM_API_URL}/permission/search"
  context.query_params = {"search_query": f"{group_name}"}


@when("API request is sent for fetch all the permissions based on group name")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to fetch permissions
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """
  context.res = get_method(url=context.url, query_params=context.query_params)


@then("the permissions is failed to fetch for group name")
def step_impl_3(context: Context) -> None:
  """
  Assert the fetch permissions details
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """
  assert context.res.status_code == 200
  assert context.res.json()["success"] is True
  assert context.res.json()[
    "message"] == "Successfully fetched the permissions"
  assert type(context.res.json()["data"]) is list


@given("fetch all the permissions for incorrect search query")
def step_impl_1(context: Context) -> None:
  """
  Construct query param to fetch permission details
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """
  context.url = f"{UM_API_URL}/permission/search"
  context.query_params = {"search_query": "Hello"}


@when("API request is sent for fetch all the permissions for incorrect "
      "search query")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to fetch permissions
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """
  context.res = get_method(url=context.url, query_params=context.query_params)


@then("the permissions is failed to fetch for incorrect search query")
def step_impl_3(context: Context) -> None:
  """
  Assert the fetch permissions details
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """

  assert context.res.status_code == 200
  assert context.res.json()["success"] is True
  assert context.res.json()[
    "message"] == "Successfully fetched the permissions"
  assert type(context.res.json()["data"]) is list


@given("user want to update their permission with correct permission ID")
def step_impl_1(context: Context) -> None:
  """
  Construct the request payload and query param to update the permission
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """

  action_dict = {**TEST_ACTION, "name": f"action-{uuid4()}"}
  action_res = post_method(url=f"{UM_API_URL}/action", request_body=action_dict)
  assert action_res.status_code == 200
  context.action_id = action_res.json().get("data").get("uuid")

  module_dict = {**TEST_MODULE, "name": f"module-{uuid4()}", "actions": [context.action_id]}
  module_res = post_method(url=f"{UM_API_URL}/module", request_body=module_dict)
  assert module_res.status_code == 200
  context.module_id = module_res.json().get("data").get("uuid")

  application_dict = {**TEST_APPLICATION, "modules": [context.module_id]}
  application_dict["name"] = str(uuid4())
  application_res = post_method(url=f"{UM_API_URL}/application", request_body=application_dict)
  assert application_res.status_code == 200
  context.application_id = application_res.json().get("data").get("uuid")

  context.permission_dict = {**TEST_PERMISSION, "name": f"{application_dict.get('name')}.{module_dict.get('name')}.{action_dict.get('name')}",
                      "application_id":context.application_id, "action_id":context.action_id, "module_id": context.module_id}
  del context.permission_dict["user_groups"]
  post_url = f"{UM_API_URL}/permission"
  post_permission = post_method(url=post_url,
                                request_body=context.permission_dict)
  context.permission_id = post_permission.json()["data"]["uuid"]

  assert post_permission.status_code == 200


@when("API request is sent to update permission with correct permission ID")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to update the permission with correct permission ID
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """
  update_req_body = {"name": "william"}
  context.url = f"{UM_API_URL}/permission/{context.permission_id}"
  context.res = put_method(url=context.url,
                           request_body=update_req_body)


@then("the permission has been updated successfully with correct permission ID")
def step_impl_3(context: Context) -> None:
  """
  Assert the Updated permission Response
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """

  assert context.res.status_code == 200
  assert context.res.json()["success"] is True
  assert context.res.json()["message"] == "Successfully updated the permission"
  assert context.res.json()["data"]["name"] == "william"


@given("user try to update their permission with incorrect permission ID")
def step_impl_1(context: Context) -> None:
  """
  Construct the request payload and incorrect query param to update the
  permission
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """

  context.permission_dict = {
    "name": "admin",
    "description": "Description for permission"
  }
  context.permission_id = "12322121we3"


@when("API request is sent to update the permission for incorrect permission "
      "ID")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to update the permission with incorrect permission ID
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """
  context.permission_dict["name"] = "william"
  context.url = f"{UM_API_URL}/permission/{context.permission_id}"
  context.res = put_method(url=context.url,
                           request_body=context.permission_dict)


@then("the permission has been failed to update with incorrect permission ID")
def step_impl_3(context: Context) -> None:
  """
  Assert the Updated Permission Response
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """

  assert context.res.status_code == 404
  assert context.res.json()["success"] is False
  assert context.res.json()["message"] == f"Permission with uuid " \
                                          f"{context.permission_id} not found"
  assert context.res.json()["data"] is None


@given("permission is fetch from the datastore with correct permission ID")
def step_impl_1(context: Context) -> None:
  """
  Construct query param to fetch permission details
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """
  action_dict = {**TEST_ACTION, "name": f"action-{uuid4()}"}
  action_res = post_method(url=f"{UM_API_URL}/action", request_body=action_dict)
  assert action_res.status_code == 200
  context.action_id = action_res.json().get("data").get("uuid")

  module_dict = {**TEST_MODULE, "name": f"module-{uuid4()}", "actions": [context.action_id]}
  module_res = post_method(url=f"{UM_API_URL}/module", request_body=module_dict)
  assert module_res.status_code == 200
  context.module_id = module_res.json().get("data").get("uuid")

  application_dict = {**TEST_APPLICATION, "modules": [context.module_id]}
  application_dict["name"] = str(uuid4())
  application_res = post_method(url=f"{UM_API_URL}/application", request_body=application_dict)
  assert application_res.status_code == 200
  context.application_id = application_res.json().get("data").get("uuid")

  context.permission_dict = {**TEST_PERMISSION, "name": f"{application_dict.get('name')}.{module_dict.get('name')}.{action_dict.get('name')}",
                      "application_id":context.application_id, "action_id":context.action_id, "module_id": context.module_id}
  del context.permission_dict["user_groups"]
  post_url = f"{UM_API_URL}/permission"
  post_permission = post_method(url=post_url,
                                request_body=context.permission_dict)
  context.permission_id = post_permission.json()["data"]["uuid"]

  assert post_permission.status_code == 200


@when("API request is sent to fetch the permission details with correct "
      "permission ID")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to fetch permission Based on permission ID
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """

  context.url = f"{UM_API_URL}/permission/{context.permission_id}"
  context.res = get_method(url=context.url)


@then("the permission is fetched successfully with correct permission ID")
def step_impl_3(context: Context) -> None:
  """
  Assert the fetch permission details
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """

  assert context.res.status_code == 200
  assert context.res.json()["success"] is True
  assert context.res.json()["message"] == "Successfully fetched the permission"
  assert context.res.json()["data"]["uuid"] == context.permission_id


@given("User try to fetch their permission with incorrect permission ID")
def step_impl_1(context: Context) -> None:
  """
  Construct query param to fetch permission details
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """

  context.permission_id = "121212314324jjj3r345"


@when("API request is sent to fetch the permission with incorrect permission "
      "ID")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to fetch permission Based on permission ID
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """

  context.url = f"{UM_API_URL}/permission/{context.permission_id}"
  context.res = get_method(url=context.url)


@then("the permission details is failed to fetch for incorrect permission ID")
def step_impl_3(context: Context) -> None:
  """
  Assert the fetch permission details
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """

  assert context.res.status_code == 404
  assert context.res.json()["success"] is False
  assert context.res.json()["message"] == f"Permission with uuid " \
                                          f"{context.permission_id} not found"
  assert context.res.json()["data"] is None


@given("fetch all the permissions from the datastore")
def step_impl_1(context: Context) -> None:
  """
  Construct query param to fetch permission details
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """
  context.url= f"{UM_API_URL}/permissions"


@when("API request is sent to fetch all the permissions")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to fetch permissions
  Params
  ------
  context: behave.runner.Context
  Returns
  -------
  None
  """
  context.query_params = {"skip": "0", "limit": "10"}
  context.res = get_method(url=context.url, query_params=context.query_params)


@then("the permissions is fetched successfully")
def step_impl_3(context: Context) -> None:
  """
  Assert the fetch permissions details
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


@given("fetch all the permissions from the datastore for a given application_id")
def step_impl_1(context: Context) -> None:
  """
  Construct query param to fetch permission details for a given application_id
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """
  action_dict = {**TEST_ACTION, "name": str(uuid4())}
  action_url = f"{UM_API_URL}/action"
  action_res = post_method(url=action_url, request_body=action_dict)
  action_data = action_res.json()["data"]
  action_id = action_data["uuid"]

  module_dict = {**TEST_MODULE, "name": str(uuid4())}
  module_dict["actions"] = [action_id]
  module_url = f"{UM_API_URL}/module"
  module_res = post_method(url=module_url, request_body=module_dict)
  module_id = module_res.json()["data"]["uuid"]

  app_dict = {**TEST_APPLICATION, "name": str(uuid4())}
  app_dict["modules"] = [module_id]
  app_url = f"{UM_API_URL}/application"
  app_res = post_method(url=app_url, request_body=app_dict)
  app_id = app_res.json()["data"]["uuid"]

  group_dict = {**TEST_USER_GROUP, "name": f"{uuid4()}"}
  post_group = post_method(url=f"{UM_API_URL}/user-group",
                           request_body=group_dict)
  post_group_data = post_group.json()
  context.group_uuid = post_group_data["data"]["uuid"]

  context.permission_dict = {**TEST_PERMISSION, "application_id": app_id, "module_id": module_id,
    "action_id": action_id}
  del context.permission_dict["user_groups"]

  post_url = f"{UM_API_URL}/permission"
  post_permission = post_method(url=post_url,
                                request_body=context.permission_dict)

  assert post_permission.status_code == 200


@when("API request is sent to fetch all the permissions for a given application_id")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to fetch permissions for a given application_id
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """
  context.url = f"{UM_API_URL}/permissions"
  context.query_params = {"skip": "0", "limit": "10",
                      "application_id": context.permission_dict["application_id"]}
  context.res = get_method(url=context.url, query_params=context.query_params)


@then("the permissions for given application_id are fetched successfully")
def step_impl_3(context: Context) -> None:
  """
  Assert the fetched permissions details
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
  assert context.res.json()["data"][0][
    "application_id"] == context.permission_dict["application_id"]

@given("fetch all the permissions for incorrect query params")
def step_impl_1(context: Context) -> None:
  """
  Construct query param to fetch permissions details
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  context.url = f"{UM_API_URL}/permissions"
  context.query_params = {"skip": "-1", "limit": "10"}


@when("API request is sent for fetch all the permissions with incorrect query "
      "params")
def step_impl_2(context: Context) -> None:
  """
  Sent API request to fetch permissions
  Params
  ------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  context.res = get_method(url=context.url, query_params=context.query_params)


@then("the permissions is failed to fetch for incorrect query params")
def step_impl_3(context: Context) -> None:
  """
  Assert the fetch permissions details
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


@given("A user has access to User management and needs to delete a permission")
def step_impl_1(context):
  user_group_dict = {**TEST_USER_GROUP, "name": f"{uuid4()}"}
  user_group_url = f"{UM_API_URL}/user-group"
  post_user_group_res = post_method(url=user_group_url,
                                    request_body=user_group_dict)
  context.user_group_id = post_user_group_res.json()["data"]["uuid"]

  action_dict = {**TEST_ACTION, "name": f"action-{uuid4()}"}
  action_res = post_method(url=f"{UM_API_URL}/action", request_body=action_dict)
  assert action_res.status_code == 200
  context.action_id = action_res.json().get("data").get("uuid")

  module_dict = {**TEST_MODULE, "name": f"module-{uuid4()}", "actions": [context.action_id]}
  module_res = post_method(url=f"{UM_API_URL}/module", request_body=module_dict)
  assert module_res.status_code == 200
  context.module_id = module_res.json().get("data").get("uuid")

  application_dict = {**TEST_APPLICATION, "modules": [context.module_id]}
  application_dict["name"] = str(uuid4())
  application_res = post_method(url=f"{UM_API_URL}/application", request_body=application_dict)
  assert application_res.status_code == 200
  context.application_id = application_res.json().get("data").get("uuid")

  context.permission_dict = {**TEST_PERMISSION, "name": f"{application_dict.get('name')}.{module_dict.get('name')}.{action_dict.get('name')}",
                      "application_id":context.application_id, "action_id":context.action_id, "module_id": context.module_id,
                      }
  del context.permission_dict["user_groups"]
  post_application = post_method(
    url=f"{UM_API_URL}/permission", request_body=context.permission_dict)
  context.post_permission_data = post_application.json()
  context.permission_uuid = context.post_permission_data["data"]["uuid"]
  assert post_application.status_code == 200

  #TODO:
  # update_user_group = put_method(
  #     url=f"{UM_API_URL}/user-group/{context.user_group_id}",
  #     request_body=updated_user_group_data)
  # assert update_user_group.status_code == 200


@when("API request is sent to delete permission by providing correct uuid")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/permission/{context.permission_uuid}"
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()


@then("permission object will be deleted successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is True"
  assert context.res_data["message"] == "Successfully deleted the permission"


# @then("And the deleted permission is unassigned from all the user groups")
# def step_impl_3(context):
#   get_user_group_res = get_method(
#     url=f"{UM_API_URL}/user-group/{context.user_group_id}")
#   get_user_group_res_data = get_user_group_res.json()
#   assert get_user_group_res.status_code == 200
#   assert get_user_group_res_data["data"]["permissions"] == []

# --- Positive Scenario 1 ---
@given("A user has access to User management and needs to fetch all permissions using valid application id")
def step_impl_1(context):
  application_url = f"{UM_API_URL}/application"
  application_dict = deepcopy(TEST_APPLICATION)
  application_dict["name"] = f"app-{uuid4()}"
  post_application = post_method(
    url=application_url,
    request_body=application_dict
  )
  post_application_res = post_application.json()
  context.application_id = post_application_res["data"]["uuid"]
  assert post_application.status_code == 200

  module_url = f"{UM_API_URL}/module"
  module_dict = deepcopy(TEST_MODULE)
  module_dict["name"] = f"module-{uuid4()}"
  post_module = post_method(
    url=module_url,
    request_body=module_dict
  )
  post_module_res = post_module.json()
  context.module_id = post_module_res["data"]["uuid"]
  assert post_module.status_code == 200

  action_url = f"{UM_API_URL}/action"
  action_dict = deepcopy(TEST_ACTION)
  action_dict["name"] = f"action-{uuid4()}"
  post_action = post_method(
    url=action_url,
    request_body=action_dict
  )
  post_action_res = post_action.json()
  context.action_id = post_action_res["data"]["uuid"]
  assert post_action.status_code == 200

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


@when("API request is sent to fetch permissions by providing valid application id")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/permissions"
  params = {
    "skip": 0,
    "limit": 10,
    "application_ids": context.application_id
  }
  context.res = get_method(url=context.url, query_params=params)
  context.res_data = context.res.json()

@then("API will return a list of permissions based on the provided application id")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Data fetched successfully"
  assert len(context.res_data["data"]) == 1


# --- Positive Scenario 2 ---
@given("A user has access to User management and needs to fetch all permissions using valid user group id")
def step_impl_1(context):
  user_group_url = f"{UM_API_URL}/user-group"
  user_group_dict = deepcopy(TEST_USER_GROUP)
  user_group_dict["name"] = f"ug-{uuid4()}"
  post_user_group = post_method(
    url=user_group_url,
    request_body=user_group_dict
  )
  post_user_group_res = post_user_group.json()
  context.user_group_id = post_user_group_res["data"]["uuid"]
  assert post_user_group.status_code == 200

  application_url = f"{UM_API_URL}/application"
  application_dict = deepcopy(TEST_APPLICATION)
  application_dict["name"] = f"app-{uuid4()}"
  post_application = post_method(
    url=application_url,
    request_body=application_dict
  )
  post_application_res = post_application.json()
  context.application_id = post_application_res["data"]["uuid"]
  assert post_application.status_code == 200

  module_url = f"{UM_API_URL}/module"
  module_dict = deepcopy(TEST_MODULE)
  module_dict["name"] = f"module-{uuid4()}"
  post_module = post_method(
    url=module_url,
    request_body=module_dict
  )
  post_module_res = post_module.json()
  context.module_id = post_module_res["data"]["uuid"]
  assert post_module.status_code == 200

  action_url = f"{UM_API_URL}/action"
  action_dict = deepcopy(TEST_ACTION)
  action_dict["name"] = f"action-{uuid4()}"
  post_action = post_method(
    url=action_url,
    request_body=action_dict
  )
  post_action_res = post_action.json()
  context.action_id = post_action_res["data"]["uuid"]
  assert post_action.status_code == 200

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
  post_permission_res = post_permission.json()
  context.permission_id = post_permission_res["data"]["uuid"]
  assert post_permission.status_code == 200

  # add application to user group
  ug_application_url = f"{UM_API_URL}/user-group/{context.user_group_id}/applications"
  req_body = {
    "applications": [context.application_id],
      "action_id": context.action_id
  }
  ug_application = put_method(
    url=ug_application_url,
    request_body= req_body
  )
  assert ug_application.status_code == 200

  # add user group to permission
  ug_permission_url = f"{UM_API_URL}/user-group/{context.user_group_id}/application/{context.application_id}/permissions"
  ug_permission_dict = {
      "permission_ids": [ context.permission_id ]
  }
  post_ug_permission = post_method(
    url = ug_permission_url,
    request_body= ug_permission_dict
  )
  assert post_ug_permission.status_code == 200

@when("API request is sent to fetch permissions by providing valid user group id")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/permissions"
  params = {
    "skip": 0,
    "limit": 10,
    "user_groups": context.user_group_id
  }
  context.res = get_method(url=context.url, query_params=params)
  context.res_data = context.res.json()


@then("API will return a list of permissions based on the provided user group id")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Data fetched successfully"
  assert len(context.res_data["data"]) == 1


# --- Positive Scenario 3 ---
@given("A user has access to User management and needs to fetch all permissions using valid application, module and action ids")
def step_impl_1(context):
  application_url = f"{UM_API_URL}/application"
  application_dict = deepcopy(TEST_APPLICATION)
  application_dict["name"] = f"app-{uuid4()}"
  post_application = post_method(
    url=application_url,
    request_body=application_dict
  )
  post_application_res = post_application.json()
  context.application_id = post_application_res["data"]["uuid"]
  assert post_application.status_code == 200

  application_url = f"{UM_API_URL}/application"
  application_dict = deepcopy(TEST_APPLICATION)
  application_dict["name"] = f"app-{uuid4()}"
  post_application = post_method(
    url=application_url,
    request_body=application_dict
  )
  post_application_res = post_application.json()
  context.application_id2 = post_application_res["data"]["uuid"]
  assert post_application.status_code == 200

  module_url = f"{UM_API_URL}/module"
  module_dict = deepcopy(TEST_MODULE)
  module_dict["name"] = f"module-{uuid4()}"
  post_module = post_method(
    url=module_url,
    request_body=module_dict
  )
  post_module_res = post_module.json()
  context.module_id = post_module_res["data"]["uuid"]
  assert post_module.status_code == 200

  module_url = f"{UM_API_URL}/module"
  module_dict = deepcopy(TEST_MODULE)
  module_dict["name"] = f"module-{uuid4()}"
  post_module = post_method(
    url=module_url,
    request_body=module_dict
  )
  post_module_res = post_module.json()
  context.module_id2 = post_module_res["data"]["uuid"]
  assert post_module.status_code == 200

  action_url = f"{UM_API_URL}/action"
  action_dict = deepcopy(TEST_ACTION)
  action_dict["name"] = f"action-{uuid4()}"
  post_action = post_method(
    url=action_url,
    request_body=action_dict
  )
  post_action_res = post_action.json()
  context.action_id = post_action_res["data"]["uuid"]
  assert post_action.status_code == 200

  action_url = f"{UM_API_URL}/action"
  action_dict = deepcopy(TEST_ACTION)
  action_dict["name"] = f"action-{uuid4()}"
  post_action = post_method(
    url=action_url,
    request_body=action_dict
  )
  post_action_res = post_action.json()
  context.action_id2 = post_action_res["data"]["uuid"]
  assert post_action.status_code == 200

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

  permission_url = f"{UM_API_URL}/permission"
  permission_dict = deepcopy(TEST_PERMISSION)
  permission_dict["application_id"] = context.application_id2
  permission_dict["module_id"] = context.module_id2
  permission_dict["action_id"] = context.action_id2
  del permission_dict["user_groups"]
  post_permission = post_method(
    url=permission_url,
    request_body=permission_dict
  )
  assert post_permission.status_code == 200


@when("API request is sent to fetch permissions by providing valid application, module and action ids")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/permissions"
  params = {
    "skip": 0,
    "limit": 10,
    "application_ids": context.application_id + context.application_id2,
    "module_ids": context.module_id + context.module_id2,
    "action_ids": context.action_id + context.action_id2,
  }
  context.res = get_method(url=context.url, query_params=params)
  context.res_data = context.res.json()


@then("API will return a list of permissions based on the provided ids")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Data fetched successfully"
  assert len(context.res_data["data"]) == 2


# --- Negative Scenario 1 ---
@given("A user has access to User management and needs to fetch all permissions using valid user group id and invalid module id")
def step_impl_1(context):
  application_url = f"{UM_API_URL}/application"
  application_dict = deepcopy(TEST_APPLICATION)
  application_dict["name"] = f"app-{uuid4()}"
  post_application = post_method(
    url=application_url,
    request_body=application_dict
  )
  post_application_res = post_application.json()
  context.application_id = post_application_res["data"]["uuid"]
  assert post_application.status_code == 200

  module_url = f"{UM_API_URL}/module"
  module_dict = deepcopy(TEST_MODULE)
  module_dict["name"] = f"module-{uuid4()}"
  post_module = post_method(
    url=module_url,
    request_body=module_dict
  )
  post_module_res = post_module.json()
  context.module_id = post_module_res["data"]["uuid"]
  assert post_module.status_code == 200

  action_url = f"{UM_API_URL}/action"
  action_dict = deepcopy(TEST_ACTION)
  action_dict["name"] = f"action-{uuid4()}"
  post_action = post_method(
    url=action_url,
    request_body=action_dict
  )
  post_action_res = post_action.json()
  context.action_id = post_action_res["data"]["uuid"]
  assert post_action.status_code == 200

  user_group_url = f"{UM_API_URL}/user-group"
  user_group_dict = deepcopy(TEST_USER_GROUP)
  user_group_dict["name"] = f"ug-{uuid4()}"
  post_user_group = post_method(
    url=user_group_url,
    request_body=user_group_dict
  )
  post_user_group_res = post_user_group.json()
  context.user_group_id = post_user_group_res["data"]["uuid"]
  assert post_user_group.status_code == 200

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
  post_permission_res = post_permission.json()
  context.permission_id = post_permission_res["data"]["uuid"]
  assert post_permission.status_code == 200

  # add application to user group
  ug_application_url = f"{UM_API_URL}/user-group/{context.user_group_id}/applications"
  req_body = {
    "applications": [context.application_id],
      "action_id": context.action_id
  }
  ug_application = put_method(
    url=ug_application_url,
    request_body= req_body
  )
  assert ug_application.status_code == 200

  # add user group to permission
  ug_permission_url = f"{UM_API_URL}/user-group/{context.user_group_id}/application/{context.application_id}/permissions"
  ug_permission_dict = {
      "permission_ids": [ context.permission_id ]
  }
  post_ug_permission = post_method(
    url = ug_permission_url,
    request_body= ug_permission_dict
  )
  assert post_ug_permission.status_code == 200

@when("API request is sent to fetch permissions by providing valid user group id and invalid module id")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/permissions"
  params = {
    "skip": 0,
    "limit": 10,
    "module_ids": "invalid_module_id",
    "user_groups": context.user_group_id
  }
  context.res = get_method(url=context.url, query_params=params)
  context.res_data = context.res.json()


@then("API will return an empty list of permissions based on the provided user group and module ids")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Data fetched successfully"
  assert len(context.res_data["data"]) == 0


# --- Negative Scenario 2 ---
@given("A user has access to User management and needs to fetch all permissions using invalid user group id and valid action id")
def step_impl_1(context):
  application_url = f"{UM_API_URL}/application"
  application_dict = deepcopy(TEST_APPLICATION)
  application_dict["name"] = f"app-{uuid4()}"
  post_application = post_method(
    url=application_url,
    request_body=application_dict
  )
  post_application_res = post_application.json()
  context.application_id = post_application_res["data"]["uuid"]
  assert post_application.status_code == 200

  module_url = f"{UM_API_URL}/module"
  module_dict = deepcopy(TEST_MODULE)
  module_dict["name"] = f"module-{uuid4()}"
  post_module = post_method(
    url=module_url,
    request_body=module_dict
  )
  post_module_res = post_module.json()
  context.module_id = post_module_res["data"]["uuid"]
  assert post_module.status_code == 200

  action_url = f"{UM_API_URL}/action"
  action_dict = deepcopy(TEST_ACTION)
  action_dict["name"] = f"action-{uuid4()}"
  post_action = post_method(
    url=action_url,
    request_body=action_dict
  )
  post_action_res = post_action.json()
  context.action_id = post_action_res["data"]["uuid"]
  assert post_action.status_code == 200

  user_group_url = f"{UM_API_URL}/user-group"
  user_group_dict = deepcopy(TEST_USER_GROUP)
  user_group_dict["name"] = f"ug-{uuid4()}"
  post_user_group = post_method(
    url=user_group_url,
    request_body=user_group_dict
  )
  post_user_group_res = post_user_group.json()
  context.user_group_id = post_user_group_res["data"]["uuid"]
  assert post_user_group.status_code == 200

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


@when("API request is sent to fetch permissions by providing invalid user group id and valid action id")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/permissions"
  params = {
    "skip": 0,
    "limit": 10,
    "action_ids": context.action_id,
    "user_groups": "invalid_ug_id"
  }
  context.res = get_method(url=context.url, query_params=params)
  context.res_data = context.res.json()


@then("API will return an empty list of permissions based on the provided user group and action ids")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Data fetched successfully"
  assert len(context.res_data["data"]) == 0


# --- Negative Scenario 3 ---
@given("A user has access to User management and needs to fetch all permissions using invalid application, module and action ids")
def step_impl_1(context):
  application_url = f"{UM_API_URL}/application"
  application_dict = deepcopy(TEST_APPLICATION)
  application_dict["name"] = f"app-{uuid4()}"
  post_application = post_method(
    url=application_url,
    request_body=application_dict
  )
  post_application_res = post_application.json()
  context.application_id = post_application_res["data"]["uuid"]
  assert post_application.status_code == 200

  module_url = f"{UM_API_URL}/module"
  module_dict = deepcopy(TEST_MODULE)
  module_dict["name"] = f"module-{uuid4()}"
  post_module = post_method(
    url=module_url,
    request_body=module_dict
  )
  post_module_res = post_module.json()
  context.module_id = post_module_res["data"]["uuid"]
  assert post_module.status_code == 200

  action_url = f"{UM_API_URL}/action"
  action_dict = deepcopy(TEST_ACTION)
  action_dict["name"] = f"action-{uuid4()}"
  post_action = post_method(
    url=action_url,
    request_body=action_dict
  )
  post_action_res = post_action.json()
  context.action_id = post_action_res["data"]["uuid"]
  assert post_action.status_code == 200

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


@when("API request is sent to fetch permissions by providing invalid application, module and action ids")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/permissions"
  params = {
    "skip": 0,
    "limit": 10,
    "application_ids": "random_application_id",
    "module_ids": "random_module_id",
    "action_ids": "random_action_id",
  }
  context.res = get_method(url=context.url, query_params=params)
  context.res_data = context.res.json()


@then("API will return an empty list of permissions based on the provided ids")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Data fetched successfully"
  assert len(context.res_data["data"]) == 0

@given("Retrieve all unique applications, modules, actions and user groups")
def step_impl_1(context):
  action_dict = {**TEST_ACTION, "name": f"action-{uuid4()}"}
  action_res = post_method(url=f"{UM_API_URL}/action", request_body=action_dict)
  assert action_res.status_code == 200
  context.action_id = action_res.json().get("data").get("uuid")

  module_dict = {**TEST_MODULE, "name": f"module-{uuid4()}", "actions": [context.action_id]}
  module_res = post_method(url=f"{UM_API_URL}/module", request_body=module_dict)
  assert module_res.status_code == 200
  context.module_id = module_res.json().get("data").get("uuid")

  application_dict = {**TEST_APPLICATION, "modules": [context.module_id]}
  application_dict["name"] = str(uuid4())
  application_res = post_method(url=f"{UM_API_URL}/application", request_body=application_dict)
  assert application_res.status_code == 200

@when("API request is sent to fetch unique records")
def step_impl_2(context):
  url = f"{UM_API_URL}/permission_filter/unique"
  unique_records = get_method(url)
  print(unique_records)
  context.unique_records_res = unique_records.json()

@then("Object will be returned with unique values")
def step_impl_3(context):
  assert context.unique_records_res["success"] is True
  assert context.unique_records_res["message"] == "Successfully fetched the unique values for applications, modules, actions and user_groups."
