"""
Create, Read, Update and Delete learning object and learning experiences
"""

import behave
import uuid
import os
from copy import copy
from common.models import LearningExperience, LearningObject, LearningResource
import sys
sys.path.append("../")
from setup import post_method, get_method, put_method, delete_method
from test_config import API_URL_LEARNING_OBJECT_SERVICE, TESTING_OBJECTS_PATH, DEL_KEYS
from test_object_schemas import (TEST_LEARNING_OBJECT, TEST_LEARNING_EXPERIENCE, TEST_LEARNING_RESOURCE)


API_URL = API_URL_LEARNING_OBJECT_SERVICE
# ----------------------------- Creation (Positive) --------------------------------------

@behave.given("that a LXE or CD has access to the content authoring tool")
def step_1_1(context):
  context.req_body = copy(TEST_LEARNING_EXPERIENCE)
  for key in DEL_KEYS:
    if key in context.req_body:
      del context.req_body[key]
  context.url = f"{API_URL}/learning-experience"

@behave.when("they design the learning experience using a third party tool")
def step_1_2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()

@behave.then("the learning experiences will be created in a third-party tool")
def step_1_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert "uuid" in context.res_data["data"]
  assert "created_time" in context.res_data["data"]
  assert "last_modified_time" in context.res_data["data"]
  context.req_id = context.res_data["data"]["uuid"]

@behave.then("all metadata will be ingested and stored in learning object service")
def step_1_4(context):
  url = f"{API_URL}/learning-experience/{context.req_id}"
  res = get_method(url=url)
  context.get_data = res.json()
  assert res.status_code == 200
  assert context.get_data["data"]["display_name"] == context.req_body["display_name"]

@behave.then("uuid for learning experiences will be stored in learning object service")
def step_1_5(context):
  assert "uuid" in context.get_data["data"]
  assert context.get_data["data"]["uuid"] == context.req_id

# ---------------------------- Creation (Negative) --------------------------------------

@behave.given("that a LXE or CD has access to content authoring tool")
def step_2_1(context):
  context.req_body = copy(TEST_LEARNING_EXPERIENCE)
  context.req_body["title"] = "Title"
  context.url = f"{API_URL}/learning-experience"

@behave.when("they design the learning experience using a third party tool with invalid request")
def step_2_2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()

@behave.then("the learning experiences will not be created in learning object service")
def step_2_3(context):
  assert context.res.status_code == 422

# ---------------------------- Updation (Positive) --------------------------------------

@behave.given("that an LXE or CD has access to the content authoring tool")
def step_3_1_1(context):
  lx_dict = copy(TEST_LEARNING_EXPERIENCE)
  context.url = f"{API_URL}/learning-experience"
  for key in DEL_KEYS:
    if key in lx_dict:
      del lx_dict[key]
  context.res = post_method(url=context.url,request_body=lx_dict)
  context.res_data = context.res.json()
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  context.req_id = context.res_data["data"]["uuid"]


@behave.when("they update the learning experience using a third-party tool")
def step_3_1_2(context):
  lx_dict = copy(TEST_LEARNING_EXPERIENCE)
  lx_dict["name"] = "Kubernetes Platform"
  lx_dict["display_name"] = "Kubernetes Platform"
  lx_dict["description"] = "Kubernetes was developed by Google"
  for key in DEL_KEYS:
    if key in lx_dict:
      del lx_dict[key]
  context.request = lx_dict
  context.params = {"create_version": False}
  context.url = f"{API_URL}/learning-experience/{context.req_id}"
  context.res = put_method(url=context.url, query_params=context.params,
            request_body=lx_dict)
  context.res_data = context.res.json()

@behave.then("the learning experiences will be updated in a third-party tool")
def step_3_1_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.req_id
  assert context.res_data["data"]["name"] == "Kubernetes Platform"
  assert context.res_data["data"]["display_name"] == "Kubernetes Platform"
  assert context.res_data["data"]["description"] == "Kubernetes was developed by Google"
  assert context.res_data["data"]["is_archived"] == False


@behave.then("all metadata will be updated in learning object service")
def step_3_1_4(context):
  url = f"{API_URL}/learning-experience/{context.req_id}"
  res = get_method(url=url)
  context.get_data = res.json()
  assert res.status_code == 200
  assert context.get_data["data"]["metadata"] == context.request["metadata"]
  assert context.get_data["data"]["version"] == 1

# ---------------------------- Update and Create Version --------------------------------------

@behave.given("that an LXE or CD has access to the content authoring tool to create version of learning experience")
def step_3_2_1(context):
  lx_dict = copy(TEST_LEARNING_EXPERIENCE)
  for key in DEL_KEYS:
    if key in lx_dict:
      del lx_dict[key]
  context.url = f"{API_URL}/learning-experience"
  context.res = post_method(url=context.url,request_body=lx_dict)
  context.res_data = context.res.json()
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  context.req_id = context.res_data["data"]["uuid"]

@behave.when("they update the learning experience using a third-party tool to create version")
def step_3_2_2(context):
  lx_dict = copy(TEST_LEARNING_EXPERIENCE)
  lx_dict["name"] = "Online Platform"
  lx_dict["display_name"] = "Online Platform"
  lx_dict["description"] = "Online Platform was developed by Google"
  for key in DEL_KEYS:
    if key in lx_dict:
      del lx_dict[key]
  context.request = lx_dict
  context.params = {"create_version": True}
  context.url = f"{API_URL}/learning-experience/{context.req_id}"
  context.res = put_method(url=context.url, query_params=context.params,
              request_body=lx_dict)
  context.res_data = context.res.json()
  context.updated_doc_id = context.res_data["data"]["uuid"]

@behave.then("a version of learning experience will be created")
def step_3_2_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["name"] == "Online Platform"
  assert context.res_data["data"]["display_name"] == "Online Platform"
  assert context.res_data["data"]["parent_version_uuid"] == context.req_id

@behave.then("all metadata for the learning experience will be updated learning object service")
def step_3_2_4(context):
  url = f"{API_URL}/learning-experience/{context.req_id}"
  res = get_method(url=url)
  context.get_data = res.json()
  assert res.status_code == 200
  assert context.get_data["data"]["metadata"] == context.request["metadata"]

@behave.then("a version document for the learning experience will be created in learing object service")
def step_3_2_5(context):
  url = f"{API_URL}/learning-experience/{context.req_id}"
  res = get_method(url=url)
  context.get_data = res.json()
  assert res.status_code == 200
  assert context.res_data["data"]["version"] != 1
  assert context.res_data["data"]["uuid"] != context.req_id

# ---------------------------- Updation (Negative 1) --------------------------------------

@behave.given("that an LXE or CD has access to content authoring tool")
def step_4_1(context):
  lx_dict = copy(TEST_LEARNING_EXPERIENCE)
  for key in DEL_KEYS:
    if key in lx_dict:
      del lx_dict[key]
  context.url = f"{API_URL}/learning-experience"
  context.res = post_method(url=context.url,request_body=lx_dict)
  context.res_data = context.res.json()
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  context.req_id = context.res_data["data"]["uuid"]

@behave.when("they update the learning experience using a third-party tool with invalid uuid")
def step_4_2(context):
  context.req_id = str(uuid.uuid4())
  lx_dict = copy(TEST_LEARNING_EXPERIENCE)
  lx_dict["name"] = "Kubernetes Platform"
  lx_dict["display_name"] = "Kubernetes Platform"
  lx_dict["description"] = "Kubernetes was developed by Google"
  for key in DEL_KEYS:
    if key in lx_dict:
      del lx_dict[key]
  context.url = f"{API_URL}/learning-experience/{context.req_id}"
  context.res = put_method(url=context.url, request_body=lx_dict)
  context.res_data = context.res.json()

@behave.then("the learning experiences will not be updated in learning object service")
def step_4_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data["message"] == f"Learning Experience with uuid {context.req_id} not found"

# ---------------------------- Updation (Negative 2) --------------------------------------

@behave.given("that a LXE has access to content authoring tool")
def step_5_1(context):
  lx_dict = copy(TEST_LEARNING_EXPERIENCE)
  for key in DEL_KEYS:
    if key in lx_dict:
      del lx_dict[key]
  context.url = f"{API_URL}/learning-experience"
  context.res = post_method(url=context.url,request_body=lx_dict)
  context.res_data = context.res.json()
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  context.req_id = context.res_data["data"]["uuid"]

@behave.when("they update the learning experience using a third-party tool with invalid request")
def step_5_2(context):
  lx_dict = copy(TEST_LEARNING_EXPERIENCE)
  lx_dict["title"] = "Kubernetes was developed by Google"
  for key in DEL_KEYS:
    if key in lx_dict:
      del lx_dict[key]
  context.url = f"{API_URL}/learning-experience/{context.req_id}"
  context.res = put_method(url=context.url, request_body=lx_dict)
  context.res_data = context.res.json()

@behave.then("the learning experience will not be updated in learning object service")
def step_5_3(context):
  assert context.res.status_code == 422

# ---------------------------- Deletion (Positive) --------------------------------------

@behave.given("that an LXE has access to content authoring tool")
def step_6_1(context):
  lx_dict = copy(TEST_LEARNING_EXPERIENCE)
  for key in DEL_KEYS:
    if key in lx_dict:
      del lx_dict[key]
  context.url = f"{API_URL}/learning-experience"
  context.res = post_method(url=context.url,request_body=lx_dict)
  context.res_data = context.res.json()
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  context.req_id = context.res_data["data"]["uuid"]

@behave.when("they delete the learning experience using a third-party tool")
def step_6_2(context):
  context.url = f"{API_URL}/learning-experience/{context.req_id}"
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("the learning experiences will be deleted from a third-party tool")
def step_6_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["message"] == "Successfully deleted the learning experience"

  learning_experience = LearningExperience.find_by_uuid(context.req_id, is_deleted=True)
  assert learning_experience.uuid == context.req_id

@behave.then("all metadata will be deleted from learning object service")
def step_6_4(context):
  url = f"{API_URL}/learning-experience/{context.req_id}"
  res = get_method(url=url)
  context.get_data = res.json()
  assert res.status_code == 404
  assert context.get_data["message"] == f"Learning Experience with uuid {context.req_id} not found"

# ---------------------------- Deletion (Negative) --------------------------------------

@behave.given("that an LXE has access to the content authoring tool")
def step_7_1(context):
  lx_dict = copy(TEST_LEARNING_EXPERIENCE)
  for key in DEL_KEYS:
    if key in lx_dict:
      del lx_dict[key]
  context.url = f"{API_URL}/learning-experience"
  context.res = post_method(url=context.url,request_body=lx_dict)
  context.res_data = context.res.json()
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  context.req_id = context.res_data["data"]["uuid"]

@behave.when("they delete the learning experience using a third-party tool wiht incorrect uuid")
def step_7_2(context):
  context.req_id = str(uuid.uuid4())
  context.url = f"{API_URL}/learning-experience/{context.req_id}"
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("the learning experiences will not be deleted from learning object service")
def step_7_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data["message"] == f"Learning Experience with uuid {context.req_id} not found"

# ---------------------------- Ingestion (Positive) --------------------------------------

@behave.given("that an CD or LXE has access to the content authoring tool")
def step_8_1(context):
  context.url = f"{API_URL}/learning-experience/import/json"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH,
                                        "learning_experiences.json")
  assert os.path.exists(context.json_file_path)

@behave.when("Learning Experience JSON data with correct payload request is imported")
def step_8_2(context):
  with open(context.json_file_path, encoding="UTF-8") as lx_json_file:
    context.res = post_method(context.url, files={"json_file": lx_json_file})
    context.res_data = context.res.json()

@behave.then("That Learning Experience JSON data should be ingested into learning object service")
def step_8_3(context):
  assert context.res.status_code == 200, "Status not 200"
  assert isinstance(context.res_data.get("data"), list), "Response is not a list"
  assert len(
      context.res_data.get("data")) > 0, "Empty list returned in import json api"
  inserted_lx_uuids = context.res_data.get("data")
  api_url = f"{API_URL}/learning-experiences"
  params = {"skip": 0, "limit": 30}
  resp = get_method(api_url, query_params=params)
  resp_data = resp.json()
  assert resp.status_code == 200, "Status not 200"
  lx_uuids = [i.get("uuid") for i in resp_data.get("data")]
  assert set(inserted_lx_uuids).intersection(set(lx_uuids)) \
    == set(inserted_lx_uuids), "all data not retrieved"

# ---------------------------- Ingestion (Negative) --------------------------------------

@behave.given("that a CD or LXE has access to the content authoring tool")
def step_9_1(context):
  context.url = f"{API_URL}/learning-experience/import/json"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH,
                                        "learning_experiences_invalid.json")
  context.required_fields = "'name'"
  assert os.path.exists(context.json_file_path)

@behave.when("Learning Experience JSON data with incorrect payload request is imported")
def step_9_2(context):
  with open(context.json_file_path, encoding="UTF-8") as lx_json_file:
    context.res = post_method(context.url, files={"json_file": lx_json_file})
    context.res_data = context.res.json()

@behave.then("ingestion of Learning Experience JSON data into learning object service should fail")
def step_9_3(context):
  # JSON file without required fields
  assert context.res.status_code == 422, "Status should be 422 if required fields are missing"
  assert context.res_data.get(
      "message") == f"Missing required fields - {context.required_fields}", "Expected response message is not same"

#CREATE POSITIVE---------------------------------------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool for creation of learning object with correct payload")
def step_impl_1(context):
    context.payload = TEST_LEARNING_OBJECT
    context.url= f"{API_URL}/learning-object"
    for key in DEL_KEYS:
      if key in context.payload:
        del context.payload[key]

@behave.when("they design the learning object using a third party content authoring tool with correct payload")
def step_impl_2(context):
     context.res = post_method(url=context.url, request_body=context.payload)
     context.res_data = context.res.json()

@behave.then("the learning object and their components will be created in the learning object service with correct payload")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_data["message"] == "Successfully created the learning object"
    context.uuid = context.res_data["data"]["uuid"]

@behave.then("all the associated metadata will will be created in learning object service")
def step_impl_4(context):
    get_url = f"{API_URL}/learning-object/{context.uuid}"
    context.response = get_method(url = get_url)
    context.result = context.response.json()
    assert context.result["data"]["name"] == "Online presentation"
    assert context.result["data"]["display_name"] == "Online presentation"
    assert context.result["data"]["description"] == "Details on ppt"
    assert context.result["data"]["metadata"] == {"design_config":{"theme": "blue", "illustration": "U1C1"}}
    

@behave.then("Unique IDs for learning objects will be stored in learning object service")
def step_impl_5(context):
    check_url = f"{API_URL}/learning-object/{context.uuid}"
    context.check = get_method(url = check_url)
    context.check_data = context.check.json()
    assert context.uuid == context.check_data.get("data").get("uuid")
    #tear down part
    LearningObject.delete_by_id(context.uuid)

#CREATE NEAGTIVE-------------------------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool for creation of learning object with incorrect payload")
def step_impl_1(context):
    WRONG_TEMPLATE = TEST_LEARNING_OBJECT.copy()
    del WRONG_TEMPLATE["name"]
    context.payload = WRONG_TEMPLATE
    context.url= f"{API_URL}/learning-object"

@behave.when("they design the learning object using a third party content authoring tool with incorrect payload")
def step_impl_2(context):
     context.res = post_method(url=context.url, request_body=context.payload)
     context.res_data = context.res.json()

@behave.then("the learning object and their components will not be created in the learning object service")
def step_impl_3(context):
    assert context.res.status_code == 422

@behave.then("the user gets an error message for create")
def step_impl_4(context):
    assert context.res_data["data"][0]["msg"] == "field required"


#UPDATE POSITIVE---------------------------------------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool for updation of learning object with correct payload")
def step_impl_1(context):
    LTEMP = TEST_LEARNING_OBJECT.copy()
    context.learning_object_dict = LTEMP
    context.url = f"{API_URL}/learning-object"
    context.res = post_method(url=context.url,request_body=LTEMP)
    context.res_data = context.res.json()
    assert context.res.status_code == 200
    assert context.res_data["success"] is True
    context.uuid = context.learning_object_dict["uuid"] = context.res_data["data"]["uuid"]
    context.url = f"{API_URL}/learning-object/{context.uuid}"

@behave.when("they updated the design of the learning object using a third party content authoring tool with correct payload")
def step_impl_2(context):
    updated_data = context.learning_object_dict
    updated_data["name"] = "Imagination"
    updated_data["display_name"] = "Imagination"
    updated_data["metadata"] = {"design_config": {"theme": "red", "illustration": "U1C2"}}
    for key in DEL_KEYS:
      if key in updated_data:
        del updated_data[key]
    context.params = {"create_version": False}
    context.resp = put_method(url = context.url,
      query_params=context.params, request_body = updated_data)
    context.resp_data = context.resp.json()

@behave.then("the learning object and their components will be updated in the learning object service with correct payload")
def step_impl_3(context):
    assert context.resp.status_code == 200
    assert context.resp_data.get("success") is True

@behave.then("all the associated metadata will will be updated in learning object service")
def step_impl_4(context):
    assert context.resp_data["data"]["name"] == "Imagination"
    assert context.resp_data["data"]["display_name"] == "Imagination"
    assert context.resp_data["data"]["description"] == "Details on ppt"
    assert context.resp_data["data"]["metadata"] == {"design_config":{"theme": "red", "illustration": "U1C2"}}

@behave.then("Unique IDs for the updated learning objects will be stored in learning object service")
def step_impl_5(context):
    check_url = f"{API_URL}/learning-object/{context.uuid}"
    context.check = get_method(url = check_url)
    context.check_data = context.check.json()
    assert context.check_data["data"]["uuid"]  == context.uuid

    #tear down part
    LearningObject.delete_by_id(context.uuid)

#UPDATE and Create Version POSITIVE---------------------------------------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool to create version of learning object")
def step_impl_1(context):
    LTEMP = TEST_LEARNING_OBJECT.copy()
    context.learning_object_dict = LTEMP
    context.url = f"{API_URL}/learning-object"
    context.res = post_method(url=context.url,request_body=LTEMP)
    context.res_data = context.res.json()
    assert context.res.status_code == 200
    assert context.res_data["success"] is True
    context.uuid = context.learning_object_dict["uuid"] = context.res_data["data"]["uuid"]
    context.url = f"{API_URL}/learning-object/{context.uuid}"

@behave.when("they update the learning object using a third-party tool to create version")
def step_impl_2(context):
    updated_data = context.learning_object_dict
    updated_data["name"] = "Culmination"
    updated_data["display_name"] = "Culmination"
    updated_data["metadata"] = {"design_config":{"theme": "red", "illustration": "U1C2"}}
    for key in DEL_KEYS:
      if key in updated_data:
        del updated_data[key]
    context.params = {"create_version": True}
    context.resp = put_method(url = context.url, query_params=context.params,
      request_body = updated_data)
    context.resp_data = context.resp.json()
    context.updated_doc_id = context.resp_data["data"]["uuid"]

@behave.then("a version of learning object will be created")
def step_impl_3(context):
    assert context.resp.status_code == 200
    assert context.resp_data.get("success") is True

@behave.then("all metadata for the learning object will be updated in learning object service")
def step_impl_4(context):
    assert context.resp_data["data"]["name"] == "Culmination"
    assert context.resp_data["data"]["display_name"] == "Culmination"
    assert context.resp_data["data"]["description"] == "Details on ppt"
    assert context.resp_data["data"]["metadata"] == {"design_config": {"theme": "red", "illustration": "U1C2"}}

@behave.then("a version for the learning object document will be created in learing object service")
def step_impl_5(context):
    check_url = f"{API_URL}/learning-object/{context.updated_doc_id}"
    context.check = get_method(url = check_url)
    context.check_data = context.check.json()
    assert context.check_data["data"]["uuid"] != context.uuid
    assert context.check_data["data"]["version"] != 1
    #tear down part
    LearningObject.delete_by_id(context.uuid)

#UPDATE NEGATIVE---------------------------------------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool for updation of learning object with incorrect payload")
def step_impl_1(context):
    WRONG_TEMPLATE = TEST_LEARNING_OBJECT.copy()
    context.learning_object_dict = WRONG_TEMPLATE
    context.url = f"{API_URL}/learning-object"
    context.res = post_method(url=context.url,request_body=WRONG_TEMPLATE)
    context.res_data = context.res.json()
    assert context.res.status_code == 200
    assert context.res_data["success"] is True
    context.uuid = context.learning_object_dict["uuid"] = context.res_data["data"]["uuid"]

    context.url = f"{API_URL}/learning-object/{context.uuid}"

@behave.when("they updated the design of the learning object using a third party content authoring tool with incorrect payload")
def step_impl_2(context):
    updated_data = context.learning_object_dict
    wrong_update = updated_data.copy()
    del wrong_update["name"]
    updated_data["description"] = "Imagination and description"
    updated_data["is_archived"] = False
    context.resp = put_method(url = context.url, request_body = wrong_update)
    context.resp_data = context.resp.json()

@behave.then("the learning object and their components will not be updated in the learning object service")
def step_impl_3(context):
    assert context.resp.status_code == 422

@behave.then("the user will get an error message for update")
def step_impl_4(context):
    assert context.resp_data["data"][0]["msg"] == "extra fields not permitted"
    #tear down part
    LearningObject.delete_by_id(context.uuid)

#DELETE POSITIVE -------------------------------------------------------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool for deletion of learning object with correct payload")
def step_impl_1(context):
    context.payload = TEST_LEARNING_OBJECT
    context.url= f"{API_URL}/learning-object"
    context.res_data = post_method(url=context.url, request_body=context.payload)
    context.res_data = context.res_data.json()
    context.uuid = context.res_data["data"]["uuid"]

    lo_2 = copy(TEST_LEARNING_OBJECT)
    lo_2["prerequisites"] = {}
    lo_2["prerequisites"]["learning_objects"] = [context.uuid]
    res_data_2 = post_method(url=context.url, request_body=lo_2)
    res_data_2 = res_data_2.json()
    context.lo_2_uuid = res_data_2["data"]["uuid"]

@behave.when("they delete the learning object using a third party content authoring tool with correct payload")
def step_impl_2(context):
    id = context.uuid
    context.url= f"{API_URL}/learning-object/{id}"
    context.res = delete_method(url=context.url)
    context.res_data = context.res.json()

@behave.then("the learning object and their components will be deleted in the learning object service with correct payload")
def step_impl_3(context):
    assert context.res_data["success"] is True
    assert context.res_data["message"] == "Successfully deleted the learning object"

    learning_object = LearningObject.find_by_uuid(context.uuid, is_deleted=True)
    assert learning_object.uuid == context.uuid

@behave.then("all the associated metadata will will be deleted in learning object service")
def step_impl_4(context):
    uuid = context.uuid
    geturl = f"{API_URL}/learning-object/{uuid}"
    context.res = get_method(url = geturl)
    context.resdata = context.res.json()
    msg = f"Learning Object with uuid {uuid} not found"
    assert context.resdata["success"] is False
    assert context.resdata["message"] == msg

    # check if deleted LO is removed from other LO's prerequisites
    geturl2 = f"{API_URL}/learning-object/{context.lo_2_uuid}"
    resp_2 = get_method(url=geturl2)
    resp_data_2 = resp_2.json()
    assert context.uuid not in resp_data_2["data"]["prerequisites"]["learning_objects"]


#DELETE NEGATIVE -------------------------------------------------------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool for deletion of learning object with incorrect payload")
def step_impl_1(context):
    context.learning_object_dict = TEST_LEARNING_OBJECT
    context.url = f"{API_URL}/learning-object"
    context.res = post_method(url=context.url,request_body=context.learning_object_dict)
    context.res_data = context.res.json()
    assert context.res.status_code == 200
    assert context.res_data["success"] is True
    context.uuid = context.learning_object_dict["uuid"] = context.res_data["data"]["uuid"]
    context.uuid =  context.learning_object_dict["uuid"]

@behave.when("they delete the learning object using a third party content authoring tool with incorrect payload")
def step_impl_2(context):
    id = "random-id"
    context.url= f"{API_URL}/learning-object/{id}"
    context.res = delete_method(url=context.url)
    context.res_data = context.res.json()

@behave.then("the learning object and their components will not be deleted in the learning object service")
def step_impl_3(context):
    assert context.res.status_code == 404

@behave.then("the user will get an error message")
def step_impl_4(context):
    assert context.res_data["success"] is False
    msg = f"Learning Object with uuid random-id not found"
    assert context.res_data["message"] == msg
    #tear down part
    LearningObject.delete_by_id(context.uuid)

#CREATE POSITVE FROM JSON----------------------------------------------------------------------------
@behave.given("that an CD or LXE has access to the content authoring tool with correct request payload")
def step_8_1(context):
  context.url = f"{API_URL}/learning-object/import/json"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH,
                                        "learning_objects.json")

@behave.when("Learning object JSON data with correct payload request is imported")
def step_8_2(context):
  with open(context.json_file_path, encoding="UTF-8") as lo_json_file:
    context.res = post_method(context.url, files={"json_file": lo_json_file})
    context.res_data = context.res.json()

@behave.then("That Learning object JSON data should be ingested into learning object service")
def step_8_3(context):
  assert context.res.status_code == 200
  assert isinstance(context.res_data.get("data"), list)
  assert len(context.res_data.get("data")) > 0
  inserted_lo_uuids = context.res_data.get("data")
  api_url = f"{API_URL}/learning-objects"
  params = {"skip": 0, "limit": 30}

  resp = get_method(api_url, query_params=params)
  resp_data = resp.json()
  assert resp.status_code == 200
  lo_uuids = [i.get("uuid") for i in resp_data.get("data")]
  assert set(inserted_lo_uuids).intersection(set(lo_uuids)) == set(inserted_lo_uuids)

#CREATE NEGATIVE FROM JSON----------------------------------------------------------------------------
@behave.given("that an CD or LXE has access to the content authoring tool with incorrect request payload")
def step_9_1(context):
  context.url = f"{API_URL}/learning-object/import/json"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH,
                                        "learning_objects_invalid.json")
  context.required_fields = "'name'"
  assert os.path.exists(context.json_file_path)

@behave.when("Learning object JSON data with incorrect payload request is not imported")
def step_9_2(context):
  with open(context.json_file_path, encoding="UTF-8") as lo_json_file:
    context.res = post_method(context.url, files={"json_file": lo_json_file})
    context.res_data = context.res.json()

@behave.then("That user gets an error message")
def step_9_3(context):
  # JSON file without required fields
  assert context.res.status_code == 422
  assert context.res_data.get(
      "message") == f"Missing required fields - {context.required_fields}"


#CREATE LR POSITIVE---------------------------------------------------------------------------------
@behave.given("that a LXE or CD has access to the content authoring tool for creating LR")
def step_impl_1(context):
    context.payload = TEST_LEARNING_RESOURCE
    for key in DEL_KEYS:
      if key in context.payload:
        del context.payload[key]
    context.url= f"{API_URL}/learning-resource"

@behave.when("they design the learning resource using a third party tool")
def step_impl_2(context):
    context.res = post_method(url=context.url, request_body=context.payload)
    context.res_data = context.res.json()

@behave.then("the learning resource will be created in a third-party tool")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_data["message"] == "Successfully created the learning resource"
    context.uuid = context.res_data["data"]["uuid"]

@behave.then("all LR metadata will be ingested and stored in learning object service")
def step_impl_4(context):
    get_url = f"{API_URL}/learning-resource/{context.uuid}"
    context.response = get_method(url = get_url)
    context.result = context.response.json()
    assert context.result["data"]["name"] == TEST_LEARNING_RESOURCE["name"]
    assert context.result["data"]["display_name"] == TEST_LEARNING_RESOURCE["display_name"]
    assert context.result["data"]["description"] == TEST_LEARNING_RESOURCE["description"]
    assert context.result["data"]["metadata"] == TEST_LEARNING_RESOURCE["metadata"]

@behave.then("Unique IDs for learning resources will be stored in learning object service")
def step_impl_5(context):
  check_url = f"{API_URL}/learning-resources"
  params = {"skip": 0, "limit": 30}
  context.check = get_method(url = check_url, query_params=params)
  context.check_data = context.check.json()
  uuids = [obj["uuid"] for obj in context.check_data["data"]]
  assert context.uuid in uuids

  #tear down part
  LearningObject.delete_by_id(context.uuid)

#CREATE LR NEAGTIVE-------------------------------------------------------------------
@behave.given("that a LXE or CD has access to content authoring tool with incorrect LR payload")
def step_impl_1(context):
    WRONG_TEMPLATE = TEST_LEARNING_RESOURCE.copy()
    del WRONG_TEMPLATE["name"]
    context.payload = WRONG_TEMPLATE
    context.url= f"{API_URL}/learning-resource"

@behave.when("they design the learning resource using a third party tool with invalid request")
def step_impl_2(context):
     context.res = post_method(url=context.url, request_body=context.payload)
     context.res_data = context.res.json()

@behave.then("the learning resource will not be created in learning object service")
def step_impl_3(context):
    assert context.res.status_code == 422

@behave.then("the user gets an error message for LR create")
def step_impl_4(context):
    assert context.res_data["data"][0]["msg"] == "field required"
#---------------------------------------------------------------------------------------------------------------

#UPDATE LR POSITIVE---------------------------------------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool for updation of learning resource with correct payload")
def step_impl_1(context):
    LRTEMP = TEST_LEARNING_RESOURCE.copy()
    context.learning_resource_dict = LRTEMP
    for key in DEL_KEYS:
      if key in context.learning_resource_dict:
        del context.learning_resource_dict[key]
    context.url = f"{API_URL}/learning-resource"
    context.res = post_method(url=context.url, request_body=LRTEMP)
    context.res_data = context.res.json()
    context.learning_resource_dict["uuid"] = context.res_data["data"]["uuid"]
    context.uuid = context.res_data["data"]["uuid"]
    

@behave.when("they updated the learning resource using a third party content authoring tool with correct payload")
def step_impl_2(context):
    context.updated_data = context.learning_resource_dict
    context.updated_data["name"] = "Updated Name"
    context.updated_data["display_name"] = "Updated Name"
    context.updated_data["metadata"] = {"design_config": {"theme": "red", "illustration": "U1C2"}}
    for key in DEL_KEYS:
      if key in context.updated_data:
        del context.updated_data[key]
    context.resp = put_method(url = f"{context.url}/{context.uuid}",
      request_body = context.updated_data)
    context.resp_data = context.resp.json()

@behave.then("the learning resource and their components will be updated in the learning object service with correct payload")
def step_impl_3(context):
    assert context.resp.status_code == 200
    assert context.resp_data.get("success") is True

@behave.then("all the learning resource associated metadata will will be updated in learning object service")
def step_impl_4(context):
    assert context.resp_data["data"]["name"] == context.updated_data["name"]
    assert context.resp_data["data"]["display_name"] == context.updated_data["display_name"]
    assert context.resp_data["data"]["description"] == context.updated_data["description"]
    assert context.resp_data["data"]["metadata"] == context.updated_data["metadata"]

@behave.then("Unique IDs for the updated learning resource will be stored in learning object service")
def step_impl_5(context):
    check_url = f"{API_URL}/learning-resources"
    params = {"skip": 0, "limit": 30}
    context.check = get_method(url = check_url, query_params=params)
    context.check_data = context.check.json()
    uuids = [obj["uuid"] for obj in context.check_data["data"]]
    assert context.uuid in uuids

    #tear down part
    LearningResource.delete_by_id(context.uuid)

#UPDATE LR and CREATE VERSION-----------------------------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool to create version of learning resource")
def step_1(context):
  LRTEMP = TEST_LEARNING_RESOURCE.copy()
  context.learning_resource_dict = LRTEMP
  for key in DEL_KEYS:
    if key in context.learning_resource_dict:
      del context.learning_resource_dict[key]
  context.url = f"{API_URL}/learning-resource"
  context.res = post_method(url=context.url, request_body=LRTEMP)
  context.res_data = context.res.json()
  context.learning_resource_dict["uuid"] = context.res_data["data"]["uuid"]
  context.uuid = context.res_data["data"]["uuid"]

@behave.when("they update the learning resource using a third-party tool to create version")
def step_2(context):
  context.updated_data = context.learning_resource_dict
  context.updated_data["name"] = "Updated Name"
  context.updated_data["display_name"] = "Updated Name"
  context.updated_data["metadata"] = {"design_config": {"theme": "red", "illustration": "U1C2"}}
  for key in DEL_KEYS:
      if key in context.updated_data:
        del context.updated_data[key]
  context.params = {"create_version": True}
  context.url = f"{API_URL}/learning-resource/{context.uuid}"
  context.resp = put_method(url=context.url,
      request_body=context.updated_data, query_params=context.params)
  context.version_data = context.resp.json()
  context.updated_doc_id = context.version_data["data"]["uuid"]

@behave.then("a version of learning resource will be created")
def step_3(context):
  assert context.res.status_code == 200
  assert context.version_data["success"] is True
  assert context.version_data["data"]["name"] == "Updated Name"
  assert context.version_data["data"]["display_name"] == "Updated Name"
  assert context.version_data["data"]["parent_version_uuid"] == context.uuid

@behave.then("all metadata for the learning resource will be updated learning object service")
def step_4(context):
  url = f"{API_URL}/learning-resource/{context.updated_doc_id}"
  res = get_method(url=url)
  context.get_data = res.json()
  assert res.status_code == 200
  assert context.get_data["data"]["metadata"] == \
    context.version_data["data"]["metadata"]

@behave.then("a version document for the learning resource will be created in learing object service")
def step_5(context):
  assert context.get_data["data"]["version"] != 1
  assert context.get_data["data"]["uuid"] != context.uuid

#UPDATE LR NEGATIVE---------------------------------------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool for updation of learning resource with incorrect payload")
def step_impl_1(context):
    WRONG_LR_TEMPLATE = TEST_LEARNING_RESOURCE.copy()
    context.learning_resource_dict = WRONG_LR_TEMPLATE
    context.url = f"{API_URL}/learning-resource"
    for key in DEL_KEYS:
      if key in context.learning_resource_dict:
        del context.learning_resource_dict[key]
    context.res = post_method(url=context.url, request_body=WRONG_LR_TEMPLATE)
    context.res_data = context.res.json()
    context.learning_resource_dict["uuid"] = context.res_data["data"]["uuid"]
    context.uuid = context.res_data["data"]["uuid"]

@behave.when("they updated the learning resource using a third party content authoring tool with incorrect payload")
def step_impl_2(context):
    wrong_LR_update = context.learning_resource_dict
    for key in DEL_KEYS:
      if key in wrong_LR_update:
        del wrong_LR_update[key]
    wrong_LR_update["title"] = "New description description"
    context.resp = put_method(url = f"{context.url}/{context.uuid}",
    request_body = wrong_LR_update)
    context.resp_data = context.resp.json()

@behave.then("the learning resource and their components will not be updated in the learning object service")
def step_impl_3(context):
    assert context.resp.status_code == 422

@behave.then("the user will get an error message for Learning resource update")
def step_impl_4(context):
    assert context.resp_data["data"][0]["msg"] == "extra fields not permitted"
    #tear down part
    LearningResource.delete_by_id(context.uuid)


@behave.given("that an LXE or CD has access to content authoring tool to update the learning resource")
def step_impl_1(context):
    LR_TEMPLATE = TEST_LEARNING_RESOURCE.copy()
    context.learning_resource_dict = LR_TEMPLATE
    context.url = f"{API_URL}/learning-resource"
    for key in DEL_KEYS:
      if key in context.learning_resource_dict:
        del context.learning_resource_dict[key]
    context.res = post_method(url=context.url,
      request_body=context.learning_resource_dict)
    context.res_data = context.res.json()
    context.learning_resource_dict["uuid"] = context.res_data["data"]["uuid"]
    context.uuid = context.res_data["data"]["uuid"]


@behave.when("they update the learning resource using a third-party tool with invalid uuid")
def step_impl_2(context):
    context.updated_data = context.learning_resource_dict
    context.updated_data["name"] = "Updated Name"
    context.updated_data["display_name"] = "Updated Name"
    context.updated_data["metadata"] = {"design_config": {"theme": "red", "illustration": "U1C2"}}
    del context.updated_data["uuid"]
    context.resp = put_method(url = f"{context.url}/random-id",
    request_body = context.updated_data)
    context.resp_data = context.resp.json()

@behave.then("the learning resource will not be updated in learning object service")
def step_impl_3(context):
    assert context.resp.status_code == 404

@behave.then("the user will get an error message for invalid uuid for Learning Resource update")
def step_impl_4(context):
    assert context.resp_data["success"] is False
    msg = "Learning Resource with uuid random-id not found"
    assert context.resp_data["message"] == msg
    #tear down part
    LearningObject.delete_by_id(context.uuid)

#LR DELETE POSTIVE-------------------

@behave.given("that an LXE has access to content authoring tool for deleting LR")
def step_impl_1(context):
    context.payload = TEST_LEARNING_RESOURCE
    context.url= f"{API_URL}/learning-resource"
    context.res_data = post_method(url=context.url, request_body=context.payload)
    context.res_data = context.res_data.json()
    context.uuid = context.res_data["data"]["uuid"]

@behave.when("they delete the learning resource using a third-party tool")
def step_impl_2(context):
    id = context.uuid
    context.url= f"{API_URL}/learning-resource/{id}"
    context.res = delete_method(url=context.url)
    context.res_data = context.res.json()

@behave.then("the learning resources will be deleted from a third-party tool")
def step_impl_3(context):
    assert context.res_data["success"] is True
    assert context.res_data["message"] == "Successfully deleted the learning resource"

    learning_resource = LearningResource.find_by_uuid(context.uuid, is_deleted=True)
    assert learning_resource.uuid == context.uuid

@behave.then("all LR associated metadata will be deleted from learning object service")
def step_impl_4(context):
    uuid = context.uuid
    geturl = f"{API_URL}/learning-resource/{uuid}"
    context.res = get_method(url = geturl)
    context.resdata = context.res.json()
    assert context.resdata["success"] is False

#LR DELETE NEGATIVE -------------------------------------------------------------------------------------------------
@behave.given("that an LXE has access to the content authoring tool for deletion with an incorrect LR payload")
def step_impl_1(context):
    context.learning_object_dict = TEST_LEARNING_RESOURCE
    context.url = f"{API_URL}/learning-resource"
    context.res = post_method(url=context.url,request_body=context.learning_object_dict)
    context.res_data = context.res.json()
    assert context.res.status_code == 200
    assert context.res_data["success"] is True
    context.uuid = context.learning_object_dict["uuid"] = context.res_data["data"]["uuid"]

@behave.when("they delete the learning resource using a third-party tool with incorrect uuid")
def step_impl_2(context):
    id = "random-id"
    context.url= f"{API_URL}/learning-resource/{id}"
    context.res = delete_method(url=context.url)
    context.res_data = context.res.json()

@behave.then("the learning resource will not be deleted from learning object service")
def step_impl_3(context):
    assert context.res.status_code == 404

@behave.then("the user will get an error message for incorrect LR delete request")
def step_impl_4(context):
    assert context.res_data["success"] is False
    msg = "Learning Resource with uuid random-id not found"
    assert context.res_data["message"] == msg
    #tear down part
    LearningObject.delete_by_id(context.uuid)

#CREATE POSITVE LR FROM JSON----------------------------------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool with correct Learning Resource request payload")
def step_8_1(context):
  context.url = f"{API_URL}/learning-resource/import/json"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH,
                                        "los_learning_resources.json")

@behave.when("Learning resource JSON data with correct payload request is imported")
def step_8_2(context):
  with open(context.json_file_path, encoding="UTF-8") as lr_json_file:
    context.res = post_method(context.url, files={"json_file": lr_json_file})
    context.res_data = context.res.json()

@behave.then("That Learning resoruce JSON data should be ingested into learning object service")
def step_8_3(context):
  assert context.res.status_code == 200
  assert isinstance(context.res_data.get("data"), list)
  assert len(context.res_data.get("data")) > 0
  inserted_lr_uuids = context.res_data.get("data")
  api_url = f"{API_URL}/learning-resources"
  params = {"skip": 0, "limit": 30}

  resp = get_method(api_url, query_params=params)
  assert resp.status_code == 200
  resp_data = resp.json()
  lr_uuids = [i.get("uuid") for i in resp_data.get("data")]
  assert set(inserted_lr_uuids).intersection(set(lr_uuids)) == set(inserted_lr_uuids)

#CREATE NEGATIVE LR FROM JSON----------------------------------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool with incorrect Learning resource request payload")
def step_9_1(context):
  context.url = f"{API_URL}/learning-resource/import/json"
  context.json_file_path = os.path.join(TESTING_OBJECTS_PATH,
                                        "los_learning_resources_invalid.json")
  context.required_fields = "'name'"
  assert os.path.exists(context.json_file_path)

@behave.when("Learning resource JSON data with incorrect payload request is not imported")
def step_9_2(context):
  with open(context.json_file_path, encoding="UTF-8") as lr_json_file:
    context.res = post_method(context.url, files={"json_file": lr_json_file})
    context.res_data = context.res.json()

@behave.then("That user gets an error message for Learning Resrouce")
def step_9_3(context):
  # JSON file without required fields
  assert context.res.status_code == 422
  assert context.res_data["success"] == False
  assert context.res_data.get(
      "message") == f"Missing required fields - {context.required_fields}"
