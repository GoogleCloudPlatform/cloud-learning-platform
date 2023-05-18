"""
Feature: Grant Access to an Application for a UserGroup
"""
import behave
import sys
from uuid import uuid4

sys.path.append("../")
from common.models import UserGroup
from test_object_schemas import TEST_APPLICATION, TEST_MODULE, TEST_USER, TEST_USER_GROUP, TEST_ACTION, TEST_PERMISSION
from test_config import (API_URL_USER_MANAGEMENT as UM_API_URL)
from setup import post_method, get_method, put_method
'''
Scenario: Grant Access to an Application for a UserGroup
'''

@behave.given(
    "A UserGroup and an application already exists and Admin wants to grant access for the UserGroup to the application")
def step_impl_1(context):

    group_dict = {**TEST_USER_GROUP, "name": "lxe"}
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

    user_dict = {**TEST_USER, "user_groups":[context.group_id], "user_type": "lxe"}
    user_dict["email"] = f"{str(uuid4())}@gmail.com"
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

    context.url = f"{UM_API_URL}/user-group/{context.group_id}/applications"




@behave.when("API request is sent to link application to a UserGroup")
def step_impl_2(context):
    update_applications_req_body = {"applications":[context.application_id], "action_id": context.action_id}
    context.res = put_method(url=context.url, request_body=update_applications_req_body)
    context.res_data = context.res.json()


@behave.then("the UserGroup document will hold reference to the application")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_data["message"] == "Successfully updated applications of a user group"
    assert context.application_id in context.res_data["data"]["applications"]
    assert context.permission_id in context.res_data["data"]["permissions"]

@behave.then("the users belong to the UserGroup have access to the linked application")
def step_impl_3(context):
    get_applications_assigned_to_user = get_method(url = f"{UM_API_URL}/user/{context.user_id}/applications")
    assert get_applications_assigned_to_user.status_code == 200
    applications_of_user_res = get_applications_assigned_to_user.json()
    applications_of_user = [i.get("application_id") for i in applications_of_user_res.get("data").get("applications")]
    assert context.application_id in applications_of_user

'''
Scenario: A UserGroup should not get access to an invalid Application
'''

@behave.given(
    "A UserGroup already exists and Admin wants to link UserGroup to an invalid application")
def step_impl_1(context):

    group_dict = {**TEST_USER_GROUP, "name": f"{uuid4()}"}
    group_res = post_method(url=f"{UM_API_URL}/user-group", request_body=group_dict)
    context.group_id = group_res.json().get("data").get("uuid")


    context.url = f"{UM_API_URL}/user-group/{context.group_id}/applications"

@behave.when("API request is sent to link invalis application to a UserGroup")
def step_impl_2(context):
    update_applications_req_body = {"applications":["random_application_id"], "action_id": "random_id"}
    context.res = put_method(url=context.url, request_body=update_applications_req_body)
    context.res_data = context.res.json()


@behave.then("Resource not found exception for application will be thrown by the user management")
def step_impl_3(context):
    assert context.res.status_code == 404
    assert context.res_data["message"] == "Application with uuid random_application_id not found"

'''
Scenario: An invalid UserGroup should not get access to an Application
'''

@behave.given(
    "A UserGroup doesn't exists and Admin wants to give access to a invalid UserGroup to an application")
def step_impl_1(context):

    context.group_id = "random_group_id"


    context.url = f"{UM_API_URL}/user-group/{context.group_id}/applications"

@behave.when("API request is sent to link application to a invalid UserGroup")
def step_impl_2(context):
    update_applications_req_body = {"applications":["random_application_id"], "action_id":"random"}
    context.res = put_method(url=context.url, request_body=update_applications_req_body)
    context.res_data = context.res.json()


@behave.then("Resource not found exception for UserGroup will be thrown by the user management")
def step_impl_3(context):
    assert context.res.status_code == 404
    assert context.res_data["message"] == f"UserGroup with uuid {context.group_id} not found"
