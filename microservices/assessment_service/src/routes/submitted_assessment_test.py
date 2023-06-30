"""
  Unit tests for Assessment, Submitted Assessment & Rubric endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
import os
import json
import copy
import pytest
from fastapi import FastAPI
from unittest import mock
from fastapi.testclient import TestClient
from testing.test_config import API_URL, TESTING_FOLDER_PATH
from schemas.schema_examples import (SUBMITTED_ASSESSMENT_EXAMPLE,
                                     FULL_SUBMITTED_ASSESSMENT_EXAMPLE,
                                     UPDATE_SUBMITTED_ASSESSMENT_EXAMPLE)
with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  from routes.submitted_assessment import router
from services.submitted_assessment_test import (create_single_assessment,
                                                create_single_learner,
                                                create_single_user)
from common.models import (Learner, SubmittedAssessment,
                           LearningExperience, User, LearningObject)
from common.utils.http_exceptions import add_exception_handlers
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/assessment-service/api/v1")

client_with_emulator = TestClient(app)
ASSESSMENT_TESTDATA_FILENAME = os.path.join(TESTING_FOLDER_PATH +
                                            "/assessment.json")
# assigning url
api_url = f"{API_URL}"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"
RELATIVE_PATH = "../../../e2e/testing_objects/"


@pytest.fixture(name="create_assessment")
def fixture_create_assessment():
  create_single_assessment()


def create_single_learning_experience():
  """Function to create a learnin experience"""
  # create a learning experience
  with open(
      RELATIVE_PATH + "learning_experiences.json",
      encoding="UTF-8") as json_file:
    le_fields = json.load(json_file)[0]
  le_fields["child_nodes"]["assessments"] = [
      SUBMITTED_ASSESSMENT_EXAMPLE["assessment_id"]
  ]
  learning_experience = LearningExperience()
  learning_experience = learning_experience.from_dict(le_fields)
  learning_experience.uuid = "le_id"
  learning_experience.save()
  return learning_experience


def create_single_learning_object():
  with open(RELATIVE_PATH + "learning_objects.json",
  encoding="UTF-8") as json_file:
    lo_fields = json.load(json_file)[0]
  learning_object = LearningObject()
  learning_object = learning_object.from_dict(lo_fields)
  learning_object.uuid = "lo_id"
  learning_object.save()
  return learning_object


def create_single_submitted_assessment(assign_assessor=True):
  """Function to create submitted assessment"""
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


class LearnerTest():

  @classmethod
  def find_by_uuid(cls, uuid, is_deleted=False):
    learner = Learner()
    return learner


def create_user(user_id, user_type="assessor"):
  user = User()
  user.user_type = user_type
  user.user_id = user_id
  user.first_name = "Random"
  user.last_name = "User"
  user.email = "random.user@abc.com"
  user.status = "active"
  user.save()
  return user


@mock.patch("common.models.learner_profile.Learner",
            mock.MagicMock(side_effect=LearnerTest))
def test_post_submitted_assessment(mocker, clean_firestore, create_assessment):

  url = f"{api_url}/submitted-assessment"
  input_submitted_assessment = SUBMITTED_ASSESSMENT_EXAMPLE

  last_submitted_assessment = copy.deepcopy(FULL_SUBMITTED_ASSESSMENT_EXAMPLE)

  learner = create_single_learner()
  learner.uuid = input_submitted_assessment["learner_id"]
  learner.update()
  assessment = create_single_assessment()
  user = create_single_user()
  assessment.instructor_id = user.user_id
  assessment.update()
  input_submitted_assessment["assessment_id"] = assessment.uuid

  last_submitted_assessment[
      "attempt_no"] = last_submitted_assessment["attempt_no"] - 1

  mocker.patch("services.submitted_assessment.get_latest_submission",
               return_value=last_submitted_assessment)
  mocker.patch("services.submitted_assessment.traverse_up", return_value=None)
  mocker.patch("services.submitted_assessment.assessor_handler",
               return_value="assessor_id")
  mocker.patch("services.submitted_assessment.fetch_response",
               return_value=None)
  post_resp = client_with_emulator.post(url, json=input_submitted_assessment)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"

  assert post_resp.status_code == 200, "Status 200"

  # post_json_response = post_resp.json()
  del post_resp_json["data"]["created_time"]
  del post_resp_json["data"]["last_modified_time"]

  uuid = post_resp_json.get("data").get("uuid")
  # # now see if GET endpoint returns same data
  url = f"{api_url}/submitted-assessment/{uuid}"
  get_resp = client_with_emulator.get(url)
  get_resp_json = get_resp.json()
  del get_resp_json["data"]["created_time"]
  del get_resp_json["data"]["last_modified_time"]
  assert get_resp_json.get("data") == post_resp_json.get("data")


def test_get_all_submitted_assessment(mocker, clean_firestore):

  input_submitted_assessment = SUBMITTED_ASSESSMENT_EXAMPLE

  learner = create_single_learner()
  learner.uuid = input_submitted_assessment["learner_id"]
  learner.update()
  assessment = create_single_assessment()
  input_submitted_assessment["assessment_id"] = assessment.uuid
  user = create_single_user()

  post_url = f"{api_url}/submitted-assessment"

  mocker.patch("services.submitted_assessment.traverse_up", return_value=None)
  mocker.patch(
      "services.submitted_assessment.assessor_handler",
      return_value=user.user_id)
  mocker.patch(
      "services.submitted_assessment.instructor_handler",
      return_value=None)
  mocker.patch(
      "services.submitted_assessment.fetch_response", return_value=None)
  # create a submitted assessment using POST
  post_responses = []
  for _ in range(2):
    post_resp = client_with_emulator.post(
        post_url, json=input_submitted_assessment)
    post_resp_json = post_resp.json()
    assert post_resp_json.get("success") is True, "Success not true"
    assert post_resp.status_code == 200, "Status 200"
    post_resp_json["data"]["learner_name"] = \
        learner.first_name + " " + learner.last_name
    post_resp_json["data"]["unit_name"] = ""
    post_resp_json["data"]["discipline_name"] = ""
    post_resp_json["data"]["assigned_to"] = user.first_name + " " + \
      user.last_name
    post_resp_json["data"]["max_attempts"] = assessment.max_attempts
    post_resp_json["data"]["instructor_name"] = "Unassigned"
    post_resp_json["data"]["instructor_id"] = ""
    post_resp_json["data"]["assessment_name"] = None
    post_responses.append(post_resp_json.get("data"))

  submitted_assessment_uuid = post_responses[0]["uuid"]

  get_url = f"{api_url}/submitted-assessment/{submitted_assessment_uuid}/" +\
             "learner/all-submissions"

  # get the list of submitted assessments
  get_resp = client_with_emulator.get(get_url)
  get_resp_json = get_resp.json()
  assert get_resp_json.get("success") is True, "Success not true"
  assert get_resp.status_code == 200, "Status 200"
  # check if the created submission and the fetched submissions are same
  for resp in post_responses:
    resp["assessment_name"] = None
  assert get_resp_json.get("data")["records"] == list(reversed(post_responses))


def test_filtered_searched_submitted_assessments1(clean_firestore,
                                                 create_assessment):
  # Get submitted assessments assigned to an assessor

  learner_user = create_single_user()
  assessor_user = create_single_user()
  instructor_user = create_single_user()
  learner = create_single_learner()
  assessment = create_single_assessment()
  learning_experience = create_single_learning_experience()
  submitted_assessment = create_single_submitted_assessment()
  # Preparing data for UT

  learner_user.user_type_ref = learner.id
  learner_user.user_id = learner_user.id
  learner_user.update()

  assessor_user.user_type = "assessor"
  assessor_user.update()

  instructor_user.user_type = "instructor"
  instructor_user.update()

  submitted_assessment.assessor_id = assessor_user.id
  submitted_assessment.learner_id = learner.id
  submitted_assessment.assessment_id = assessment.id
  submitted_assessment.uuid = submitted_assessment.id
  submitted_assessment.update()

  learning_experience.child_nodes = {"assessments": [assessment.id]}
  learning_experience.uuid = learning_experience.id
  learning_experience.update()

  assessment.parent_nodes = {"learning_experiences": [learning_experience.id]}
  assessment.instructor_id = instructor_user.id
  assessment.learner_id = learner.id
  assessment.assessor_id = assessor_user.id
  assessment.uuid = assessment.id
  assessment.update()

  learner.uuid = learner.id
  learner.update()

  get_url = f"{api_url}/submitted-assessments"
  # get the list of submitted assessments by filter
  #  on unit assessor_id, name and type
  params = {
      "type": ["practice"],
      "unit_name": [learning_experience.name],
      "assessor_id": [assessor_user.id],
      "skip": 0,
      "limit": 2
  }
  get_resp = client_with_emulator.get(get_url, params=params)
  get_resp_json = get_resp.json()
  assert get_resp_json.get("success") is True, "Success not true"
  assert get_resp.status_code == 200, "Status 200"
  # check if the created submission and the fetched submissions are same
  assert get_resp_json.get("data")["records"][0][
    "unit_name"] == params["unit_name"][0]
  assert get_resp_json.get("data")["records"][0]["type"] == params["type"][0]

  # get list of submitted assessments by filter on wrong assessor_id
  params = {"assessor_id": ["assessor_id"], "skip": 0, "limit": 2}
  get_resp = client_with_emulator.get(get_url, params=params)
  get_resp_json = get_resp.json()
  assert get_resp.status_code == 404, "Status not 404"


def test_filtered_searched_submitted_assessments2(mocker,
                                                 clean_firestore,
                                                 create_assessment):
  # Get submitted assessments assigned to a coach/instructor

  learner_user = create_single_user()
  instructor_user = create_single_user()
  learner = create_single_learner()
  assessment = create_single_assessment()
  learning_experience = create_single_learning_experience()
  submitted_assessment = create_single_submitted_assessment(False)
  # Preparing data for UT

  learner_user.user_type_ref = learner.id
  learner_user.user_id = learner_user.id
  learner_user.update()

  mocker.patch("routes.submitted_assessment.staff_to_learner_handler",
                return_value=[learner_user.user_type_ref])

  instructor_user.user_type = "instructor"
  instructor_user.update()

  submitted_assessment.learner_id = learner.id
  submitted_assessment.assessment_id = assessment.id
  submitted_assessment.uuid = submitted_assessment.id
  submitted_assessment.update()

  learning_experience.child_nodes = {"assessments": [assessment.id]}
  learning_experience.uuid = learning_experience.id
  learning_experience.update()

  assessment.parent_nodes = {"learning_experiences": [learning_experience.id]}
  assessment.instructor_id = instructor_user.id
  assessment.learner_id = learner.id
  assessment.uuid = assessment.id
  assessment.update()

  learner.uuid = learner.id
  learner.update()

  get_url = f"{api_url}/submitted-assessments"
  # get the list of submitted assessments by filter
  # on instructor_id and type
  params = {
      "assessor_id": instructor_user.id,
      "skip": 0,
      "limit": 2
  }
  get_resp = client_with_emulator.get(get_url, params=params)
  get_resp_json = get_resp.json()
  assert get_resp_json.get("success") is True, "Success not true"
  assert get_resp.status_code == 200, "Status 200"
  # check if the created submission and the fetched submissions are same
  assert get_resp_json.get("data")["records"][0]["instructor_id"] == \
      params["assessor_id"]


def test_filtered_searched_submitted_assessments3(mocker,
                                                 clean_firestore,
                                                 create_assessment):
  # Get all flagged submitted assessments assigned to an instructor

  learner_user = create_single_user()
  instructor_user = create_single_user()
  learner = create_single_learner()
  assessment = create_single_assessment()
  learning_experience = create_single_learning_experience()
  submitted_assessment = create_single_submitted_assessment(False)
  # Preparing data for UT

  learner_user.user_type_ref = learner.id
  learner_user.user_id = learner_user.id
  learner_user.update()

  mocker.patch("routes.submitted_assessment.staff_to_learner_handler",
                return_value=[learner_user.user_type_ref])

  instructor_user.user_type = "instructor"
  instructor_user.update()

  submitted_assessment.learner_id = learner.id
  submitted_assessment.assessment_id = assessment.id
  submitted_assessment.uuid = submitted_assessment.id
  submitted_assessment.is_flagged = True
  submitted_assessment.comments = [{
        "comment": "Flagged comment",
        "type": "flag",
        "access": instructor_user.user_id,
        "author": "assessor1"
    }]
  submitted_assessment.update()

  learning_experience.child_nodes = {"assessments": [assessment.id]}
  learning_experience.uuid = learning_experience.id
  learning_experience.update()

  assessment.parent_nodes = {"learning_experiences": [learning_experience.id]}
  assessment.instructor_id = instructor_user.id
  assessment.learner_id = learner.id
  assessment.update()

  learner.uuid = learner.id
  learner.update()

  get_url = f"{api_url}/submitted-assessments"
  # get the list of submitted assessments by filter
  # on instructor_id and type
  params = {
      "assessor_id": instructor_user.id,
      "is_flagged": True,
      "skip": 0,
      "limit": 2
  }
  get_resp = client_with_emulator.get(get_url, params=params)
  get_resp_json = get_resp.json()
  assert get_resp_json.get("success") is True, "Success not true"
  assert get_resp.status_code == 200, "Status 200"
  # check if the created submission and the fetched submissions are same
  assert get_resp_json.get("data")["records"][0]["instructor_id"] == \
      params["assessor_id"]
  assert get_resp_json.get("data")["records"][0]["is_flagged"] == \
      params["is_flagged"]


def test_get_latest_submitted_assessment(mocker, clean_firestore):

  input_submitted_assessment = SUBMITTED_ASSESSMENT_EXAMPLE

  learner = create_single_learner()
  learner.uuid = input_submitted_assessment["learner_id"]
  learner.update()
  assessment = create_single_assessment()
  user = create_single_user()
  input_submitted_assessment["assessment_id"] = assessment.uuid

  post_url = f"{api_url}/submitted-assessment"

  mocker.patch("services.submitted_assessment.traverse_up", return_value=None)
  mocker.patch(
      "services.submitted_assessment.assessor_handler",
      return_value=user.user_id)
  mocker.patch(
      "services.submitted_assessment.instructor_handler",
      return_value=None)
  mocker.patch(
      "services.submitted_assessment.fetch_response", return_value=None)
  # create a submitted assessment using POST
  post_resp = client_with_emulator.post(
      post_url, json=input_submitted_assessment)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"
  post_resp_json["data"]["learner_name"] = \
      learner.first_name + " " + learner.last_name
  post_resp_json["data"]["unit_name"] = ""
  post_resp_json["data"]["discipline_name"] = ""
  post_resp_json["data"]["assigned_to"] = user.first_name + " " + user.last_name
  post_resp_json["data"]["max_attempts"] = assessment.max_attempts
  post_resp_json["data"]["instructor_name"] = "Unassigned"
  post_resp_json["data"]["instructor_id"] = ""
  post_resp_json["data"]["assessment_name"] = None

  submitted_assessment_uuid = post_resp_json["data"]["uuid"]

  get_url = f"{api_url}/submitted-assessment/{submitted_assessment_uuid}/" +\
             "learner/latest-submission"

  # get the submitted assessment
  get_resp = client_with_emulator.get(get_url)
  get_resp_json = get_resp.json()
  assert get_resp_json.get("success") is True, "Success not true"
  assert get_resp.status_code == 200, "Status 200"
  # check if the created submission and the fetched submission are same
  post_resp_json["data"]["assessment_name"] = None
  assert get_resp_json.get("data") == post_resp_json.get("data")


@mock.patch("common.models.learner_profile.Learner",
            mock.MagicMock(side_effect=LearnerTest))
def test_get_submitted_assessment(mocker, clean_firestore, create_assessment):

  input_submitted_assessment = SUBMITTED_ASSESSMENT_EXAMPLE

  learner = create_single_learner()
  learner.uuid = input_submitted_assessment["learner_id"]
  learner.update()
  assessment = create_single_assessment()
  user = create_single_user()
  assessment.instructor_id = user.user_id
  assessment.update()
  input_submitted_assessment["assessment_id"] = assessment.uuid

  post_url = f"{api_url}/submitted-assessment"

  mocker.patch("services.submitted_assessment.traverse_up", return_value=None)
  mocker.patch(
      "services.submitted_assessment.assessor_handler",
      return_value="assessor_id")
  mocker.patch(
      "services.submitted_assessment.fetch_response", return_value=None)
  # create a submitted assessment using POST
  post_resp = client_with_emulator.post(
      post_url, json=input_submitted_assessment)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  submitted_assessment_uuid = post_resp_json.get("data")["uuid"]
  get_url = f"{api_url}/submitted-assessment/{submitted_assessment_uuid}"

  # get the submitted assessment
  get_resp = client_with_emulator.get(get_url)
  get_resp_json = get_resp.json()
  assert get_resp_json.get("success") is True, "Success not true"
  assert get_resp.status_code == 200, "Status 200"
  # check if the created submission and the fetched submission are same
  assert get_resp_json.get("data") == post_resp_json.get("data")


@mock.patch("common.models.learner_profile.Learner",
            mock.MagicMock(side_effect=LearnerTest))
def test_update_submitted_assessment(mocker, clean_firestore,
                                     create_assessment):

  input_submitted_assessment = SUBMITTED_ASSESSMENT_EXAMPLE

  learner = create_single_learner()
  learner.uuid = input_submitted_assessment["learner_id"]
  learner.update()
  assessment = create_single_assessment()
  user = create_single_user()
  assessment.instructor_id = user.user_id
  assessment.update()
  input_submitted_assessment["assessment_id"] = assessment.uuid

  post_url = f"{api_url}/submitted-assessment"

  mocker.patch("services.submitted_assessment.traverse_up", return_value=None)
  mocker.patch(
      "services.submitted_assessment.assessor_handler",
      return_value="assessor_id")
  mocker.patch(
      "services.submitted_assessment.fetch_response", return_value=None)
  # create a submitted assessment using POST
  post_resp = client_with_emulator.post(
      post_url, json=input_submitted_assessment)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  submitted_assessment_uuid = post_resp_json.get("data")["uuid"]
  put_url = f"{api_url}/submitted-assessment/{submitted_assessment_uuid}"

  update_submitted_assessment = UPDATE_SUBMITTED_ASSESSMENT_EXAMPLE
  # update the submitted assessment
  update_resp = client_with_emulator.put(
      put_url, json=update_submitted_assessment)
  update_resp_json = update_resp.json()
  assert update_resp_json.get("success") is True, "Success not true"
  assert update_resp.status_code == 200, "Status 200"

  update_flag = all(
      update_resp_json.get("data").get(key, None) == val
      for key, val in update_submitted_assessment.items())
  assert update_flag, "Submitted assessment not updated."


@mock.patch("common.models.learner_profile.Learner",
            mock.MagicMock(side_effect=LearnerTest))
def test_update_submitted_assessment_evaluate_from_rubrics(
  mocker, clean_firestore, create_assessment):

  input_submitted_assessment = SUBMITTED_ASSESSMENT_EXAMPLE

  learner = create_single_learner()
  learner.uuid = input_submitted_assessment["learner_id"]
  learner.update()
  assessment = create_single_assessment(create_rubric=True)
  user = create_single_user()
  assessment.instructor_id = user.user_id
  assessment.update()
  input_submitted_assessment["assessment_id"] = assessment.uuid

  post_url = f"{api_url}/submitted-assessment"

  mocker.patch("services.submitted_assessment.traverse_up", return_value=None)
  mocker.patch(
      "services.submitted_assessment.assessor_handler",
      return_value="assessor_id")
  mocker.patch(
      "services.submitted_assessment.fetch_response", return_value=None)
  # create a submitted assessment using POST
  post_resp = client_with_emulator.post(
      post_url, json=input_submitted_assessment)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  submitted_assessment_uuid = post_resp_json.get("data")["uuid"]
  put_url = f"{api_url}/submitted-assessment/{submitted_assessment_uuid}"

  update_submitted_assessment = UPDATE_SUBMITTED_ASSESSMENT_EXAMPLE
  update_submitted_assessment["overall_feedback"] = "feedback"
  update_submitted_assessment["submitted_rubrics"] = [
    {
      "rubric_criteria_id": "r_id1",
      "result": "Exemplary",
      "feedback": "feedback_1"
    },
    {
      "rubric_criteria_id": "r_id2",
      "result": "Proficient",
      "feedback": "feedback_2"
    },
    {
      "rubric_criteria_id": "r_id3",
      "result": "Needs Improvement",
      "feedback": "feedback_3"
    },
    {
      "rubric_criteria_id": "r_id4",
      "result": "Not Evident",
      "feedback": "feedback_4"
    }
  ]
  # update the submitted assessment
  update_resp = client_with_emulator.put(
      put_url, json=update_submitted_assessment)
  update_resp_json = update_resp.json()
  assert update_resp_json.get("success") is True, "Success not true"
  assert update_resp.status_code == 200, "Status 200"
  assert update_resp_json["data"]["result"] == "Not Evident", "wrong result"
  assert update_resp_json["data"]["status"] == "evaluated", "wrong status"
  assert update_resp_json["data"]["pass_status"] is False, "wrong pass_status"
  assert update_resp_json["data"]["overall_feedback"] == \
    update_submitted_assessment["overall_feedback"]
  assert update_resp_json["data"]["submitted_rubrics"] == \
    update_submitted_assessment["submitted_rubrics"]


@mock.patch("common.models.learner_profile.Learner",
            mock.MagicMock(side_effect=LearnerTest))
def test_update_submitted_assessment_evaluate_from_rubrics2(
  mocker, clean_firestore, create_assessment):

  input_submitted_assessment = SUBMITTED_ASSESSMENT_EXAMPLE

  learner = create_single_learner()
  learner.uuid = input_submitted_assessment["learner_id"]
  learner.update()
  assessment = create_single_assessment(create_rubric=True)
  user = create_single_user()
  assessment.instructor_id = user.user_id
  assessment.update()
  input_submitted_assessment["assessment_id"] = assessment.uuid

  post_url = f"{api_url}/submitted-assessment"

  mocker.patch("services.submitted_assessment.traverse_up", return_value=None)
  mocker.patch(
      "services.submitted_assessment.assessor_handler",
      return_value="assessor_id")
  mocker.patch(
      "services.submitted_assessment.fetch_response", return_value=None)
  # create a submitted assessment using POST
  post_resp = client_with_emulator.post(
      post_url, json=input_submitted_assessment)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  submitted_assessment_uuid = post_resp_json.get("data")["uuid"]
  put_url = f"{api_url}/submitted-assessment/{submitted_assessment_uuid}"

  update_submitted_assessment = UPDATE_SUBMITTED_ASSESSMENT_EXAMPLE
  update_submitted_assessment["overall_feedback"] = "feedback"
  update_submitted_assessment["submitted_rubrics"] = [
    {
      "rubric_criteria_id": "r_id1",
      "result": "Exemplary",
      "feedback": "feedback_1"
    },
    {
      "rubric_criteria_id": "r_id2",
      "result": "Proficient",
      "feedback": "feedback_2"
    },
    {
      "rubric_criteria_id": "r_id3",
      "result": "Exemplary",
      "feedback": "feedback_3"
    },
    {
      "rubric_criteria_id": "r_id4",
      "result": "Proficient",
      "feedback": "feedback_4"
    }
  ]
  # update the submitted assessment
  update_resp = client_with_emulator.put(
      put_url, json=update_submitted_assessment)
  update_resp_json = update_resp.json()
  assert update_resp_json.get("success") is True, "Success not true"
  assert update_resp.status_code == 200, "Status 200"
  assert update_resp_json["data"]["result"] == "Proficient", "wrong result"
  assert update_resp_json["data"]["status"] == "completed", "wrong status"
  assert update_resp_json["data"]["pass_status"] is True, "wrong pass_status"
  assert update_resp_json["data"]["overall_feedback"] == \
    update_submitted_assessment["overall_feedback"]
  assert update_resp_json["data"]["submitted_rubrics"] == \
    update_submitted_assessment["submitted_rubrics"]


@mock.patch("common.models.learner_profile.Learner",
            mock.MagicMock(side_effect=LearnerTest))
def test_update_submitted_assessment_evaluate_from_rubrics3(
  mocker, clean_firestore, create_assessment):

  input_submitted_assessment = SUBMITTED_ASSESSMENT_EXAMPLE

  learner = create_single_learner()
  learner.uuid = input_submitted_assessment["learner_id"]
  learner.update()
  assessment = create_single_assessment(create_rubric=True)
  user = create_single_user()
  assessment.instructor_id = user.user_id
  assessment.update()
  input_submitted_assessment["assessment_id"] = assessment.uuid

  post_url = f"{api_url}/submitted-assessment"

  mocker.patch("services.submitted_assessment.traverse_up", return_value=None)
  mocker.patch(
      "services.submitted_assessment.assessor_handler",
      return_value="assessor_id")
  mocker.patch(
      "services.submitted_assessment.fetch_response", return_value=None)
  # create a submitted assessment using POST
  post_resp = client_with_emulator.post(
      post_url, json=input_submitted_assessment)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  submitted_assessment_uuid = post_resp_json.get("data")["uuid"]
  put_url = f"{api_url}/submitted-assessment/{submitted_assessment_uuid}"

  update_submitted_assessment = UPDATE_SUBMITTED_ASSESSMENT_EXAMPLE
  update_submitted_assessment["overall_feedback"] = "feedback"
  update_submitted_assessment["submitted_rubrics"] = [
    {
      "rubric_criteria_id": "r_id1",
      "result": "Not Evident",
      "feedback": "feedback_1"
    },
    {
      "rubric_criteria_id": "r_id2",
      "result": "Needs Improvement",
      "feedback": "feedback_2"
    },
    {
      "rubric_criteria_id": "r_id3",
      "result": "Needs Improvement",
      "feedback": "feedback_3"
    },
    {
      "rubric_criteria_id": "r_id4",
      "result": "Not Evident",
      "feedback": "feedback_4"
    }
  ]
  # update the submitted assessment
  update_resp = client_with_emulator.put(
      put_url, json=update_submitted_assessment)
  update_resp_json = update_resp.json()
  assert update_resp_json.get("success") is True, "Success not true"
  assert update_resp.status_code == 200, "Status 200"
  assert update_resp_json["data"]["result"] == "Not Evident", "wrong result"
  assert update_resp_json["data"]["status"] == "evaluated", "wrong status"
  assert update_resp_json["data"]["pass_status"] is False, "wrong pass_status"
  assert update_resp_json["data"]["overall_feedback"] == \
    update_submitted_assessment["overall_feedback"]
  assert update_resp_json["data"]["submitted_rubrics"] == \
    update_submitted_assessment["submitted_rubrics"]


@mock.patch("common.models.learner_profile.Learner",
            mock.MagicMock(side_effect=LearnerTest))
def test_delete_submitted_assessment(mocker, clean_firestore,
                                     create_assessment):

  input_submitted_assessment = SUBMITTED_ASSESSMENT_EXAMPLE

  learner = create_single_learner()
  learner.uuid = input_submitted_assessment["learner_id"]
  learner.update()
  assessment = create_single_assessment()
  user = create_single_user()
  assessment.instructor_id = user.user_id
  assessment.update()
  input_submitted_assessment["assessment_id"] = assessment.uuid

  post_url = f"{api_url}/submitted-assessment"
  mocker.patch("services.submitted_assessment.traverse_up", return_value=None)
  mocker.patch(
      "services.submitted_assessment.assessor_handler",
      return_value="assessor_id")
  mocker.patch(
      "services.submitted_assessment.fetch_response", return_value=None)
  # create a submitted assessment using POST
  post_resp = client_with_emulator.post(
      post_url, json=input_submitted_assessment)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  submitted_assessment_uuid = post_resp_json.get("data")["uuid"]
  delete_url = f"{api_url}/submitted-assessment/{submitted_assessment_uuid}"

  # delete the submitted assessment
  update_resp = client_with_emulator.delete(delete_url)
  update_resp_json = update_resp.json()
  assert update_resp_json.get("success") is True, "Success not true"
  assert update_resp.status_code == 200, "Status 200"
  assert update_resp_json.get("message")==\
    "Successfully deleted the submitted assessment."


@mock.patch("common.models.learner_profile.Learner",
            mock.MagicMock(side_effect=LearnerTest))
def test_get_all_submitted_assessment_for_learner(mocker, clean_firestore):

  input_submitted_assessment = SUBMITTED_ASSESSMENT_EXAMPLE
  learner_id = SUBMITTED_ASSESSMENT_EXAMPLE["learner_id"]
  # assessment_id = SUBMITTED_ASSESSMENT_EXAMPLE["assessment_id"]

  learner = create_single_learner()
  learner.uuid = input_submitted_assessment["learner_id"]
  learner.update()
  assessment = create_single_assessment()
  instructor_user = create_single_user()
  instructor_user.user_type = "instructor"
  assessment.instructor_id = instructor_user.user_id
  assessment.update()
  input_submitted_assessment["assessment_id"] = assessment.uuid

  post_url = f"{api_url}/submitted-assessment"

  mocker.patch("services.submitted_assessment.traverse_up", return_value=None)
  mocker.patch(
      "services.submitted_assessment.assessor_handler",
      return_value="assessor_id")
  mocker.patch(
      "services.submitted_assessment.fetch_response", return_value=None)
  # create a submitted assessment using POST
  post_resp = client_with_emulator.post(
      post_url, json=input_submitted_assessment)
  post_resp_json = post_resp.json()
  post_resp_json["instructor_id"] = "user_id"
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"



  get_url = f"{api_url}/learner/{learner_id}/submitted-assessments/"

  # get the submitted assessment
  query_params = {"skip": 0, "limit": 1}
  get_resp = client_with_emulator.get(get_url, params=query_params)
  get_resp_json = get_resp.json()
  assert get_resp_json.get("success") is True, "Success not true"
  assert get_resp.status_code == 200, "Status 200"
  # check if the created submission and the fetched submission are same
  assert get_resp_json.get("data")["records"][0] == post_resp_json.get("data")

  # get the submitted assessment with filter on assessment_id
  query_params = {"skip": 0, "limit": 1, "assessment_id": \
                  post_resp_json.get("data")["assessment_id"]}
  get_resp = client_with_emulator.get(get_url, params=query_params)
  get_resp_json = get_resp.json()
  assert get_resp_json.get("success") is True, "Success not true"
  assert get_resp.status_code == 200, "Status 200"
  # check if the created submission and the fetched submission are same
  assert get_resp_json.get("data")["records"][0] == post_resp_json.get("data")


@mock.patch("common.models.learner_profile.Learner",
            mock.MagicMock(side_effect=LearnerTest))
def test_get_unique_values_submitted_assessments(clean_firestore,
                                                 create_assessment):

  learner_user = create_single_user()
  assessor_user = create_single_user()
  instructor_user = create_single_user()
  learner = create_single_learner()
  assessment = create_single_assessment()
  learning_experience = create_single_learning_experience()
  submitted_assessment = create_single_submitted_assessment()
  # Preparing data for UT

  learner_user.user_type_ref = learner.id
  learner_user.user_id = learner_user.id
  learner_user.update()

  assessor_user.user_type = "assessor"
  assessor_user.update()

  instructor_user.user_type = "instructor"
  instructor_user.update()

  submitted_assessment.assessor_id = assessor_user.id
  submitted_assessment.learner_id = learner.id
  submitted_assessment.assessment_id = assessment.id
  submitted_assessment.uuid = submitted_assessment.id
  submitted_assessment.update()

  learning_experience.child_nodes = {"assessments": [assessment.id]}
  learning_experience.uuid = learning_experience.id
  learning_experience.update()

  assessment.parent_nodes = {"learning_experiences": [learning_experience.id]}
  assessment.instructor_id = instructor_user.id
  assessment.learner_id = learner.id
  assessment.assessor_id = assessor_user.id
  assessment.uuid = assessment.id
  assessment.update()

  learner.uuid = learner.id
  learner.update()

  get_url = f"{api_url}/submitted-assessments/unique"
  query_params = {
    "assessor_id": assessor_user.id,
    "is_autogradable": submitted_assessment.is_autogradable
  }

  # get the unique values of unit_names, types and results
  get_resp = client_with_emulator.get(get_url, params=query_params)
  get_resp_json = get_resp.json()
  assert get_resp_json.get("success") is True, "Success not true"
  assert get_resp.status_code == 200, "Status 200"

  assert set(get_resp_json.get("data")["discipline_names"]) == set([])
  # check if the list of unit_names are same as the assessment unit_names
  assert set(get_resp_json.get("data")["unit_names"]) == \
    set([learning_experience.name])
  assert set(get_resp_json.get("data")["types"]) == \
      set([assessment.type])
  assert set(get_resp_json.get("data")["results"]) == set([])


def test_get_all_manual_evaluation_submitted_assessments_for_learner(
    clean_firestore,
    create_assessment):
  learner_user = create_single_user()
  assessor_user = create_single_user()
  instructor_user = create_single_user()
  learner = create_single_learner()
  assessment = create_single_assessment()
  learning_object = create_single_learning_object()
  learning_experience = create_single_learning_experience()
  submitted_assessment = create_single_submitted_assessment()
  # Preparing data for UT

  learner_user.user_type_ref = learner.id
  learner_user.user_id = learner_user.id
  learner_user.update()

  assessor_user.user_type = "assessor"
  assessor_user.update()

  instructor_user.user_type = "instructor"
  instructor_user.update()

  submitted_assessment.assessor_id = assessor_user.id
  submitted_assessment.learner_id = learner.id
  submitted_assessment.assessment_id = assessment.id
  submitted_assessment.uuid = submitted_assessment.id
  submitted_assessment.update()

  learning_experience.child_nodes = {"learning_objects": [learning_object.id]}
  learning_experience.uuid = learning_experience.id
  learning_experience.update()

  learning_object.parent_nodes = {
    "learning_experiences": [learning_experience.id]}
  learning_object.uuid = learning_object.id
  learning_object.update()

  assessment.parent_nodes = {"learning_objects": [learning_object.id]}
  assessment.instructor_id = instructor_user.id
  assessment.learner_id = learner.id
  assessment.assessor_id = assessor_user.id
  assessment.uuid = assessment.id
  assessment.update()

  learning_object.child_nodes = {"assessments": [assessment.id]}
  learning_object.update()

  learner.uuid = learner.id
  learner.update()

  get_url = (f"{api_url}/learner/{learner.uuid}/learning-experience/"
  f"{learning_experience.uuid}/submitted-assessments/manual-evaluation")

  # get the unique values of unit_names, types and results
  get_resp = client_with_emulator.get(get_url)
  get_resp_json = get_resp.json()
  assert get_resp_json.get("success") is True, "Success not true"
  assert get_resp.status_code == 200, "Status 200"
  assert get_resp_json.get("data")["records"][0][
    "submitted_assessments"][0]["learner_id"] == learner.uuid
  assert get_resp_json.get("data")["records"][0][
    "submitted_assessments"][0]["is_autogradable"] is False
