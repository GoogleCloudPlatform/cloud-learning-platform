""" Learning Object endpoints """
import traceback
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Query
from common.models import LearningObject
from common.utils.logging_handler import Logger
from common.utils.parent_child_nodes_handler import ParentChildNodesHandler
from common.utils.common_api_handler import CommonAPIHandler
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from schemas.learning_object_schema import (
    BasicLearningObjectModel, LearningObjectModel, LearningObjectResponseModel,
    UpdateLearningObjectModel, DeleteLearningObject,
    LearningObjectSearchResponseModel, AllLearningObjectsResponseModel,
    LearningObjectImportJsonResponse, CopyLearningObjectModel)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from services.json_import import json_import
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES

router = APIRouter(tags=["Learning Object"])

# pylint: disable = broad-except
router = APIRouter(tags=["Learning Object"], responses=ERROR_RESPONSES)



@router.get(
    "/learning-object/search", response_model=LearningObjectSearchResponseModel)
def search_learning_object(name: Optional[str] = None):
  """Search for learning object based on the name

  ### Args:
  name: `str`
    Name of the learning object. Defaults to None.

  ### Raises:
  ValueError:
    Raised when input angles are outside range. <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong.

  ### Returns:
  List of learning object: `LearningObjectSearchResponseModel`
  """
  if name:
    # fetch learning object that matches name
    learning_objects = LearningObject.find_by_name(name)
    result = [
        learning_object.get_fields(reformat_datetime=True)
        for learning_object in learning_objects
    ]
    return {
        "success": True,
        "message": "Successfully fetched the learning objects",
        "data": result
    }
  else:
    raise BadRequest("Missing or invalid request parameters")


@router.get(
    "/learning-objects",
    response_model=AllLearningObjectsResponseModel,
    name="Get all Learning Objects",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_learning_objects(display_name: str = None,
                         fetch_archive: bool = None,
                         learning_experience: str = None,
                         learning_object: str = None,
                         learning_resource: str = None,
                         assessment: str = None,
                         author: str = None,
                         skip: int = Query(0, ge=0, le=2000),
                         limit: int = Query(10, ge=1, le=100),
                         version: int = None,
                         relation: str = "child"):
  """The get learning objects endpoint will return an array learning objects
  from firestore

  ### Args:
  display_name: `str`
    Display name of the learning objects <br/>
  learning_experience: `str`
    UUID of the learning experience
  learning_object: `str`
    UUID of the learning object
  assessments: `str`
    UUID of the assessments
  version: `int`
    Version of the data object
  author: `str`
    Name of the Author of the data object
  relation: `str`
    Points where to filter the learning object, from parent_nodes or child_nodes
  skip: `int`
    Number of objects to be skipped. <br/>
  limit: `int`
    Size of learning object array to be returned
  fetch_archive: 'boolean'
    Flag to verify if we need to fetch archived data objects

  ### Raises:
  ValueError:
    Raised when input angles are outside range. <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong

  ### Returns:
  List of Learning Object: `AllLearningObjectsModelResponse`
  """
  try:
    collection_manager = LearningObject.collection.filter(
        "is_deleted", "==", False)
    array_flag = 0
    if display_name:
      collection_manager = collection_manager.filter("display_name", "==",
                                                     display_name)
      array_flag += 1
    if learning_experience:
      collection_manager = collection_manager.filter(
          "parent_nodes.learning_experiences", "array_contains",
          learning_experience)
      array_flag += 1

    if learning_object:
      collection_manager = collection_manager.filter(
          f"{relation}_nodes.learning_objects", "array_contains",
          learning_object)
      array_flag += 1

    if learning_resource:
      collection_manager = collection_manager.filter(
          "child_nodes.learning_resources", "array_contains", learning_resource)
      array_flag += 1

    if assessment:
      collection_manager = collection_manager.filter(
          "child_nodes.assessment_items", "array_contains", assessment)
      array_flag += 1

    if version:
      collection_manager = collection_manager.filter("version", "==", version)

    if author:
      collection_manager = collection_manager.filter("author", "==", author)

    if array_flag > 1:
      raise ValidationError(
          # pylint: disable=line-too-long
          "Please use only one of the following fields for filter at a time - author, learning_object, learning_experience, version"
      )
    if fetch_archive:
      collection_manager = collection_manager.filter("is_archived", "==", True)
    elif fetch_archive is False:
      collection_manager = collection_manager.filter("is_archived", "==", False)

    learning_objects = collection_manager.order("-created_time").offset(
        skip).fetch(limit)
    learning_objects = [
        i.get_fields(reformat_datetime=True) for i in learning_objects
    ]
    count = 10000
    response = {"records": learning_objects, "total_count": count}
    return {
        "success": True,
        "message": "Data fetched successfully",
        "data": response
    }
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
    "/learning-object/{uuid}",
    response_model=LearningObjectResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_learning_object(uuid: str, fetch_tree: Optional[bool] = False):
  """The get learning object endpoint will return the learning object from
  firestore of which uuid is provided

  ### Args:
  uuid: `str`
    Unique identifier for learning object
  fetch_all_versions: `bool`
    Flag to determine whether to fetch all versions or not
  version: `int`
    Number to identify which version number of the document to fetch
  ### Raises:
  ResourceNotFoundException:
    If the learning object does not exist <br/>
  Exception 500:
    Internal Server Error if something went wrong

  ### Returns:
  Learning Object: `LearningObjectResponseModel`
  """
  try:
    learning_object = LearningObject.find_by_uuid(uuid)
    learning_object = learning_object.get_fields(reformat_datetime=True)

    if fetch_tree:
      learning_object = ParentChildNodesHandler.load_child_nodes_data(
          learning_object)
      learning_object = \
        ParentChildNodesHandler.load_immediate_parent_nodes_data(
              learning_object)
    return {
        "success": True,
        "message": "Successfully fetched the learning object",
        "data": learning_object
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
    "/learning-object",
    response_model=LearningObjectResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def create_learning_object(input_learning_object: LearningObjectModel):
  """The create learning object endpoint will add the learning object to the
  firestore if it does not exist.If the learning object exist then it will
  update the learning object

  ### Args:
  input_learning_object: `LearningObjectModel`
    Input learning object to be inserted

  ### Raises:
  ResourceNotFoundException:
    If the learning object does not exist <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong

  ### Returns:
  UUID: `str`
    Unique identifier for learning object
  """
  try:
    input_learning_object_dict = {**input_learning_object.dict()}
    if "display_name" not in input_learning_object_dict:
      input_learning_object_dict["display_name"] = \
        input_learning_object_dict["name"]

    ParentChildNodesHandler.validate_parent_child_nodes_references(
        input_learning_object_dict)

    new_learning_object = LearningObject()
    new_learning_object = new_learning_object.from_dict(
        input_learning_object_dict)
    new_learning_object.uuid = ""
    for prereq_level in new_learning_object.prerequisites:
      if new_learning_object.prerequisites[prereq_level]:
        new_learning_object.is_locked = True
        break
    new_learning_object.version = 1
    new_learning_object.save()

    new_learning_object.uuid = new_learning_object.id
    new_learning_object.root_version_uuid = \
      new_learning_object.id
    new_learning_object.update()
    learning_object_fields = new_learning_object.get_fields(
        reformat_datetime=True)

    ParentChildNodesHandler.update_child_references(
        learning_object_fields, LearningObject, operation="add")
    ParentChildNodesHandler.update_parent_references(
        learning_object_fields, LearningObject, operation="add")

    return {
        "success": True,
        "message": "Successfully created the learning object",
        "data": learning_object_fields
    }
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.put(
    "/learning-object/{uuid}",
    response_model=LearningObjectResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_learning_object(uuid: str,
                           input_learning_object: UpdateLearningObjectModel,
                           create_version: bool = False):
  """Update a learning object

  ### Args:
  input_learning_object: `UpdateLearningObjectModel`
    Required body of the learning object

  ### Raises:
  ResourceNotFoundException:
    If the learning object does not exist <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong

  ### Returns:
  Updated Learning Object: `LearningObjectResponseModel`
  """
  try:
    input_lo_dict = {**input_learning_object.dict()}
    if create_version:
      updated_doc_fields = \
        CommonAPIHandler.update_and_create_version(LearningObject,
                                                   uuid,
                                                   input_lo_dict)
    else:
      # Updating the original doc
      updated_doc_fields = \
        CommonAPIHandler.update_document(LearningObject,
                                         uuid,
                                         input_lo_dict)

    return {
        "success": True,
        "message": "Successfully updated the learning object",
        "data": updated_doc_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/learning-object/{uuid}",
    response_model=DeleteLearningObject,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_learning_object(uuid: str):
  """Delete a learning object from firestore

  ### Args:
  uuid: `str`
    Unique id of the learning object

  ### Raises:
  ResourceNotFoundException:
    If the learning object does not exist <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong

  ### Returns:
  Success/Fail Message: `JSON`
  """
  try:
    learning_object = LearningObject.find_by_uuid(uuid)
    learning_object_fields = learning_object.get_fields(reformat_datetime=True)

    ParentChildNodesHandler.validate_parent_child_nodes_references(
        learning_object_fields)
    ParentChildNodesHandler.update_child_references(
        learning_object_fields, LearningObject, operation="remove")
    ParentChildNodesHandler.update_parent_references(
        learning_object_fields, LearningObject, operation="remove")

    LearningObject.delete_by_uuid(learning_object.uuid)

    # remove deleted LO from prerequisites of other LOs
    CommonAPIHandler.remove_uuid_from_prerequisites(
      LearningObject, "learning_objects", uuid)

    return {}
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/learning-object/import/json",
    response_model=LearningObjectImportJsonResponse,
    name="Import Learning Object from JSON file",
    responses={413: {
        "model": PayloadTooLargeResponseModel
    }})
async def import_learning_objects(json_file: UploadFile = File(...)):
  """Create learning objects from json file

  ### Args:
  json_file: `UploadFile`
    Upload json file consisting of learning objects. json_schema should match
    LearningObjectModel

  ### Raises:
  Exception 500: Internal Server Error Raised if something fails

  ### Returns:
  Learning Object UUID: `LearningObjectImportJsonResponse`
  """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
        f"File size is too large: {json_file.filename}"
      )
    await json_file.seek(0)
    final_output = json_import(
        json_file=json_file,
        json_schema=BasicLearningObjectModel,
        model_obj=LearningObject,
        object_name="learning objects")
    return final_output
  except PayloadTooLargeError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise PayloadTooLarge(str(e)) from e
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/learning-object/copy/{uuid}",
    response_model=CopyLearningObjectModel,
    name="Copy a learning object",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def copy_learning_object(uuid: str):
  """Copy a learning object

  ### Args:
  uuid: `str`
    Unique identifier for learning object

  ### Raises:
  ResourceNotFoundException:
    If the learning object does not exist <br/>
  Exception 500:
    Internal Server Error if something went wrong

  ### Returns:
  Learning Object: `LearningObjectModel`
  """
  try:
    learning_object_fields = CommonAPIHandler.create_copy(LearningObject, uuid)
    return {
        "success": True,
        "message": "Successfully copied the learning object",
        "data": learning_object_fields
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
