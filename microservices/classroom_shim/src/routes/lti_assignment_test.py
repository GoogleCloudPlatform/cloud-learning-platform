"""
  Tests for LTI Assignment endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import,line-too-long
import os
import json
import datetime
import pytest
from copy import deepcopy
from fastapi import FastAPI
from fastapi.testclient import TestClient
from common.models import LTIAssignment
from common.testing.firestore_emulator import firestore_emulator, clean_firestore
from common.utils.http_exceptions import add_exception_handlers
import mock
with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  with mock.patch("routes.lti_assignment.Logger"):
    from routes.lti_assignment import router
    from schemas.schema_examples import (INSERT_LTI_ASSIGNMENT_EXAMPLE,
                                         COPY_LTI_ASSIGNMENT_EXAMPLE)
    from testing.test_config import API_URL

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/classroom-shim/api/v1")

client_with_emulator = TestClient(app)

api_url = f"{API_URL}/lti-assignment"


@pytest.fixture
def create_lti_assignment():
  lti_assignment = LTIAssignment.from_dict(INSERT_LTI_ASSIGNMENT_EXAMPLE)
  lti_assignment.save()
  return lti_assignment


def test_get_lti_assignment(create_lti_assignment):
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
  resp_data.pop("course_work_id")

  assert resp_data == input_data, "Incorrect response received"


def test_get_lti_assignment_negative():
  lti_assignment_id = "1v38m1v64m37cj"
  url = f"{api_url}/{lti_assignment_id}"
  resp = client_with_emulator.get(url)

  assert resp.status_code == 404, "Status should be 404"

  json_response = resp.json()
  assert json_response.get("success") is False, "Response is incorrect"


def test_get_lti_assignments(create_lti_assignment):
  lti_assignment = create_lti_assignment
  url = f"{api_url}s"
  resp = client_with_emulator.get(url)

  assert resp.status_code == 200, "Status should be 200"

  json_response = resp.json()

  resp_data = json_response.get("data")

  assert lti_assignment.id in [i["id"] for i in resp_data
                              ], "Incorrect response received"


def test_get_lti_assignments_negative():
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params={"skip": -1})

  assert resp.status_code == 422, "Status should be 422"

  json_response = resp.json()
  assert json_response.get("success") is False, "Response is incorrect"


@mock.patch("routes.lti_assignment.get_context_details")
@mock.patch("routes.lti_assignment.classroom_crud.create_coursework")
def test_post_lti_assignment(mock_classroom_post_coursework, mock_context):
  mock_context.return_value = {"data": {"classroom_id": "2v1boyeui"}}
  mock_classroom_post_coursework.return_value = {"id": "8v7tcaw"}

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


@mock.patch("routes.lti_assignment.get_context_details")
@mock.patch("routes.lti_assignment.classroom_crud.update_course_work")
def test_update_lti_assignment(mock_classroom_update_coursework, mock_context,
                               create_lti_assignment):
  mock_context.return_value = {"data": {"classroom_id": "2v1boyeui"}}
  mock_classroom_update_coursework.return_value = {"id": "8v7tcaw"}

  lti_assignment = create_lti_assignment

  url = f"{api_url}/{lti_assignment.id}"
  input_data = {"end_date": "2023-10-14T00:00:00+00:00"}
  resp = client_with_emulator.patch(url, json=input_data)

  assert resp.status_code == 200

  json_response = resp.json()
  assert json_response.get("success") is True, "Success not true"
  assert json_response.get("data").get(
      "end_date") == input_data["end_date"], "Expected response not same"


def test_update_lti_assignment_negative():

  lti_assignment_id = "TB2vb9VP8d9YvN8W"
  input_data = {"end_date": "2023-10-14T00:00:00"}
  url = f"{api_url}/{lti_assignment_id}"

  resp = client_with_emulator.patch(url, json=input_data)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response.get("success") is False, "Response is incorrect"


@mock.patch("routes.lti_assignment.get_context_details")
@mock.patch("routes.lti_assignment.classroom_crud.delete_course_work")
def test_delete_lti_assignment(mock_classroom_delete_coursework, mock_context,
                               create_lti_assignment):
  mock_context.return_value = {"data": {"classroom_id": "2v1boyeui"}}
  mock_classroom_delete_coursework.return_value = {"id": "8v7tcaw"}

  lti_assignment = create_lti_assignment

  url = f"{api_url}/{lti_assignment.id}"
  resp = client_with_emulator.delete(url)
  json_resp = resp.json()

  expected_data = {
      "success":
          True,
      "message":
          f"Successfully deleted the LTI Assignment with id {lti_assignment.id}",
      "data":
          None
  }
  print("json_resp", json_resp)
  assert resp.status_code == 200, "Status code not 200"
  assert json_resp == expected_data, "Incorrect response received"


def test_delete_lti_assignment_negative():
  lti_assignment_id = "aG1Jh2sv78fAv5S7F"
  url = f"{api_url}/{lti_assignment_id}"

  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status should be 404"
  assert json_response.get("success") is False, "Response is incorrect"


@mock.patch("routes.lti_assignment.create_content_item")
@mock.patch("routes.lti_assignment.get_content_item")
def test_copy_lti_assignment(mock_get_content_item, mock_create_content_item,
                             create_lti_assignment):
  content_item_details = {
      "id": "aC72Vos31iFQt09c",
      "created_time": "2022-03-03 09:22:49.843674+00:00",
      "last_modified_time": "2022-03-03 09:22:49.843674+00:00",
      "tool_id": "A6cS8vaCsOavO",
      "content_item_type": "ltiResourceLink",
      "content_item_info": {
          "custom": {
              "resourceid": "d83dd1d0-a937-3341-8e9a-eb3cf1146bff"
          },
          "text": "test-image.jpg",
          "title": "test-image.jpg",
          "type": "ltiResourceLink",
          "url": "https://testtool.com/api/ltilaunch/ltitoollaunch"
      },
      "context_id": "F2j4v5b3Vk96b2B"
  }

  mock_get_content_item.return_value = content_item_details
  mock_create_content_item.return_value = {
      **content_item_details, "id": "Ob8Qb2Bn1V7j3"
  }

  lti_assignment_details = create_lti_assignment
  url = f"{api_url}/copy"
  req_body = {
      **COPY_LTI_ASSIGNMENT_EXAMPLE, "lti_assignment_id":
          lti_assignment_details.id,
      "start_date":
          str(COPY_LTI_ASSIGNMENT_EXAMPLE["start_date"]),
      "end_date":
          str(COPY_LTI_ASSIGNMENT_EXAMPLE["end_date"]),
      "due_date":
          str(COPY_LTI_ASSIGNMENT_EXAMPLE["due_date"])
  }
  resp = client_with_emulator.post(url, json=req_body)
  print("resp", resp.status_code, resp.text)
  assert resp.status_code == 200, "Status should be 200"
  json_resp = resp.json()
  assert lti_assignment_details.lti_assignment_title == json_resp.get(
      "data").get("lti_assignment_title")
