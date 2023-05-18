"""
Feature: CRUD for managing Application in user management
"""
import behave
import sys
from uuid import uuid4

sys.path.append("../")
from common.models import UserGroup, Action, Module
from test_object_schemas import TEST_ACTION, TEST_APPLICATION, TEST_MODULE, \
  TEST_PERMISSION, TEST_USER, TEST_USER_GROUP
from test_config import (API_URL_USER_MANAGEMENT as UM_API_URL)
from setup import post_method, get_method, put_method, delete_method


@behave.given(
    "A user has permission to user management and wants to create a Application")
def step_impl_1(context):
  action_dict = {**TEST_ACTION, "name": "view"}
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()

  module_dict = {**TEST_MODULE}
  module = Module.from_dict(module_dict)
  module.uuid = ""
  module.save()
  module.uuid = module.id
  module.update()

  context.application_dict = {**TEST_APPLICATION,
                              "name": f"Application - {uuid4()}",
                              "modules": [module.id]}


@behave.when("API request is sent to create Application with correct request payload")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/application"

  context.res = post_method(url=context.url, request_body=context.application_dict)
  context.res_data = context.res.json()


@behave.then("that Application object will be created in the database")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["message"] == "Successfully created the application"
  application_uuid = context.res_data["data"]["uuid"]
  url = f"{UM_API_URL}/application/{application_uuid}"
  request = get_method(url)
  application_data = request.json()
  assert request.status_code == 200
  assert application_data["message"] == "Successfully fetched the application"
  assert application_data["data"]["name"] == context.application_dict["name"]


@behave.given(
    "A user has permission to user management and wants to create a Application with incorrect payload"
)
def step_impl_1(context):
  context.payload = {**TEST_APPLICATION}
  del context.payload["name"]
  context.url = f"{UM_API_URL}/application"


@behave.when(
    "API request is sent to create Application with incorrect request payload")
def step_impl_2(context):
  context.res = post_method(url=context.url, request_body=context.payload)
  context.res_data = context.res.json()


@behave.then(
    "that Application object will not be created and a validation error is thrown")
def step_impl_3(context):
  assert context.res.status_code == 422
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Validation Failed"
  assert context.res_data["data"][0]["msg"] == "field required"
  assert context.res_data["data"][0]["type"] == "value_error.missing"

@behave.given(
    "A user has access privileges to User management and needs to fetch a Application"
)
def step_impl_1(context):
  context.application_dict = {**TEST_APPLICATION}
  context.application_dict["name"] = f"Application - {uuid4()}"

  post_application = post_method(
      url=f"{UM_API_URL}/application", request_body=context.application_dict)
  context.post_application_data = post_application.json()
  context.application_uuid = context.post_application_data["data"]["uuid"]
  assert post_application.status_code == 200


@behave.when("API request is sent to fetch Application by providing correct uuid")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/application/{context.application_uuid}"
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then(
    "Application object corresponding to given uuid will be returned successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["message"] == "Successfully fetched the application"
  assert context.res_data["data"] == context.post_application_data["data"]


@behave.given("A user has permission to user management and wants to create a Application with name already existing in database")
def step_impl_1(context):
  context.application_dict = {**TEST_APPLICATION}
  context.application_dict["name"] = f"Application - {uuid4()}"
  context.url=f"{UM_API_URL}/application"

  post_application = post_method(
      url=context.url, request_body=context.application_dict)
  post_application_data = post_application.json()
  context.application_name = post_application_data["data"]["name"]
  assert post_application.status_code == 200

@behave.when("API request is sent to create Application with name already existing in database")
def step_impl_2(context):
  context.res = post_method(url=context.url, request_body=context.application_dict)
  context.res_data = context.res.json()


@behave.then("Application object will not be created and a conflict error is thrown")
def step_impl_3(context):
  assert context.res.status_code == 409
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == \
    f"Application with the given name: {context.application_name} already exists"

@behave.given("A user has access to User management and needs to fetch a Application")
def step_impl_1(context):
  invalid_application_uuid = "random_id"
  context.url = f"{UM_API_URL}/application/{invalid_application_uuid}"


@behave.when("API request is sent to fetch Application by providing invalid uuid")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then(
    "Application object will not be returned and Resource not found error will be thrown by User management"
)
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data[
      "message"] == "Application with uuid random_id not found", "Expected message not returned"


@behave.given(
    "A user has access to User management and needs to fetch all Applications")
def step_impl_1(context):
  context.application_dict = {**TEST_APPLICATION}
  context.application_dict["name"] = f"Application - {uuid4()}"

  post_application = post_method(
      url=f"{UM_API_URL}/application", request_body=context.application_dict)
  context.post_application_data = post_application.json()
  context.application_uuid = context.post_application_data["data"]["uuid"]
  assert post_application.status_code == 200
  context.url = f"{UM_API_URL}/applications"


@behave.when("API request is sent to fetch all Applications")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then(
    "User management will return all existing Application objects successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["message"] == "Data fetched successfully"
  fetched_uuids = [i.get(
    "uuid") for i in context.res_data.get("data")["records"]]
  assert context.application_uuid in fetched_uuids


@behave.given("A user can access User management and needs to fetch all Applications")
def step_impl_1(context):
  context.url = f"{UM_API_URL}/applications"
  context.params = params = {"skip": "-1", "limit": "10"}


@behave.when(
    "API request is sent to fetch all Applications with incorrect request payload")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()


@behave.then(
    "The Applications will not be fetched and User management will throw a Validation error"
)
def step_impl_3(context):
  assert context.res.status_code == 422, "Status not 422"
  assert context.res_data.get("message") == \
    "Validation Failed", \
    "unknown response received"


@behave.given("A user has access to User management and needs "
              "to update a Application")
def step_impl_1(context):
  action_dict = {**TEST_ACTION, "name": "view"}
  action = Action.from_dict(action_dict)
  action.uuid = ""
  action.save()
  action.uuid = action.id
  action.update()

  module_dict = {**TEST_MODULE}
  module = Module.from_dict(module_dict)
  module.uuid = ""
  module.save()
  module.uuid = module.id
  module.update()

  context.application_dict = {**TEST_APPLICATION,
                              "name": f"Application - {uuid4()}",
                              "modules": [module.id]}

  post_application = post_method(
      url=f"{UM_API_URL}/application", request_body=context.application_dict)
  context.post_application_data = post_application.json()
  context.application_uuid = context.post_application_data["data"]["uuid"]
  assert post_application.status_code == 200


@behave.when("API request is sent to update Application with correct request payload")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/application/{context.application_uuid}"
  context.application_dict["name"] = f"Application - {uuid4()}"
  updated_data = context.application_dict
  updated_data["description"] = "updated description"
  context.res = put_method(url=context.url, request_body=updated_data)
  context.res_data = context.res.json()


@behave.then("Application object will be updated successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully updated the application"
  assert context.res_data["data"]["description"] == "updated description"


@behave.given(
    "A user has access to User management and needs to update users in a Application")
def step_impl_1(context):
  context.application_dict = {**TEST_APPLICATION}
  context.application_dict["name"] = f"Application - {uuid4()}"

  post_application = post_method(
      url=f"{UM_API_URL}/application", request_body=context.application_dict)
  context.post_application_data = post_application.json()
  context.application_uuid = context.post_application_data["data"]["uuid"]
  assert post_application.status_code == 200


@behave.when("API request is sent to update users in a Application with incorrect payload")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/application/{context.application_uuid}"
  incorrect_payload = {"email" : "exam@example.com"}
  context.res = put_method(url=context.url, request_body=incorrect_payload)
  context.res_data = context.res.json()


@behave.then("Users in Application object will not be updated")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False


@behave.given(
    "A user has access privileges to User management and needs to update a Application"
)
def step_impl_1(context):
  invalid_application_uuid = "random_id"
  context.url = f"{UM_API_URL}/application/{invalid_application_uuid}"


@behave.when("API request is sent to update Application by providing invalid uuid")
def step_impl_2(context):
  correct_payload = {**TEST_APPLICATION}
  correct_payload["name"] = f"Application - {uuid4()}"
  context.res = put_method(url=context.url, request_body=correct_payload)
  context.res_data = context.res.json()


@behave.then(
    "Application object will not be updated and User management will throw a resource not found error"
)
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Application with uuid random_id not found"


@behave.given("A user has access to User management and needs to delete a Application and usergroups have access to the application"
             )
def step_impl_1(context):

  group_dict = {**TEST_USER_GROUP, "name": "curriculum_designer"}
  group_res = post_method(url=f"{UM_API_URL}/user-group/immutable", request_body=group_dict)
  group_res_data = group_res.json()
  assert group_res.status_code in [200, 409]
  if group_res.status_code == 200:
    context.group_id = group_res_data["data"]["uuid"]
  if group_res.status_code == 409:
    user_group = UserGroup.find_by_name(group_dict["name"])
    user_group.is_immutable = True
    user_group.update()
    context.group_id = user_group.id

  user_dict = {**TEST_USER, "user_groups":[context.group_id], "user_type": "curriculum_designer"}
  user_dict["email"] = f"{uuid4()}@gmail.com"
  user_res = post_method(
      url= f"{UM_API_URL}/user",
      request_body= user_dict
  )
  context.user_id = user_res.json().get("data").get("user_id")

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

  permission_dict = {**TEST_PERMISSION, "name": f"{application_dict.get('name')}.{module_dict.get('name')}.{action_dict.get('name')}",
                      "application_id":context.application_id, "action_id":context.action_id, "module_id": context.module_id}
  del permission_dict["user_groups"]
  
  permission_res = post_method(url=f"{UM_API_URL}/permission", request_body=permission_dict)
  assert permission_res.status_code == 200
  context.permission_id = permission_res.json().get("data").get("uuid")

  update_applications_req_body = {"applications":[context.application_id], "action_id": context.action_id}
  update_group_with_applications = put_method(url=f"{UM_API_URL}/user-group/{context.group_id}/applications", request_body=update_applications_req_body)
  
  assert update_group_with_applications.status_code == 200
  updated_group = update_group_with_applications.json()["data"]
  assert context.application_id in updated_group["applications"]
  assert context.permission_id in updated_group["permissions"]

@behave.when("API request is sent to delete Application by providing correct uuid")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/application/{context.application_id}"
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("the reference of deleted Applicationis removed from usergroups")
def step_impl_3(context):
  get_user_group = get_method(url=f"{UM_API_URL}/user-group/{context.group_id}")
  assert get_user_group.status_code == 200
  user_group_res = get_user_group.json()
  
  assert user_group_res["success"] is True, "Success is not True"
  assert context.permission_id not in user_group_res["data"]["permissions"]

@behave.then("the permissions related to the application are also deleted")
def step_impl_3(context):
  get_permission = get_method(url=f"{UM_API_URL}/permission/{context.group_id}")
  assert get_permission.status_code == 404


@behave.then("Application object will be deleted successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully deleted the application"


@behave.given(
    "A user has access privileges to User management and needs to delete a Application"
)
def step_impl_1(context):
  invalid_application_uuid = "random_id"
  context.url = f"{UM_API_URL}/application/{invalid_application_uuid}"


@behave.when("API request is sent to delete Application by providing invalid uuid")
def step_impl_2(context):
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()


@behave.then(
    "Application object will not be deleted and User management will throw a resource not found error"
)
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Application with uuid random_id not found"