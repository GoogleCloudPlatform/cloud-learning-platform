"""
Feature 4 - Get files uploaded to temp folder on GCS
"""

import sys
import behave
from uuid import uuid4
sys.path.append("../")
from common.models import (Assessment, User, Learner, LearnerProfile)
from e2e.setup import post_method, get_method, delete_test_files_from_gcs
from environment import TEST_ASSESSMENT_SUBMISSION_FILE_PATH
from e2e.test_object_schemas import (TEST_PRACTICE_ASSESSMENT,
                                  TEST_LEARNER,
                                  TEST_USER,
                                  LEARNER_PROFILE_TEMPLATE)
from e2e.test_config import API_URL_ASSESSMENT_SERVICE

API_URL = API_URL_ASSESSMENT_SERVICE

#------------------------------------------------------------------------------
# Scenario 1: User wants to fetch the files present in the Assessment Author's temp folder on GCS
#------------------------------------------------------------------------------
@behave.given(
    "that valid user_id exists and files are successfully uploaded to Assessment Author's temp folder on GCS"
)
def step_impl_1(context):
  # Create Assessment Author
  user_dict = {**TEST_USER}
  user_dict["email"] = f"{uuid4()}@gmail.com"
  user = User.from_dict(user_dict)
  user.user_type_ref=""
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  context.user_id = user.user_id

  # Upload File to Temp
  content_file = open(TEST_ASSESSMENT_SUBMISSION_FILE_PATH,"rb")
  content_file_input_dict = {"content_file":
              ("sample_assessment_authoring_1.txt", content_file, "text/plain")}

  content_res = post_method(
            url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-authoring/upload-sync/{context.user_id}",
            files=content_file_input_dict,
            )
  assert content_res.status_code == 200
  res_json = content_res.json()

  context.input_file_list = [res_json["data"]["resource_path"]]

@behave.when(
    "API request is sent to get list of files from Assessment Author's temp folder on GCS"
)
def step_impl_2(context):
  res = get_method(
    url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-content/uploaded-files/{context.user_id}"
  )
  context.status_code = res.status_code
  context.res_json = res.json()

@behave.then(
  "the API will successfully fetch the files from Assessment Author's temp folder on GCS"
)
def step_impl_3(context):
  assert context.status_code == 200
  assert context.res_json["success"] is True
  assert context.res_json["message"] == f"Successfully fetched files list"
  assert len(context.res_json["data"]) == 1

  files_to_delete = []
  for record in context.res_json["data"]:
    assert f"assessments/{context.user_id}/temp/" in record["file_path"]
    files_to_delete.append(record["file_path"])

  # Delete Uploaded File
  delete_test_files_from_gcs(files_to_delete)

#------------------------------------------------------------------------------
# Scenario 2: User wants to fetch the files present in the Learner's temp folder on GCS
#------------------------------------------------------------------------------
@behave.given(
    "that valid user_id exists and files are successfully uploaded to Learner's temp folder on GCS"
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
  context.user_id = learner.id

  # Upload File to Temp
  content_file = open(TEST_ASSESSMENT_SUBMISSION_FILE_PATH,"rb")
  content_file_input_dict = {"content_file":
              ("sample_assessment_submission_1.txt", content_file, "text/plain")}

  content_res = post_method(
            url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-submission/upload-sync/{context.user_id}/{context.assessment_id}",
            files=content_file_input_dict,
            )
  assert content_res.status_code == 200

  context.input_file_list = [content_res.json()["data"]["resource_path"]]

@behave.when(
    "API request is sent to get list of files from Learner's temp folder on GCS"
)
def step_impl_2(context):
  res = get_method(
    url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-content/uploaded-files/{context.user_id}",
    query_params={
      "assessment_id": context.assessment_id
    }
  )
  context.status_code = res.status_code
  context.res_json = res.json()

@behave.then(
  "the API will successfully fetch the files from Learner's temp folder on GCS"
)
def step_impl_3(context):
  assert context.status_code == 200
  assert context.res_json["success"] is True
  assert context.res_json["message"] == f"Successfully fetched files list"
  assert len(context.res_json["data"]) == 1

  files_to_delete = []
  for record in context.res_json["data"]:
    assert f"submissions/{context.user_id}/{context.assessment_id}/temp/" in record["file_path"]
    files_to_delete.append(record["file_path"])

  # Delete Uploaded File
  delete_test_files_from_gcs(files_to_delete)
