"""
    User should be able to fetch FAQ data
"""
import behave
import sys
from copy import copy
from common.utils.gcs_adapter import GcsCrudService
from common.models import FAQContent

sys.path.append("../")
from e2e.setup import get_method, post_method, CONTENT_SERVING_BUCKET, set_cache, get_cache, put_method, delete_method, CONTENT_SERVING_BUCKET
from environment import TEST_CONTENT_SERVING_PATH, TEST_CONTENT_SERVING_ZIP_PATH
from e2e.test_config import API_URL_LEARNING_OBJECT_SERVICE, DEL_KEYS
from e2e.test_object_schemas import (TEST_BASIC_FAQ, TEST_CURRICULUM_PATHWAY)

API_URL = API_URL_LEARNING_OBJECT_SERVICE

# -----------------------------------------------------
# Scenario 1: User wants to fetch a FAQ document with UUID
# -----------------------------------------------------
@behave.given("that an LXE or CD wants to fetch a FAQ document with valid UUID")
def step_impl_1(context):
    context.gcs_object = GcsCrudService(CONTENT_SERVING_BUCKET)
    context.content_serving_uri = context.gcs_object.upload_file_to_bucket(
                                    "faq-resources/dev_testing/testing-files",
                                    "content_serving.html", TEST_CONTENT_SERVING_PATH)
    context.content_serving_uri = context.content_serving_uri.split("faq-resources/")[1]

    faq_content = FAQContent.from_dict({
                                        **TEST_BASIC_FAQ, 
                                        "uuid":"",
                                        "resource_path": context.content_serving_uri
                                        })
    faq_content.save()
    faq_content.uuid = faq_content.id
    faq_content.update()

    context.faq_uuid =  faq_content.uuid

@behave.when("API request is sent to get the FAQ by UUID")
def step_impl_2(context):
    context.res = get_method(
        url=f"{API_URL}/faq/{context.faq_uuid}"
    )
    context.res_json = context.res.json()

@behave.then("the service responds a success status")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_json["success"] == True
    assert context.res_json["message"] == "Successfully Fetched FAQ by UUID"

@behave.then("signed URL can be generated for this faq.")
def step_impl_4(context):
    res = get_method(
        url=f"{API_URL}/content-serving/{context.faq_uuid}",
        query_params={
            "is_faq":True
        }
    )
    res_json = res.json()

    assert res.status_code == 200
    assert res_json["success"] == True
    assert res_json["message"] == "Successfully fetched the signed url"

# -----------------------------------------------------
# Scenario 2: User wants to fetch all FAQ documents
# -----------------------------------------------------
@behave.given("that an LXE or CD wants to fetch all the FAQ documents")
def step_impl_1(context):
    faq_content = FAQContent.from_dict({**TEST_BASIC_FAQ, "uuid":""})
    faq_content.save()
    faq_content.uuid = faq_content.id
    faq_content.update()

    context.faq_uuid =  faq_content.uuid

@behave.when("API request is sent to get the FAQ list")
def step_impl_2(context):
    context.res = get_method(
        url=f"{API_URL}/faq"
    )
    print(context.res)
    context.res_json = context.res.json()

@behave.then("the service responds with a success status and list of all faqs")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_json["success"] == True
    assert context.res_json["message"] == "Successfully Fetched FAQs"
    assert len(context.res_json["data"]) >= 1

# -----------------------------------------------------
# Scenario 3: User wants to fetch a FAQ document with invalid FAQ uuid
# -----------------------------------------------------
@behave.given("that an LXE or CD wants to fetch a FAQ document with invalid FAQ uuid")
def step_impl_1(context):
    context.faq_uuid = "random_faq_uuid"

@behave.when("API request is sent to get the FAQ with invalid UUID")
def step_impl_2(context):
    context.res = get_method(
        url=f"{API_URL}/faq/{context.faq_uuid}"
    )
    context.res_json = context.res.json()

@behave.then("the service responds with 404 status saying the FAQ does not exists")
def step_impl_3(context):
    assert context.res.status_code == 404
    assert context.res_json["success"] == False
    assert context.res_json["message"] == f"FAQ with uuid {context.faq_uuid} not found"

# --------------------------------------------------------------------
# Scenario 4: User wants to fetch FAQ documents by curriculum_pathway_id
# --------------------------------------------------------------------
@behave.given("that an LXE or CD wants to fetch FAQ documents for given curriculum_pathway_id")
def step_impl_1(context):
    curriculum_req_body = copy(TEST_CURRICULUM_PATHWAY)
    for key in DEL_KEYS:
        if key in curriculum_req_body:
            del curriculum_req_body[key]
    curriculum_url = f"{API_URL}/curriculum-pathway"
    curriculum_res = post_method(url=curriculum_url, request_body=curriculum_req_body)
    curriculum_res_data = curriculum_res.json()
    context.curriculum_pathway_id = curriculum_res_data["data"]["uuid"]
  
    faq_content = FAQContent.from_dict({**TEST_BASIC_FAQ, "uuid":"",
                            "curriculum_pathway_id": context.curriculum_pathway_id})
    faq_content.save()
    faq_content.uuid = faq_content.id
    faq_content.update()

    context.faq_uuid =  faq_content.uuid

    context.query_params = {
    "curriculum_pathway_id": context.curriculum_pathway_id
    }

@behave.when("API request is sent to get the FAQ list by curriculum_pathway_id")
def step_impl_2(context):
    context.res = get_method(
        url=f"{API_URL}/faq", query_params=context.query_params
    )
    print(context.res)
    context.res_json = context.res.json()

@behave.then("the service responds with a success status and list of faqs for the given curriculum_pathway_id")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_json["success"] == True
    assert context.res_json["message"] == "Successfully Fetched FAQs"
    assert context.res_json["data"][
        "records"][0]['curriculum_pathway_id'] == context.curriculum_pathway_id

# -------------------------------------------------------------------------
# Scenario 5: User wants to create FAQ documents
# -------------------------------------------------------------------------
@behave.given("that an LXE or CD wants to create FAQ documents")
def step_impl_1(context):
    curriculum_req_body = copy(TEST_CURRICULUM_PATHWAY)
    for key in DEL_KEYS:
        if key in curriculum_req_body:
            del curriculum_req_body[key]
    curriculum_req_body["alias"] = "program"
    curriculum_url = f"{API_URL}/curriculum-pathway"
    curriculum_res = post_method(url=curriculum_url, request_body=curriculum_req_body)
    print(curriculum_res)
    curriculum_res_data = curriculum_res.json()
    context.curriculum_pathway_id = curriculum_res_data["data"]["uuid"]

    context.faq_content = {**TEST_BASIC_FAQ,
                         "curriculum_pathway_id": context.curriculum_pathway_id}

@behave.when("API request is sent to create the FAQ")
def step_impl_2(context):
    context.res = post_method(
        url=f"{API_URL}/faq", request_body=context.faq_content)
    context.res_json = context.res.json()

@behave.then("the service responds with a success status on creating FAQ")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_json["success"] == True
    assert context.res_json["message"] == "Successfully Created FAQ"
    assert context.res_json["data"] != []

# -------------------------------------------------------------------------
# Scenario 5: User wants to create FAQ documents with an invalid name
# -------------------------------------------------------------------------
@behave.given("that an LXE or CD wants to create FAQ documents with an invalid name")
def step_impl_1(context):
    context.faq_content = {**TEST_BASIC_FAQ,
        "name": "Sample gjhxkjjclkvhkskcxzjchsjhuxbnjcgsadyuxbzjdcnskaxlzkcs\
        jdskalkJScidhsvusjkasxjkhsdjciosojcdncjksldasfyhuia"}

@behave.when("API request is sent to create the FAQ with an invalid name")
def step_impl_2(context):
    context.res = post_method(
        url=f"{API_URL}/faq", request_body=context.faq_content)
    context.res_json = context.res.json()

@behave.then("the service fails to create FAQ")
def step_impl_3(context):
    assert context.res.status_code == 422
    assert context.res_json["success"] == False
    assert context.res_json["message"] == "Validation Failed"

# -------------------------------------------------------------------------
# Scenario 6: User wants to recreate FAQ for a curriculum pathway
# -------------------------------------------------------------------------
@behave.given("that an LXE or CD wants to recreate a FAQ for a curriculum pathway")
def step_impl_1(context):
    curriculum_req_body = copy(TEST_CURRICULUM_PATHWAY)
    for key in DEL_KEYS:
        if key in curriculum_req_body:
            del curriculum_req_body[key]
    curriculum_req_body["alias"] = "program"
    curriculum_url = f"{API_URL}/curriculum-pathway"
    curriculum_res = post_method(url=curriculum_url, request_body=curriculum_req_body)

    assert curriculum_res.status_code == 200
    context.cp_uuid = curriculum_res.json()["data"]["uuid"]

    context.faq_content = {**TEST_BASIC_FAQ,"curriculum_pathway_id":context.cp_uuid}

    res = post_method(
        url=f"{API_URL}/faq", request_body=context.faq_content)
    assert res.status_code == 200

@behave.when("API request is sent to create the new FAQ with curriculum pathway uuid which is already used")
def step_impl_2(context):
    context.res = post_method(
        url=f"{API_URL}/faq", request_body=context.faq_content)
    context.res_json = context.res.json()

@behave.then("the service returns validation error saying FAQ for curriculum pathway already exists")
def step_impl_3(context):
    assert context.res.status_code == 422
    assert context.res_json["success"] == False
    assert context.res_json["message"] == f"Curriculum Pathway {context.cp_uuid} is already linked to an FAQ."

# -------------------------------------------------------------------------
# Scenario 6: User wants to update FAQ with correct payload
# -------------------------------------------------------------------------
@behave.given("that an LXE or CD wants to update a FAQ with correct payload")
def step_impl_1(context):
    context.gcs_object = GcsCrudService(CONTENT_SERVING_BUCKET)
    context.content_serving_uri = context.gcs_object.upload_file_to_bucket(
                                        "faq-resources/dev_testing/testing-files",
                                        "content_serving.html", TEST_CONTENT_SERVING_PATH)
    context.content_serving_uri = context.content_serving_uri.split("faq-resources/")[1]

    curriculum_req_body = copy(TEST_CURRICULUM_PATHWAY)
    for key in DEL_KEYS:
        if key in curriculum_req_body:
            del curriculum_req_body[key]
    curriculum_req_body["alias"] = "program"
    curriculum_url = f"{API_URL}/curriculum-pathway"
    curriculum_res = post_method(url=curriculum_url, request_body=curriculum_req_body)
    print(curriculum_res)
    curriculum_res_data = curriculum_res.json()
    context.curriculum_pathway_id = curriculum_res_data["data"]["uuid"]

    context.faq_content = {
                         **TEST_BASIC_FAQ,
                         "curriculum_pathway_id": context.curriculum_pathway_id,
                         "resource_path": context.content_serving_uri
                        }

    context.res = post_method(
        url=f"{API_URL}/faq", request_body=context.faq_content)
    context.res_json = context.res.json()

    assert context.res.status_code == 200
    assert context.res_json["success"] == True
    assert context.res_json["message"] == "Successfully Created FAQ"

    context.faq_uuid = context.res_json["data"]["uuid"]
    set_cache("faq_content_uuid", context.faq_uuid)

@behave.when("API request is sent to update the new FAQ with correct payload")
def step_impl_2(context):
    context.res = put_method(
        url=f"{API_URL}/faq/{context.faq_uuid}", request_body=context.faq_content)
    context.res_json = context.res.json()

@behave.then("the FAQ is successfully updated with correct payload")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_json["success"] == True
    assert context.res_json["message"] == "Successfully updated FAQ"

# -------------------------------------------------------------------------
# Scenario 7: User wants to update FAQ with incorrect payload
# -------------------------------------------------------------------------
@behave.given("that an LXE or CD wants to update a FAQ with incorrect payload")
def step_impl_1(context):
    context.faq_uuid = get_cache("faq_content_uuid")
    context.faq_content = {
        "resource_path": "random_resource_path"
    }

@behave.when("API request is sent to update the new FAQ with incorrect payload")
def step_impl_2(context):
    context.res = put_method(
        url=f"{API_URL}/faq/{context.faq_uuid}", request_body=context.faq_content)
    context.res_json = context.res.json()

@behave.then("the service returns error saying FAQ with incorrect payload")
def step_impl_3(context):
    assert context.res.status_code == 404
    assert context.res_json["success"] == False
    assert context.res_json["message"] == "Provided resource path does not exist on GCS bucket"

# -------------------------------------------------------------------------
# Scenario 8: User wants to delete FAQ with correct uuid
# -------------------------------------------------------------------------
@behave.given("that an LXE or CD wants to delete a FAQ with correct uuid")
def step_impl_1(context):
    context.faq_uuid = get_cache("faq_content_uuid")

@behave.when("API request is sent to delete the new FAQ with correct uuid")
def step_impl_2(context):
    context.res = delete_method(
        url=f"{API_URL}/faq/{context.faq_uuid}")
    context.res_json = context.res.json()

@behave.then("the FAQ is successfully deleted")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_json["success"] == True
    assert context.res_json["message"] == "Successfully deleted FAQ"

# -----------------------------------------------------
# Scenario 9: User wants to upload a faq file/zip with sync api
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to upload a faq file/zip with sync api")
def step_impl_1(context):
    pass

@behave.when("API request is sent to upload a faq file/zip with sync api")
def step_impl_2(context):
    content_file = open(TEST_CONTENT_SERVING_ZIP_PATH,"rb")
    content_file_input_dict = {"content_file":
              ("content_serving_sample_upload_zip.zip", content_file, "application/zip")}

    content_res = post_method(
            url=f"{API_URL_LEARNING_OBJECT_SERVICE}/content-serving/upload/sync",
            query_params = {"is_faq": True},
            files=content_file_input_dict,
            )
    context.res_json = content_res.json()
    context.status_code = content_res.status_code

@behave.then("LOS will return a json response with file and folder list of the uploaded faq file/zip")
def step_impl_3(context):
    assert context.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json["message"] == "Successfully uploaded the faq content"
    assert context.res_json["data"].get("prefix") is not None
    print(context.res_json)
    assert "faq-resources" in context.res_json["data"].get("prefix")