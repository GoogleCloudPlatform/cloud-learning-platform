"""
Ingest skills from Burning Glass via API, break out skills and organize them into skill graph
"""

import time
import behave
import requests
import json
from fastapi.responses import JSONResponse

import sys 
sys.path.append("../")
from setup import post_method, get_method
from test_config import API_URL_SKILL_SERVICE

from unittest import mock

API_URL = API_URL_SKILL_SERVICE

@behave.given("Burning Glass has approved University for API usage")
def step_impl_1(context):
  context.url = f"{API_URL}/import/emsi"
  context.param1 = {"size": 1}
  
@behave.when("Skill service accesses Burning Glass to download records from their registry with correct request payload")
def step_impl_2(context):
  context.res = post_method(url = context.url, query_params=context.param1)
  context.res_data = context.res.json()

@behave.then("records from EMSI should be ingested into skill service")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["status"] == "active"
  job_name = context.res_data["data"]["job_name"]
  url = f"{API_URL}/jobs/emsi_ingestion/{job_name}"
  for i in range(60):
    res = get_method(url=url)
    data = res.json()
    if data["data"]["status"] in ["succeeded", "failed"]:
      break
    time.sleep(10)
  assert data["data"]["status"] == "succeeded"



@behave.given("University is approved by Burning Glass for API usage")
def step_impl_1(context):
  context.url = f"{API_URL}/import/emsi"
  context.param2 = {"size": 0}

@behave.when("Skill service accesses Burning Glass to download records from their registry with incorrect request payload")
def step_impl_2(context):
  context.res = post_method(url = context.url, query_params=context.param2)
  context.res_data = context.res.json()

@behave.then("Ingestion from EMSI in skill service should fail")
def step_impl_3(context):
  time.sleep(20)
  assert context.res.status_code == 422
  assert context.res_data["success"] is False
  assert context.res_data["data"] is None



@behave.given("University has access to Burning Glass for API usage")
def step_impl_1(context):
  context.url = f"{API_URL}/import/emsi"
  context.param1 = {"size": 1}

@behave.when("Skill service accesses Burning Glass to download records from their registry and University server is not running")
def step_impl_2(context):
  with mock.patch("requests.post",
    return_value=JSONResponse(status_code=502, content={
          "success": False,
          "message": str(requests.exceptions.ConnectionError()),
          "data": {}
        })) as mok:
    context.res = post_method(url = context.url, query_params=context.param1)
  context.res_data = json.loads(context.res.body)

@behave.then("Skill service ingestion from EMSI should fail")
def step_impl_3(context):
  assert context.res.status_code == 502
  assert context.res_data["success"] is False
  assert context.res_data["data"] == {}
