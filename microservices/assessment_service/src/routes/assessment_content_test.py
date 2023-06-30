"""
  Unit tests for Assessment Content endpoints
"""
# pylint: disable = line-too-long,redefined-outer-name,unspecified-encoding
# pylint: disable = unused-import,unused-argument,consider-using-with
import os
import json
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest import mock
with mock.patch(
    "google.cloud.logging.Client", side_effect=mock.MagicMock()) as mok:
  from routes.assessment_content import router
  from routes.assessment import router as assessmentrouter
from testing.test_config import (API_URL, TESTING_FOLDER_PATH)
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers
from common.models import Assessment, SubmittedAssessment, Learner, LearnerProfile
from schemas.schema_examples import (SUBMITTED_ASSESSMENT_EXAMPLE,
                                      BASIC_ASSESSMENT_EXAMPLE,
                                      BASIC_LEARNER_EXAMPLE,
                                      BASIC_LEARNER_PROFILE_EXAMPLE)
from config import (ASSESSMENT_SUBMISSION_BASE_PATH,
                    ASSESSMENT_AUTHORING_BASE_PATH)

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/assessment-service/api/v1")
app.include_router(assessmentrouter,prefix="/assessment-service/api/v1")

assessment_api_url = f"{API_URL}/assessment"

client_with_emulator = TestClient(app)

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


class MockedDataModel():
  """
    Mock class for Assessment and Learner DataModel
  """

  def __init__(self):
    pass

  def find_by_uuid(self,uuid):
    return {uuid}

class MockedBlob():
  def __init__(self):
    self.size = 0

class GcsCrudService:
  """
    Mock class for GCSCrudService
  """

  def __init__(self, bucket_name):
    self.bucket_name = bucket_name
    self.size = 0

  def generate_url(self, prefix, expiration):
    self.prefix = prefix
    return "signed_url_dummy"

  def get_files_from_folder(self, prefix):
    return ["abc.txt","def.txt"]


def create_single_submitted_assessment(assign_assessor=True):
  """Function to create a submitted assessment"""
  # create a submitted assessment
  with open(
      "./testing/submitted_assessment.json", encoding="UTF-8") as json_file:
    sa_fields = json.load(json_file)[0]
  sa_fields["assessment_id"] = SUBMITTED_ASSESSMENT_EXAMPLE["assessment_id"]
  if assign_assessor:
    sa_fields["assessor_id"] = "user_id"
  sa_fields["status"] = "evaluation_pending"
  sa_fields["result"] = None
  submitted_assessment = SubmittedAssessment()
  submitted_assessment = submitted_assessment.from_dict(sa_fields)
  submitted_assessment.uuid = "sa_id"
  submitted_assessment.save()
  return submitted_assessment

def create_single_assessment():
  assessment_dict = {**BASIC_ASSESSMENT_EXAMPLE}
  assessment_dict["name"] = "Questionnaire"
  assessment = Assessment.from_dict(assessment_dict)
  assessment.uuid = ""
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()
  return assessment

# ---------------------------------------------------------
# Assessment Response File Upload API
# ---------------------------------------------------------
def test_upload_assessment_response_positive(clean_firestore, mocker):
  """
    Positive Scenario
  """
  mocker.patch("routes.assessment_content.is_valid_path", return_value=False)
  mocker.patch("routes.assessment_content.upload_file_to_bucket")

  input_assessment = BASIC_ASSESSMENT_EXAMPLE
  url_assessment = assessment_api_url
  post_resp = client_with_emulator.post(url_assessment, json=input_assessment)
  assessment_resp_json = post_resp.json()
  assert assessment_resp_json.get("success") is True, "Success not true"

  #creating learner model
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner_dict["email_address"] = "jon_doe_tglp@gmail.com"
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()
  learner_id = learner.id

  learner_profile_dict = {**BASIC_LEARNER_PROFILE_EXAMPLE}
  learner_profile_dict["learner_id"] = learner_id
  learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  learner_profile.uuid = ""
  learner_profile.save()
  learner_profile.uuid = learner_profile.id
  learner_profile.progress = {
    "assessments":{assessment_resp_json["data"]["uuid"]:{"name":"content_upload","num_attempts":1}}}
  learner_profile.update()
  learner_profile_dict["uuid"] = learner_profile.id
  learner_profile_dict["is_archived"] = False

  assessment_id = assessment_resp_json["data"]["uuid"]

  api_url = f"{API_URL}/assessment-submission/upload-sync/{learner_id}/{assessment_id}"

  file_path = f"{TESTING_FOLDER_PATH}/sample_file_upload.txt"

  upload_file = open(file_path)
  resp = client_with_emulator.post(
      api_url,
      files={
          "content_file": ("sample_file_upload.txt", upload_file, "text/plain")
      })
  resp_json = resp.json()
  assert resp.status_code == 200
  assert resp_json["success"] is True
  assert resp_json["message"] == "Successfully uploaded file"

  expected_file_path = f"{ASSESSMENT_SUBMISSION_BASE_PATH}/{learner_id}/{assessment_id}"
  expected_file_path += "/temp/sample_file_upload.txt"

  assert resp_json["data"]["resource_path"] == expected_file_path


def test_upload_assessment_response_negative_1(clean_firestore, mocker):
  """
    Negative Scenario
    -------------------------------------------------------
    Validation Error should occur when file with same name
    already exists for the same assessment id
  """
  mocker.patch("routes.assessment_content.is_valid_path", return_value=True)
  mocker.patch("routes.assessment_content.upload_file_to_bucket")

  input_assessment = BASIC_ASSESSMENT_EXAMPLE
  url_assessment = assessment_api_url
  post_resp = client_with_emulator.post(url_assessment, json=input_assessment)
  assessment_resp_json = post_resp.json()
  assert assessment_resp_json.get("success") is True, "Success not true"

  #creating learner model
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner_dict["email_address"] = "jon_doe_tglp@gmail.com"
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()
  learner_id = learner.id

  learner_profile_dict = {**BASIC_LEARNER_PROFILE_EXAMPLE}
  learner_profile_dict["learner_id"] = learner_id
  learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  learner_profile.uuid = ""
  learner_profile.save()
  learner_profile.uuid = learner_profile.id
  learner_profile.progress = {"assessments":{assessment_resp_json["data"]["uuid"]:{"name":"content_upload","num_attempts":1}}}
  learner_profile.update()
  learner_profile_dict["uuid"] = learner_profile.id
  learner_profile_dict["is_archived"] = False

  assessment_id = assessment_resp_json["data"]["uuid"]

  api_url = f"{API_URL}/assessment-submission/upload-sync/{learner_id}/{assessment_id}"

  file_path = f"{TESTING_FOLDER_PATH}/sample_file_upload.txt"

  upload_file = open(file_path)
  resp = client_with_emulator.post(
      api_url,
      files={
          "content_file": ("sample_file_upload.txt", upload_file, "text/plain")
      })
  resp_json = resp.json()
  assert resp.status_code == 422
  assert resp_json["success"] is False
  assert resp_json[
      "message"] == "File with same name already exists"


def test_upload_assessment_response_negative_2(clean_firestore, mocker):
  """
    Negative Scenario
    -------------------------------------------------------
    Validation Error should occur when assessment id is invalid
  """
  mocker.patch("routes.assessment_content.is_valid_path", return_value=False)
  mocker.patch("routes.assessment_content.upload_file_to_bucket")

  input_assessment = BASIC_ASSESSMENT_EXAMPLE
  url_assessment = assessment_api_url
  post_resp = client_with_emulator.post(url_assessment, json=input_assessment)
  assessment_resp_json = post_resp.json()
  assert assessment_resp_json.get("success") is True, "Success not true"

  #creating learner model
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner_dict["email_address"] = "jon_doe_tglp@gmail.com"
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()
  learner_id = learner.id

  learner_profile_dict = {**BASIC_LEARNER_PROFILE_EXAMPLE}
  learner_profile_dict["learner_id"] = learner_id
  learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  learner_profile.uuid = ""
  learner_profile.save()
  learner_profile.uuid = learner_profile.id
  learner_profile.progress = {"assessments":{assessment_resp_json["data"]["uuid"]:{"name":"content_upload","num_attempts":1}}}
  learner_profile.update()
  learner_profile_dict["uuid"] = learner_profile.id
  learner_profile_dict["is_archived"] = False

  assessment_id = "incorrect_assessment_id"

  api_url = f"{API_URL}/assessment-submission/upload-sync/{learner_id}/{assessment_id}"

  file_path = f"{TESTING_FOLDER_PATH}/sample_file_upload.txt"

  upload_file = open(file_path)
  resp = client_with_emulator.post(
      api_url,
      files={
          "content_file": ("sample_file_upload.txt", upload_file, "text/plain")
      })
  resp_json = resp.json()
  assert resp.status_code == 404
  assert resp_json["success"] is False
  assert resp_json[
      "message"] == f"Assessment with uuid {assessment_id} not found"


def test_upload_assessment_response_negative_3(clean_firestore, mocker):
  """
    Negative Scenario
    -------------------------------------------------------
    Validation Error should occur when learner id is invalid
  """
  mocker.patch("routes.assessment_content.is_valid_path", return_value=False)
  mocker.patch("routes.assessment_content.upload_file_to_bucket")

  input_assessment = BASIC_ASSESSMENT_EXAMPLE
  url_assessment = assessment_api_url
  post_resp = client_with_emulator.post(url_assessment, json=input_assessment)
  assessment_resp_json = post_resp.json()
  assert assessment_resp_json.get("success") is True, "Success not true"

  #creating learner model
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner_dict["email_address"] = "jon_doe_tglp@gmail.com"
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()
  learner_id = learner.id

  learner_profile_dict = {**BASIC_LEARNER_PROFILE_EXAMPLE}
  learner_profile_dict["learner_id"] = learner_id
  learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  learner_profile.uuid = ""
  learner_profile.save()
  learner_profile.uuid = learner_profile.id
  learner_profile.progress = {"assessments":{assessment_resp_json["data"]["uuid"]:{"name":"content_upload","num_attempts":1}}}
  learner_profile.update()
  learner_profile_dict["uuid"] = learner_profile.id
  learner_profile_dict["is_archived"] = False

  learner_id = "incorrect_learner_id"
  assessment_id = assessment_resp_json["data"]["uuid"]

  api_url = f"{API_URL}/assessment-submission/upload-sync/{learner_id}/{assessment_id}"

  file_path = f"{TESTING_FOLDER_PATH}/sample_file_upload.txt"

  upload_file = open(file_path)
  resp = client_with_emulator.post(
      api_url,
      files={
          "content_file": ("sample_file_upload.txt", upload_file, "text/plain")
      })
  resp_json = resp.json()
  assert resp.status_code == 422
  assert resp_json["success"] is False
  assert resp_json["message"] == f"No learner profile with learner id {learner_id} found"

def test_upload_assessment_response_negative_4(clean_firestore, mocker):
  """
    Negative Scenario
    -------------------------------------------------------
    Validation Error should occur when current attempt is greater than max attempt
  """
  mocker.patch("routes.assessment_content.is_valid_path", return_value=False)
  mocker.patch("routes.assessment_content.upload_file_to_bucket")

  input_assessment = BASIC_ASSESSMENT_EXAMPLE
  url_assessment = assessment_api_url
  post_resp = client_with_emulator.post(url_assessment, json=input_assessment)
  assessment_resp_json = post_resp.json()
  assert assessment_resp_json.get("success") is True, "Success not true"

  #creating learner model
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner_dict["email_address"] = "jon_doe_tglp@gmail.com"
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()
  learner_id = learner.id

  learner_profile_dict = {**BASIC_LEARNER_PROFILE_EXAMPLE}
  learner_profile_dict["learner_id"] = learner_id
  learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  learner_profile.uuid = ""
  learner_profile.save()
  learner_profile.uuid = learner_profile.id
  learner_profile.progress = {"assessments":{assessment_resp_json["data"]["uuid"]:{"name":"content_upload","num_attempts":7}}}
  learner_profile.update()

  assessment_id = assessment_resp_json["data"]["uuid"]

  api_url = f"{API_URL}/assessment-submission/upload-sync/{learner_id}/{assessment_id}"

  file_path = f"{TESTING_FOLDER_PATH}/sample_file_upload.txt"

  upload_file = open(file_path)
  resp = client_with_emulator.post(
      api_url,
      files={
          "content_file": ("sample_file_upload.txt", upload_file, "text/plain")
      })
  resp_json = resp.json()
  assert resp.status_code == 422
  assert resp_json["success"] is False
  cur_attempts = learner_profile.progress["assessments"][assessment_id]["num_attempts"]
  max_attempts = assessment_resp_json["data"]["max_attempts"]
  assert resp_json["message"] == f"current attempt {cur_attempts} cannot be greater than max attempts {max_attempts}"

# ---------------------------------------------------------
# Assessment Authoring File Upload API
# ---------------------------------------------------------
def test_upload_assessment_authoring_positive(clean_firestore, mocker):
  """
    Positive Scenario
  """
  mocker.patch("routes.assessment_content.is_valid_path", return_value=False)
  mocker.patch("routes.assessment_content.upload_file_to_bucket")
  mocker.patch(
      "routes.assessment_content.User", return_value=MockedDataModel())

  user_id = "random_user_id"

  api_url = f"{API_URL}/assessment-authoring/upload-sync/{user_id}"

  file_path = f"{TESTING_FOLDER_PATH}/sample_file_upload.txt"

  upload_file = open(file_path)
  resp = client_with_emulator.post(
      api_url,
      files={
          "content_file": ("sample_file_upload.txt", upload_file, "text/plain")
      })
  resp_json = resp.json()
  assert resp.status_code == 200
  assert resp_json["success"] is True
  assert resp_json["message"] == "Successfully uploaded file"

  expected_file_path = f"{ASSESSMENT_AUTHORING_BASE_PATH}/{user_id}"
  expected_file_path += "/temp/sample_file_upload.txt"

  assert resp_json["data"]["resource_path"] == expected_file_path


def test_upload_assessment_authoring_negative_1(clean_firestore, mocker):
  """
    Negative Scenario
    -------------------------------------------------------
    Validation Error should occur when file with same name
    already exists for the same assessment id
  """
  mocker.patch("routes.assessment_content.is_valid_path", return_value=True)
  mocker.patch("routes.assessment_content.upload_file_to_bucket")
  mocker.patch(
      "routes.assessment_content.User", return_value=MockedDataModel())

  user_id = "random_user_id"

  api_url = f"{API_URL}/assessment-authoring/upload-sync/{user_id}"

  file_path = f"{TESTING_FOLDER_PATH}/sample_file_upload.txt"

  upload_file = open(file_path)
  resp = client_with_emulator.post(
      api_url,
      files={
          "content_file": ("sample_file_upload.txt", upload_file, "text/plain")
      })
  resp_json = resp.json()
  assert resp.status_code == 422
  assert resp_json["success"] is False
  assert resp_json[
      "message"] == "File with same name already exists"

def test_upload_assessment_authoring_negative_2(clean_firestore, mocker):
  """
    Negative Scenario
    -------------------------------------------------------
    Validation Error should occur when assessment id is invalid
  """
  mocker.patch("routes.assessment_content.is_valid_path", return_value=False)
  mocker.patch("routes.assessment_content.upload_file_to_bucket")

  user_id = "random_user_id"

  api_url = f"{API_URL}/assessment-authoring/upload-sync/{user_id}"

  file_path = f"{TESTING_FOLDER_PATH}/sample_file_upload.txt"

  upload_file = open(file_path)
  resp = client_with_emulator.post(
      api_url,
      files={
          "content_file": ("sample_file_upload.txt", upload_file, "text/plain")
      })
  resp_json = resp.json()
  assert resp.status_code == 404
  assert resp_json["success"] is False
  assert resp_json[
      "message"] == f"User with user_id {user_id} not found"

# ---------------------------------------------------------
# Get Signed URLs for Assessment/Submitted assessment
# ---------------------------------------------------------

def test_get_url_for_assessment_content_positive(clean_firestore, mocker):
  """
    Scenario 1:
      1. Signed URL for Assessment

    Scenario 2:
      1. Signed URL for Submitted Assessment
  """
  mocker.patch("routes.assessment_content.is_valid_path", return_value=True)
  mocker.patch(
      "routes.assessment_content.GcsCrudService",
      return_value=GcsCrudService("GCP_LEARNING_RESOURCE_BUCKET"))
  mocker.patch("routes.assessment_content.isinstance", return_value=True)
  mocker.patch("routes.assessment_content.get_blob_from_gcs_path",\
               return_value=MockedBlob())

  file_paths = [
    "abc.txt",
    "def.txt",
    "ghi.txt"
  ]

  # -------------------------------------------------
  # Scenario 1: Signed URL for Assessment
  # -------------------------------------------------
  assessment = create_single_assessment()

  assessment_uuid = assessment.uuid
  assessment.resource_paths = file_paths
  assessment.update()

  api_url = f"{API_URL}/assessment-content/{assessment_uuid}/signed-url"

  resp = client_with_emulator.get(api_url)
  resp_json = resp.json()

  assert resp.status_code == 200
  assert resp_json["success"] is True
  assert resp_json["message"] == "Successfully generated signed urls for all files"

  for i in range(len(resp_json["data"])):
    assert resp_json["data"][i]["file_path"] == file_paths[i]
    assert resp_json["data"][i]["signed_url"] is not None
    assert resp_json["data"][i]["status"] == "Signed url generated successfully"

  # -------------------------------------------------
  # Scenario 2: Signed URL for Submitted Assessment
  # -------------------------------------------------
  submitted_assessment = create_single_submitted_assessment(assign_assessor=False)

  submitted_assessment_uuid = submitted_assessment.uuid
  submitted_assessment.submission_gcs_paths = file_paths
  submitted_assessment.update()

  api_url = f"{API_URL}/assessment-content/{submitted_assessment_uuid}/signed-url"

  resp = client_with_emulator.get(
                                  api_url,
                                  params={
                                    "is_submitted_assessment": True
                                  })
  resp_json = resp.json()

  assert resp.status_code == 200
  assert resp_json["success"] is True
  assert resp_json["message"] == "Successfully generated signed urls for all files"

  for i in range(len(resp_json["data"])):
    assert resp_json["data"][i]["file_path"] == file_paths[i]
    assert resp_json["data"][i]["signed_url"] is not None
    assert resp_json["data"][i]["status"] == "Signed url generated successfully"

def test_get_url_for_assessment_content_negative_1(clean_firestore, mocker):
  """
    Scenario 1:
      1. Files are not found
      2. All failed

    Scenario 2:
      1. Files are not found
      2. Partial Success
  """
  mocker.patch("routes.assessment_content.is_valid_path", return_value=False)
  mocker.patch(
      "routes.assessment_content.GcsCrudService",
      return_value=GcsCrudService("GCP_LEARNING_RESOURCE_BUCKET"))
  mocker.patch("routes.assessment_content.isinstance", return_value=True)

  assessment = create_single_assessment()

  file_paths = [
    "abc.txt",
    "def.txt",
    "ghi.txt"
  ]

  assessment_uuid = assessment.uuid
  assessment.resource_paths = file_paths
  assessment.update()

  api_url = f"{API_URL}/assessment-content/{assessment_uuid}/signed-url"

  # -------------------------------------------------
  # Scenario 1: Files are not found and all failed
  # -------------------------------------------------
  resp = client_with_emulator.get(api_url)
  resp_json = resp.json()

  assert resp.status_code == 500
  assert resp_json["success"] is False
  assert resp_json["message"] == "Some error occurred while generating signed urls"

  for i in range(len(resp_json["data"])):
    assert resp_json["data"][i]["file_path"] == file_paths[i]
    assert resp_json["data"][i]["signed_url"] is None
    assert resp_json["data"][i]["status"] == "File Not Found"

  # -------------------------------------------------
  # Scenario 2: Files are not found and some failed
  # -------------------------------------------------
  mocker.patch("routes.assessment_content.len", return_value=4)

  resp = client_with_emulator.get(api_url)
  resp_json = resp.json()

  assert resp.status_code == 200
  assert resp_json["success"] is True
  assert resp_json["message"] == "Could not generate urls for some files"

  for i in range(len(resp_json["data"])):
    assert resp_json["data"][i]["file_path"] == file_paths[i]
    assert resp_json["data"][i]["signed_url"] is None
    assert resp_json["data"][i]["status"] == "File Not Found"

def test_get_url_for_assessment_content_negative_2(clean_firestore, mocker):
  """
    Scenario 1:
      1. Some error occurred
      2. All failed

    Scenario 2:
      1. Some error occurred
      2. Partial Success
  """
  mocker.patch("routes.assessment_content.is_valid_path", return_value=True)
  mocker.patch(
      "routes.assessment_content.GcsCrudService",
      return_value=GcsCrudService("GCP_LEARNING_RESOURCE_BUCKET"))
  mocker.patch("routes.assessment_content.isinstance", return_value=False)
  mocker.patch("routes.assessment_content.get_blob_from_gcs_path",\
               return_value=MockedBlob())

  assessment = create_single_assessment()

  file_paths = [
    "abc.txt",
    "def.txt",
    "ghi.txt"
  ]

  assessment_uuid = assessment.uuid
  assessment.resource_paths = file_paths
  assessment.update()

  api_url = f"{API_URL}/assessment-content/{assessment_uuid}/signed-url"

  # -------------------------------------------------
  # Scenario 1: Some error occurred and all failed
  # -------------------------------------------------
  resp = client_with_emulator.get(api_url)
  resp_json = resp.json()

  assert resp.status_code == 500
  assert resp_json["success"] is False
  assert resp_json["message"] == "Some error occurred while generating signed urls"

  for i in range(len(resp_json["data"])):
    assert resp_json["data"][i]["file_path"] == file_paths[i]
    assert resp_json["data"][i]["signed_url"] is None
    assert resp_json["data"][i]["status"] == "Some error occurred while generating singed url"

  # -------------------------------------------------
  # Scenario 1: Some error occurred and some failed
  # -------------------------------------------------
  mocker.patch("routes.assessment_content.len", return_value=4)

  resp = client_with_emulator.get(api_url)
  resp_json = resp.json()

  assert resp.status_code == 200
  assert resp_json["success"] is True
  assert resp_json["message"] == "Could not generate urls for some files"

  for i in range(len(resp_json["data"])):
    assert resp_json["data"][i]["file_path"] == file_paths[i]
    assert resp_json["data"][i]["signed_url"] is None
    assert resp_json["data"][i]["status"] == "Some error occurred while generating singed url"

# ---------------------------------------------------------
# Download all contents linked to Assessment
# ---------------------------------------------------------
def test_download_all_content_for_assessment_positive(clean_firestore, mocker):
  """
    Positive Scenario
  """
  user_id = "random_user_id"

  file_paths = [
    "abc.txt",
    "def.txt",
    "ghi.txt"
  ]

  zip_file_location = f"{TESTING_FOLDER_PATH}/sample_zip_download.zip"

  mocker.patch("services.assessment_content_helper.download_files_for_assessment",
      return_value=[])
  mocker.patch("services.zip_file_processor.create_zip_file",
      return_value=zip_file_location)

  assessment = create_single_assessment()

  assessment_uuid = assessment.uuid
  assessment.author_id = user_id
  assessment.resource_paths = file_paths
  assessment.update()

  api_url = f"{API_URL}/assessment-content/{assessment_uuid}/download-all"

  res = client_with_emulator.get(url= api_url)

  print(res.status_code)
  print(res.headers)
  print(res.content)

  assert res.status_code == 200
  assert res.headers["content-type"] == "application/zip"
  assert res.content is not None

def test_download_all_content_for_assessment_negative(clean_firestore, mocker):
  """
    Scenario:
      1. Some files are missing
      2. No files are linked
  """
  mocker.patch("services.assessment_content_helper.is_valid_path", return_value=False)

  user_id = "random_user_id"

  file_paths = [
    "abc.txt",
    "def.txt",
    "ghi.txt"
  ]

  assessment = create_single_assessment()
  assessment_uuid = assessment.uuid
  assessment.author_id = user_id
  assessment.resource_paths = file_paths
  assessment.update()

  api_url = f"{API_URL}/assessment-content/{assessment_uuid}/download-all"

  # -------------------------------------------------------
  # Scenario 1: Some files are missing
  # -------------------------------------------------------

  res = client_with_emulator.get(url=api_url)

  print(res.status_code)
  print(res.json())

  assert res.status_code == 404
  res_json = res.json()
  assert "Total missing files: 3" in res_json["message"]

  # -------------------------------------------------------
  # Scenario 2: No files are linked
  # -------------------------------------------------------

  assessment.resource_paths = []
  assessment.update()

  res = client_with_emulator.get(url=api_url)

  print(res.status_code)
  print(res.json())

  assert res.status_code == 422
  res_json = res.json()
  assert "Cannot generate zip" in res_json["message"]

# ---------------------------------------------------------
# Delete files uploaded for Assessment by Author
# ---------------------------------------------------------

def test_delete_file_uploaded_for_assessment_positive(clean_firestore, mocker):
  """
    Positive Scenario
  """
  mocker.patch("services.assessment_content_helper.is_valid_path", return_value=True)
  mocker.patch(
      "routes.assessment_content.User", return_value=MockedDataModel())
  mocker.patch("services.assessment_content_helper.delete_file_from_gcs")

  file_paths = [
    "folder/abc.txt",
    "folder/def.txt",
    "folder/ghi.txt"
  ]

  user_id = "random_user_id"

  api_url = f"{API_URL}/assessment-authoring/delete-file/{user_id}"

  res = client_with_emulator.put(
                                url=api_url,
                                json={
                                  "file_list": file_paths
                                }
                              )
  print(res.status_code)
  print(res.json())
  assert res.status_code == 200
  res_json = res.json()
  assert res_json["success"] is True
  assert res_json["message"] == f"Successfully deleted files for user with uuid {user_id}"

def test_delete_file_uploaded_for_assessment_negative(clean_firestore, mocker):
  """
    Scenario: Requested file does not exists on GCS
  """
  mocker.patch("services.assessment_content_helper.is_valid_path", return_value=False)
  mocker.patch(
      "routes.assessment_content.User", return_value=MockedDataModel())

  file_paths = [
    "folder/abc.txt",
    "folder/def.txt",
    "folder/ghi.txt"
  ]

  user_id = "random_user_id"

  api_url = f"{API_URL}/assessment-authoring/delete-file/{user_id}"

  res = client_with_emulator.put(
                                url=api_url,
                                json={
                                  "file_list": file_paths
                                }
                              )
  print(res.status_code)
  print(res.json())
  assert res.status_code == 404
  res_json = res.json()
  assert res_json["success"] is False
  assert "Total missing files:" in res_json["message"]

# ---------------------------------------------------------
# Get uploaded content from `temp` folder
# ---------------------------------------------------------

def test_get_files_from_temp_folder_positive(clean_firestore, mocker):
  """
    Scenario 1: List files from Assessment author's temp
    Scenario 2: List files from Learner's temp
  """
  mocker.patch("services.assessment_content_helper.GcsCrudService",
                return_value=GcsCrudService(""))
  mocker.patch("routes.assessment_content.get_blob_from_gcs_path",
               return_value=MockedBlob())
  mocker.patch("routes.assessment_content.User",
                return_value=MockedDataModel())
  mocker.patch("routes.assessment_content.Assessment",
                return_value=MockedDataModel())
  mocker.patch("routes.assessment_content.Learner",
                return_value=MockedDataModel())

  user_id = "random_user_id"
  api_url = f"{API_URL}/assessment-content/uploaded-files/{user_id}"

  # Scenario 1: Fetch files from Assessment author's temp folder
  res = client_with_emulator.get(url=api_url)
  assert res.status_code == 200
  res_json = res.json()
  print(res_json)
  assert res_json["success"] is True
  assert res_json["message"] == "Successfully fetched files list"
  assert len(res_json["data"]) == 2

  # Scenario 2: Fetch files from Learner's temp folder
  assessment_id = "random_assessment_id"
  res = client_with_emulator.get(url=api_url,
                                  params={
                                    "assessment_id": assessment_id
                                  })
  assert res.status_code == 200
  res_json = res.json()
  print(res_json)
  assert res_json["success"] is True
  assert res_json["message"] == "Successfully fetched files list"
  assert len(res_json["data"]) == 2


# ---------------------------------------------------------
# Delete files uploaded for Assessment by Learner
# ---------------------------------------------------------

def test_delete_file_uploaded_for_assessment_submission_positive(clean_firestore, mocker):
  """
    Positive Scenario
  """
  mocker.patch("services.assessment_content_helper.is_valid_path", return_value=True)
  mocker.patch(
      "routes.assessment_content.Learner", return_value=MockedDataModel())
  mocker.patch(
      "routes.assessment_content.Assessment", return_value=MockedDataModel())
  mocker.patch("services.assessment_content_helper.delete_file_from_gcs")

  file_paths = [
    "folder/abc.txt",
    "folder/def.txt",
    "folder/ghi.txt"
  ]

  learner_id = "random_learner_id"
  assessment_id = "random_assessment_id"

  api_url = f"{API_URL}/assessment-submission/delete-file/{learner_id}/{assessment_id}"

  res = client_with_emulator.put(
                                url=api_url,
                                json={
                                  "file_list": file_paths
                                }
                              )
  print(res.status_code)
  print(res.json())
  assert res.status_code == 200
  res_json = res.json()
  assert res_json["success"] is True

  msg = f"Successfully deleted files for Learner with uuid {learner_id}"
  msg += f" against Assessment with uuid {assessment_id}"
  assert res_json["message"] == msg

def test_delete_file_uploaded_for_assessment_submission_negative(clean_firestore, mocker):
  """
    Scenario: Requested file does not exists on GCS
  """
  mocker.patch("services.assessment_content_helper.is_valid_path", return_value=False)
  mocker.patch(
      "routes.assessment_content.Learner", return_value=MockedDataModel())
  mocker.patch(
      "routes.assessment_content.Assessment", return_value=MockedDataModel())

  file_paths = [
    "folder/abc.txt",
    "folder/def.txt",
    "folder/ghi.txt"
  ]

  learner_id = "random_learner_id"
  assessment_id = "random_assessment_id"

  api_url = f"{API_URL}/assessment-submission/delete-file/{learner_id}/{assessment_id}"

  res = client_with_emulator.put(
                                url=api_url,
                                json={
                                  "file_list": file_paths
                                }
                              )
  print(res.status_code)
  print(res.json())
  assert res.status_code == 404
  res_json = res.json()
  assert res_json["success"] is False
  assert "Total missing files:" in res_json["message"]
