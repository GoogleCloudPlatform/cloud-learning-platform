""" Session endpoints """
from typing import Optional
from fastapi import APIRouter, Query
from common.models import User, Session
from common.utils.errors import ResourceNotFoundException
from common.utils.http_exceptions import (InternalServerError, ResourceNotFound)
from schemas.session_schema import (GetSessionResponseModel, PostSessionModel,
                                    UpdateSessionModel,
                                    PostSessionResponseModel,
                                    UpdateSessionResponseModel,
                                    GetAllSessionResponseModel)
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ValidationErrorResponseModel)
# pylint: disable = broad-except

router = APIRouter(
    tags=["Session"],
    responses={
        500: {
            "model": InternalServerErrorResponseModel
        },
        422: {
            "model": ValidationErrorResponseModel
        }
    })


@router.get("/session", response_model=GetAllSessionResponseModel)
def get_sessions(user_id: str,
                 node_id: Optional[str] = None,
                 parent_session_id: Optional[str] = None,
                 skip: int = Query(0, ge=0, le=2000),
                 limit: int = Query(10, ge=1, le=100)):
  """Get all sessions based on user_id, node_id and/or parent_session_id

  Args:
      user_id(str): User Id for which sessions need to fetched.
      node_id(str): Node id of the node. Defaults to None.
      parent_session_id(str): Session id of the user. Defaults to None.
      skip (int): Number of objects to be skipped.
      limit (int): Size of session array to be returned.

  Returns:
      GetAllSessionResponseModel: Latest session for given criteria
  """
  try:
    sessions = Session.collection.filter("user_id", "==", user_id)
    if node_id is not None:
      sessions = sessions.filter("session_data.node_id", "==", node_id)
    if parent_session_id is not None:
      sessions = sessions.filter("parent_session_id", "==", parent_session_id)
    all_sessions = sessions.order("-last_modified_time").offset(
        skip).fetch(limit)
    all_sessions = [i.get_fields(reformat_datetime=True) for i in all_sessions]
    return {
        "success": True,
        "message": "Successfully fetched the sessions",
        "data": all_sessions
    }
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/session/latest",
    response_model=GetSessionResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_latest_session(user_id: str,
                       node_id: Optional[str] = None,
                       parent_session_id: Optional[str] = None):
  """Get latest session based on user_id, node_id and/or session_id

  Args:
      user_id(str): User Id for which sessions need to fetched
      node_id(str): Node id of the node. Defaults to None.
      parent_session_id(str): Session id of the user. Defaults to None.

  Returns:
      GetSessionResponseModel: Latest session for given criteria
  """
  try:
    sessions = Session.collection.filter("user_id", "==", user_id)
    if node_id is not None:
      sessions = sessions.filter("session_data.node_id", "==", node_id)
    if parent_session_id is not None:
      sessions = sessions.filter("parent_session_id", "==", parent_session_id)
    latest_session = sessions.order("-last_modified_time").get()
    if not latest_session:
      raise ResourceNotFoundException("No session found")
    return {
        "success": True,
        "message": "Successfully fetched latest session",
        "data": latest_session.get_fields(reformat_datetime=True)
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/session/{session_id}",
    response_model=GetSessionResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_session_for_given_id(session_id: str):
  """Gets session based on given session_id
     Raises ResourceNotFoundException if not found

  Args:
      session_id (str) : Unique id of the session

  Raises:
      ResourceNotFoundException: If the session does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      GetSessionResponseModel: Session Object
  """
  try:
    session = Session.find_by_uuid(session_id)

    session_fields = session.get_fields(reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully fetched the session",
        "data": session_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/session",
    response_model=PostSessionResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def create_session(input_session: PostSessionModel):
  """The create session endpoint will add the given session in
  request body to the firestore

  Args:
      input_session (PostSessionModel): input session to be inserted

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      PostSessionResponseModel: Session Object
  """
  try:
    # Check if learner or user exist
    new_session = Session()
    input_session_dict = {**input_session.dict()}
    User.find_by_uuid(input_session_dict["user_id"])

    new_session = new_session.from_dict(input_session_dict)
    new_session.session_id = ""

    new_session.save()
    new_session.session_id = new_session.id
    new_session.update()
    session_fields = new_session.get_fields(reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully created the session",
        "data": session_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/session/{session_id}",
    response_model=UpdateSessionResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_session(session_id: str, input_session: UpdateSessionModel):
  """Update a session with the session_id passed in the request body

  Args:
      session_id (str) : Unique id of the session
      input_session (UpdateSessionModel): Required body of the session

  Raises:
      ResourceNotFoundException: If the learner profile does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      UpdateSessionResponseModel: Session Object
  """
  try:
    existing_session = Session.find_by_uuid(session_id)

    input_session_dict = {**input_session.dict()}

    session_fields = existing_session.get_fields()

    for key, value in input_session_dict.items():
      session_fields[key] = value
    for key, value in session_fields.items():
      setattr(existing_session, key, value)

    existing_session.update()
    session_fields = existing_session.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully updated the session",
        "data": session_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
