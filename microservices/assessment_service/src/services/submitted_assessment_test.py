"""Test file for submitted assessment endpoints."""
# pylint: disable=unused-argument,redefined-outer-name,unused-import
import os
import json
import copy
import pytest
from testing.submitted_assessment import TEST_LEARNOSITY_DATA
from testing.test_config import TESTING_FOLDER_PATH
from common.models import (Learner, Assessment, User, SubmittedAssessment,
                           Rubric)
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.assessor_handler import (
  replace_assessor_of_submitted_assessments,
  filter_submitted_assessments
)

from unittest import mock
from schemas.schema_examples import (SUBMITTED_ASSESSMENT_EXAMPLE)
with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  from config import PASS_THRESHOLD, UM_BASE_URL
  from services.submitted_assessment import (
      submit_assessment, evaluate_assessment, get_latest_submission,
      get_all_submission)

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"
RELATIVE_PATH = "../../../e2e/testing_objects/"
ASSESSMENT_TESTDATA_FILENAME = os.path.join(TESTING_FOLDER_PATH +
                                            "/assessment.json")
SUBMITTED_ASSESSMENT_TESTDATA_FILENAME = os.path.join(
    TESTING_FOLDER_PATH + "/submitted_assessment.json")


@pytest.fixture(name="create_assessment")
def fixture_create_assessment():
  # create an assessment
  with open(ASSESSMENT_TESTDATA_FILENAME, encoding="UTF-8") as json_file:
    assessment_fields = json.load(json_file)[0]
  assessment = Assessment()
  assessment = assessment.from_dict(assessment_fields)
  assessment.uuid = SUBMITTED_ASSESSMENT_EXAMPLE["assessment_id"]
  assessment.save()
  return assessment


def create_single_user(user_id="user_id", ref="learner1"):
  """create a user"""
  with open(RELATIVE_PATH + "user.json", encoding="UTF-8") as json_file:
    user_fields = json.load(json_file)[0]
  user_fields["user_id"] = user_id
  user_fields["user_type_ref"] = ref
  user = User()
  user = user.from_dict(user_fields)
  user.save()
  user.user_id = user.id
  user.update()
  return user


def create_single_learner():
  # create a learner
  with open(RELATIVE_PATH + "learner.json", encoding="UTF-8") as json_file:
    learner_fields = json.load(json_file)[0]
  learner_fields["learner_id"] = "learner_id"
  learner = Learner()
  learner = learner.from_dict(learner_fields)
  learner.save()
  return learner


def create_single_assessment(create_rubric = False):
  """create an assessment"""
  if create_rubric:
    rubric = Rubric()
    rubric.uuid = ""
    rubric.save()
    rubric.evaluation_criteria = {
      "0": "Exemplary",
      "1": "Proficient",
      "2": "Needs Improvement",
      "3": "Not Evident"
    }
    rubric.uuid = rubric.id
    rubric.update()

  with open(ASSESSMENT_TESTDATA_FILENAME, encoding="UTF-8") as json_file:
    assessment_fields = json.load(json_file)[0]
  assessment_fields["parent_nodes"]["learning_experiences"] = ["le_id"]
  assessment = Assessment()
  assessment = assessment.from_dict(assessment_fields)
  assessment.uuid = ""
  assessment.save()
  assessment.uuid = assessment.id
  if create_rubric:
    assessment.child_nodes = {
      "rubrics": [rubric.uuid]
    }
  assessment.update()
  return assessment


class LearnerTest():

  @classmethod
  def find_by_uuid(cls, uuid, is_deleted=False):
    learner = Learner()
    return learner


submitted_assessment_request = SUBMITTED_ASSESSMENT_EXAMPLE

submitted_assessment_response = {
    **submitted_assessment_request, "type": "practice",
    "pass_status": None,
    "status": "evaluation_pending",
    "attempt_no": 1,
    "learner_session_data": None,
    "submission_gcs_paths": [],
    "is_flagged": False,
    "assessor_id": None,
    "comments": None,
    "plagiarism_report_path": None,
    "plagiarism_score": None,
    "result": None,
    "assessor_session_id": None,
    "is_deleted": False,
    "is_autogradable": False,
    "metadata": {"tag_info": {}},
    "submitted_rubrics": None,
    "overall_feedback": None
}


def create_submitted_assessment(input_submitted_assessment):
  # create an assessment
  sub_assessment = SubmittedAssessment()
  sub_assessment = sub_assessment.from_dict(input_submitted_assessment)
  sub_assessment.uuid = ""
  sub_assessment.save()
  sub_assessment.uuid = sub_assessment.id
  sub_assessment.update()
  return sub_assessment


@mock.patch("common.models.learner_profile.Learner",
            mock.MagicMock(side_effect=LearnerTest))
@pytest.mark.parametrize(
    "input_submitted_assessment,output",
    [(submitted_assessment_request, submitted_assessment_response)])
def test_submit_assessment(clean_firestore, mocker, input_submitted_assessment,
                           output, create_assessment):

  mocker.patch(
      "services.submitted_assessment.evaluate_assessment", return_value=True)
  # set the previous submitted assessment same as the current except
  # attempt no should be current - 1
  last_submitted_assessment = copy.deepcopy(submitted_assessment_response)
  last_submitted_assessment[
      "attempt_no"] = last_submitted_assessment["attempt_no"] - 1

  mocker.patch(
      "services.submitted_assessment.get_latest_submission",
      return_value=last_submitted_assessment)
  mocker.patch("services.submitted_assessment.traverse_up", return_value=None)
  mocker.patch(
      "services.submitted_assessment.assessor_handler", return_value=None)
  mocker.patch(
      "services.submitted_assessment.fetch_response", return_value=None)
  mocker.patch(
    "services.assessment_content_helper.attach_files_to_assessment_submission",
    return_value=None
  )
  learner = create_single_learner()
  learner.uuid = input_submitted_assessment["learner_id"]
  learner.update()
  assessment = create_single_assessment()
  user = create_single_user()
  assessment.instructor_id = user.user_id
  assessment.update()
  input_submitted_assessment["assessment_id"] = assessment.uuid
  #FIXME: Update the UT logic for attempt_no

  submission_output = submit_assessment(input_submitted_assessment, "token")
  assert submission_output["timer_start_time"] == submission_output[
      "created_time"]
  del submission_output["id"]
  del submission_output["timer_start_time"]
  del submission_output["created_time"]
  del submission_output["last_modified_time"]
  del submission_output["created_by"]
  del submission_output["last_modified_by"]
  del submission_output["uuid"]
  del submission_output["archived_at_timestamp"]
  del submission_output["archived_by"]
  del submission_output["deleted_at_timestamp"]
  del submission_output["deleted_by"]
  output["assessment_id"]= assessment.uuid
  assert submission_output == output


learnosity_data = TEST_LEARNOSITY_DATA["data"][0]


@pytest.mark.parametrize("learnosity_data,expected_evaluation",
                         [(learnosity_data, True)])
def test_evaluate_assessment(clean_firestore, learnosity_data,
                             expected_evaluation):
  output_evaluation = evaluate_assessment(learnosity_data, PASS_THRESHOLD)
  assert output_evaluation == expected_evaluation


def test_get_all_submission(mocker, clean_firestore):
  # get created assessment object

  input_submitted_assessment = SUBMITTED_ASSESSMENT_EXAMPLE

  learner = create_single_learner()
  learner.uuid = input_submitted_assessment["learner_id"]
  learner.update()
  assessment = create_single_assessment()
  user = create_single_user()
  input_submitted_assessment["assessment_id"] = assessment.uuid

  mocker.patch("services.submitted_assessment.traverse_up", return_value=None)
  mocker.patch(
      "services.submitted_assessment.assessor_handler",
      return_value=user.user_id)
  mocker.patch(
      "services.submitted_assessment.instructor_handler",
      return_value=None)
  mocker.patch(
      "services.submitted_assessment.get_latest_submission", return_value=None)
  mocker.patch(
      "services.submitted_assessment.fetch_response", return_value=None)
  submitted_assessment_dict = submit_assessment(input_submitted_assessment,
                                                None)
  submitted_assessment_dict["learner_name"] = \
      learner.first_name + " " + learner.last_name
  submitted_assessment_dict["unit_name"] = ""
  submitted_assessment_dict["discipline_name"] = ""
  submitted_assessment_dict["assigned_to"] = user.first_name + " " + \
      user.last_name
  submitted_assessment_dict["max_attempts"] = assessment.max_attempts
  submitted_assessment_dict["instructor_id"] = ""
  submitted_assessment_dict["instructor_name"] = "Unassigned"
  submitted_assessment_dict["assessment_name"] = assessment.display_name
  submitted_assessment_dict["attempt_no"] = 1

  submitted_assessment_uuid = submitted_assessment_dict["uuid"]
  all_submissions = get_all_submission(submitted_assessment_uuid, 0, 2)
  assert all_submissions == [submitted_assessment_dict]


def test_latest_submitted_assessment(mocker, clean_firestore):
  # get created assessment object

  input_submitted_assessment = SUBMITTED_ASSESSMENT_EXAMPLE

  learner = create_single_learner()
  learner.uuid = input_submitted_assessment["learner_id"]
  learner.update()
  assessment = create_single_assessment()
  assessment.uuid = assessment.id
  assessment.update()
  input_submitted_assessment["assessment_id"] = assessment.uuid

  user = create_single_user()

  mocker.patch("services.submitted_assessment.traverse_up", return_value=None)
  mocker.patch(
      "services.submitted_assessment.assessor_handler",
      return_value=user.user_id)
  mocker.patch(
      "services.submitted_assessment.instructor_handler",
      return_value=None)
  mocker.patch(
      "services.submitted_assessment.get_latest_submission",
      return_value={"attempt_no": 1})
  mocker.patch(
      "services.submitted_assessment.fetch_response", return_value=None)
  #FIXME: Update the UT logic for attempt_no
  for i in range(2):
    submitted_assessment_dict = submit_assessment(input_submitted_assessment,
                                                  None)
    submitted_assessment_dict["learner_name"] = \
        learner.first_name + " " + learner.last_name
    submitted_assessment_dict["unit_name"] = ""
    submitted_assessment_dict["discipline_name"] = ""
    submitted_assessment_dict["assigned_to"] = user.first_name + " " + \
      user.last_name
    submitted_assessment_dict["max_attempts"] = assessment.max_attempts
    submitted_assessment_dict["instructor_id"] = ""
    submitted_assessment_dict["instructor_name"] = "Unassigned"
    submitted_assessment_dict["assessment_name"] = assessment.display_name
    submitted_assessment_dict["attempt_no"] = i

  learner_id = submitted_assessment_dict["learner_id"]
  assessment_id = submitted_assessment_dict["assessment_id"]
  latest_submission = get_latest_submission(learner_id, assessment_id)
  assert latest_submission == submitted_assessment_dict
