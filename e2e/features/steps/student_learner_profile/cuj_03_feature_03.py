"""
Feature 03 - Negative scenarios for CRUD APIs for managing learner, learner-profile, achievement and goal data in SLP
"""

import behave
from uuid import uuid4
import sys
from copy import deepcopy
sys.path.append("../")
from e2e.setup import post_method, get_method, put_method, delete_method
from e2e.test_config import API_URL_LEARNER_PROFILE_SERVICE
from e2e.test_object_schemas import (LEARNER_OBJECT_TEMPLATE, GOAL_OBJECT_TEMPLATE,
                                ACHIEVEMENT_OBJECT_TEMPLATE, LEARNER_PROFILE_TEMPLATE)

# ------------------------------ Scenario 01 -----------------------------------
@behave.given("that no learner with same e-mail id already exists, format the API request url to create a learner with one or more required fields missing in request payload")
def step_impl1(context):
  learner_dict = deepcopy(LEARNER_OBJECT_TEMPLATE)
  learner_dict["email_address"] = f"{uuid4()}_test_cuj3_feature03_scenario01@gmail.com"
  del learner_dict["first_name"]
  del learner_dict["uuid"]
  
  context.req_body = learner_dict
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner"


@behave.when("API request is sent to create learner with one or more required fields missing in request payload")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("SLP Service will throw a validation error message while trying to create the learner as required field is missing")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data["success"] is False, "Success not False"
  assert context.res_data["message"] == "Validation Failed", "Expected message not returned"
  assert context.res_data["data"][0]["msg"] == "field required", "Expected message not returned"



# ------------------------------ Scenario 02 -----------------------------------
@behave.given("that a Learner account exists, format the API request url to update non-editable field of learner in request payload")
def step_impl1(context):
  learner_dict = deepcopy(LEARNER_OBJECT_TEMPLATE)
  learner_dict["email_address"] = f"{uuid4()}_test_cuj3_feature03_scenario02@gmail.com"
  del learner_dict["uuid"]

  # post request to create a learner
  learner_api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner"
  post_response = post_method(url=learner_api_url, request_body=learner_dict)
  post_response_data = post_response.json()

  assert post_response.status_code == 200, "Status not 200 for post request"
  assert post_response_data.get("success") is True, "Success not true for post request"
  assert post_response_data.get("message") == "Successfully created the learner", "Expected response not same for post request"
  assert post_response_data.get("data").get("first_name") == learner_dict.get("first_name"), "Expected response not same for post request"

  learner_uuid = post_response_data["data"]["uuid"]
  updated_data = post_response_data["data"]
  
  removed_fields = [
      "first_name", "middle_name", "last_name", "suffix", "prefix", "uuid",
      "birth_date", "created_time", "last_modified_time"
  ]
  for i in removed_fields:
    del updated_data[i]
  updated_data["middle_name"] = "RandomLearner"

  context.req_body = updated_data
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{learner_uuid}"


@behave.when("API request is sent to update non-editable field of the learner in request payload")
def step_impl2(context):
  context.res = put_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("SLP Service will throw a validation error message while trying to update the learner as non-editable field was attempted to be updated")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Validation Failed", "Expected message not returned"
  assert context.res_data["data"][0]["msg"] == "extra fields not permitted", "Expected message not returned"
  

# ------------------------------ Scenario 03 -----------------------------------
@behave.given("that a Learner account exists, format the API request url to update the learner by providing incorrect uuid in request payload")
def step_impl1(context):
  learner_dict = deepcopy(LEARNER_OBJECT_TEMPLATE)
  learner_dict["email_address"] = f"{uuid4()}_test_cuj3_feature03_scenario03@gmail.com"
  del learner_dict["uuid"]

  # post request to create a learner
  learner_api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner"
  post_response = post_method(url=learner_api_url, request_body=learner_dict)
  post_response_data = post_response.json()

  assert post_response.status_code == 200, "Status not 200 for post request"
  assert post_response_data.get("success") is True, "Success not true for post request"
  assert post_response_data.get("message") == "Successfully created the learner", "Expected response not same for post request"
  assert post_response_data.get("data").get("first_name") == learner_dict.get("first_name"), "Expected response not same for post request"

  learner_uuid = post_response_data["data"]["uuid"]
  updated_data = post_response_data["data"]
  invalid_uuid = "random_id"
  context.invalid_uuid = invalid_uuid
  removed_fields = [
      "first_name", "middle_name", "last_name", "suffix", "prefix", "uuid",
      "birth_date", "created_time", "last_modified_time"
  ]
  for i in removed_fields:
    del updated_data[i]
  updated_data["first_name"] = "RandomLearner"

  context.req_body = updated_data
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{invalid_uuid}"


@behave.when("API request is sent to update learner with incorrect uuid in request payload")
def step_impl2(context):
  context.res = put_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("SLP Service will throw a validation error message while trying to update learner as incorrect uuid was provided")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["message"] == f"Learner with uuid {context.invalid_uuid} not found", "Expected message not returned"


# ------------------------------ Scenario 04 -----------------------------------
@behave.given("that a Learner account exists, format the API request url to fetch the learner by providing incorrect uuid in request payload")
def step_impl1(context):
  learner_dict = deepcopy(LEARNER_OBJECT_TEMPLATE)
  learner_dict["email_address"] = f"{uuid4()}_test_cuj3_feature03_scenario04@gmail.com"
  del learner_dict["uuid"]

  # post request to create a learner
  learner_api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner"
  post_response = post_method(url=learner_api_url, request_body=learner_dict)
  post_response_data = post_response.json()

  assert post_response.status_code == 200, "Status not 200 for post request"
  assert post_response_data.get("success") is True, "Success not true for post request"
  assert post_response_data.get("message") == "Successfully created the learner", "Expected response not same for post request"
  assert post_response_data.get("data").get("first_name") == learner_dict.get("first_name"), "Expected response not same for post request"

  invalid_uuid = "random_id"
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{invalid_uuid}"


@behave.when("API request is sent to fetch learner with incorrect uuid in request payload")
def step_impl2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("SLP Service will throw an error message while trying to fetch the learner as incorrect uuid was provided")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["success"] is False, "Success is not False"
  assert context.res_data["message"] == "Learner with uuid random_id not found", "Expected message not returned"


# ------------------------------ Scenario 05 -----------------------------------
@behave.given("that a Learner account exists, format the API request url to delete the learner by providing incorrect uuid in request payload")
def step_impl1(context):
  learner_dict = deepcopy(LEARNER_OBJECT_TEMPLATE)
  learner_dict["email_address"] = f"{uuid4()}_test_cuj3_feature03_scenario05@gmail.com"
  del learner_dict["uuid"]

  # post request to create a learner
  learner_api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner"
  post_response = post_method(url=learner_api_url, request_body=learner_dict)
  post_response_data = post_response.json()

  assert post_response.status_code == 200, "Status not 200 for post request"
  assert post_response_data.get("success") is True, "Success not true for post request"
  assert post_response_data.get("message") == "Successfully created the learner", "Expected response not same for post request"
  assert post_response_data.get("data").get("first_name") == learner_dict.get("first_name"), "Expected response not same for post request"

  invalid_uuid = "random_id"
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{invalid_uuid}"


@behave.when("API request is sent to delete learner with incorrect uuid in request payload")
def step_impl2(context):
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("SLP Service will throw a validation error message while trying to delete learner as incorrect uuid was provided")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Learner with uuid random_id not found", "Expected message not returned"



# ------------------------------ Scenario 06 -----------------------------------
@behave.given("that a Learner account exists, format the API request url to create a learner profile by providing invalid learner_id in request payload")
def step_impl1(context):
  learner_dict = deepcopy(LEARNER_OBJECT_TEMPLATE)
  learner_dict["email_address"] = f"{uuid4()}test_cuj3_feature03_scenario06@gmail.com"
  del learner_dict["uuid"]

  # post request to create a learner
  learner_api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner"
  post_response = post_method(url=learner_api_url, request_body=learner_dict)
  post_response_data = post_response.json()
  assert post_response.status_code == 200, "Status not 200 for post request"
  assert post_response_data.get("success") is True, "Success not true for post request"
  assert post_response_data.get("message") == "Successfully created the learner", "Expected response not same for post request"
  assert post_response_data.get("data").get("first_name") == learner_dict.get("first_name"), "Expected response not same for post request"

  # post request to create a learner-profile
  learner_uuid = post_response_data["data"]["uuid"]
  learner_profile_dict = deepcopy(LEARNER_PROFILE_TEMPLATE)
  learner_profile_dict["learner_id"] = learner_uuid

  invalid_learner_id = "random_id"
  
  context.req_body = learner_profile_dict
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{invalid_learner_id}/learner-profile"


@behave.when("API request is sent to create learner profile with invalid learner_id in request payload")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("SLP Service will throw a validation error message while trying to create the learner profile as invalid learner_id was provided")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["success"] is False, "Success not False"
  assert context.res_data["message"] == "Learner with uuid random_id not found", "Expected message not returned"



# ------------------------------ Scenario 07 -----------------------------------
@behave.given("that a Learner profile exists, format the API request url to update learner profile by including invalid extra field in request payload")
def step_impl1(context):
  learner_dict = deepcopy(LEARNER_OBJECT_TEMPLATE)
  learner_dict["email_address"] = f"{uuid4()}test_cuj3_feature03_scenario07@gmail.com"
  del learner_dict["uuid"]

  # post request to create a learner
  learner_api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner"
  post_response = post_method(url=learner_api_url, request_body=learner_dict)
  post_response_data = post_response.json()
  assert post_response.status_code == 200, "Status not 200 for post request"
  assert post_response_data.get("success") is True, "Success not true for post request"
  assert post_response_data.get("message") == "Successfully created the learner", "Expected response not same for post request"
  assert post_response_data.get("data").get("first_name") == learner_dict.get("first_name"), "Expected response not same for post request"

  # post request to create a learner-profile
  learner_uuid = post_response_data["data"]["uuid"]
  learner_profile_dict = deepcopy(LEARNER_PROFILE_TEMPLATE)
  learner_profile_dict["learner_id"] = learner_uuid
  learner_profile_api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{learner_uuid}/learner-profile"
  lp_post_response = post_method(url=learner_profile_api_url, request_body=learner_profile_dict)
  lp_post_response_data = lp_post_response.json()
  assert lp_post_response.status_code == 200, "Status not 200 for post request"
  assert lp_post_response_data.get("success") is True, "Success not true for post request"
  assert lp_post_response_data.get("message") == "Successfully created the learner profile", "Expected response not same for post request"
  assert lp_post_response_data.get("data").get("learner_id") == learner_profile_dict.get("learner_id"), "Expected response not same for post request"

  learner_profile_uuid = lp_post_response_data["data"]["uuid"]
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{learner_uuid}/learner-profile"
  context.req_body = learner_profile_dict


@behave.when("API request is sent to update a learner profile by providing invalid extra field in request payload")
def step_impl2(context):
  context.res = put_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("SLP Service will throw a validation error message while trying to update the learner profile as invalid extra field was provided")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data["success"] is False, "Success not False"
  assert context.res_data["message"] == "Validation Failed", "Expected message not returned"
  assert context.res_data["data"][0]["msg"] == "extra fields not permitted", "Expected message not returned"



# ------------------------------ Scenario 08 -----------------------------------
@behave.given("that a Learner profile exists, format the API request url to update non-editable field of learner profile in request payload")
def step_impl1(context):
  learner_dict = deepcopy(LEARNER_OBJECT_TEMPLATE)
  learner_dict["email_address"] = f"{uuid4()}test_cuj3_feature03_scenario08@gmail.com"
  del learner_dict["uuid"]

  # post request to create a learner
  learner_api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner"
  post_response = post_method(url=learner_api_url, request_body=learner_dict)
  post_response_data = post_response.json()
  assert post_response.status_code == 200, "Status not 200 for post request"
  assert post_response_data.get("success") is True, "Success not true for post request"
  assert post_response_data.get("message") == "Successfully created the learner", "Expected response not same for post request"
  assert post_response_data.get("data").get("first_name") == learner_dict.get("first_name"), "Expected response not same for post request"

  # post request to create a learner-profile
  learner_uuid = post_response_data["data"]["uuid"]
  learner_profile_dict = deepcopy(LEARNER_PROFILE_TEMPLATE)
  learner_profile_dict["learner_id"] = learner_uuid
  learner_profile_api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{learner_uuid}/learner-profile"
  lp_post_response = post_method(url=learner_profile_api_url, request_body=learner_profile_dict)
  lp_post_response_data = lp_post_response.json()
  assert lp_post_response.status_code == 200, "Status not 200 for post request"
  assert lp_post_response_data.get("success") is True, "Success not true for post request"
  assert lp_post_response_data.get("message") == "Successfully created the learner profile", "Expected response not same for post request"
  assert lp_post_response_data.get("data").get("learner_id") == learner_profile_dict.get("learner_id"), "Expected response not same for post request"

  learner_profile_uuid = lp_post_response_data["data"]["uuid"]
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{learner_uuid}/learner-profile"
  learner_profile_dict["enrollment_information"] = {}
  context.req_body = learner_profile_dict


@behave.when("API request is sent to update non-editable field of the learner profile in request payload")
def step_impl2(context):
  context.res = put_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("SLP Service will throw a validation error message while trying to update the learner profile as non-editable field was attempted to be updated")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data["success"] is False, "Success not False"
  assert context.res_data["message"] == "Validation Failed", "Expected message not returned"
  assert context.res_data["data"][0]["msg"] == "extra fields not permitted", "Expected message not returned"



# ------------------------------ Scenario 09 -----------------------------------
@behave.given("that a Learner profile exists, format the API request url to fetch the learner profile by providing incorrect learner uuid in request payload")
def step_impl1(context):
  learner_dict = deepcopy(LEARNER_OBJECT_TEMPLATE)
  learner_dict["email_address"] = f"{uuid4()}test_cuj3_feature03_scenario09@gmail.com"
  del learner_dict["uuid"]

  # post request to create a learner
  learner_api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner"
  post_response = post_method(url=learner_api_url, request_body=learner_dict)
  post_response_data = post_response.json()
  assert post_response.status_code == 200, "Status not 200 for post request"
  assert post_response_data.get("success") is True, "Success not true for post request"
  assert post_response_data.get("message") == "Successfully created the learner", "Expected response not same for post request"
  assert post_response_data.get("data").get("first_name") == learner_dict.get("first_name"), "Expected response not same for post request"

  # post request to create a learner-profile
  learner_uuid = post_response_data["data"]["uuid"]
  learner_profile_dict = deepcopy(LEARNER_PROFILE_TEMPLATE)
  learner_profile_dict["learner_id"] = learner_uuid
  learner_profile_api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{learner_uuid}/learner-profile"
  lp_post_response = post_method(url=learner_profile_api_url, request_body=learner_profile_dict)
  lp_post_response_data = lp_post_response.json()
  assert lp_post_response.status_code == 200, "Status not 200 for post request"
  assert lp_post_response_data.get("success") is True, "Success not true for post request"
  assert lp_post_response_data.get("message") == "Successfully created the learner profile", "Expected response not same for post request"
  assert lp_post_response_data.get("data").get("learner_id") == learner_profile_dict.get("learner_id"), "Expected response not same for post request"

  invalid_learner_id = "random_id"
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{invalid_learner_id}/learner-profile"


@behave.when("API request is sent to fetch learner profile with incorrect learner uuid in request payload")
def step_impl2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()



@behave.then("SLP Service will throw an error message while trying to fetch the learner profile as incorrect learner uuid was provided")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["success"] is False, "Success not False"
  assert context.res_data["message"] == "Learner with uuid random_id not found", "Expected message not returned"



# ------------------------------ Scenario 10 -----------------------------------
@behave.given("that a Learner profile exists, format the API request url to delete the learner profile by providing incorrect learner uuid in request payload")
def step_impl1(context):
  learner_dict = deepcopy(LEARNER_OBJECT_TEMPLATE)
  learner_dict["email_address"] = f"{uuid4()}test_cuj3_feature03_scenario10@gmail.com"
  del learner_dict["uuid"]

  # post request to create a learner
  learner_api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner"
  post_response = post_method(url=learner_api_url, request_body=learner_dict)
  post_response_data = post_response.json()
  assert post_response.status_code == 200, "Status not 200 for post request"
  assert post_response_data.get("success") is True, "Success not true for post request"
  assert post_response_data.get("message") == "Successfully created the learner", "Expected response not same for post request"
  assert post_response_data.get("data").get("first_name") == learner_dict.get("first_name"), "Expected response not same for post request"

  # post request to create a learner-profile
  learner_uuid = post_response_data["data"]["uuid"]
  learner_profile_dict = deepcopy(LEARNER_PROFILE_TEMPLATE)
  learner_profile_dict["learner_id"] = learner_uuid
  learner_profile_api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{learner_uuid}/learner-profile"
  lp_post_response = post_method(url=learner_profile_api_url, request_body=learner_profile_dict)
  lp_post_response_data = lp_post_response.json()
  assert lp_post_response.status_code == 200, "Status not 200 for post request"
  assert lp_post_response_data.get("success") is True, "Success not true for post request"
  assert lp_post_response_data.get("message") == "Successfully created the learner profile", "Expected response not same for post request"
  assert lp_post_response_data.get("data").get("learner_id") == learner_profile_dict.get("learner_id"), "Expected response not same for post request"

  invalid_learner_id = "random_id"
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{invalid_learner_id}/learner-profile"


@behave.when("API request is sent to delete learner profile with incorrect learner uuid in request payload")
def step_impl2(context):
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()



@behave.then("SLP Service will throw a validation error message while trying to delete learner profile as incorrect learner uuid was provided")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["success"] is False, "Success not False"
  assert context.res_data["message"] == "Learner with uuid random_id not found", "Expected message not returned"



# ------------------------------ Scenario 11 -----------------------------------
@behave.given("that a Learner account exists, format the API request url to create an achievement with one or more required fields missing in request payload")
def step_impl1(context):
  # post request to create an achievement
  achievement_dict = deepcopy(ACHIEVEMENT_OBJECT_TEMPLATE)
  del achievement_dict["type"]

  context.req_body = achievement_dict
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/achievement"


@behave.when("API request is sent to create achievement with one or more required fields missing in request payload")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("SLP Service will throw a validation error message as one or more required fields are missing")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data["success"] is False, "Success not False"
  assert context.res_data["message"] == "Validation Failed", "Expected message not returned"
  assert context.res_data["data"][0]["msg"] == "field required", "Expected message not returned"




# ------------------------------ Scenario 12 -----------------------------------
@behave.given("that an Achievement exists, format the API request url to update the achievement with required field missing in request payload")
def step_impl1(context):
  # post request to create an achievement
  achievement_dict = deepcopy(ACHIEVEMENT_OBJECT_TEMPLATE)
  achievement_api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/achievement"
  achv_post_response = post_method(url=achievement_api_url, request_body=achievement_dict)
  achv_post_response_data = achv_post_response.json()
  assert achv_post_response.status_code == 200, "Status not 200 for post request"
  assert achv_post_response_data.get("success") is True, "Success not true for post request"
  assert achv_post_response_data.get("message") == "Successfully created the achievement", "Expected response not same for post request"
  assert achv_post_response_data.get("data").get("type") == achievement_dict.get("type"), "Expected response not same for post request"

  achievement_uuid = achv_post_response_data.get("data").get("uuid")
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/achievement/{achievement_uuid}"
  updated_data = achv_post_response_data["data"]
  del updated_data["uuid"]
  updated_data["description"] = "Test description"
  context.req_body = updated_data


@behave.when("API request is sent to update achievement with required field missing in request payload")
def step_impl2(context):
  context.res = put_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("SLP Service will throw a validation error message as required field is missing")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data["success"] is False, "Success not False"
  assert context.res_data["message"] == "Validation Failed", "Expected message not returned"




# ------------------------------ Scenario 13 -----------------------------------
@behave.given("that an Achievement exists, format the API request url to fetch the achievement by providing incorrect uuid in request payload")
def step_impl1(context):
  # post request to create an achievement
  achievement_dict = deepcopy(ACHIEVEMENT_OBJECT_TEMPLATE)
  achievement_api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/achievement"
  achv_post_response = post_method(url=achievement_api_url, request_body=achievement_dict)
  achv_post_response_data = achv_post_response.json()
  assert achv_post_response.status_code == 200, "Status not 200 for post request"
  assert achv_post_response_data.get("success") is True, "Success not true for post request"
  assert achv_post_response_data.get("message") == "Successfully created the achievement", "Expected response not same for post request"
  assert achv_post_response_data.get("data").get("type") == achievement_dict.get("type"), "Expected response not same for post request"

  invalid_achievement_uuid = "random_id"
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/achievement/{invalid_achievement_uuid}"


@behave.when("API request is sent to fetch achievement with incorrect uuid in request payload")
def step_impl2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("SLP Service will throw an error message while trying to fetch achievement as incorrect uuid was provided")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["success"] is False, "Success not False"
  assert context.res_data["message"] == "Achievement with uuid random_id not found", "Expected message not returned"




# ------------------------------ Scenario 14 -----------------------------------
@behave.given("that an Achievement exists, format the API request url to delete the achievement by providing incorrect uuid in request payload")
def step_impl1(context):
  # post request to create an achievement
  achievement_dict = deepcopy(ACHIEVEMENT_OBJECT_TEMPLATE)
  achievement_api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/achievement"
  achv_post_response = post_method(url=achievement_api_url, request_body=achievement_dict)
  achv_post_response_data = achv_post_response.json()
  assert achv_post_response.status_code == 200, "Status not 200 for post request"
  assert achv_post_response_data.get("success") is True, "Success not true for post request"
  assert achv_post_response_data.get("message") == "Successfully created the achievement", "Expected response not same for post request"
  assert achv_post_response_data.get("data").get("type") == achievement_dict.get("type"), "Expected response not same for post request"

  invalid_achievement_uuid = "random_id"
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/achievement/{invalid_achievement_uuid}"


@behave.when("API request is sent to delete achievement with incorrect uuid in request payload")
def step_impl2(context):
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("SLP Service will throw a validation error message while trying to delete achievement as incorrect uuid was provided")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 422"
  assert context.res_data["success"] is False, "Success not False"
  assert context.res_data["message"] == "Achievement with uuid random_id not found", "Expected message not returned"



# ------------------------------ Scenario 15 -----------------------------------
@behave.given("format the API request url to create a goal with one or more required fields missing in request payload")
def step_impl1(context):
  wrong_goal_dict = deepcopy(GOAL_OBJECT_TEMPLATE)
  del wrong_goal_dict["name"]
  context.req_body = wrong_goal_dict
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/goal"


@behave.when("API request is sent to create goal with one or more required fields missing in request payload")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()



@behave.then("SLP Service will throw a validation error message while creating the goal as one or more required fields are missing")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data["success"] is False, "Success not False"
  assert context.res_data["message"] == "Validation Failed", "Expected message not returned"
  assert context.res_data["data"][0]["msg"] == "field required", "Expected message not returned"



# ------------------------------ Scenario 16 -----------------------------------
@behave.given("that a goal exists, format the API request url to update the goal by providing invalid uuid in request payload")
def step_impl1(context):
  goal_dict = deepcopy(GOAL_OBJECT_TEMPLATE)

  # post request to create a goal
  goal_api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/goal"
  post_response = post_method(url=goal_api_url, request_body=goal_dict)
  post_response_data = post_response.json()
  assert post_response.status_code == 200, "Status not 200 for post request"
  assert post_response_data.get("success") is True, "Success not true for post request"
  assert post_response_data.get("message") == "Successfully created the goal", "Expected response not same for post request"
  assert post_response_data.get("data").get("name") == goal_dict.get("name"), "Expected response not same for post request"

  invalid_goal_id = "random_id"
  context.url = f"{goal_api_url}/{invalid_goal_id}"
  context.req_body = goal_dict

@behave.when("API request is sent to update goal by providing invalid uuid in request payload")
def step_impl2(context):
  context.res = put_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("SLP Service will throw a validation error message while updating the goal as invalid uuid provided")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["success"] is False, "Success not False"
  assert context.res_data["message"] == "Goal with uuid random_id not found", "Expected message not returned"


# ------------------------------ Scenario 17 -----------------------------------
@behave.given("that a goal exists, format the API request url to fetch the goal by providing incorrect uuid in request payload")
def step_impl1(context):
  goal_dict = deepcopy(GOAL_OBJECT_TEMPLATE)

  # post request to create a goal
  goal_api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/goal"
  post_response = post_method(url=goal_api_url, request_body=goal_dict)
  post_response_data = post_response.json()
  assert post_response.status_code == 200, "Status not 200 for post request"
  assert post_response_data.get("success") is True, "Success not true for post request"
  assert post_response_data.get("message") == "Successfully created the goal", "Expected response not same for post request"
  assert post_response_data.get("data").get("name") == goal_dict.get("name"), "Expected response not same for post request"

  invalid_goal_id = "random_id"
  context.url = f"{goal_api_url}/{invalid_goal_id}"


@behave.when("API request is sent to fetch goal with incorrect uuid in request payload")
def step_impl2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("SLP Service will throw an error message as incorrect uuid was provided")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["success"] is False, "Success not False"
  assert context.res_data["message"] == "Goal with uuid random_id not found", "Expected message not returned"


# ------------------------------ Scenario 18 -----------------------------------
@behave.given("that a goal exists, format the API request url to delete the goal by providing incorrect uuid in request payload")
def step_impl1(context):
  goal_dict = deepcopy(GOAL_OBJECT_TEMPLATE)

  # post request to create a goal
  goal_api_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/goal"
  post_response = post_method(url=goal_api_url, request_body=goal_dict)
  post_response_data = post_response.json()
  assert post_response.status_code == 200, "Status not 200 for post request"
  assert post_response_data.get("success") is True, "Success not true for post request"
  assert post_response_data.get("message") == "Successfully created the goal", "Expected response not same for post request"
  assert post_response_data.get("data").get("name") == goal_dict.get("name"), "Expected response not same for post request"

  invalid_goal_id = "random_id"
  context.url = f"{goal_api_url}/{invalid_goal_id}"


@behave.when("API request is sent to delete goal with incorrect uuid in request payload")
def step_impl2(context):
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("SLP Service will throw a validation error message while trying to delete goal as incorrect uuid was provided")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["success"] is False, "Success not False"
  assert context.res_data["message"] == "Goal with uuid random_id not found", "Expected message not returned"
