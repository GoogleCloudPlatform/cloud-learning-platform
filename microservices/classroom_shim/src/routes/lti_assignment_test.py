"""
  Tests for LTI Assignment endpoints
"""
import os
import json
import datetime
import pytest

# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import,line-too-long
from copy import deepcopy
from common.models import LTIAssignment
from common.testing.firestore_emulator import firestore_emulator, clean_firestore
from common.utils.http_exceptions import add_exception_handlers
from schemas.schema_examples import INSERT_LTI_ASSIGNMENT_EXAMPLE
from testing.test_config import API_URL
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.platform_auth import router

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/classroom-shim/api/v1")

client_with_emulator = TestClient(app)

api_url = f"{API_URL}/lti-assignment"


@pytest.fixture
def create_lti_assignment(client_with_emulator):
  lti_assignment = LTIAssignment.from_dict(INSERT_LTI_ASSIGNMENT_EXAMPLE)
  lti_assignment.save()
  return lti_assignment


def test_get_lti_assignment(client_with_emulator, create_lti_assignment):
  lti_assignment = create_lti_assignment
  input_data = deepcopy(INSERT_LTI_ASSIGNMENT_EXAMPLE)
  url = f"{api_url}/{lti_assignment.id}"
  resp = client_with_emulator.get(url)

  assert resp.status_code == 200, "Status should be 200"

  json_response = resp.json()

  resp_data = json_response.get("data")
  del resp_data["id"]

  resp_data["start_date"] = datetime.datetime.strptime(
      resp_data.pop("start_date").split("+")[0], "%Y-%m-%dT%H:%M:%S")
  resp_data["end_date"] = datetime.datetime.strptime(
      resp_data.pop("end_date").split("+")[0], "%Y-%m-%dT%H:%M:%S")
  resp_data["due_date"] = datetime.datetime.strptime(
      resp_data.pop("due_date").split("+")[0], "%Y-%m-%dT%H:%M:%S")

  assert resp_data == input_data, "Incorrect response received"


def test_get_lti_assignment_negative(client_with_emulator):
  lti_assignment_id = "1v38m1v64m37cj"
  url = f"{api_url}/{lti_assignment_id}"
  resp = client_with_emulator.get(url)

  assert resp.status_code == 404, "Status should be 404"

  json_response = resp.json()
  assert json_response.get("success") is False, "Response is incorrect"


def test_get_lti_assignments(client_with_emulator, create_lti_assignment):
  lti_assignment = create_lti_assignment
  url = f"{api_url}s"
  resp = client_with_emulator.get(url)

  assert resp.status_code == 200, "Status should be 200"

  json_response = resp.json()

  resp_data = json_response.get("data")

  assert lti_assignment.id in [i["id"] for i in resp_data
                               ], "Incorrect response received"


def test_get_lti_assignments_negative(client_with_emulator):
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params={"skip": -1})

  assert resp.status_code == 422, "Status should be 422"

  json_response = resp.json()
  assert json_response.get("success") is False, "Response is incorrect"


def test_post_lti_assignment(client_with_emulator):
  input_lti_assignment = deepcopy(INSERT_LTI_ASSIGNMENT_EXAMPLE)
  url = f"{api_url}"

  input_lti_assignment["start_date"] = datetime.datetime.strftime(
      input_lti_assignment.pop("start_date"), "%Y-%m-%dT%H:%M:%S")
  input_lti_assignment["end_date"] = datetime.datetime.strftime(
      input_lti_assignment.pop("end_date"), "%Y-%m-%dT%H:%M:%S")
  input_lti_assignment["due_date"] = datetime.datetime.strftime(
      input_lti_assignment.pop("due_date"), "%Y-%m-%dT%H:%M:%S")

  post_resp = client_with_emulator.post(url, json=input_lti_assignment)

  assert post_resp.status_code == 200, "Status should be 200"

  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"

  post_json_response = json.loads(post_resp.text)

  lti_assignment_id = post_json_response.get("data").get("id")

  # now see if GET endpoint returns same data
  url = f"{api_url}/{lti_assignment_id}"
  get_resp = client_with_emulator.get(url)
  get_json_response = get_resp.json()

  assert get_resp.status_code == 200, "Status should be 200"
  assert get_json_response.get("data") == post_json_response.get("data")


def test_update_lti_assignment(client_with_emulator, create_lti_assignment):
  lti_assignment = create_lti_assignment

  url = f"{api_url}/{lti_assignment.id}"
  input_data = {"end_date": "2023-10-14T00:00:00+00:00"}
  resp = client_with_emulator.patch(url, json=input_data)

  assert resp.status_code == 200

  json_response = resp.json()
  assert json_response.get("success") is True, "Success not true"
  assert json_response.get("data").get(
      "end_date") == input_data["end_date"], "Expected response not same"


def test_update_lti_assignment_negative(client_with_emulator):

  lti_assignment_id = "TB2vb9VP8d9YvN8W"
  input_data = {"end_date": "2023-10-14T00:00:00"}
  url = f"{api_url}/{lti_assignment_id}"

  resp = client_with_emulator.patch(url, json=input_data)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response.get("success") is False, "Response is incorrect"


def test_delete_lti_assignment(client_with_emulator, create_lti_assignment):
  lti_assignment = create_lti_assignment

  url = f"{api_url}/{lti_assignment.id}"
  resp = client_with_emulator.delete(url)
  json_resp = resp.json()

  expected_data = {
      "success": True,
      "message":
      f"Successfully deleted the LTI Assignment with id {lti_assignment.id}",
      "data": None
  }
  print("json_resp", json_resp)
  assert resp.status_code == 200, "Status code not 200"
  assert json_resp == expected_data, "Incorrect response received"


def test_delete_lti_assignment_negative(client_with_emulator):
  lti_assignment_id = "aG1Jh2sv78fAv5S7F"
  url = f"{api_url}/{lti_assignment_id}"

  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status should be 404"
  assert json_response.get("success") is False, "Response is incorrect"
