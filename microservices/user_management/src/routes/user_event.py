""" UserEvent endpoints """
import traceback
from fastapi import APIRouter
from schemas.user_event import (UserEventModel, UpdateUserEventModel,
                                UserEventModelResponse, GetUserEvent,
                                GetAllUserEvents, DeleteUserEvent)
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel,
                                  NotFoundErrorResponseModel)
from common.models import User, UserEvent, LearningUnit
from common.utils.logging_handler import Logger
from common.utils.http_exceptions import InternalServerError, ResourceNotFound
from common.utils.errors import ResourceNotFoundException

router = APIRouter(
    prefix="/user/{user_id}/user_event",
    tags=["UserEvent"],
    responses={
        500: {
            "model": InternalServerErrorResponseModel
        },
        422: {
            "model": ValidationErrorResponseModel
        }
    })

SUCCESS_RESPONSE = {"status": "Success"}
FAILED_RESPONSE = {"status": "Failed"}


# pylint: disable=broad-except
@router.get(
    "/",
    response_model=GetAllUserEvents,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_all_user_event(user_id: str):
  """Get a user_event

  ### Args:
    user_event_id (str): unique id of the User

  ### Raises:
    ResourceNotFound: 404 Not Found if user doesn't exist
                    for the given user_event id
    InternalServerError: 500 Internal Server Error if something fails

  ### Returns:
    [user_event]: all user_event objects for the provided user id
  """
  try:
    User.find_by_id(user_id)
    all_user_events = list(UserEvent.collection.filter(user_id=user_id).fetch())
    output = []
    for user_event in all_user_events:
      user_event_fields = user_event.get_fields(reformat_datetime=True)
      user_event_fields["id"] = user_event.id
      output.append(user_event_fields)
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
  return {"data": output}


@router.get(
    "/{user_event_id}",
    response_model=GetUserEvent,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_user_event(user_event_id: str):
  """Get a user_event

  ### Args:
    user_event_id (str): unique id of the UserEvent

  ### Raises:
    ResourceNotFound: 404 Not Found if user_event doesn't
                  exist for the given user_event id
    InternalServerError: 500 Internal Server Error if something fails

  ### Returns:
    [user_event]: user_event object for the provided user_event id
  """
  try:
    user_event = UserEvent.find_by_id(user_event_id)
    user_event_fields = user_event.get_fields(reformat_datetime=True)
    user_event_fields["id"] = user_event.id
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
  return {"data": user_event_fields}


@router.post(
    "/",
    response_model=UserEventModelResponse,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def create_user_event(user_id: str, input_user_event: UserEventModel):
  """Register a user_event

  ### Args:
    input_user_event (UserEventModel): Required body of the user_event

  ### Raises:
    ResourceNotFound: 404 Not Found if user_event doesn't
                  exist for the given user_event id
    InternalServerError: 500 Internal Server Error if something fails
  """
  try:
    new_user_event = UserEvent()
    input_user_event_dict = {**input_user_event.dict()}
    user = User.find_by_id(user_id)
    learning_unit = LearningUnit.find_by_id(input_user_event.learning_unit)
    new_user_event = new_user_event.from_dict(input_user_event_dict)
    new_user_event.learning_unit = learning_unit.id
    if user:
      setattr(new_user_event, "user_id", user.id)
    new_user_event.save()
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
  return get_user_event(new_user_event.id)


@router.put(
    "/{user_event_id}", responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_user_event(user_event_id: str,
                      input_user_event: UpdateUserEventModel):
  """Update a user_event

  ### Args:
    input_user_event (UserEventModel): Required body of the user_event

  ### Raises:
    ResourceNotFound: 404 if user event is not found
    InternalServerError: 500 Internal Server Error if something fails

  ### Returns:
    Updated User Event
  """
  try:
    existing_user_event = UserEvent.find_by_id(user_event_id)
    user_event_fields = existing_user_event.get_fields()
    for key, value in {**input_user_event.dict()}.items():
      if value:
        user_event_fields[key] = value
    for key, value in user_event_fields.items():
      setattr(existing_user_event, key, value)
    existing_user_event.update()
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
  return get_user_event(user_event_id)


@router.delete(
    "/{user_event_id}",
    response_model=DeleteUserEvent,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_user_event(user_event_id: str):
  """Delete a user_event

  ### Args:
    user_event_id (str): unique id of the user_event

  ### Raises:
    ResourceNotFound: 404 If user is not found
    InternalServerError: 500 Internal Server Error if something fails

  """
  try:
    user_event = UserEvent.find_by_id(user_event_id)
    user_event.delete_by_id(user_event_id)
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
  return SUCCESS_RESPONSE
