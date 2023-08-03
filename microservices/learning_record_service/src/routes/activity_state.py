"""Activity State endpoints"""

from fastapi import APIRouter, UploadFile, File, Query
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from common.models import ActivityState
from schemas.activity_state_schema import (
    DeleteActivityState, UpdateActivityStateModel,
    UpdateActivityStateResponseModel, ActivityStateModel,
    PostActivityStateResponseModel, GetActivityStateResponseModel,
    AllActivityStateResponseModel, ActivityStateImportJsonResponse)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from services.json_import import json_import
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES
# pylint: disable = broad-except

router = APIRouter(
    tags=["Activity State"],
    responses=ERROR_RESPONSES)

@router.get(
    "/activity-states",
    response_model=AllActivityStateResponseModel,
    name="Get all Activity States")
def get_all_activity_states(skip: int = Query(0, ge=0, le=2000),
                            limit: int = Query(10, ge=1, le=100)
):
  """
  Returns an array of ActivityStates from firestore
  Args:
    skip (int): Number of objects to be skipped
    limit (int): Size of Activity States array to be returned
  Raises:
    Exception: 500 Internal Server Error if something went wrong
  Returns:
    AllActivityStateResponseModel: Array of ActivityState objects
  """
  try:
    activity_states = ActivityState.collection.order("-created_time").offset(
        skip).fetch(limit)
    activity_states = [
        i.get_fields(reformat_datetime=True) for i in activity_states
    ]
    count = 10000
    response = {"records": activity_states, "total_count": count}
    return {
        "success": True,
        "message": "Successfully fetched the activity states",
        "data": response
    }
  except ValidationError as e:
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/activity-state/{uuid}",
    response_model=GetActivityStateResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_activity_state(uuid: str):
  """
  Returns the ActivityState document from Firestore of which uuid is provided.
  Args:
    uuid (str): Unique identifier for the ActivityState
  Raises:
    ResourceNotFoundException: If the Activity State does not exist
    Exception: 500 Internal Server Error if something went wrong
  Returns:
    ActivityStateResponseModel: ActivityState document
  """
  try:
    activity_state = ActivityState.find_by_uuid(uuid)
    activity_state_fields = activity_state.get_fields(reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully fetched the activity state",
        "data": activity_state_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post("/activity-state", response_model=PostActivityStateResponseModel)
def create_activity_state(input_activity_state: ActivityStateModel):
  """
  The post activity_state endpoint will add the given activity state
  in request body to the firestore

  Args:
    input_skill (ActivityStateModel): input activity state to be inserted

  Raises:
    Exception: 500 Internal Server Error if something went wrong

  Returns:
    PostActivityStateResponseModel: ActivityState Object
  """
  try:
    input_activity_state_dict = {**input_activity_state.dict()}

    new_activity_state = ActivityState()
    new_activity_state = new_activity_state.from_dict(input_activity_state_dict)
    new_activity_state.uuid = ""
    new_activity_state.save()
    new_activity_state.uuid = new_activity_state.id
    new_activity_state.update()

    activity_state_fields = new_activity_state.get_fields(
        reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully created the activity state",
        "data": activity_state_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/activity-state/{uuid}",
    response_model=UpdateActivityStateResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_activity_state(uuid: str,
                          input_activity_state: UpdateActivityStateModel):
  """
  Updates an activity state

  Args:
    input_activity_state (UpdateActivityStateModel): Required body of the
      activity state

  Raises:
    ResourceNotFoundException: If the activity state does not exist
    Exception: 500 Internal Server Error if something went wrong

  Returns:
    UpdateActivityStateResponseModel: ActivityState Object
  """
  try:
    existing_activity_state = ActivityState.find_by_uuid(uuid)

    input_activity_state_dict = {
        **input_activity_state.dict(exclude_unset=True)
    }
    activity_state_fields = existing_activity_state.get_fields()

    for key, value in input_activity_state_dict.items():
      activity_state_fields[key] = value
    for key, value in activity_state_fields.items():
      setattr(existing_activity_state, key, value)

    existing_activity_state.update()
    activity_state_fields = existing_activity_state.get_fields(
        reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully updated the activity state",
        "data": activity_state_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/activity-state/{uuid}",
    response_model=DeleteActivityState,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_activity_state(uuid: str):
  """
  Delete an activity state with the given uuid from firestore

  Args:
    uuid (str): Unique id of the activity state

  Raises:
    ResourceNotFoundException: If the activity state does not exist
    Exception: 500 Internal Server Error if something went wrong

  Returns:
    JSON: Success/Fail Message
  """
  try:
    activity_state = ActivityState.find_by_uuid(uuid)
    ActivityState.collection.delete(activity_state.key)
    return {
        "success": True,
        "message": "Successfully deleted the activity state"
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/activity-state/import/json",
    response_model=ActivityStateImportJsonResponse,
    name="Import Activity States from JSON file",
    responses={413: {
        "model": PayloadTooLargeResponseModel
    }})
async def import_activity_state(json_file: UploadFile = File(...)):
  """
  Create activity states from json file

  Args:
    json_file (UploadFile): Upload json file consisting of activity states.
    json_schema should match ActivityStateModel

  Raises:
    Exception: 500 Internal Server Error if something fails

  Returns:
    ActivityStateImportJsonResponse: Array of uuid's
  """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
        f"File size is too large: {json_file.filename}"
      )
    await json_file.seek(0)
    final_output = json_import(
        json_file=json_file,
        json_schema=ActivityStateModel,
        model_obj=ActivityState,
        object_name="activity_states")
    return final_output
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
