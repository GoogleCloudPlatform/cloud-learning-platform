"""Functions for submitted assessment endpoints."""
import json
import traceback
from common.models import Assessment, Learner, SubmittedAssessment, User
from common.utils.gcs_adapter import is_valid_path
from common.utils.collection_references import (collection_references)
from common.utils.errors import PreconditionFailedError, ValidationError
from common.utils.logging_handler import Logger
from common.utils.rest_method import get_method
from config import (UM_BASE_URL, USE_LEARNOSITY_SECRET,
                    CONTENT_SERVING_BUCKET)
from services.data_utils import (fetch_response, get_user_name,
                                 update_item_responses)
from services.assessment_content_helper import\
  attach_files_to_assessment_submission

ITEM_REFERENCES = "testing/item_references.json"
LEARNOSITY_DATA = "testing/response.json"

#pylint: disable=broad-exception-raised,too-many-function-args


def staff_to_learner_handler(header, staff_id: str, user_type):
  """
  Function to get all the users associated to a staff from learner association
  """
  api_url = f"{UM_BASE_URL}/association-groups/learner-association/"+\
            f"{user_type}/{staff_id}/learners"
  query_params = {"fetch_tree": True}

  users = get_method(
      url=api_url,
      query_params=query_params,
      token=header.get("Authorization")
  )
  # Raise the exception if API call fail
  if users.status_code != 200:
    raise Exception("User management service internal server error")

  users_list = users.json()["data"]
  ## TODO: This will not be required once learner_ids are replaced with
  ## user_ids for submitted assessments
  learner_ids = [user.get("user_type_ref") for user in users_list
                 if user.get("user_type_ref")]

  return learner_ids


def instructor_handler(header, curriculum_pathway_id: str):
  """
  Function to get the instructor assigned to the discipline
  """
  api_url = f"{UM_BASE_URL}/association-groups/discipline-association/"+\
            f"discipline/{curriculum_pathway_id}/users"
  query_params = {"user_type": "instructor", "fetch_tree": False}

  instructors = get_method(
      url=api_url,
      query_params=query_params,
      token=header.get("Authorization"))

  # Raise the exception if API call fail
  if instructors.status_code != 200:
    raise Exception("User management service internal server error")

  instructors_list = instructors.json()["data"]
  if instructors_list:
    instructor = instructors_list[0]
  else:
    instructor = None

  return instructor


def assessor_handler(header, curriculum_pathway_id: str):
  """
  Function use to assign the assessor to the
  given submitted assessment
  To solve this we have design custom
  RoundRobin Algorithm
  """
  api_url = f"{UM_BASE_URL}/association-groups/discipline-association/"+\
            f"discipline/{curriculum_pathway_id}/users"
  query_params = {"user_type": "assessor", "fetch_tree": True}

  # FIXME: Improve the API call using multithreading
  # logic to fetch all the assessor
  # rather then limit to 500

  # FIXME: Add more user_type in the user model

  assessors = get_method(
      url=api_url,
      query_params=query_params,
      token=header.headers.get("authorization"))

  # Raise the exception if API call fail
  if assessors.status_code != 200:
    Logger.info(f"Status code: {assessors.status_code}")
    Logger.info(f"API Response: {assessors.json()}")
    # raise Exception("User management service internal server error")
    return None

  assessor_list = assessors.json()["data"]

  if assessor_list and len(assessor_list) > 0:
    assessor_list = [assessor["user_id"] for assessor in assessor_list]

    collection_manager = SubmittedAssessment.collection
    last_submitted_assessment = collection_manager.order("-created_time").get()

    if last_submitted_assessment:
      last_submitted_assessment = last_submitted_assessment.get_fields(
          reformat_datetime=True)
      if last_submitted_assessment["assessor_id"] is None:
        assessor_id = assessor_list[0]
      elif last_submitted_assessment[
          "assessor_id"] is not None and last_submitted_assessment[
              "assessor_id"] == assessor_list[-1]:
        assessor_id = assessor_list[0]
      else:
        if last_submitted_assessment["assessor_id"] not in assessor_list:
          assessor_id = assessor_list[0]
        else:
          assessor_id = assessor_list[(assessor_list.index(
              last_submitted_assessment["assessor_id"]) + 1) %
                                      len(assessor_list)]
    else:
      assessor_id = assessor_list[0]
    return assessor_id

def submit_assessment(submitted_assessment_dict, header):
  """Helper function to handle the submit assessment flow"""
  assessor_id = None
  pass_status = None
  result = None
  session_data = None
  items = {}

  assessment_id = submitted_assessment_dict["assessment_id"]
  assessment = Assessment.find_by_uuid(assessment_id)
  is_autogradable = assessment.is_autogradable
  max_attempts = assessment.max_attempts
  attempt_no = submitted_assessment_dict["attempt_no"]
  submission_gcs_paths = submitted_assessment_dict.get(
    "submission_gcs_paths", [])
  valid_gcs_path = bool(submission_gcs_paths)
  #pylint: disable=chained-comparison
  if max_attempts is not None and max_attempts > 0 and \
    attempt_no > max_attempts:
    raise PreconditionFailedError(
      f"Allowed number of attempts exceeded ({attempt_no}/{max_attempts})")

  learner_id = submitted_assessment_dict["learner_id"]
  Learner.find_by_uuid(learner_id)
  user = User.find_by_user_type_ref(learner_id)

  if is_autogradable:
    activity_id = assessment.assessment_reference
    if activity_id is not None and activity_id != {}:
      activity_id = activity_id.get("activity_template_id", None)

    learnosity_req_body = {
        "user_id": user.id,
        "session_id": submitted_assessment_dict["learner_session_id"],
        "activity_id": activity_id
    }
    if USE_LEARNOSITY_SECRET:
      session_data = fetch_response(**learnosity_req_body)
      if assessment.metadata is not None:
        items = assessment.metadata.get("items", {})
      items = update_item_responses(items, session_data)
    # Autogradable assessments are always passed

    # Load Sample data to run e2e for pretests
    if not USE_LEARNOSITY_SECRET and assessment.type == "pretest":
      with open(LEARNOSITY_DATA, encoding="utf-8") as data:
        session_data = json.load(data)
      with open(ITEM_REFERENCES, encoding="utf-8") as data:
        items = json.load(data)
    pass_status = True
    status = "completed"
    result = "Pass"
  else:
    status = "evaluation_pending"
    if submission_gcs_paths:
      for path in submission_gcs_paths:
        path = f"gs://{CONTENT_SERVING_BUCKET}/{path}"
        valid_current_gcs_path = is_valid_path(path)
        valid_gcs_path = valid_gcs_path and valid_current_gcs_path
        if not valid_current_gcs_path:
          raise ValidationError(
            "The following GCS Path for the assessment submission does" +\
              f" not exist: {path}")
    # assign assessor only if assessment is human graded and is not an srl
    # or pretest
    if assessment.type not in ["srl", "static_srl", "cognitive_wrapper",
                               "pretest"]:
      discipline = traverse_up(assessment, "assessments", "discipline")
      pathway_id = discipline.get_fields()[
        "uuid"] if discipline is not None else ""
      assessor_id = assessor_handler(header, pathway_id)

  # create document for submitted_assessment
  submitted_assessment_dict = {
    **submitted_assessment_dict, "type": assessment.type,
    "pass_status": pass_status,
    "status": status,
    "result": result,
    "attempt_no": attempt_no,
    "is_autogradable": is_autogradable,
    "learner_session_data": session_data,
    "metadata": {
      "tag_info": items
    }
  }
  new_submitted_assessment = SubmittedAssessment()
  new_submitted_assessment = new_submitted_assessment.from_dict(
      submitted_assessment_dict)
  new_submitted_assessment.assessor_id = assessor_id
  new_submitted_assessment.uuid = ""
  new_submitted_assessment.save()
  new_submitted_assessment.uuid = new_submitted_assessment.id
  if valid_gcs_path:
    attached_files_path = attach_files_to_assessment_submission(
            learner_id, assessment_id, new_submitted_assessment.id,
            submission_gcs_paths, CONTENT_SERVING_BUCKET)
    new_submitted_assessment.submission_gcs_paths = attached_files_path
  elif submission_gcs_paths:
    raise ValidationError(
          "Some of the GCS Path for the assessment submission does not exist")
  new_submitted_assessment.timer_start_time = \
      new_submitted_assessment.created_time
  new_submitted_assessment.update()

  submitted_assessment_fields = new_submitted_assessment.get_fields(
      reformat_datetime=True)
  submitted_assessment_fields["timer_start_time"] = str(
      submitted_assessment_fields["timer_start_time"])
  return submitted_assessment_fields


def evaluate_assessment(learnosity_data, pass_threshold):
  """Function to evaluate the assessment based on scores earned
  and max_score possible for the given assessment
  Args:
    learnosity_data (dict): {}
    pass_threshold (float): 0.7
  Returns:
    True: If score >= pass_threshold
    False: If score < pass_threshold
  """
  if not learnosity_data:
    return False
  student_score = learnosity_data["score"]
  max_score = learnosity_data["max_score"]

  if student_score / max_score >= pass_threshold:
    return True
  return False


def get_all_submission(submitted_assessment_uuid, skip, limit, header=None):
  """
  Function to get the latest submission for a learner on an assessment.
  Args:
    submitted_assessment_uuid: Unique identifier for submitted_assessment
    skip (int): Number of objects to be skipped
    limit (int): Size of submitted assessment array to be returned
  Returns:
    submitted_assessments: List of SubmittedAssessment object
  """
  submitted_assessment = SubmittedAssessment.find_by_uuid(
      submitted_assessment_uuid)
  assessment_id = submitted_assessment.assessment_id
  learner_id = submitted_assessment.learner_id

  Assessment.find_by_uuid(assessment_id)
  Learner.find_by_uuid(learner_id)

  collection_manager = SubmittedAssessment.collection
  # TODO: filter by assessor id because we need to display
  # the submitted assessments assigned to an assessor
  collection_manager = collection_manager.filter("is_deleted", "==", False)
  collection_manager = collection_manager.filter("learner_id", "==", learner_id)
  collection_manager = collection_manager.filter("assessment_id", "==",
                                                 assessment_id)

  submitted_assessments = collection_manager.order("-created_time").offset(
      skip).fetch(limit)
  learner_submitted_assessments = []
  for submitted_assessment in submitted_assessments:
    submitted_assessment_data = \
      get_submitted_assessment_data(submitted_assessment, True, header)
    learner_submitted_assessments.append(submitted_assessment_data)
  return learner_submitted_assessments


def get_latest_submission(learner_id, assessment_id,
                get_unit_discipline_instructor_data=True, header=None):
  """
  Function to get the latest submission for a learner on an assessment.
  Args:
    learner_id (str): Unique identifier for Learner
    assessment_id (str): Unique identifier for Assessment
    get_unit_discipline_instructor_data (bool): if the unit name, discipline
          name and instructor name and id is to be returned in the
          submitted_assessment dictionary
  Returns:
    latest_submitted_assessment: SubmittedAssessment object
  """

  Assessment.find_by_uuid(assessment_id)
  Learner.find_by_uuid(learner_id)

  collection_manager = SubmittedAssessment.collection
  # TODO: filter by assessor id because we need to display
  # the submitted assessments assigned to an assessor
  collection_manager = collection_manager.filter("is_deleted", "==", False)
  collection_manager = collection_manager.filter("learner_id", "==", learner_id)
  collection_manager = collection_manager.filter("assessment_id", "==",
                                                 assessment_id)
  latest_submitted_assessment = collection_manager.order("-created_time").get()
  if latest_submitted_assessment:

    latest_submitted_assessment = get_submitted_assessment_data(
          latest_submitted_assessment, get_unit_discipline_instructor_data,
          header)

    latest_submitted_assessment["timer_start_time"] = str(
        latest_submitted_assessment["timer_start_time"])
  else:
    latest_submitted_assessment = {}
  return latest_submitted_assessment


def get_submitted_assessment_data(submitted_assessment,
    get_unit_discipline_instructor_data=True, header=None,
    assessment_node=None, assessor_map = None):
  """
  Function to get all data for a submitted assessment to be returned to assessor
  Args:
    submitted_assessment: SubmittedAssessment object
    get_unit_discipline_instructor_data (bool): if the unit name, discipline
          name and instructor name and id is to be returned in the
          submitted_assessment dictionary
    header: Authorization header
    assessment_node: pre fetched Assessment object
    assessor_map: hashmap to store existing assessors
  Returns:
    submitted_assessment: all submitted assessment required by assessor
  """

  submitted_assessment = submitted_assessment.get_fields(reformat_datetime=True)
  # Fetching and Validating Learner, Assessment, Assessor and Instructor data
  learner = Learner.find_by_uuid(submitted_assessment[
    "learner_id"]).get_fields()
  if assessment_node is None:
    assessment_node = Assessment.find_by_uuid(
      submitted_assessment["assessment_id"])
  assessment_data = assessment_node.get_fields(reformat_datetime=True)

  assessor_id = submitted_assessment.get("assessor_id")
  assessor = None
  if assessor_id:
    if isinstance(assessor_map, dict) and assessor_id in assessor_map:
      assessor = assessor_map[assessor_id]
    else:
      try:
        assessor = User.find_by_user_id(submitted_assessment[
          "assessor_id"]).get_fields()
        assessor_map[assessor_id] = {
          "first_name": assessor.get("first_name", ""),
          "last_name": assessor.get("last_name", "")
        }
      except Exception as e:
        Logger.error(e)
        Logger.error(traceback.print_exc())

  if get_unit_discipline_instructor_data:
    try:
      le_node = traverse_up(assessment_node, "assessments",
        "learning_experience")
      le_data = le_node.get_fields()
    except Exception as e:
      Logger.error(e)
      Logger.error(traceback.print_exc())
      Logger.info("Passing Empty Dict to Get Success Response")
      le_data = {}

    try:
      discipline_data = traverse_up(le_node, "learning_experiences",
          "discipline").get_fields()
    except Exception as e:
      Logger.error(e)
      Logger.error(traceback.print_exc())
      Logger.info("Passing Empty Dict to Get Success Response")
      discipline_data = {}

    try:
      instructor_id = instructor_handler(header, discipline_data["uuid"])
      instructor_data = User.find_by_user_id(instructor_id).get_fields()
      submitted_assessment["instructor_id"] = instructor_data.get("user_id", "")
      submitted_assessment["instructor_name"] = (instructor_data.get(
        "first_name", "") + " " + instructor_data.get("last_name", "")).lstrip()
    except Exception as e:
      Logger.error(e)
      Logger.error(traceback.print_exc())
      submitted_assessment["instructor_id"] = ""
      submitted_assessment["instructor_name"] = "Unassigned"

    submitted_assessment["unit_name"] = le_data.get("name", "")
    submitted_assessment["discipline_name"] = discipline_data.get("name", "")
  submitted_assessment["learner_name"] = \
    get_user_name(learner)
  submitted_assessment["assigned_to"] = \
    get_user_name(assessor)
  if assessment_data.get("max_attempts"):
    submitted_assessment["max_attempts"] = assessment_data.get("max_attempts")
  ## TODO: max_attempts will be added in the assessments in hierarchy which will
  ## be 1 for practice and 3 for final
  elif assessment_data.get("type") in ["practice", "pretest"]:
    submitted_assessment["max_attempts"] = 1
  else:
    submitted_assessment["max_attempts"] = 3
  submitted_assessment["timer_start_time"] = \
    str(submitted_assessment["timer_start_time"])
  return submitted_assessment


def traverse_up(node, level: str, parent_alias: str):
  """This function is to traverse from child to parent
  till a parent with alias `parent_alias` is encountered
  The `node` and `level` define the child from where to start"""
  if level not in ["assessments", "learning_resources"] and \
    node.alias == parent_alias:
    return node
  parent_nodes = node.parent_nodes
  for parent_level in parent_nodes:
    for parent_uuid in parent_nodes[parent_level]:
      parent_node = collection_references[parent_level].find_by_uuid(parent_uuid)
      return traverse_up(parent_node, parent_level, parent_alias)


def traverse_up_uuid(uuid: str, level: str, parent_alias: str):
  """This function is to traverse from child to parent
  till a parent with alias `parent_alias` is encountered
  The `uuid` and `level` define the child from where to start"""
  node = collection_references[level].find_by_uuid(uuid)
  if level not in ["assessments", "learning_resources"] and \
    node.alias == parent_alias:
    return node
  parent_nodes = node.parent_nodes
  for parent_level in parent_nodes:
    for parent_uuid in parent_nodes[parent_level]:
      return traverse_up_uuid(parent_uuid, parent_level, parent_alias)
