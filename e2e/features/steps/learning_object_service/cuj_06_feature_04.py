"""
    User should be able to upload learning content files to be published
"""
import behave
import sys
from common.utils.gcs_adapter import GcsCrudService

sys.path.append("../")
from setup import post_method, get_method, put_method, set_cache, get_cache,CONTENT_SERVING_BUCKET
from environment import TEST_CONTENT_SERVING_PATH
from test_config import API_URL_LEARNING_OBJECT_SERVICE, DEL_KEYS
from test_object_schemas import (TEST_LEARNING_RESOURCE,)

API_URL = API_URL_LEARNING_OBJECT_SERVICE
LEARNING_RESOURCE_UUID=""

# -----------------------------------------------------
# Scenario 1: User wants to get all versions of initial learning content
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to get all versions of initial learning content")
def step_impl_1(context):
    context.gcs_object = GcsCrudService(CONTENT_SERVING_BUCKET)
    context.content_serving_uri = context.gcs_object.upload_file_to_bucket(
                                        "learning-resources/dev_testing/testing-files",
                                        "content_serving.html", TEST_CONTENT_SERVING_PATH)
    context.content_serving_uri = context.content_serving_uri.split("learning-resources/")[1]
    set_cache("content_serving_uri", context.content_serving_uri)
    context.payload = TEST_LEARNING_RESOURCE
    for key in DEL_KEYS:
        if key in context.payload:
            del context.payload[key]
    learning_resource = post_method(
        url=f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-resource",
        request_body={
            **context.payload, 
            "resource_path": "",
            "type":""
        })
    learning_resource_data = learning_resource.json()
    context.uuid= learning_resource_data["data"]["uuid"]

@behave.when("API request is sent to get all versions of initial learning content")
def step_impl_2(context):
    context.res = get_method(
        url=f"{API_URL}/content-serving/content-versions/{context.uuid}"
    )
    context.res_json = context.res.json()

@behave.then("LOS will return a json response with list of learning resource documents including only initial learning content")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json["message"] == "Successfully fetched content version for learning resource"
    assert len(context.res_json["data"]) == 1

    version_data = context.res_json["data"][0]
    assert version_data["content_version_uuid"] == context.uuid
    assert version_data["status"] == "draft"
    assert version_data["resource_path"] == ""
    assert version_data["type"] == ""

# -----------------------------------------------------
# Scenario 2: User wants to get all versions in a generic case
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to get all versions in a generic case")
def step_impl_1(context):
    context.gcs_object = GcsCrudService(CONTENT_SERVING_BUCKET)
    context.content_serving_uri = context.gcs_object.upload_file_to_bucket(
                                        "learning-resources/dev_testing/testing-files",
                                        "content_serving.html", TEST_CONTENT_SERVING_PATH)
    context.content_serving_uri = context.content_serving_uri.split("learning-resources/")[1]
    context.payload = TEST_LEARNING_RESOURCE
    for key in DEL_KEYS:
        if key in context.payload:
            del context.payload[key]
    
    # Create first LR
    learning_resource = post_method(
        url=f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-resource",
        request_body={
            **context.payload, 
            "resource_path": "",
            "type":"",
            "child_nodes":{
                "learning_objects":[]
            }
        })
    learning_resource_data = learning_resource.json()
    context.uuid= learning_resource_data["data"]["uuid"]

    # Link content 1
    res = put_method(
        url=f"{API_URL}/content-serving/link/{context.uuid}",
        request_body = {
            "resource_path": context.content_serving_uri,
            "type": "html_package"
        }
    )
    res_json = res.json()

    assert res.status_code == 200
    assert res_json["success"] is True
    assert res_json[
        "message"] == "Successfully linked learning resource with content"
    context.resource_1_uuid = res_json["data"]["resource_uuid"]

    # Link content 2
    res = put_method(
        url=f"{API_URL}/content-serving/link/{context.uuid}",
        request_body = {
            "resource_path": context.content_serving_uri,
            "type": "html_package"
        }
    )
    res_json = res.json()

    assert res.status_code == 200
    assert res_json["success"] is True
    assert res_json[
        "message"] == "Successfully linked learning resource with content"
    context.resource_2_uuid = res_json["data"]["resource_uuid"]

    # Link content 3
    res = put_method(
        url=f"{API_URL}/content-serving/link/{context.uuid}",
        request_body = {
            "resource_path": context.content_serving_uri,
            "type": "html_package"
        }
    )
    res_json = res.json()

    assert res.status_code == 200
    assert res_json["success"] is True
    assert res_json[
        "message"] == "Successfully linked learning resource with content"
    context.resource_3_uuid = res_json["data"]["resource_uuid"]

    # Publish content 1
    context.res = put_method(
        url=f"{API_URL}/content-serving/publish/{context.uuid}",
        query_params={"target_version_uuid":context.resource_1_uuid},
        request_body={}
    )
    context.res_json = context.res.json()

    assert context.res.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json["message"] == "Successfully published content"

    # Publish content 2
    context.res = put_method(
        url=f"{API_URL}/content-serving/publish/{context.resource_1_uuid}",
        query_params={"target_version_uuid":context.resource_2_uuid},
        request_body={}
    )
    context.res_json = context.res.json()

    assert context.res.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json["message"] == "Successfully published content"

@behave.when("API request is sent to get all versions in a generic case")
def step_impl_2(context):
    context.res = get_method(
        url=f"{API_URL}/content-serving/content-versions/{context.uuid}"
    )
    context.res_json = context.res.json()

@behave.then("LOS will return a json response with list of learning resource documents")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json["message"] == "Successfully fetched content version for learning resource"
    assert len(context.res_json["data"]) == 4

# -----------------------------------------------------
# Scenario 3: User wants to get all versions for invalid learning resource
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to get all versions for invalid learning resource")
def step_impl_1(context):
    context.uuid="random_learning_resource_uuid"

@behave.when("API request is sent to get all versions for invalid learning resource")
def step_impl_2(context):
    context.res = get_method(
        url=f"{API_URL}/content-serving/content-versions/{context.uuid}"
    )
    context.res_json = context.res.json()

@behave.then("LOS will return a resource not found error for learning resource")
def step_impl_3(context):
    assert context.res.status_code == 404
    assert context.res_json["success"] is False
    assert context.res_json[
        "message"] == f"Learning Resource with uuid {context.uuid} not found"

# -----------------------------------------------------
# Scenario 4: User wants to get all versions in a generic case with status filter
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to get all versions in a generic case with status filter")
def step_impl_1(context):
    context.gcs_object = GcsCrudService(CONTENT_SERVING_BUCKET)
    context.content_serving_uri = context.gcs_object.upload_file_to_bucket(
                                        "learning-resources/dev_testing/testing-files",
                                        "content_serving.html", TEST_CONTENT_SERVING_PATH)
    context.content_serving_uri = context.content_serving_uri.split("learning-resources/")[1]
    context.payload = TEST_LEARNING_RESOURCE
    for key in DEL_KEYS:
        if key in context.payload:
            del context.payload[key]
    
    # Create first LR
    learning_resource = post_method(
        url=f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-resource",
        request_body={
            **context.payload, 
            "resource_path": "",
            "type":"",
            "child_nodes":{
                "learning_objects":[]
            }
        })
    learning_resource_data = learning_resource.json()
    context.uuid= learning_resource_data["data"]["uuid"]

    # Link content 1
    res = put_method(
        url=f"{API_URL}/content-serving/link/{context.uuid}",
        request_body = {
            "resource_path": context.content_serving_uri,
            "type": "html_package"
        }
    )
    res_json = res.json()

    assert res.status_code == 200
    assert res_json["success"] is True
    assert res_json[
        "message"] == "Successfully linked learning resource with content"
    context.resource_1_uuid = res_json["data"]["resource_uuid"]

    # Link content 2
    res = put_method(
        url=f"{API_URL}/content-serving/link/{context.uuid}",
        request_body = {
            "resource_path": context.content_serving_uri,
            "type": "html_package"
        }
    )
    res_json = res.json()

    assert res.status_code == 200
    assert res_json["success"] is True
    assert res_json[
        "message"] == "Successfully linked learning resource with content"
    context.resource_2_uuid = res_json["data"]["resource_uuid"]

    # Link content 3
    res = put_method(
        url=f"{API_URL}/content-serving/link/{context.uuid}",
        request_body = {
            "resource_path": context.content_serving_uri,
            "type": "html_package"
        }
    )
    res_json = res.json()

    assert res.status_code == 200
    assert res_json["success"] is True
    assert res_json[
        "message"] == "Successfully linked learning resource with content"
    context.resource_3_uuid = res_json["data"]["resource_uuid"]

    # Publish content 1
    context.res = put_method(
        url=f"{API_URL}/content-serving/publish/{context.uuid}",
        query_params={"target_version_uuid":context.resource_1_uuid},
        request_body={}
    )
    context.res_json = context.res.json()

    assert context.res.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json["message"] == "Successfully published content"

    # Publish content 2
    context.res = put_method(
        url=f"{API_URL}/content-serving/publish/{context.resource_1_uuid}",
        query_params={"target_version_uuid":context.resource_2_uuid},
        request_body={}
    )
    context.res_json = context.res.json()

    assert context.res.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json["message"] == "Successfully published content"

@behave.when("API request is sent to get all versions in a generic case with status filter")
def step_impl_2(context):

    res_1 = get_method(
        url=f"{API_URL}/content-serving/content-versions/{context.uuid}",
        query_params={"status" : "draft"}
    )
    res_2 = get_method(
        url=f"{API_URL}/content-serving/content-versions/{context.uuid}",
        query_params={"status" : "published"}
    )
    res_3 = get_method(
        url=f"{API_URL}/content-serving/content-versions/{context.uuid}",
        query_params={"status" : "unpublished"}
    )

    context.res_list = [res_1,res_2,res_3]

@behave.then("LOS will return a json response with list of learning resource documents with status filter")
def step_impl_3(context):
    assert context.res_list[0].status_code == 200
    res_json = context.res_list[0].json()
    assert res_json["success"] is True
    assert res_json["message"] == "Successfully fetched content version for learning resource"
    assert len(res_json["data"]) == 2
    assert res_json["data"][0]["status"] == "draft"

    assert context.res_list[1].status_code == 200
    res_json = context.res_list[1].json()
    assert res_json["success"] is True
    assert res_json["message"] == "Successfully fetched content version for learning resource"
    assert len(res_json["data"]) == 1
    assert res_json["data"][0]["status"] == "published"

    assert context.res_list[2].status_code == 200
    res_json = context.res_list[2].json()
    assert res_json["success"] is True
    assert res_json["message"] == "Successfully fetched content version for learning resource"
    assert len(res_json["data"]) == 1
    assert res_json["data"][0]["status"] == "unpublished"
