""" Learner Profile endpoints """
import json
import traceback
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Query
from common.models import LearnerProfile, Learner, Achievement
from common.utils.errors import (ConflictError, ResourceNotFoundException,
                                 ValidationError, PayloadTooLargeError)
from common.utils.logging_handler import Logger
from common.utils.http_exceptions import (Conflict, InternalServerError,
                                          BadRequest, PayloadTooLarge,
                                          ResourceNotFound)
from schemas.learner_profile_schema import (
    GetAllLearnerProfilesResponseModel, PostLearnerProfileModel,
    GetLearnerProfileResponseModel, PostLearnerProfileResponseModel,
    UpdateLearnerProfileResponseModel, UpdateLearnerProfileModel,
    DeleteLearnerProfile, LearnerProfileSearchResponseModel,
    LearnerProfileImportJsonResponse)
from schemas.error_schema import (ConflictResponseModel,
                                  NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES
# pylint: disable = broad-exception-raised

router = APIRouter(tags=["Learner Profile"], responses=ERROR_RESPONSES)


@router.get(
    "/learner-profile/search", response_model=LearnerProfileSearchResponseModel)
def search_learner_profile(learner_id: Optional[str] = None):
  """Search for learner profiles based on the learner id

  Args:
      learner_id(str): Learner id of the learner. Defaults to None.

  Returns:
      LearnerProfileSearchResponseModel: List of learner profile objects
  """
  try:
    result = []
    if learner_id:
      # fetch learner profile that matches learner id
      learner_profile_node_item = LearnerProfile.find_by_learner_id(learner_id)
      if learner_profile_node_item:
        learner_profile_node_dict = learner_profile_node_item.get_fields(
            reformat_datetime=True)
        result.append(learner_profile_node_dict)
      return {
          "success": True,
          "message": "Successfully fetched the learner profiles",
          "data": result
      }
    else:
      raise ValidationError("Missing or invalid request parameters")
  except ResourceNotFoundException as e:
    Logger.info(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.info(traceback.print_exc())
    raise BadRequest(str(e)) from e


@router.get(
    "/learner-profile",
    response_model=GetAllLearnerProfilesResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_all_learner_profiles(learning_goal: str = None,
                             skip: int = Query(0, ge=0, le=2000),
                             limit: int = Query(10, ge=1, le=100),
                             fetch_archive: Optional[bool] = None):
  """The get all learner profiles endpoint will return all the learner
  profiles from firestore along with the provided filters

  Args:
      learning_goal (str): name of the learning goal to be filtered
                            for learner profile
      skip (int): Number of objects to be skipped
      limit (int): Size of learner array to be returned

  Raises:
      ResourceNotFoundException: If the learner profile does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      GetLearnerProfileResponseModel: Learner Profile Object
  """
  try:
    collection_manager = LearnerProfile.collection.filter(
        "is_deleted", "==", False)
    if fetch_archive is not None:
      collection_manager = collection_manager\
                            .filter("is_archived", "==", fetch_archive)
    array_flag = 0
    if learning_goal:
      collection_manager = collection_manager.filter("learning_goals",
                                                     "array_contains",
                                                     learning_goal)
      array_flag += 1

    if array_flag > 1:
      raise Exception(
          # pylint: disable-next = line-too-long
          "Please use only one of the following fields for filter at " + \
            "a time - learning_goal, learning_pathway, learning_experience"
      )

    learner_profile = collection_manager.order("-created_time").offset(
        skip).fetch(limit)

    learner_profile_fields = [
        i.get_fields(reformat_datetime=True) for i in learner_profile
    ]
    return {
        "success": True,
        "message": "Successfully fetched the learner profile/s",
        "data": learner_profile_fields
    }
  except ResourceNotFoundException as e:
    Logger.info(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.info(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.info(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
    "/learner/{learner_id}/learner-profile",
    response_model=GetLearnerProfileResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_learner_profile(learner_id: str):
  """The get learner profile endpoint will return the learner profile of
  the given learner from the firestore

  Args:
      learner_id (str): Unique id of the learner as path param

  Raises:
      ResourceNotFoundException: If the learner profile does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      GetLearnerProfileResponseModel: Learner Profile Object
  """
  try:
    learner_profile = LearnerProfile.find_by_learner_id(learner_id)

    learner_profile_fields = learner_profile.get_fields(reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully fetched the learner profile",
        "data": learner_profile_fields
    }
  except ResourceNotFoundException as e:
    Logger.info(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.info(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
    "/learner/{learner_id}/learner-profile/{uuid}",
    response_model=GetLearnerProfileResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_learner_profile_for_given_id(learner_id: str, uuid: str):
  """The get learner profile for given id endpoint will return the
  learner profile from firestore of which uuid is provided for the
  given learner id

  Args:
      learner_id (str) : Unique id of the learner
      uuid (str): Unique id of learner profile

  Raises:
      ResourceNotFoundException: If the learner profile does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      GetLearnerProfileResponseModel: Learner Profile Object
  """
  try:
    Learner.find_by_uuid(learner_id)
    learner_profile = LearnerProfile.find_by_uuid(uuid)
    if learner_profile.learner_id != learner_id:
      raise ResourceNotFoundException(
          f"Learner profile with id '{uuid}' and learner id \
          '{learner_id}' not found")

    learner_profile_fields = learner_profile.get_fields(reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully fetched the learner profile",
        "data": learner_profile_fields
    }
  except ResourceNotFoundException as e:
    Logger.info(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.info(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/learner/{learner_id}/learner-profile",
    response_model=PostLearnerProfileResponseModel,
    responses={
        404: {
            "model": NotFoundErrorResponseModel
        },
        409: {
            "model": ConflictResponseModel
        }
    })
def create_learner_profile(learner_id: str,
                           input_learner_profile: PostLearnerProfileModel):
  """The create learner profile endpoint will add the given learner profile in
  request body to the firestore

  Args:
      learner_id (str) : Unique id of the learner
      input_learner_profile (PostLearnerProfileModel): input learner profile
      to be inserted

  Raises:
      ResourceNotFoundException: If the learner profile does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      PostLearnerProfileResponseModel: Learner Profile Object
  """
  try:
    learner = Learner.find_by_uuid(learner_id)\
    # Check if learner is archived

    if learner.is_archived is True:
      raise ValidationError("Learner Profile cannot be created for the Learner"
                            f" id: {learner_id} which is archived")
    # Checking if a learner_profile already exists with the same learner id
    learner_profile = LearnerProfile.collection.\
      filter("learner_id", "==", learner_id).get()
    if learner_profile is not None:
      raise ConflictError(
          f"Learner Profile with the given learner id: {learner_id} "
          "already exists")
    new_learner_profile = LearnerProfile()
    input_learner_profile_dict = {**input_learner_profile.dict()}
    input_learner_profile_dict["learner_id"] = learner_id

    if input_learner_profile_dict["achievements"]:
      for achievement_id in input_learner_profile_dict["achievements"]:
        Achievement.find_by_uuid(achievement_id)

    new_learner_profile = new_learner_profile.from_dict(
        input_learner_profile_dict)
    new_learner_profile.uuid = ""

    new_learner_profile.save()
    new_learner_profile.uuid = new_learner_profile.id
    new_learner_profile.update()
    learner_profile_fields = new_learner_profile.get_fields(
        reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully created the learner profile",
        "data": learner_profile_fields
    }
  except ResourceNotFoundException as e:
    Logger.info(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ConflictError as e:
    Logger.info(traceback.print_exc())
    raise Conflict(str(e)) from e
  except ValidationError as e:
    Logger.info(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.info(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.put(
    "/learner/{learner_id}/learner-profile",
    response_model=UpdateLearnerProfileResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_learner_profile(learner_id: str,
                           input_learner_profile: UpdateLearnerProfileModel):
  """Update a learner profile with the uuid passed in the request body

  Args:
      learner_id (str) : Unique id of the learner
      input_learner_profile (UpdateLearnerProfileModel): Required body of the
      learner profile

  Raises:
      ResourceNotFoundException: If the learner profile does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      UpdateLearnerProfileResponseModel: Learner Profile Object
  """
  try:
    existing_learner_profile = LearnerProfile.find_by_learner_id(learner_id)

    input_learner_profile_dict = {**input_learner_profile.dict()}

    if input_learner_profile_dict["achievements"]:
      for achievement_id in input_learner_profile_dict["achievements"]:
        Achievement.find_by_uuid(achievement_id)

    learner_profile_fields = existing_learner_profile.get_fields()

    for key, value in input_learner_profile_dict.items():
      learner_profile_fields[key] = value
    for key, value in learner_profile_fields.items():
      setattr(existing_learner_profile, key, value)

    existing_learner_profile.update()
    learner_profile_fields = existing_learner_profile.get_fields(
        reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully updated the learner profile",
        "data": learner_profile_fields
    }
  except ResourceNotFoundException as e:
    Logger.info(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.info(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.delete(
    "/learner/{learner_id}/learner-profile",
    response_model=DeleteLearnerProfile,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_learner_profile(learner_id: str):
  """Delete a learner profile with the given uuid from firestore

  Args:
      learner_id (str) : Unique id of the learner
      uuid (str): Unique id of the learner profile

  Raises:
      ResourceNotFoundException: If the learner profile does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      JSON: Success/Fail Message
  """
  try:
    existing_learner_profile = LearnerProfile.find_by_learner_id(learner_id)
    uuid = existing_learner_profile.uuid

    LearnerProfile.delete_by_uuid(uuid)
    return {
        "success": True,
        "message": "Successfully deleted the learner profile"
    }
  except ResourceNotFoundException as e:
    Logger.info(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.info(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/learner-profile/import/json",
    response_model=LearnerProfileImportJsonResponse,
    name="Import Learner Profiles from JSON file",
    responses={
        404: {
            "model": NotFoundErrorResponseModel
        },
        413: {
            "model": PayloadTooLargeResponseModel
        }
    })
async def import_learner_profiles(json_file: UploadFile = File(...)):
  """Create learner profiles from json file

  Args:
    json_file (UploadFile): Upload json file consisting of learner profiles.
    json_schema should match PostLearnerProfileModel

  Raises:
    Exception: 500 Internal Server Error if something fails

  Returns:
      LearnerProfileImportJsonResponse: Array of uuid's
  """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
          f"File size is too large: {json_file.filename}")
    await json_file.seek(0)
    learner_profiles = json.load(json_file.file)
    inserted_data = []
    for learner_profile in learner_profiles:
      new_learner_profile = LearnerProfile()
      new_learner_profile = new_learner_profile.from_dict(learner_profile)
      new_learner_profile.uuid = ""
      new_learner_profile.save()
      new_learner_profile.uuid = new_learner_profile.id
      new_learner_profile.update()
      inserted_data.append(new_learner_profile.uuid)
    return {
        "success": True,
        "message": "Successfully created the learner profiles",
        "data": inserted_data
    }
  except PayloadTooLargeError as e:
    Logger.info(traceback.print_exc())
    raise PayloadTooLarge(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.info(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.info(traceback.print_exc())
    raise InternalServerError(str(e)) from e
