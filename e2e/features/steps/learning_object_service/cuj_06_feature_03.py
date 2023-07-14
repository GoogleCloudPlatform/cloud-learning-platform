"""
    User should be able to publish a learning content version
"""
import behave
import sys
from common.utils.gcs_adapter import GcsCrudService

sys.path.append("../")
from e2e.setup import post_method, get_method, put_method, CONTENT_SERVING_BUCKET
from environment import TEST_CONTENT_SERVING_PATH
from e2e.test_config import API_URL_LEARNING_OBJECT_SERVICE, DEL_KEYS
from e2e.test_object_schemas import (TEST_LEARNING_RESOURCE,TEST_LEARNING_OBJECT)

API_URL = API_URL_LEARNING_OBJECT_SERVICE
LEARNING_RESOURCE_UUID=""

# -----------------------------------------------------
# Scenario 1: User wants to publish a valid initial learning content version
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to publish a valid initial learning content version")
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

    context.res = put_method(
        url=f"{API_URL}/content-serving/link/{context.uuid}",
        request_body = {
            "resource_path": context.content_serving_uri,
            "type": "html_package"
        }
    )
    context.res_json = context.res.json()

    assert context.res.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json[
        "message"] == "Successfully linked learning resource with content"

    context.new_resource_uuid = context.res_json["data"]["resource_uuid"]

@behave.when("API request is sent to publish a valid initial learning content version")
def step_impl_2(context):
    context.res = put_method(
        url=f"{API_URL}/content-serving/publish/{context.uuid}",
        query_params = {"target_version_uuid":context.new_resource_uuid},
        request_body={}
    )
    context.res_json = context.res.json()

@behave.then("LOS will return a json response with signed URl for preview of published content and published initial content uuid")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json["message"] == "Successfully published content"

    context.res = get_method(
      url=f"{API_URL}/learning-resource/{context.uuid}")
    context.res_json = context.res.json()

    assert context.res.status_code == 200
    assert context.res_json["data"]["status"] == "draft"

    context.res = get_method(
      url=f"{API_URL}/learning-resource/{context.new_resource_uuid}")
    context.res_json = context.res.json()

    assert context.res.status_code == 200
    assert context.res_json["data"]["status"] == "published"

# -----------------------------------------------------
# Scenario 2: User wants to publish a valid learning content version
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to publish a valid learning content version")
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

    context.res = put_method(
        url=f"{API_URL}/content-serving/link/{context.uuid}",
        request_body = {
            "resource_path": context.content_serving_uri,
            "type": "html_package"
        }
    )
    context.res_json = context.res.json()

    assert context.res.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json[
        "message"] == "Successfully linked learning resource with content"
    
    context.new_resource_uuid = context.res_json["data"]["resource_uuid"]

    context.res = put_method(
        url=f"{API_URL}/content-serving/publish/{context.uuid}",
        query_params={"target_version_uuid":context.new_resource_uuid},
        request_body={}
    )
    context.res_json = context.res.json()
    assert context.res.status_code == 200
    assert context.res_json["message"] == "Successfully published content"

    context.res = put_method(
        url=f"{API_URL}/content-serving/link/{context.new_resource_uuid}",
        request_body = {
            "resource_path": context.content_serving_uri,
            "type": "html_package"
        }
    )
    context.res_json = context.res.json()

    assert context.res.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json[
        "message"] == "Successfully linked learning resource with content"
    context.new_resource_uuid_1 = context.res_json["data"]["resource_uuid"]

@behave.when("API request is sent to publish a valid learning content version")
def step_impl_2(context):
    context.res = put_method(
        url=f"{API_URL}/content-serving/publish/{context.new_resource_uuid}",
        query_params={"target_version_uuid":context.new_resource_uuid_1},
        request_body={}
    )
    context.res_json = context.res.json()

@behave.then("LOS will return a json response with signed URl for preview of published content and published content uuid")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json["message"] == "Successfully published content"

    # check new document fields
    context.res = get_method(
      url=f"{API_URL}/learning-resource/{context.new_resource_uuid_1}")
    context.res_json = context.res.json()

    assert context.res.status_code == 200
    assert context.res_json["data"]["status"] == "published"

    # check old document fields
    context.res = get_method(
      url=f"{API_URL}/learning-resource/{context.new_resource_uuid}")
    context.res_json = context.res.json()

    assert context.res.status_code == 200
    assert context.res_json["data"]["status"] == "unpublished"


# -----------------------------------------------------
# Scenario 3: User wants to republish a valid learning content version
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to republish a valid learning content version")
def step_impl_1(context):
    context.gcs_object = GcsCrudService(CONTENT_SERVING_BUCKET)
    context.content_serving_uri = context.gcs_object.upload_file_to_bucket(
                                        "learning-resources/dev_testing/testing-files",
                                        "content_serving.html", TEST_CONTENT_SERVING_PATH)
    context.content_serving_uri = context.content_serving_uri.split("learning-resources/")[1]
    
    lo_payload = TEST_LEARNING_OBJECT
    for key in DEL_KEYS:
        if key in lo_payload:
            del context.payload[key]
    learning_object_data = post_method(
        url=f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-object",
        request_body={
            **lo_payload, 
            "child_nodes":{
                "learning_resources":[]
            }
        })
    learning_object_data = learning_object_data.json()
    context.lo_uuid= learning_object_data["data"]["uuid"]

    context.payload = TEST_LEARNING_RESOURCE
    for key in DEL_KEYS:
        if key in context.payload:
            del context.payload[key]
    learning_resource = post_method(
        url=f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-resource",
        request_body={
            **context.payload, 
            "resource_path": "",
            "type":"",
            "child_nodes":{
                "learning_resources":[]
            },
            "parent_nodes":{
                "learning_objects":[context.lo_uuid]
            }
        })
    learning_resource_data = learning_resource.json()
    context.uuid= learning_resource_data["data"]["uuid"]

    lo_object = get_method(
        url = f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-object/{context.lo_uuid}"
    )
    assert lo_object.status_code == 200
    lo_object = lo_object.json()["data"]
    assert lo_object["child_nodes"]["learning_resources"][0] == context.uuid 

    context.res = put_method(
        url=f"{API_URL}/content-serving/link/{context.uuid}",
        request_body = {
            "resource_path": context.content_serving_uri,
            "type": "html_package"
        }
    )
    context.res_json = context.res.json()

    assert context.res.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json[
        "message"] == "Successfully linked learning resource with content"
    context.new_resource_uuid = context.res_json["data"]["resource_uuid"]

    context.res = put_method(
        url=f"{API_URL}/content-serving/publish/{context.uuid}",
        query_params={"target_version_uuid":context.new_resource_uuid},
        request_body={}
    )
    context.res_json = context.res.json()
    assert context.res.status_code == 200
    assert context.res_json["message"] == "Successfully published content"

    context.res = put_method(
        url=f"{API_URL}/content-serving/link/{context.uuid}",
        request_body = {
            "resource_path": context.content_serving_uri,
            "type": "html_package"
        }
    )
    context.res_json = context.res.json()

    assert context.res.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json[
        "message"] == "Successfully linked learning resource with content"

    context.new_resource_uuid_1 = context.res_json["data"]["resource_uuid"]

    context.res = put_method(
        url=f"{API_URL}/content-serving/publish/{context.new_resource_uuid}",
        query_params={"target_version_uuid":context.new_resource_uuid_1},
        request_body={}
    )
    context.res_json = context.res.json()

    assert context.res.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json["message"] == "Successfully published content"

@behave.when("API request is sent to republish a valid learning content version")
def step_impl_2(context):
    context.res = put_method(
        url=f"{API_URL}/content-serving/publish/{context.new_resource_uuid_1}",
        query_params= {
            "target_version_uuid": context.new_resource_uuid
        },
        request_body={}
    )
    context.res_json = context.res.json()
    context.new_resource_uuid_2 = context.res_json["data"]["resource_uuid"]

@behave.then("LOS will return a json response with signed URl for preview of published content and new content uuid")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json["message"] == "Successfully published content"

    res_1 = get_method(
      url=f"{API_URL}/learning-resource/{context.new_resource_uuid}")
    res_json_1 = res_1.json()
    assert res_1.status_code == 200
    assert res_json_1["data"]["status"] == "unpublished"

    res_2 = get_method(
        url=f"{API_URL}/learning-resource/{context.new_resource_uuid_1}")
    res_json_2 = res_2.json()
    assert res_2.status_code == 200
    assert res_json_2["data"]["status"] == "unpublished"

    res_3 = get_method(
        url=f"{API_URL}/learning-resource/{context.new_resource_uuid_2}")
    res_json_3 = res_3.json()
    assert res_3.status_code == 200
    assert res_json_3["data"]["status"] == "published"

    lo_object = get_method(
        url = f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-object/{context.lo_uuid}"
    )
    assert lo_object.status_code == 200
    lo_object = lo_object.json()["data"]
    assert lo_object["child_nodes"]["learning_resources"][0] == context.new_resource_uuid_2 

# -----------------------------------------------------
# Scenario 4: User wants to publish invalid learning content version
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to publish invalid learning content version")
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
    learning_resource = post_method(
        url=f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-resource",
        request_body={
            **context.payload, 
            "resource_path":"",
            "type":"",
            "parent_nodes":{
                "learning_objects":[]
            }
        })
    learning_resource_data = learning_resource.json()
    context.uuid= learning_resource_data["data"]["uuid"]

    context.res = put_method(
        url=f"{API_URL}/content-serving/link/{context.uuid}",
        request_body = {
            "resource_path": context.content_serving_uri,
            "type": "html_package"
        }
    )
    context.res_json = context.res.json()

    assert context.res.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json[
        "message"] == "Successfully linked learning resource with content"
    context.invalid_content_version = "random_uuid"

@behave.when("API request is sent to to publish invalid learning content version")
def step_impl_2(context):
    context.res = put_method(
        url=f"{API_URL}/content-serving/publish/{context.uuid}",
        query_params={"target_version_uuid":context.invalid_content_version},
        request_body={}
    )
    context.res_json = context.res.json()

@behave.then("LOS will return a resource is not found error response for invalid learning content version")
def step_impl_3(context):
    assert context.res.status_code == 404
    assert context.res_json["success"] is False
    assert context.res_json[
        "message"] == f"Learning Resource with uuid {context.invalid_content_version} not found"

# -----------------------------------------------------
# Scenario 5: User wants to publish invalid learning resource
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to publish invalid learning resource")
def step_impl_1(context):
    context.gcs_object = GcsCrudService(CONTENT_SERVING_BUCKET)
    context.content_serving_uri = context.gcs_object.upload_file_to_bucket(
                                        "learning-resources/dev_testing/testing-files",
                                        "content_serving.html", TEST_CONTENT_SERVING_PATH)
    context.content_serving_uri = context.content_serving_uri.split("learning-resources/")[1]
    
    context.uuid= "random_learning_resource_uuid"
    context.new_resource_uuid = "random_content_version_uuid"

@behave.when("API request is sent to to publish invalid learning resource")
def step_impl_2(context):
    context.res = put_method(
        url=f"{API_URL}/content-serving/publish/{context.uuid}",
        query_params={
            "target_version_uuid": context.new_resource_uuid
        },
        request_body={}
    )
    context.res_json = context.res.json()

@behave.then("LOS will return a resource is not found error response for invalid learning resource")
def step_impl_3(context):
    assert context.res.status_code == 404
    assert context.res_json["success"] is False
    assert context.res_json[
        "message"] == f"Learning Resource with uuid {context.uuid} not found"