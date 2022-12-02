# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" User endpoints """
import datetime
from fastapi import APIRouter
from google.api_core.exceptions import PermissionDenied
from common.models import User
from common.utils.logging_handler import Logger
from common.utils.errors import ResourceNotFoundException
from common.utils.http_exceptions import ResourceNotFound, InternalServerError, Conflict
from schemas.user import UserModel
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ConflictResponseModel,
                                  ValidationErrorResponseModel)

router = APIRouter(prefix="/users",
                   tags=["Users"],
                   responses={
                       500: {
                           "model": InternalServerErrorResponseModel
                       },
                       404: {
                           "model": NotFoundErrorResponseModel
                       },
                       409: {
                           "model": ConflictResponseModel
                       },
                       422: {
                           "model": ValidationErrorResponseModel
                       }
                   })

SUCCESS_RESPONSE = {"status": "Success"}
FAILED_RESPONSE = {"status": "Failed"}


@router.get("/{user_id}", response_model=UserModel)
def get_user(user_id: str):
  """Get a user

  Args:
    user_id (str): unique id of the user

  Raises:
    ResourceNotFoundException: If the user does not exist
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [user]: user object for the provided user id
  """
  try:
    user = User.find_by_uuid(user_id)
    if user is None:
      raise ResourceNotFoundException(f"User with uuid {user_id} is not found")
    else:
      return user
  except ResourceNotFoundException as re:
    raise ResourceNotFound(str(re)) from re
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post("")
def create_user(input_user: UserModel):
  """Register a user

  Args:
    input_user (UserModel): Required body of the user

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: user ID of the user if the user is successfully created,
    InternalServerErrorResponseModel if the user creation raises an exception
  """
  existing_user = None
  try:
    new_user = User()
    input_user_dict = {**input_user.dict()}
    new_user = new_user.from_dict(input_user_dict)
    existing_user = User.find_by_email(input_user_dict["email"])
  except Exception as e:
    raise InternalServerError(str(e)) from e
  if existing_user is not None:
    raise Conflict()
  try:
    timestamp = datetime.datetime.utcnow()
    new_user.created_timestamp = timestamp
    new_user.last_updated_timestamp = timestamp
    new_user.save()
    new_user.uuid = new_user.id
    new_user.update()
    return new_user.uuid
  except PermissionDenied as e:
    # Firestore auth misconfigured usually
    Logger.error(e)
    raise InternalServerError(str(e)) from e
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.put("")
def update_user(input_user: UserModel):
  """Update a user

  Args:
    input_user (UserModel): Required body of the user

  Raises:
    ResourceNotFoundException: If the User does not exist
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: {'status': 'Succeed'} if the user is updated,
    NotFoundErrorResponseModel if the user not found,
    InternalServerErrorResponseModel if the user updation raises an exception
  """
  try:
    user = User()
    input_user_dict = {**input_user.dict()}
    user = user.from_dict(input_user_dict)
    existing_user = User.find_by_uuid(input_user_dict["uuid"])
    if existing_user is None:
      raise ResourceNotFoundException(
          f'User with uuid {input_user_dict["uuid"]} is not found')
    timestamp = datetime.datetime.utcnow()
    user.last_updated_timestamp = timestamp
    user.created_timestamp = existing_user.created_timestamp
    user.update(existing_user.id)
    return SUCCESS_RESPONSE
  except ResourceNotFoundException as re:
    raise ResourceNotFound(str(re)) from re
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete("/{user_id}")
def delete_user(user_id: str):
  """Delete a user

  Args:
    user_id (str): unique id of the user

  Raises:
    ResourceNotFoundException: If the User does not exist
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: {'status': 'Succeed'} if the user is deleted,
    NotFoundErrorResponseModel if the user not found,
    InternalServerErrorResponseModel if the user deletion raises an exception
  """
  try:
    if User.archive_by_uuid(user_id):
      return SUCCESS_RESPONSE
    else:
      raise ResourceNotFoundException(f"User with uuid {user_id} is not found")
  except ResourceNotFoundException as re:
    raise ResourceNotFound(str(re)) from re
  except Exception as e:
    raise InternalServerError(str(e)) from e
