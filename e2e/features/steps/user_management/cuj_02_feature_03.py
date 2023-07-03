"""
Feature: Update permissions related to an application for a UserGroup
"""
import behave
import sys
from uuid import uuid4

sys.path.append("../")
from e2e.test_object_schemas import TEST_APPLICATION, TEST_MODULE, TEST_USER, TEST_USER_GROUP, TEST_ACTION, TEST_PERMISSION
from e2e.test_config import (API_URL_USER_MANAGEMENT as UM_API_URL)
from e2e.setup import post_method, get_method, put_method
'''
Scenario: Update permissions related to an assigned application for a UserGroup
'''

@behave.given(
    "A UserGroup already has access to an application and Admin wants to update permissions for the application to the UserGroup")
def step_impl_1(context):

    group_dict = {**TEST_USER_GROUP, "name": str(uuid4())}
    group_res = post_method(url=f"{UM_API_URL}/user-group", request_body=group_dict)
    context.group_id = group_res.json().get("data").get("uuid")

    
    actions = [ {**TEST_ACTION, "name": f"action-{uuid4()}"}, {**TEST_ACTION, "name": f"action-{uuid4()}"}]
    context.action_ids = []
    for action in actions:
        action_res = post_method(url=f"{UM_API_URL}/action", request_body=action)
        assert action_res.status_code == 200
        context.action_ids.append(action_res.json().get("data").get("uuid"))
    

    module_dict = {**TEST_MODULE, "name": f"module-{uuid4()}", "actions": context.action_ids}
    module_res = post_method(url=f"{UM_API_URL}/module", request_body=module_dict)
    assert module_res.status_code == 200
    context.module_id = module_res.json().get("data").get("uuid")

    application_dict = {**TEST_APPLICATION, "modules": [context.module_id]}
    application_dict["name"] = str(uuid4())
    application_res = post_method(url=f"{UM_API_URL}/application", request_body=application_dict)
    assert application_res.status_code == 200
    context.application_id = application_res.json().get("data").get("uuid")

    context.permission_ids = []
    permissions  = [{**TEST_PERMISSION, "name": f"{application_dict.get('name')}.{module_dict.get('name')}.{actions[0].get('name')}",
                       "application_id":context.application_id, "action_id":context.action_ids[0], "module_id": context.module_id},
                    {**TEST_PERMISSION, "name": f"{application_dict.get('name')}.{module_dict.get('name')}.{actions[1].get('name')}",
                    "application_id":context.application_id, "action_id":context.action_ids[1], "module_id": context.module_id}]
    for permission in permissions:
        del permission["user_groups"]
        permission_res = post_method(url=f"{UM_API_URL}/permission", request_body=permission)
        assert permission_res.status_code == 200
        context.permission_ids.append(permission_res.json().get("data").get("uuid"))

    

    update_applications_req_body = {"applications":[context.application_id], "action_id": context.action_ids[0]}
    update_application_res = put_method(url=f"{UM_API_URL}/user-group/{context.group_id}/applications", request_body=update_applications_req_body)
    assert update_application_res.status_code == 200

    context.url = f"{UM_API_URL}/user-group/{context.group_id}/application/{context.application_id}/permissions"




@behave.when("API request is sent to update permissions of a UserGroup")
def step_impl_2(context):
    update_applications_req_body = {"permission_ids": [context.permission_ids[1]]}
    context.res = post_method(url=context.url, request_body=update_applications_req_body)
    context.res_data = context.res.json()


@behave.then("the UserGroup is updated with the permissions")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_data["message"] == "Successfully updated permissions for the applcation of a user group"
    assert context.application_id in context.res_data["data"]["applications"]
    assert context.permission_ids[1] in context.res_data["data"]["permissions"]

@behave.then("the permissions will hold the reference of UserGroup")
def step_impl_3(context):
    get_permission = get_method(url = f"{UM_API_URL}/permission/{context.permission_ids[1]}")
    assert get_permission.status_code == 200
    permission_doc = get_permission.json()
    assert context.group_id in permission_doc.get("data").get("user_groups")

'''
Scenario: Update permissions related to an unassigned application for a UserGroup
'''

@behave.given(
    "A UserGroup already exists and Admin wants to update permissions related to unassigned application for UserGroup")
def step_impl_1(context):

    group_dict = {**TEST_USER_GROUP, "name": str(uuid4())}
    group_res = post_method(url=f"{UM_API_URL}/user-group", request_body=group_dict)
    context.group_id = group_res.json().get("data").get("uuid")

    application_dict = {**TEST_APPLICATION}
    application_dict["name"] = str(uuid4())
    application_res = post_method(url=f"{UM_API_URL}/application", request_body=application_dict)
    assert application_res.status_code == 200
    context.application_id = application_res.json().get("data").get("uuid")

    context.url = f"{UM_API_URL}/user-group/{context.group_id}/application/{context.application_id}/permissions"




@behave.when("API request is sent to update permissions related to unassigned application of a UserGroup")
def step_impl_2(context):
    update_applications_req_body = {"permission_ids": ["random_permission_id"]}
    context.res = post_method(url=context.url, request_body=update_applications_req_body)
    context.res_data = context.res.json()


@behave.then("Validation error for application is thrown by the User management service")
def step_impl_3(context):
    assert context.res.status_code == 422
    assert context.res_data["message"] == "UserGroup doesn't have access to the given application"

'''
Scenario: Update permissions related to an assigned application for a UserGroup but provided invalid permissions
'''

@behave.given(
    "Admin wants to update permissions for the application to the UserGroup but provided permissions not related to valid application in request body")
def step_impl_1(context):

    group_dict = {**TEST_USER_GROUP, "name": str(uuid4())}
    group_res = post_method(url=f"{UM_API_URL}/user-group", request_body=group_dict)
    context.group_id = group_res.json().get("data").get("uuid")

    action_dict = {**TEST_ACTION, "name": f"action-{uuid4()}"}
    action_res = post_method(url=f"{UM_API_URL}/action", request_body=action_dict)
    assert action_res.status_code == 200
    context.action_id = action_res.json().get("data").get("uuid")

    module_dict = {**TEST_MODULE, "name": f"module-{uuid4()}", "actions": [context.action_id]}
    module_res = post_method(url=f"{UM_API_URL}/module", request_body=module_dict)
    assert module_res.status_code == 200
    context.module_id = module_res.json().get("data").get("uuid")

    applications = [{**TEST_APPLICATION,"name": str(uuid4()),"modules": [context.module_id]}, {**TEST_APPLICATION,"name": str(uuid4()), "modules": [context.module_id]}]
    context.application_ids = []
    for application in applications:
        application_res = post_method(url=f"{UM_API_URL}/application", request_body=application)
        assert application_res.status_code == 200
        context.application_ids.append(application_res.json().get("data").get("uuid"))


    context.permission_ids = []
    permissions  = [{**TEST_PERMISSION, "name": f"{applications[0].get('name')}.{module_dict.get('name')}.{action_dict.get('name')}",
                       "application_id":context.application_ids[0], "action_id":context.action_id, "module_id": context.module_id},
                    {**TEST_PERMISSION, "name": f"{applications[1].get('name')}.{module_dict.get('name')}.{action_dict.get('name')}",
                    "application_id":context.application_ids[1], "action_id":context.action_id, "module_id": context.module_id}]
    for permission in permissions:
        del permission["user_groups"]
        permission_res = post_method(url=f"{UM_API_URL}/permission", request_body=permission)
        assert permission_res.status_code == 200
        context.permission_ids.append(permission_res.json().get("data").get("uuid"))

    

    update_applications_req_body = {"applications":[context.application_ids[0]], "action_id": context.action_id}
    update_application_res = put_method(url=f"{UM_API_URL}/user-group/{context.group_id}/applications", request_body=update_applications_req_body)
    assert update_application_res.status_code == 200

    context.url = f"{UM_API_URL}/user-group/{context.group_id}/application/{context.application_ids[0]}/permissions"


@behave.when("API request is sent to update permissions of a UserGroup but provided permissions not related to valid application in request body")
def step_impl_2(context):
    update_applications_req_body = {"permission_ids": [context.permission_ids[1]]}
    context.res = post_method(url=context.url, request_body=update_applications_req_body)
    context.res_data = context.res.json()


@behave.then("Validation error of permission is thrown by the User management service")
def step_impl_3(context):
    assert context.res.status_code == 422
    assert context.res_data["message"] == f"The permission with uuid {context.permission_ids[1]} doesn't belong to the application with uuid {context.application_ids[0]}"
