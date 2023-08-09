""" Learning Record endpoints """
from fastapi import APIRouter, UploadFile, File, Query
from copy import deepcopy
from common.models import Activity
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                PayloadTooLargeError, ConflictError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          Conflict,ResourceNotFound,
                                          PayloadTooLarge)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from schemas.activity_schema import (ActivityImportJsonResponse, DeleteActivity,
    UpdateActivityResponseModel, PostActivityResponseModel, BasicActivityModel,
    UpdateActivityModel, AllActivitiesResponseModel, GetActivityResponseModel)
from services.json_import import json_import
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES
# pylint: disable = broad-except

ERROR_RESPONSE_DICT = deepcopy(ERROR_RESPONSES)
del ERROR_RESPONSE_DICT[422]

router = APIRouter(
    tags=["Activity"],
    responses=ERROR_RESPONSE_DICT)


@router.get(
    "/activities",
    response_model=AllActivitiesResponseModel,
    name="Get All Activities")
def get_activities(skip: int = Query(0, ge=0, le=2000),
                  limit: int = Query(10, ge=1, le=100)):
  """The get activities endpoint will return an array of activities from
  firestore

  Args:
      agent : Id of the agent.
      skip (int): Number of objects to be skipped
      limit (int): Size of activity array to be returned

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      AllActivitiesResponseModel: Array of Activity Objects
  """
  try:
    collection_manager = Activity.collection

    activities = collection_manager.order("-created_time").offset(skip).fetch(
        limit)
    activities = [i.get_fields(reformat_datetime=True) for i in activities]
    count = 10000
    response = {"records": activities, "total_count": count}
    return {
        "success": True,
        "message": "Data fetched successfully",
        "data": response
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/activity/{uuid}",
    response_model=GetActivityResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_activity(uuid: str):
  """The get activity endpoint will return the activity from firestore of which
  uuid is provided

  Args:
      uuid (str): Unique identifier for activity
  Raises:
      ResourceNotFoundException: If the activity does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      GetactivityResponseModel: activity Object
  """
  try:
    activity = Activity.find_by_uuid(uuid)
    activity_fields = activity.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully fetched the activity",
        "data": activity_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post("/activity", response_model=PostActivityResponseModel)
def create_activity(input_actvity: BasicActivityModel):
  """The post activity endpoint will add the given activity in request body to
  the firestore

  Args:
      input_activity (BasicActivityModel): input activity to be inserted

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      PostActivityResponseModel: Activity Object
  """
  try:
    input_activity_dict = {**input_actvity.dict()}
    activity = Activity.find_by_name(input_activity_dict["name"])
    if activity is None:
      new_activity = Activity()
      new_activity = new_activity.from_dict(input_activity_dict)
      new_activity.uuid = ""
      new_activity.save()
      new_activity.uuid = new_activity.id
      new_activity.update()

      activity_fields = new_activity.get_fields(reformat_datetime=True)

      return {
          "success": True,
          "message": "Successfully created the activity",
          "data": activity_fields
      }
    else:
      raise ConflictError(
    f"Activity with the given name {input_activity_dict['name']} already exists"
    )

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ConflictError as e:
    raise Conflict(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/activity/{uuid}",
    response_model=UpdateActivityResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_activity(uuid: str, input_activity: UpdateActivityModel):
  """Update a activity with the uuid passed in the request body

  Args:
      input_activity (UpdateActivityModel): Required body of the activity

  Raises:
      ResourceNotFoundException: If the activity does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      UpdateActivityResponseModel: Activity Object
  """
  try:
    existing_activity = Activity.find_by_uuid(uuid)

    input_activity_dict = {**input_activity.dict(exclude_unset=True)}
    activity_fields = existing_activity.get_fields()

    for key, value in input_activity_dict.items():
      activity_fields[key] = value
    for key, value in activity_fields.items():
      setattr(existing_activity, key, value)

    existing_activity.update()
    activity_fields = existing_activity.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully updated the activity",
        "data": activity_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/activity/{uuid}",
    response_model=DeleteActivity,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_activity(uuid: str):
  """Delete a activity with the given uuid from firestore

  Args:
      uuid (str): Unique id of the activity

  Raises:
      ResourceNotFoundException: If the actvity does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      JSON: Success/Fail Message
  """
  try:
    activity = Activity.find_by_uuid(uuid)

    Activity.collection.delete(activity.key)

    return {"success": True, "message": "Successfully deleted the Activity"}

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/activity/import/json",
    response_model=ActivityImportJsonResponse,
    name="Import Activities from JSON file",
    responses={413: {
        "model": PayloadTooLargeResponseModel
    }})
async def import_activities(json_file: UploadFile = File(...)):
  """Create activities from json file

  Args:
    json_file (UploadFile): Upload json file consisting of activities.
    json_schema should match BasicActivityModel

  Raises:
    Exception: 500 Internal Server Error if something fails

  Returns:
      ActivityImportJsonResponse: Array of uuid's
  """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
        f"File size is too large: {json_file.filename}"
      )
    await json_file.seek(0)
    final_output = json_import(
        json_file=json_file,
        json_schema=BasicActivityModel,
        model_obj=Activity,
        object_name="activities")
    return final_output
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
