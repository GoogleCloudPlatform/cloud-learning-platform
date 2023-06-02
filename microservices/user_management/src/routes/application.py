""" application endpoints """
from fastapi import APIRouter, Query
from typing import Optional
from common.models import Application, Module
from common.utils.errors import ResourceNotFoundException, ValidationError, ConflictError
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound,Conflict)
from services.permissions import get_permissions_based_on_application
from services.collection_handler import CollectionHandler
from schemas.application_schema import (
    PostApplicationResponseModel, ApplicationModel,
    DeleteApplicationResponseModel, AllApplicationResponseModel,
    UpdateApplicationModel, UpdateApplicationResponseModel,
    GetApplicationResponseModel)
from schemas.error_schema import NotFoundErrorResponseModel
from config import ERROR_RESPONSES

router = APIRouter(tags=["Application"], responses=ERROR_RESPONSES)


@router.get(
    "/applications",
    response_model=AllApplicationResponseModel,
    name="Get all applications")
def get_all_applications(skip: int = Query(0, ge=0, le=2000),
                         limit: int = Query(10, ge=1, le=100),
                         fetch_tree: Optional[bool] = False):
  """The get applications endpoint will return an array applications from
  firestore

  ### Args:
      skip (int): Number of objects to be skipped
      limit (int): Size of application array to be returned
      fetch_tree (bool): To fetch the entire object instead
      of the UUID of the object

  ### Raises:
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      AllModuleResponseModel: Array of application Object
  """
  try:
    collection_manager = Application.collection
    applications = collection_manager.order("-created_time").offset(
        skip).fetch(limit)
    if fetch_tree:
      applications = [
          CollectionHandler.loads_field_data_from_collection(
              i.get_fields(reformat_datetime=True)) for i in applications
      ]
    else:
      applications = [
          i.get_fields(reformat_datetime=True) for i in applications
      ]
    return {
        "success": True,
        "message": "Data fetched successfully",
        "data": applications
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/application/{uuid}",
    response_model=GetApplicationResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_application(uuid: str, fetch_tree: Optional[bool] = False):
  """The get application endpoint will return the application from firestore of
  which uuid is provided

  ### Args:
      uuid (str): Unique identifier for application
      fetch_tree (bool): To fetch the entire object instead
      of the UUID of the object

  ### Raises:
      ResourceNotFoundException: If the application does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      GetApplicationResponseModel: application Object
  """
  try:
    application = Application.find_by_uuid(uuid)
    if fetch_tree:
      application_fields = CollectionHandler.loads_field_data_from_collection(
          application.get_fields(reformat_datetime=True))
    else:
      application_fields = application.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully fetched the application",
        "data": application_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post("/application", response_model=PostApplicationResponseModel)
def create_application(input_data: ApplicationModel):
  """The create application endpoint will add the application
   in request body to the firestore

  ### Args:
      input_application (ApplicationModel): input application to be inserted
      name : Unique for every application

  ### Raises:
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      PostApplicationResponseModel: Application Object
  """
  try:
    existing_application = Application.find_by_name(input_data.name)
    if existing_application is not None:
      raise ConflictError(
        f"Application with the given name: {input_data.name} "
        "already exists")

    input_application_dict = {**input_data.dict()}

    # module validation
    if "modules" in input_application_dict and input_data.modules != []:
      for module in input_data.modules:
        Module.find_by_uuid(uuid=module)

    new_application = Application()
    new_application = new_application.from_dict(input_application_dict)
    new_application.uuid = ""
    new_application.save()
    new_application.uuid = new_application.id
    new_application.update()
    # TODO: uncomment below line to create permissions
    # create_permissions_for_application(
    #     input_application_dict.get("modules", []), new_application.uuid,
    #     new_application.name)
    application_fields = new_application.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully created the application",
        "data": application_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ConflictError as e:
    raise Conflict(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/application/{uuid}",
    response_model=UpdateApplicationResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_application(uuid: str, input_application: UpdateApplicationModel):
  """Update a application with the uuid passed in the request body

  ### Args:
      input_application (ApplicationModel): Required body of the application
      name : Unique for every application

  ### Raises:
      ResourceNotFoundException: If the application does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      UpdateApplicationResponseModel: Application Object
  """
  try:
    existing_application = Application.find_by_name(input_application.name)
    if existing_application is not None:
      raise ConflictError(
        f"Application with the given name: {input_application.name} "
        "already exists")

    input_application_dict = {**input_application.dict()}

    if "modules" in input_application_dict and input_application.modules != []:
      for module in input_application.modules:
        Module.find_by_uuid(uuid=module)

    existing_application = Application.find_by_uuid(uuid)

    application_fields = existing_application.get_fields()

    for key, value in input_application_dict.items():
      application_fields[key] = value
    for key, value in application_fields.items():
      setattr(existing_application, key, value)

    existing_application.update()
    application_fields = existing_application.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully updated the application",
        "data": application_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/application/{uuid}",
    response_model=DeleteApplicationResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_application(uuid: str):
  """Delete a application with the given uuid from firestore

  ### Args:
      uuid (str): Unique id of the application

  ### Raises:
      ResourceNotFoundException: If the application does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      JSON: Success/Fail Message
  """
  try:
    application = Application.find_by_uuid(uuid)
    #TODO:update permissions of application in user_group

    user_groups,permissions = get_permissions_based_on_application(uuid)
    for user_group in user_groups:
      user_group = CollectionHandler.get_document_from_collection("user_groups",
                                                            user_group, False)
      user_group_dict = user_group.get_fields()
      if uuid in user_group_dict.get("applications"):
        user_group_dict.get("applications").remove(uuid)
        user_group_dict["permissions"] = list(
          set(user_group_dict.get("permissions")) - set(permissions))
      setattr(user_group,"applications",user_group_dict["applications"])
      setattr(user_group,"permissions",user_group_dict["permissions"])
      user_group.update()
    Application.collection.delete(application.key)

    return {"success": True, "message": "Successfully deleted the application"}

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
