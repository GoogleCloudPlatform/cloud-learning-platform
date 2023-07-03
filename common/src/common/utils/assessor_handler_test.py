"""Unit test for assessor handler"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from unittest import mock
with mock.patch(
    "google.cloud.logging.Client",
    side_effect=mock.MagicMock()) as mok:
  from common.models import (
      User,
      Learner,
      Assessment,
      SubmittedAssessment
  )
from common.utils.assessor_handler import (
    replace_assessor_of_submitted_assessments,
    update_assessor_of_submitted_assessments_of_a_discipline,
    filter_submitted_assessments
)
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)

SUBMITTED_ASSESSMENT_EXAMPLE = {
    "assessment_id": "assessment1",
    "learner_id": "learner1",
    "learner_session_id": "learner_session_id1",
    "attempt_no": 1,
    "submission_gcs_paths": []
}

USER_EXAMPLE = {
    "first_name": "user01",
    "last_name": "abc",
    "email": "dweh4gf834gh34fh34jff39h@gmail.com",
    "status": "active",
    "user_type": "learner",
    "user_groups": [],
    "is_registered": True,
    "failed_login_attempts_count": 0,
    "user_type_ref": "learner1",
    "gaia_id": "F2GGRg5etyty",
    "photo_url": "//lh3.googleusercontent.com/a/default-user"
}

LEARNER_EXAMPLE = {
    "uuid": "tzlyrXWaSDC4n2XwQabX",
    "first_name": "Jon",
    "middle_name": "Jon",
    "last_name": "Doe",
    "suffix": "",
    "prefix": "",
    "preferred_name": "",
    "preferred_first_name": "",
    "preferred_middle_name": "",
    "preferred_last_name": "",
    "preferred_name_type": "PreferredName",
    "preferred_pronoun": "",
    "student_identifier": "",
    "student_identification_system": "",
    "personal_information_verification": "",
    "personal_information_type": "",
    "address_type": "",
    "street_number_and_name": "",
    "apartment_room_or_suite_number": "",
    "city": "",
    "state_abbreviation": "",
    "postal_code": "",
    "country_name": "",
    "country_code": "",
    "latitude": "",
    "longitude": "",
    "country_ansi_code": 10000,
    "address_do_not_publish_indicator": "Yes",
    "phone_number": {
      "mobile": {
        "phone_number_type": "Work",
        "primary_phone_number_indicator": "Yes",
        "phone_number": "",
        "phone_do_not_publish_indicator": "Yes",
        "phone_number_listed_status": "Listed"
      },
      "telephone": {
        "phone_number_type": "Home",
        "primary_phone_number_indicator": "No",
        "phone_number": "",
        "phone_do_not_publish_indicator": "Yes",
        "phone_number_listed_status": "Listed"
      }
    },
    "email_address_type": "Work",
    "email_address": "jon.doe@gmail.com",
    "email_do_not_publish_indicator": "Yes",
    "backup_email_address": "jon.doe2@gmail.com",
    "birth_date": "",
    "gender": "NotSelected",
    "country_of_birth_code": "",
    "ethnicity": "",
    "employer_id": "test_employer_id",
    "employer": "",
    "employer_email": "test@mail.com",
    "organisation_email_id": "jon.doe@foobar.com",
    "affiliation": "",
    "is_archived": False
  }

ASSESSMENT_EXAMPLE = {
    "name": "Assessment 1",
    "type": "practice",
    "author_id": "author_id",
    "instructor_id": "instructor_id",
    "instructor_name": "instructor_name",
    "assessor_id": "assessor_id",
    "assessment_reference": {},
    "max_attempts": 3,
    "pass_threshold": 0.7,
    "achievements": [],
    "alignments": {},
    "references": {},
    "parent_nodes": {"learning_experiences": [], "learning_objects": []},
    "child_nodes": {},
    "prerequisites": {},
    "metadata": {}
  }

SUBMITTED_ASSESSMENT_EXAMPLE_2 = {
    "assessment_id": "WcHMiIgfSa639iY4eEAe",
    "learner_id": "00QjHUTZ4WUpzxBVZQoV",
    "assessor_id": None,
    "type": "practice",
    "is_autogradable": False,
    "plagiarism_score": None,
    "plagiarism_report_path": None,
    "submission_gcs_paths": [],
    "result": None,
    "pass_status": True,
    "status": "evaluated",
    "is_flagged": False,
    "comments": None,
    "attempt_no": 1,
    "learner_session_id": "learner_session_id1",
    "learner_session_data": {
        "activity_id": "chemistry_classtest1",
        "user_id": "17c456c0-89ad-4f72-8010-2f7d991f54bd",
        "max_score": 40,
        "status": "Completed",
        "subscores": [
            {
                "score": 19,
                "id": "subscore-1",
                "attempted_max_score": 20,
                "items": [
                    "293486384",
                    "293481468",
                    "293475858",
                    "293475234",
                    "292922805"
                ],
                "num_attempted": 20,
                "max_score": 20,
                "num_questions": 20,
                "title": "biochem"
            },
            {
                "num_attempted": 20,
                "max_score": 20,
                "score": 20,
                "items": [
                    "293486384",
                    "293481468",
                    "293475858",
                    "293475234",
                    "292922805"
                ],
                "num_questions": 20,
                "attempted_max_score": 20,
                "title": "inorganics",
                "id": "subscore-2"
            }
        ],
        "session_id": "4d3115f0-1235-4613-5be6fc6e6b2e",
        "responses": [
            {
                "item_reference": "293486384",
                "dt_score_updated": "2017-06-19T02:03:19Z",
                "response_id": "2571d802-0095-4d66-94bc-4cfa44b0ebbe",
                "max_score": 1,
                "score": 1
            }
        ],
        "score": 39
    },
    "assessor_session_id": None
  }

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

# -----------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------

def create_single_user(user_id="user_id", ref="learner1"):
  """Function to create user"""
  # create a user
  user_fields = USER_EXAMPLE
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
  learner_fields = LEARNER_EXAMPLE
  learner_fields["learner_id"] = "learner_id"
  learner = Learner()
  learner = learner.from_dict(learner_fields)
  learner.save()
  return learner

def create_single_assessment():
  """Function to create assessment"""
  # create an assessment
  assessment_fields = ASSESSMENT_EXAMPLE
  assessment_fields["parent_nodes"]["learning_experiences"] = ["le_id"]
  assessment = Assessment()
  assessment = assessment.from_dict(assessment_fields)
  assessment.uuid = ""
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()
  return assessment

def create_single_submitted_assessment(assign_assessor=True):
  """Function to create submitted assessment"""
  # create a submitted assessment
  sa_fields = SUBMITTED_ASSESSMENT_EXAMPLE_2
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

def create_submitted_assessment(input_submitted_assessment):
  # create an assessment
  sub_assessment = SubmittedAssessment()
  sub_assessment = sub_assessment.from_dict(input_submitted_assessment)
  sub_assessment.uuid = ""
  sub_assessment.save()
  sub_assessment.uuid = sub_assessment.id
  sub_assessment.update()
  return sub_assessment

# -----------------------------------------------------------------------------
# UNIT TESTS
# -----------------------------------------------------------------------------

def test_replace_assessor_with_new_assessor_for_submitted_assessments(
    mocker, clean_firestore):

  assessor_user = create_single_user()
  assessor_user.user_type = "assessor"
  assessor_user.update()
  new_assessor_user = create_single_user()
  new_assessor_user.user_type = "assessor"
  new_assessor_user.update()
  assessment = create_single_assessment()
  submitted_assessment = create_single_submitted_assessment()

  submitted_assessment.assessor_id = assessor_user.id
  submitted_assessment.assessment_id = assessment.id
  submitted_assessment.uuid = submitted_assessment.id
  submitted_assessment.update()

  discipline_id = "test_discipline_id"
  # get created assessment object

  mocker.patch(
      "common.utils.assessor_handler.traverse_down",
      return_value=[assessment.uuid])
  mocker.patch(
      "common.utils.assessor_handler.get_assessors_of_dag",
      return_value=[{
          "user": assessor_user.user_id
      }, {
          "user": new_assessor_user.user_id
      }])

  task_status, _ = update_assessor_of_submitted_assessments_of_a_discipline(
    "random_dag_id",
    discipline_id,{
        "user": assessor_user.user_id
    })
  assert task_status == 1

  get_submitted_assessment_1 = SubmittedAssessment.find_by_uuid(
      submitted_assessment.uuid)
  assert get_submitted_assessment_1.assessor_id == new_assessor_user.user_id

def test_remove_assessor_for_submitted_assessments_of_discipline(
    mocker, clean_firestore):

  assessor_user = create_single_user()
  assessor_user.user_type = "assessor"
  assessor_user.update()
  new_assessor_user = create_single_user()
  new_assessor_user.user_type = "assessor"
  new_assessor_user.update()
  assessment = create_single_assessment()
  submitted_assessment = create_single_submitted_assessment()

  submitted_assessment.assessor_id = assessor_user.id
  submitted_assessment.assessment_id = assessment.id
  submitted_assessment.uuid = submitted_assessment.id
  submitted_assessment.update()

  discipline_id = "test_discipline_id"
  dag_id = "dag_id"
  # create assessment object
  mocker.patch(
      "common.utils.assessor_handler.traverse_down",
      return_value=[assessment.uuid])
  mocker.patch(
      "common.utils.assessor_handler.get_assessors_of_dag",
      return_value=[{
          "user": assessor_user.user_id
      }])

  task_status, _ = update_assessor_of_submitted_assessments_of_a_discipline(
                                                            dag_id,
                                                            discipline_id)

  assert task_status == 1

  get_submitted_assessment_1 = SubmittedAssessment.find_by_uuid(
      submitted_assessment.uuid)
  assert get_submitted_assessment_1.assessor_id == ""

def test_replace_assessor_with_new_assessor_for_submitted_assessments_negative(
    mocker, clean_firestore):

  discipline_id = "test_discipline_id"
  # get created assessment object

  submitted_assessement_1 = create_submitted_assessment(
      {**submitted_assessment_response})

  mocker.patch(
      "common.utils.assessor_handler.get_assessors_of_dag",
      return_value=[{
          "user": submitted_assessement_1.assessor_id
      }])

  submitted_assessments = filter_submitted_assessments(
      [submitted_assessement_1.assessment_id],
      submitted_assessement_1.assessor_id)
  replace_assessor_of_submitted_assessments(
                                    discipline_id,
                                    submitted_assessments,
                                    [submitted_assessement_1.assessment_id],
                                    submitted_assessement_1.assessor_id)
  get_submitted_assessment_1 = SubmittedAssessment.find_by_uuid(
      submitted_assessement_1.uuid)
  assert get_submitted_assessment_1.assessor_id == ""

