"""
Feature 09 - Ingest/Import knowledge data from json files
"""

import time
import behave
import json
import os
import csv
from environment import (TEST_CSV_SKILLS_PATH, TEST_CSV_COMPETENCIES_PATH,
  TEST_CSV_CATEGORIES_PATH, TEST_CSV_SUBDOMAINS_PATH, TEST_CSV_DOMAINS_PATH)
from setup import post_method, get_method, put_method, delete_method
from fastapi.responses import JSONResponse
from test_config import API_URL_KNOWLEDGE_SERVICE, TESTING_OBJECTS_PATH


SAMPLE_CSV_FILE_PATH = os.path.join("testing_objects", "sample_csv_file.csv")



# ------------------------------Scenario 1-----------------------------------

@behave.given("We have access to raw data in json format for Learning Resource")
def step_impl_1(context):
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "learning_resource.json")
  assert os.path.exists(context.json_file_path)


@behave.when("Skill service accesses this Learning Resource json data with correct payload request")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as lr_json_file:
    context.res = post_method(f"{context.url}/learning-resource/import/json",
                       files={"json_file": lr_json_file})
    context.res_data = context.res.json()


@behave.then("That Learning Resource json data should be ingested into skill service")
def step_impl_3(context):
  assert context.res.status_code == 200, "Status not 200"
  assert isinstance(context.res_data.get("data"), list), "Response is not a list"
  assert len(
      context.res_data.get("data")) > 0, "Empty list returned in import json api"
  inserted_lr_uuids = context.res_data.get("data")
  api_url = f"{context.url}/learning-resources"
  params = {"skip": 0, "limit": 100}

  resp = get_method(api_url, query_params=params)
  resp_data = resp.json()
  assert resp.status_code == 200, "Status 200"
  lr_uuids = [i.get("uuid") for i in resp_data.get("data")]
  assert set(inserted_lr_uuids).intersection(set(lr_uuids)) \
    == set(inserted_lr_uuids), "all data not retrieved"


# ------------------------------Scenario 2-----------------------------------

@behave.given("We have access to raw data of csv type for Learning Resource")
def step_impl_1(context):
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}"
  context.json_file_path = SAMPLE_CSV_FILE_PATH
  context.required_fields = "'name','description'"
  assert os.path.exists(context.json_file_path)


@behave.when("Skill service accesses this Learning Resource csv data instead of the JSON")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as lr_csv_file:
    context.res = post_method(f"{context.url}/learning-resource/import/json",
                       files={"json_file": lr_csv_file})
    context.res_data = context.res.json()


@behave.then("Ingestion of that Learning Resource data from csv file into skill service should fail")
def step_impl_3(context):
  assert context.res.status_code == 500, "Status is not 500"
  assert context.res_data.get("success") is False, "Success not False"


# ------------------------------Scenario 3-----------------------------------

@behave.given("We have access to raw data in json format for concept")
def step_impl_1(context):
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "concept.json")
  assert os.path.exists(context.json_file_path)


@behave.when("Skill service accesses this concept json data with correct payload request")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as concept_json_file:
    context.res = post_method(f"{context.url}/concept/import/json",
                       files={"json_file": concept_json_file})
    context.res_data = context.res.json()


@behave.then("That concept json data should be ingested into skill service")
def step_impl_3(context):
  assert context.res.status_code == 200, "Status not 200"
  assert isinstance(context.res_data.get("data"), list), "Response is not a list"
  assert len(
      context.res_data.get("data")) > 0, "Empty list returned in import json api"
  inserted_concept_uuids = context.res_data.get("data")
  api_url = f"{context.url}/concepts"
  params = {"skip": 0, "limit": 100}

  resp = get_method(api_url, query_params=params)
  resp_data = resp.json()
  assert resp.status_code == 200, "Status 200"
  concept_uuids = [i.get("uuid") for i in resp_data.get("data")]
  assert set(inserted_concept_uuids).intersection(set(concept_uuids)) \
    == set(inserted_concept_uuids), "all data not retrieved"


# ------------------------------Scenario 4-----------------------------------

@behave.given("We have access to raw data of csv type for concept")
def step_impl_1(context):
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}"
  context.json_file_path = SAMPLE_CSV_FILE_PATH
  context.required_fields = "'name','description'"
  assert os.path.exists(context.json_file_path)


@behave.when("Skill service accesses this concept csv data instead of the JSON")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as concept_csv_file:
    context.res = post_method(f"{context.url}/concept/import/json",
                       files={"json_file": concept_csv_file})
    context.res_data = context.res.json()


@behave.then("Ingestion of that concept data from csv file into skill service should fail")
def step_impl_3(context):
  assert context.res.status_code == 500, "Status is not 500"
  assert context.res_data.get("success") is False, "Success not False"

# ------------------------------Scenario 5-----------------------------------

@behave.given("We have access to raw data in json format for sub-concept")
def step_impl_1(context):
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "subconcept.json")
  assert os.path.exists(context.json_file_path)


@behave.when("Skill service accesses this sub-concept json data with correct payload request")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as sc_json_file:
    context.res = post_method(f"{context.url}/subconcept/import/json",
                       files={"json_file": sc_json_file})
    context.res_data = context.res.json()


@behave.then("That sub-concept json data should be ingested into skill service")
def step_impl_3(context):
  assert context.res.status_code == 200, "Status not 200"
  assert isinstance(context.res_data.get("data"), list), "Response is not a list"
  assert len(
      context.res_data.get("data")) > 0, "Empty list returned in import json api"
  inserted_sc_uuids = context.res_data.get("data")
  api_url = f"{context.url}/subconcepts"
  params = {"skip": 0, "limit": 100}

  resp = get_method(api_url, query_params=params)
  resp_data = resp.json()
  assert resp.status_code == 200, "Status 200"
  sc_uuids = [i.get("uuid") for i in resp_data.get("data")]
  assert set(inserted_sc_uuids).intersection(set(sc_uuids)) \
    == set(inserted_sc_uuids), "all data not retrieved"


# ------------------------------Scenario 6-----------------------------------

@behave.given("We have access to raw data of csv type for sub-concept")
def step_impl_1(context):
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}"
  context.json_file_path = SAMPLE_CSV_FILE_PATH
  context.required_fields = "'name','description'"
  assert os.path.exists(context.json_file_path)


@behave.when("Skill service accesses this sub-concept csv data instead of the JSON")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as sc_csv_file:
    context.res = post_method(f"{context.url}/subconcept/import/json",
                       files={"json_file": sc_csv_file})
    context.res_data = context.res.json()


@behave.then("Ingestion of that sub-concept data from csv file into skill service should fail")
def step_impl_3(context):
  assert context.res.status_code == 500, "Status is not 500"
  assert context.res_data.get("success") is False, "Success not False"

# ------------------------------Scenario 7-----------------------------------

@behave.given("We have access to raw data in json format for learning objective")
def step_impl_1(context):
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "learning_objective.json")
  assert os.path.exists(context.json_file_path)


@behave.when("Skill service accesses this learning objective json data with correct payload request")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as lo_json_file:
    context.res = post_method(f"{context.url}/learning-objective/import/json",
                       files={"json_file": lo_json_file})
    context.res_data = context.res.json()


@behave.then("That learning objective json data should be ingested into skill service")
def step_impl_3(context):
  assert context.res.status_code == 200, "Status not 200"
  assert isinstance(context.res_data.get("data"), list), "Response is not a list"
  assert len(
      context.res_data.get("data")) > 0, "Empty list returned in import json api"
  inserted_lo_uuids = context.res_data.get("data")
  api_url = f"{context.url}/learning-objectives"
  params = {"skip": 0, "limit": 100}

  resp = get_method(api_url, query_params=params)
  resp_data = resp.json()
  assert resp.status_code == 200, "Status 200"
  lo_uuids = [i.get("uuid") for i in resp_data.get("data")]
  assert set(inserted_lo_uuids).intersection(set(lo_uuids)) \
    == set(inserted_lo_uuids), "all data not retrieved"


# ------------------------------Scenario 8-----------------------------------

@behave.given("We have access to raw data of csv type for learning objective")
def step_impl_1(context):
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}"
  context.json_file_path = SAMPLE_CSV_FILE_PATH
  context.required_fields = "'name','description'"
  assert os.path.exists(context.json_file_path)


@behave.when("Skill service accesses this learning objective csv data instead of the JSON")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as lo_csv_file:
    context.res = post_method(f"{context.url}/learning-objective/import/json",
                       files={"json_file": lo_csv_file})
    context.res_data = context.res.json()


@behave.then("Ingestion of that learning objective data from csv file into skill service should fail")
def step_impl_3(context):
  assert context.res.status_code == 500, "Status is not 500"
  assert context.res_data.get("success") is False, "Success not False"


# ------------------------------Scenario 9-----------------------------------

@behave.given("We have access to raw data in json format for learning unit")
def step_impl_1(context):
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "learning_unit.json")
  assert os.path.exists(context.json_file_path)


@behave.when("Skill service accesses this learning unit json data with correct payload request")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as lu_json_file:
    context.res = post_method(f"{context.url}/learning-unit/import/json",
                       files={"json_file": lu_json_file})
    context.res_data = context.res.json()


@behave.then("That learning unit json data should be ingested into skill service")
def step_impl_3(context):
  assert context.res.status_code == 200, "Status not 200"
  assert isinstance(context.res_data.get("data"), list), "Response is not a list"
  assert len(
      context.res_data.get("data")) > 0, "Empty list returned in import json api"
  inserted_lu_uuids = context.res_data.get("data")
  api_url = f"{context.url}/learning-units"
  params = {"skip": 0, "limit": 100}

  resp = get_method(api_url, query_params=params)
  resp_data = resp.json()
  assert resp.status_code == 200, "Status 200"
  lu_uuids = [i.get("uuid") for i in resp_data.get("data")]
  assert set(inserted_lu_uuids).intersection(set(lu_uuids)) \
    == set(inserted_lu_uuids), "all data not retrieved"


# ------------------------------Scenario 10-----------------------------------

@behave.given("We have access to raw data of csv type for learning unit")
def step_impl_1(context):
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}"
  context.json_file_path = SAMPLE_CSV_FILE_PATH
  context.required_fields = "'name','description'"
  assert os.path.exists(context.json_file_path)


@behave.when("Skill service accesses this learning unit csv data instead of the JSON")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as lu_csv_file:
    context.res = post_method(f"{context.url}/learning-unit/import/json",
                       files={"json_file": lu_csv_file})
    context.res_data = context.res.json()


@behave.then("Ingestion of that learning unit data from csv file into skill service should fail")
def step_impl_3(context):
  assert context.res.status_code == 500, "Status is not 500"
  assert context.res_data.get("success") is False, "Success not False"
