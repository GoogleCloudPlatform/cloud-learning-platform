"""
Feature 4 - Delete uploaded files during assessment authoring and submission
"""

import sys
import behave
from uuid import uuid4
sys.path.append("../")
from common.models import (User, Assessment, Learner, LearnerProfile)
from e2e.setup import post_method, put_method, set_cache, get_cache
from environment import TEST_ASSESSMENT_SUBMISSION_FILE_PATH
from e2e.test_object_schemas import (TEST_FINAL_ASSESSMENT,
                                  TEST_SUBMITTED_ASSESSMENT_INPUT,
                                  TEST_LEARNER,
                                  TEST_USER,
                                  LEARNER_PROFILE_TEMPLATE,
                                  TEST_PRACTICE_ASSESSMENT)
from e2e.test_config import API_URL_ASSESSMENT_SERVICE

API_URL = API_URL_ASSESSMENT_SERVICE

#------------------------------------------------------------------------------
# Scenario 1: User wants to delete uploaded file during assessment authoring
#------------------------------------------------------------------------------
@behave.given(
    "that valid user_id exists and files are successfully uploaded"
)
def step_impl_1(context):
  # Create Assessor
  user_dict = {**TEST_USER}
  user_dict["email"] = f"{uuid4()}@gmail.com"
  user = User.from_dict(user_dict)
  user.user_type_ref=""
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  context.user_id = user.user_id

  # Upload File
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

  print(context.input_file_list)

  set_cache("user_for_assessment_content_delete", context.user_id)

@behave.when(
    "API request is sent to delete a file from temp folder of the user"
)
def step_impl_2(context):
  res = put_method(
    url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-authoring/delete-file/{context.user_id}",
    request_body={
      "file_list": context.input_file_list
    }
  )
  print(res.status_code)
  print(res.json())
  context.status_code = res.status_code
  context.res_json = res.json()

@behave.then(
  "the API will successfully delete the file from temp folder of the user"
)
def step_impl_3(context):
  assert context.status_code == 200
  assert context.res_json["success"] is True
  assert context.res_json["message"] == f"Successfully deleted files for user with uuid {context.user_id}"

  for i,file in enumerate(context.input_file_list):
      context.input_file_list[i] = file.split('/')[-1]
  
  assert context.input_file_list == context.res_json["data"]

#------------------------------------------------------------------------------
# Scenario 2: User wants to delete uploaded file during assessment authoring but invalid path is sent
#------------------------------------------------------------------------------
@behave.given(
    "that valid user_id exists but the file to be deleted does not exist"
)
def step_impl_1(context):
  context.user_id = get_cache("user_for_assessment_content_delete")
  context.input_file_list = ["some_random_path"]

@behave.when(
    "API request is sent to delete a file from temp folder of the user with invalid path"
)
def step_impl_2(context):
  res = put_method(
    url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-authoring/delete-file/{context.user_id}",
    request_body={
      "file_list": context.input_file_list
    }
  )
  print(res.status_code)
  print(res.json())
  context.status_code = res.status_code
  context.res_json = res.json()

@behave.then(
  "the API will return resource not found error for the file to be deleted from temp folder of the user"
)
def step_impl_3(context):
  assert context.status_code == 404
  assert context.res_json["success"] is False
  assert "Total missing files: 1" in context.res_json["message"]

#------------------------------------------------------------------------------
# Scenario 3: User wants to delete uploaded file during assessment subission
#------------------------------------------------------------------------------
@behave.given(
    "that valid learner_id and assessment_id exists and files are successfully uploaded"
)
def step_impl_1(context):
  # Create Assessment
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

  # Upload File
  content_file = open(TEST_ASSESSMENT_SUBMISSION_FILE_PATH,"rb")
  content_file_input_dict = {"content_file":
              ("sample_assessment_submission_1.txt", content_file, "text/plain")}

  content_res = post_method(
            url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-submission/upload-sync/{context.learner_id}/{context.assessment_id}",
            files=content_file_input_dict,
            )
  assert content_res.status_code == 200
  res_json = content_res.json()

  context.input_file_list = [res_json["data"]["resource_path"]]

  print(context.input_file_list)

  set_cache("learner_for_assessment_content_delete", context.learner_id)
  set_cache("assessment_for_assessment_content_delete", context.assessment_id)

@behave.when(
    "API request is sent to delete a file from temp folder of the learner"
)
def step_impl_2(context):
  res = put_method(
    url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-submission/delete-file/{context.learner_id}/{context.assessment_id}",
    request_body={
      "file_list": context.input_file_list
    }
  )
  print(res.status_code)
  print(res.json())
  context.status_code = res.status_code
  context.res_json = res.json()

@behave.then(
  "the API will successfully delete the file from temp folder of the learner"
)
def step_impl_3(context):
  assert context.status_code == 200
  assert context.res_json["success"] is True
  assert context.res_json["message"] == f"Successfully deleted files for Learner with uuid {context.learner_id} against Assessment with uuid {context.assessment_id}"

  for i,file in enumerate(context.input_file_list):
      context.input_file_list[i] = file.split('/')[-1]
  
  assert context.input_file_list == context.res_json["data"]

#------------------------------------------------------------------------------
# Scenario 4: User wants to delete uploaded file during assessment subission but invalid path is sent
#------------------------------------------------------------------------------
@behave.given(
    "that valid learner_id and assessment_id exists but the file to be deleted does not exist"
)
def step_impl_1(context):
  context.learner_id = get_cache("learner_for_assessment_content_delete")
  context.assessment_id = get_cache("assessment_for_assessment_content_delete")
  context.input_file_list = ["some_random_path"]

@behave.when(
    "API request is sent to delete a file from temp folder of the learner with invalid path"
)
def step_impl_2(context):
  res = put_method(
    url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-submission/delete-file/{context.learner_id}/{context.assessment_id}",
    request_body={
      "file_list": context.input_file_list
    }
  )
  print(res.status_code)
  print(res.json())
  context.status_code = res.status_code
  context.res_json = res.json()

@behave.then(
  "the API will return resource not found error for the file to be deleted from temp folder of the learner"
)
def step_impl_3(context):
  assert context.status_code == 404
  assert context.res_json["success"] is False
  assert "Total missing files: 1" in context.res_json["message"]
