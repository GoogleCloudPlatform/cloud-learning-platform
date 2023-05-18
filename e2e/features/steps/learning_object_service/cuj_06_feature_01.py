"""
    Create Signed URls for video and HTML5 content
"""
import behave
import sys
from copy import copy

from common.utils.gcs_adapter import GcsCrudService

sys.path.append("../")
from setup import post_method, get_method, put_method, CONTENT_SERVING_BUCKET
from test_config import API_URL_LEARNING_OBJECT_SERVICE, DEL_KEYS
from test_object_schemas import (TEST_LEARNING_RESOURCE,)
from environment import TEST_CONTENT_SERVING_PATH
API_URL = API_URL_LEARNING_OBJECT_SERVICE
LEARNING_RESOURCE_UUID=""

# User wants a Signed URl to access video/HTML content and expecting response in json format

@behave.given("that an LXE or CD has access to the content authoring tool and want to Create a signed url for video/Html5 content and wants response in json format")
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
          **context.payload, "resource_path": context.content_serving_uri,
          "type":"html"
      })
  learning_resource_data = learning_resource.json()
  context.uuid= learning_resource_data["data"]["uuid"]
  context.url= f"{API_URL}/content-serving/{context.uuid}"
  context.params={"redirect": False}

@behave.when("API request is sent to create Signed Url with valid learning resource uuid and redirect as False")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("LOS will return a json response with signed URl")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["message"] == "Successfully fetched the signed url"

# User wants to redirect to a Signed URl to access video or HTML content 

@behave.given("that an LXE or CD has access to the content authoring tool and wants to redirect to signed url")
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
          "resource_path": context.content_serving_uri,
          "type": "html"
      })
  learning_resource_data = learning_resource.json()
  context.uuid= learning_resource_data["data"]["uuid"]
  context.url= f"{API_URL}/content-serving/{context.uuid}"
  context.params={"redirect": True}

@behave.when("API request is sent to create Signed Url with valid learning resource uuid and redirect as True")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)

@behave.then("LOS will serve the redirect response with signed url")
def step_impl_3(context):
  assert context.res.status_code == 307

# User wants a Signed URl to access video/HTML content with incorrect learning resource uuid

@behave.given("that an LXE or CD has access to the content authoring tool and want to Create a signed url for video/Html5 content providing invalid uuid")
def step_impl_1(context):
  
  context.uuid= "ghtyhfhgfhgyygvhj"
  context.url= f"{API_URL}/content-serving/{context.uuid}"
  context.params={"redirect": False}

@behave.when("API request is sent to create Signed Url with invalid learning resource uuid")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("LOS will not return signed url and throws ResourceNotFound error for learning resource")
def step_impl_3(context):
  assert context.res.status_code == 404
  assert context.res_data["message"] == f"Learning Resource with uuid {context.uuid} not found"

# User wants a Signed URl to access video/HTML content with correct learning resource uuid which has incorrect resource path

@behave.given("that an LXE or CD has access to the content authoring tool and want to Create a signed url for video/Html5 content which has incorrect resource path")
def step_impl_1(context):
  context.payload = TEST_LEARNING_RESOURCE
  for key in DEL_KEYS:
    if key in context.payload:
     del context.payload[key]
  learning_resource = post_method(
      url=f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-resource",
      request_body={
          **context.payload, 
          "resource_path": "dev_testing/content_serving.html",
          "type":"html"
      })
  learning_resource_data = learning_resource.json()
  context.uuid= learning_resource_data["data"]["uuid"]
  context.url= f"{API_URL}/content-serving/{context.uuid}"
  context.params={"redirect": False}

@behave.when("API request is sent to create Signed Url with valid learning resource uuid which has incorrect resource path")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("LOS will not return signed url and throws ResourceNotFound error for video/html5 content")
def step_impl_3(context):
  assert context.res.status_code == 404
  assert context.res_data["message"] == "Provided resource path does not exist on GCS bucket"

# User wants a Signed URl to access video/HTML content with correct learning resource uuid with empty resource path

@behave.given("that an LXE or CD has access to the content authoring tool and want to Create a signed url for video/Html5 for which resource path is empty")
def step_impl_1(context):
  context.payload = TEST_LEARNING_RESOURCE
  for key in DEL_KEYS:
    if key in context.payload:
     del context.payload[key]
  learning_resource = post_method(
      url=f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-resource",
      request_body={
          **context.payload, "resource_path": "",
          "type":"html"
      })
  learning_resource_data = learning_resource.json()
  context.uuid= learning_resource_data["data"]["uuid"]
  context.url= f"{API_URL}/content-serving/{context.uuid}"
  context.params={"redirect": False}

@behave.when("API request is sent to create Signed Url with valid learning resource uuid which has empty resource path")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()

@behave.then("LOS will not return signed url and throws ResourceNotFound error for resource path")
def step_impl_3(context):
  assert context.res.status_code == 404
  assert context.res_data["message"] == f"No resource path found for resource with uuid {context.uuid}"

