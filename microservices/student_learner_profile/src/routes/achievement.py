""" Achievement endpoints """
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Query
from common.models import Achievement, LearnerProfile
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from schemas.achievement_schema import (
    PostAchievementModel, GetAchievementResponseModel,
    PostAchievementResponseModel, UpdateAchievementResponseModel,
    UpdateAchievementModel, DeleteAchievement, AllAchievementsResponseModel,
    AchievementSearchResponseModel, AchievementImportJsonResponse,
    BasicAchievementModel, ALLOWED_ACHIEVEMENT_TYPES)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from services.json_import import json_import
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES
# pylint: disable = broad-except

router = APIRouter(tags=["Achievement"], responses=ERROR_RESPONSES)


@router.get(
    "/achievement/search", response_model=AchievementSearchResponseModel)
def search_achievement(
    type: Optional[ALLOWED_ACHIEVEMENT_TYPES] = "Achievement"):  # pylint: disable=redefined-builtin
  """Search for achievements based on the achievement first name

  Args:
      type(str): First name of the achievement. Defaults to 'Achievement'.

  Returns:
      AchievementSearchResponseModel: List of achievement objects
  """
  result = []
  if type:
    # fetch achievement that matches achievement id
    achievement_node_items = Achievement.find_by_type(type)
    for achievement_node_item in achievement_node_items:
      achievement_node_dict = achievement_node_item.get_fields(
          reformat_datetime=True)
      result.append(achievement_node_dict)
    return {
        "success": True,
        "message": "Successfully fetched the achievements",
        "data": result
    }
  else:
    raise BadRequest("Missing or invalid request parameters")


@router.get(
    "/achievements",
    response_model=AllAchievementsResponseModel,
    name="Get all Achievements")
def get_achievements(name: str = None,
                     achievement_type: ALLOWED_ACHIEVEMENT_TYPES = None,
                     tag: str = None,
                     skip: int = Query(0, ge=0, le=2000),
                     limit: int = Query(10, ge=1, le=100),
                     fetch_archive: Optional[bool] = None):
  """The get achievements endpoint will return an array achievements from
  firestore

  Args:
      achievement_type (str) : name of the achievement type to be filtered
                                for achievement
      name (str) : name given to achievement
      tag (str) : tag given to achievement
      skip (int): Number of objects to be skipped
      limit (int): Size of achievement array to be returned

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      AllAchievementsResponseModel: Array of Achievement Object
  """
  try:
    collection_manager = Achievement.collection.filter("is_deleted", "==",
                                                       False)

    if name:
      collection_manager = collection_manager.filter("name", "==", name)
    if achievement_type:
      collection_manager = collection_manager.filter("type", "==",
                                                     achievement_type)
    if tag:
      collection_manager = collection_manager.filter("tags", "array_contains",
                                                     tag)
    if fetch_archive is not None:
      collection_manager = collection_manager\
                            .filter("is_archived", "==", fetch_archive)

    achievements = collection_manager.order("-created_time").offset(skip).fetch(
        limit)

    achievements = [i.get_fields(reformat_datetime=True) for i in achievements]
    count = 10000
    response = {"records": achievements, "total_count": count}
    return {
        "success": True,
        "message": "Data fetched successfully",
        "data": response
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/achievement",
    response_model=PostAchievementResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def create_achievement(input_achievement: PostAchievementModel):
  """The create achievement endpoint will add the given achievement in request
  body to the firestore

  Args:
      input_achievement (PostAchievementModel): input achievement to be
      inserted

  Raises:
      ResourceNotFoundException: If the achievement does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      PostAchievementResponseModel: Achievement Object
  """
  try:
    input_achievement_dict = {**input_achievement.dict()}
    new_achievement = Achievement.create_object(input_achievement_dict)
    achievement_fields = new_achievement.get_fields(reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully created the achievement",
        "data": achievement_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/achievement/{uuid}",
    response_model=GetAchievementResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_achievement(uuid: str):
  """The get achievement endpoint will return the achievement from
  firestore of which uuid is provided

  Args:
      uuid (str): Unique identifier for achievement

  Raises:
      ResourceNotFoundException: If the achievement does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      AchievementResponseModel: Achievement Object
  """
  try:
    achievement = Achievement.find_by_uuid(uuid)
    achievement_fields = achievement.get_fields(reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully fetched the achievement",
        "data": achievement_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/achievement/{uuid}",
    response_model=UpdateAchievementResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_achievement(uuid: str, input_achievement: UpdateAchievementModel):
  """Update a achievement with the uuid passed in the request body

  Args:
      input_achievement (UpdateAchievementModel): Required body of the
      achievement

  Raises:
      ResourceNotFoundException: If the achievement does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      UpdateAchievementResponseModel: Achievement Object
  """
  try:
    existing_achievement = Achievement.find_by_uuid(uuid)

    input_achievement_dict = {**input_achievement.dict()}
    achievement_fields = existing_achievement.get_fields()

    for key, value in input_achievement_dict.items():
      achievement_fields[key] = value
    for key, value in achievement_fields.items():
      setattr(existing_achievement, key, value)

    existing_achievement.update()
    achievement_fields = existing_achievement.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully updated the achievement",
        "data": achievement_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/achievement/{uuid}",
    response_model=DeleteAchievement,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_achievement(uuid: str):
  """Delete a achievement with the given uuid from firestore

  Args:
      uuid (str): Unique id of the achievement

  Raises:
      ResourceNotFoundException: If the achievement does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      JSON: Success/Fail Message
  """
  try:
    learner_profiles_to_update = LearnerProfile.collection.filter(
        "achievements", "array_contains", uuid).fetch()
    learner_profile_ids = [
        learner_profile.uuid for learner_profile in learner_profiles_to_update
    ]
    for learner_profile_id in learner_profile_ids:
      learner_profile = LearnerProfile.find_by_uuid(learner_profile_id)
      achievements_list = learner_profile.achievements
      if uuid in achievements_list:
        achievements_list.remove(uuid)
        learner_profile.achievements = achievements_list
        learner_profile.update()
    Achievement.delete_by_uuid(uuid)
    return {"success": True, "message": "Successfully deleted the achievement"}
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/achievement/import/json",
    response_model=AchievementImportJsonResponse,
    responses={413: {
        "model": PayloadTooLargeResponseModel
    }},
    name="Import Achievements from JSON file")
async def import_achievements(json_file: UploadFile = File(...)):
  """Create achievements from json file

  Args:
    json_file (UploadFile): Upload json file consisting of achievements.
    json_schema should match PostAchievementModel

  Raises:
    Exception: 500 Internal Server Error if something fails

  Returns:
      AchievementImportJsonResponse: Array of uuid's
  """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
        f"File size is too large: {json_file.filename}"
      )
    await json_file.seek(0)
    final_output = json_import(
        json_file=json_file,
        json_schema=BasicAchievementModel,
        model_obj=Achievement,
        object_name="achievements")
    return final_output
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
