"""
Ingest external (OSN) data, break out skills and organize them in skill graph
"""

import os
import time
import behave
import requests
import pytest
import json
from fastapi.responses import JSONResponse

import sys 
sys.path.append("../")
from setup import post_method, get_method
from test_config import API_URL_SKILL_SERVICE, TESTING_OBJECTS_PATH

API_URL = API_URL_SKILL_SERVICE

@behave.given("the OSN skill data set can be accessed")
def step_impl_1(context):
  context.url = f"{API_URL}/import/csv"
  context.skill_csv_file_path = os.path.join(TESTING_OBJECTS_PATH, "generic_skill.csv")
  context.param = {"source": "osn"}
  
@behave.when("the OSN skill data set is uploaded into the skill graph")
def step_impl_2(context):
  with open(context.skill_csv_file_path, encoding="UTF-8") as skills_file:
    files = {"skills": skills_file}
    context.res = post_method(url = context.url, query_params = context.param , files = files)
    context.res_data = context.res.json()

@behave.then("that data should be ingested into the skill graph in csv format")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["status"] == "active"
  job_name = context.res_data["data"]["job_name"]
  url = f"{API_URL}/jobs/generic_csv_ingestion/{job_name}"
  for i in range(60):
    res = get_method(url=url)
    data = res.json()
    if data["data"]["status"] in ["succeeded", "failed"]:
      break
    time.sleep(10)
  assert data["data"]["status"] == "succeeded"

@behave.then("mapped with internal skills using correct request payload")
def step_impl_4(context):
  alignment_url = f"{API_URL}/unified-alignment/batch"
  internal_skill_id = "1c17caad-5580-4d10-85ce-32dc369c5cd7"
  req_body = {
      "ids": [internal_skill_id],
      "input_type": "skill",
      "top_k": 5,
      "output_alignment_sources" : {"skill_sources": ["e2e_osn"],
            "learning_resource_ids": [] },
      "update_aligned_skills": True
  }
  response = post_method(url = alignment_url, request_body = req_body)
  res_data = response.json()
  time.sleep(20)
  assert response.status_code == 200
  assert res_data["success"] is True
  assert res_data["data"]["status"] == "active"
  #check if job succeeded
  job_name = res_data["data"]["job_name"]
  url = f"{API_URL}/jobs/unified_alignment/{job_name}"
  for i in range(50):
    res = get_method(url=url)
    data = res.json()
    if data["data"]["status"] in ["succeeded", "failed"]:
      break
    time.sleep(10)
  assert data["data"]["status"] == "succeeded"
  #check alignment
  skill_url = f"{API_URL}/skill/{internal_skill_id}"
  resp = get_method(url = skill_url)
  resp_data = resp.json()
  assert resp.status_code == 200
  assert resp_data["success"] == True
  assert len(resp_data["data"]["alignments"]["skill_alignment"]["e2e_osn"]["suggested"]) >0

@behave.given("the OSN skill data set can be accessed by University")
def step_impl_1(context):
  context.url = f"{API_URL}/import/csv"
  context.skill_csv_file_path = os.path.join(TESTING_OBJECTS_PATH,
                                     "invalid_generic_skill.csv")
  context.param = {"source": "osn"}
  
@behave.when("the OSN skill data set is uploaded into the skill graph with incorrect request payload")
def step_impl_2(context):
  with open(context.skill_csv_file_path, encoding="UTF-8") as skills_file:
    files = {"skills": skills_file}
    context.res = post_method(url = context.url, query_params = context.param , files = files)
    context.res_data = context.res.json()
 
@behave.then("the data ingestion into the skill graph should fail due to incorrect request payload")
def step_impl_3(context):
  assert context.res.status_code == 422, "Status code not 500"
  assert context.res_data.get("message") == "Required column \"description\" is missing in skills csv", \
    "Unexpected response message"



@behave.given("University has access to OSN for API usage")
def step_impl_1(context):
  context.url = f"{API_URL}/import/csv"
  context.skill_csv_file_path = os.path.join(TESTING_OBJECTS_PATH, "generic_skill.csv")
  context.param = {"source": "osn"}
  
@behave.when("the OSN skill data set is uploaded into the skill graph with correct payload")
def step_impl_2(context):
  with open(context.skill_csv_file_path, encoding="UTF-8") as skills_file:
    files = {"skills": skills_file}
    context.res = post_method(url = context.url, query_params = context.param , files = files)
    context.res_data = context.res.json()

@behave.then("that data should be ingested into the skill graph in csv format with correct request payload")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["status"] == "active"
  job_name = context.res_data["data"]["job_name"]
  url = f"{API_URL}/jobs/generic_csv_ingestion/{job_name}"
  for i in range(60):
    res = get_method(url=url)
    data = res.json()
    if data["data"]["status"] in ["succeeded", "failed"]:
      break
    time.sleep(10)
  assert data["data"]["status"] == "succeeded"

@behave.then("mapped with internal skills should fail due to incorrect request payload")
def step_impl_4(context):
  alignment_url = f"{API_URL}/unified-alignment/batch"
  internal_skill_id = "0Av13VYzAiPWw9RdSVmy"
  req_body = {
      "ids": [internal_skill_id],
      "input_type": "skill",
      "top_k": 5,
      "output_alignment_sources" : {"skill_sources": ["osn"],
            "learning_resource_ids": [] },
      "update_aligned_skills": True
  }
  response = post_method(url = alignment_url, request_body = req_body)
  res_data = response.json()
  assert response.status_code == 404
  assert res_data["message"] == "Skill with uuid 0Av13VYzAiPWw9RdSVmy not found"
