"""
Ingest skill graph from Credential Engine via API, break out skills and organize them in skill graph
"""

import time
import behave
from setup import post_method, get_method
from test_config import API_URL_KNOWLEDGE_SERVICE
from common.utils.gcs_adapter import is_valid_path

API_URL = API_URL_KNOWLEDGE_SERVICE

#------------------------------ Scenario 1 ---------------------------------#

@behave.given("Textbooks can be accessed in a digital format")
def step_1_1(context):
  context.req_body = {
      "title": "Behave E2E learning Resource ingestion",
      "resource_path": "gs://aitutor-dev/course-resources/Bio 101/Introduction to Biology/The Process of Science/chapter 1.2.pdf",
      "format": "pdf",
      "start_page": 2,
      "end_page": 5,
      "created_by": "Behave E2E User",
      "last_modified_by": "Behave E2E User",
      "description": "Behave Test Content File",
      "create_learning_units": True
  }
  context.url = f"{API_URL}/learning-resource/ingest"


@behave.when("A textbook is uploaded into the knowledge graph in pdf format with correct payload request")
def step_1_2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()
  print(context.res_data)


@behave.then("That data should be ingested into the knowledge graph")
def step_1_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, f'Failed to start job: {context.res_data["message"]}'
  assert context.res_data["data"]["status"] == "active"
  job_name = context.res_data["data"]["job_name"]
  url = f"{API_URL}/jobs/learning_resource_ingestion/{job_name}"
  for _ in range(80):
    res = get_method(url=url)
    data = res.json()
    if data["data"]["status"] in ["succeeded", "failed"]:
      break
    time.sleep(20)
  assert data["data"]["status"] == "succeeded"

  # check inserted data
  item_id = data["data"]["generated_item_id"]
  print(item_id)
  url = f"{API_URL}/learning-resource/{item_id}"
  res = get_method(url=url)
  data = res.json()
  print(data)
  assert data["success"] is True


#------------------------------ Scenario 2 ---------------------------------#

@behave.given("Textbooks is accessible in a digital format")
def step_2_1(context):
  context.req_body = {
      "title": "E2E learning Resource ingestion",
      "resource_path": "gs://aitutor-dev/course-resources/Bio 101/Introduction to Biology/The Process of Science/chapter 1.2.pdf",
      "format": "e2e",  # unsupported format: test
      "start_page": 2,
      "end_page": 5,
      "created_by": "E2E User",
      "last_modified_by": "E2E User",
      "description": "Test Content File",
      "create_learning_units": True
  }
  context.url = f"{API_URL}/learning-resource/ingest"


@behave.when("A textbook is uploaded into the knowledge graph in pdf format with incorrect format value")
def step_2_2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("The data ingestion into the knowledge graph should fail with unsupported format")
def step_2_3(context):
  assert context.res.status_code == 422

#------------------------------ Scenario 3 ---------------------------------#

@behave.given("Textbooks can be accessed in a pdf format")
def step_3_1(context):
  context.resource_path = "gs://aitutor-dev/course-resources/test.pdf" # invalid gcs path
  context.req_body = {
      "title": "E2E learning Resource ingestion",
      "resource_path": context.resource_path,  # invalid gcs path
      "format": "pdf",
      "start_page": 2,
      "end_page": 5,
      "created_by": "E2E User",
      "last_modified_by": "E2E User",
      "description": "Test Content File",
      "create_learning_units": True
  }
  context.url = f"{API_URL}/learning-resource/ingest"
  assert not is_valid_path(context.resource_path), "Skill csv uri is valid."


@behave.when("A textbook is uploaded into the knowledge graph in pdf format with invalid GCS path")
def step_3_2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("The data ingestion into the knowledge graph should fail with invalid GCS path")
def step_3_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False
  assert context.res_data["data"] is None
  assert context.res_data["message"] == "Skill csv uri is invalid."

#------------------------------ Scenario 4 ---------------------------------#

@behave.given("We can access to textbooks in a pdf format")
def step_3_1(context):
  context.req_body = {
      "title": "E2E learning Resource ingestion",
      "resource_path": "gs://aitutor-dev/course-resources/Bio 101/Introduction to Biology/The Process of Science/chapter 1.2.pdf",
      "format": "pdf",
      "start_page": -1,
      "end_page": 2,
      "created_by": "E2E User",
      "last_modified_by": "E2E User",
      "description": "Test Content File",
      "create_learning_units": True
  }
  context.url = f"{API_URL}/learning-resource/ingest"
  valid_start_page = context.req_body["start_page"] >= 0
  valid_end_page = context.req_body["start_page"] >= 0
  if not (valid_start_page and valid_end_page):
    valid_page = False
  else:
    valid_page = True
  assert not valid_page, "Invalid start or end page."


@behave.when("A textbook is uploaded into the knowledge graph in pdf format with invalid start or end page")
def step_3_2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("The data ingestion into the knowledge graph should fail with invalid start or end page")
def step_3_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] is False
  assert context.res_data["data"] is None
  assert context.res_data["message"] == "Invalid start or end page."
