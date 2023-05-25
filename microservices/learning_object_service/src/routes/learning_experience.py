""" Learning Experience endpoints """
import traceback
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Query
from common.models import LearningExperience
from common.utils.logging_handler import Logger
from common.utils.parent_child_nodes_handler import ParentChildNodesHandler
from common.utils.common_api_handler import CommonAPIHandler
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from schemas.learning_experience_schema import (
    BasicLearningExperienceModel, LearningExperienceModel,
    LearningExperienceResponseModel, UpdateLearningExperienceModel,
    DeleteLearningExperience, LearningExperienceSearchResponseModel,
    AllLearningExperiencesResponseModel, LearningExperienceImportJsonResponse,
    CopyLearningExperienceModel)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from services.json_import import json_import
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES

router = APIRouter(tags=["Learning Experience"])

# pylint: disable = broad-except
router = APIRouter(tags=["Learning Experience"], responses=ERROR_RESPONSES)


@router.get(
    "/learning-experience/search",
    response_model=LearningExperienceSearchResponseModel)
def search_learning_experience(name: Optional[str] = None):
  """Search for learning experience based on the name
  ### Args:
  name: `str`
    Name of the learning experience. Defaults to None.
  ### Raises:
  ValueError:
    Raised when input angles are outside range. <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong.
  ### Returns:
  List of learning experience experiences: \
  `LearningExperienceSearchResponseModel`
  """
  if name:
    # fetch learning experience that matches name
    learning_experiences = LearningExperience.find_by_name(name)
    result = [
        learning_experience.get_fields(reformat_datetime=True)
        for learning_experience in learning_experiences
    ]
    return {
        "success": True,
        "message": "Successfully fetched the learning experiences",
        "data": result
    }
  else:
    raise BadRequest("Missing or invalid request parameters")


@router.get(
    "/learning-experiences",
    response_model=AllLearningExperiencesResponseModel,
    name="Get all Learning Experiences",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_learning_experiences(display_name: str = None,
                             fetch_archive: bool = None,
                             curriculum_pathway: str = None,
                             learning_opportunity: str = None,
                             learning_object: str = None,
                             assessment: str = None,
                             author: str = None,
                             version: int = None,
                             skip: int = Query(0, ge=0, le=2000),
                             limit: int = Query(10, ge=1, le=100)):
  """The get learning experiences endpoint will return an array learning
  experiences from firestore
  ### Args:
  display_name: `str`
    Display name of the learning experience <br/>
  curriculum_pathway: `str`
    UUID of the learning pathway <br/>
  learning_opportunity: `str`
    UUID of the learning opportunity <br/>
  learning_object: `str`
    UUID of the learning object <br/>
  assessments: `str`
    UUID of the assessments <br/>
  version: `int`
    Version of the data object <br/>
  author: `str`
    Name of the Author of the data object <br/>
  skip: `int`
    Number of experiences to be skipped <br/>
  limit: `int`
    Size of learning experience array to be returned <br/>
  ### Raises:
  ValueError:
    Raised when input angles are outside range. <br/>
  Exception 500
    Internal Server Error Raised. Raised if something went wrong
  ### Returns:
  Array of Learning Experience: `AllLearningExperiencesResponseModel`
  """
  try:
    collection_manager = LearningExperience.collection.filter(
        "is_deleted", "==", False)
    array_flag = 0
    if display_name:
      collection_manager = collection_manager.filter("display_name", "==",
                                                     display_name)
      array_flag += 1
    if learning_opportunity:
      collection_manager = collection_manager.filter(
          "parent_nodes.learning_opportunities", "array_contains",
          learning_opportunity)
      array_flag += 1

    if curriculum_pathway:
      collection_manager = collection_manager.filter(
          "parent_nodes.curriculum_pathways", "array_contains",
          curriculum_pathway)
      array_flag += 1

    if learning_object:
      collection_manager = collection_manager.filter(
          "child_nodes.learning_objects", "array_contains", learning_object)
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
          "Please use only one of the following fields for filter at a time - author, learning_object, curriculum_pathway, learning_opportunity, version"
      )
    if fetch_archive:
      collection_manager = collection_manager.filter("is_archived", "==", True)
    elif fetch_archive is False:
      collection_manager = collection_manager.filter("is_archived", "==", False)

    learning_experiences = collection_manager.order("-created_time").offset(
        skip).fetch(limit)
    learning_experiences = [
        i.get_fields(reformat_datetime=True) for i in learning_experiences
    ]
    return {
        "success": True,
        "message": "Data fetched successfully",
        "data": learning_experiences
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
    "/learning-experience/{uuid}",
    response_model=LearningExperienceResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_learning_experience(uuid: str, fetch_tree: Optional[bool] = False):
  """The get learning experience endpoint will return the learning experience
  from firestore of which uuid is provided
  ### Args:
  uuid: `str`
    Unique identifier for learning experience
  fetch_all_versions: `bool`
    Flag to determine whether to fetch all versions or not
  version: `int`
    Number to identify which version number of the document to fetch
  ### Raises:
  ResourceNotFoundException:
    If the learning experience does not exist. <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Learning Experience: `LearningExperienceResponseModel`
  """
  try:
    learning_experience = LearningExperience.find_by_uuid(uuid)
    learning_experience = learning_experience.get_fields(reformat_datetime=True)

    if fetch_tree:
      learning_experience = ParentChildNodesHandler.load_child_nodes_data(
          learning_experience)
      learning_experience = \
        ParentChildNodesHandler.load_immediate_parent_nodes_data(
              learning_experience)
    return {
        "success": True,
        "message": "Successfully fetched the learning object",
        "data": learning_experience
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
    "/learning-experience",
    response_model=LearningExperienceResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def create_learning_experience(
    input_learning_experience: LearningExperienceModel):
  """The create learning experience endpoint will add the learning experience to
  the firestore if it does not exist.If the learning experience exist then it
  will update the learning experience
  ### Args:
  input_learning_experience: `LearningExperienceModel`
    Input learning experience to be inserted
  ### Raises:
  ResourceNotFoundException:
    If the learning experience does not exist <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  UUID: `str`
    Unique identifier for learning experience
  """
  try:
    input_learning_experience_dict = {**input_learning_experience.dict()}
    if "display_name" not in input_learning_experience_dict:
      input_learning_experience_dict["display_name"] = \
        input_learning_experience_dict["name"]

    ParentChildNodesHandler.validate_parent_child_nodes_references(
        input_learning_experience_dict)

    new_learning_experience = LearningExperience()
    new_learning_experience = new_learning_experience.from_dict(
        input_learning_experience_dict)
    new_learning_experience.uuid = ""
    new_learning_experience.is_locked = False
    for prereq_level in new_learning_experience.prerequisites:
      if new_learning_experience.prerequisites[prereq_level]:
        new_learning_experience.is_locked = True
        break
    new_learning_experience.version = 1
    new_learning_experience.save()

    new_learning_experience.uuid = new_learning_experience.id
    new_learning_experience.root_version_uuid = \
      new_learning_experience.id
    new_learning_experience.update()

    learning_experience_fields = new_learning_experience.get_fields(
        reformat_datetime=True)
    ParentChildNodesHandler.update_child_references(
        learning_experience_fields, LearningExperience, operation="add")
    ParentChildNodesHandler.update_parent_references(
        learning_experience_fields, LearningExperience, operation="add")

    return {
        "success": True,
        "message": "Successfully created the learning experience",
        "data": learning_experience_fields
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
    "/learning-experience/{uuid}",
    response_model=LearningExperienceResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_learning_experience(
    uuid: str,
    input_learning_experience: UpdateLearningExperienceModel,
    create_version: bool = False):
  """Update a learning experience
  ### Args:
  input_learning_experience: `UpdateLearningExperienceModel`
    Required body of the learning experience
  ### Raises:
  ResourceNotFoundException:
    If the learning experience does not exist <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Updated Learning Experience: `LearningExperienceResponseModel`
  """
  try:
    input_le_dict = {**input_learning_experience.dict()}
    if create_version:
      updated_doc_fields = \
        CommonAPIHandler.update_and_create_version(LearningExperience,
                                                   uuid,
                                                   input_le_dict)
    else:
      # Updating the original doc
      updated_doc_fields = \
        CommonAPIHandler.update_document(LearningExperience,
                                         uuid,
                                         input_le_dict)

    return {
        "success": True,
        "message": "Successfully updated the learning experience",
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
    "/learning-experience/{uuid}",
    response_model=DeleteLearningExperience,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_learning_experience(uuid: str):
  """Delete a learning experience from firestore
  ### Args:
  uuid: `str`
    Unique ID of the learning experience
  ### Raises:
  ResourceNotFoundException:
    If the learning experience does not exist. <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Success/Fail Message: `JSON`
  """
  try:
    learning_experience = LearningExperience.find_by_uuid(uuid)
    learning_experience_fields = learning_experience.get_fields(
        reformat_datetime=True)

    ParentChildNodesHandler.validate_parent_child_nodes_references(
        learning_experience_fields)
    ParentChildNodesHandler.update_child_references(
        learning_experience_fields, LearningExperience, operation="remove")
    ParentChildNodesHandler.update_parent_references(
        learning_experience_fields, LearningExperience, operation="remove")

    LearningExperience.delete_by_uuid(learning_experience.uuid)
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
    "/learning-experience/import/json",
    response_model=LearningExperienceImportJsonResponse,
    name="Import Learning Experience from JSON file",
    responses={413: {
        "model": PayloadTooLargeResponseModel
    }})
async def import_learning_experiences(json_file: UploadFile = File(...)):
  """Create learning experiences from json file
  ### Args:
  json_file: `UploadFile`
    Upload json file consisting of learning experiences.
  ### Raises:
  Exception 500:
    Internal Server Error. Raised if something fails
  ### Returns:
    Learning Experience UUID: `LearningExperienceImportJsonResponse`
  """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
        f"File size is too large: {json_file.filename}"
      )
    await json_file.seek(0)
    final_output = json_import(
        json_file=json_file,
        json_schema=BasicLearningExperienceModel,
        model_obj=LearningExperience,
        object_name="learning experiences")
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
    "/learning-experience/copy/{uuid}",
    response_model=CopyLearningExperienceModel,
    name="Copy a learning experience",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def copy_learning_experience(uuid: str):
  """Copy a learning experience

  ### Args:
  uuid: `str`
    Unique identifier for learning experience

  ### Raises:
  ResourceNotFoundException:
    If the learning experience does not exist <br/>
  Exception 500:
    Internal Server Error if something went wrong

  ### Returns:
  Learning Experience: `LearningExperienceModel`
  """
  try:
    learning_experience_fields = CommonAPIHandler.create_copy(
        LearningExperience, uuid)
    return {
        "success": True,
        "message": "Successfully copied the learning experience",
        "data": learning_experience_fields
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
