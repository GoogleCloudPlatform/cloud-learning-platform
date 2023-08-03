""" Learner endpoints """

import re
import traceback

from typing import Optional
from typing_extensions import Literal
from fastapi import APIRouter, UploadFile, File, Query
from common.models import (Learner, User, Staff, AssociationGroup,
                           CurriculumPathway)
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 ConflictError, PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, Conflict,
                                          PayloadTooLarge)
from common.utils.logging_handler import Logger
from common.utils.sorting_logic import collection_sorting
from schemas.learner_schema import (
    LearnerModel, GetLearnerResponseModel, PostLearnerResponseModel,
    UpdateLearnerResponseModel, UpdateLearnerModel, DeleteLearner,
    AllLearnersResponseModel, LearnerSearchResponseModel,
    LearnerImportJsonResponse, BasicLearnerModel, CoachesResponseModel,
    InstructorResponseModel, GetLearnerPathwayIdResponse,
    GetInstructorsResponseModel)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from services.json_import import json_import
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES

# pylint: disable = broad-exception-raised

router = APIRouter(tags=["Learner"], responses=ERROR_RESPONSES)


@router.get("/learner/search", response_model=LearnerSearchResponseModel)
def search_learner(first_name: Optional[str] = None,
                   email_address: Optional[str] = None):
  """Search for learners based on the learner firstname and email address

  Args:
      first_name(str): First name of the learner. Defaults to None.
      email_address(str): Email address of the learner. Defaults to None.

  Returns:
      LearnerSearchResponseModel: List of learner objects
  """
  result = []
  try:
    if first_name:
      learner_node_items = Learner.find_by_first_name(first_name)
    elif email_address:
      pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
      email_match = re.compile(pattern=pattern)

      if not email_match.fullmatch(email_address):
        raise ValidationError(f"Invalid email ID format: {email_address}")

      learner_node_items = Learner.find_by_email_address(email_address)
    else:
      raise ValidationError("Missing or invalid request parameters")

    for learner_node_item in learner_node_items:
      learner_node_dict = learner_node_item.get_fields(reformat_datetime=True)
      result.append(learner_node_dict)

    return {
      "success": True,
      "message": "Successfully fetched the learners",
      "data": result
    }
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
  "/learners",
  response_model=AllLearnersResponseModel,
  name="Get all Learners")
def get_learners(skip: int = Query(0, ge=0, le=2000),
                 limit: int = Query(10, ge=1, le=100),
                 fetch_archive: Optional[bool] = None,
                 sort_by: Optional[Literal["first_name", "last_name",
                 "created_time"]] = "created_time",
                 sort_order: Optional[Literal["ascending", "descending"]] =
                 "descending"):
  """The get learners endpoint will return an array learners from firestore

  Args:
      skip (int): Number of objects to be skipped
      limit (int): Size of a learner array to be returned
      sort_by (str): Data Model Fields name
      sort_order (str): ascending/descending
      fetch_archive (bool): to fetch archive

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      AllLearnersResponseModel: Array of Learner Object
  """
  try:
    collection_manager = Learner.collection.filter("is_deleted", "==", False)
    if fetch_archive is not None:
      collection_manager = collection_manager.filter("is_archived", "==",
                                                     fetch_archive)

    learners = collection_sorting(collection_manager=collection_manager,
                                  sort_by=sort_by, sort_order=sort_order,
                                  skip=skip, limit=limit)

    learners = [i.get_fields(reformat_datetime=True) for i in learners]
    count = 10000
    response = {"records": learners, "total_count": count}
    return {
        "success": True,
        "message": "Data fetched successfully",
        "data": response
    }
  except ValidationError as e:
    Logger.info(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.info(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
  "/learner/{uuid}",
  response_model=GetLearnerResponseModel,
  responses={404: {
    "model": NotFoundErrorResponseModel
  }})
def get_learner(uuid: str):
  """The get learner endpoint will return the learner from
  firestore of which uuid is provided

  Args:
      uuid (str): Unique identifier for learner

  Raises:
      ResourceNotFoundException: If the learner does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      LearnerResponseModel: Learner Object
  """
  try:
    learner = Learner.find_by_uuid(uuid)
    learner_fields = learner.get_fields(reformat_datetime=True)
    return {
      "success": True,
      "message": "Successfully fetched the learner",
      "data": learner_fields
    }
  except ResourceNotFoundException as e:
    Logger.info(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.info(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
  "/learner",
  response_model=PostLearnerResponseModel,
  responses={404: {
    "model": NotFoundErrorResponseModel
  }})
def create_learner(input_learner: LearnerModel):
  """The created learner endpoint will add the given learner in request body to
  the firestore

  Args:
      input_learner (LearnerModel): input learner to be inserted

  Raises:
      ResourceNotFoundException: If the learner does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      PostLearnerResponseModel: Learner Object
  """
  try:
    new_learner = Learner()
    input_learner_dict = {**input_learner.dict()}
    learner = Learner.collection.filter("email_address", "==",
      input_learner_dict.get("email_address", "").lower()).filter(
      "is_deleted", "==", False).get()

    # Checking if a learner document already exists with the same email id
    if learner is not None:
      raise ConflictError(
          "Learner with the given email address {} already exists".format(
              input_learner_dict.get("email_address", "").lower()))

    # Checking if the learner email id and backup email id are the same
    if input_learner_dict.get("email_address",
                              "").lower() == input_learner_dict.get(
      "backup_email_address", "").lower():
      raise ValidationError(
        "Primary email address and backup email address cannot be the same.")

    new_learner = new_learner.from_dict(input_learner_dict)
    new_learner.uuid = ""

    new_learner.save()
    new_learner.uuid = new_learner.id
    new_learner.update()
    learner_fields = new_learner.get_fields(reformat_datetime=True)
    return {
      "success": True,
      "message": "Successfully created the learner",
      "data": learner_fields
    }
  except ResourceNotFoundException as e:
    Logger.info(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ConflictError as e:
    Logger.info(traceback.print_exc())
    raise Conflict(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.put(
  "/learner/{uuid}",
  response_model=UpdateLearnerResponseModel,
  responses={404: {
    "model": NotFoundErrorResponseModel
  }})
def update_learner(uuid: str, input_learner: UpdateLearnerModel):
  """Update a learner with the uuid passed in the request body

  Args:
      uuid (str): Unique identifier for learner
      input_learner (UpdateLearnerModel): Required body of the learner

  Raises:
      ResourceNotFoundException: If the learner does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      UpdateLearnerResponseModel: Learner Object
  """
  try:
    existing_learner = Learner.find_by_uuid(uuid)
    input_learner_dict = {**input_learner.dict(exclude_unset=True)}

    archive = input_learner_dict.get("is_archived")
    if archive is not None:
      Learner.archive_by_uuid(uuid, archive=archive)

    learner_fields = existing_learner.get_fields()

    # Check if the existing backup email and updated primary email are the same
    # pylint: disable=C0301
    if (input_learner_dict.get("email_address", "").lower() ==
        learner_fields["backup_email_address"] and
        learner_fields["backup_email_address"]) or \
      input_learner_dict.get("backup_email_address", "").lower() == \
      learner_fields["email_address"]:
      raise ValidationError(
        "Primary email address and backup email address cannot be the same.")

    if input_learner_dict.get("email_address") and \
      input_learner_dict.get("backup_email_address"):
      if input_learner_dict["email_address"] == \
        input_learner_dict["backup_email_address"]:
        raise ValidationError(
          "Primary email address and backup email address cannot be the same.")

    for key, value in input_learner_dict.items():
      if value is not None:
        learner_fields[key] = value
    for key, value in learner_fields.items():
      setattr(existing_learner, key, value)
    existing_learner.update()
    learner_fields = existing_learner.get_fields(reformat_datetime=True)

    return {
      "success": True,
      "message": "Successfully updated the learner",
      "data": learner_fields
    }
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.info(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.delete(
  "/learner/{uuid}",
  response_model=DeleteLearner,
  responses={404: {
    "model": NotFoundErrorResponseModel
  }})
def delete_learner(uuid: str):
  """Delete a learner with the given uuid from firestore

  Args:
      uuid (str): Unique id of the learner

  Raises:
      ResourceNotFoundException: If the learner does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      JSON: Success/Fail Message
  """
  try:
    Learner.delete_by_uuid(uuid)
    return {"success": True, "message": "Successfully deleted the learner"}
  except ResourceNotFoundException as e:
    Logger.info(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.info(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
  "/learner/import/json",
  response_model=LearnerImportJsonResponse,
  name="Import Learners from JSON file",
  responses={413: {
    "model": PayloadTooLargeResponseModel
  }})
async def import_learners(json_file: UploadFile = File(...)):
  """Create learners from json file

  Args:
    json_file (UploadFile): Upload json file consisting of learners.
    json_schema should match LearnerModel

  Raises:
    Exception: 500 Internal Server Error if something fails

  Returns:
      LearnerImportJsonResponse: Array of uuid's
  """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
        f"File size is too large: {json_file.filename}")
    await json_file.seek(0)
    final_output = json_import(
      json_file=json_file,
      json_schema=BasicLearnerModel,
      model_obj=Learner,
      object_name="learners")
    return final_output
  except PayloadTooLargeError as e:
    Logger.info(traceback.print_exc())
    raise PayloadTooLarge(str(e)) from e
  except ValidationError as e:
    Logger.info(traceback.print_exc())
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    Logger.info(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
  "/learner/{learner_id}/curriculum-pathway/"
  "{curriculum_pathway_id}/instructor",
  response_model=InstructorResponseModel)
def get_instructor_details(learner_id: str, curriculum_pathway_id: str):
  """Function to fetch Instructor Details for a given learner_id and
  curriculum_pathway_id corresponding to discipline.
  The details will be fetched from LearnerAssociationGroup by first
  identifying and fetching the LearnerAssociationGroup details where
  the Learner is associated. From the AssociationGroup, identify and fetch
  details of the Instructor which are mapped to the given curriculum_pathway_id

  ### Args:
      learner_id (str): ID of the Learner
      curriculum_pathway_id (str): ID of the Pathway with alias as discipline

  ### Returns:
      instructor_id: InstructorResponseModel
  """
  try:

    # TODO: rather then using the learner_id
    # we need to use user_id
    # Validation if Learner Exists
    Learner.find_by_uuid(learner_id)
    instructors_learner_group = []
    # Validation if User of the given Learner Exists
    user_learner = User.find_by_user_type_ref(learner_id)

    # Validation if Pathway Exists
    pathway = CurriculumPathway.find_by_uuid(curriculum_pathway_id)

    if pathway.alias != "discipline":
      raise ValidationError(
        f"Pathway with {curriculum_pathway_id} has alias as {pathway.alias}"
        " instead of discipline")

    learner_association_groups = AssociationGroup.collection.filter(
      "association_type", "==", "learner").order("-created_time").fetch()

    learner_group = None
    for learner_association_group in learner_association_groups:
      if any(user_dict["user"] == user_learner.user_id
             for user_dict in learner_association_group.users):
        learner_group = learner_association_group
        break

    if not learner_group:
      raise ValidationError(
        f"Learner with User ID {user_learner.id} "
        "not found in any Association Groups"
      )

    if learner_group.associations:
      instructors_learner_group = learner_group.associations.get(
        "instructors", [])

    instructor_id = None
    for instructor in instructors_learner_group:
      if instructor["curriculum_pathway_id"] == curriculum_pathway_id and \
        instructor["status"] == "active":
        instructor_id = instructor["instructor"]
        break

    if instructor_id is None:
      raise ValidationError(
        "No Active Instructors Available for the given CurriculumPathway "
        f"= {curriculum_pathway_id} in AssociationGroup = {learner_group.uuid}")

    instructor_user = User.find_by_id(instructor_id)
    instructor_staff = Staff.find_by_uuid(instructor_user.user_type_ref)

    data = {
      "instructor_staff_id": instructor_staff.uuid,
      "instructor_user_id": instructor_user.user_id
    }

    return {
      "success": True,
      "message": "Successfully fetched instructor",
      "data": data
    }

  except ValidationError as e:
    Logger.info(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.info(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.info(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
  "/learner/{learner_id}/curriculum-pathway/{program_id}/instructors",
  response_model=GetInstructorsResponseModel)
def get_instructor_details_for_program(learner_id: str,
                                       program_id: str):
  """Fetch All Instructor Details for given learner_id and curriculum_pathway_id
  corresponding to the program.
  The details will be fetched from LearnerAssociationGroup where the given
  Learner & given program_id is associated.

  ### Args:
      learner_id (str): ID of the Learner
      curriculum_pathway_id (str): ID of the Pathway with alias as program

  ### Returns:
      instructor_id: GetInstructorsResponseModel
  """

  try:

    # TODO: rather then using the learner_id
    # we need to use user_id
    # Validation if Learner Exists
    Learner.find_by_uuid(learner_id)

    # Validation if User of the given Learner Exists
    user_learner = User.find_by_user_type_ref(learner_id)

    # Validation if Pathway Exists
    pathway = CurriculumPathway.find_by_uuid(program_id)

    if pathway.alias != "program":
      raise ValidationError(
        f"Pathway with {program_id} has alias as {pathway.alias}"
        " instead of program"
      )
    filter_user = {
      "user": user_learner.user_id,
      "status": "active"
    }
    learner_association_group = AssociationGroup.collection.filter(
      "associations.curriculum_pathway_id", "==", program_id).filter(
      "users", "array_contains", filter_user).get()

    if not learner_association_group:
      raise ValidationError(
        f"Learner with User ID {user_learner.id} "
        "is not actively associated with with the given "
        f"program with uuid {program_id} in any Association group"
      )

    instructor_list = []
    instructors = learner_association_group.associations.get("instructors", [])
    for instructor in instructors:
      if instructor["status"] == "active":
        instructor_user = User.find_by_id(instructor["instructor"])
        instructor_staff = Staff.find_by_uuid(instructor_user.user_type_ref)
        discipline = CurriculumPathway.find_by_uuid(
          instructor["curriculum_pathway_id"])
        instructor_dict = {
          "user_id": instructor["instructor"],
          "staff_id": instructor_staff.uuid,
          "discipline_id": instructor["curriculum_pathway_id"],
          "discipline_name": discipline.name
        }
        instructor_list.append(instructor_dict)

    return {
      "success": True,
      "message": "Successfully fetched instructor details",
      "data": instructor_list
    }

  except ValidationError as e:
    Logger.info(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.info(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.info(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
  "/learner/{learner_id}/curriculum-pathway",
  response_model=GetLearnerPathwayIdResponse)
def get_curriculum_pathway_for_the_learner(learner_id: str):
  """The get curriculum pathway for the given learner
  ### Args:
    learner_id (str): Unique identifier for the learner

  ### Raises:
    ResourceNotFoundException: If the learner does not exist.
    Exception 500:
    Internal Server Error. Raised if something went wrong

  ### Returns:
    GetLearnerPathwayIdResponse: curriculum_pathway_id belongs to given learner

  NOTE: To get the curriculum pathway for the given learner,
  We need to make sure that the given learner should add in the learner
  association group
  """
  try:
    # TODO: rather then using the learner_id
    # we need to use user_id
    learner = Learner.find_by_uuid(learner_id)

    user = User.find_by_user_type_ref(learner.uuid)

    learner_association_groups = AssociationGroup.collection.filter(
      "association_type", "==", "learner").order("-created_time").fetch()

    curriculum_pathway_id = None

    # It will first check the learner-id in all the
    # learner association group if learner association
    # found then will fetch the curriculum pathway id
    # association with that learner association group
    for learner_association_group in learner_association_groups:

      if any(user_dict["user"] == user.user_id
             for user_dict in learner_association_group.users):
        curriculum_pathway_id = learner_association_group.associations[
          "curriculum_pathway_id"]
        break

    if curriculum_pathway_id is None:
      raise ResourceNotFoundException(
        f"Given Learner with uuid {learner_id} is not "
        "present in any of the learner association group")

    if curriculum_pathway_id == "":
      raise ResourceNotFoundException("No curriculum pathway id "
                                      f"found for the given Learner "
                                      f"with uuid {learner_id}")

    data = {"curriculum_pathway_id": curriculum_pathway_id}

    return {
      "success": True,
      "message": "Successfully fetch the curriculum pathway "
                 "for the learner",
      "data": data
    }
  except ValidationError as e:
    Logger.info(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.info(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.info(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
  "/learner/{learner_id}/coach",
  response_model=CoachesResponseModel,
  responses={404: {
    "model": NotFoundErrorResponseModel
  }})
def get_coach_details(learner_id: str):
  """
  Function to fetch Coach Details for a given learner_id.
  The details will be fetched from LearnerAssociationGroup by first
  identifying and fetching the LearnerAssociationGroup details where
  the Learner is associated. Then from the AssociationGroup the corresponding
  coach will be identified, and details of the coach will be fetched

  NOTE: To get the coach details for given learner, the user_id for user
  corresponding to given learner must exist in any one learner association
  groups.

  Args:
    learner_id: str, ID of the Learner

  Returns:
    coach_id: CoachesResponseModel
  """
  try:
    # Validate if Learner Exists
    Learner.find_by_uuid(learner_id)

    # Fetch if User corresponding to the given Learner
    user_learner = User.find_by_user_type_ref(learner_id)
    if user_learner.user_type != "learner":
      raise ValidationError(f"User for given user_id {user_learner.user_id} is "
                            "not of Learner type")

    # Fetch all learner association groups
    learner_association_groups = AssociationGroup.collection.filter(
      "association_type", "==", "learner").fetch()
    group_fields = [i.get_fields(reformat_datetime=True) for i in
                    learner_association_groups]

    # Find Learner Association Groups in which user_id for given learner exists
    learner_group = None
    for group in group_fields:
      for user in group["users"]:
        if user_learner.user_id == user["user"] and user["status"] == "active":
          learner_group = group
          break

    if not learner_group:
      raise ValidationError(f"User for given learner_id {learner_id} is not "
                            "associated in any Learner Association Group")

    # Identify coaches from Learner Association Groups
    coach_user_id = None
    for coach in learner_group.get("associations").get("coaches"):
      if coach["status"] == "active":
        coach_user_id = coach["coach"]
      break

    if not coach_user_id:
      raise ValidationError("No active coach exists in Learner Association "
                            f"Group for user corresponding to "
                            f"given learner_id {learner_id}")

    coach_user = User.find_by_user_id(coach_user_id)
    coach_staff = Staff.find_by_uuid(coach_user.user_type_ref)

    return {
      "success": True,
      "message": "Successfully fetched the coach",
      "data": {
        "coach_staff_id": coach_staff.uuid,
        "coach_user_id": coach_user.user_id
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
