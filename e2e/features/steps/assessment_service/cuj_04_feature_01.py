"""
Feature 4 - Upload File for Assessment Submission
"""

import sys
import behave
sys.path.append("../")
from common.models import (Assessment, Learner, LearnerProfile)
from e2e.setup import post_method, set_cache, get_cache, delete_test_files_from_gcs
from environment import TEST_ASSESSMENT_SUBMISSION_FILE_PATH
from e2e.test_object_schemas import (TEST_PRACTICE_ASSESSMENT, TEST_LEARNER, LEARNER_PROFILE_TEMPLATE)
from e2e.test_config import API_URL_ASSESSMENT_SERVICE
import json

API_URL = API_URL_ASSESSMENT_SERVICE

#------------------------------------------------------------------------------
# Scenario 1: Learner wants to upload a single file for assessment submission
#------------------------------------------------------------------------------
@behave.given(
    "that valid learner and assessment exists"
)
def step_impl_1(context):
  assessment_dict = {**TEST_PRACTICE_ASSESSMENT}
  assessment_dict["name"] = "CLP TEST"
  assessment = Assessment.from_dict(assessment_dict)
  assessment.uuid = ""
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()
  assessment_dict["uuid"] = assessment.id

  learner_dict = TEST_LEARNER
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()
  learner_dict["uuid"] = learner.id
  learner_dict["is_archived"] = False

  learner_profile_dict = {**LEARNER_PROFILE_TEMPLATE}
  learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  learner_profile.learner_id = learner.uuid
  learner_profile.uuid = ""
  learner_profile.save()
  learner_profile.uuid = learner_profile.id
  learner_profile.progress = {"assessments":{assessment.uuid :{"name":"content_upload","num_attempts":1}}}
  learner_profile.update()
  learner_profile_dict["uuid"] = learner_profile.id
  learner_profile_dict["is_archived"] = False

  context.assessment_id = assessment.id
  context.learner_id = learner.id

  set_cache("assessment_id_for_file_upload", assessment.id)
  set_cache("learner_id_for_file_upload", learner.id)
  set_cache("learner_profile_id_for_file_upload", learner_profile.id)
  set_cache("max_attempt",assessment.max_attempts)
@behave.when(
    "API request is sent to upload a file for assessment submission"
)
def step_impl_2(context):
  content_file = open(TEST_ASSESSMENT_SUBMISSION_FILE_PATH,"rb")
  content_file_input_dict = {"content_file":
              ("sample_assessment_submission.txt", content_file, "text/plain")}

  content_res = post_method(
            url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-submission/upload-sync/{context.learner_id}/{context.assessment_id}",
            files=content_file_input_dict,
            )
  context.res_json = content_res.json()
  context.status_code = content_res.status_code

@behave.then("the API will upload file to learner-id/assessment-id/temp folder on GCS")
def step_impl_3(context):
    assert context.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json["message"] == "Successfully uploaded file"

    expected_file_path = f"submissions/{context.learner_id}/{context.assessment_id}"
    expected_file_path+="/temp/sample_assessment_submission.txt"

    assert context.res_json["data"]["resource_path"] == expected_file_path

    files_to_delete = [context.res_json["data"]["resource_path"]]
    set_cache("files_to_delete", json.dumps(files_to_delete))

#------------------------------------------------------------------------------
# Scenario 2: Learner wants to reupload a file with same name for assessment submission
#------------------------------------------------------------------------------
@behave.given(
    "that valid learner and assessment exists and file is already uploaded"
)
def step_impl_1(context):
  context.assessment_id = get_cache("assessment_id_for_file_upload")
  context.learner_id = get_cache("learner_id_for_file_upload")

@behave.when(
    "API request is sent to reupload a file for assessment submission"
)
def step_impl_2(context):
  content_file = open(TEST_ASSESSMENT_SUBMISSION_FILE_PATH,"rb")
  content_file_input_dict = {"content_file":
              ("sample_assessment_submission.txt", content_file, "text/plain")}

  content_res = post_method(
            url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-submission/upload-sync/{context.learner_id}/{context.assessment_id}",
            files=content_file_input_dict,
            )
  context.res_json = content_res.json()
  context.status_code = content_res.status_code

@behave.then("the API will respond with validation error for already existing file with same name for same assessment")
def step_impl_3(context):
    assert context.status_code == 422
    assert context.res_json["success"] is False
    assert context.res_json["message"] == f"File with same name already exists"

    # Delete Uploaded File
    files_to_delete = json.loads(get_cache("files_to_delete"))
    delete_test_files_from_gcs(files_to_delete)

#------------------------------------------------------------------------------
# Scenario 3: Learner wants to upload a file for assessment submission with invalid assessment_id
#------------------------------------------------------------------------------
@behave.given(
    "that learner_id is valid but assessment_id is invalid"
)
def step_impl_1(context):
  context.assessment_id = "invalid_assessment_id"
  context.learner_id = get_cache("learner_id_for_file_upload")

@behave.when(
    "API request is sent to upload a file for assessment submission with invalid assessment_id"
)
def step_impl_2(context):
  content_file = open(TEST_ASSESSMENT_SUBMISSION_FILE_PATH,"rb")
  content_file_input_dict = {"content_file":
              ("sample_assessment_submission_1.txt", content_file, "text/plain")}

  content_res = post_method(
            url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-submission/upload-sync/{context.learner_id}/{context.assessment_id}",
            files=content_file_input_dict,
            )
  context.res_json = content_res.json()
  context.status_code = content_res.status_code

@behave.then("the API will respond with validation error for invalid assessment_id")
def step_impl_3(context):
  assert context.status_code == 404
  assert context.res_json["success"] is False
  assert context.res_json["message"] == f"Assessment with uuid {context.assessment_id} not found"

#------------------------------------------------------------------------------
# Scenario 4: Learner wants to upload a file for assessment submission with invalid learner_id
#------------------------------------------------------------------------------
@behave.given(
    "that learner_id is invalid but assessment_id is valid"
)
def step_impl_1(context):
  context.assessment_id = get_cache("assessment_id_for_file_upload")
  context.learner_id = "invalid_learner_id"

@behave.when(
    "API request is sent to upload a file for assessment submission with invalid learner_id"
)
def step_impl_2(context):
  content_file = open(TEST_ASSESSMENT_SUBMISSION_FILE_PATH,"rb")
  content_file_input_dict = {"content_file":
              ("sample_assessment_submission_2.txt", content_file, "text/plain")}

  content_res = post_method(
            url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-submission/upload-sync/{context.learner_id}/{context.assessment_id}",
            files=content_file_input_dict,
            )
  context.res_json = content_res.json()
  print(context.res_json,"#"*10)
  context.status_code = content_res.status_code

@behave.then("the API will respond with validation error for invalid learner_id")
def step_impl_3(context):
  assert context.status_code == 422
  assert context.res_json["success"] is False
  assert context.res_json["message"] == f"No learner profile with learner id {context.learner_id} found"


#------------------------------------------------------------------------------
# Scenario 5: Learner wants to upload a file for assessment submission with current attempt greater than max attempt
#------------------------------------------------------------------------------
@behave.given(
    "that valid learner,learner profile and assessment exists"
)
def step_impl_1(context):
  context.assessment_id = get_cache("assessment_id_for_file_upload")
  context.learner_id = get_cache("learner_id_for_file_upload")
  learner_profile = LearnerProfile.find_by_id(get_cache("learner_profile_id_for_file_upload"))
  learner_profile_dict = learner_profile.get_fields()
  learner_profile_dict["progress"] = {"assessments":{context.assessment_id :{"name":"content_upload","num_attempts":5}}}
  learner_profile.progress = learner_profile_dict["progress"]
  learner_profile.update()
  context.current_attempt = learner_profile_dict["progress"]["assessments"][context.assessment_id]["num_attempts"]
  context.max_attempt = get_cache("max_attempt")

@behave.when(
    "API request is sent to upload a file for assessment submission with current attempt greater than max attempt"
)
def step_impl_2(context):
  content_file = open(TEST_ASSESSMENT_SUBMISSION_FILE_PATH,"rb")
  content_file_input_dict = {"content_file":
              ("sample_assessment_submission_2.txt", content_file, "text/plain")}

  content_res = post_method(
            url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-submission/upload-sync/{context.learner_id}/{context.assessment_id}",
            files=content_file_input_dict,
            )
  context.res_json = content_res.json()
  context.status_code = content_res.status_code
  

@behave.then("the API will respond with validation error for  current attempt greater than max attempt")
def step_impl_3(context):
  assert context.status_code == 422
  assert context.res_json["success"] is False
  assert context.res_json["message"] == f"current attempt {context.current_attempt} cannot be greater than max attempts {context.max_attempt}"

