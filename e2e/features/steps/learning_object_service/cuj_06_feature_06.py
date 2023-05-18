"""
    User should be able to upload a learning content with sync api
"""
import behave
import sys

sys.path.append("../")
from setup import post_method
from environment import TEST_CONTENT_SERVING_PDF_PATH, TEST_CONTENT_SERVING_ZIP_PATH
from test_config import API_URL_LEARNING_OBJECT_SERVICE

API_URL = API_URL_LEARNING_OBJECT_SERVICE
LEARNING_RESOURCE_UUID=""

# -----------------------------------------------------
# Scenario 1: User wants to upload a learning content file with sync api
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to upload a learning content file with sync api")
def step_impl_1(context):
    pass

@behave.when("API request is sent to upload a learning content file with sync api")
def step_impl_2(context):
    content_file = open(TEST_CONTENT_SERVING_PDF_PATH,"rb")
    content_file_input_dict = {"content_file":
              ("content_serving_sample_upload_pdf.pdf", content_file, "application/pdf")}

    content_res = post_method(
            url=f"{API_URL_LEARNING_OBJECT_SERVICE}/content-serving/upload/sync",
            files=content_file_input_dict,
            )
    context.res_json = content_res.json()
    context.status_code = content_res.status_code

@behave.then("LOS will return a json response with file and folder list of the uploaded file")
def step_impl_3(context):
    assert context.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json["message"] == "Successfully uploaded the learning content"
    assert context.res_json["data"].get("prefix") is not None
    assert context.res_json["data"].get("files") is not None
    assert context.res_json["data"].get("folders") is not None


# -----------------------------------------------------
# Scenario 2: User wants to upload a learning content zip with sync api
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to upload a learning content zip with sync api")
def step_impl_1(context):
    pass

@behave.when("API request is sent to upload a learning content zip with sync api")
def step_impl_2(context):
    content_file = open(TEST_CONTENT_SERVING_ZIP_PATH,"rb")
    content_file_input_dict = {"content_file":
              ("content_serving_sample_upload_scorm.zip", content_file, "application/zip")}

    content_res = post_method(
            url=f"{API_URL_LEARNING_OBJECT_SERVICE}/content-serving/upload/sync",
            files=content_file_input_dict
            )
    context.res_json = content_res.json()
    context.status_code = content_res.status_code

@behave.then("LOS will return a json response with file and folder list of the uploaded zip")
def step_impl_3(context):
    assert context.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json["message"] == "Successfully uploaded the learning content"
    assert context.res_json["data"].get("prefix") is not None
    assert context.res_json["data"].get("files") is not None
    assert context.res_json["data"].get("folders") is not None

# -----------------------------------------------------
# Scenario 3: User wants to upload a learning content with invalid content headers
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to upload a learning content file with invalid content headers")
def step_impl_1(context):
    pass

@behave.when("API request is sent to upload a learning content file with invalid content headers")
def step_impl_2(context):
    content_file = open(TEST_CONTENT_SERVING_PDF_PATH,"rb")
    content_file_input_dict = {"content_file":
              ("content_serving_sample_upload_pdf.pdf", content_file, "application/abc")}

    content_res = post_method(
            url=f"{API_URL_LEARNING_OBJECT_SERVICE}/content-serving/upload/sync",
            files=content_file_input_dict,
            )
    context.res_json = content_res.json()
    context.status_code = content_res.status_code

@behave.then("LOS will return a validation error for invalid content headers")
def step_impl_3(context):
    assert context.status_code == 422
    assert context.res_json["success"] is False
    assert context.res_json["message"] == "content_type not allowed"

# -----------------------------------------------------
# Scenario 4: User wants to upload a learning content where content headers and file extension does not match
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to upload a learning content file where content headers and file extension does not match")
def step_impl_1(context):
    pass

@behave.when("API request is sent to upload a learning content file where content headers and file extension does not match")
def step_impl_2(context):
    context.invalid_content_type = "application/zip"
    context.file_extension = "pdf"

    content_file = open(TEST_CONTENT_SERVING_PDF_PATH,"rb")
    content_file_input_dict = {"content_file":
              ("content_serving_sample_upload_pdf.pdf", content_file, context.invalid_content_type)}

    content_res = post_method(
            url=f"{API_URL_LEARNING_OBJECT_SERVICE}/content-serving/upload/sync",
            files=content_file_input_dict,
            )
    context.res_json = content_res.json()
    context.status_code = content_res.status_code

@behave.then("LOS will return a validation error for mismatched content headers and file extension")
def step_impl_3(context):
    assert context.status_code == 422
    assert context.res_json["success"] is False
    assert context.res_json["message"] == f"Content Type header and file extension does not match. Received header contentType: {context.invalid_content_type}, received file extension .{context.file_extension}"