""" Action endpoints """
from fastapi import APIRouter, Query
from common.models import Action
from common.utils.errors import ResourceNotFoundException, ValidationError, ConflictError
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound)
from schemas.action_schema import (AllActionResponseModel,
                                   GetActionResponseModel, ActionModel,
                                   PostActionResponseModel, UpdateActionModel,
                                   UpdateActionResponseModel, DeleteAction)
from schemas.error_schema import NotFoundErrorResponseModel
from config import ERROR_RESPONSES

router = APIRouter(tags=["Action"], responses=ERROR_RESPONSES)


@router.get(
    "/actions", response_model=AllActionResponseModel, name="Get all Actions")
def get_actions(skip: int = Query(0, ge=0, le=2000),
                limit: int = Query(10, ge=1, le=100)):
  """The get actions endpoint will return an array actions from
  firestore

  ### Args:
      skip (int): Number of objects to be skipped
      limit (int): Size of action array to be returned
      fetch_tree (bool): To fetch the entire object instead
      of the UUID of the object

  ### Raises:
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      AllActionResponseModel: Array of Action Object
  """
  try:
    collection_manager = Action.collection
    actions = collection_manager.order("-created_time").offset(
      skip).fetch(limit)
    actions = [i.get_fields(reformat_datetime=True) for i in actions]
    return {
        "success": True,
        "message": "Data fetched successfully",
        "data": actions
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/action/{uuid}",
    response_model=GetActionResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_action(uuid: str):
  """The get action endpoint will return the action from firestore of
  which uuid is provided

  ### Args:
      uuid (str): Unique identifier for action

  ### Raises:
      ResourceNotFoundException: If the action does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      GetActionResponseModel: action Object
  """
  try:
    action = Action.find_by_uuid(uuid)
    action_fields = action.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully fetched the action",
        "data": action_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post("/action", response_model=PostActionResponseModel)
def create_action(input_action: ActionModel):
  """The create action endpoint will add the action in request body to the
  firestore

  ### Args:
      input_action (ActionModel): input action to be inserted
      name : Unique for every action

  ### Raises:
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      PostActionResponseModel: Action Object
  """
  try:
    existing_action = Action.find_by_name(input_action.name)
    if existing_action is not None:
      raise ConflictError(
        f"Action with the given name: {input_action.name} "
        "already exists")

    input_action_dict = {**input_action.dict()}
    new_action = Action()
    new_action = new_action.from_dict(input_action_dict)
    new_action.uuid = ""
    new_action.save()
    new_action.uuid = new_action.id
    new_action.update()

    action_fields = new_action.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully created the action",
        "data": action_fields
    }

  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/action/{uuid}",
    response_model=UpdateActionResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_action(uuid: str, input_action: UpdateActionModel):
  """Update a action with the uuid passed in the request body

  ### Args:
      input_action (ActionModel): Required body of the action
      name : Unique for every action

  ### Raises:
      ResourceNotFoundException: If the action does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      UpdateActionResponseModel: Action Object
  """
  try:
    existing_action = Action.find_by_name(input_action.name)
    if existing_action is not None:
      raise ConflictError(
        f"Action with the given name: {input_action.name} "
        "already exists")

    existing_action = Action.find_by_uuid(uuid)

    input_action_dict = {**input_action.dict()}
    action_fields = existing_action.get_fields()

    for key, value in input_action_dict.items():
      action_fields[key] = value
    for key, value in action_fields.items():
      setattr(existing_action, key, value)

    existing_action.update()
    action_fields = existing_action.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully updated the action",
        "data": action_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/action/{uuid}",
    response_model=DeleteAction,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_action(uuid: str):
  """Delete a action with the given uuid from firestore

  ### Args:
      uuid (str): Unique id of the action

  ### Raises:
      ResourceNotFoundException: If the action does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      JSON: Success/Fail Message
  """
  try:
    action = Action.find_by_uuid(uuid)

    Action.collection.delete(action.key)

    return {"success": True, "message": "Successfully deleted the action"}

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
