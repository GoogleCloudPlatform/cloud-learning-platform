""" Submitted Assessment endpoints """
import traceback
from datetime import datetime
from requests.exceptions import ConnectTimeout
from fastapi import APIRouter, Query, Request
from typing import List, Union, Optional
from typing_extensions import Literal
from common.models import (SubmittedAssessment, Assessment, Learner, User,
                          LearningExperience, Rubric)
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 PreconditionFailedError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, ConnectionTimeout,
                                          PreconditionFailed)
from common.utils.logging_handler import Logger
from common.utils.assessor_handler import (
    traverse_down,
    remove_assessor_for_submitted_assessments,
    replace_assessor_of_submitted_assessments,
    filter_submitted_assessments
)
from services.submitted_assessment import (
    traverse_up,
    traverse_up_uuid,
    submit_assessment,
    get_latest_submission,
    get_all_submission,
    get_submitted_assessment_data,
    instructor_handler,
    staff_to_learner_handler)
from schemas.submitted_assessment_schema import (
    SubmittedAssessmentRequestModel, SubmittedAssessmentResponseModel,
    AllSubmittedAssessmentResponseModel, UpdateSubmittedAssessmentModel,
    DeleteSubmittedAssessment, SubmittedAssessmentUniqueResponseModel,
    SubmittedAssessmentAssessorResponseModel, ManualEvaluationResponseModel,
    AllSubmittedAssessmentAssessorResponseModel, UpdateAssessorIdRequestModel,
    ReplaceAssessorofSubmittedAssessmentsResponseModel)

from schemas.error_schema import (NotFoundErrorResponseModel,
                                  ConnectionTimeoutResponseModel,
                                  PreconditionFailedResponseModel)
from config import ERROR_RESPONSES

router = APIRouter(tags=["Submitted Assessment"], responses=ERROR_RESPONSES)

# pylint: disable = broad-except,redefined-builtin,broad-exception-raised,too-many-function-args


@router.post(
    "/submitted-assessment",
    response_model=SubmittedAssessmentResponseModel,
    responses={
        412: {
            "model": PreconditionFailedResponseModel
        },
        404: {
            "model": NotFoundErrorResponseModel
        },
        408: {
            "model": ConnectionTimeoutResponseModel
        }
    })
def create_submitted_assessment(
    request: Request,
    input_submitted_assessment: SubmittedAssessmentRequestModel):
  """
    The create_submitted_assessment endpoint will add the
    submitted_assessment to firestore.

    ### Args:
    - input_submitted_assessment (SubmittedAssessmentSchema): input
    submitted_assessment to be inserted

    ### Raises:
    - ResourceNotFoundException: If the assessment  or learner does not exist
    - PreconditionFailed: If max_attempt is exceeded
    - ConnectTimeout: If external service call fails
    - Exception: 500 Internal Server Error if something went wrong

    ### Returns:
    - SubmittedAssessmentResponseModel: SubmittedAssessment object
  """
  try:
    submitted_assessment_dict = {**input_submitted_assessment.dict()}

    submitted_assessment_fields = submit_assessment(submitted_assessment_dict,
                                                    request)

    return {
        "success": True,
        "message": "Successfully created the submitted assessment.",
        "data": submitted_assessment_fields
    }

  except ConnectTimeout as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ConnectionTimeout(str(e)) from e
  except PreconditionFailedError as e:
    Logger.error(e)
    Logger.info(traceback.print_exc())
    raise PreconditionFailed(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
    "/submitted-assessment/{uuid}/learner/all-submissions",
    response_model=AllSubmittedAssessmentAssessorResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_all_submitted_assessment(req: Request, uuid: str,
                                  skip: int = Query(0, ge=0, le=2000),
                                  limit: int = Query(10, ge=1, le=100)):
  """
    The get_all_submitted_assessment endpoint will fetch all the
    submitted_assessment from firestore for the learner and the assessment of
    the given submitted_assessment uuid

    ### Args:
    - uuid (str): Unique identifier for submitted_assessment
    - skip (int): Number of objects to be skipped
    - limit (int): Size of submitted assessment array to be returned

    ### Raises:
    - ResourceNotFoundException: If the learner_id/assessment_id does not exist
    - Exception: 500 Internal Server Error if something went wrong

    ### Returns:
    - AllSubmittedAssessmentAssessorResponseModel: List of SubmittedAssessment
  """
  try:
    header = {"Authorization": req.headers.get("authorization")}
    all_submissions = get_all_submission(uuid, skip, limit, header)
    count = 10000
    response = {"records": all_submissions, "total_count": count}
    return {
        "success": True,
        "message": "Successfully fetched the submitted assessments.",
        "data": response
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e

  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e

@router.get(
    "/submitted-assessment/{uuid}/learner/latest-submission",
    response_model=SubmittedAssessmentAssessorResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_latest_submitted_assessment(req: Request, uuid: str):
  """
    The get_latest_submitted_assessment endpoint will fetch the latest
    submitted_assessment from firestore for the learner and the assessment of
    the given submitted_assessment uuid.

    ### Args:
    - uuid (str): Unique identifier for submitted_assessment

    ### Raises:
    - ResourceNotFoundException: If the submitted_assessment does not exist
    - Exception: 500 Internal Server Error if something went wrong

    ### Returns:
    - SubmittedAssessmentAssessorResponseModel: SubmittedAssessment object
  """
  try:
    header = {"Authorization": req.headers.get("authorization")}
    submitted_assessment = SubmittedAssessment.find_by_uuid(uuid)
    assessment_id = submitted_assessment.assessment_id
    learner_id = submitted_assessment.learner_id
    latest_submission = get_latest_submission(
        learner_id, assessment_id, True, header)

    return {
        "success": True,
        "message": "Successfully fetched the submitted assessment.",
        "data": latest_submission
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
    "/submitted-assessment/{uuid}",
    response_model=SubmittedAssessmentResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_submitted_assessment(uuid: str):
  """
    The get submitted_assessment endpoint will return the submitted_assessment
    from firestore of which uuid is provided

    ### Args:
    - uuid (str): Unique identifier for submitted_assessment

    ### Raises:
    - ResourceNotFoundException: If the submitted_assessment does not exist
    - Exception: 500 Internal Server Error if something went wrong

    ### Returns:
    - SubmittedAssessmentResponseModel: SubmittedAssessment Object
  """
  try:
    submitted_assessment = SubmittedAssessment.find_by_uuid(uuid)
    submitted_assessment_fields = submitted_assessment.get_fields(
        reformat_datetime=True)
    submitted_assessment_fields["timer_start_time"] = str(
        submitted_assessment_fields["timer_start_time"])

    return {
        "success": True,
        "message": "Successfully fetched the submitted assessment.",
        "data": submitted_assessment_fields
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.put(
    "/submitted-assessment/{uuid}",
    name="Update Submitted Assessment",
    response_model=SubmittedAssessmentResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_assessment_item(
    uuid: str, input_submitted_assessment: UpdateSubmittedAssessmentModel):
  """
    Update a submitted_assessment

    ### Args:
    - input_submitted_assessment (UpdateSubmittedAssessmentModel):
    Required body of submitted_assessment

    ### Raises:
    - ResourceNotFoundException: If the submitted_assessment does not exist
    - Exception: 500 Internal Server Error if something went wrong

    ### Returns:
    - SubmittedAssessmentResponseModel: SubmittedAssessment Object
  """
  try:
    submitted_assessment = SubmittedAssessment.find_by_uuid(uuid)
    submitted_assessment_dict = {**input_submitted_assessment.dict()}
    submitted_assessment_fields = submitted_assessment.get_fields()

    # Update status, pass_status, and result based on submitted_rubrics
    evaluated = False
    if submitted_assessment_fields.get("type") in \
      ["srl", "static_srl", "cognitive_wrapper"] and \
      submitted_assessment_fields.get("is_autogradable", False):
      # Always pass SRL assessments
      pass_status = True
      result = "Pass"
      status = "completed"
      evaluated = True
    else:
      submitted_rubrics = submitted_assessment_dict.get("submitted_rubrics",
                                                        None)
      if submitted_rubrics is not None:
        assessment_id = submitted_assessment.assessment_id
        assessment = Assessment.find_by_uuid(assessment_id)
        if assessment.child_nodes and "rubrics" in assessment.child_nodes:
          # FIXME: Assumption: only one rubric for each assessment
          rubric_id = assessment.child_nodes["rubrics"][0]
          rubric = Rubric.find_by_uuid(rubric_id)
          criteria = rubric.evaluation_criteria
          criteria = {v: k for k, v in criteria.items()}
          if len(submitted_rubrics):
            pass_status = True
            result = "Exemplary"
            for r_criterion in submitted_assessment_dict["submitted_rubrics"]:
              if criteria[r_criterion["result"]] > criteria[result]:
                result = r_criterion["result"]
            if criteria[result] > criteria["Proficient"]:
              pass_status = False
              status = "evaluated"
            else:
              status = "completed"
            evaluated = True
    if evaluated:
      submitted_assessment_dict["status"] = status
      submitted_assessment_dict["result"] = result
      submitted_assessment_dict["pass_status"] = pass_status

    for key, value in submitted_assessment_dict.items():
      if key == "comments" and value is not None:
        if value.get("created_time") is None:
          value["created_time"] = str(datetime.now())
        if submitted_assessment_fields.get("comments"):
          value = [value] + submitted_assessment_fields.get(
              "comments", [])
        else:
          value = [value]
      submitted_assessment_fields[key] = value
    for key, value in submitted_assessment_fields.items():
      setattr(submitted_assessment, key, value)

    submitted_assessment.update()

    submitted_assessment_fields = submitted_assessment.get_fields(
        reformat_datetime=True)
    submitted_assessment_fields["timer_start_time"] = str(
        submitted_assessment_fields["timer_start_time"])

    return {
        "success": True,
        "message": "Successfully updated the submitted assessment.",
        "data": submitted_assessment_fields
    }
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.delete(
    "/submitted-assessment/{uuid}",
    response_model=DeleteSubmittedAssessment,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_submitted_assessment(uuid: str):
  """
    Delete a submitted_assessment from firestore

    ### Args:
    - uuid (str): Unique id of the submitted_assessment

    ### Raises:
    - ResourceNotFoundException: If the submitted_assessment does not exist
    - Exception: 500 Internal Server Error if something went wrong

    ### Returns:
    - JSON: Success/Fail Message
  """
  try:
    SubmittedAssessment.delete_by_uuid(uuid)

    return {
        "success": True,
        "message": "Successfully deleted the submitted assessment."
    }
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
    "/learner/{learner_id}/submitted-assessments",
    name="Get all Submitted Assessments for Learner",
    response_model=AllSubmittedAssessmentResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_all_submitted_assessment_for_learner(req: Request, learner_id: str,
                                        assessment_id: Optional[str] = None,
                                        skip: int = Query(0, ge=0, le=2000),
                                        limit: int = Query(10, ge=1, le=100)):
  """
    The get_all_submitted_assessment_for_learner endpoint will fetch all the
    submitted_assessments for a learner from firestore.

    ### Args:
    - learner_id (str): uuid of learner
    - assessment_id (str): optional uuid of the assessment
    - skip (int): Number of objects to be skipped
    - limit (int): Size of array to be returned

    ### Raises:
    - ResourceNotFoundException: If the learner_id does not exist
    - Exception: 500 Internal Server Error if something went wrong

    ### Returns:
    - SubmittedAssessmentResponseModel: SubmittedAssessment object
  """
  try:
    # Check to validate if Learner with given ID exists or not
    header = {"Authorization": req.headers.get("authorization")}
    _ = Learner.find_by_uuid(learner_id)
    collection_manager = SubmittedAssessment.collection
    collection_manager = collection_manager.filter("is_deleted", "==",
                                                   False)
    collection_manager = collection_manager.filter("learner_id", "==",
                                                   learner_id)
    if assessment_id:
      collection_manager = collection_manager.filter("assessment_id",
                                                     "==", assessment_id)
    submitted_assessments = collection_manager.order("-created_time").offset(
        skip).fetch(limit)
    if submitted_assessments:
      submitted_assessments = [
          get_submitted_assessment_data(submitted_assessment, True, header)
          for submitted_assessment in submitted_assessments
      ]
    for assessment in submitted_assessments:
      assessment["timer_start_time"] = str(assessment["timer_start_time"])
    count = 10000
    response = {"records": submitted_assessments, "total_count": count}
    return {
        "success": True,
        "message": "Successfully fetched the submitted assessments",
        "data": response
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/submitted-assessments",
    response_model=AllSubmittedAssessmentAssessorResponseModel,
    name="Get filtered/searched Submitted Assessments")
def get_filtered_submitted_assessments(
    req: Request,
    sort_by: Optional[Literal["learner_name", "unit_name", "result",
                              "attempt_no",
                              "timer_start_time"]] = "timer_start_time",
    sort_order: Optional[Literal["ascending", "descending"]] = "ascending",
    name: Optional[str] = None,
    assessor_id: Optional[str] = None,
    is_autogradable: Union[bool, None] = Query(default=None),
    discipline_name: Union[List[str], None] = Query(default=None),
    unit_name: Union[List[str], None] = Query(default=None),
    status: Union[List[str], None] = Query(default=None),
    type: Union[List[str], None] = Query(default=None),
    result: Union[List[str], None] = Query(default=None),
    is_flagged: Union[bool, None] = Query(default=None),
    skip: int = Query(0, ge=0, le=2000),
    limit: int = Query(10, ge=1, le=100)):
  """
    The get filtered submitted assessments endpoint will return an array
    of submitted assessments from firestore

    ### Args:
    - sort_by (str): sort submitted assessment based on this parameter value
    - sort_order (str): ascending or descending sort
    - name (str): search submitted assessment based on assessment name keyword
    - assessor_id (str): uuid of assessor
    - is_autogradable (bool): to return autogradable or human gradable or both
      type of assessments
    - discipline_name (list): Pathway disciplines to filter submitted assessment
    - unit_name (list): Pathway units to filter submitted assessments on
    - type (list): type to filter submitted assessments on
    - status (list): status of submitted assessment to filter on
    - result (list): result to filter submitted assessments on
    - is_flagged (bool): return flagged assessments or not or both
    - skip (int): Number of objects to be skipped
    - limit (int): Size of array to be returned

    ### Raises:
    - ValidationError: If filters are incorrect
    - Exception: 500 Internal Server Error if something went wrong

    ### Returns:
    - AllSubmittedAssessmentAssessorResponseModel: List of SubmittedAssessments
  """
  try:
    header = {"Authorization": req.headers.get("authorization")}
    collection_manager = SubmittedAssessment.collection
    collection_manager = collection_manager.filter("is_deleted", "==", False)

    in_query_used = False
    status_filter_applied = True
    type_filter_applied = True
    learner_filter_applied = True

    # assessor_id is a string because an assessor can either view only the
    # submissions assigned to him or all the submissions
    if assessor_id:
      assessor = User.find_by_user_id(assessor_id)
      if assessor.user_type == "assessor":
        collection_manager = collection_manager.filter("assessor_id", "==",
                                                     assessor_id)
      elif assessor.user_type in ["coach", "instructor"]:
        ## TODO: Store user_id of the learner instead of user_id
        learner_ids = staff_to_learner_handler(header, assessor_id,
                                               assessor.user_type)
        if not learner_ids:
          ## FIXME: return statement should be executed in the end only
          return {
            "success": True,
            "message": "Successfully fetched the submitted assessments.",
            "data": []
          }
        elif len(learner_ids)<=30:
          in_query_used = True
          collection_manager = collection_manager.filter("learner_id", "in",
                                                        learner_ids)
        else:
          learner_filter_applied = False

      else:
        raise ResourceNotFoundException(f"User of type {assessor.user_type} "\
          "not found.")

    if is_flagged is not None:
      collection_manager = collection_manager.filter("is_flagged", "==",
                                                     is_flagged)

    if is_autogradable is not None:
      collection_manager = collection_manager.filter("is_autogradable", "==",
                                                     is_autogradable)

    if result:
      if len(result) == 1:
        collection_manager = collection_manager.filter("result", "==",
                                                       result[0])
      else:
        in_query_used = True
        collection_manager = collection_manager.filter("result", "in", result)

    if status:
      if len(status) == 1:
        collection_manager = collection_manager.filter("status", "==",
                                                       status[0])
      elif not in_query_used:
        in_query_used = True
        collection_manager = collection_manager.filter("status", "in", status)
      else:
        status_filter_applied = False

    if type:
      if len(type) == 1:
        collection_manager = collection_manager.filter("type", "==", type[0])
      elif not in_query_used:
        in_query_used = True
        collection_manager = collection_manager.filter("type", "in", type)
      else:
        type_filter_applied = False

    # check if the collection can be directly sorted if the field
    # to sort on is a field in the data model of SubmittedAssessment
    if sort_by in ["result", "attempt_no", "timer_start_time"]:
      sorted_collection = True
      if sort_order == "descending":
        sort_by = "-" + sort_by
      submitted_assessments = collection_manager.order(sort_by).fetch()
    else:
      sorted_collection = False
      submitted_assessments = collection_manager.fetch()

    filtered_submitted_assessments = []
    le_map = {}
    discipline_map = {}
    instructor_map = {}
    assessment_map = {}
    assessor_map = {}
    # iterate through all the submitted assessments
    for submitted_assessment in submitted_assessments:
      assessment_id = submitted_assessment.assessment_id
      # if the submitted assessments are already sorted, then we need to fetch
      # only limit number of values
      if not limit:
        break
      # if status filter is not applied above and the submitted_assessment
      # status does not lie in the status query, then do not add this submission
      if not status_filter_applied and \
          submitted_assessment.status not in status:
        continue
      # if type filter is not applied above and the submitted_assessment
      # type does not lie in the type query, then do not add this submission
      elif not type_filter_applied and \
          submitted_assessment.type not in type:
        continue
      # if filter by learner is not applied above and the submitted_assessment
      # learner_id does not lie in the list of learner_ids query, then do not
      # add this submission
      elif not learner_filter_applied and \
          submitted_assessment.learner_id not in learner_ids:
        continue
      if assessment_id in assessment_map:
        assessment_node = assessment_map[assessment_id]
      else:
        assessment_node = Assessment.find_by_uuid(assessment_id)
        assessment_map[assessment_id] = assessment_node

      assessment_data = assessment_node.get_fields(reformat_datetime=True)
      assessment_name = assessment_data["name"]

      # 1. If search query (name) is None, or
      # 2. if it is not None, then it exists in assessment name
      # Then the submitted assessment document can be added
      keyword_exists = not name or \
                  (name and name.lower() in assessment_name.lower())
      if keyword_exists:
        try:
          if assessment_id in le_map:
            le_data = le_map[assessment_id]
          else:
            le_node = traverse_up_uuid(assessment_id, "assessments",
              "learning_experience")
            le_data = le_node.get_fields()
            le_map[assessment_id] = {
              "name": le_data.get("name", ""),
              "uuid": le_data.get("uuid")
            }
        except Exception as e:
          Logger.error(e)
          Logger.error(traceback.print_exc())
          Logger.info("Passing Empty Dict to Get Success Response")
          le_data = {}

        try:
          le_id = le_data.get("uuid")
          if le_id in discipline_map:
            discipline_data = discipline_map[le_id]
          else:
            discipline_data = traverse_up_uuid(le_id, "learning_experiences",
                "discipline").get_fields()
            discipline_map[le_id] = {
              "name": discipline_data.get("name", ""),
              "uuid": discipline_data.get("uuid")
            }
        except Exception as e:
          Logger.error(e)
          Logger.error(traceback.print_exc())
          Logger.info("Passing Empty Dict to Get Success Response")
          discipline_data = {}

        # 1a. If unit_name query filter is None, OR
        # 1b. if it is not None, then the unit pathway's name lies in any
        #    unit_name, AND
        # 2a. If discipline_name query filter is None, OR
        # 2b. if it is not None, then the pathway discipline's name lies in
        #    any discipline_name
        # Then the submitted assessment document can be added
        if (not unit_name or le_data.get("name", "") in unit_name) and (not
        discipline_name or discipline_data.get("name", "") in discipline_name):
          # 1. if the submitted assessment collection is already sorted
          # 2. if the number of assessments to be skipped is not yet complete
          # Then skip this submitted assessment and reduce skip by 1
          # else add the submitted assessment
          if sorted_collection and skip:
            skip -= 1
          else:
            submitted_assessment_data = get_submitted_assessment_data(
                submitted_assessment, False, None, assessment_node,
                assessor_map)
            submitted_assessment_data["unit_name"] = le_data.get("name", "")
            submitted_assessment_data["discipline_name"] = discipline_data.get(
              "name", "")
            # get instructor data
            try:
              discipline_id = discipline_data.get("uuid")
              if discipline_id in instructor_map:
                instructor_data = instructor_map[discipline_id]
              elif assessor and assessor.user_type == "instructor":
                instructor_id = assessor.user_id
                instructor_data = User.find_by_user_id(
                  instructor_id).get_fields()
                instructor_map[discipline_id] = {
                  "first_name": instructor_data.get("first_name", ""),
                  "last_name": instructor_data.get("last_name", ""),
                  "user_id": instructor_data.get("user_id")
                }
              else:
                instructor_id = instructor_handler(
                    header, discipline_data["uuid"])
                instructor_data = User.find_by_user_id(
                  instructor_id).get_fields()
                instructor_map[discipline_id] = {
                  "first_name": instructor_data.get("first_name", ""),
                  "last_name": instructor_data.get("last_name", ""),
                  "user_id": instructor_data.get("user_id")
                }
              submitted_assessment_data["instructor_id"] = instructor_data.get(
                "user_id", "")
              submitted_assessment_data["instructor_name"] = \
                (instructor_data.get("first_name", "") + " " +
                  instructor_data.get("last_name", "")).lstrip()
            except Exception as e:
              Logger.error(e)
              Logger.error(traceback.print_exc())
              submitted_assessment_data["instructor_id"] = ""
              submitted_assessment_data["instructor_name"] = "Unassigned"
            filtered_submitted_assessments.append(submitted_assessment_data)
            if sorted_collection:
              limit -= 1

    # if the submitted assessments are not sorted, then sort it and return the
    # only those submissions defined by skip and limit
    if not sorted_collection:
      if sort_by == "ascending":
        filtered_submitted_assessments = sorted(
            filtered_submitted_assessments, key=lambda i: i[sort_by])
      else:
        filtered_submitted_assessments = sorted(
            filtered_submitted_assessments,
            key=lambda i: i[sort_by],
            reverse=True)
      filtered_submitted_assessments = \
              filtered_submitted_assessments[skip:skip+limit]
    count = 10000
    response = {"records": filtered_submitted_assessments, "total_count": count}
    return {
        "success": True,
        "message": "Successfully fetched the submitted assessments.",
        "data": response
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e

  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e), data=e.data) from e

  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
    "/submitted-assessments/unique",
    response_model=SubmittedAssessmentUniqueResponseModel,
    name="Get Unique Values for Submitted Assessment Filters")
def get_unique_values_submitted_assessments(
      assessor_id: Optional[str] = None,
      is_autogradable: Union[bool, None] = Query(default=None),
      status: Union[List[str], None] = Query(default=None)
):
  """
    The get_unique_values_submitted_assessments endpoint will return an array
    of unique values for competency, type and result

    ### Args:
    - assessor_id (str): filter submitted assessments based on assessor id
    - is_autogradable (bool): to return autogradable or human gradable or both
      type of assessments
    - status (list): status of submitted assessment to filter on

    ### Raises:
    - ResourceNotFoundException: If the assessor does not exist
    - Exception: 500 Internal Server Error if something went wrong

    ### Returns:
    - SubmittedAssessmentUniqueResponseModel: Dictionary of unique values of
      required SubmittedAssessment fields.
  """
  try:

    collection_manager = SubmittedAssessment.collection
    if assessor_id:
      user = User.find_by_user_id(assessor_id)
      if user.user_type != "assessor":
        raise ResourceNotFoundException(
            f"Assessor with uuid {assessor_id} not found")
      collection_manager = collection_manager.filter("assessor_id", "==",
                                                     assessor_id)

    if is_autogradable:
      collection_manager.filter("is_autogradable", "==", is_autogradable)

    if status:
      if len(status) == 1:
        collection_manager = collection_manager.filter("status", "==",
                                                       status[0])
      else:
        collection_manager = collection_manager.filter("status", "in", status)

    submitted_assessments = collection_manager.order("timer_start_time").fetch()
    unique_discipline_names = set()
    unique_unit_names = set()
    unique_types = set()
    unique_results = set()

    for submitted_assessment in submitted_assessments:
      # adding unique type
      if submitted_assessment.type:
        unique_types.add(submitted_assessment.type)
      # adding unique result
      if submitted_assessment.result:
        unique_results.add(submitted_assessment.result)
      assessment_node = Assessment.find_by_uuid(
          submitted_assessment.assessment_id)

      try:
        le_node = traverse_up(assessment_node, "assessments",
          "learning_experience")
        le_data = le_node.get_fields(reformat_datetime=True)
        unique_unit_names.add(le_data.get("name", ""))
        discipline_data = traverse_up(le_node, "learning_experiences",
            "discipline").get_fields(reformat_datetime=True)
        unique_discipline_names.add(discipline_data.get("name", ""))
      except Exception as e:
        Logger.error(e)
        Logger.error(traceback.print_exc())
        pass

    unique_discipline_names = sorted(list(unique_discipline_names))
    unique_unit_names = sorted(list(unique_unit_names))
    unique_types = sorted(list(unique_types))
    unique_results = sorted(list(unique_results))

    return {
      "success": True,
      "message": "Successfully fetched the unique " + \
        "values for submitted assessments.",
      "data": {
          "discipline_names": unique_discipline_names,
          "unit_names": unique_unit_names,
          "types": unique_types,
          "results": unique_results
        }
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e

  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e), data=e.data) from e

  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
  "/learner/{learner_id}/learning-experience/{le_id}/submitted-assessments/"
  "manual-evaluation",
  name="Get Human Graded Assessments of an Unit for a Learner",
  response_model=ManualEvaluationResponseModel,
  responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_all_manual_evaluation_submitted_assessments_for_learner(
    req: Request,
    learner_id: str,
    le_id: str,
    skip: int = Query(0, ge=0, le=2000),
    limit: int = Query(10, ge=1, le=100)):
  """
    This endpoint will fetch all the submitted_assessments of a learner for a
    given unit from firestore, that can get feedback from the Assessor.

    ### Args:
    - learner_id : uuid of learner
    - le_id: uuid of learning_experience (unit)
    - skip (int): Number of objects to be skipped. Default 0.
    - limit (int): Size of array to be returned. Default 10.

    ### Raises:
    - ResourceNotFoundException: If the learner_id or le_id does not exist
    - Exception: 500 Internal Server Error if something went wrong

    ### Returns:
    - SubmittedAssessmentResponseModel: SubmittedAssessment object
  """
  try:
    header = {"Authorization": req.headers.get("authorization")}
    # Check to validate if Learner and learning_experience
    # with given ID exists or not
    Learner.find_by_uuid(learner_id)
    LearningExperience.find_by_uuid(le_id)
    assessor_map = {}

    collection_manager = SubmittedAssessment.collection

    collection_manager = collection_manager.filter(
      "learner_id", "==", learner_id)

    collection_manager = collection_manager.filter(
      "is_autogradable", "==", False)

    submitted_assessments = collection_manager.order("-created_time").offset(
        skip).fetch(limit)

    response = []
    for submitted_assessment in submitted_assessments:
      assessment_node = Assessment.find_by_uuid(
        submitted_assessment.assessment_id)
      try:
        lo_node = traverse_up(assessment_node, "assessments",
          "module")
        le_node = traverse_up(lo_node, "learning_objects",
          "learning_experience")
        le_data = le_node.get_fields()
      except Exception as e:
        Logger.error(e)
        Logger.error(traceback.print_exc())
        Logger.info("Passing Empty Dict to Get Success Response")
        le_data = {}

      if le_id == le_data.get("uuid", ""):
        try:
          discipline_data = traverse_up(le_node, "learning_experiences",
            "discipline").get_fields()
        except Exception as e:
          Logger.error(e)
          Logger.error(traceback.print_exc())
          Logger.info("Passing Empty Dict to Get Success Response")
          discipline_data = {}

        submitted_assessment_data = get_submitted_assessment_data(
            submitted_assessment, False, None, assessment_node,
            assessor_map)
        submitted_assessment_data["unit_name"] = le_data.get("name", "")
        submitted_assessment_data["discipline_name"] = discipline_data.get(
          "name", "")
        if discipline_data:
          instructor_id = instructor_handler(header, discipline_data["uuid"])
          instructor_data = User.find_by_user_id(instructor_id).get_fields()
          submitted_assessment_data["instructor_id"] = instructor_data.get(
            "user_id", "")
          submitted_assessment_data["instructor_name"] = \
            (instructor_data.get("first_name", "") + " " +
              instructor_data.get("last_name", "")).lstrip()
        else:
          submitted_assessment_data["instructor_id"] = ""
          submitted_assessment_data["instructor_name"] = "Unassigned"
        found = False
        for item in response:
          if item.get("learning_object", "") == lo_node.uuid:
            found = True
            item["submitted_assessments"].append(submitted_assessment_data)
        if not found:
          response.append({
            "learning_object": lo_node.uuid,
            "learning_object_name": lo_node.name,
            "submitted_assessments": [submitted_assessment_data]
          })
    count = 10000
    final_response = {"records": response, "total_count": count}
    return {
        "success": True,
        "message": "Successfully fetched the submitted assessments",
        "data": final_response
    }

  except ResourceNotFoundException as e:
    print(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    print(traceback.print_exc())
    raise InternalServerError(str(e)) from e

@router.put(
  "/discipline/{discipline_id}/submitted-assessments"\
  "/update-assessor",
  include_in_schema=False,
  response_model=ReplaceAssessorofSubmittedAssessmentsResponseModel,
  responses={404: {
      "model": NotFoundErrorResponseModel
  }})
def update_assessor_of_submitted_assessments_of_a_discipline(
    req: Request, discipline_id: str,
    input_assessor: Optional[UpdateAssessorIdRequestModel] = None):
  """
    Unassign and assign another assessor for all non-evaluated
    submitted assessments related to a discipline

    ### Args:
    - discipline_id (str): Unique identifier of a curriculum_pathway
      of alias discipline
    - assessor_id (str): Unique identifier of user(assessor)

    ### Raises:
    - ResourceNotFoundException: If the discipline_id does not exist
    - Exception: 500 Internal Server Error if something went wrong

    ### Returns:
    - JSON: Success/Fail Message
  """
  try:
    assessor_id = None
    if input_assessor:
      input_assessor= {**input_assessor.dict()}
      assessor_id = input_assessor.get("assessor_id")
    assessment_ids = []
    assessment_ids = traverse_down(
        discipline_id, "curriculum_pathways", "assessments",assessment_ids)
    assessment_ids = list(set(assessment_ids))
    response_msg= "No assessments found for discipline "\
          f"with uuid {discipline_id}"
    if assessment_ids:
      submitted_assessments = filter_submitted_assessments(
                                          assessment_ids, assessor_id)
      if assessor_id:
        response_msg = f"Successfully replaced assessor {assessor_id} "\
          f"for submitted assessments of discipline with uuid {discipline_id}."
        replace_assessor_of_submitted_assessments(discipline_id,req,
                    submitted_assessments,assessment_ids,assessor_id)
      else:
        remove_assessor_for_submitted_assessments(submitted_assessments)
        response_msg = "Successfully unassigned assessor for all evaluation "\
        f"pending submitted assessments of discipline with uuid {discipline_id}"

    return {
        "success": True,
        "message": response_msg
    }

  except ResourceNotFoundException as e:
    print(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e

  except Exception as e:
    print(traceback.print_exc())
    raise InternalServerError(str(e)) from e
