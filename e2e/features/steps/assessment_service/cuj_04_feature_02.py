"""
Feature 4 - Upload File for Assessment Authoring
"""

import sys
import behave
from uuid import uuid4
sys.path.append("../")
from common.models import (User)
from e2e.setup import post_method, set_cache, get_cache, delete_test_files_from_gcs
from environment import TEST_ASSESSMENT_SUBMISSION_FILE_PATH
from e2e.test_object_schemas import (TEST_USER)
from e2e.test_config import API_URL_ASSESSMENT_SERVICE
import json

API_URL = API_URL_ASSESSMENT_SERVICE

#------------------------------------------------------------------------------
# Scenario 1: LXE wants to upload a single file for assessment authoring
#------------------------------------------------------------------------------
@behave.given(
    "that valid user_id exists"
)
def step_impl_1(context):
  user_dict = {**TEST_USER}
  user_dict["email"] = f"{uuid4()}@gmail.com"
  user = User.from_dict(user_dict)
  user.user_type_ref = ""
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  context.user_id = user.user_id

  set_cache("user_id_for_file_upload", user.user_id)

@behave.when(
    "API request is sent to upload a file for assessment authoring"
)
def step_impl_2(context):
  content_file = open(TEST_ASSESSMENT_SUBMISSION_FILE_PATH,"rb")
  content_file_input_dict = {"content_file":
              ("sample_assessment_authoring.txt", content_file, "text/plain")}

  content_res = post_method(
            url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-authoring/upload-sync/{context.user_id}",
            files=content_file_input_dict,
            )
  context.res_json = content_res.json()
  context.status_code = content_res.status_code

@behave.then("the API will upload file to user-id/temp folder on GCS")
def step_impl_3(context):
    assert context.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json["message"] == "Successfully uploaded file"

    expected_file_path = f"assessments/{context.user_id}"
    expected_file_path+="/temp/sample_assessment_authoring.txt"

    assert context.res_json["data"]["resource_path"] == expected_file_path

    files_to_delete = [context.res_json["data"]["resource_path"]]
    set_cache("files_to_delete", json.dumps(files_to_delete))

#------------------------------------------------------------------------------
# Scenario 2: LXE wants to reupload a file with same name for assessment authoring
#------------------------------------------------------------------------------
@behave.given(
    "that valid user_id exists and file is already uploaded"
)
def step_impl_1(context):
  context.user_id = get_cache("user_id_for_file_upload")

@behave.when(
    "API request is sent to reupload a file for assessment authoring"
)
def step_impl_2(context):
  content_file = open(TEST_ASSESSMENT_SUBMISSION_FILE_PATH,"rb")
  content_file_input_dict = {"content_file":
              ("sample_assessment_authoring.txt", content_file, "text/plain")}

  content_res = post_method(
            url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-authoring/upload-sync/{context.user_id}",
            files=content_file_input_dict,
            )
  context.res_json = content_res.json()
  context.status_code = content_res.status_code

@behave.then("the API will respond with validation error for already existing file with same name")
def step_impl_3(context):
    assert context.status_code == 422
    assert context.res_json["success"] is False
    assert context.res_json["message"] == f"File with same name already exists"

    # Delete Uploaded File
    files_to_delete = json.loads(get_cache("files_to_delete"))
    delete_test_files_from_gcs(files_to_delete)

#------------------------------------------------------------------------------
# Scenario 3: LXE wants to upload a file for assessment authoring with invalid user_id
#------------------------------------------------------------------------------
@behave.given(
    "that user_id is invalid"
)
def step_impl_1(context):
  context.user_id = "invalid_user_id"

@behave.when(
    "API request is sent to upload a file for assessment authoring with invalid user_id"
)
def step_impl_2(context):
  content_file = open(TEST_ASSESSMENT_SUBMISSION_FILE_PATH,"rb")
  content_file_input_dict = {"content_file":
              ("sample_assessment_authoring_1.txt", content_file, "text/plain")}

  content_res = post_method(
            url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-authoring/upload-sync/{context.user_id}",
            files=content_file_input_dict,
            )
  context.res_json = content_res.json()
  context.status_code = content_res.status_code

@behave.then("the API will respond with validation error for invalid user_id")
def step_impl_3(context):
  assert context.status_code == 404
  assert context.res_json["success"] is False
  assert context.res_json["message"] == f"User with user_id {context.user_id} not found"
