""" User endpoints """
import re
import traceback
import math

from concurrent.futures import ThreadPoolExecutor
from typing import Optional
from typing_extensions import Literal
from fastapi import APIRouter, UploadFile, File, Request, Query
from common.models import User, Staff, UserGroup
from common.utils.logging_handler import Logger
from common.utils.sorting_logic import collection_sorting
from common.utils.errors import ConflictError, ResourceNotFoundException, \
  ValidationError
from common.utils.http_exceptions import (Conflict, InternalServerError,
                                          BadRequest, ResourceNotFound)
from common.utils.inspace import (create_inspace_user_helper,
                                  get_inspace_user_helper,
                                  update_inspace_user_helper,
                                  delete_inspace_user_helper,
                                  is_inspace_enabled)
from common.utils.config import STAFF_USERS
from schemas.user_schema import (
  AllUserResponseModel, BasicUserModel, GetUserResponseModel, UserModel,
  PostUserResponseModel, UpdateUserModel, UpdateUserResponseModel, DeleteUser,
  UserSearchResponseModel, BulkImportUserResponseModel, UpdateStatusModel,
  GetApplicationsOfUser)
from schemas.staff_schema import UpdateStaffModel
from schemas.error_schema import NotFoundErrorResponseModel
from services.json_import import json_import, add_user_to_db
from services.collection_handler import CollectionHandler
from services.learner import (delete_learner, delete_learner_profile,
                              update_learner)
from services.staff import update_staff
from services.agent import delete_agent, get_agent, update_agent
from services.association_group_handler import (update_refs_for_user_by_type)
from config import ERROR_RESPONSES

# pylint: disable=unused-variable,no-value-for-parameter

router = APIRouter(tags=["User"], responses=ERROR_RESPONSES)


@router.get("/user/search/email", response_model=UserSearchResponseModel)
def search_user_by_email(email: str):
  """Search for users based on the user first name

  ### Args:
      email(str): Email id of the user.

  ### Returns:
      UserSearchResponseModel: List of user objects
  """
  try:
    result = []
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    email_match = re.compile(pattern=pattern)

    if not email_match.fullmatch(email):
      raise ValidationError(f"Invalid email ID format: {email}")

    user = User.find_by_email(email)
    if user:
      result = [user.get_fields(reformat_datetime=True)]
    return {
      "success": True,
      "message": "Successfully fetched the user",
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


@router.get("/user/search", response_model=UserSearchResponseModel)
def search_user(search_query: str,
                skip: int = Query(0, ge=0, le=2000),
                limit: int = Query(10, ge=1, le=100)):
  """Filter users based on the user email, first name and last name

  ### Args:
      search_query(str): key to search against email, first name and last name
      skip (int): Number of objects to be skipped
      limit (int): Size of group array to be returned

  ### Returns:
      UserSearchResponseModel: List of user objects
  """
  try:
    filtered_user_list = []
    users = User.collection.order("-created_time").filter(
      "is_deleted", "==", False).fetch()
    fetch_length = skip + limit
    for user in users:
      user_dict = user.get_fields(reformat_datetime=True)

      if search_query.lower() in user_dict["email"].lower():
        filtered_user_list.append(user_dict)

      elif search_query.lower() in user_dict["first_name"].lower():
        filtered_user_list.append(user_dict)

      elif search_query.lower() in user_dict["last_name"].lower():
        filtered_user_list.append(user_dict)

      if len(filtered_user_list) == fetch_length:
        break
    result = filtered_user_list[skip:fetch_length]
    return {
      "success": True,
      "message": "Successfully fetched the users",
      "data": result
    }
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get("/users", response_model=AllUserResponseModel, name="Get all Users")
def get_users(user_type: Optional[str] = None,
              skip: int = Query(0, ge=0, le=2000),
              limit: int = Query(10, ge=1, le=100),
              user_group: Optional[str] = None,
              fetch_tree: Optional[bool] = False,
              status: Optional[str] = None,
              sort_by: Optional[Literal["first_name", "last_name",
              "email", "created_time"]] = "created_time",
              sort_order: Optional[Literal["ascending", "descending"]] =
              "descending"):
  """The get users endpoint will return an array users from
  firestore

  ### Args:
      skip (int): Number of objects to be skipped
      limit (int): Size of user array to be returned
      user_group (str): To fetch the User belong to given group
      fetch_tree (bool): To fetch the entire
      object instead of the UUID of the object
      status (str): To fetch the user having given status (action or inactive)
      user_type (str): Type of the user example: faculty or learner etc.
      sort_by (str): sorting field name
      sort_order (str): ascending / descending

  ### Raises:
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      AllUserResponseModel: Array of User Object
  """
  try:
    collection_manager = User.collection.filter("is_deleted", "==", False)
    if user_type:
      collection_manager = collection_manager.filter("user_type", "==",
                                                     user_type)
    if user_group:
      collection_manager = collection_manager.filter("user_groups",
                                                     "array_contains",
                                                     user_group)
    if status is not None:
      collection_manager = collection_manager.filter("status", "==", status)

    total_users = collection_manager.fetch()
    count = 0
    for idx, i in enumerate(total_users):
      count = idx + 1

    users = collection_sorting(collection_manager=collection_manager,
                               sort_by=sort_by, sort_order=sort_order,
                               skip=skip, limit=limit)
    if fetch_tree:
      users = [
        CollectionHandler.loads_field_data_from_collection(
          i.get_fields(reformat_datetime=True)) for i in users
      ]
    else:
      users = [i.get_fields(reformat_datetime=True) for i in users]

    response = {"records": users, "total_count": count}

    return {
        "success": True,
        "message": "Data fetched successfully",
        "data": response
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
  "/user/{user_id}",
  response_model=GetUserResponseModel,
  responses={404: {
    "model": NotFoundErrorResponseModel
  }})
def get_user(user_id: str, fetch_tree: Optional[bool] = False):
  """The get user endpoint will return the user from firestore of
  which user_id is provided

  ### Args:
      user_id (str): Unique identifier for user
      fetch_tree (bool): To fetch the entire object
      instead of the UUID of the object

  ### Raises:
      ResourceNotFoundException: If the user does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      GetuserResponseModel: user Object
  """
  try:
    user = User.find_by_uuid(user_id)
    user_fields = user.get_fields(reformat_datetime=True)
    if fetch_tree:
      user_fields = CollectionHandler.loads_field_data_from_collection(
        user.get_fields(reformat_datetime=True))
    else:
      user_fields = user.get_fields(reformat_datetime=True)

    return {
      "success": True,
      "message": "Successfully fetched the user",
      "data": user_fields
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post("/user", response_model=PostUserResponseModel)
def create_user(input_user: UserModel, request: Request,
                create_inspace_user: Optional[bool] = False):
  """The create user endpoint will add the user in request body to the
  firestore.
  This endpoint also creates corresponding learner, learner_profile, agent
  and staff document based on the user_type or the user_group in which the
  user that is to be created is assigned.

  ### Args:
      input_user (UserModel): input user to be inserted
      create_inspace_user (bool): To create inspace user after
              GP-Core user creation

  ### Raises:
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      PostUserResponseModel: User Object
  """
  try:
    if not is_inspace_enabled(create_inspace_user):
      raise ValidationError("Inspace is disabled, please make "
                            "'create_inspace_user' as false in "
                            "the API request body")
    existing_user = User.find_by_email(input_user.email)
    if existing_user is not None:
      raise ConflictError(
          f"User with the given email: {input_user.email} "
          "already exists")
    input_user_dict = {**input_user.dict(),
                       "create_inspace_user": create_inspace_user}
    headers = {"Authorization": request.headers.get("Authorization")}
    user_id = add_user_to_db(headers, input_user_dict)
    new_user = User.find_by_id(user_id)

    response_message = "Successfully created User and corresponding agent"

    # ---- Inspace User creation ----
    if create_inspace_user:
      if create_inspace_user_helper(new_user):
        response_message = ("Successfully created new User, "
                            "corresponding agent and Inspace User")
      else:
        response_message = ("Successfully created User and "
                            "corresponding agent. Cannot create "
                            "Inspace User for current User")

      # fetch and return updated user
      new_user = User.find_by_id(user_id)
      user_fields = new_user.get_fields(reformat_datetime=True)
    else:
      user_fields = new_user.get_fields(reformat_datetime=True)

    return {
      "success": True,
      "message": response_message,
      "data": user_fields
    }
  except ConflictError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise Conflict(str(e)) from e
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.put(
  "/user/{user_id}",
  response_model=UpdateUserResponseModel,
  responses={404: {
    "model": NotFoundErrorResponseModel
  }})
def update_user(user_id: str,
                  input_user: UpdateUserModel,
                  request: Request,
                  update_inspace_user: Optional[bool] = False):
  """Update a user with the user_id passed in the request body

  ### Args:
      input_user (UserModel): Required body of the user

  ### Raises:
      ResourceNotFoundException: If the user does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      UpdateUserResponseModel: User Object
  """
  try:
    if not is_inspace_enabled(update_inspace_user):
      raise ValidationError("Inspace is disabled, please make "
                            "'update_inspace_user' as false in "
                            "the API request body")
    existing_user = User.find_by_uuid(user_id)

    input_user_dict = {**input_user.dict(exclude_unset=True)}
    user_fields = existing_user.get_fields()

    # update learner or staff based on user_type
    update_dict = {}
    agent_dict = {}
    first_name = input_user_dict.get("first_name")
    last_name = input_user_dict.get("last_name")

    if input_user_dict.get("email"):
      updated_email = input_user_dict.get("email")
      _ = User.find_by_email(updated_email)
      if _ is not None:
        raise ConflictError(
          f"User with the given email: {updated_email} "
          "already exists")

      if user_fields["user_type"] == "learner":
        update_dict["email_address"] = input_user_dict.get("email")
      elif user_fields["user_type"] in STAFF_USERS:
        update_dict["email"] = input_user_dict.get("email")

    if input_user_dict.get("user_groups"):
      for uuid in input_user_dict["user_groups"]:
        user_group = UserGroup.find_by_uuid(uuid)
        if user_group.is_immutable and \
          user_fields["user_type"] != user_group.name:
          raise ValidationError((f"User of user type {user_fields['user_type']}"
                                 f" cannot be assigned to User Group "
                                 f"{user_group.name} with uuid {uuid}"))

    if first_name:
      update_dict["first_name"] = first_name
      agent_dict["name"] = first_name
    else:
      agent_dict["name"] = user_fields["first_name"]
    if last_name:
      update_dict["last_name"] = last_name
      agent_dict["name"] += " " + last_name
    else:
      agent_dict["name"] += " " + user_fields["last_name"]

    if update_dict:
      headers = {"Authorization": request.headers.get("Authorization")}
      if user_fields["user_type"] == "learner":  # update learner
        learner_id = user_fields["user_type_ref"]
        update_learner(headers, learner_id, learner_dict=update_dict)
      elif user_fields["user_type"] in STAFF_USERS:  # update staff
        staff_id = user_fields["user_type_ref"]
        update_staff(staff_id, input_staff=UpdateStaffModel(**update_dict))

    for key, value in input_user_dict.items():
      if key == "user_groups" and user_fields.get("status") == "inactive":
        value = []
      elif key == "user_groups":
        value = CollectionHandler.update_existing_references(
            user_id, "user_groups", "users",
            input_user_dict.get("user_groups", []),
            user_fields.get("user_groups", []))

      if value is not None:
        user_fields[key] = value

    for key, value in user_fields.items():
      setattr(existing_user, key, value)

    existing_user.update()
    user_fields = existing_user.get_fields(reformat_datetime=True)

    response_msg = "Successfully updated the user"

    if first_name or last_name:
      # update agent
      agent_id = get_agent(headers, user_id)
      update_agent(headers, agent_id, agent_dict)

      if update_inspace_user:
        if existing_user.inspace_user["is_inspace_user"] is True:
          # update Inspace User
          update_payload = {}
          if first_name is not None:
            update_payload["firstName"] = first_name
          if last_name is not None:
            update_payload["lastName"] = last_name

          is_update_successful = update_inspace_user_helper(existing_user,
                                                            update_payload)

          if is_update_successful is True:
            response_msg = "Successfully updated the user and corresponding"
            response_msg += " Inspace user"
          else:
            response_msg = "Successfully updated the user but corresponding"
            response_msg += " Inspace user couldn't be updated"
    return {
      "success": True,
      "message": response_msg,
      "data": user_fields
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.delete(
  "/user/{user_id}",
  response_model=DeleteUser,
  responses={404: {
    "model": NotFoundErrorResponseModel
  }})
def delete_user(user_id: str,
                  request: Request,
                  delete_inspace_user: Optional[bool]=False):
  """Delete a user with the given user_id from firestore

  ### Args:
      user_id (str): Unique id of the user

  ### Raises:
      ResourceNotFoundException: If the user does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      JSON: Success/Fail Message
  """
  try:
    if not is_inspace_enabled(delete_inspace_user):
      raise ValidationError("Inspace is disabled, please make "
                            "'delete_inspace_user' as false in "
                            "the API request body")
    user = User.find_by_uuid(user_id)
    user_fields = user.get_fields()
    headers = {"Authorization": request.headers.get("Authorization")}
    if user_fields.get("user_type", "") == "learner":
      learner_id = user_fields.get("user_type_ref")
      delete_learner_profile(headers, learner_id)
      delete_learner(headers, learner_id)
    agent_id = get_agent(headers, user_id)
    delete_agent(headers, agent_id)
    update_refs_for_user_by_type(user)
    CollectionHandler.remove_doc_from_all_references(
      user_id, "user_groups", user_fields.get("user_groups", []), "users")
    if user_fields.get("user_type").lower() in STAFF_USERS:
      staff_uuid = user_fields.get("user_type_ref", "")
      Staff.delete_by_uuid(staff_uuid)

    response_msg = "Successfully deleted the user and associated agent, "
    response_msg += "learner/faculty"

    if delete_inspace_user:
      # Delete Inspace user
      if user.inspace_user["is_inspace_user"] is True:
        is_delete_successful = delete_inspace_user_helper(user)

        if is_delete_successful is True:
          response_msg = "Successfully deleted the user and associated agent, "
          response_msg += "learner/faculty and Inspace User"
        else:
          response_msg = "Successfully deleted the user and associated agent, "
          response_msg += "learner/faculty but could not delete Inspace User"

    User.delete_by_uuid(user_id)

    return {
      "success": True,
      "message": response_msg
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
  "/user/import/json",
  response_model=BulkImportUserResponseModel,
  name="Import User from JSON file")
def import_users(request: Request, json_file: UploadFile = File(...)):
  """Create user from json file

  ### Args:
    json_file (UploadFile): Upload json file consisting of user.
    json_schema should match UserModel

  ### Raises:
    Exception: 500 Internal Server Error if something fails

  ### Returns:
      LearnerImportJsonResponse: Array of uuid's
  """
  try:
    final_output = json_import(
      token={"Authorization": request.headers.get("Authorization")},
      json_file=json_file,
      json_schema=BasicUserModel,
      object_name="users")
    return final_output
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.put(
  "/user/{user_id}/status",
  response_model=UpdateUserResponseModel,
  responses={404: {
    "model": NotFoundErrorResponseModel
  }})
def update_user_status(user_id: str, input_status: UpdateStatusModel):
  """Change the status of a user with the user_id passed in the request body

  ### Args:
      input_status (UpdateStatusModel): Required body of the user

  ### Raises:
      ResourceNotFoundException: If the user does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      UpdateUserResponseModel: User Object
  """
  try:
    existing_user = User.find_by_uuid(user_id)

    input_user_dict = {**input_status.dict()}
    user_fields = existing_user.get_fields()
    if not input_user_dict["status"] == user_fields["status"]:
      if input_user_dict["status"] == "inactive":
        update_refs_for_user_by_type(existing_user)
        CollectionHandler.remove_doc_from_all_references(
          user_id, "user_groups", user_fields["user_groups"], "users")
        user_fields["user_groups"] = []
      user_fields["status"] = input_user_dict["status"]

    for key, value in user_fields.items():
      setattr(existing_user, key, value)

    existing_user.update()
    user_fields = existing_user.get_fields(reformat_datetime=True)

    return {
      "success": True,
      "message": "Successfully updated the user status",
      "data": user_fields
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
  "/user/{user_id}/applications",
  # include_in_schema=False,
  response_model=GetApplicationsOfUser,
  responses={404: {
    "model": NotFoundErrorResponseModel
  }})
def get_applications_assigned_to_user(user_id: str):
  """Get all applications for which the user has access

  ### Args:
      user_id: Unique identifier of the user

  ### Raises:
      ResourceNotFoundException: If the user does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      GetApplicationsOfUser: List of applications
  """
  try:
    user = CollectionHandler.get_document_from_collection("users", user_id)
    applications_assigned_to_user = []
    for user_group in user.get("user_groups", []):
      group = CollectionHandler. \
        get_document_from_collection("user_groups", user_group)
      applications_assigned_to_user += group.get("applications", [])
    applications_assigned_to_user = list(set(applications_assigned_to_user))
    response = []
    for i in applications_assigned_to_user:
      application = CollectionHandler. \
        get_document_from_collection("applications", i)
      response.append(application)

    return {
      "success": True,
      "message": "Successfully fetched applications assigned to the user",
      "data": {
        "applications": response
      }
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
  "/inspace/user/{user_id}",
  include_in_schema=False,
  response_model=PostUserResponseModel)
def create_inspace_user_account(user_id: str):
  """The create inspace user endpoint will create an Inspace user for an
      already existing GPCore user.

  ### Args:
      user_id (str): User id of the GPCore user for which Inspace User
                     is to be created

  ### Raises:
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      PostUserResponseModel: User Object
  """
  try:
    if not is_inspace_enabled():
      raise ValidationError("you don't have permission to access this endpoint")
    user = User.find_by_user_id(user_id)

    allowed_inspace_user_types = ["learner"]
    allowed_inspace_user_types.extend(STAFF_USERS)

    if user.user_type not in allowed_inspace_user_types:
      inspace_mapping = {
        "is_inspace_user": False,
        "inspace_user_id": ""
      }
      user.inspace_user = inspace_mapping
      user.update()
      raise ValidationError("Cannot create Inspace user for user"
                            f" of type {user.user_type}")

    if (user.inspace_user is None or
        user.inspace_user.get("is_inspace_user") is False):
      inspace_mapping = {
        "is_inspace_user": True,
        "inspace_user_id": ""
      }
      user.inspace_user = inspace_mapping
      user.update()
    elif (user.inspace_user.get("is_inspace_user") is True and
          user.inspace_user.get("inspace_user_id") != ""):
      raise ConflictError("Inspace User already exists for current user")

    # ---- Try fetching Inspace User
    status_code, inspace_user_res = get_inspace_user_helper(user)
    if status_code == 200:
      inspace_mapping = {
        "is_inspace_user": True,
        "inspace_user_id": inspace_user_res["inspaceUser"]["id"]
      }
      user.inspace_user = inspace_mapping
      user.update()
      response_message = "Successfully updated Inspace User id for current user"
    elif status_code == 404:
      # ---- Inspace User creation if user doesn't exist----
      if create_inspace_user_helper(user):
        response_message = "Successfully created Inspace User for current user"
      else:
        response_message = "Cannot create Inspace User for current User"

    # fetch and return updated user
    user = User.find_by_user_id(user_id)
    user_fields = user.get_fields(reformat_datetime=True)

    return {
      "success": True,
      "message": response_message,
      "data": user_fields
    }
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ConflictError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise Conflict(str(e)) from e
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post("/non-exist/inspace/user", include_in_schema=False)
def update_inspace_user_field(skip: Optional[int]=0, limit: Optional[int]=100):
  """
  Update Inspace User Field Value
  """
  try:
    if not is_inspace_enabled():
      raise ValidationError("you don't have permission to access this endpoint")
    # ids for which inspace user was created
    created_inspace_users = []
    # ids for which inspace user creation failed
    failed_user_ids = []
    # fields where inspace mapping was set as True
    inspace_users = []
    # fields where inspace mapping was set as False
    non_inspace_users = []
    # users for which inspace user already exists
    already_created_inspace_users = []
    # users whose document was not modified
    non_modified_users = []
    response_message = ""
    allowed_inspace_user_types = ["learner"]
    allowed_inspace_user_types.extend(STAFF_USERS)

    users = User.collection.order("-created_time").filter(
      "is_deleted", "==", False).offset(skip).fetch(limit)

    for user in users:
      if user.inspace_user is None:
        if user.user_type in allowed_inspace_user_types:
          user.inspace_user = {"is_inspace_user": True, "inspace_user_id": ""}
          user.update()
          inspace_users.append(user.user_id)
        else:
          user.inspace_user = {"is_inspace_user": False, "inspace_user_id": ""}
          user.update()
          non_inspace_users.append(user.user_id)

    users = User.collection.order("-created_time").filter(
      "is_deleted", "==", False).offset(skip).fetch(limit)

    for user in users:
      if user.user_type in allowed_inspace_user_types:
        try:
          if user.inspace_user.get("is_inspace_user") is False:
            non_modified_users.append(user.user_id)

          elif (user.inspace_user.get("is_inspace_user") is True
            and user.inspace_user.get("inspace_user_id") == ""):
            # ---- Inspace User creation ----
            response_message = create_inspace_user_helper(user)
            if response_message:
              Logger.info(f"Inspace User Created for {user.user_id}")
              created_inspace_users.append(user.user_id)

          else:
            already_created_inspace_users.append(user.user_id)

        except Exception as e:
          Logger.error(e)
          Logger.error(traceback.print_exc())
          failed_user_ids.append(user.user_id)

      else:
        non_modified_users.append(user.user_id)

    return {
        "success": True,
        "message": response_message,
        "data": {
            "created_inspace_users": created_inspace_users,
            "failed_inspace_user_creation": failed_user_ids,
            "inspace_users_true": inspace_users,
            "inspace_users_false": non_inspace_users,
            "non_modified_users": non_modified_users,
            "already_created_inspace_users": already_created_inspace_users
        }
    }
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post("/user/add-is-deleted", include_in_schema=False)
def update_user_documents():
  """This endpoint will add the is_deleted field in User documents where it
      doesn't exist.

  ### Raises:
      Exception: 500 Internal Server Error if something went wrong
  """
  try:
    users = list(User.collection.order("-created_time").fetch())

    # list of user documents which are updated with the is_deleted field
    updated_users = []

    # total count of all user records
    user_count = 0
    for i in enumerate(users):
      user_count+=1

    # calculate number of workers required (100 docs per worker)
    workers = math.ceil(user_count / 100)

    # function to update the document
    def update_field(user_list):
      for user in user_list:
        if user.is_deleted is None:
          user.is_deleted = False
          user.update()
          Logger.info(f"Updated {user.user_id}: is_deleted={user.is_deleted}")
          updated_users.append(user.user_id)
        else:
          Logger.info(f"{user.user_id}: is_deleted={user.is_deleted}")

    # initialize executor
    executor = ThreadPoolExecutor(max_workers=workers)

    for i in range(workers):
      executor.submit(update_field, users[i*100:(i+1)*100])

    executor.shutdown(wait=True)

    return {
      "success": True,
      "message": "Successfully added the is_deleted field for following users",
      "data": {
        "updated_users": updated_users
      }
    }
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
