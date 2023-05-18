"""
    User wants to list contents from content serving bucket based on prefix
"""
import behave
import sys

sys.path.append("../")
from setup import get_method
from test_config import API_URL_LEARNING_OBJECT_SERVICE

API_URL = API_URL_LEARNING_OBJECT_SERVICE
LEARNING_RESOURCE_UUID=""

# -----------------------------------------------------
# Scenario 1: User wants to list content from GCS bucket
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to list content from GCS bucket")
def step_impl_1(context):
    context.prefix = "abc/"

@behave.when("API request is sent to list content from GCS bucket")
def step_impl_2(context):
    context.res = get_method(
        url=f"{API_URL}/content-serving/list-contents", 
        query_params={"prefix": context.prefix})
    context.res_json = context.res.json()

@behave.then("LOS will return a json response with file and folder list")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json[
        "message"] == "Successfully listed all files and folder at given prefix"
    assert context.res_json["data"]["prefix"] == context.prefix


# -----------------------------------------------------
# Scenario 2: User wants to list content from GCS bucket with no prefix
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to list content from GCS bucket without a prefix")
def step_impl_1(context):
    pass

@behave.when("API request is sent to list content from GCS bucket without prefix")
def step_impl_2(context):
    context.res = get_method(
        url=f"{API_URL}/content-serving/list-contents")
    context.res_json = context.res.json()

@behave.then("LOS will return data present at the root of the bucket")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json["message"] == "Successfully listed all files and folder at given prefix"
    assert context.res_json["data"]["prefix"] == ""
