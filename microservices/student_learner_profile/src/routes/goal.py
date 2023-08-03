""" Goal endpoints """
import json
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Query
from common.models import Goal
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from schemas.goal_schema import (GetAllGoalsResponseModel, GoalModel,
                                 GetGoalResponseModel, PostGoalResponseModel,
                                 UpdateGoalResponseModel, UpdateGoalModel,
                                 GoalImportJsonResponse, DeleteGoal,
                                 GoalSearchResponseModel)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES
# pylint: disable = broad-except

router = APIRouter(prefix="/goal", tags=["Goal"], responses=ERROR_RESPONSES)


@router.get("/search", response_model=GoalSearchResponseModel)
def search_goal(name: Optional[str] = None):
  """Search for goals based on the goal name

  Args:
      name(str): Name of the goal. Defaults to None.

  Returns:
      GoalSearchResponseModel: List of goal objects
  """
  result = []
  if name:
    # fetch goal that matches goal name
    name_node_items = Goal.find_by_name(name)
    for name_node_item in name_node_items:
      name_node_dict = name_node_item.get_fields(reformat_datetime=True)
      result.append(name_node_dict)
    return {
        "success": True,
        "message": "Successfully fetched the goals",
        "data": result
    }
  else:
    raise BadRequest("Missing or invalid request parameters")


@router.get(
    "",
    response_model=GetAllGoalsResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_all_goals(goal_type: str = None,
                  skip: int = Query(0, ge=0, le=2000),
                  limit: int = Query(10, ge=1, le=100),
                  fetch_archive: Optional[bool] = None):
  """The get all goals endpoint will return the goal from firestore
  along with the provided filters

  Args:
      goal_type (str) : name of the goal type to be filtered for goal
      skip (int): Number of objects to be skipped
      limit (int): Size of learner array to be returned

  Raises:
      ResourceNotFoundException: If the goal does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      GetGoalResponseModel: Goal Object
  """
  try:
    collection_manager = Goal.collection.filter("is_deleted", "==", False)
    if goal_type:
      collection_manager = collection_manager.filter("type", "==", goal_type)
    if fetch_archive is not None:
      collection_manager = collection_manager\
                            .filter("is_archived", "==", fetch_archive)
    goal = collection_manager.order("-created_time").offset(skip).fetch(limit)
    goal_fields = [i.get_fields(reformat_datetime=True) for i in goal]
    count = 10000
    response = {"records": goal_fields, "total_count": count}
    return {
        "success": True,
        "message": "Successfully fetched the goal",
        "data": response
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/{uuid}",
    response_model=GetGoalResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_goal(uuid: str):
  """The get goal endpoint will return the goal from firestore of which uuid is
  provided

  Args:
      uuid (str): Unique identifier for goal

  Raises:
      ResourceNotFoundException: If the goal does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      GetGoalResponseModel: Goal Object
  """
  try:
    goal = Goal.find_by_uuid(uuid)
    goal_fields = goal.get_fields(reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully fetched the goal",
        "data": goal_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "",
    response_model=PostGoalResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def create_goal(input_goal: GoalModel):
  """The create goal endpoint will add the given goal in request body to the
  firestore

  Args:
      input_goal (GoalModel): input goal to be inserted

  Raises:
      ResourceNotFoundException: If the goal does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      PostGoalResponseModel: Goal Object
  """
  try:
    new_goal = Goal()
    input_goal_dict = {**input_goal.dict()}
    new_goal = new_goal.from_dict(input_goal_dict)
    new_goal.uuid = ""

    new_goal.save()
    new_goal.uuid = new_goal.id
    new_goal.update()
    goal_fields = new_goal.get_fields(reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully created the goal",
        "data": goal_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/{uuid}",
    response_model=UpdateGoalResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_goal(uuid: str, input_goal: UpdateGoalModel):
  """Update a goal with the uuid passed in the request body

  Args:
      uuid (str) : Unique id of the goal
      input_goal (UpdateGoalModel): Required body of the goal

  Raises:
      ResourceNotFoundException: If the goal does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      UpdateGoalResponseModel: Goal Object
  """
  try:
    existing_goal = Goal.find_by_uuid(uuid)

    input_goal_dict = {**input_goal.dict()}
    goal_fields = existing_goal.get_fields()

    for key, value in input_goal_dict.items():
      goal_fields[key] = value
    for key, value in goal_fields.items():
      setattr(existing_goal, key, value)

    existing_goal.update()
    goal_fields = existing_goal.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully updated the goal",
        "data": goal_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/{uuid}",
    response_model=DeleteGoal,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_goal(uuid: str):
  """Delete a goal with the given uuid from firestore

  Args:
      uuid (str): Unique id of the goal

  Raises:
      ResourceNotFoundException: If the goal does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      JSON: Success/Fail Message
  """
  try:
    Goal.delete_by_uuid(uuid)
    return {"success": True, "message": "Successfully deleted the goal"}
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/import/json",
    response_model=GoalImportJsonResponse,
    name="Import Goals from JSON file",
    responses={
      404: {
        "model": NotFoundErrorResponseModel
      },
      413: {
        "model": PayloadTooLargeResponseModel
      }
    })
async def import_goals(json_file: UploadFile = File(...)):
  """Create goals from json file

  Args:
    json_file (UploadFile): Upload json file consisting of goals.
    json_schema should match GoalModel

  Raises:
    Exception: 500 Internal Server Error if something fails

  Returns:
      GoalImportJsonResponse: Array of uuid's
  """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
        f"File size is too large: {json_file.filename}"
      )
    await json_file.seek(0)
    goals = json.load(json_file.file)
    inserted_data = []
    for goal in goals:
      new_goal = Goal()
      new_goal = new_goal.from_dict(goal)
      new_goal.uuid = ""
      new_goal.save()
      new_goal.uuid = new_goal.id
      new_goal.update()
      inserted_data.append(new_goal.uuid)
    return {
        "success": True,
        "message": "Successfully created the goals",
        "data": inserted_data
    }
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
