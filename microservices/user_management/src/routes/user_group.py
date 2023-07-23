""" UserGroup endpoints """
import traceback
from fastapi import APIRouter, Query
from typing import Optional
from typing_extensions import Literal
from common.models import User, UserGroup, Action
from common.utils.logging_handler import Logger
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 ConflictError)
from common.utils.http_exceptions import (Conflict, InternalServerError,
                                          BadRequest, ResourceNotFound)
from common.utils.sorting_logic import collection_sorting
from schemas.user_group_schema import (
    AddUserToUserGroupResponseModel, AllUserGroupResponseModel,
    GetUserGroupResponseModel, PostUserGroupModel, PostUserGroupResponseModel,
    RemoveUserFromUserGroupResponseModel, UpdatePermissionsOfGroupResponseModel,
    UpdateUserGroupModel, UpdateUserGroupPermissions,ImmutableUserGroupModel,
    UpdateUserGroupResponseModel, DeleteUserGroup,
    AddUserFromUserGroupModel, UserGroupSearchResponseModel,
    RemoveUserFromUserGroupModel, GetUsersBasedOnGroupIdResponseModel,
    UpdateApplicationsOfGroupResponseModel, UpdateGroupApplications)
from schemas.error_schema import NotFoundErrorResponseModel
from services.collection_handler import CollectionHandler
from services.permissions import (update_permissions_with_user_group,
                                  validate_permission_with_application,
                                  filter_and_update_permissions_of_applications)
from config import ERROR_RESPONSES, IMMUTABLE_USER_GROUPS

router = APIRouter(tags=["UserGroup"], responses=ERROR_RESPONSES)


@router.get("/user-group/search", response_model=UserGroupSearchResponseModel)
def search_user_group(name: str):
  """Search for user group based on the name

    ### Args:
        name(str): Name of the user group. Defaults to None.

    ### Returns:
        GetGroupResponseModel: UserGroup object
    """
  try:
    result = []
    # fetch user group that matches name
    group = UserGroup.find_by_name(name)
    if group:
      result = [group.get_fields(reformat_datetime=True)]
    return {
        "success": True,
        "message": "Successfully fetched the user group",
        "data": result
    }
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
    "/user-groups",
    response_model=AllUserGroupResponseModel,
    name="Get all Groups")
def get_user_groups(skip: int = Query(0, ge=0, le=2000),
                    limit: int = Query(10, ge=1, le=100),
                    is_immutable: Optional[bool] = None,
                    fetch_tree: Optional[bool] = False,
                    sort_by: Optional[Literal["name", "created_time"]] =
                    "created_time",
                    sort_order: Optional[Literal["ascending", "descending"]] =
                    "descending"):
  """The get user groups endpoint will return an array of user groups from
  firestore

  ### Args:
      skip (int): Number of objects to be skipped
      limit (int): Size of user-group array to be returned
      sort_by (str): Data Model Fields name
      sort_order (str): ascending/descending
      fetch_tree (bool): To fetch the entire object
      instead of the UUID of the object

  ### Raises:
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      AllGroupResponseModel: Array of UserGroup Object
  """
  try:
    collection_manager = UserGroup.collection
    if is_immutable is not None:
      collection_manager = collection_manager.filter("is_immutable", "==",
                                                     is_immutable)

    total_user_groups= collection_manager.fetch()
    count = 0
    for idx, _ in enumerate(total_user_groups):
      count = idx + 1

    groups = collection_sorting(collection_manager=collection_manager,
                                sort_by=sort_by, sort_order=sort_order,
                                skip=skip, limit=limit)

    if fetch_tree:
      groups = [
          CollectionHandler.loads_field_data_from_collection(
              i.get_fields(reformat_datetime=True)) for i in groups
      ]
    else:
      groups = [i.get_fields(reformat_datetime=True) for i in groups]

    response = {"records": groups, "total_count": count}

    return {
        "success": True,
        "message": "Successfully fetched user groups",
        "data": response
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/user-group/{uuid}",
    response_model=GetUserGroupResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_user_group(uuid: str, fetch_tree: Optional[bool] = False):
  """The get user-group endpoint will return the user group from firestore of
  which uuid is provided

  ### Args:
      uuid (str): Unique identifier for user group
      fetch_tree (bool): To fetch the entire object
      instead of the UUID of the object

  ### Raises:
      ResourceNotFoundException: If the user group does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      GetGroupResponseModel: user group Object
  """
  try:
    group = UserGroup.find_by_uuid(uuid)
    if fetch_tree:
      group_fields = CollectionHandler.loads_field_data_from_collection(
          group.get_fields(reformat_datetime=True))
    else:
      group_fields = group.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully fetched the user group",
        "data": group_fields
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post("/user-group", response_model=PostUserGroupResponseModel)
def create_user_group(input_group: PostUserGroupModel):
  """The create user group endpoint will add the group in request body to the
  firestore

  ### Args:
      input_group (PostUserGroupModel): input user group to be inserted

  ### Raises:
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      PostGroupResponseModel: UserGroup Object
  """
  try:
    existing_group = UserGroup.find_by_name(input_group.name)
    if existing_group is not None:
      raise ConflictError(f"UserGroup with the given name: {input_group.name} "
                          "already exists")
    input_group_dict = {**input_group.dict()}
    new_group = UserGroup()
    new_group = new_group.from_dict({**input_group_dict, "users": []})
    new_group.uuid = ""
    new_group.save()
    new_group.uuid = new_group.id
    new_group.update()

    group_fields = new_group.get_fields(reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully created the user group",
        "data": group_fields
    }
  except ConflictError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise Conflict(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.put(
    "/user-group/{uuid}",
    response_model=UpdateUserGroupResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_user_group(uuid: str, input_group: UpdateUserGroupModel):
  """Update a user group with the uuid passed in the request body

  ### Args:
      input_group (UpdateGroupModel): Required body of the user group

  ### Raises:
      ResourceNotFoundException: If the user group does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      UpdateGroupResponseModel: UserGroup Object
  """
  try:
    existing_group = UserGroup.find_by_uuid(uuid)

    input_group_dict = {**input_group.dict(exclude_unset=True)}
    group_fields = existing_group.get_fields()

    if existing_group.is_immutable or \
      existing_group.name in IMMUTABLE_USER_GROUPS:
      if input_group_dict.get("name"):
        raise ValidationError(f"Cannot update name of an "
                              f"immutable Usergroup with uuid:{uuid}")

    for key, value in input_group_dict.items():
      if key == "name" and value is not None:
        _ = UserGroup.find_by_name(input_group_dict.get("name"))
        if _ is not None:
          raise ConflictError(f"UserGroup with the given name: "
                  f"{input_group_dict.get('name')} already exists")
      group_fields[key] = value
    for key, value in group_fields.items():
      setattr(existing_group, key, value)

    existing_group.update()
    group_fields = existing_group.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully updated the user group",
        "data": group_fields
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.delete(
    "/user-group/{uuid}",
    response_model=DeleteUserGroup,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_user_group(uuid: str):
  """Delete a user group with the given uuid from firestore

  ### Args:
      uuid (str): Unique id of the user group

  ### Raises:
      ResourceNotFoundException: If the user group does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      JSON: Success/Fail Message
  """
  try:
    group = UserGroup.find_by_uuid(uuid)

    group_fields = group.get_fields()

    if group.is_immutable or group.name in IMMUTABLE_USER_GROUPS:
      raise ValidationError(f"Cannot delete an "\
                          f"immutable Usergroup with uuid:{uuid}")

    CollectionHandler.remove_doc_from_all_references(
        uuid, "users", group_fields.get("users", []), "user_groups")
    CollectionHandler.remove_doc_from_all_references(
        uuid, "permissions", group_fields.get("permissions", []), "user_groups")
    UserGroup.collection.delete(group.key)

    return {"success": True, "message": "Successfully deleted the user group"}

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/user-group/{uuid}/users/add",
    response_model=AddUserToUserGroupResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def add_users_to_user_group(uuid: str,
                            input_users: AddUserFromUserGroupModel):
  """Add Users to the group with the uuid passed in the request body

  ### Args:
    input_group (UpdateGroupUsersModel): List of users to be added to the group

  ### Raises:
    ResourceNotFoundException: If the group or user does not exist
    Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      UpdateGroupResponseModel: UserGroup Object
  """
  try:
    input_users_dict = {**input_users.dict()}

    user_group = UserGroup.find_by_uuid(uuid)
    user_group_fields = user_group.get_fields()
    users_in_user_group = user_group_fields.get("users")

    input_users_dict["user_ids"] = set(input_users_dict.get("user_ids"))
    redundant_users = list(set(user_group.users) & input_users_dict["user_ids"])
    input_users_dict["user_ids"] = list(input_users_dict["user_ids"])
    if redundant_users:
      raise ValidationError(f"UserGroup with uuid {uuid} "\
              f"already contains users with uuids {','.join(redundant_users)}")

    validate_users_with_user_group = user_group.name in IMMUTABLE_USER_GROUPS

    user_data = []
    for user in input_users_dict.get("user_ids"):
      user = User.find_by_uuid(user)
      if validate_users_with_user_group \
      and not user.user_type == user_group.name:
        raise ValidationError(f"User with user_type {user.user_type} "\
                  f"cannot be added to user group: {user_group.name}")
      user_data.append(user)

    for user in user_data:
      user.user_groups.append(uuid)
      user.update()
      users_in_user_group.append(user.user_id)
    setattr(user_group, "users", users_in_user_group)
    user_group.update()
    user_group_fields = user_group.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully added users to user group",
        "data": user_group_fields
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/user-group/{uuid}/user/remove",
    response_model=RemoveUserFromUserGroupResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def remove_users_from_user_group(uuid: str,
                                 input_user: RemoveUserFromUserGroupModel):
  """Remove users from group with the uuid passed in the request body

  ### Args:
    input_group (UpdateGroupUsersModel): List of users to be added to the group

  ### Raises:
    ResourceNotFoundException: If the group does not exist
    Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      UpdateGroupResponseModel: UserGroup Object
  """
  try:
    input_user_id = {**input_user.dict()}.get("user_id")

    user_group = UserGroup.find_by_uuid(uuid)
    user_group_fields = user_group.get_fields()
    users_in_user_group = user_group_fields.get("users")
    if input_user_id not in users_in_user_group:
      raise ValidationError(f"UserGroup with uuid {uuid} "
          f"doesn't contain given user with uuid {input_user_id}")

    try:
      user = User.find_by_uuid(input_user_id)
      user_fields = user.get_fields()
      user_groups_of_user = user_fields.get("user_groups")

      if uuid in user_groups_of_user:
        user_groups_of_user.remove(uuid)
        setattr(user, "user_groups", user_groups_of_user)
        user.update()
    except ResourceNotFoundException:
      pass

    users_in_user_group.remove(input_user_id)

    setattr(user_group, "users", users_in_user_group)
    user_group.update()
    user_group_fields = user_group.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully removed user from user group",
        "data": user_group_fields
    }


  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.put(
    "/user-group/{uuid}/applications",
    response_model=UpdateApplicationsOfGroupResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_applications_of_user_group(
    uuid: str, input_group_applications: UpdateGroupApplications):
  """Assign/unassign applications of user group with the uuid passed in
     the request body

  ### Args:
      input_group_applications (UpdateGroupApplications): List of
                      users to be added to the user group

  ### Raises:
      ResourceNotFoundException: If the user group does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      UpdateApplicationsOfGroupResponseModel: UserGroup Object
  """
  try:
    existing_group = UserGroup.find_by_uuid(uuid)
    input_dict = {**input_group_applications.dict()}
    input_group_applications = input_dict.get("applications", [])
    CollectionHandler.validate_documents("applications",
                                         input_group_applications)
    group_fields = existing_group.get_fields(reformat_datetime=True)
    group_permissions = group_fields.get("permissions") if group_fields.get(
        "permissions") else []
    group_applications = group_fields.get("applications") if group_fields.get(
        "applications") else []

    added_applications = list(
        set(input_group_applications) - set(group_applications))
    permissions_to_add = []
    if len(added_applications) > 0:
      default_action_id = input_dict.get("action_id")
      _ = Action.find_by_uuid(default_action_id)
      for application in added_applications:
        permissions_to_add = filter_and_update_permissions_of_applications(
            application, uuid, "add", default_action_id)
        group_permissions += permissions_to_add
        group_applications.append(application)

    removed_applications = list(
        set(group_applications) - set(input_group_applications))
    if len(removed_applications) > 0:
      permissions_to_remove = []
      for application in removed_applications:
        permission_to_remove = filter_and_update_permissions_of_applications(
            application, uuid, "remove")
        permissions_to_remove += permission_to_remove
      group_permissions = list(
          set(group_permissions) - set(permissions_to_remove))
      group_applications = list(
          set(group_applications) - set(removed_applications))

    setattr(existing_group, "permissions", group_permissions)
    setattr(existing_group, "applications", group_applications)
    existing_group.update()
    group_fields = existing_group.get_fields(reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully updated applications of a user group",
        "data": group_fields
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/user-group/{uuid}/application/{application_uuid}/permissions",
    response_model=UpdatePermissionsOfGroupResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_permissions_of_user_group(
    uuid: str, application_uuid: str,
    input_application_permissions: UpdateUserGroupPermissions):
  """Assign/unassign permissions related to an application
      of user group with the uuid passed in the request body

  ### Args:
      input_application_permissions (UpdateUserGroupPermissions): Dict
      containing updated permissions of the application

  ### Raises:
      ResourceNotFoundException: If the user group does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      UpdatePermissionsOfGroupResponseModel: UserGroup Object
  """
  try:
    existing_group = UserGroup.find_by_uuid(uuid)
    input_dict = {**input_application_permissions.dict()}
    input_permissions = input_dict.get("permission_ids")

    group_fields = existing_group.get_fields(reformat_datetime=True)
    group_permissions = group_fields.get("permissions") if group_fields.get(
        "permissions") else []
    group_applications = group_fields.get("applications") if group_fields.get(
        "applications") else []

    if not application_uuid in group_applications:
      raise ValidationError(
          "UserGroup doesn't have access to the given application")

    CollectionHandler.get_document_from_collection("applications",
                                                   application_uuid)

    added_permissions = list(set(input_permissions) - set(group_permissions))
    permissions_to_add = []
    if len(added_permissions) > 0:
      for permission in added_permissions:
        permissions_to_add.append(
            validate_permission_with_application(permission, application_uuid))

      for permission in permissions_to_add:
        update_permissions_with_user_group(permission, uuid, "add")

      group_permissions += added_permissions

    removed_permissions = list(set(group_permissions) - set(input_permissions))
    removed_permissions_of_application = []
    permissions_to_remove = []
    if len(removed_permissions) > 0:
      for permission in removed_permissions:
        permission = validate_permission_with_application(
            permission, application_uuid, False)
        if permission:
          permissions_to_remove.append(permission)
      for permission in permissions_to_remove:
        update_permissions_with_user_group(permission, uuid, "remove")
        removed_permissions_of_application.append(permission.uuid)
      group_permissions = list(
          set(group_permissions) - set(removed_permissions_of_application))

    setattr(existing_group, "permissions", group_permissions)
    existing_group.update()
    group_fields = existing_group.get_fields(reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully updated permissions for " +
                   "the applcation of a user group",
        "data": group_fields
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e

@router.post("/user-group/immutable",
             include_in_schema= False,
             response_model=PostUserGroupResponseModel)
def create_immutable_user_group(input_group: ImmutableUserGroupModel):
  """The create immutable user group endpoint will
      add the immutable group in request body to the
  firestore

  ### Args:
      input_group (ImmutableUserGroupModel): input user group to be inserted

  ### Raises:
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      PostGroupResponseModel: UserGroup Object
  """
  try:
    existing_group = UserGroup.find_by_name(input_group.name)
    if existing_group is not None:
      raise ConflictError(f"UserGroup with the given name: {input_group.name} "
                          "already exists")
    input_group_dict = {**input_group.dict(), "is_immutable": True}
    new_group = UserGroup()
    new_group = new_group.from_dict({**input_group_dict, "users": []})
    new_group.uuid = ""
    new_group.save()
    new_group.uuid = new_group.id
    new_group.update()
    group_fields = new_group.get_fields(reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully created the user group",
        "data": group_fields
    }
  except ConflictError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise Conflict(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
    "/user-group/{uuid}/addable-users",
    response_model=GetUsersBasedOnGroupIdResponseModel,
    responses={404: {"model": NotFoundErrorResponseModel}},
)
def users_add_to_user_group(uuid: str):
  """Returns users that can be added to a particular user group

  ### Args:
    uuid (str): Unique ID for User Group

  ### Raises:
    ResourceNotFoundException: If the group does not exist
    Exception: 500 Internal Server Error if something goes wrong

  ### Returns:
      GetUsersBasedOnGroupIdResponseModel: Array of User Object
  """
  try:
    user_group = UserGroup.find_by_uuid(uuid)

    if user_group.is_immutable:
      users_list = User.collection.filter(
        "user_type", "==", user_group.name).filter(
        "is_deleted", "==", False).fetch()
    else:
      users_list = User.collection.filter("is_deleted", "==", False).fetch()

    result = [
      user.get_fields(reformat_datetime=True)
      for user in users_list if user.user_id not in user_group.users
    ]

    return {
      "success": True,
      "message": "Successfully fetched users "\
              "that can be added to user group",
      "data": result,
    }
  except ResourceNotFoundException as e:
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
