"""
    User should be able to link valid madcap htm file against a learning resource
"""
import behave
import sys
from copy import copy

sys.path.append("../")
from common.utils.gcs_adapter import GcsCrudService
from setup import post_method, get_method, get_cache, set_cache, CONTENT_SERVING_BUCKET
from environment import TEST_CONTENT_SERVING_PATH, TEST_CONTENT_SERVING_MADCAP_V1_PATH, TEST_CONTENT_SERVING_MADCAP_V2_PATH
from test_config import API_URL_LEARNING_OBJECT_SERVICE, DEL_KEYS
from test_object_schemas import (TEST_LEARNING_OBJECT, TEST_LEARNING_EXPERIENCE, TEST_LEARNING_RESOURCE)

API_URL = API_URL_LEARNING_OBJECT_SERVICE
LEARNING_RESOURCE_UUID=""
# -----------------------------------------------------
# Scenario 1: User wants to be able to link valid madcap htm file against a learning resource
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to link valid madcap htm file against a learning resource")
def step_impl_1(context):
    context.req_body = copy(TEST_LEARNING_EXPERIENCE)
    context.url = f"{API_URL}/learning-experience"
    context.req_body["child_nodes"] = {
        "learning_objects":[]
    }
    context.res = post_method(url=context.url, request_body=context.req_body)
    context.res_data = context.res.json()
    assert context.res.status_code == 200
    assert context.res_data["success"] is True

    context.le_uuid = context.res_data["data"]["uuid"]

    lx_dict = copy(TEST_LEARNING_OBJECT)
    context.url = f"{API_URL}/learning-object"
    for key in DEL_KEYS:
        if key in lx_dict:
            del lx_dict[key]
    lx_dict["parent_nodes"]["learning_experiences"]=[context.le_uuid]
    context.res = post_method(url=context.url, request_body=lx_dict)
    context.res_data = context.res.json()
    assert context.res.status_code == 200
    assert context.res_data["success"] is True

    context.lo_uuid = context.res_data["data"]["uuid"]

    lr_dict = copy(TEST_LEARNING_RESOURCE)
    context.url = f"{API_URL}/learning-resource"
    for key in DEL_KEYS:
        if key in lr_dict:
            del lr_dict[key]
    lr_dict["parent_nodes"]["learning_objects"]=[context.lo_uuid]
    context.res = post_method(url=context.url, request_body=lr_dict)
    context.res_data = context.res.json()
    assert context.res.status_code == 200
    assert context.res_data["success"] is True

    context.lr_uuid = context.res_data["data"]["uuid"]

    set_cache("le_uuid_madcap_2",context.le_uuid)
    set_cache("lo_uuid_madcap_2",context.lo_uuid)
    set_cache("lr_uuid_madcap_2",context.lr_uuid)

    content_file = open(TEST_CONTENT_SERVING_MADCAP_V1_PATH,"rb")
    content_file_input_dict = {"content_file":
              ("content_serving_sample_upload_madcap_v1.zip", content_file, "application/x-zip-compressed")}

    content_res = post_method(
            url=f"{API_URL_LEARNING_OBJECT_SERVICE}/content-serving/upload/madcap/{context.le_uuid}",
            files=content_file_input_dict
            )
    context.res_json = content_res.json()
    context.status_code = content_res.status_code

    assert context.status_code == 200
    assert context.res_json["success"] == True
    assert context.res_json["message"] == f"Successfully uploaded the content for learning experience with uuid {context.le_uuid}"

    url = f"{API_URL}/learning-experience/{context.le_uuid}"
    res = get_method(url)
    res_json = res.json()
    assert res.status_code == 200
    assert res_json["success"] == True
    assert res_json["data"]["resource_path"] == "learning-resources/content_serving_sample_upload_madcap_v1/"

@behave.when("API request is sent to link valid madcap htm file against a learning resource")
def step_impl_2(context):
    context.res = post_method(
        url=f"{API_URL}/content-serving/link/madcap/{context.le_uuid}/{context.lr_uuid}",
        request_body={
            "resource_path": "learning-resources/content_serving_sample_upload_madcap_v1/Dummy_Madcap/Content/test_module.htm",
            "type": "html"
        }
    )
    context.res_json = context.res.json()

@behave.then("LOS will return a success response for the link")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_json["success"] == True
    assert context.res_json["message"] == f"Successfully linked content to Learning Resource with uuid {context.lr_uuid}"
    
    res = get_method(url=f"{API_URL}/learning-resource/{context.lr_uuid}")
    res_json = res.json()
    assert res_json["data"]["resource_path"] == "learning-resources/content_serving_sample_upload_madcap_v1/Dummy_Madcap/Content/test_module.htm"

# -----------------------------------------------------
# Scenario 2: User wants to link a file against a learning resource which is not allowed by the learning experience
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to link file against a learning resource which is not allowed by the learning experience")
def step_impl_1(context):
    context.le_uuid = get_cache("le_uuid_madcap_2")

    lx_dict = copy(TEST_LEARNING_OBJECT)
    context.url = f"{API_URL}/learning-object"
    for key in DEL_KEYS:
        if key in lx_dict:
            del lx_dict[key]
    lx_dict["parent_nodes"]["learning_experiences"]=[context.le_uuid]
    context.res = post_method(url=context.url, request_body=lx_dict)
    context.res_data = context.res.json()
    assert context.res.status_code == 200
    assert context.res_data["success"] is True

    context.lo_uuid = context.res_data["data"]["uuid"]

    lr_dict = copy(TEST_LEARNING_RESOURCE)
    context.url = f"{API_URL}/learning-resource"
    for key in DEL_KEYS:
        if key in lr_dict:
            del lr_dict[key]
    lr_dict["parent_nodes"]["learning_objects"]=[context.lo_uuid]
    context.res = post_method(url=context.url, request_body=lr_dict)
    context.res_data = context.res.json()
    assert context.res.status_code == 200
    assert context.res_data["success"] is True

    context.lr_uuid = context.res_data["data"]["uuid"]

    context.gcs_object = GcsCrudService(CONTENT_SERVING_BUCKET)
    context.content_serving_uri = context.gcs_object.upload_file_to_bucket(
                                        "learning-resources/dev_testing/testing-files",
                                        "content_serving.html", TEST_CONTENT_SERVING_PATH)
    context.content_serving_uri = context.content_serving_uri.split("learning-resources/")[1]

@behave.when("API request is sent to link file against a learning resource which is not allowed by the learning experience")
def step_impl_2(context):
    context.res = post_method(
        url=f"{API_URL}/content-serving/link/madcap/{context.le_uuid}/{context.lr_uuid}",
        request_body={
            "resource_path": context.content_serving_uri,
            "type": "html"
        }
    )
    context.res_json = context.res.json()

@behave.then("LOS will return a validation error for a file which does not share prefix with the parent learning experience")
def step_impl_3(context):
    assert context.res.status_code == 422
    assert context.res_json["success"] == False
    print(context.res_json)
    assert "Cannot link Learning Resource with a file that does not belong to the folder given by Learning Experience." in context.res_json["message"]

# -----------------------------------------------------
# Scenario 3: User wants to link valid madcap htm file against a learning resource but invalid learning experience
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to link valid madcap htm file against a learning resource but invalid learning experience")
def step_impl_1(context):
    context.le_uuid = "random_le_uuid"
    context.lr_uuid = get_cache("lr_uuid_madcap_2")

@behave.when("API request is sent to link valid madcap htm file against a learning resource but invalid learning experience")
def step_impl_2(context):
    context.res = post_method(
        url=f"{API_URL}/content-serving/link/madcap/{context.le_uuid}/{context.lr_uuid}",
        request_body={
            "resource_path": "learning-resources/content_serving_sample_upload_madcap_v1/Dummy_Madcap/Content/test_module.htm",
            "type": "html"
        }
    )
    context.res_json = context.res.json()

@behave.then("LOS will return a validation error for the invalid learning experience in link api")
def step_impl_3(context):
    assert context.res.status_code == 404
    assert context.res_json["success"] == False
    assert context.res_json["message"] == f"Learning Experience with uuid {context.le_uuid} not found"

# -----------------------------------------------------
# Scenario 4: User wants to link valid madcap htm file against invalid learning resource
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to link valid madcap htm file against invalid learning resource")
def step_impl_1(context):
    context.le_uuid = get_cache("le_uuid_madcap_2")
    context.lr_uuid = "random_lr_uuid"

@behave.when("API request is sent to link valid madcap htm file against invalid learning resource")
def step_impl_2(context):
    context.res = post_method(
        url=f"{API_URL}/content-serving/link/madcap/{context.le_uuid}/{context.lr_uuid}",
        request_body={
            "resource_path": "learning-resources/content_serving_sample_upload_madcap_v1/Dummy_Madcap/Content/test_module.htm",
            "type": "html"
        }
    )
    context.res_json = context.res.json()

@behave.then("LOS will return a validation error for the invalid learning resource in link api")
def step_impl_3(context):
    assert context.res.status_code == 404
    assert context.res_json["success"] == False
    assert context.res_json["message"] == f"Learning Resource with uuid {context.lr_uuid} not found"

# -----------------------------------------------------
# Scenario 5: User wants to link valid madcap htm file against a learning resource which is not child of given learning experience
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to link valid madcap htm file against a learning resource which is not child of given learning experience")
def step_impl_1(context):
    context.le_uuid = get_cache("le_uuid_madcap_2")

    lr_dict = copy(TEST_LEARNING_RESOURCE)
    lr_dict["parent_nodes"] = {
        "learning_objects":[]
    }
    context.url = f"{API_URL}/learning-resource"
    for key in DEL_KEYS:
        if key in lr_dict:
            del lr_dict[key]
    context.res = post_method(url=context.url, request_body=lr_dict)
    context.res_data = context.res.json()
    assert context.res.status_code == 200
    assert context.res_data["success"] is True

    context.lr_uuid = context.res_data["data"]["uuid"]

@behave.when("API request is sent to link valid madcap htm file against a learning resource which is not child of given learning experience")
def step_impl_2(context):
    context.res = post_method(
        url=f"{API_URL}/content-serving/link/madcap/{context.le_uuid}/{context.lr_uuid}",
        request_body={
            "resource_path": "learning-resources/content_serving_sample_upload_madcap_v1/Dummy_Madcap/Content/test_module.htm",
            "type": "html"
        }
    )
    context.res_json = context.res.json()

@behave.then("LOS will return a validation error for the invalid learning resource and learning experience pair")
def step_impl_3(context):
    assert context.res.status_code == 422
    assert context.res_json["success"] == False
    assert context.res_json["message"] == f"Given Learning Resource {context.lr_uuid} is not a child of Learning Experience {context.le_uuid}", context.res_json["message"]

# -----------------------------------------------------
# Scenario 6: User wants to link valid madcap htm file against a learning resource for which the learning experience does not have a resource_path
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to link valid madcap htm file against a learning resource for which the learning experience does not have a resource_path")
def step_impl_1(context):
    context.req_body = copy(TEST_LEARNING_EXPERIENCE)
    context.req_body["resource_path"] = ""
    context.url = f"{API_URL}/learning-experience"
    context.req_body["child_nodes"] = {
        "learning_objects":[]
    }
    context.res = post_method(url=context.url, request_body=context.req_body)
    context.res_data = context.res.json()
    assert context.res.status_code == 200
    assert context.res_data["success"] is True

    context.le_uuid = context.res_data["data"]["uuid"]

    lx_dict = copy(TEST_LEARNING_OBJECT)
    context.url = f"{API_URL}/learning-object"
    for key in DEL_KEYS:
        if key in lx_dict:
            del lx_dict[key]
    lx_dict["parent_nodes"]["learning_experiences"]=[context.le_uuid]
    context.res = post_method(url=context.url, request_body=lx_dict)
    context.res_data = context.res.json()
    assert context.res.status_code == 200
    assert context.res_data["success"] is True

    context.lo_uuid = context.res_data["data"]["uuid"]

    lr_dict = copy(TEST_LEARNING_RESOURCE)
    context.url = f"{API_URL}/learning-resource"
    for key in DEL_KEYS:
        if key in lr_dict:
            del lr_dict[key]
    lr_dict["parent_nodes"]["learning_objects"]=[context.lo_uuid]
    context.res = post_method(url=context.url, request_body=lr_dict)
    context.res_data = context.res.json()
    assert context.res.status_code == 200
    assert context.res_data["success"] is True

    context.lr_uuid = context.res_data["data"]["uuid"]

    url = f"{API_URL}/learning-experience/{context.le_uuid}"
    res = get_method(url)
    res_json = res.json()
    assert res.status_code == 200
    assert res_json["success"] == True
    assert res_json["data"]["resource_path"] == ""

@behave.when("API request is sent to link valid madcap htm file against a learning resource for which the learning experience does not have a resource_path")
def step_impl_2(context):
    context.res = post_method(
        url=f"{API_URL}/content-serving/link/madcap/{context.le_uuid}/{context.lr_uuid}",
        request_body={
            "resource_path": "learning-resources/content_serving_sample_upload_madcap_v1/Dummy_Madcap/Content/test_module.htm",
            "type": "html"
        }
    )
    context.res_json = context.res.json()

@behave.then("LOS will return a validation error for the missing resource_path for the learning experience")
def step_impl_3(context):
    assert context.res.status_code == 422
    assert context.res_json["success"] == False
    assert context.res_json["message"] == f"The resource_path of Learning Experience {context.le_uuid} is empty. Hence, we cannot link content to Learning resource with uuid {context.lr_uuid}"
