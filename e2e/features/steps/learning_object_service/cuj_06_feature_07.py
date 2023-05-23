"""
    User should be able to upload a learning content with async api
"""
import behave
import sys
import time

sys.path.append("../")
from e2e.setup import post_method, get_method
from environment import TEST_CONTENT_SERVING_PDF_PATH, TEST_CONTENT_SERVING_ZIP_PATH
from e2e.test_config import API_URL_LEARNING_OBJECT_SERVICE

API_URL = API_URL_LEARNING_OBJECT_SERVICE
LEARNING_RESOURCE_UUID=""
VALIDATE_AND_UPLOAD_ZIP = "validate_and_upload_zip"

# -----------------------------------------------------
# Scenario 1: User wants to upload a learning content with async api
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to upload a learning content zip with async api")
def step_impl_1(context):
    pass

@behave.when("API request is sent to upload a learning content zip with async api")
def step_impl_2(context):
    content_file = open(TEST_CONTENT_SERVING_ZIP_PATH,"rb")
    content_file_input_dict = {"content_file":
              ("content_serving_sample_upload_scorm.zip", content_file, "application/zip")}

    content_res = post_method(
            url=f"{API_URL_LEARNING_OBJECT_SERVICE}/content-serving/upload/async",
            files=content_file_input_dict
            )
    context.res_json = content_res.json()
    context.status_code = content_res.status_code

@behave.then("LOS will return a json response with file and folder list of the uploaded zip for async api")
def step_impl_3(context):
    assert context.status_code == 200
    assert context.res_json["success"] is True

    assert context.res_json["message"] == "Successfully initiated the job with type 'validate_and_upload_zip'. Please use the job name to track the job status"


    context.job_name = context.res_json["data"]["job_name"]
    batch_job_url = f"{API_URL_LEARNING_OBJECT_SERVICE}/jobs/{VALIDATE_AND_UPLOAD_ZIP}/{context.job_name}"

    for i in range(40):
        time.sleep(3)

        res = get_method(
            url=batch_job_url
        )
        
        json_data = res.json()
        if json_data["data"]["status"] in ["succeeded","failed"]:
            break

    print(json_data)
    assert json_data["data"]["status"] == "succeeded"


# -----------------------------------------------------
# Scenario 2: User wants to upload a learning content with invalid content headers with async api
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to upload a learning content file with invalid content headers with async api")
def step_impl_1(context):
    pass

@behave.when("API request is sent to upload a learning content file with invalid content headers with async api")
def step_impl_2(context):
    context.invalid_content_type = "application/abc"

    content_file = open(TEST_CONTENT_SERVING_ZIP_PATH,"rb")
    content_file_input_dict = {"content_file":
              ("content_serving_sample_upload_scorm.zip", content_file, context.invalid_content_type)}

    content_res = post_method(
            url=f"{API_URL_LEARNING_OBJECT_SERVICE}/content-serving/upload/async",
            files=content_file_input_dict
            )
    context.res_json = content_res.json()
    context.status_code = content_res.status_code

@behave.then("LOS will return a validation error for invalid content headers for async api")
def step_impl_3(context):
    assert context.status_code == 422
    assert context.res_json["success"] is False
    assert context.res_json["message"] == "Content Type as application/zip is only supported"

# -----------------------------------------------------
# Scenario 3: User wants to upload a learning content where content headers and file extension does not match
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to upload a learning content zip where content headers and file extension does not match")
def step_impl_1(context):
    pass

@behave.when("API request is sent to upload a learning content file where content headers and zip file extension does not match")
def step_impl_2(context):

    content_file = open(TEST_CONTENT_SERVING_PDF_PATH,"rb")
    content_file_input_dict = {"content_file":
              ("content_serving_sample_upload_pdf.pdf", content_file, "application/zip")}

    content_res = post_method(
            url=f"{API_URL_LEARNING_OBJECT_SERVICE}/content-serving/upload/async",
            files=content_file_input_dict
            )
    context.res_json = content_res.json()
    context.status_code = content_res.status_code

@behave.then("LOS will return a validation error for mismatched content headers and file extension for async api")
def step_impl_3(context):
    assert context.status_code == 422
    assert context.res_json["success"] is False
    assert context.res_json["message"] == "Content Type header and file extension does not match. Received header contentType: application/zip, received file extension .pdf"