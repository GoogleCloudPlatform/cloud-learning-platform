"""
Feature 4 - Learner can download a zip containing all files linked to an assessment
"""

import sys
import behave
from uuid import uuid4
sys.path.append("../")
from common.models import (Assessment, User)
from e2e.setup import post_method, get_method, set_cache, get_cache, delete_test_files_from_gcs
from environment import TEST_ASSESSMENT_SUBMISSION_FILE_PATH
from e2e.test_object_schemas import (TEST_FINAL_ASSESSMENT,
                                  TEST_USER)
from e2e.test_config import API_URL_ASSESSMENT_SERVICE

API_URL = API_URL_ASSESSMENT_SERVICE

#------------------------------------------------------------------------------
# Scenario 1: Learner wants to download a zip containing all files linked to an assessment
#------------------------------------------------------------------------------
@behave.given(
    "that valid assessment with linked resources exists"
)
def step_impl_1(context):
  # Create Assessor
  assessor_dict = {**TEST_USER}
  assessor_dict["email"] = f"{uuid4()}@gmail.com"
  assessor = User.from_dict(assessor_dict)
  assessor.user_type_ref=""
  assessor.user_id = ""
  assessor.user_type = "assessor"
  assessor.save()
  assessor.user_id = assessor.id
  assessor.update()
  context.user_id = assessor.user_id

  # Create Assessment
  assessment_dict = {**TEST_FINAL_ASSESSMENT}
  assessment_dict["name"] = "Questionnaire"
  assessment = Assessment.from_dict(assessment_dict)
  assessment.uuid = ""
  assessment.author_id = assessor.user_id
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()

  context.assessment_uuid = assessment.uuid

  # Upload Files for Assessment
  content_file = open(TEST_ASSESSMENT_SUBMISSION_FILE_PATH,"rb")
  content_file_input_dict = {"content_file":
              ("sample_assessment_authoring_1.txt", content_file, "text/plain")}

  content_res = post_method(
            url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-authoring/upload-sync/{context.user_id}",
            files=content_file_input_dict,
            )
  assert content_res.status_code == 200
  res_json_1 = content_res.json()

  content_file_input_dict = {"content_file":
              ("sample_assessment_authoring_2.txt", content_file, "text/plain")}

  content_res = post_method(
            url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-authoring/upload-sync/{context.user_id}",
            files=content_file_input_dict,
            )
  assert content_res.status_code == 200
  res_json_2 = content_res.json()

  # Link Files
  context.valid_resource_path_1 = res_json_1["data"]["resource_path"]
  context.valid_resource_path_2 = res_json_2["data"]["resource_path"]

  assessment = Assessment.find_by_uuid(context.assessment_uuid)
  assessment.resource_paths = [
    context.valid_resource_path_1,
    context.valid_resource_path_2,
  ]
  assessment.update()

  # Set Cache
  set_cache("assessment_for_download_content", context.assessment_uuid)

@behave.when(
    "API request is sent to download zip of all contents"
)
def step_impl_2(context):
  res = get_method(
    url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-content/{context.assessment_uuid}/download-all"
  )
  context.res = res

@behave.then(
  "the API will return a zip file"
)
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res.headers["content-type"] == "application/zip"
  assert context.res.content is not None

  # Delete Uploaded File
  files_to_delete = [context.valid_resource_path_1, context.valid_resource_path_2]
  delete_test_files_from_gcs(files_to_delete)

#------------------------------------------------------------------------------
# Scenario 2: Learner wants to download a zip but some files are missing on GCS
#------------------------------------------------------------------------------
@behave.given(
    "that valid assessment but some files are missing"
)
def step_impl_1(context):
  context.assessment_uuid = get_cache("assessment_for_download_content")

  assessment = Assessment.find_by_uuid(context.assessment_uuid)
  resource_paths = assessment.resource_paths
  resource_paths.append("random_file_name")
  assessment.resource_paths = resource_paths
  assessment.update()

@behave.when(
    "API request is sent to download zip with missing contents"
)
def step_impl_2(context):
  res = get_method(
    url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-content/{context.assessment_uuid}/download-all"
  )
  context.res = res

@behave.then(
  "the API will return an error saying some files are missing on GCS"
)
def step_impl_3(context):
  assert context.res.status_code == 404
  res_json = context.res.json()
  assert res_json["success"] is False
  assert "Total missing files:" in res_json["message"]

#------------------------------------------------------------------------------
# Scenario 3: Learner wants to download a zip but no files are linked to the assessment
#------------------------------------------------------------------------------
@behave.given(
    "that valid assessment but no files are linked to the assessment"
)
def step_impl_1(context):
  context.assessment_uuid = get_cache("assessment_for_download_content")

  assessment = Assessment.find_by_uuid(context.assessment_uuid)
  assessment.resource_paths = []
  assessment.update()

@behave.when(
    "API request is sent to download zip of missing contents"
)
def step_impl_2(context):
  res = get_method(
    url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-content/{context.assessment_uuid}/download-all"
  )
  context.res = res

@behave.then(
  "the API will return an error saying no files are linked to the assessment"
)
def step_impl_3(context):
  assert context.res.status_code == 422
  res_json = context.res.json()
  assert res_json["success"] is False
  assert "Cannot generate zip" in res_json["message"]
