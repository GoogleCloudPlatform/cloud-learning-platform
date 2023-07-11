"""
  Unit Tests for PLA record endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
import os
import pytest
from copy import deepcopy
from fastapi import FastAPI
from fastapi.testclient import TestClient
from testing.test_config import API_URL, TESTING_FOLDER_PATH
from routes.pla_record import router
from schemas.schema_examples import (BASIC_PLA_RECORD_MODEL_EXAMPLE,
                                    BASIC_PRIOR_EXPERIENCE_MODEL_EXAMPLE,
                                    BASIC_APPROVED_EXPERIENCE_MODEL_EXAMPLE)
from common.models import PLARecord, PriorExperience, ApprovedExperience
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/prior-learning-assessment/api/v1")

client_with_emulator = TestClient(app)
os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

def test_search_pla_record(clean_firestore):
  pla_record_dict = deepcopy(BASIC_PLA_RECORD_MODEL_EXAMPLE)
  pla_record_dict["type"] = "saved"
  pla_record = PLARecord.from_dict(pla_record_dict)
  pla_record.uuid = ""
  pla_record.save()
  pla_record.uuid = pla_record.id
  pla_record.update()
  pla_record_dict["uuid"] = pla_record.id

  params = {"keyword": "PLA Title"}

  url = f"{API_URL}/pla-record/search"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  print(json_response)
  assert resp.status_code == 200, "Status 200"
  print(json_response)
  assert json_response.get("data")["records"][0].get(
      "title") == BASIC_PLA_RECORD_MODEL_EXAMPLE.get(
          "title"), "Response received"

def test_post_and_get_pla_record(clean_firestore):
  pla_record_dict = deepcopy(BASIC_PLA_RECORD_MODEL_EXAMPLE)
  pla_record_dict["prior_experiences"]=["pe_uuid"]
  pla_record_dict["approved_experiences"]=["ap_uuid"]

  pe_dict = deepcopy(BASIC_PRIOR_EXPERIENCE_MODEL_EXAMPLE)
  del pe_dict["date_completed"]
  pe = PriorExperience.from_dict(pe_dict)
  pe.uuid = ""
  pe.save()
  pe.uuid = pla_record_dict["prior_experiences"][0]
  pe.update()

  ae_dict = deepcopy(BASIC_APPROVED_EXPERIENCE_MODEL_EXAMPLE)
  ae = ApprovedExperience.from_dict(ae_dict)
  ae.uuid = ""
  ae.save()
  ae.uuid = pla_record_dict["approved_experiences"][0]
  ae.update()

  url = f"{API_URL}/pla-record"
  resp = client_with_emulator.post(url, json=pla_record_dict)
  json_response = resp.json()
  print(json_response)
  pla_record_uuid = json_response["data"]["uuid"]

  assert resp.status_code == 200, "Status is not 200"
  assert json_response.get("success") is True, "Success not true"
  assert json_response.get("message") == \
    "Successfully created the PLA Record", "Expected response not same"
  assert json_response.get("data").get("id_number") == 10000
  assert json_response.get("data").get("title") == pla_record_dict.get(
    "title"), "Expected response not same"

  url = f"{API_URL}/pla-record/{pla_record_uuid}"
  resp = client_with_emulator.get(url)
  json_response_get_req = resp.json()

  assert resp.status_code == 200, "Status code not 200"
  assert json_response_get_req.get("data") == json_response.get(
    "data"), "Expected response not same"

def test_get_pla_record_negative(clean_firestore):
  invalid_pla_record_uuid = "random_id"
  url = f"{API_URL}/pla-record/{invalid_pla_record_uuid}"
  response = {
      "success": False,
      "message": "PLA Record with uuid random_id not found",
      "data": None
  }
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"

def test_delete_pla_record_positive(clean_firestore):
  pla_record_dict = deepcopy(BASIC_PLA_RECORD_MODEL_EXAMPLE)
  pla_record_dict["prior_experiences"]=["pe_uuid"]
  pla_record_dict["approved_experiences"]=["ap_uuid"]

  pe_dict = deepcopy(BASIC_PRIOR_EXPERIENCE_MODEL_EXAMPLE)
  del pe_dict["date_completed"]
  pe = PriorExperience.from_dict(pe_dict)
  pe.uuid = ""
  pe.save()
  pe.uuid = pla_record_dict["prior_experiences"][0]
  pe.update()

  ae_dict = deepcopy(BASIC_APPROVED_EXPERIENCE_MODEL_EXAMPLE)
  ae = ApprovedExperience.from_dict(ae_dict)
  ae.uuid = ""
  ae.save()
  ae.uuid = pla_record_dict["approved_experiences"][0]
  ae.update()

  url = f"{API_URL}/pla-record"
  resp = client_with_emulator.post(url, json=pla_record_dict)
  json_response = resp.json()
  pla_record_uuid = json_response["data"]["uuid"]

  url = f"{API_URL}/pla-record/{pla_record_uuid}"
  resp = client_with_emulator.delete(url)
  json_response_delete_req = resp.json()

  expected_data = {
    "success": True,
    "message": "Successfully deleted the PLA Record"
  }
  assert resp.status_code == 200, "Status code not 200"
  assert json_response_delete_req == expected_data, "Expected response not same"

def test_delete_pla_record_negative(clean_firestore):
  invalid_pla_record_uuid = "random_id"
  url = f"{API_URL}/pla-record/{invalid_pla_record_uuid}"
  response = {
      "success": False,
      "message": "PLA Record with uuid random_id not found",
      "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"

def test_update_pla_record_positive(clean_firestore):
  pla_record_dict = deepcopy(BASIC_PLA_RECORD_MODEL_EXAMPLE)
  pla_record_dict["prior_experiences"]=["pe_uuid"]
  pla_record_dict["approved_experiences"]=["ap_uuid"]
  url = f"{API_URL}/pla-record"

  pe_dict = deepcopy(BASIC_PRIOR_EXPERIENCE_MODEL_EXAMPLE)
  del pe_dict["date_completed"]
  pe = PriorExperience.from_dict(pe_dict)
  pe.uuid = ""
  pe.save()
  pe.uuid = pla_record_dict["prior_experiences"][0]
  pe.update()

  ae_dict = deepcopy(BASIC_APPROVED_EXPERIENCE_MODEL_EXAMPLE)
  ae = ApprovedExperience.from_dict(ae_dict)
  ae.uuid = ""
  ae.save()
  ae.uuid = pla_record_dict["approved_experiences"][0]
  ae.update()

  resp = client_with_emulator.post(url, json=pla_record_dict)
  json_response = resp.json()
  updated_data= json_response["data"]
  updated_data["title"] = "updated_title"
  del updated_data ["created_time"]
  del updated_data ["last_modified_time"]

  uuid = updated_data["uuid"]
  del updated_data["uuid"]
  url = f"{API_URL}/pla-record/{uuid}"
  resp = client_with_emulator.put(url, json=updated_data)
  json_response_update_req = resp.json()

  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get("message") == \
    "Successfully updated the PLA Record", "Expected response not same"
  assert json_response_update_req.get("data").get("title") == \
    "updated_title", "Expected response not same"

def test_update_pla_record_negative(clean_firestore):
  req_json = deepcopy(BASIC_PLA_RECORD_MODEL_EXAMPLE)

  uuid = "random_id"
  response = {
      "success": False,
      "message": "PLA Record with uuid random_id not found",
      "data": None
  }

  url = f"{API_URL}/pla-record/{uuid}"
  resp = client_with_emulator.put(url, json=req_json)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"

def test_import_pla_record(clean_firestore):
  url = f"{API_URL}/pla-record/import/json"
  file_path = os.path.join(TESTING_FOLDER_PATH, "pla_records.json")
  with open(file_path, "rb") as file:
    resp = client_with_emulator.post(url, files={"json_file": file})

  json_response = resp.json()

  assert resp.status_code == 200, "Success not 200"
  assert isinstance(json_response.get("data"), list), "Response is not a list"
  assert len(json_response.get("data")) == 2, "returned length is not same"

def test_get_all_assessor_names(clean_firestore):
  pla_record_dict_1 = deepcopy(BASIC_PLA_RECORD_MODEL_EXAMPLE)
  pla_record_dict_1["assessor_name"] = "user1"
  pla_record_1 = PLARecord.from_dict(pla_record_dict_1)
  pla_record_1.uuid = ""
  pla_record_1.save()
  pla_record_1.assessor_name = "user_1"
  pla_record_1.update()

  pla_record_dict_2 = deepcopy(BASIC_PLA_RECORD_MODEL_EXAMPLE)
  pla_record_2 = PLARecord.from_dict(pla_record_dict_2)
  pla_record_2.uuid = ""
  pla_record_2.save()
  pla_record_2.assessor_name = "user_2"
  pla_record_2.update()

  pla_record_dict_3 = deepcopy(BASIC_PLA_RECORD_MODEL_EXAMPLE)
  pla_record_3 = PLARecord.from_dict(pla_record_dict_3)
  pla_record_3.uuid = ""
  pla_record_3.save()
  pla_record_3.assessor_name = "user_3"
  pla_record_3.update()

  url = f"{API_URL}/pla-record/assessors/unique"
  resp = client_with_emulator.get(url)
  resp_json = resp.json()
  print(pla_record_1.get_fields())
  print(pla_record_2.get_fields())
  print(pla_record_3.get_fields())
  assert sorted([pla_record_1.assessor_name, pla_record_2.assessor_name,
                 pla_record_3.assessor_name]) == sorted(resp_json.get("data"))
