""" Permission endpoints """
from operator import itemgetter
import traceback
from fastapi import APIRouter, Query
from typing import Optional
from typing_extensions import Literal
from iteration_utilities import unique_everseen
from common.models import Permission, Application, Module, Action, UserGroup
from common.utils.logging_handler import Logger
from common.utils.errors import ResourceNotFoundException, ValidationError
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound)
from common.utils.sorting_logic import sort_records
from schemas.permission_schema import (
    AllPermissionResponseModel, GetPermissionResponseModel,
    PermissionFilerUniqueResponseModel, PermissionModel,
    PostPermissionResponseModel, UpdatePermissionModel,
    UpdatePermissionResponseModel, DeletePermission)
from schemas.error_schema import NotFoundErrorResponseModel
from services.collection_handler import CollectionHandler
from services.permissions import get_unique_records
from services.helper import get_data_for_fetch_tree
from config import ERROR_RESPONSES

router = APIRouter(tags=["Permission"], responses=ERROR_RESPONSES)


@router.get("/permission/search", response_model=AllPermissionResponseModel)
def search_permission(search_query: str,
                      skip: int = Query(0, ge=0, le=2000),
                      limit: int = Query(10, ge=1, le=100)) -> dict:
  """
  Endpoint to search permission
  parameters
  ----------
  search_query: str
  skip: int
  limit: int
  Returns
  -------
  Permission: dict
  Raise
  -----
  Exception: 500 Internal Server Error
  """
  try:
    res = []
    fetch_length = skip + limit
    data = Permission.collection.order("-created_time").fetch()
    permissions = [CollectionHandler.loads_field_data_from_collection(
        i.get_fields(reformat_datetime=True)) for i in data]

    for permission in permissions:
      if search_query.lower() in permission["name"].lower():
        res.append(permission)
      if search_query.lower() in permission["application_id"]["name"].lower():
        res.append(permission)
      if search_query.lower() in permission["module_id"]["name"].lower():
        res.append(permission)
      if search_query.lower() in permission["action_id"]["name"].lower():
        res.append(permission)
      if permission["user_groups"]:
        if [i for i in permission["user_groups"] if search_query.lower() in
                                                    i["name"].lower()]:
          res.append(permission)

      res = list(unique_everseen(res))

      if len(res) == fetch_length:
        break
    count = 10000
    response = {"records": res[skip:fetch_length], "total_count": count}
    return {
      "success": True,
      "message": "Successfully fetched the permissions",
      "data": response
    }
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e

@router.get(
    "/permissions",
    response_model=AllPermissionResponseModel,
    name="Get Permissions")
def get_permissions(skip: int = Query(None, ge=0, le=2000),
                      limit: int = Query(None, ge=1, le=100),
                      application_ids: Optional[str] = None,
                      module_ids: Optional[str] = None,
                      action_ids: Optional[str] = None,
                      user_groups: Optional[str] = None,
                      fetch_tree: Optional[bool] = False,
                      sort_by: Optional[Literal["application", "module",
                        "action", "user_groups","created_time"]]
                        = "created_time",
                      sort_order: Optional[Literal["ascending", "descending"]]
                        = "descending"):
  """The get permissions endpoint will fetch the permissions
     matching the values in request body from firestore

  ### Args:
      skip (int): Number of objects to be skipped
      limit (int): Size of user array to be returned
      application_ids (str): Application id which is to be filtered
      module_ids (str): Module id which is to be filtered
      action_ids (str): Action id which is to be filtered
      user_groups (str): User groups to be filtered
      fetch_tree (bool): To fetch the entire object
      instead of the UUID of the object
      sort_by (str): sorting field name
      sort_order (str): ascending / descending

  ### Raises:
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      AllPermissionResponseModel: Array of Permission Object
  """
  try:
    collection_manager = Permission.collection

    filtered_list = []
    if application_ids is not None or module_ids is not None or\
      action_ids is not None or user_groups is not None:
      input_permission_dict = {
        "application_id": application_ids,
        "module_id": module_ids,
        "action_id": action_ids,
        "user_groups": [ug.strip() for ug in user_groups.split(",")]
                          if user_groups is not None else None
      }

      fetch_length = skip + limit
      permissions = list(Permission.collection.order("-created_time").fetch())
      permissions_with_fields = [
        i.get_fields(reformat_datetime=True) for i in permissions
      ]

      # filter permissions
      for idx, permission in enumerate(permissions_with_fields):
        match = True
        for key, value in input_permission_dict.items():
          if value is not None:
            if isinstance(value,list):
              if not any(item in permission[key] for item in value):
                match = False
                break
            elif permission[key] not in value:
              match = False
              break
        if match:
          filtered_list.append(permissions[idx])
        if len(filtered_list) == fetch_length:
          break
      filtered_list = filtered_list[skip:fetch_length]
    else:
      filtered_list = collection_manager.order("-created_time").offset(skip).\
        fetch(limit)

    if fetch_tree:
      filtered_list = get_data_for_fetch_tree(filtered_list)
      # sort permissions
      if sort_by in ["application", "module", "action"]:
        filtered_list = sort_records(sort_by="name",sort_order=sort_order,
                                    records=filtered_list, key=sort_by+"_id")
      elif sort_by == "user_groups":
        reverse = sort_order == "descending"
        # Sort user_groups array within each record
        for record in filtered_list:
          record["user_groups"] = sorted(record["user_groups"],key=itemgetter(
                                          "name"),reverse=reverse)

        # Sort user_groups array across all records
        filtered_list = sorted(filtered_list, key=lambda x:(itemgetter("name")\
         (x["user_groups"][0])) if x["user_groups"] else "" ,reverse=reverse)
    else:
      filtered_list = [i.get_fields(reformat_datetime=True) for i in
                        filtered_list]

    count = 10000
    response = {"records": filtered_list, "total_count": count}
    return {
        "success": True,
        "message": "Data fetched successfully",
        "data": response
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e

@router.get(
    "/permission/{uuid}",
    response_model=GetPermissionResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_permission(uuid: str, fetch_tree: Optional[bool] = False):
  """The get permission endpoint will return the permission from firestore of
  which uuid is provided

  ### Args:
      uuid (str): Unique identifier for permission
      fetch_tree (bool): To fetch the entire object
      instead of the UUID of the object

  ### Raises:
      ResourceNotFoundException: If the permission does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      GetPermissionResponseModel: permission Object
  """
  try:
    permission = Permission.find_by_uuid(uuid)
    if fetch_tree:
      permission_fields = CollectionHandler.loads_field_data_from_collection(
          permission.get_fields(reformat_datetime=True))
    else:
      permission_fields = permission.get_fields(reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully fetched the permission",
        "data": permission_fields
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post("/permission", response_model=PostPermissionResponseModel)
def create_permission(input_permission: PermissionModel):
  """The create permission endpoint will add the permission in request body to
  firestore

  ### Args:
      input_permission (PermissionModel): input permission to be inserted

  ### Raises:
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      PostPermissionResponseModel: Permission Object
  """
  permission_fields = None
  try:
    input_permission_dict = {**input_permission.dict()}
    if CollectionHandler.get_document_from_collection("applications",
                            input_permission_dict["application_id"]) and\
      CollectionHandler.get_document_from_collection("modules",
                            input_permission_dict["module_id"]) and\
      CollectionHandler.get_document_from_collection("actions",
                            input_permission_dict["action_id"]):

      new_permission = Permission()
      new_permission = new_permission.from_dict(input_permission_dict)
      new_permission.uuid = ""
      new_permission.save()
      new_permission.uuid = new_permission.id
      new_permission.update()

      permission_fields = new_permission.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully created the permission",
        "data": permission_fields
    }

  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.put(
    "/permission/{uuid}",
    response_model=UpdatePermissionResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_permission(uuid: str, input_permission: UpdatePermissionModel):
  """Update a permission with the uuid passed in the request body

  ### Args:
      input_permission (PermissionModel): Required body of the permission

  ### Raises:
      ResourceNotFoundException: If the permission does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      UpdatePermissionResponseModel: Permission Object
  """
  try:
    existing_permission = Permission.find_by_uuid(uuid)

    input_permission_dict = {**input_permission.dict()}
    permission_fields = existing_permission.get_fields()

    for key, value in input_permission_dict.items():
      permission_fields[key] = value
    for key, value in permission_fields.items():
      setattr(existing_permission, key, value)

    existing_permission.update()
    permission_fields = existing_permission.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully updated the permission",
        "data": permission_fields
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
    "/permission/{uuid}",
    response_model=DeletePermission,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_permission(uuid: str):
  """Delete a permission with the given uuid from firestore

  ### Args:
      uuid (str): Unique id of the permission

  ### Raises:
      ResourceNotFoundException: If the permission does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      JSON: Success/Fail Message
  """
  try:
    permission = Permission.find_by_uuid(uuid)
    permission_fields = permission.get_fields()
    CollectionHandler.remove_doc_from_all_references(
        uuid, "user_groups", permission_fields.get("user_groups", []),
        "permissions")
    Permission.collection.delete(permission.key)

    return {"success": True, "message": "Successfully deleted the permission"}

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e

@router.get(
    "/permission_filter/unique",
    response_model=PermissionFilerUniqueResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_permission_filters_unique(application: Optional[str] = None,
                                  module: Optional[str] = None,
                                  action: Optional[str] = None,
                                  user_group: Optional[str] = None):
  """The get unique permission endpoint will return an array
  of unique values for applications, modules, actions and user groups from
  firestore

  ### Query:
      application: uuid of application that needs to be filtered
      module: uuid of module that needs to be filtered
      action: uuid of action that needs to be filtered
      user_group: uuid of user_group that needs to be filtered

  ### Raises:
      ResourceNotFoundException: 404 If the permission does not exist
      Exception: 500 Internal Server Error if something went wrong
      ValidationError: If filter length is more than 30 for any query param

  ### Returns:
      Dict containing list of unique filters for applications,
      modules, actions and user groups
  """
  try:
    permission_collection = Permission.collection
    unique_record_keys = ["uuid","name"]

    filter_limit_30_reached = False

    application_uuid_list = module_uuid_list = None
    action_uuid_list = user_group_uuid_list = None
    if application:
      application_uuid_list = application.split(",")
      if len(application_uuid_list) > 30:
        filter_limit_30_reached = True
      else:
        permission_collection = permission_collection.filter(
          "application_id", "in", application_uuid_list)
    if module:
      module_uuid_list = module.split(",")
      if len(module_uuid_list) > 30:
        filter_limit_30_reached = True
      else:
        permission_collection = permission_collection.filter(
          "module_id", "in", module_uuid_list)
    if action:
      action_uuid_list = action.split(",")
      if len(action_uuid_list) > 30:
        filter_limit_30_reached = True
      else:
        permission_collection = permission_collection.filter(
          "action_id", "in", action_uuid_list)
    if user_group:
      user_group_uuid_list = user_group.split(",")
      if len(user_group_uuid_list) > 30:
        filter_limit_30_reached = True
      else:
        permission_collection = permission_collection.filter(
          "user_groups", "array_contains_any", user_group_uuid_list)

    if filter_limit_30_reached:
      raise ValidationError(str("Filter has a limit of 30 values"))

    final_data = permission_collection.fetch()
    application_id_list = []
    module_id_list = []
    action_id_list = []
    user_group_id_list = []
    for each in final_data:
      application_id_list.append(each.get_fields()["application_id"])
      module_id_list.append(each.get_fields()["module_id"])
      action_id_list.append(each.get_fields()["action_id"])
      user_group_id_list.extend(each.get_fields()["user_groups"])

    if not application_id_list:
      unique_applications = []
    else:
      unique_applications = get_unique_records(
        Application.collection.filter(
        "uuid", "in", application_id_list).fetch(),unique_record_keys)

    if not module_id_list:
      unique_modules = []
    else:
      unique_modules = get_unique_records(
        Module.collection.filter(
        "uuid", "in", module_id_list).fetch(),unique_record_keys)

    if not action_id_list:
      unique_actions = []
    else:
      unique_actions = get_unique_records(
        Action.collection.filter(
        "uuid", "in", action_id_list).fetch(),unique_record_keys)

    if not user_group_id_list:
      unique_user_groups = []
    else:
      unique_user_groups = get_unique_records(
        UserGroup.collection.filter(
        "uuid", "in",user_group_id_list).fetch(),unique_record_keys)

    return {
      "success": True,
      "message": "Successfully fetched the unique values for " + \
        "applications, modules, actions and user_groups.",
      "data": {
          "applications": unique_applications,
          "modules": unique_modules,
          "actions": unique_actions,
          "user_groups": unique_user_groups
        }
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
