"""
Feature: New User/Users is/are to be created
"""
import behave
import sys
from copy import deepcopy
from uuid import uuid4
from behave.runner import Context

sys.path.append("../")
from test_object_schemas import TEST_USER
from environment import TEST_USER_MANAGEMENT_PATH
from test_config import (API_URL_USER_MANAGEMENT as UM_API_URL,
                        API_URL_LEARNER_PROFILE_SERVICE as SLP_API_URL,
                        API_URL_LEARNING_RECORD_SERVICE as LRS_API_URL)
from setup import post_method, get_method

'''
Scenario: A user wants to be registered with correct account details 
'''
@behave.given("A user has access to the application and submits correct form")
def step_impl_1(context):
    context.user_dict = deepcopy(TEST_USER)
    context.user_dict["email"] = f"{uuid4()}@gmail.com"
    
    context.url = f"{UM_API_URL}/user"

@behave.when("A POST api call is made to the User Management Service with correct details")
def step_impl_2(context):

    context.post_user_res = post_method(
        url= context.url,
        request_body= context.user_dict
    )

@behave.then("The User is successfully created")
def step_impl_3(context):
    assert context.post_user_res.status_code == 200
    context.post_user_res_dict = context.post_user_res.json()["data"] 

@behave.then("The respective Agent, Learner, Learner Profile are also created")
def step_impl_4(context):

    get_learner_url = f'''{SLP_API_URL}/learner/{context.post_user_res_dict["user_type_ref"]}'''
    get_learner_res = get_method(url = get_learner_url)

    print("\n\n**************************")
    print(context.post_user_res_dict["user_type_ref"])
    print(get_learner_res.status_code)
    print(get_learner_res.json())

    assert get_learner_res.status_code == 200

    get_learner_profile_url = f'''{SLP_API_URL}/learner/{context.post_user_res_dict["user_type_ref"]}/learner-profile'''
    get_learner_profile_res = get_method(url = get_learner_profile_url)
    assert get_learner_profile_res.status_code == 200
    assert get_learner_profile_res.json()["data"]["learner_id"] == context.post_user_res_dict["user_type_ref"]

    get_agent_url = f'''{LRS_API_URL}/agents'''
    get_agent_res = get_method(
        url= get_agent_url,
        query_params= {"user_id":context.post_user_res_dict["user_id"]}
    )
    assert get_agent_res.status_code == 200
    assert get_agent_res.json()["data"][0]["user_id"] == context.post_user_res_dict["user_id"]


'''
Scenario: A user wants to be registered with incorrect account details
'''
@behave.given("A user has access to the application and will submits incorrect form")
def step_impl_1(context):
    context.user_dict = deepcopy(TEST_USER)
    del context.user_dict["email"]

    context.url = f"{UM_API_URL}/user"

@behave.when("A POST api call is made to the User Management Service with incorrect details")
def step_impl_2(context):
    context.post_user_res = post_method(
        url= context.url,
        request_body= context.user_dict
    )

@behave.then("User will not be created and appropriate error response will be sent")
def step_impl_3(context):
    assert context.post_user_res.status_code == 422
    assert context.post_user_res.json()["message"] == "Validation Failed"


'''
Scenario: Multiple users are to be created
'''
@behave.given("A faculty/admin has access to the application")
def step_impl_1(context):
    context.url = f"{UM_API_URL}/user/import/json"
    

@behave.when("A POST api call is made to the User Management Service Bulk Import api with correct input json file")
def step_impl_2(context):

    json_file_path = TEST_USER_MANAGEMENT_PATH

    with open(json_file_path, encoding="UTF-8") as users_json_file:
        post_res = post_method(context.url, files={"json_file": users_json_file})

        print(post_res.status_code)
        print(post_res.json())

        assert post_res.status_code == 200

        post_res_data = post_res.json()
        context.imported_user_ids = post_res_data["data"]

@behave.then("The Users are successfully created")
def step_impl_3(context):
    
    context.learner_id_list = []
    for user_id in context.imported_user_ids:
        get_user_res = get_method(url=f"{UM_API_URL}/user/{user_id}")
        assert get_user_res.status_code == 200

        context.learner_id_list.append(get_user_res.json()["data"]["user_type_ref"])

@behave.then("The respective Agent, Learner, Learner Profile for each user are also created")
def step_impl_4(context):
    
    for i in range(len(context.learner_id_list)):
        get_learner_url = f'''{SLP_API_URL}/learner/{context.learner_id_list[i]}'''
        get_learner_res = get_method(url = get_learner_url)
        assert get_learner_res.status_code == 200

        get_learner_profile_url = f'''{SLP_API_URL}/learner/{context.learner_id_list[i]}/learner-profile'''
        get_learner_profile_res = get_method(url = get_learner_profile_url)
        assert get_learner_profile_res.status_code == 200
        assert get_learner_profile_res.json()["data"]["learner_id"] == context.learner_id_list[i]

        get_agent_url = f'''{LRS_API_URL}/agents'''
        get_agent_res = get_method(
            url= get_agent_url,
            query_params= {"user_id":context.imported_user_ids[i]}
        )
        assert get_agent_res.status_code == 200
        assert get_agent_res.json()["data"][0]["user_id"] == context.imported_user_ids[i]


@behave.Given("A User has access to the application and will submit form "
              "with incorrect firstname")
def step_impl_1(context: Context) -> None:
    """
    Create Incorrect Request payload to create a User
    Parameters
    ----------
    context: behave.runner.Context

    Returns
    ------
    None
    """

    context.user_dict = deepcopy(TEST_USER)
    context.user_dict["first_name"] = ""

    context.url = f"{UM_API_URL}/user"


@behave.when("Send API request to create User with incorrect request payload")
def step_impl_2(context: Context) -> None:
    """
    Send API request to create User
    Parameters
    ----------
    context: behave.runner.Context

    Returns
    -------
    None
    """

    context.post_user_res = post_method(
        url=context.url,
        request_body=context.user_dict
    )


@behave.then("Failed to create User with incorrect firstname and appropriate "
             "error response will be sent")
def step_impl_3(context: Context) -> None:
    """
    Assert the API response
    Parameters
    ----------
    context: behave.runner.Context

    Returns
    -------
    None
    """

    assert context.post_user_res.status_code == 422


@behave.Given("A User has access to the application and will submit form "
              "with incorrect lastname")
def step_impl_1(context: Context) -> None:
    """
    Create Incorrect Request payload to create a User
    Parameters
    ----------
    context: behave.runner.Context

    Returns
    ------
    None
    """

    context.user_dict = deepcopy(TEST_USER)
    context.user_dict["last_name"] = ""

    context.url = f"{UM_API_URL}/user"


@behave.when("Send API request to create User with incorrect lastname request "
             "payload")
def step_impl_2(context: Context) -> None:
    """
    Send API request to create User
    Parameters
    ----------
    context: behave.runner.Context

    Returns
    -------
    None
    """

    context.post_user_res = post_method(
        url=context.url,
        request_body=context.user_dict
    )


@behave.then("Failed to create User with incorrect lastname and appropriate "
             "error response will be sent")
def step_impl_3(context: Context) -> None:
    """
    Assert the API response
    Parameters
    ----------
    context: behave.runner.Context

    Returns
    -------
    None
    """

    assert context.post_user_res.status_code == 422


@behave.Given("A User has access to the application and will submit form "
              "with incorrect Email ID format")
def step_impl_1(context: Context) -> None:
    """
    Create Incorrect Request payload to create a User
    Parameters
    ----------
    context: behave.runner.Context

    Returns
    ------
    None
    """

    context.user_dict = deepcopy(TEST_USER)
    context.user_dict["email"] = f"TestEmail"

    context.url = f"{UM_API_URL}/user"


@behave.when("Send API request to create User with incorrect Email ID request "
             "payload")
def step_impl_2(context: Context) -> None:
    """
    Send API request to create User
    Parameters
    ----------
    context: behave.runner.Context

    Returns
    -------
    None
    """

    context.post_user_res = post_method(
        url=context.url,
        request_body=context.user_dict
    )


@behave.then("Failed to create User with incorrect Email ID and appropriate "
             "error response will be sent")
def step_impl_3(context: Context) -> None:
    """
    Assert the API response
    Parameters
    ----------
    context: behave.runner.Context

    Returns
    -------
    None
    """

    assert context.post_user_res.status_code == 422


# Scenario: Create User of type Faculty

@behave.given("A user has access to the application and submits correct form for user type faculty")
def step_impl_1(context):
	context.user_dict = deepcopy(TEST_USER)
	context.user_dict["email"] = f"{uuid4()}@gmail.com"
	context.user_dict["user_type"] = "coach"
	
	context.url = f"{UM_API_URL}/user"

@behave.when("A POST api call is made to the User Management Service with user type faculty")
def step_impl_2(context):
	context.post_user_res = post_method(
		url=context.url, request_body=context.user_dict)

@behave.then("The User should be successfully created")
def step_impl_3(context):
	assert context.post_user_res.status_code == 200
	context.post_user_res_dict = context.post_user_res.json()["data"] 

@behave.then("The respective Staff and Agent will also be created")
def step_impl_4(context):
	get_agent_url = f'''{LRS_API_URL}/agents'''
	get_agent_res = get_method(
		url= get_agent_url,
		query_params= {"user_id":context.post_user_res_dict["user_id"]}
	)
	assert get_agent_res.status_code == 200
	assert get_agent_res.json()["data"][0]["user_id"] == context.post_user_res_dict["user_id"]
	
	staff_uuid = context.post_user_res_dict["user_type_ref"]
	get_staff_url = f"{UM_API_URL}/staff/{staff_uuid}"
	get_staff_res = get_method(url=get_staff_url)
	get_staff_res_json = get_staff_res.json()
	assert get_staff_res.status_code == 200
	assert get_staff_res_json["data"]["email"] == context.user_dict["email"]

