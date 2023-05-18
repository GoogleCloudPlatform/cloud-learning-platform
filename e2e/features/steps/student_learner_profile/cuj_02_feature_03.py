"""Filter achievement data, learner account data, and learner profile data based on various Student Learner Profile attributes"""

import sys
import json
import os
from setup import post_method, get_method, delete_method, put_method
import behave

from test_config import API_URL_LEARNER_PROFILE_SERVICE, TESTING_OBJECTS_PATH
from test_object_schemas import (LEARNER_OBJECT_TEMPLATE,
                                LEARNER_PROFILE_TEMPLATE,
                                ACHIEVEMENT_OBJECT_TEMPLATE,
                                GOAL_OBJECT_TEMPLATE)

TEST_LP_PATH = os.path.join(TESTING_OBJECTS_PATH, "learner_profile.json")
TEST_ACHV_ACHIEVEMENT = os.path.join(TESTING_OBJECTS_PATH, "learner_achievement.json")
TEST_LEARNER_ACHIEVEMENT = os.path.join(TESTING_OBJECTS_PATH, "learner.json")
TEST_GOAL_PATH = os.path.join(TESTING_OBJECTS_PATH, "goals.json")

API_URL = API_URL_LEARNER_PROFILE_SERVICE

#SLP Postive --------------------------------------------------------
@behave.given("SNHU Administrator has access to SLP service with the correct filter payloads")
def step_impl_1(context):
    fileObject = open(TEST_LP_PATH, "r")
    jsonContent = fileObject.read()
    aList = json.loads(jsonContent)
    context.lp = aList[0]
    context.payload ={
        "learning_goal": "Develop Communication Skills"
    }
    context.url= f"{API_URL}/learner-profile?skip=0&limit=10"

@behave.when("SNHU Administrator wants to filter learner profiles based on correct filter payloads")
def step_impl_2(context):
    context.res = get_method(url= context.url, query_params = context.payload)
    context.res_data = context.res.json()

@behave.then("the relevant learner profiles are retrieved as per the correct filters")
def step_impl_3(context):
    assert context.res.status_code == 200 , "Response Failure"
    assert context.res_data["message"] == "Successfully fetched the learner profile/s" , "Couldnot fetch the learner profile/s"
    assert len(context.res_data) > 0 , "No data added to be DB"
    if(len(context.res_data) > 0):
        assert context.res_data["data"][0]["learner_id"] == context.lp["learner_id"] , "Fetched the wrong learner id"
        assert context.res_data["data"][0]["uuid"] == context.lp["uuid"] , "UUID mismatch"

#SLP Negative --------------------------------------------------------
@behave.given("SNHU Administrator has access to SLP service with the correct filter payloads for more than one list filters")
def step_impl_1(context):
    context.payload ={
        "learning_goal": "Develop Communication Skills",
        "learning_experience": "Developing APIs"
    }
    context.url= f"{API_URL}/learner-profile?skip=0&limit=10"

@behave.when("SNHU Administrator wants to filter learner profiles based on correct filter payloads for more than one list filters")
def step_impl_2(context):
    context.res = get_method(url= context.url, query_params = context.payload)
    context.res_data = context.res.json()

@behave.then("the SNHU administrator gets the right error message")
def step_impl_3(context):
    assert context.res_data["success"] == False , "Succesfully fetched the right learner profiles based on filter payload"
    assert context.res_data["message"] == "Please use only one of the following fields for filter at a time - learning_goal, learning_pathway, learning_experience"

#LEARNER ACHIEVEMENT Positive ---------------------------------------------------------------
@behave.given("SNHU Administrator has access to SLP service with the correct learner specific achievements filter payloads")
def step_impl_1(context):
    context.payload ={
        "credential_id": "c1",
        "skill_id": "S1"
    }
    fileObject = open(TEST_ACHV_ACHIEVEMENT, "r")
    jsonContent = fileObject.read()
    acList = json.loads(jsonContent)

    context.achv = acList[0]
    context.learner_id = context.achv["learner_id"]
    context.url= f"{API_URL}/learner/{context.learner_id}/achievements?skip=0&limit=10"

@behave.when("SNHU Administrator wants to filter learner specific achievements based on correct filter payloads")
def step_impl_2(context):
    context.res = get_method(url= context.url, query_params = context.payload)
    context.res_data = context.res.json()

@behave.then("the relevant learner specific achievements are retrieved as per the correct filters")
def step_impl_3(context):
    assert context.res.status_code == 200 , "Failed response"
    assert context.res_data["message"] == "Data fetched successfully", "Data couldn't be fetched"
    assert len(context.res_data) > 0, "No learner specific acheivement data added to DB"
    if len(context.res_data["data"]) > 0:
        assert context.res_data["data"][0]["learner_id"] == context.achv["learner_id"], "Learner id mismatch"
        assert context.res_data["data"][0]["uuid"] == context.achv["uuid"], "UUID doesn't match"
        assert context.res_data["data"][0]["type"] == context.achv["type"], "Type of achievement mismatched"

#LEARNER  ACHIEVEMENT Negative ---------------------------------------------------------------
@behave.given("SNHU Administrator has access to SLP service with the incorrect learner id")
def step_impl_1(context):
    context.payload ={
        "competency_id": "cd1",
        "skill_id": "S1"
    }
    context.learner_id = "Learner three"
    context.url= f"{API_URL}/learner/{context.learner_id}/achievements?skip=0&limit=10"

@behave.when("SNHU Administrator wants to filter learner specific achievements based on incorrect learner id")
def step_impl_2(context):
    context.res = get_method(url= context.url, query_params = context.payload)
    context.res_data = context.res.json()

@behave.then("the relevant learner specific achievements are retrieved as per the incorrect learner id")
def step_impl_3(context):
    assert context.res.status_code == 404
    assert context.res_data["message"] == "Learner with uuid Learner three not found"

#ACHIEVEMENT Positive ---------------------------------------------------------------
@behave.given("SNHU Administrator has access to SLP service with the correct achievements filter payloads")
def step_impl_1(context):
    context.payload ={
        "credential_id": "c1",
        "skill_id": "S1"
    }
    fileObject = open(TEST_ACHV_ACHIEVEMENT, "r")
    jsonContent = fileObject.read()
    acList = json.loads(jsonContent)

    context.achv = acList[0]
    context.url= f"{API_URL}/achievements?skip=0&limit=10"

@behave.when("SNHU Administrator wants to filter achievements based on correct filter payloads")
def step_impl_2(context):
    context.res = get_method(url= context.url, query_params = context.payload)
    context.res_data = context.res.json()

@behave.then("the relevant achievements are retrieved as per the correct filters")
def step_impl_3(context):
    assert context.res.status_code == 200 , "Failed response"
    assert context.res_data["message"] == "Data fetched successfully" ,"Achievement Data couldn't be fetched succesfully"
    assert len(context.res_data) > 0, "No achievement data added to DB"
    if len(context.res_data["data"]) > 0:
        assert context.res_data["data"][0]["learner_id"] == context.achv["learner_id"] , "Learner ID mismatch for achievements fetched"
        assert context.res_data["data"][0]["uuid"] == context.achv["uuid"], "UUID msmatched for the achievements fetched"
        assert context.res_data["data"][0]["type"] == context.achv["type"], "Achievement type mismatch for the fetched achievements"

#ACHIEVEMENT Negative ---------------------------------------------------------------
@behave.given("SNHU Administrator has access to SLP service with the incorrect achievements filter payloads")
def step_impl_1(context):
    context.payload ={
        "competency_id": "cd1",
        "skill_id": "S1"
    }
    context.url= f"{API_URL}/achievements?skip=0&limit=10"

@behave.when("SNHU Administrator wants to filter achievements based on incorrect achievements filter payloads")
def step_impl_2(context):
    context.res = get_method(url= context.url, query_params = context.payload)
    context.res_data = context.res.json()

@behave.then("the relevant achievements are retrieved as per the incorrect achievements filter payloads")
def step_impl_3(context):
    assert context.res.status_code == 500
    assert context.res_data["success"] == False
    assert context.res_data["message"] == "Please use only one of the following fields for filter at a time - skill_id, competency_id"

#GOAL Positive ---------------------------------------------------------------
@behave.given("SNHU Administrator has access to SLP service with the correct Goals filter payloads")
def step_impl_1(context):
    context.payload ={
        "goal_type": "Long-term"
    }
    fileObject = open(TEST_GOAL_PATH, "r")
    jsonContent = fileObject.read()
    glist = json.loads(jsonContent)
    context.goal = glist[0]
    context.url= f"{API_URL}/goal?skip=0&limit=10"

@behave.when("SNHU Administrator wants to filter Goals based on correct filter payloads")
def step_impl_2(context):
    context.res = get_method(url= context.url, query_params = context.payload)
    context.res_data = context.res.json()

@behave.then("the relevant Goals are retrieved as per the correct filters")
def step_impl_3(context):
    assert context.res.status_code == 200, f"Status code is {context.res.status_code} not 200"
    assert context.res_data["message"] == "Successfully fetched the goal", "Couldn't fetch the goal"
    assert len(context.res_data) > 0, "No Goals data added to DB"
    if len(context.res_data["data"]) > 0:
        assert context.res_data["data"][0]["name"] == context.goal["name"]
        assert context.res_data["data"][0]["type"] == context.goal["type"]

#GOAL Negative ---------------------------------------------------------------
@behave.given("SNHU Administrator has access to SLP service with the incorrect Goals filter payloads")
def step_impl_1(context):
    context.payload ={
        "goal_type": 1
    }
    context.url= f"{API_URL}/goal?skip=0&limit=10"

@behave.when("SNHU Administrator wants to filter Goals based on incorrect filter payloads")
def step_impl_2(context):
    context.res = get_method(url= context.url, query_params = context.payload)
    context.res_data = context.res.json()

@behave.then("the user gets no retreived Goal")
def step_impl_3(context):
    assert context.res.status_code == 200, "Succesful response"
    assert len(context.res_data["data"]) == 0, "Goal Data was retreived"

# Fetch archived Learner ------------------------------------------------------
@behave.given("There is an archived Learner in database")
def step_impl_1(context):
    # Add an archived learner
    learner_dict = {**LEARNER_OBJECT_TEMPLATE}
    learner_dict["email_address"] = "jondoe_c2f3s10@gmail.com"
    context.learner_payload = learner_dict
    context.learner_url = f"{API_URL}/learner"
    context.learner_post_res = post_method(
        url=context.learner_url, request_body=context.learner_payload)
    context.learner_post_res_data = context.learner_post_res.json()

    assert context.learner_post_res.status_code == 200, \
        f"status is {context.learner_post_res.status_code} not 200"
    assert context.learner_post_res_data.get("success") is True, \
        "success not true"
    context.learner_id = context.learner_post_res_data["data"]["uuid"]

    context.item_url = f"{context.learner_url}/{context.learner_id}"
    context.learner_post_res = put_method(
        url=context.item_url, request_body={"is_archived": True})

@behave.when(
    "SNHU Administrator fetches the archived Learner with correct request payload")
def step_impl_2(context):
    # Fetch an archived learner
    url = f"{context.learner_url}s"
    params = {"skip": 0, "limit": 30, "fetch_archive": True}
    context.learner_get_res = get_method(url=url, query_params=params)
    context.learner_get_res_data = context.learner_get_res.json()

    assert context.learner_get_res.status_code == 200, \
        f"status is {context.learner_get_res.status_code} not 200"
    assert context.learner_get_res_data.get("success") is True, \
        "success not true"

@behave.then("the relevant Learner is retrieved")
def step_impl_3(context):
    assert all(i["is_archived"] for i in \
        context.learner_get_res_data.get("data")["records"]), \
            "all learners not archived"

    fetched_learners = [i.get("uuid") for i in \
        context.learner_get_res_data.get("data")["records"]]
    assert context.learner_id in fetched_learners, f"learner not retrieved"

    # delete learner
    delete_method(url=context.item_url)

# Fetch un-archived Learner ---------------------------------------------------
@behave.given("There is an un-archived Learner in database")
def step_impl_1(context):
    # Add an un-archived learner
    learner_dict = {**LEARNER_OBJECT_TEMPLATE}
    learner_dict["email_address"] = "jondoe_c2f3s11@gmail.com"
    context.learner_payload = learner_dict
    context.learner_url = f"{API_URL}/learner"
    context.learner_post_res = post_method(
        url=context.learner_url, request_body=context.learner_payload)
    context.learner_post_res_data = context.learner_post_res.json()

    assert context.learner_post_res.status_code == 200, \
        f"status is {context.learner_post_res.status_code} not 200"
    assert context.learner_post_res_data.get("success") is True, \
        "success not true"
    context.learner_id = context.learner_post_res_data["data"]["uuid"]

    context.item_url = f"{context.learner_url}/{context.learner_id}"

@behave.when(
    "SNHU Administrator fetches the un-archived Learner with correct request payload")
def step_impl_2(context):
    # Fetch an un-archived learner
    url = f"{context.learner_url}s"
    params = {"skip": 0, "limit": 30, "fetch_archive": False}
    context.learner_get_res = get_method(url=url, query_params=params)
    context.learner_get_res_data = context.learner_get_res.json()

    assert context.learner_get_res.status_code == 200, \
        f"status is {context.learner_get_res.status_code} not 200"
    assert context.learner_get_res_data.get("success") is True, \
        "success not true"

@behave.then("the relevant Learners are retrieved")
def step_impl_3(context):
    assert all(i["is_archived"] is False for i in \
        context.learner_get_res_data.get("data")["records"]), \
            "all learners not un-archived"

    fetched_learners = [i.get("uuid") for i in \
        context.learner_get_res_data.get("data")["records"]]
    assert context.learner_id in fetched_learners, f"learner not retrieved"

    # delete learner
    delete_method(url=context.item_url)

# Fetch archived and un-archived learner --------------------------------------
@behave.given("There is an archived and an un-archived Learner in database")
def step_impl_1(context):
    # Add an archived learner
    learner_dict = {**LEARNER_OBJECT_TEMPLATE}
    learner_dict["email_address"] = "jondoe_c2f3s12a@gmail.com"
    context.learner_payload = learner_dict
    context.learner_url = f"{API_URL}/learner"
    context.learner_post_res = post_method(
        url=context.learner_url, request_body=context.learner_payload)
    context.learner_post_res_data = context.learner_post_res.json()

    assert context.learner_post_res.status_code == 200, \
        f"status is {context.learner_post_res.status_code} not 200"
    assert context.learner_post_res_data.get("success") is True, \
        "success not true"
    context.learner_id_1 = context.learner_post_res_data["data"]["uuid"]

    context.item_url_1 = f"{context.learner_url}/{context.learner_id_1}"
    context.learner_post_res = put_method(
        url=context.item_url_1, request_body={"is_archived": True})

     # Add an un-archived learner
    learner_dict = {**LEARNER_OBJECT_TEMPLATE}
    learner_dict["email_address"] = "jondoe_c2f3s12u@gmail.com"
    context.learner_payload = learner_dict
    context.learner_url = f"{API_URL}/learner"
    context.learner_post_res = post_method(
        url=context.learner_url, request_body=context.learner_payload)
    context.learner_post_res_data = context.learner_post_res.json()

    assert context.learner_post_res.status_code == 200, \
        f"status is {context.learner_post_res.status_code} not 200"
    assert context.learner_post_res_data.get("success") is True, \
        "success not true"
    context.learner_id_2 = context.learner_post_res_data["data"]["uuid"]
    context.item_url_2 = f"{context.learner_url}/{context.learner_id_2}"

@behave.when(
    "SNHU Administrator fetches the Learner with correct request payload")
def step_impl_2(context):
    # Fetch learners
    url = f"{context.learner_url}s"
    params = {"skip": 0, "limit": 30}
    context.learner_get_res = get_method(url=url, query_params=params)
    context.learner_get_res_data = context.learner_get_res.json()

    assert context.learner_get_res.status_code == 200, \
        f"status is {context.learner_get_res.status_code} not 200"
    assert context.learner_get_res_data.get("success") is True, \
        "success not true"

@behave.then("the relevant Learner(s) are retrieved")
def step_impl_3(context):
    fetched_learners = [i.get("uuid") for i in context.learner_get_res_data.get("data")["records"]]
    assert context.learner_id_1 in fetched_learners, \
        "archived learner not retrieved"
    assert context.learner_id_2 in fetched_learners, \
        "un-archived learner not retrieved"

    # delete learner
    delete_method(url=context.item_url_1)
    delete_method(url=context.item_url_2)

# Fetch archived Learner Profile ----------------------------------------------
@behave.given("There is an archived Learner Profile in database")
def step_impl_1(context):
    # Add a learner
    learner_dict = {**LEARNER_OBJECT_TEMPLATE}
    learner_dict["email_address"] = "jondoe_c2f3s13@gmail.com"
    context.learner_payload = learner_dict
    context.learner_url = f"{API_URL}/learner"
    context.learner_post_res = post_method(
        url=context.learner_url, request_body=context.learner_payload)
    context.learner_post_res_data = context.learner_post_res.json()

    assert context.learner_post_res.status_code == 200, \
        f"status is {context.learner_post_res.status_code} not 200"
    assert context.learner_post_res_data.get("success") is True, \
        "success not true"
    context.learner_id = context.learner_post_res_data["data"]["uuid"]

    # Add an archived learner_profile
    learner_profile_dict = {**LEARNER_PROFILE_TEMPLATE}
    learner_profile_dict["learner_id"] = context.learner_id
    context.learner_profile_payload = learner_profile_dict
    context.learner_profile_url = f"{API_URL}/learner/{context.learner_id}/learner-profile"
    context.learner_profile_post_res = post_method(
        url=context.learner_profile_url,
        request_body=context.learner_profile_payload)
    context.learner_profile_post_res_data = context.learner_profile_post_res.json()

    assert context.learner_profile_post_res.status_code == 200, \
        f"status is {context.learner_profile_post_res.status_code} not 200"
    assert context.learner_profile_post_res_data.get("success") is True, \
        "success not true"
    context.learner_profile_id = \
        context.learner_profile_post_res_data["data"]["uuid"]

    context.item_url = f"{context.learner_profile_url}/{context.learner_profile_id}"

    url = f"{context.learner_url}/{context.learner_id}"
    context.learner_post_res = put_method(
        url=url, request_body={"is_archived": True})

@behave.when(
    "SNHU Administrator fetches the archived Learner Profile with correct request payload")
def step_impl_2(context):
    # Fetch all learner_profile
    url = f"{API_URL}/learner-profile"
    params = {"skip": 0, "limit": 30, "fetch_archive": True}
    context.learner_profile_get_all_res = get_method(url=url, query_params=params)
    context.learner_profile_get_all_res_data = \
        context.learner_profile_get_all_res.json()

    assert context.learner_profile_get_all_res.status_code == 200, \
        f"status is {context.learner_profile_get_all_res.status_code} not 200"
    assert context.learner_profile_get_all_res_data.get("success") is True, \
        "success not true"

@behave.then("the relevant Learner Profile is retrieved")
def step_impl_3(context):
    assert all(i["is_archived"] for i in \
        context.learner_profile_get_all_res_data.get("data")["records"]), \
            "all learner profiles not archived"

    fetched_learner_profile = [i.get("uuid") for i in \
        context.learner_profile_get_all_res_data.get("data")["records"]]
    assert context.learner_profile_id in fetched_learner_profile, \
        "get all learner_profile not retrieved"
    
    # delete learner_profile
    delete_method(url=context.item_url)

# Fetch un-archived Learner Profile -------------------------------------------
@behave.given("There is an un-archived Learner Profile in database")
def step_impl_1(context):
    # Add a learner
    learner_dict = {**LEARNER_OBJECT_TEMPLATE}
    learner_dict["email_address"] = "jondoe_c2f3s14@gmail.com"
    context.learner_payload = learner_dict
    context.learner_url = f"{API_URL}/learner"
    context.learner_post_res = post_method(
        url=context.learner_url, request_body=context.learner_payload)
    context.learner_post_res_data = context.learner_post_res.json()

    assert context.learner_post_res.status_code == 200, \
        f"status is {context.learner_post_res.status_code} not 200"
    assert context.learner_post_res_data.get("success") is True, \
        "success not true"
    context.learner_id = context.learner_post_res_data["data"]["uuid"]

    # Add an un-archived learner_profile
    learner_profile_dict = {**LEARNER_PROFILE_TEMPLATE}
    learner_profile_dict["learner_id"] = context.learner_id
    context.learner_profile_payload = learner_profile_dict
    context.learner_profile_url = \
        f"{API_URL}/learner/{context.learner_id}/learner-profile"
    context.learner_profile_post_res = post_method(
        url=context.learner_profile_url,
        request_body=context.learner_profile_payload)
    context.learner_profile_post_res_data = context.learner_profile_post_res.json()

    assert context.learner_profile_post_res.status_code == 200, \
        f"status is {context.learner_profile_post_res.status_code} not 200"
    assert context.learner_profile_post_res_data.get("success") is True, \
        "success not true"
    context.learner_profile_id = \
        context.learner_profile_post_res_data["data"]["uuid"]

    context.item_url = f"{context.learner_profile_url}/{context.learner_profile_id}"

@behave.when(
    "SNHU Administrator fetches the un-archived Learner Profile with correct request payload")
def step_impl_2(context):
    # Fetch all learner_profile
    url = f"{API_URL}/learner-profile"
    params = {"skip": 0, "limit": 30, "fetch_archive": False}
    context.learner_profile_get_all_res = get_method(url=url, query_params=params)
    context.learner_profile_get_all_res_data = \
        context.learner_profile_get_all_res.json()

    assert context.learner_profile_get_all_res.status_code == 200, \
        f"status is {context.learner_profile_get_all_res.status_code} not 200"
    assert context.learner_profile_get_all_res_data.get("success") is True, \
        "success not true"

@behave.then("the relevant Learner Profiles are retrieved")
def step_impl_3(context):
    assert all(i["is_archived"] is False for i in \
        context.learner_profile_get_all_res_data.get("data")["records"]), \
            "all learner profiles not un-archived"

    fetched_learner_profile = [i.get("uuid") for i in \
        context.learner_profile_get_all_res_data.get("data")["records"]]
    assert context.learner_profile_id in fetched_learner_profile, \
        "get all learner_profile not retrieved"

    # delete learner_profile
    delete_method(url=context.item_url)

# Fetch archived Achievement ---------------------------------------------------------
@behave.given("There is an archived Achievement in database")
def step_impl_1(context):
    # Add a learner
    learner_dict = {**LEARNER_OBJECT_TEMPLATE}
    learner_dict["email_address"] = "jondoe_c2f3s16@gmail.com"
    context.learner_payload = learner_dict
    context.learner_url = f"{API_URL}/learner"
    context.learner_post_res = post_method(
        url=context.learner_url, request_body=context.learner_payload)
    context.learner_post_res_data = context.learner_post_res.json()

    assert context.learner_post_res.status_code == 200, \
        f"status is {context.learner_post_res.status_code} not 200"
    assert context.learner_post_res_data.get("success") is True, \
        "success not true"
    context.learner_id = context.learner_post_res_data["data"]["uuid"]

    # Add an archived achievement
    achievement_dict = {**ACHIEVEMENT_OBJECT_TEMPLATE}
    achievement_dict["learner_id"] = context.learner_id
    context.achievement_payload = achievement_dict
    context.achievement_url = f"{API_URL}/learner/{context.learner_id}/achievement"
    context.achievement_post_res = post_method(
        url=context.achievement_url, request_body=context.achievement_payload)
    context.achievement_post_res_data = context.achievement_post_res.json()

    assert context.achievement_post_res.status_code == 200, \
        f"status is {context.achievement_post_res.status_code} not 200"
    assert context.achievement_post_res_data.get("success") is True, \
        "success not true"
    context.achievement_id = context.achievement_post_res_data["data"]["uuid"]

    context.item_url = f"{context.achievement_url}/{context.achievement_id}"
    context.achievement_post_res = put_method(
        url=context.item_url, request_body={"is_archived": True})

@behave.when(
    "SNHU Administrator fetches the archived Achievement with correct request payload")
def step_impl_2(context):
    # Fetch an archived achievement
    url = f"{context.achievement_url}s"
    params = {"skip": 0, "limit": 30, "fetch_archive": True}
    context.achievement_get_res = get_method(url=url, query_params=params)
    context.achievement_get_res_data = context.achievement_get_res.json()

    assert context.achievement_get_res.status_code == 200, \
        f"status is {context.achievement_get_res.status_code} not 200" \
            f"{context.achievement_get_res_data}"
    assert context.achievement_get_res_data.get("success") is True, \
        "success not true"

    # Fetch all achievements
    url = f"{API_URL}/achievements"
    params = {"skip": 0, "limit": 30, "fetch_archive": True}
    context.achievement_get_all_res = get_method(url=url, query_params=params)
    context.achievement_get_all_res_data = context.achievement_get_all_res.json()

    assert context.achievement_get_all_res.status_code == 200, \
        f"status is {context.achievement_get_all_res.status_code} not 200"
    assert context.achievement_get_all_res_data.get("success") is True, \
        "success not true"

@behave.then("the relevant Achievement is retrieved")
def step_impl_3(context):
    assert all(i["is_archived"] for i in \
        context.achievement_get_res_data.get("data")["records"]), \
            "all achievements not un-archived"

    fetched_achievements = [i.get("uuid") \
        for i in context.achievement_get_res_data.get("data")["records"]]
    assert context.achievement_id in fetched_achievements, \
        "achievement not retrieved"

    assert all(i["is_archived"] for i in \
        context.achievement_get_all_res_data.get("data")["records"]), \
            "all achievements not un-archived"

    fetched_achievements = [i.get("uuid") \
        for i in context.achievement_get_all_res_data.get("data")["records"]]
    assert context.achievement_id in fetched_achievements, \
        "get all achievement not retrieved"

    # delete achievement
    delete_method(url=context.item_url)

# Fetch un-archived Achievement ------------------------------------------------------
@behave.given("There is an un-archived Achievement in database")
def step_impl_1(context):
    # Add a learner
    learner_dict = {**LEARNER_OBJECT_TEMPLATE}
    learner_dict["email_address"] = "jondoe_c2f3s17@gmail.com"
    context.learner_payload = learner_dict
    context.learner_url = f"{API_URL}/learner"
    context.learner_post_res = post_method(
        url=context.learner_url, request_body=context.learner_payload)
    context.learner_post_res_data = context.learner_post_res.json()

    assert context.learner_post_res.status_code == 200, \
        f"status is {context.learner_post_res.status_code} not 200"
    assert context.learner_post_res_data.get("success") is True, \
        "success not true"
    context.learner_id = context.learner_post_res_data["data"]["uuid"]

    # Add an archived achievement
    achievement_dict = {**ACHIEVEMENT_OBJECT_TEMPLATE}
    achievement_dict["learner_id"] = context.learner_id
    context.achievement_payload = achievement_dict
    context.achievement_url = f"{API_URL}/learner/{context.learner_id}/achievement"
    context.achievement_post_res = post_method(
        url=context.achievement_url, request_body=context.achievement_payload)
    context.achievement_post_res_data = context.achievement_post_res.json()

    assert context.achievement_post_res.status_code == 200, \
        f"status is {context.achievement_post_res.status_code} not 200"
    assert context.achievement_post_res_data.get("success") is True, \
        "success not true"
    context.achievement_id = context.achievement_post_res_data["data"]["uuid"]

    context.item_url = f"{context.achievement_url}/{context.achievement_id}"

@behave.when(
    "SNHU Administrator fetches the un-archived Achievement with correct request payload")
def step_impl_2(context):
    # Fetch an archived achievement
    url = f"{context.achievement_url}s"
    params = {"skip": 0, "limit": 30, "fetch_archive": False}
    context.achievement_get_res = get_method(url=url, query_params=params)
    context.achievement_get_res_data = context.achievement_get_res.json()

    assert context.achievement_get_res.status_code == 200, \
        f"status is {context.achievement_get_res.status_code} not 200"
    assert context.achievement_get_res_data.get("success") is True, \
        "success not true"

    # Fetch all achievements
    url = f"{API_URL}/achievements"
    params = {"skip": 0, "limit": 30, "fetch_archive": False}
    context.achievement_get_all_res = get_method(url=url, query_params=params)
    context.achievement_get_all_res_data = context.achievement_get_all_res.json()

    assert context.achievement_get_all_res.status_code == 200, \
        f"status is {context.achievement_get_all_res.status_code} not 200"
    assert context.achievement_get_all_res_data.get("success") is True, \
        "success not true"

@behave.then("the relevant Achievements are retrieved")
def step_impl_3(context):
    assert all(i["is_archived"] is False for i in \
        context.achievement_get_res_data.get("data")["records"]), \
            "all achievements not un-archived"

    fetched_achievements = [i.get("uuid") \
        for i in context.achievement_get_res_data.get("data")["records"]]
    assert context.achievement_id in fetched_achievements, \
        "achievement not retrieved"

    assert all(i["is_archived"] is False for i in \
        context.achievement_get_all_res_data.get("data")["records"]), \
            "all achievements not un-archived"

    fetched_achievements = [i.get("uuid") \
        for i in context.achievement_get_all_res_data.get("data")["records"]]
    assert context.achievement_id in fetched_achievements, \
        "get all achievement not retrieved"

    # delete achievement
    delete_method(url=context.item_url)

# Fetch archived and un-archived Achievements ---------------------------------
@behave.given("There is an archived and an un-archived Achievement in database")
def step_impl_1(context):
    # Add a learner
    learner_dict = {**LEARNER_OBJECT_TEMPLATE}
    learner_dict["email_address"] = "jondoe_c2f3s18@gmail.com"
    context.learner_payload = learner_dict
    context.learner_url = f"{API_URL}/learner"
    context.learner_post_res = post_method(
        url=context.learner_url, request_body=context.learner_payload)
    context.learner_post_res_data = context.learner_post_res.json()

    assert context.learner_post_res.status_code == 200, \
        f"status is {context.learner_post_res.status_code} not 200"
    assert context.learner_post_res_data.get("success") is True, \
        "success not true"
    context.learner_id = context.learner_post_res_data["data"]["uuid"]

    achievement_dict = {**ACHIEVEMENT_OBJECT_TEMPLATE}
    achievement_dict["learner_id"] = context.learner_id
    context.achievement_payload = achievement_dict
    context.achievement_url = f"{API_URL}/learner/{context.learner_id}/achievement"

    # Add an archived achievement
    context.achievement_post_res = post_method(
        url=context.achievement_url, request_body=context.achievement_payload)
    context.achievement_post_res_data = context.achievement_post_res.json()

    assert context.achievement_post_res.status_code == 200, \
        f"status is {context.achievement_post_res.status_code} not 200"
    assert context.achievement_post_res_data.get("success") is True, \
        "success not true"
    context.achievement_id_1 = context.achievement_post_res_data["data"]["uuid"]

    context.item_url_1 = f"{context.achievement_url}/{context.achievement_id_1}"
    context.achievement_post_res = put_method(
        url=context.item_url_1, request_body={"is_archived": True})

    # Add an un-archived achievement
    context.achievement_post_res = post_method(
        url=context.achievement_url, request_body=context.achievement_payload)
    context.achievement_post_res_data = context.achievement_post_res.json()

    assert context.achievement_post_res.status_code == 200, \
        f"status is {context.achievement_post_res.status_code} not 200"
    assert context.achievement_post_res_data.get("success") is True, \
        "success not true"
    context.achievement_id_2 = context.achievement_post_res_data["data"]["uuid"]

    context.item_url_2 = f"{context.achievement_url}/{context.achievement_id_2}"
        

@behave.when(
    "SNHU Administrator fetches the Achievement with correct request payload")
def step_impl_2(context):
    # Fetch an archived achievement
    url = f"{context.achievement_url}s"
    params = {"skip": 0, "limit": 30}
    context.achievement_get_res = get_method(url=url, query_params=params)
    context.achievement_get_res_data = context.achievement_get_res.json()

    assert context.achievement_get_res.status_code == 200, \
        f"status is {context.achievement_get_res.status_code} not 200" \
            f"{context.achievement_get_res_data}"
    assert context.achievement_get_res_data.get("success") is True, \
        "success not true"

    # Fetch all achievements
    url = f"{API_URL}/achievements"
    params = {"skip": 0, "limit": 30}
    context.achievement_get_all_res = get_method(url=url, query_params=params)
    context.achievement_get_all_res_data = context.achievement_get_all_res.json()

    assert context.achievement_get_all_res.status_code == 200, \
        f"status is {context.achievement_get_all_res.status_code} not 200" \
            f"{context.achievement_get_all_res_data}"
    assert context.achievement_get_all_res_data.get("success") is True, \
        "success not true"

@behave.then("the relevant Achievement(s) are retrieved")
def step_impl_3(context):
    fetched_achievements = [i.get("uuid") \
        for i in context.achievement_get_res_data.get("data")["records"]]
    assert context.achievement_id_1 in fetched_achievements, \
        "archived achievement not retrieved"
    assert context.achievement_id_2 in fetched_achievements, \
        "un-archived achievement not retrieved"

    fetched_achievements = [i.get("uuid") \
        for i in context.achievement_get_all_res_data.get("data")["records"]]
    assert context.achievement_id_1 in fetched_achievements, \
        "all archived achievement not retrieved"
    assert context.achievement_id_2 in fetched_achievements, \
        "all un-archived achievement not retrieved"

    # delete achievement
    delete_method(url=context.item_url_1)
    delete_method(url=context.item_url_2)

# Fetch archived Goal ---------------------------------------------------------
@behave.given("There is an archived Goal in database")
def step_impl_1(context):
    # Add an archived goal
    goal_dict = {**GOAL_OBJECT_TEMPLATE}
    context.goal_payload = goal_dict
    context.goal_url = f"{API_URL}/goal"
    context.goal_post_res = post_method(
        url=context.goal_url, request_body=context.goal_payload)
    context.goal_post_res_data = context.goal_post_res.json()

    assert context.goal_post_res.status_code == 200, \
        f"status is {context.goal_post_res.status_code} not 200"
    assert context.goal_post_res_data.get("success") is True, \
        "success not true"
    context.goal_id = context.goal_post_res_data["data"]["uuid"]

    context.item_url = f"{context.goal_url}/{context.goal_id}"
    context.goal_post_res = put_method(
        url=context.item_url, request_body={"is_archived": True})

@behave.when(
    "SNHU Administrator fetches the archived Goal with correct request payload")
def step_impl_2(context):
    # Fetch an archived goal
    url = f"{context.goal_url}"
    params = {"skip": 0, "limit": 30, "fetch_archive": True}
    context.goal_get_res = get_method(url=url, query_params=params)
    context.goal_get_res_data = context.goal_get_res.json()

    assert context.goal_get_res.status_code == 200, \
        f"status is {context.goal_get_res.status_code} not 200"
    assert context.goal_get_res_data.get("success") is True, \
        "success not true"

@behave.then("the relevant Goal is retrieved")
def step_impl_3(context):
    assert all(i["is_archived"] for i in \
        context.goal_get_res_data.get("data")["records"]), \
            "all goals not un-archived"

    fetched_goals = [i.get("uuid") for i in context.goal_get_res_data.get("data")["records"]]
    assert context.goal_id in fetched_goals, "goal not retrieved"

    # delete goal
    delete_method(url=context.item_url)

# Fetch un-archived Goal ------------------------------------------------------
@behave.given("There is an un-archived Goal in database")
def step_impl_1(context):
    # Add an archived goal
    goal_dict = {**GOAL_OBJECT_TEMPLATE}
    context.goal_payload = goal_dict
    context.goal_url = f"{API_URL}/goal"
    context.goal_post_res = post_method(
        url=context.goal_url, request_body=context.goal_payload)
    context.goal_post_res_data = context.goal_post_res.json()

    assert context.goal_post_res.status_code == 200, \
        f"status is {context.goal_post_res.status_code} not 200"
    assert context.goal_post_res_data.get("success") is True, \
        "success not true"
    context.goal_id = context.goal_post_res_data["data"]["uuid"]

    context.item_url = f"{context.goal_url}/{context.goal_id}"

@behave.when(
    "SNHU Administrator fetches the un-archived Goal with correct request payload")
def step_impl_2(context):
    # Fetch an archived goal
    url = f"{context.goal_url}"
    params = {"skip": 0, "limit": 30, "fetch_archive": False}
    context.goal_get_res = get_method(url=url, query_params=params)
    context.goal_get_res_data = context.goal_get_res.json()

    assert context.goal_get_res.status_code == 200, \
        f"status is {context.goal_get_res.status_code} not 200"
    assert context.goal_get_res_data.get("success") is True, \
        "success not true"

@behave.then("the relevant Goals are retrieved")
def step_impl_3(context):
    assert all(i["is_archived"] is False for i in \
        context.goal_get_res_data.get("data")["records"]), \
            "all goals not un-archived"

    fetched_goals = [i.get("uuid") for i in context.goal_get_res_data.get("data")["records"]]
    assert context.goal_id in fetched_goals, "goal not retrieved"

    # delete goal
    delete_method(url=context.item_url)


# Fetch archived and un-archived goals ----------------------------------------
@behave.given("There is an archived and an un-archived Goal in database")
def step_impl_1(context):
    goal_dict = {**GOAL_OBJECT_TEMPLATE}
    context.goal_payload = goal_dict
    context.goal_url = f"{API_URL}/goal"

    # Add an archived goal
    context.goal_post_res = post_method(
        url=context.goal_url, request_body=context.goal_payload)
    context.goal_post_res_data = context.goal_post_res.json()

    assert context.goal_post_res.status_code == 200, \
        f"status is {context.goal_post_res.status_code} not 200"
    assert context.goal_post_res_data.get("success") is True, \
        "success not true"
    context.goal_id_1 = context.goal_post_res_data["data"]["uuid"]

    context.item_url_1 = f"{context.goal_url}/{context.goal_id_1}"
    context.goal_post_res = put_method(
        url=context.item_url_1, request_body={"is_archived": True})

    # Add an un-archived goal
    context.goal_post_res = post_method(
        url=context.goal_url, request_body=context.goal_payload)
    context.goal_post_res_data = context.goal_post_res.json()

    assert context.goal_post_res.status_code == 200, \
        f"status is {context.goal_post_res.status_code} not 200"
    assert context.goal_post_res_data.get("success") is True, \
        "success not true"
    context.goal_id_2 = context.goal_post_res_data["data"]["uuid"]

    context.item_url_2 = f"{context.goal_url}/{context.goal_id_2}"

@behave.when(
    "SNHU Administrator fetches the Goal with correct request payload")
def step_impl_2(context):
    # Fetch an archived goal
    url = f"{context.goal_url}"
    params = {"skip": 0, "limit": 30}
    context.goal_get_res = get_method(url=url, query_params=params)
    context.goal_get_res_data = context.goal_get_res.json()

    assert context.goal_get_res.status_code == 200, \
        f"status is {context.goal_get_res.status_code} not 200"
    assert context.goal_get_res_data.get("success") is True, \
        "success not true"

@behave.then("the relevant Goal(s) are retrieved")
def step_impl_3(context):
    fetched_goals = [i.get("uuid") for i in context.goal_get_res_data.get("data")["records"]]
    assert context.goal_id_1 in fetched_goals, "archived goal not retrieved"
    assert context.goal_id_2 in fetched_goals, "un-archived goal not retrieved"

    # delete goal
    delete_method(url=context.item_url_1)
    delete_method(url=context.item_url_2)