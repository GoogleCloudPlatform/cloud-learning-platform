"""
Feature 01 - Import achievement, and learner account data from json files
"""

import behave
import os
from e2e.setup import post_method, get_method
from e2e.test_config import API_URL_LEARNER_PROFILE_SERVICE, TESTING_OBJECTS_PATH
from common.models import Learner, Achievement


INVALID_JSON_FILE_PATH = os.path.join("testing_objects", "invalid_json_file.json")

SAMPLE_CSV_FILE_PATH = os.path.join("testing_objects", "sample_csv_file.csv")


# ------------------------------Scenario 1-----------------------------------

@behave.given("We have access to learner data in json format with all required fields")
def step_impl_1(context):
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "learner.json")
  assert os.path.exists(context.json_file_path)


@behave.when("SLP service accesses this learner data from given json file with all required fields")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as learners_json_file:
    context.res = post_method(f"{context.url}/learner/import/json",
                       files={"json_file": learners_json_file})
    context.res_data = context.res.json()


@behave.then("learner data from given json file should get ingested into SLP service")
def step_impl_3(context):
  assert context.res.status_code == 200, f"Status {context.res.status_code}"
  assert isinstance(context.res_data.get("data"), list), "Response is not a list"
  assert len(
      context.res_data.get("data")) > 0, "Empty list returned in import json api"
  
  inserted_learner_ids = context.res_data.get("data")
  inserted_learners = [Learner.find_by_id(id) for id in inserted_learner_ids]
  inserted_learner_names = [i.first_name for i in inserted_learners]
  
  api_url = f"{context.url}/learners"
  params = {"skip": 0, "limit": 30}

  resp = get_method(api_url, query_params=params)
  resp_data = resp.json()
  assert resp.status_code == 200, f"Status {resp.status_code}"
  learner_names = [i.get("first_name") for i in resp_data.get("data")["records"]]
  for name in inserted_learner_names:
    assert name in learner_names


# ------------------------------Scenario 2-----------------------------------

@behave.given("We have access to learner data in csv format")
def step_impl_1(context):
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}"
  context.json_file_path = SAMPLE_CSV_FILE_PATH
  context.required_fields = "'name','description'"
  assert os.path.exists(context.json_file_path)


@behave.when("SLP service accesses this learner data in csv formart instead of JSON format")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as learner_csv_file:
    context.res = post_method(f"{context.url}/learner/import/json",
                       files={"json_file": learner_csv_file})
    context.res_data = context.res.json()


@behave.then("SLP service will throw a validation error and learner data will not get imported")
def step_impl_3(context):
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data.get("success") is False, "Success not False"
  assert context.res_data.get("message") == "Valid JSON file type is supported", "Expected message not returned"

# ------------------------------Scenario 3-----------------------------------

@behave.given("We have access to learner data in json format with invalid format")
def step_impl_1(context):
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}"
  context.json_file_path = INVALID_JSON_FILE_PATH
  assert os.path.exists(context.json_file_path)


@behave.when("SLP service accesses this learner data from given json file with invalid format")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as invalid_json_file:
    context.res = post_method(f"{context.url}/learner/import/json",
                       files={"json_file": invalid_json_file})
    context.res_data = context.res.json()


@behave.then("SLP service will throw a validation error due to invalid format of the json file and learner data will not get imported")
def step_impl_3(context):
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data.get("success") is False, "Success not False"
  assert context.res_data.get("message") == "Provided JSON is invalid", "Expected message not returned"


# ------------------------------Scenario 4-----------------------------------

@behave.given("We have access to learner data in json format with missing fields")
def step_impl_1(context):
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "learners_invalid.json")
  context.required_fields = "'name','description'"
  assert os.path.exists(context.json_file_path)


@behave.when("SLP service accesses this learner data from given json file with missing fields")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as invalid_json_file:
    context.res = post_method(f"{context.url}/learner/import/json",
                       files={"json_file": invalid_json_file})
    context.res_data = context.res.json()


@behave.then("SLP service will throw a validation error and learner data will not get imported as some required fields are missing")
def step_impl_3(context):
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data.get("success") is False, "Success not False"
  assert context.res_data.get("message") == "Missing required fields - 'first_name','email_address','employer_email'", "Expected message not returned"



# ------------------------------Scenario 5-----------------------------------

@behave.given("We have access to achievement data in json format with all required fields")
def step_impl_1(context):
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "achievements.json")
  assert os.path.exists(context.json_file_path)


@behave.when("SLP service accesses this achievement data from given json file with all required fields")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as achievement_json_file:
    context.res = post_method(f"{context.url}/achievement/import/json",
                       files={"json_file": achievement_json_file})
    context.res_data = context.res.json()

@behave.then("achievement data from given json file should get ingested into SLP service")
def step_impl_3(context):
  assert context.res.status_code == 200, f"Status {context.res.status_code}"
  assert isinstance(context.res_data.get("data"), list), "Response is not a list"
  assert len(
      context.res_data.get("data")) > 0, "Empty list returned in import json api"
  
  inserted_achievement_ids = context.res_data.get("data")
  inserted_achievements = [Achievement.find_by_id(id) for id in inserted_achievement_ids]
  inserted_achievement_names = [i.name for i in inserted_achievements]
  
  api_url = f"{context.url}/achievements"
  params = {"skip": 0, "limit": len(inserted_achievement_names)}

  resp = get_method(api_url, query_params=params)
  resp_data = resp.json()
  assert resp.status_code == 200, f"Status {resp.status_code}"
  achievement_names = [i.get("name") for i in resp_data.get("data")["records"]]
  for name in inserted_achievement_names:
    assert name in achievement_names


# ------------------------------Scenario 6-----------------------------------

@behave.given("We have access to achievement data in csv format")
def step_impl_1(context):
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}"
  context.json_file_path = SAMPLE_CSV_FILE_PATH
  context.required_fields = "'name','description'"
  assert os.path.exists(context.json_file_path)


@behave.when("SLP service accesses this achievement data in csv formart instead of JSON format")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as achievement_csv_file:
    context.res = post_method(f"{context.url}/achievement/import/json",
                       files={"json_file": achievement_csv_file})
    context.res_data = context.res.json()
    


@behave.then("SLP service will throw a validation error and achievement data will not get imported")
def step_impl_3(context):
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data.get("success") is False, "Success not False"
  assert context.res_data.get("message") == "Valid JSON file type is supported", "Expected message not returned"



# ------------------------------Scenario 7-----------------------------------

@behave.given("We have access to achievement data in json format with invalid format")
def step_impl_1(context):
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}"
  context.json_file_path = INVALID_JSON_FILE_PATH
  assert os.path.exists(context.json_file_path)


@behave.when("SLP service accesses this achievement data from given json file with invalid format")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as invalid_json_file:
    context.res = post_method(f"{context.url}/achievement/import/json",
                       files={"json_file": invalid_json_file})
    context.res_data = context.res.json()


@behave.then("SLP service will throw a validation error due to invalid format of the json file and achievement data will not get imported")
def step_impl_3(context):
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data.get("success") is False, "Success not False"
  assert context.res_data.get("message") == "Provided JSON is invalid", "Expected message not returned"


# ------------------------------Scenario 8-----------------------------------

@behave.given("We have access to achievement data in json format with missing fields")
def step_impl_1(context):
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "achievements_invalid.json")
  context.required_fields = "'name','description'"
  assert os.path.exists(context.json_file_path)


@behave.when("SLP service accesses this achievement data from given json file with missing fields")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as invalid_json_file:
    context.res = post_method(f"{context.url}/achievement/import/json",
                       files={"json_file": invalid_json_file})
    context.res_data = context.res.json()


@behave.then("SLP service will throw a validation error and achievement data will not get imported as some required fields are missing")
def step_impl_3(context):
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data.get("success") is False, "Success not False"
  assert context.res_data.get("message") == "Missing required fields - 'type','name'", "Expected message not returned"
