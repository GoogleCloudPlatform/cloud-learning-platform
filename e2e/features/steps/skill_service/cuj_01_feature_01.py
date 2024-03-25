"""
Ingest skill graph from Credential Engine via API, break out skills and organize them in skill graph
"""

import time
import behave
import requests
import uuid
import pytest
import json
from fastapi.responses import JSONResponse
import sys
sys.path.append("../")
from setup import post_method, get_method, put_method, delete_method
from test_config import API_URL_SKILL_SERVICE

from unittest import mock

API_URL = API_URL_SKILL_SERVICE

@behave.given("Credential Engine has approved University for API usage")
def step_impl_1(context):
  url = "https://credentialengineregistry.org/resources/ce-6fdd56d3-0214-4a67-b0c4-bb4c16ce9a13"
  request = get_method(url=url)
  assert request.status_code == 200
  context.req_body = {
      "competency_frameworks": [
          url
      ]
  }
  context.url = f"{API_URL}/import/credential-engine"


@behave.when("Skill service accesses Credential Engine to download records from their registry with correct request payload")
def step_impl_2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("records should be ingested into skill service")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["status"] == "active"
  job_name = context.res_data["data"]["job_name"]
  url = f"{API_URL}/jobs/credential_engine_ingestion/{job_name}"
  for i in range(60):
    res = get_method(url=url)
    data = res.json()
    if data["data"]["status"] in ["succeeded", "failed"]:
      break
    time.sleep(10)
  assert data["data"]["status"] == "succeeded"


@behave.given("University is approved by Credential Engine for API usage")
def step_impl_1(context):
  _id = uuid.uuid4()
  url = f"https://credentialengineregistry.org/resources/{_id}"
  request = get_method(url)
  assert request.status_code == 404
  context.req_body = {
      "competency_frameworks": [
          url
      ]
  }
  context.url = f"{API_URL}/import/credential-engine"


@behave.when("Skill service accesses Credential Engine to download records from their registry with incorrect request payload")
def step_impl_2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Ingestion in skill service should fail")
def step_impl_3(context):
  assert context.res.status_code == 500
  assert context.res_data["success"] is False
  assert context.res_data["data"] is None


@behave.given("University has access to Credential Engine for API usage")
def step_impl_1(context):
  url = "https://credentialengineregistry.org/resources/ce-1a0b5c43-f3c5-45af-83f6-698da60b9fd8"

  with mock.patch("requests.get",
    return_value=JSONResponse(status_code=502, content={
          "success": False,
          "message": str(requests.exceptions.ConnectionError()),
          "data": {}
        })) as mok:
    request = get_method(url=url)

  assert request.status_code == 502
  context.req_body = {
      "competency_frameworks": [
          url
      ]
  }
  context.url = f"{API_URL}/import/credential-engine"


@behave.when("Skill service accesses Credential Engine to download records from their registry and University server is not running")
def step_impl_2(context):
  with mock.patch("requests.post",
    return_value=JSONResponse(status_code=502, content={
          "success": False,
          "message": str(requests.exceptions.ConnectionError()),
          "data": {}
        })) as mok:
    context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = json.loads(context.res.body)


@behave.then("Skill service ingestion should fail")
def step_impl_3(context):
  assert context.res.status_code == 502
  assert context.res_data["success"] is False
  assert context.res_data["data"] == {}
