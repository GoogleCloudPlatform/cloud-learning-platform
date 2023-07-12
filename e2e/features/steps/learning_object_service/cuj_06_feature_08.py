"""
    User should be able to upload a valid madcap export at learning experience level
"""
import behave
import sys
from copy import copy

sys.path.append("../")
from e2e.setup import post_method, get_method, get_cache, set_cache
from environment import TEST_CONTENT_SERVING_ZIP_PATH, TEST_CONTENT_SERVING_MADCAP_V1_PATH, TEST_CONTENT_SERVING_MADCAP_V2_PATH
from e2e.test_config import API_URL_LEARNING_OBJECT_SERVICE, DEL_KEYS
from e2e.test_object_schemas import (TEST_LEARNING_OBJECT, TEST_LEARNING_EXPERIENCE, TEST_LEARNING_RESOURCE)

API_URL = API_URL_LEARNING_OBJECT_SERVICE
LEARNING_RESOURCE_UUID=""

# -----------------------------------------------------
# Scenario 1: User wants to upload a valid madcap export at learning experience level
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to upload a valid madcap export at learning experience level")
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

    set_cache("le_uuid_madcap_1",context.le_uuid)
    set_cache("lo_uuid_madcap_1",context.lo_uuid)
    set_cache("lr_uuid_madcap_1",context.lr_uuid)

@behave.when("API request is sent to upload a valid madcap export at learning experience level")
def step_impl_2(context):
    content_file = open(TEST_CONTENT_SERVING_MADCAP_V1_PATH,"rb")
    content_file_input_dict = {"content_file":
              ("content_serving_sample_upload_madcap_v1.zip", content_file, "application/zip")}

    content_res = post_method(
            url=f"{API_URL_LEARNING_OBJECT_SERVICE}/content-serving/upload/madcap/{context.le_uuid}",
            files=content_file_input_dict
            )
    context.res_json = content_res.json()
    context.status_code = content_res.status_code

@behave.then("LOS will return a json response with file and folder list of the uploaded madcap zip")
def step_impl_3(context):
    assert context.status_code == 200
    assert context.res_json["success"] == True
    assert context.res_json["message"] == f"Successfully uploaded the content for learning experience with uuid {context.le_uuid}"

    url = f"{API_URL}/learning-experience/{context.le_uuid}"
    res = get_method(url)
    res_json = res.json()
    assert res.status_code == 200
    assert res_json["success"] == True
    assert res_json["data"]["resource_path"] == "learning-resources/content_serving_sample_upload_madcap_v1/"

# -----------------------------------------------------
# Scenario 2: User wants to upload an invalid madcap export at learning experience level
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to upload an invalid madcap export at learning experience level")
def step_impl_1(context):
    context.le_uuid = get_cache("le_uuid_madcap_1")

@behave.when("API request is sent to upload an invalid madcap export at learning experience level")
def step_impl_2(context):
    content_file = open(TEST_CONTENT_SERVING_ZIP_PATH,"rb")
    content_file_input_dict = {"content_file":
              ("content_serving_sample_upload_scorm.zip", content_file, "application/zip")}

    content_res = post_method(
            url=f"{API_URL_LEARNING_OBJECT_SERVICE}/content-serving/upload/madcap/{context.le_uuid}",
            files=content_file_input_dict
            )
    context.res_json = content_res.json()
    context.status_code = content_res.status_code

@behave.then("LOS will return a validation error for invalid madcap export upload")
def step_impl_3(context):
    assert context.status_code == 422
    assert context.res_json["success"] == False
    assert f"content_serving_sample_upload_scorm is not a valid Madcap Export." in context.res_json["message"]

# -----------------------------------------------------
# Scenario 3: User wants to reupload a valid and identical madcap export at learning experience level
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to reupload a valid and identical madcap export at learning experience level")
def step_impl_1(context):
    context.le_uuid = get_cache("le_uuid_madcap_1")

@behave.when("API request is sent to reupload a valid and identical madcap export at learning experience level")
def step_impl_2(context):
    content_file = open(TEST_CONTENT_SERVING_MADCAP_V1_PATH,"rb")
    content_file_input_dict = {"content_file":
              ("content_serving_sample_upload_madcap_v2.zip", content_file, "application/zip")}

    content_res = post_method(
            url=f"{API_URL_LEARNING_OBJECT_SERVICE}/content-serving/upload/madcap/{context.le_uuid}",
            files=content_file_input_dict
            )
    context.res_json = content_res.json()
    context.status_code = content_res.status_code

@behave.then("LOS will return a json response with file and folder list of the reuploaded and identical zip")
def step_impl_3(context):
    assert context.status_code == 200
    assert context.res_json["success"] == True
    assert context.res_json["message"] == f"Successfully uploaded the content for learning experience with uuid {context.le_uuid}"

    url = f"{API_URL}/learning-experience/{context.le_uuid}"
    res = get_method(url)
    res_json = res.json()
    assert res.status_code == 200
    assert res_json["success"] == True
    assert res_json["data"]["resource_path"] == "learning-resources/content_serving_sample_upload_madcap_v2/"


# -----------------------------------------------------
# Scenario 4: User wants to reupload a valid but non-identical madcap export at learning experience level
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to reupload a valid but non-identical madcap export at learning experience level")
def step_impl_1(context):
    context.le_uuid = get_cache("le_uuid_madcap_1")

@behave.when("API request is sent to reupload a valid but non-identical madcap export at learning experience level")
def step_impl_2(context):
    content_file = open(TEST_CONTENT_SERVING_MADCAP_V2_PATH,"rb")
    content_file_input_dict = {"content_file":
              ("content_serving_sample_upload_madcap_v2.zip", content_file, "application/zip")}

    content_res = post_method(
            url=f"{API_URL_LEARNING_OBJECT_SERVICE}/content-serving/upload/madcap/{context.le_uuid}",
            files=content_file_input_dict
            )
    context.res_json = content_res.json()
    context.status_code = content_res.status_code

@behave.then("LOS will return a validation error for the missing htm files in the reuploaded zip")
def step_impl_3(context):
    assert context.status_code == 422
    assert context.res_json["success"] == False
    assert f"Content override is forbidden because of missing files." in context.res_json["message"]


# -----------------------------------------------------
# Scenario 5: User wants to upload a valid madcap export against invalid learning experience
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to upload a valid madcap export against invalid learning experience")
def step_impl_1(context):
    context.le_uuid = "Invalid LE uuid"

@behave.when("API request is sent to upload a valid madcap export against invalid learning experience")
def step_impl_2(context):
    content_file = open(TEST_CONTENT_SERVING_MADCAP_V1_PATH,"rb")
    content_file_input_dict = {"content_file":
              ("content_serving_sample_upload_madcap_v1.zip", content_file, "application/zip")}

    content_res = post_method(
            url=f"{API_URL_LEARNING_OBJECT_SERVICE}/content-serving/upload/madcap/{context.le_uuid}",
            files=content_file_input_dict
            )
    context.res_json = content_res.json()
    context.status_code = content_res.status_code

@behave.then("LOS will return a validation error for the invalid learning experience")
def step_impl_3(context):
    assert context.status_code == 404
    assert context.res_json["success"] == False
    assert context.res_json["message"] == f"Learning Experience with uuid {context.le_uuid} not found"
