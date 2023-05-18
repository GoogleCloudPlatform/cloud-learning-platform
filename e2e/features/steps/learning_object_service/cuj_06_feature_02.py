"""
    User should be able to link uploaded content with a learning resource
"""
import behave
import sys
from common.utils.gcs_adapter import GcsCrudService

sys.path.append("../")
from setup import post_method, get_method, put_method,get_cache, set_cache, CONTENT_SERVING_BUCKET
from environment import TEST_CONTENT_SERVING_PATH
from test_config import API_URL_LEARNING_OBJECT_SERVICE, DEL_KEYS
from test_object_schemas import (TEST_LEARNING_RESOURCE,)

API_URL = API_URL_LEARNING_OBJECT_SERVICE
LEARNING_RESOURCE_UUID=""

# -----------------------------------------------------
# Scenario 1: User wants to link an existing file with a valid learning resource
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to link an existing file with a valid learning resource")
def step_impl_1(context):
    context.gcs_object = GcsCrudService(CONTENT_SERVING_BUCKET)
    context.content_serving_uri = context.gcs_object.upload_file_to_bucket(
                                        "learning-resources/dev_testing/testing-files",
                                        "content_serving.html", TEST_CONTENT_SERVING_PATH)
    context.content_serving_uri = context.content_serving_uri.split("learning-resources/")[1]
    set_cache("content_serving_uri",context.content_serving_uri)
    context.payload = TEST_LEARNING_RESOURCE
    for key in DEL_KEYS:
        if key in context.payload:
            del context.payload[key]
    learning_resource = post_method(
        url=f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-resource",
        request_body={
            **context.payload, 
            "resource_path": "",
            "type": ""
        })
    learning_resource_data = learning_resource.json()
    context.uuid= learning_resource_data["data"]["uuid"]
    set_cache("lr_link_uuid",learning_resource_data["data"]["uuid"])

@behave.when("API request is sent to link the content with learning resource")
def step_impl_2(context):
    context.res = put_method(
        url=f"{API_URL}/content-serving/link/{context.uuid}",
        request_body = {
            "resource_path": context.content_serving_uri,
            "type": "html_package"
        }
    )
    context.res_json = context.res.json()

@behave.then("LOS will return a json response with signed URl for preview of linked content from learning resource")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json[
        "message"] == "Successfully linked learning resource with content"

    new_resource_uuid = context.res_json["data"]["resource_uuid"]

    res = get_method(
        url=f"{API_URL}/learning-resource/{new_resource_uuid}")
    res_json = res.json()

    assert res.status_code == 200
    assert res_json["data"]["resource_path"] == context.content_serving_uri
    assert res_json["data"]["status"] == "draft"
    assert res_json["data"]["parent_version_uuid"] == context.uuid

# -----------------------------------------------------
# Scenario 2: User wants to link an existing file with invalid learning resource
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to link an existing file with invalid learning resource")
def step_impl_1(context):
    context.gcs_object = GcsCrudService(CONTENT_SERVING_BUCKET)
    context.content_serving_uri = context.gcs_object.upload_file_to_bucket(
                                        "learning-resources/dev_testing/testing-files",
                                        "content_serving.html", TEST_CONTENT_SERVING_PATH)
    context.content_serving_uri = context.content_serving_uri.split("learning-resources/")[1]
    
    context.uuid= "invalid_lr_uuid"

@behave.when("API request is sent to link the content with invalid learning resource")
def step_impl_2(context):
    context.res = put_method(
        url=f"{API_URL}/content-serving/link/{context.uuid}",
        request_body = {
            "resource_path": context.content_serving_uri,
            "type": "html_package"
        }
    )
    context.res_json = context.res.json()

@behave.then("LOS will return a resource is not found error response for invalid learning resource uuid for linking content")
def step_impl_3(context):
    assert context.res.status_code == 404
    assert context.res_json["success"] is False
    assert context.res_json[
        "message"] == f"Learning Resource with uuid {context.uuid} not found"

# -----------------------------------------------------
# Scenario 3: User wants to link a nonexisting file with learning resource
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to link a non existing file with learning resource")
def step_impl_1(context):
    context.uuid= get_cache("lr_link_uuid")
    context.content_serving_uri = "random/resource/path"


@behave.when("API request is sent to link the non existent content with a learning resource")
def step_impl_2(context):
    context.res = put_method(
        url=f"{API_URL}/content-serving/link/{context.uuid}",
        request_body = {
            "resource_path": context.content_serving_uri,
            "type": "html_package"
        }
    )
    context.res_json = context.res.json()

@behave.then("LOS will return a resource is not found error response for nonexisting file")
def step_impl_3(context):
    assert context.res.status_code == 404
    assert context.res_json["success"] is False
    assert context.res_json[
        "message"] == "Provided resource path does not exist on GCS bucket"