""" Module endpoints """
from fastapi import APIRouter, Query
from typing import Optional
from common.models import Module, Action
from common.utils.errors import ResourceNotFoundException, ValidationError, \
  ConflictError
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound)
from schemas.module_schema import (AllModuleResponseModel,
                                   GetModuleResponseModel, ModuleModel,
                                   PostModuleResponseModel, UpdateModuleModel,
                                   UpdateModuleResponseModel, DeleteModule)
from schemas.error_schema import NotFoundErrorResponseModel
from services.collection_handler import CollectionHandler
from config import ERROR_RESPONSES

router = APIRouter(tags=["Module"], responses=ERROR_RESPONSES)


@router.get(
    "/modules", response_model=AllModuleResponseModel, name="Get all Modules")
def get_modules(skip: int = Query(0, ge=0, le=2000),
                limit: int = Query(10, ge=1, le=100),
                fetch_tree: Optional[bool] = False):
  """The get modules endpoint will return an array modules from
  firestore

  ### Args:
      skip (int): Number of objects to be skipped
      limit (int): Size of module array to be returned
      fetch_tree (bool): To fetch the entire object instead
      of the UUID of the object

  ### Raises:
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      AllModuleResponseModel: Array of Module Object
  """
  try:
    collection_manager = Module.collection
    modules = collection_manager.order("-created_time").offset(
        skip).fetch(limit)
    if fetch_tree:
      modules = [
          CollectionHandler.loads_field_data_from_collection(
              i.get_fields(reformat_datetime=True)) for i in modules
      ]
    else:
      modules = [i.get_fields(reformat_datetime=True) for i in modules]
    return {
        "success": True,
        "message": "Data fetched successfully",
        "data": modules
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/module/{uuid}",
    response_model=GetModuleResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_module(uuid: str, fetch_tree: Optional[bool] = False):
  """The get module endpoint will return the module from firestore of
  which uuid is provided

  ### Args:
      uuid (str): Unique identifier for module
      fetch_tree (bool): To fetch the entire object instead
      of the UUID of the object

  ### Raises:
      ResourceNotFoundException: If the module does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      GetModuleResponseModel: module Object
  """
  try:
    module = Module.find_by_uuid(uuid)
    if fetch_tree:
      module_fields = CollectionHandler.loads_field_data_from_collection(
          module.get_fields(reformat_datetime=True))
    else:
      module_fields = module.get_fields(reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully fetched the module",
        "data": module_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post("/module", response_model=PostModuleResponseModel)
def create_module(input_module: ModuleModel):
  """The create module endpoint will add the module in request body to the
  firestore

  ### Args:
      input_module (ModuleModel): input module to be inserted
      name : Unique for every module

  ### Raises:
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      PostModuleResponseModel: Module Object
  """
  try:
    existing_module = Module.find_by_name(input_module.name)
    if existing_module is not None:
      raise ConflictError(
        f"Module with the given name: {input_module.name} "
        "already exists")

    input_module_dict = {**input_module.dict()}

    if "actions" in input_module_dict and input_module.actions != []:
      for action in input_module.actions:
        Action.find_by_uuid(uuid=action)

    new_module = Module()
    new_module = new_module.from_dict(input_module_dict)
    new_module.uuid = ""
    new_module.save()
    new_module.uuid = new_module.id
    new_module.update()

    module_fields = new_module.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully created the module",
        "data": module_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/module/{uuid}",
    response_model=UpdateModuleResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_module(uuid: str, input_module: UpdateModuleModel):
  """Update a module with the uuid passed in the request body

  ### Args:
      input_module (ModuleModel): Required body of the module
      name : Unique for every module

  ### Raises:
      ResourceNotFoundException: If the module does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      UpdateModuleResponseModel: Module Object
  """
  try:
    existing_module = Module.find_by_name(input_module.name)
    if existing_module is not None:
      raise ConflictError(
        f"Module with the given name: {input_module.name} "
        "already exists")

    existing_module = Module.find_by_uuid(uuid)

    input_module_dict = {**input_module.dict()}

    if "actions" in input_module_dict and input_module.actions != []:
      for action in input_module.actions:
        Action.find_by_uuid(uuid=action)

    module_fields = existing_module.get_fields()

    for key, value in input_module_dict.items():
      module_fields[key] = value
    for key, value in module_fields.items():
      setattr(existing_module, key, value)

    existing_module.update()
    module_fields = existing_module.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully updated the module",
        "data": module_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/module/{uuid}",
    response_model=DeleteModule,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_module(uuid: str):
  """Delete a module with the given uuid from firestore

  ### Args:
      uuid (str): Unique id of the module

  ### Raises:
      ResourceNotFoundException: If the module does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      JSON: Success/Fail Message
  """
  try:
    module = Module.find_by_uuid(uuid)

    Module.collection.delete(module.key)

    return {"success": True, "message": "Successfully deleted the module"}

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
