"""Routes for Learning Resource"""
import traceback
from services.json_import import json_import
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Query
from common.models import LearningResource
from common.utils.logging_handler import Logger
from common.utils.parent_child_nodes_handler import ParentChildNodesHandler
from common.utils.common_api_handler import CommonAPIHandler
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from schemas.learning_resource_schema import (
    BasicLearningResourceModel, LearningResourceModel,
    GetLearningResourceModelResponse, PostLearningResourceModelResponse,
    UpdateLearningResourceModelResponse, UpdateLearningResourceModel,
    DeleteLearningResource, LearningResourceSearchModelResponse,
    LearningResourceImportJsonResponse, CopyLearningResourceModel,
    AllLearningResourcesModelResponse)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES
# pylint: disable = broad-except

router = APIRouter(tags=["Learning Resource"], responses=ERROR_RESPONSES)

# pylint: disable=redefined-builtin


@router.get(
    "/learning-resources", response_model=AllLearningResourcesModelResponse)
def get_learning_resources(display_name: str = None,
                           fetch_archive: bool = None,
                           name: str = None,
                           learning_object: str = None,
                           concept: str = None,
                           version: int = None,
                           type: str = None,
                           course_category: str = None,
                           skip: int = Query(0, ge=0, le=2000),
                           limit: int = Query(10, ge=1, le=100)):
  """The get learning resources endpoint will return an array learning
  resources from firestore

  Args:
      display_name (str): Display name of the learning resource
      name (str): Name of the learning resource
      learning_object (str): UUID of the learning object (parent of
                              learing resource)
      concept (str): UUID of the concept (child of learning resource)
      version (str): Version of the data object
      type (str): Filter using document type of learning
                            resource
      course_category (str): Course category of learning
                                resource
      fetch_archive (bool): Flag to denote whether the data document is archived
      skip (int): Number of objects to be skipped
      limit (int): Size of learning resource array to be returned
  Raises:
      Exception: 500 Internal Server Error if something went wrong
  Returns:
      AllLearningResourcesModelResponse: Array of LearningResource Object
  """
  try:
    collection_manager = LearningResource.collection.filter(
        "is_deleted", "==", False)
    array_flag = 0
    if display_name:
      collection_manager = collection_manager.filter("display_name", "==",
                                                     display_name)
      array_flag += 1

    if name:
      collection_manager = collection_manager.filter("name", "==", name)

    if learning_object:
      collection_manager = collection_manager.filter(
          "parent_nodes.learning_objects", "array_contains", learning_object)
      array_flag += 1

    if concept:
      collection_manager = collection_manager.filter("child_nodes.concepts",
                                                     "array_contains", concept)
      array_flag += 1

    if version:
      collection_manager = collection_manager.filter("version", "==", version)

    if type:
      collection_manager = collection_manager.filter("type", "==", type)

    if course_category:
      collection_manager = collection_manager.filter("course_category",
                                                     "array_contains",
                                                     course_category)
      array_flag += 1

    if fetch_archive:
      collection_manager = collection_manager.filter("is_archived", "==", True)

    elif fetch_archive is False:
      collection_manager = collection_manager.filter("is_archived", "==", False)

    # pylint: disable = line-too-long
    # TODO: This filter should be used when the content versioning is enabled
    # collection_manager = collection_manager.filter("status", "in", ["initial", "published"])

    if array_flag > 1:
      raise ValidationError(
          "Please use only one of the following fields for filter at a time: "
          "learning_object, concept, and course_category")

    learning_resources = collection_manager.order("-created_time").offset(
        skip).fetch(limit)
    learning_resources = [
        i.get_fields(reformat_datetime=True)
        for i in learning_resources
        if i.name
    ]
    return {
        "success": True,
        "message": "Data fetched successfully",
        "data": learning_resources
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
    "/learning-resource/search",
    response_model=LearningResourceSearchModelResponse)
def search_learning_resource(name: Optional[str] = None):
  """Search for learning resources based on the name

  Args:
      name(str): Name of the learning resource. Defaults to None.

  Returns:
      LearningResourceSearchModelResponse: List of learning resource objects
  """
  result = []
  if name:
    # fetch learning resource that matches name
    learning_resources = LearningResource.find_by_name(name)
    result = [
        learning_resource.get_fields(reformat_datetime=True)
        for learning_resource in learning_resources
    ]
    return {
        "success": True,
        "message": "Successfully fetched the learning resources",
        "data": result
    }
  else:
    raise BadRequest("Missing or invalid request parameters")


@router.get(
    "/learning-resource/{uuid}",
    response_model=GetLearningResourceModelResponse,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_learning_resource(uuid: str, fetch_tree: Optional[bool] = False):
  """The get learning resource endpoint will return the learning resource from
  firestore of which uuid is provided

  Args:
      uuid (str): Unique identifier for learning resource

  Raises:
      ResourceNotFoundException: If the learning resource does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      GetLearningResourceModelResponse: Learning Resource Object
  """
  try:
    learning_resource = LearningResource.find_by_id(uuid)
    learning_resource = learning_resource.get_fields(reformat_datetime=True)

    if fetch_tree:
      learning_resource = ParentChildNodesHandler.load_child_nodes_data(
          learning_resource)
      learning_resource = \
        ParentChildNodesHandler.load_immediate_parent_nodes_data(
              learning_resource)
    return {
        "success": True,
        "message": "Successfully fetched the learning object",
        "data": learning_resource
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
    "/learning-resource",
    response_model=PostLearningResourceModelResponse,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def create_learning_resource(input_learning_resource: LearningResourceModel):
  """The create learning resource endpoint will add the given learning
  resource in request body to the firestore

  Args:
      input_learning_resource (LearningResourceModel): input learning
      resource to be inserted

  Raises:
      ResourceNotFoundException: If the learning resource does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      PostLearningResourceModelResponse: Learning Resource Object
  """
  try:
    input_learning_resource_dict = {**input_learning_resource.dict()}

    ParentChildNodesHandler.validate_parent_child_nodes_references(
        input_learning_resource_dict)

    new_learning_resource = LearningResource()
    input_learning_resource_dict = {**input_learning_resource.dict()}

    input_learning_resource_dict["status"] = "initial"

    if "display_name" not in input_learning_resource_dict:
      input_learning_resource_dict["display_name"] = \
        input_learning_resource_dict["name"]
    new_learning_resource = new_learning_resource.from_dict(
        input_learning_resource_dict)
    new_learning_resource.uuid = ""
    for prereq_level in new_learning_resource.prerequisites:
      if new_learning_resource.prerequisites[prereq_level]:
        new_learning_resource.is_locked = True
        break
    new_learning_resource.save()

    new_learning_resource.uuid = new_learning_resource.id
    new_learning_resource.root_version_uuid = \
      new_learning_resource.id
    new_learning_resource.update()
    learning_resource_fields = new_learning_resource.get_fields(
        reformat_datetime=True)

    ParentChildNodesHandler.update_child_references(
        learning_resource_fields, LearningResource, operation="add")
    ParentChildNodesHandler.update_parent_references(
        learning_resource_fields, LearningResource, operation="add")

    return {
        "success": True,
        "message": "Successfully created the learning resource",
        "data": learning_resource_fields
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
    "/learning-resource/{uuid}",
    response_model=UpdateLearningResourceModelResponse,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_learning_resource(
    uuid: str,
    input_learning_resource: UpdateLearningResourceModel,
    create_version: bool = False):
  """Update a learning resource with the uuid passed in the request body

  Args:
      input_learning_resource (LearningResourceModel): Required body of the
      learning resource

  Raises:
      ResourceNotFoundException: If the learning resource does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      UpdateLearningResourceModelResponse: LearningResource Object
  """
  try:
    input_lo_dict = {**input_learning_resource.dict()}
    if create_version:
      updated_doc_fields = \
        CommonAPIHandler.update_and_create_version(LearningResource,
                                                    uuid,
                                                    input_lo_dict)
    else:
      # Updating the original doc
      updated_doc_fields = \
        CommonAPIHandler.update_document(LearningResource,
                                         uuid,
                                         input_lo_dict)
    return {
        "success": True,
        "message": "Successfully updated the learning resource",
        "data": updated_doc_fields
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
    "/learning-resource/{uuid}",
    response_model=DeleteLearningResource,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_learning_resource(uuid: str):
  """Delete a learning resource with the given uuid from firestore

  Args:
      uuid (str): Unique id of the learning resource

  Raises:
      ResourceNotFoundException: If the learning resource does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      JSON: Success/Fail Message
  """
  try:
    learning_resource = LearningResource.find_by_id(uuid)
    learning_resource_fields = learning_resource.get_fields(
        reformat_datetime=True)

    ParentChildNodesHandler.validate_parent_child_nodes_references(
        learning_resource_fields)
    ParentChildNodesHandler.update_child_references(
        learning_resource_fields, LearningResource, operation="remove")
    ParentChildNodesHandler.update_parent_references(
        learning_resource_fields, LearningResource, operation="remove")

    LearningResource.delete_by_uuid(learning_resource.uuid)
    return {
        "success": True,
        "message": "Successfully deleted the learning resource"
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
    "/learning-resource/import/json",
    response_model=LearningResourceImportJsonResponse,
    name="Import Learning Resource from JSON file",
    responses={413: {
        "model": PayloadTooLargeResponseModel
    }})
async def import_learning_resources(json_file: UploadFile = File(...)):
  """Create learning resources from json file
  ### Args:
  json_file: `UploadFile`
    Upload json file consisting of learning resources.
  ### Raises:
  Exception 500:
    Internal Server Error. Raised if something fails
  ### Returns:
    Learning Resource UUID: `LearningResourceImportJsonResponse`
  """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
        f"File size is too large: {json_file.filename}"
      )
    await json_file.seek(0)
    final_output = json_import(
        json_file=json_file,
        json_schema=BasicLearningResourceModel,
        model_obj=LearningResource,
        object_name="learning resources")
    return final_output
  except PayloadTooLargeError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise PayloadTooLarge(str(e)) from e
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/learning-resource/copy/{uuid}",
    response_model=CopyLearningResourceModel,
    name="Copy a learning resource",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def copy_learning_resource(uuid: str):
  """Copy a learning resource
  ### Args:
  uuid: `str`
    Unique identifier for learning resource
  ### Raises:
  ResourceNotFoundException:
    If the learning resource does not exist <br/>
  Exception 500:
    Internal Server Error if something went wrong
  ### Returns:
  Learning Resource: `LearningResourceModel`
  """
  try:
    learning_resource_fields = CommonAPIHandler.create_copy(
        LearningResource, uuid)
    return {
        "success": True,
        "message": "Successfully copied the learning resource",
        "data": learning_resource_fields
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
