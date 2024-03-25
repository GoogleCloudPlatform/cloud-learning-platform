"""
Ingest data from non-API Sources, break out skills and organize them in skill graph
"""

import time
import behave
import json
import os
import csv
from environment import (TEST_CSV_SKILLS_PATH, TEST_CSV_COMPETENCIES_PATH,
  TEST_CSV_CATEGORIES_PATH, TEST_CSV_SUBDOMAINS_PATH, TEST_CSV_DOMAINS_PATH)
from setup import post_method, get_method, put_method, delete_method
from common.utils.gcs_adapter import is_valid_path
from fastapi.responses import JSONResponse
from test_config import API_URL_SKILL_SERVICE, TESTING_OBJECTS_PATH

API_URL = API_URL_SKILL_SERVICE



SAMPLE_CSV_FILE_PATH = os.path.join("testing_objects", "sample_csv_file.csv")

# ------------------------------Scenario 1-----------------------------------

@behave.given("We have access to raw data in csv format available on a gcs bucket")
def step_impl_1(context):
  context.url = f"{API_URL}"

  assert is_valid_path(context.skill_uri), "Skill csv uri is invalid"
  assert is_valid_path(context.competency_uri), "Competency csv uri is invalid"
  assert is_valid_path(context.category_uri), "Category csv uri is invalid"
  assert is_valid_path(context.sub_domain_uri), "Sub domain csv uri is invalid"
  assert is_valid_path(context.domain_uri), "Domain csv uri is invalid"


@behave.when("Skill service accesses this gcs csv data with correct payload request")
def step_impl_2(context):

  data = {
          "skill_uri": context.skill_uri,
          "competency_uri": context.competency_uri,
          "domain_uri": context.domain_uri,
          "sub_domain_uri": context.sub_domain_uri,
          "category_uri": context.category_uri
        }
  context.res = post_method(url = f"{context.url}/import/csv",
      query_params={"source":"osn"}, data=data)
  context.res_data = context.res.json()


@behave.then("That gcs csv data should be ingested into skill service")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["status"] == "active"
  job_name = context.res_data["data"]["job_name"]
  url = f"{context.url}/jobs/generic_csv_ingestion/{job_name}"
  for i in range(60):
    res = get_method(url=url)
    data = res.json()
    if data["data"]["status"] in ["succeeded", "failed"]:
      break
    time.sleep(10)
  assert data["data"]["status"] == "succeeded", "Job not succeeded"

  skill_blob = context.gcs_object.get_blob_from_gcs_path(context.skill_uri)
  skill_data = context.gcs_object.parse_gcs_csv_file(skill_blob)

  competency_blob = context.gcs_object.get_blob_from_gcs_path(context.competency_uri)
  competency_data = context.gcs_object.parse_gcs_csv_file(competency_blob)

  category_blob = context.gcs_object.get_blob_from_gcs_path(context.category_uri)
  category_data = context.gcs_object.parse_gcs_csv_file(category_blob)

  sub_domain_blob = context.gcs_object.get_blob_from_gcs_path(context.sub_domain_uri)
  sub_domain_data = context.gcs_object.parse_gcs_csv_file(sub_domain_blob)

  domain_blob = context.gcs_object.get_blob_from_gcs_path(context.domain_uri)
  domain_data = context.gcs_object.parse_gcs_csv_file(domain_blob)

  skill_ref_ids = [i.get("id") for i in skill_data]
  competency_ref_ids = [i.get("id") for i in competency_data]
  category_ref_ids = [i.get("id") for i in category_data]
  sub_domain_ref_ids = [i.get("id") for i in sub_domain_data]
  domain_ref_ids = [i.get("id") for i in domain_data]

  api_url = f"{context.url}/skills"
  params = {"skip": 0, "limit": 100}
  resp = get_method(api_url, query_params=params)
  resp_data = resp.json()
  assert resp.status_code == 200, "Status 200"
  skill_ids = [i.get("reference_id") for i in resp_data.get("data")]
  assert set(skill_ids).intersection(set(skill_ref_ids)) \
    == set(skill_ref_ids), "all data not retrieved for skill"

  api_url = f"{context.url}/competencies"
  params = {"skip": 0, "limit": 1500}
  resp = get_method(api_url, query_params=params)
  resp_data = resp.json()
  assert resp.status_code == 200, "Status 200"
  competency_ids = [i.get("reference_id") for i in resp_data.get("data")]
  assert set(competency_ids).intersection(set(competency_ref_ids)) \
    == set(competency_ref_ids), "all data not retrieved for competency"

  api_url = f"{context.url}/categories"
  params = {"skip": 0, "limit": 100}
  resp = get_method(api_url, query_params=params)
  resp_data = resp.json()
  assert resp.status_code == 200, "Status 200"
  category_ids = [i.get("reference_id") for i in resp_data.get("data")]
  assert set(category_ids).intersection(set(category_ref_ids)) \
    == set(category_ref_ids), "all data not retrieved for category"

  api_url = f"{context.url}/sub-domains"
  params = {"skip": 0, "limit": 100}
  resp = get_method(api_url, query_params=params)
  resp_data = resp.json()
  assert resp.status_code == 200, "Status 200"
  sub_domain_ids = [i.get("reference_id") for i in resp_data.get("data")]
  assert set(sub_domain_ids).intersection(set(sub_domain_ref_ids)) \
    == set(sub_domain_ref_ids), "all data not retrieved for sub_domain"

  api_url = f"{context.url}/domains"
  params = {"skip": 0, "limit": 100}
  resp = get_method(api_url, query_params=params)
  resp_data = resp.json()
  assert resp.status_code == 200, "Status 200"
  domain_ids = [i.get("reference_id") for i in resp_data.get("data")]
  assert set(domain_ids).intersection(set(domain_ref_ids)) \
    == set(domain_ref_ids), "all data not retrieved for domain"


# ------------------------------Scenario 2-----------------------------------

@behave.given("We have access to raw data of csv type available on a gcs bucket")
def step_impl_1(context):
  context.url = f"{API_URL}"

  context.skill_uri = "gs://aitutor-dev/dev_testing/testing-files/generic_skill_false.csv"
  context.competency_uri = "gs://aitutor-dev/dev_testing/testing-files/generic_competency_false.csv"
  context.category_uri = "gs://aitutor-dev/dev_testing/testing-files/generic_category_false.csv"
  context.sub_domain_uri = "gs://aitutor-dev/dev_testing/testing-files/generic_sub_domain_false.csv"
  context.domain_uri = "gs://aitutor-dev/dev_testing/testing-files/generic_domain_false.csv"

  skill_uri_valid = is_valid_path(context.skill_uri)
  competency_uri_valid = is_valid_path(context.competency_uri)
  category_uri_valid = is_valid_path(context.category_uri)
  sub_domain_uri_valid = is_valid_path(context.sub_domain_uri)
  domain_uri_valid = is_valid_path(context.domain_uri)

  if not (skill_uri_valid and competency_uri_valid and category_uri_valid and sub_domain_uri_valid and domain_uri_valid):
    uri_valid = False
  else:
    uri_valid = True

  assert not uri_valid, "csv uri is valid"


@behave.when("Skill service accesses this gcs csv data with incorrect payload request")
def step_impl_2(context):

  data = {
          "skill_uri": context.skill_uri,
          "competency_uri": context.competency_uri,
          "domain_uri": context.domain_uri,
          "sub_domain_uri": context.sub_domain_uri,
          "category_uri": context.category_uri
        }
  context.res = post_method(url = f"{context.url}/import/csv",
      query_params={"source":"osn"}, data=data)
  context.res_data = context.res.json()


@behave.then("Gcs csv ingestion into skill service should fail")
def step_impl_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data["data"] is None


# ------------------------------Scenario 3-----------------------------------

@behave.given("We have access to raw data (csv file) available on a gcs bucket")
def step_impl_1(context):
  context.url = f"{API_URL}"
  context.query_params = {"source": "osn"}

@behave.when("Skill service accesses this gcs csv data with incorrect payload request (without a file or GCS URI)")
def step_impl_2(context):
  context.res = post_method(url = f"{context.url}/import/csv",
                                    query_params=context.query_params)
  context.res_data = context.res.json()

@behave.then("Gcs csv ingestion into skill service should fail due to incorrect payload request (without a file or GCS URI)")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False
  assert context.res_data.get("message") == "Please either upload a CSV file or provide a GCS CSV file URI but not both", \
    "Unexpected response message"


# ------------------------------Scenario 4-----------------------------------

@behave.given("We have access to a csv file available on a gcs bucket")
def step_impl_1(context):
  context.url = f"{API_URL}"
  assert is_valid_path(context.skill_uri), "Skill csv uri is invalid"


@behave.when("Skill service accesses this gcs csv data with incorrect payload request (with both file & GCS URI)")
def step_impl_2(context):
  skill_csv_file_path = os.path.join("testing_objects", "invalid_generic_skill.csv")

  with open(skill_csv_file_path, encoding="UTF-8") as skills_file:
    context.res = post_method(
        url=f"{context.url}/import/csv",
        query_params={"source": "osn"},
        files={"skills": skills_file},
        data={"skill_uri": context.skill_uri})
    context.res_data = context.res.json()

@behave.then("Gcs csv ingestion into skill service should fail due to incorrect payload request (with both file & GCS URI)")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False
  assert context.res_data.get("message") == "Please either upload a CSV file or provide a GCS CSV file URI but not both", \
    "Unexpected response message"

# ------------------------------Scenario 5-----------------------------------

@behave.given("We have access to raw data for skill in a csv file with missing fields available on a gcs bucket")
def step_impl_1(context):
  context.url = f"{API_URL}"
  assert is_valid_path(context.invalid_skill_uri), "Skill csv uri is invalid"

@behave.when("Skill service accesses this csv file with skill data from gcs with missing fields")
def step_impl_2(context):
  data = {
          "skill_uri": context.invalid_skill_uri
        }
  context.res = post_method(url = f"{context.url}/import/csv",
      query_params={"source":"osn"}, data=data)
  context.res_data = context.res.json()

@behave.then("Gcs csv ingestion into skill service should fail as csv skill data has missing fields")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False
  assert context.res_data.get("message") == "Required column \"description\" is missing in skills csv", \
    "Unexpected response message"


# ------------------------------Scenario 6-----------------------------------
@behave.given("We have access to raw data for competency in a csv file with missing fields available on a gcs bucket")
def step_impl_1(context):
  context.url = f"{API_URL}"
  assert is_valid_path(context.invalid_competency_uri), "competency csv uri is invalid"

@behave.when("Skill service accesses this csv file with competency data from gcs with missing fields")
def step_impl_2(context):
  data = {
          "competency_uri": context.invalid_competency_uri
        }
  context.res = post_method(url = f"{context.url}/import/csv",
      query_params={"source":"osn"}, data=data)
  context.res_data = context.res.json()

@behave.then("Gcs csv ingestion into skill service should fail as csv competency data has missing fields")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False
  assert context.res_data.get("message") == "Required column \"description\" is missing in competencies csv", \
    "Unexpected response message"


# ------------------------------Scenario 7-----------------------------------
@behave.given("We have access to raw data for category in a csv file with missing fields available on a gcs bucket")
def step_impl_1(context):
  context.url = f"{API_URL}"
  assert is_valid_path(context.invalid_category_uri), "category csv uri is invalid"

@behave.when("Skill service accesses this csv file with category data from gcs with missing fields")
def step_impl_2(context):
  data = {
          "category_uri": context.invalid_category_uri
        }
  context.res = post_method(url = f"{context.url}/import/csv",
      query_params={"source":"osn"}, data=data)
  context.res_data = context.res.json()

@behave.then("Gcs csv ingestion into skill service should fail as csv category data has missing fields")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False
  assert context.res_data.get("message") == "Required column \"id\" is missing in categories csv", \
    "Unexpected response message"


# ------------------------------Scenario 8-----------------------------------
@behave.given("We have access to raw data for sub-domain in a csv file with missing fields available on a gcs bucket")
def step_impl_1(context):
  context.url = f"{API_URL}"
  assert is_valid_path(context.invalid_sub_domain_uri), "sub-domain csv uri is invalid"

@behave.when("Skill service accesses this csv file with sub-domain data from gcs with missing fields")
def step_impl_2(context):
  data = {
          "sub_domain_uri": context.invalid_sub_domain_uri
        }
  context.res = post_method(url = f"{context.url}/import/csv",
      query_params={"source":"osn"}, data=data)
  context.res_data = context.res.json()

@behave.then("Gcs csv ingestion into skill service should fail as csv sub-domain data has missing fields")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False
  assert context.res_data.get("message") == "Required column \"id\" is missing in sub_domains csv", \
    "Unexpected response message"


# ------------------------------Scenario 9-----------------------------------
@behave.given("We have access to raw data for domain in a csv file with missing fields available on a gcs bucket")
def step_impl_1(context):
  context.url = f"{API_URL}"
  assert is_valid_path(context.invalid_domain_uri), "domain csv uri is invalid"

@behave.when("Skill service accesses this csv file with domain data from gcs with missing fields")
def step_impl_2(context):
  data = {
          "domain_uri": context.invalid_domain_uri
        }
  context.res = post_method(url = f"{context.url}/import/csv",
      query_params={"source":"osn"}, data=data)
  context.res_data = context.res.json()

@behave.then("Gcs csv ingestion into skill service should fail as csv domain data has missing fields")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False
  assert context.res_data.get("message") == "Required column \"name\" is missing in domains csv", \
    "Unexpected response message"


# ------------------------------Scenario 10-----------------------------------

@behave.given("We have access to raw data in csv format available on our local system")
def step_impl_1(context):
  context.url = f"{API_URL}"

  context.skill_csv_file_path = TEST_CSV_SKILLS_PATH
  context.competency_csv_file_path = TEST_CSV_COMPETENCIES_PATH
  context.category_csv_file_path = TEST_CSV_CATEGORIES_PATH
  context.sub_domain_csv_file_path = TEST_CSV_SUBDOMAINS_PATH
  context.domain_csv_file_path = TEST_CSV_DOMAINS_PATH

  assert os.path.exists(context.skill_csv_file_path)
  assert os.path.exists(context.competency_csv_file_path)
  assert os.path.exists(context.category_csv_file_path)
  assert os.path.exists(context.sub_domain_csv_file_path)
  assert os.path.exists(context.domain_csv_file_path)


@behave.when("Skill service accesses this local csv data with correct payload request")
def step_impl_2(context):

  with open(context.skill_csv_file_path, encoding="UTF-8") as skills_file:
    with open(context.competency_csv_file_path, encoding="UTF-8") as competencies_file:
      with open(context.category_csv_file_path, encoding="UTF-8") as categories_file:
        with open(
            context.sub_domain_csv_file_path, encoding="UTF-8") as sub_domains_file:
          with open(context.domain_csv_file_path, encoding="UTF-8") as domains_file:
            context.res = post_method(
                url = f"{context.url}/import/csv",
                query_params={"source": "osn"},
                files={
                    "skills": skills_file,
                    "competencies": competencies_file,
                    "categories": categories_file,
                    "sub_domains": sub_domains_file,
                    "domains": domains_file
                })
            context.res_data = context.res.json()

@behave.then("That local csv data should be ingested into skill service")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["status"] == "active"
  job_name = context.res_data["data"]["job_name"]
  url = f"{context.url}/jobs/generic_csv_ingestion/{job_name}"
  for i in range(60):
    res = get_method(url=url)
    data = res.json()
    if data["data"]["status"] in ["succeeded", "failed"]:
      break
    time.sleep(10)
  assert data["data"]["status"] == "succeeded", "Job not succeeded"

  skill_data = list(
      csv.DictReader(
          open(context.skill_csv_file_path, encoding="utf-8"), delimiter=","))
  competency_data = list(
      csv.DictReader(
          open(context.competency_csv_file_path, encoding="utf-8"), delimiter=","))
  category_data = list(
      csv.DictReader(
          open(context.category_csv_file_path, encoding="utf-8"), delimiter=","))
  sub_domain_data = list(
      csv.DictReader(
          open(context.sub_domain_csv_file_path, encoding="utf-8"), delimiter=","))
  domain_data = list(
      csv.DictReader(
          open(context.domain_csv_file_path, encoding="utf-8"), delimiter=","))

  skill_ref_ids = [i.get("id") for i in skill_data]
  competency_ref_ids = [i.get("id") for i in competency_data]
  category_ref_ids = [i.get("id") for i in category_data]
  sub_domain_ref_ids = [i.get("id") for i in sub_domain_data]
  domain_ref_ids = [i.get("id") for i in domain_data]

  api_url = f"{context.url}/skills"
  params = {"skip": 0, "limit": 100}
  resp = get_method(api_url, query_params=params)
  resp_data = resp.json()
  assert resp.status_code == 200, "Status 200"
  skill_ids = [i.get("reference_id") for i in resp_data.get("data")]
  assert set(skill_ids).intersection(set(skill_ref_ids)) \
    == set(skill_ref_ids), "all data not retrieved for skill"

  api_url = f"{context.url}/competencies"
  params = {"skip": 0, "limit": 1500}
  resp = get_method(api_url, query_params=params)
  resp_data = resp.json()
  assert resp.status_code == 200, "Status 200"
  competency_ids = [i.get("reference_id") for i in resp_data.get("data")]
  assert set(competency_ids).intersection(set(competency_ref_ids)) \
    == set(competency_ref_ids), "all data not retrieved for competency"

  api_url = f"{context.url}/categories"
  params = {"skip": 0, "limit": 100}
  resp = get_method(api_url, query_params=params)
  resp_data = resp.json()
  assert resp.status_code == 200, "Status 200"
  category_ids = [i.get("reference_id") for i in resp_data.get("data")]
  assert set(category_ids).intersection(set(category_ref_ids)) \
    == set(category_ref_ids), "all data not retrieved for category"

  api_url = f"{context.url}/sub-domains"
  params = {"skip": 0, "limit": 100}
  resp = get_method(api_url, query_params=params)
  resp_data = resp.json()
  assert resp.status_code == 200, "Status 200"
  sub_domain_ids = [i.get("reference_id") for i in resp_data.get("data")]
  assert set(sub_domain_ids).intersection(set(sub_domain_ref_ids)) \
    == set(sub_domain_ref_ids), "all data not retrieved for sub_domain"

  api_url = f"{context.url}/domains"
  params = {"skip": 0, "limit": 100}
  resp = get_method(api_url, query_params=params)
  resp_data = resp.json()
  assert resp.status_code == 200, "Status 200"
  domain_ids = [i.get("reference_id") for i in resp_data.get("data")]
  assert set(domain_ids).intersection(set(domain_ref_ids)) \
    == set(domain_ref_ids), "all data not retrieved for domain"


# ------------------------------Scenario 11-----------------------------------

@behave.given("We have access to raw data (non-csv format) available on our local system")
def step_impl_1(context):
  context.url = f"{API_URL}"
  context.domain_file_path = os.path.join("testing_objects", "domains.json")
  assert os.path.exists(context.domain_file_path)

@behave.when("Skill service accesses this local csv data with invalid/wrong extension")
def step_impl_2(context):
  with open(context.domain_file_path, encoding="UTF-8") as domain_file:
    context.res = post_method(f"{context.url}/import/csv",
                      query_params={"source": "osn"},
                      files={"domains": domain_file})
    context.res_data = context.res.json()

@behave.then("local csv ingestion into skill service should fail due to csv data with invalid/wrong extension")
def step_impl_3(context):
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data.get("message") == "Invalid file type. CSV file expected", \
    "Unexpected response message"

# ------------------------------Scenario 12-----------------------------------

@behave.given("We have access to raw skill data in csv format available on our local system")
def step_impl_1(context):
  context.url = f"{API_URL}"
  context.skill_csv_file_path = os.path.join("testing_objects", "invalid_generic_skill.csv")
  assert os.path.exists(context.skill_csv_file_path)

@behave.when("Skill service accesses this local csv skill data with missing fields")
def step_impl_2(context):
  with open(context.skill_csv_file_path, encoding="UTF-8") as skills_file:
    context.res = post_method(
        url=f"{context.url}/import/csv",
        query_params={"source": "osn"},
        files={"skills": skills_file})
    context.res_data = context.res.json()

@behave.then("local csv ingestion into skill service should fail due to skill data missing some fields")
def step_impl_3(context):
  assert context.res.status_code == 422, "Status not 422"
  assert context.res_data.get("message") == "Required column \"description\" is missing in skills csv", \
    "Unexpected response message"

# ------------------------------Scenario 13-----------------------------------

@behave.given("We have access to raw competency data in csv format available on our local system")
def step_impl_1(context):
  context.url = f"{API_URL}"
  context.csv_file_path = os.path.join("testing_objects", "invalid_generic_competency.csv")
  assert os.path.exists(context.csv_file_path)

@behave.when("Skill service accesses this local csv competency data with missing fields")
def step_impl_2(context):
  with open(context.csv_file_path, encoding="UTF-8") as competency_file:
    context.res = post_method(
        url=f"{context.url}/import/csv",
        query_params={"source": "osn"},
        files={"competencies": competency_file})
    context.res_data = context.res.json()

@behave.then("local csv ingestion into skill service should fail due to competency data missing some fields")
def step_impl_3(context):
  assert context.res.status_code == 422, "Status not 422"
  assert context.res_data.get("message") == "Required column \"description\" is missing in competencies csv", \
    "Unexpected response message"

# ------------------------------Scenario 14-----------------------------------

@behave.given("We have access to raw category data in csv format available on our local system")
def step_impl_1(context):
  context.url = f"{API_URL}"
  context.csv_file_path = os.path.join("testing_objects", "invalid_generic_category.csv")
  assert os.path.exists(context.csv_file_path)

@behave.when("Skill service accesses this local csv category data with missing fields")
def step_impl_2(context):
  with open(context.csv_file_path, encoding="UTF-8") as category_file:
    context.res = post_method(
        url=f"{context.url}/import/csv",
        query_params={"source": "osn"},
        files={"categories": category_file})
    context.res_data = context.res.json()

@behave.then("local csv ingestion into skill service should fail due to category data missing some fields")
def step_impl_3(context):
  assert context.res.status_code == 422, "Status not 422"
  assert context.res_data.get("message") == "Required column \"id\" is missing in categories csv", \
    "Unexpected response message"

# # ------------------------------Scenario 15-----------------------------------

@behave.given("We have access to raw sub-domain data in csv format available on our local system")
def step_impl_1(context):
  context.url = f"{API_URL}"
  context.csv_file_path = os.path.join("testing_objects", "invalid_generic_sub_domain.csv")
  assert os.path.exists(context.csv_file_path)

@behave.when("Skill service accesses this local csv sub-domain data with missing fields")
def step_impl_2(context):
  with open(context.csv_file_path, encoding="UTF-8") as sub_domain_file:
    context.res = post_method(
        url=f"{context.url}/import/csv",
        query_params={"source": "osn"},
        files={"sub_domains": sub_domain_file})
    context.res_data = context.res.json()

@behave.then("local csv ingestion into skill service should fail due to sub-domain data missing some fields")
def step_impl_3(context):
  assert context.res.status_code == 422, "Status not 422"
  assert context.res_data.get("message") == "Required column \"id\" is missing in sub_domains csv", \
    "Unexpected response message"

# # ------------------------------Scenario 16-----------------------------------

@behave.given("We have access to raw domain data in csv format available on our local system")
def step_impl_1(context):
  context.url = f"{API_URL}"
  context.csv_file_path = os.path.join("testing_objects", "invalid_generic_domain.csv")
  assert os.path.exists(context.csv_file_path)

@behave.when("Skill service accesses this local csv domain data with missing fields")
def step_impl_2(context):
  with open(context.csv_file_path, encoding="UTF-8") as domain_file:
    context.res = post_method(
        url=f"{context.url}/import/csv",
        query_params={"source": "osn"},
        files={"domains": domain_file})
    context.res_data = context.res.json()

@behave.then("local csv ingestion into skill service should fail due to domain data missing some fields")
def step_impl_3(context):
  assert context.res.status_code == 422, "Status not 422"
  assert context.res_data.get("message") == "Required column \"name\" is missing in domains csv", \
    "Unexpected response message"

# ------------------------------Scenario 17-----------------------------------

@behave.given("We have access to raw data in json format for skill")
def step_impl_1(context):
  context.url = f"{API_URL}"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "skills.json")
  assert os.path.exists(context.json_file_path)

@behave.when("Skill service accesses this skill json data with correct payload request")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as skills_json_file:
    context.res = post_method(f"{context.url}/skill/import/json",
                       files={"json_file": skills_json_file})
    context.res_data = context.res.json()

@behave.then("That skill json data should be ingested into skill service")
def step_impl_3(context):
  assert context.res.status_code == 200, "Status not 200"
  assert isinstance(context.res_data.get("data"), list), "Response is not a list"
  assert len(
      context.res_data.get("data")) > 0, "Empty list returned in import json api"
  inserted_skill_uuids = context.res_data.get("data")
  api_url = f"{context.url}/skills"
  params = {"skip": 0, "limit": 100}

  resp = get_method(api_url, query_params=params)
  resp_data = resp.json()
  assert resp.status_code == 200, "Status 200"
  skill_uuids = [i.get("uuid") for i in resp_data.get("data")]
  assert set(inserted_skill_uuids).intersection(set(skill_uuids)) \
    == set(inserted_skill_uuids), "all data not retrieved"


# ------------------------------Scenario 18-----------------------------------

@behave.given("We have access to raw data of json type with invalid json schema for skill")
def step_impl_1(context):
  context.url = f"{API_URL}"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "skills_invalid.json")
  context.required_fields = "'name','description'"
  assert os.path.exists(context.json_file_path)

@behave.when("Skill service accesses this skill json data with invalid json schema")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as skills_json_file:
    context.res = post_method(f"{context.url}/skill/import/json",
                       files={"json_file": skills_json_file})
    context.res_data = context.res.json()

@behave.then("Ingestion of that skill json data with invalid json schema into skill service should fail")
def step_impl_3(context):
  # JSON file without required fields
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data.get(
      "message") == f"Missing required fields - {context.required_fields}", "Expected response message is not same"


# ------------------------------Scenario 19-----------------------------------

@behave.given("We have access to raw data of csv type for skill")
def step_impl_1(context):
  context.url = f"{API_URL}"
  context.json_file_path = SAMPLE_CSV_FILE_PATH
  context.required_fields = "'name','description'"
  assert os.path.exists(context.json_file_path)

@behave.when("Skill service accesses this skill csv data instead of the JSON")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as skills_json_file:
    context.res = post_method(f"{context.url}/skill/import/json",
                       files={"json_file": skills_json_file})
    context.res_data = context.res.json()

@behave.then("ingestion of that skill data from csv file into skill service should fail")
def step_impl_3(context):
  assert context.res.status_code == 422, "Status is not 422"

# ------------------------------Scenario 20-----------------------------------

@behave.given("We have access to raw data in json format for competency")
def step_impl_1(context):
  context.url = f"{API_URL}"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "competencies.json")
  assert os.path.exists(context.json_file_path)

@behave.when("Skill service accesses this competency json data with correct payload request")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as competencies_json_file:
    context.res = post_method(f"{context.url}/competency/import/json",
                       files={"json_file": competencies_json_file})
    context.res_data = context.res.json()

@behave.then("That competency json data should be ingested into skill service")
def step_impl_3(context):
  assert context.res.status_code == 200, "Status not 200"
  assert isinstance(context.res_data.get("data"), list), "Response is not a list"
  assert len(
      context.res_data.get("data")) > 0, "Empty list returned in import json api"
  inserted_competency_uuids = context.res_data.get("data")
  api_url = f"{context.url}/competencies"
  params = {"skip": 0, "limit": 1500}

  resp = get_method(api_url, query_params=params)
  resp_data = resp.json()
  assert resp.status_code == 200, "Status 200"
  competency_uuids = [i.get("uuid") for i in resp_data.get("data")]
  assert set(inserted_competency_uuids).intersection(set(competency_uuids)) \
    == set(inserted_competency_uuids), "all data not retrieved"

# ------------------------------Scenario 21-----------------------------------

@behave.given("We have access to raw data of json type with invalid json schema for competency")
def step_impl_1(context):
  context.url = f"{API_URL}"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "competencies_invalid.json")
  context.required_fields = "'description'"
  assert os.path.exists(context.json_file_path)

@behave.when("Skill service accesses this competency json data with invalid json schema")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as competencies_json_file:
    context.res = post_method(f"{context.url}/competency/import/json",
                       files={"json_file": competencies_json_file})
    context.res_data = context.res.json()

@behave.then("Ingestion of that competency json data with invalid json schema into skill service should fail")
def step_impl_3(context):
  # JSON file without required fields
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data.get(
      "message") == f"Missing required fields - {context.required_fields}", "Expected response message is not same"


# ------------------------------Scenario 22-----------------------------------

@behave.given("We have access to raw data of csv type for competency")
def step_impl_1(context):
  context.url = f"{API_URL}"
  context.json_file_path = SAMPLE_CSV_FILE_PATH
  context.required_fields = "'name','description'"
  assert os.path.exists(context.json_file_path)

@behave.when("Skill service accesses this competency csv data instead of the JSON")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as competencies_json_file:
    context.res = post_method(f"{context.url}/competency/import/json",
                       files={"json_file": competencies_json_file})
    context.res_data = context.res.json()

@behave.then("ingestion of that competency data from csv file into skill service should fail")
def step_impl_3(context):
  assert context.res.status_code == 422, "Status is not 422"


# ------------------------------Scenario 23-----------------------------------

@behave.given("We have access to raw data in json format for category")
def step_impl_1(context):
  context.url = f"{API_URL}"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "categories.json")
  assert os.path.exists(context.json_file_path)

@behave.when("Skill service accesses this category json data with correct payload request")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as categories_json_file:
    context.res = post_method(f"{context.url}/category/import/json",
                       files={"json_file": categories_json_file})
    context.res_data = context.res.json()

@behave.then("That category json data should be ingested into skill service")
def step_impl_3(context):
  assert context.res.status_code == 200, "Status not 200"
  assert isinstance(context.res_data.get("data"), list), "Response is not a list"
  assert len(
      context.res_data.get("data")) > 0, "Empty list returned in import json api"
  inserted_category_uuids = context.res_data.get("data")
  api_url = f"{context.url}/categories"
  params = {"skip": 0, "limit": 100}

  resp = get_method(api_url, query_params=params)
  resp_data = resp.json()
  assert resp.status_code == 200, "Status 200"
  category_uuids = [i.get("uuid") for i in resp_data.get("data")]
  assert set(inserted_category_uuids).intersection(set(category_uuids)) \
    == set(inserted_category_uuids), "all data not retrieved"

# ------------------------------Scenario 24-----------------------------------

@behave.given("We have access to raw data of json type with invalid json schema for category")
def step_impl_1(context):
  context.url = f"{API_URL}"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "categories_invalid.json")
  context.required_fields = "'name','description'"
  assert os.path.exists(context.json_file_path)

@behave.when("Skill service accesses this category json data with invalid json schema")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as categories_json_file:
    context.res = post_method(f"{context.url}/category/import/json",
                       files={"json_file": categories_json_file})
    context.res_data = context.res.json()

@behave.then("Ingestion of that category json data with invalid json schema into skill service should fail")
def step_impl_3(context):
  # JSON file without required fields
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data.get(
      "message") == f"Missing required fields - {context.required_fields}", "Expected response message is not same"

# ------------------------------Scenario 25-----------------------------------

@behave.given("We have access to raw data of csv type for category")
def step_impl_1(context):
  context.url = f"{API_URL}"
  context.json_file_path = SAMPLE_CSV_FILE_PATH
  context.required_fields = "'name','description'"
  assert os.path.exists(context.json_file_path)

@behave.when("Skill service accesses this category csv data instead of the JSON")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as categories_json_file:
    context.res = post_method(f"{context.url}/category/import/json",
                       files={"json_file": categories_json_file})
    context.res_data = context.res.json()

@behave.then("Ingestion of that category data from csv file into skill service should fail")
def step_impl_3(context):
  assert context.res.status_code == 422, "Status is not 422"



# ------------------------------Scenario 26-----------------------------------

@behave.given("We have access to raw data in json format for sub-domain")
def step_impl_1(context):
  context.url = f"{API_URL}"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "sub_domains.json")
  assert os.path.exists(context.json_file_path)

@behave.when("Skill service accesses this sub-domain json data with correct payload request")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as sub_domain_json_file:
    context.res = post_method(f"{context.url}/sub-domain/import/json",
                       files={"json_file": sub_domain_json_file})
    context.res_data = context.res.json()

@behave.then("That sub-domain json data should be ingested into skill service")
def step_impl_3(context):
  assert context.res.status_code == 200, "Status not 200"
  assert isinstance(context.res_data.get("data"), list), "Response is not a list"
  assert len(
      context.res_data.get("data")) > 0, "Empty list returned in import json api"
  inserted_sub_domain_uuids = context.res_data.get("data")
  api_url = f"{context.url}/sub-domains"
  params = {"skip": 0, "limit": 100}

  resp = get_method(api_url, query_params=params)
  resp_data = resp.json()
  assert resp.status_code == 200, "Status 200"
  sub_domain_uuids = [i.get("uuid") for i in resp_data.get("data")]
  assert set(inserted_sub_domain_uuids).intersection(set(sub_domain_uuids)) \
    == set(inserted_sub_domain_uuids), "all data not retrieved"

  # ------------------------------Scenario 27-----------------------------------

@behave.given("We have access to raw data of json type with invalid json schema for sub-domain")
def step_impl_1(context):
  context.url = f"{API_URL}"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "sub_domains_invalid.json")
  context.required_fields = "'name','description'"
  assert os.path.exists(context.json_file_path)

@behave.when("Skill service accesses this sub-domain json data with invalid json schema")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as sub_domains_json_file:
    context.res = post_method(f"{context.url}/sub-domain/import/json",
                       files={"json_file": sub_domains_json_file})
    context.res_data = context.res.json()

@behave.then("Ingestion of that sub-domain json data with invalid json schema into skill service should fail")
def step_impl_3(context):
  # JSON file without required fields
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data.get(
      "message") == f"Missing required fields - {context.required_fields}", "Expected response message is not same"

# ------------------------------Scenario 28-----------------------------------

@behave.given("We have access to raw data of csv type for sub-domain")
def step_impl_1(context):
  context.url = f"{API_URL}"
  context.json_file_path = SAMPLE_CSV_FILE_PATH
  context.required_fields = "'name','description'"
  assert os.path.exists(context.json_file_path)

@behave.when("Skill service accesses this sub-domain csv data instead of the JSON")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as sub_domains_json_file:
    context.res = post_method(f"{context.url}/sub-domain/import/json",
                       files={"json_file": sub_domains_json_file})
    context.res_data = context.res.json()

@behave.then("Ingestion of that sub-domain data from csv file into skill service should fail")
def step_impl_3(context):
  assert context.res.status_code == 422, "Status is not 422"


# ------------------------------Scenario 29-----------------------------------

@behave.given("We have access to raw data in json format for domain")
def step_impl_1(context):
  context.url = f"{API_URL}"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "domains.json")
  assert os.path.exists(context.json_file_path)

@behave.when("Skill service accesses this domain json data with correct payload request")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as domains_json_file:
    context.res = post_method(f"{context.url}/domain/import/json",
                       files={"json_file": domains_json_file})
    context.res_data = context.res.json()

@behave.then("That domain json data should be ingested into skill service")
def step_impl_3(context):
  assert context.res.status_code == 200, "Status not 200"
  assert isinstance(context.res_data.get("data"), list), "Response is not a list"
  assert len(
      context.res_data.get("data")) > 0, "Empty list returned in import json api"
  inserted_domain_uuids = context.res_data.get("data")
  api_url = f"{context.url}/domains"
  params = {"skip": 0, "limit": 100}

  resp = get_method(api_url, query_params=params)
  resp_data = resp.json()
  assert resp.status_code == 200, "Status 200"
  domain_uuids = [i.get("uuid") for i in resp_data.get("data")]
  assert set(inserted_domain_uuids).intersection(set(domain_uuids)) \
    == set(inserted_domain_uuids), "all data not retrieved"

# ------------------------------Scenario 30-----------------------------------

@behave.given("We have access to raw data of json type with invalid json schema for domain")
def step_impl_1(context):
  context.url = f"{API_URL}"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH, "domains_invalid.json")
  context.required_fields = "'name','description'"
  assert os.path.exists(context.json_file_path)

@behave.when("Skill service accesses this domain json data with invalid json schema")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as domains_json_file:
    context.res = post_method(f"{context.url}/domain/import/json",
                       files={"json_file": domains_json_file})
    context.res_data = context.res.json()

@behave.then("Ingestion of that domain json data with invalid json schema into skill service should fail")
def step_impl_3(context):
  # JSON file without required fields
  assert context.res.status_code == 422, "Status is not 422"
  assert context.res_data.get(
      "message") == f"Missing required fields - {context.required_fields}", "Expected response message is not same"

# ------------------------------Scenario 31-----------------------------------

@behave.given("We have access to raw data of csv type for domain")
def step_impl_1(context):
  context.url = f"{API_URL}"
  context.json_file_path = SAMPLE_CSV_FILE_PATH
  context.required_fields = "'name','description'"
  assert os.path.exists(context.json_file_path)

@behave.when("Skill service accesses this domain csv data instead of the JSON")
def step_impl_2(context):
  with open(context.json_file_path, encoding="UTF-8") as domains_json_file:
    context.res = post_method(f"{context.url}/domain/import/json",
                       files={"json_file": domains_json_file})
    context.res_data = context.res.json()

@behave.then("Ingestion of that domain data from csv file into skill service should fail")
def step_impl_3(context):
  assert context.res.status_code == 422, "Status is not 422"
