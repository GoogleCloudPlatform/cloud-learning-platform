"""
Feature 4 - Generate signed url for assessment contents
"""

import sys
import behave
from uuid import uuid4
sys.path.append("../")
from common.models import (Assessment, SubmittedAssessment, User, Learner, LearnerProfile)
from e2e.setup import post_method, get_method, set_cache, get_cache, delete_test_files_from_gcs
from environment import TEST_ASSESSMENT_SUBMISSION_FILE_PATH
from e2e.test_object_schemas import (TEST_FINAL_ASSESSMENT,
                                  TEST_SUBMITTED_ASSESSMENT_INPUT,
                                  TEST_LEARNER,
                                  TEST_USER,
                                  LEARNER_PROFILE_TEMPLATE)
from e2e.test_config import API_URL_ASSESSMENT_SERVICE
import json

API_URL = API_URL_ASSESSMENT_SERVICE

#------------------------------------------------------------------------------
# Scenario 1: LXE wants to generate signed URL for assessment contents
#------------------------------------------------------------------------------
@behave.given(
    "that valid assessment_id and resource paths exists"
)
def step_impl_1(context):
  # Create Assessment
  assessment_dict = {**TEST_FINAL_ASSESSMENT}
  assessment_dict["name"] = "Questionnaire"
  assessment = Assessment.from_dict(assessment_dict)
  assessment.uuid = ""
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()

  # Create User
  user_dict = {**TEST_USER}
  user_dict["email"] = f"{uuid4()}@gmail.com"
  user = User.from_dict(user_dict)
  user.user_type_ref=""
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  context.assessment_id = assessment.uuid
  context.user_id = user.user_id

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

  context.valid_resource_path_1 = res_json_1["data"]["resource_path"]
  context.valid_resource_path_2 = res_json_2["data"]["resource_path"]

  assessment = Assessment.find_by_uuid(assessment.uuid)
  assessment.resource_paths = [
    context.valid_resource_path_1,
    context.valid_resource_path_2,
  ]
  assessment.update()

  set_cache("assessment", assessment.uuid)
  set_cache("assessment_user", user.user_id)

@behave.when(
    "API request is sent to generate signed urls for assessment contents"
)
def step_impl_2(context):
  res = get_method(
    url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-content/{context.assessment_id}/signed-url"
  )
  context.status_code = res.status_code
  context.res_json = res.json()

@behave.then(
  "the API will return list of signed urls for assessment contents"
)
def step_impl_3(context):
  assert context.status_code == 200
  assert context.res_json["success"] == True
  assert context.res_json["message"] == "Successfully generated signed urls for all files"

  for record in context.res_json["data"]:
    assert record["signed_url"] is not None
    assert record["status"] == "Signed url generated successfully"

#------------------------------------------------------------------------------
# Scenario 2: LXE wants to generate signed URL for submitted assessment contents
#------------------------------------------------------------------------------
@behave.given(
    "that valid submitted_assessment_id and resource paths exists"
)
def step_impl_1(context):
  # Create Assessment
  assessment_id = get_cache("assessment")
  user_id = get_cache("assessment_user")

  # Create Learner
  learner_dict = TEST_LEARNER
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  #Create Learner Profile
  learner_profile_dict = {**LEARNER_PROFILE_TEMPLATE}
  learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  learner_profile.learner_id = learner.uuid
  learner_profile.uuid = ""
  learner_profile.save()
  learner_profile.uuid = learner_profile.id
  learner_profile.progress = {"assessments":{assessment_id:{"name":"content_upload","num_attempts":1}}}
  learner_profile.update()

  # Create Submitted Assessment
  sa_fields = {**TEST_SUBMITTED_ASSESSMENT_INPUT}
  sa_fields["assessment_id"] = assessment_id
  sa_fields["learner_id"] = user_id
  submitted_assessment = SubmittedAssessment()
  submitted_assessment = submitted_assessment.from_dict(sa_fields)
  submitted_assessment.uuid = ""
  submitted_assessment.save()
  submitted_assessment.uuid = submitted_assessment.id
  submitted_assessment.update()

  context.assessment_id = assessment_id
  context.submitted_assessment_id = submitted_assessment.uuid
  context.learner_id = learner.id

  # Upload Files for Assessment
  content_file = open(TEST_ASSESSMENT_SUBMISSION_FILE_PATH,"rb")
  content_file_input_dict = {"content_file":
              ("sample_assessment_submission_1.txt", content_file, "text/plain")}

  content_res = post_method(
            url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-submission/upload-sync/{context.learner_id}/{context.assessment_id}",
            files=content_file_input_dict,
            )
  print(content_res.json())
  assert content_res.status_code == 200
  res_json_1 = content_res.json()

  content_file_input_dict = {"content_file":
              ("sample_assessment_submission_2.txt", content_file, "text/plain")}

  content_res = post_method(
            url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-submission/upload-sync/{context.learner_id}/{context.assessment_id}",
            files=content_file_input_dict,
            )
  assert content_res.status_code == 200
  res_json_2 = content_res.json()

  context.valid_resource_path_1 = res_json_1["data"]["resource_path"]
  context.valid_resource_path_2 = res_json_2["data"]["resource_path"]

  submitted_assessment = SubmittedAssessment.find_by_uuid(submitted_assessment.uuid)
  submitted_assessment.submission_gcs_paths = [
    context.valid_resource_path_1,
    context.valid_resource_path_2,
  ]
  submitted_assessment.update()

  set_cache("submitted_assessment", submitted_assessment.uuid)
  set_cache("assessment_learner", learner.uuid)

@behave.when(
    "API request is sent to generate signed urls for submitted assessment contents"
)
def step_impl_2(context):
  res = get_method(
    url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-content/{context.submitted_assessment_id}/signed-url",
    query_params={
      "is_submitted_assessment": True
    }
  )
  print(res.status_code)
  print(res.json())
  context.status_code = res.status_code
  context.res_json = res.json()

@behave.then(
  "the API will return list of signed urls for submitted assessment contents"
)
def step_impl_3(context):
  assert context.status_code == 200
  assert context.res_json["success"] == True
  assert context.res_json["message"] == "Successfully generated signed urls for all files"

  files_to_delete = []
  for record in context.res_json["data"]:
    assert record["signed_url"] is not None
    assert record["status"] == "Signed url generated successfully"
    files_to_delete.append(record["file_path"])
  
  set_cache("files_to_delete", json.dumps(files_to_delete))

#------------------------------------------------------------------------------
# Scenario 3: LXE wants to generate signed URL for assessment contents with invalid assessment_id
#------------------------------------------------------------------------------
@behave.given(
    "that valid assessment_id does not exists"
)
def step_impl_1(context):
  context.assessment_id = "random_assessment_id"
  context.user_id = get_cache("assessment_user")

@behave.when(
    "API request is sent to generate signed urls for assessment contents with invalid assessment_id"
)
def step_impl_2(context):
  res = get_method(
    url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-content/{context.assessment_id}/signed-url"
  )
  context.status_code = res.status_code
  context.res_json = res.json()

@behave.then(
  "the API will return resource not found error for invalid assessment_id"
)
def step_impl_3(context):
  assert context.status_code == 404
  assert context.res_json["success"] == False
  assert context.res_json["message"] == f"Assessment with uuid {context.assessment_id} not found"

#------------------------------------------------------------------------------
# Scenario 4: LXE wants to generate signed URL for submitted assessment contents with invalid submitted_assessment_id
#------------------------------------------------------------------------------
@behave.given(
    "that valid submitted_assessment_id does not exists"
)
def step_impl_1(context):
  context.submitted_assessment_id = "random_submitted_assessment_id"
  context.learner_id = get_cache("assessment_learner")

@behave.when(
    "API request is sent to generate signed urls for submitted assessment contents with invalid submitted_assessment_id"
)
def step_impl_2(context):
  res = get_method(
    url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-content/{context.submitted_assessment_id}/signed-url",
    query_params={
      "is_submitted_assessment": True
    }
  )
  context.status_code = res.status_code
  context.res_json = res.json()

@behave.then(
  "the API will return resource not found error for invalid submitted_assessment_id"
)
def step_impl_3(context):
  assert context.status_code == 404
  assert context.res_json["success"] == False
  assert context.res_json["message"] == f"Submitted Assessment with uuid {context.submitted_assessment_id} not found"

#------------------------------------------------------------------------------
# Scenario 5: LXE wants to generate signed URL for few missing assessment contents
#------------------------------------------------------------------------------
@behave.given(
    "that valid assessment_id exists but some resource paths does not exist"
)
def step_impl_1(context):
  context.assessment_id = get_cache("assessment")

  # Add erronous data
  assessment = Assessment.find_by_uuid(context.assessment_id)
  file_list = assessment.resource_paths
  file_list.append("some random path")
  assessment.resource_paths = file_list
  assessment.update()

@behave.when(
    "API request is sent to generate signed urls for few missing assessment contents"
)
def step_impl_2(context):
  res = get_method(
    url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-content/{context.assessment_id}/signed-url"
  )
  context.status_code = res.status_code
  context.res_json = res.json()

@behave.then(
  "the API will return success response with list of signed urls with resource_not_found error message for few missing contents"
)
def step_impl_3(context):
  assert context.status_code == 200
  assert context.res_json["success"] == True
  assert context.res_json["message"] == "Could not generate urls for some files"

  assert context.res_json["data"][0]["signed_url"] is not None
  assert context.res_json["data"][0]["status"] == "Signed url generated successfully"

  assert context.res_json["data"][1]["signed_url"] is not None
  assert context.res_json["data"][1]["status"] == "Signed url generated successfully"

  assert context.res_json["data"][2]["signed_url"] is None
  assert context.res_json["data"][2]["status"] == "File Not Found"

  # Delete Uploaded File
  files_to_delete = json.loads(get_cache("files_to_delete"))
  files_to_delete.append(context.res_json["data"][0]["file_path"])
  files_to_delete.append(context.res_json["data"][1]["file_path"])
  delete_test_files_from_gcs(files_to_delete)

#------------------------------------------------------------------------------
# Scenario 6: LXE wants to generate signed URL for invalid assessment contents
#------------------------------------------------------------------------------
@behave.given(
    "that valid assessment_id exists but resource paths does not exist"
)
def step_impl_1(context):
  context.assessment_id = get_cache("assessment")

  # Add erronous data
  assessment = Assessment.find_by_uuid(context.assessment_id)
  file_list = ["some random path"]
  assessment.resource_paths = file_list
  assessment.update()

@behave.when(
    "API request is sent to generate signed urls for invalid assessment contents"
)
def step_impl_2(context):
  res = get_method(
    url=f"{API_URL_ASSESSMENT_SERVICE}/assessment-content/{context.assessment_id}/signed-url"
  )
  context.status_code = res.status_code
  context.res_json = res.json()

@behave.then(
  "the API will return failure response with list of signed urls with resource_not_found error message for all contents"
)
def step_impl_3(context):
  assert context.status_code == 500
  assert context.res_json["success"] == False
  assert context.res_json["message"] == "Some error occurred while generating signed urls"

  for record in context.res_json["data"]:
    assert record["signed_url"] is None
    assert record["status"] == "File Not Found"
