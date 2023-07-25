"""
Feature: User information is to be updated/deleted
"""
import behave
import sys
from copy import deepcopy
from uuid import uuid4

sys.path.append("../")
from e2e.test_object_schemas import TEST_USER
from environment import TEST_USER_MANAGEMENT_PATH
from e2e.test_config import (API_URL_USER_MANAGEMENT,
                        API_URL_LEARNER_PROFILE_SERVICE,
                        API_URL_LEARNING_RECORD_SERVICE)
from e2e.setup import post_method, get_method, delete_method, put_method

UM_API_URL = API_URL_USER_MANAGEMENT
LRS_API_URL = API_URL_LEARNING_RECORD_SERVICE
SLP_API_URL = API_URL_LEARNER_PROFILE_SERVICE

'''
Scenario: User information is to be updated
'''
@behave.given("User which needs to be updated already exists in the database")
def step_impl_1(context):
    user_dict = deepcopy({**TEST_USER, "user_type": "coach"})
    user_dict["email"] = f"{uuid4()}@gmail.com"

    post_user_url = f"{UM_API_URL}/user"
    post_user_res = post_method(
        url= post_user_url,
        request_body= user_dict
    )

    assert post_user_res.status_code == 200
    context.uuid = post_user_res.json()["data"]["user_id"]
    context.user_ref_id = post_user_res.json()["data"]["user_type_ref"]

@behave.when("The PUT api call is to be made with the correct uuid and fields")
def step_impl_2(context):
    url = f"{UM_API_URL}/user/{context.uuid}"

    get_user_res = get_method(url=url)
    assert get_user_res.status_code == 200

    context.request_body = {}
    context.request_body["first_name"]="UpdateUser"
    context.request_body["last_name"]="TestUser"
    context.request_body["email"] = f"update{uuid4()}@gmail.com"

    context.update_user_res = put_method(url= url,request_body=context.request_body)

@behave.then("The User data is successfully updated")
def step_impl_3(context):
    assert context.update_user_res.status_code == 200
    
    url = f"{UM_API_URL}/user/{context.uuid}"
    get_user_res = get_method(url=url)
    assert get_user_res.status_code == 200
    assert get_user_res.json()["data"]["first_name"] == context.request_body["first_name"]
    assert get_user_res.json()["data"]["last_name"] == context.request_body["last_name"]
    assert get_user_res.json()["data"]["email"] == context.request_body["email"]
    get_staff_url = f"{UM_API_URL}/staff/{context.user_ref_id}"
    get_staff_res = get_method(url=get_staff_url)
    get_staff_res_json = get_staff_res.json()
    assert get_staff_res.status_code == 200
    assert get_staff_res_json["data"]["first_name"] == context.request_body["first_name"], "staff first name not updated"
    assert get_staff_res_json["data"]["last_name"] == context.request_body["last_name"], "staff last name not updated"
    assert get_staff_res_json["data"]["email"] == context.request_body["email"]


'''
Scenario: Name of User of type learner is to be updated
'''
@behave.given("User of type learner which needs to be updated already exists in the database")
def step_impl_1(context):
    user_dict = deepcopy(TEST_USER)
    user_dict["email"] = f"{uuid4()}@gmail.com"

    post_user_url = f"{UM_API_URL}/user"
    post_user_res = post_method(
        url= post_user_url,
        request_body= user_dict
    )

    assert post_user_res.status_code == 200
    context.uuid = post_user_res.json()["data"]["user_id"]
    context.user_ref_id = post_user_res.json()["data"]["user_type_ref"]

@behave.when("The UPDATE api call is made with the correct uuid and fields")
def step_impl_2(context):
    url = f"{UM_API_URL}/user/{context.uuid}"

    get_user_res = get_method(url=url)
    assert get_user_res.status_code == 200

    request_body = {}
    request_body["first_name"] = "updated_first_name"
    request_body["last_name"] = "updated_last_name"
    request_body["email"] = f"new{uuid4()}@gmail.com"
    context.request_body = request_body

    context.update_user_res = put_method(url= url, request_body=context.request_body)

@behave.then("The user, learner and agent name is successfully updated")
def step_impl_3(context):
    assert context.update_user_res.status_code == 200
    
    url = f"{UM_API_URL}/user/{context.uuid}"
    get_user_res = get_method(url=url)
    get_user_res_json = get_user_res.json()
    assert get_user_res.status_code == 200
    assert get_user_res_json["data"]["first_name"] == context.request_body["first_name"]
    assert get_user_res_json["data"]["last_name"] == context.request_body["last_name"]
    assert get_user_res_json["data"]["email"] == context.request_body["email"]
    get_agent_url = f"{LRS_API_URL}/agents"
    get_agent_res = get_method(
        url=get_agent_url,
        query_params={"user_id": context.uuid}
    )
    get_agent_res_json = get_agent_res.json()
    assert get_agent_res.status_code == 200
    assert get_agent_res_json["data"][0]["name"] == context.request_body["first_name"] + " " + context.request_body["last_name"], "Agent name not updated"
    get_learner_url = f"{SLP_API_URL}/learner/{context.user_ref_id}"
    get_learner_res = get_method(url=get_learner_url)
    get_learner_res_json = get_learner_res.json()
    assert get_learner_res.status_code == 200
    assert get_learner_res_json["data"]["first_name"] == context.request_body["first_name"], "Learner first name not updated"
    assert get_learner_res_json["data"]["last_name"] == context.request_body["last_name"], "Learner last name not updated"
    assert get_learner_res_json["data"]["email_address"] == context.request_body["email"]


'''
Scenario: User of staff type is to be deleted
'''
@behave.given("User of staff type which needs to be deleted already exists in the database")
def step_impl_1(context):
    user_dict = deepcopy(TEST_USER)
    user_dict["email"] = f"{uuid4()}@gmail.com"
    user_dict["user_type"] = "coach"

    post_user_url = f"{UM_API_URL}/user"
    post_user_res = post_method(
        url= post_user_url,
        request_body= user_dict
    )

    assert post_user_res.status_code == 200
    context.uuid = post_user_res.json()["data"]["user_id"]
    context.staff_uuid = post_user_res.json()["data"]["user_type_ref"]

@behave.when("The DELETE api call is made with the correct uuid and fields")
def step_impl_2(context):
    url = f"{UM_API_URL}/user/{context.uuid}"
    context.delete_user_res = delete_method(url=url)

@behave.then("The User and the Staff data is successfully deleted")
def step_impl_3(context):
    assert context.delete_user_res.status_code == 200
    
    url = f"{UM_API_URL}/user/{context.uuid}"
    get_user_res = get_method(url=url)
    assert get_user_res.status_code == 404

    staff_url = f"{UM_API_URL}/staff/{context.staff_uuid}"
    get_staff_res = get_method(staff_url)
    assert get_staff_res.status_code == 404


'''
Scenario: User of type learner is to be deleted
'''
@behave.given("User of type learner needs to be deleted already exists in the database")
def step_impl_1(context):
    user_dict = deepcopy(TEST_USER)
    user_dict["email"] = f"{uuid4()}@gmail.com"

    post_user_url = f"{UM_API_URL}/user"
    post_user_res = post_method(
        url= post_user_url,
        request_body= user_dict
    )

    assert post_user_res.status_code == 200
    context.uuid = post_user_res.json()["data"]["user_id"]
    context.learner_id = post_user_res.json()["data"]["user_type_ref"]

@behave.when("The DELETE api call is to be made with the correct user uuid of type learner and fields")
def step_impl_2(context):
    url = f"{UM_API_URL}/user/{context.uuid}"
    context.delete_user_res = delete_method(url= url)

@behave.then("The User data along with Agent, learner, learner profile data gets successfully deleted")
def step_impl_3(context):
    assert context.delete_user_res.status_code == 200

    url = f"{UM_API_URL}/user/{context.uuid}"
    get_user_res = get_method(url=url)
    assert get_user_res.status_code == 404

    get_agent_url = f"{LRS_API_URL}/agents"
    get_agent_res = get_method(
        url= get_agent_url,
        query_params= {"user_id":context.uuid}
    )
    assert get_agent_res.status_code == 200
    assert len(get_agent_res.json()["data"]) == 0

    get_learner_url = f"{SLP_API_URL}/learner/{context.learner_id}"
    get_learner_res = get_method(url= get_learner_url)
    assert get_learner_res.status_code == 404
