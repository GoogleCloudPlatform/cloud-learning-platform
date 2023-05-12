"""
Unit Tests for FAQ endpoints
"""
import os
import copy
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.faq_content import router
from testing.test_config import API_URL, TESTING_FOLDER_PATH
from schemas.schema_examples import (BASIC_FAQ_CONTENT_EXAMPLE,
BASIC_CURRICULUM_PATHWAY_EXAMPLE)
from common.models import FAQContent, CurriculumPathway
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/learning-object-service/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/faq"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def create_faq_document(faq_dict):
  faq_content = FAQContent.from_dict({**faq_dict, "uuid": ""})
  faq_content.save()
  faq_content.uuid = faq_content.id
  faq_content.update()
  return faq_content


def test_get_faq_positive(clean_firestore):
  # Generate FAQ data
  new_faq_doc = create_faq_document({**BASIC_FAQ_CONTENT_EXAMPLE})

  faq_content = FAQContent.find_by_uuid(new_faq_doc.uuid)

  url = f"{api_url}/{faq_content.uuid}"

  res = client_with_emulator.get(url)
  res_json = res.json()

  assert res.status_code == 200
  assert res_json["success"] is True
  assert res_json["message"] == "Successfully Fetched FAQ by UUID"


def test_get_faq_negative(clean_firestore):
  random_faq_id = "random_faq_id"
  url = f"{api_url}/{random_faq_id}"

  res = client_with_emulator.get(url)
  res_json = res.json()

  assert res.status_code == 404
  assert res_json["success"] is False
  assert res_json["message"] == f"FAQ with uuid {random_faq_id} not found"


def test_get_all_faq_positive(clean_firestore):
  # Generate FAQ data
  new_faq_doc = create_faq_document({**BASIC_FAQ_CONTENT_EXAMPLE})

  FAQContent.find_by_uuid(new_faq_doc.uuid)

  url = f"{api_url}"

  res = client_with_emulator.get(url)
  res_json = res.json()

  assert res.status_code == 200
  assert res_json["success"] is True
  assert res_json["message"] == "Successfully Fetched FAQs"

  assert res_json["data"][0]["name"] == BASIC_FAQ_CONTENT_EXAMPLE[
      "name"]

def test_filter_faq_by_pathway_id_positive(clean_firestore):

  curriculum_pathway_dict = copy.deepcopy(BASIC_CURRICULUM_PATHWAY_EXAMPLE)
  curriculum_pathway_dict["name"] = "Kubernetes Container Orchestration"
  curriculum_pathway = CurriculumPathway.from_dict(curriculum_pathway_dict)
  curriculum_pathway.uuid = ""
  curriculum_pathway.save()
  curriculum_pathway.uuid = curriculum_pathway.id
  curriculum_pathway.update()
  curriculum_pathway_dict["uuid"] = curriculum_pathway.id

  # Generate FAQ data
  new_faq_doc = create_faq_document({**BASIC_FAQ_CONTENT_EXAMPLE,
                   "curriculum_pathway_id": curriculum_pathway_dict["uuid"]})

  FAQContent.find_by_uuid(new_faq_doc.uuid)

  url = f"{api_url}"
  params = {"curriculum_pathway_id": curriculum_pathway_dict["uuid"]}
  res = client_with_emulator.get(url, params=params)
  res_json = res.json()

  assert res.status_code == 200
  assert res_json["success"] is True
  assert res_json["message"] == "Successfully Fetched FAQs"
  assert res_json["data"][0][
    "curriculum_pathway_id"] == curriculum_pathway_dict["uuid"]

def test_filter_faq_by_pathway_id_negative(clean_firestore):
  # Generate FAQ data
  new_faq_doc = create_faq_document({**BASIC_FAQ_CONTENT_EXAMPLE})

  FAQContent.find_by_uuid(new_faq_doc.uuid)
  curriculum_pathway_id =  "something"

  url = f"{api_url}"
  params = {"curriculum_pathway_id": curriculum_pathway_id}
  res = client_with_emulator.get(url, params=params)
  res_json = res.json()

  assert res.status_code == 404
  assert res_json["success"] is False
  assert res_json["message"
    ] == f"Curriculum Pathway with uuid {curriculum_pathway_id} not found"

def test_create_faq_negative(clean_firestore):
  new_faq_doc = {**BASIC_FAQ_CONTENT_EXAMPLE, "name":
      "Sample gjhxkjjclkvhkskcxzjchsjhuxbnjcgsadyuxbzjdcnskaxlzkcs\
      jdskalkJScidhsvusjkasxjkhsdjciosojcdncjksldasfyhuia"}
  url = f"{api_url}"

  res = client_with_emulator.post(url, json=new_faq_doc)
  res_json = res.json()

  assert res.status_code == 422
  assert res_json["success"] is False
  assert res_json["message"] == "Validation Failed"

def test_create_faq_negative_2(clean_firestore):
  curriculum_pathway_dict = copy.deepcopy(BASIC_CURRICULUM_PATHWAY_EXAMPLE)
  curriculum_pathway_dict["name"] = "Kubernetes Container Orchestration"
  curriculum_pathway = CurriculumPathway.from_dict(curriculum_pathway_dict)
  curriculum_pathway.uuid = ""
  curriculum_pathway.alias = "program"
  curriculum_pathway.save()
  curriculum_pathway.uuid = curriculum_pathway.id
  curriculum_pathway.update()
  curriculum_pathway_dict["uuid"] = curriculum_pathway.id

  url = f"{api_url}"
  new_faq_doc = {**BASIC_FAQ_CONTENT_EXAMPLE}
  new_faq_doc["curriculum_pathway_id"] = curriculum_pathway.uuid

  res = client_with_emulator.post(url, json=new_faq_doc)
  assert res.status_code == 200

  new_faq_doc_2 = {**BASIC_FAQ_CONTENT_EXAMPLE}
  new_faq_doc_2["curriculum_pathway_id"] = curriculum_pathway.uuid

  res = client_with_emulator.post(url, json=new_faq_doc)
  res_json = res.json()
  assert res.status_code == 422
  # pylint: disable = line-too-long
  assert res_json["message"] == f"Curriculum Pathway {curriculum_pathway.uuid} is already linked to an FAQ."

def test_update_faq(clean_firestore, mocker):
  mocker.patch("routes.faq_content.is_valid_path", return_value = True)

  curriculum_pathway_dict = copy.deepcopy(BASIC_CURRICULUM_PATHWAY_EXAMPLE)
  curriculum_pathway_dict["name"] = "Kubernetes Container Orchestration"
  curriculum_pathway = CurriculumPathway.from_dict(curriculum_pathway_dict)
  curriculum_pathway.uuid = ""
  curriculum_pathway.alias = "program"
  curriculum_pathway.save()
  curriculum_pathway.uuid = curriculum_pathway.id
  curriculum_pathway.update()
  curriculum_pathway_dict["uuid"] = curriculum_pathway.id

  url = f"{api_url}"

  new_faq_doc = {**BASIC_FAQ_CONTENT_EXAMPLE,
                  "name":"sample_faq",
                  "curriculum_pathway_id": curriculum_pathway.id
                }

  res = client_with_emulator.post(url, json=new_faq_doc)
  res_json = res.json()

  assert res.status_code == 200
  assert res_json["success"] is True
  assert res_json["message"] == "Successfully Created FAQ"

  faq_uuid = res_json["data"]["uuid"]

  updated_faq_doc = {
    "resource_path" : "updated_resource_path"
  }

  res = client_with_emulator.put(f"{url}/{faq_uuid}", json=updated_faq_doc)
  res_json = res.json()

  assert res.status_code == 200
  assert res_json["success"] is True
  assert res_json["message"] == "Successfully updated FAQ"

def test_update_faq_negative(clean_firestore, mocker):
  mocker.patch("routes.faq_content.is_valid_path", return_value = False)

  curriculum_pathway_dict = copy.deepcopy(BASIC_CURRICULUM_PATHWAY_EXAMPLE)
  curriculum_pathway_dict["name"] = "Kubernetes Container Orchestration"
  curriculum_pathway = CurriculumPathway.from_dict(curriculum_pathway_dict)
  curriculum_pathway.uuid = ""
  curriculum_pathway.alias = "program"
  curriculum_pathway.save()
  curriculum_pathway.uuid = curriculum_pathway.id
  curriculum_pathway.update()
  curriculum_pathway_dict["uuid"] = curriculum_pathway.id

  url = f"{api_url}"

  new_faq_doc = {**BASIC_FAQ_CONTENT_EXAMPLE,
                  "name":"sample_faq",
                  "curriculum_pathway_id": curriculum_pathway.id
                }

  res = client_with_emulator.post(url, json=new_faq_doc)
  res_json = res.json()

  assert res.status_code == 200
  assert res_json["success"] is True
  assert res_json["message"] == "Successfully Created FAQ"

  faq_uuid = res_json["data"]["uuid"]

  updated_faq_doc = {
    "resource_path" : "updated_resource_path"
  }

  res = client_with_emulator.put(f"{url}/{faq_uuid}", json=updated_faq_doc)
  res_json = res.json()

  assert res.status_code == 404
  assert res_json["success"] is False
  msg = "Provided resource path does not exist on GCS bucket"
  assert res_json["message"] == msg

def test_delete_faq(clean_firestore, mocker):
  curriculum_pathway_dict = copy.deepcopy(BASIC_CURRICULUM_PATHWAY_EXAMPLE)
  curriculum_pathway_dict["name"] = "Kubernetes Container Orchestration"
  curriculum_pathway = CurriculumPathway.from_dict(curriculum_pathway_dict)
  curriculum_pathway.uuid = ""
  curriculum_pathway.alias = "program"
  curriculum_pathway.save()
  curriculum_pathway.uuid = curriculum_pathway.id
  curriculum_pathway.update()
  curriculum_pathway_dict["uuid"] = curriculum_pathway.id

  new_faq_doc = {**BASIC_FAQ_CONTENT_EXAMPLE,
                  "curriculum_pathway_id": curriculum_pathway.id}
  url = f"{api_url}"

  res = client_with_emulator.post(url, json=new_faq_doc)
  res_json = res.json()

  assert res.status_code == 200
  assert res_json["success"] is True
  assert res_json["message"] == "Successfully Created FAQ"

  faq_uuid = res_json["data"]["uuid"]

  res = client_with_emulator.delete(f"{url}/{faq_uuid}")
  res_json = res.json()

  assert res.status_code == 200
  assert res_json["success"] is True
  assert res_json["message"] == "Successfully deleted FAQ"
