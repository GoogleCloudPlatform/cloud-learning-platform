""" Curriculum Pathway endpoints """
import traceback
from typing import Optional, Union
from fastapi import APIRouter, UploadFile, File, Query, Request
from common.models import CurriculumPathway, LearnerProfile
from common.utils.rest_method import put_method
from common.utils.logging_handler import Logger
from common.utils.parent_child_nodes_handler import ParentChildNodesHandler
from common.utils.common_api_handler import CommonAPIHandler
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from schemas.curriculum_pathway_schema import (
    BasicCurriculumPathwayModel, CurriculumPathwayModel,
    CurriculumPathwayResponseModel, UpdateCurriculumPathwayModel,
    DeleteCurriculumPathway, DeleteLearningPathway,
    CurriculumPathwaySearchResponseModel,
    AllCurriculumPathwaysResponseModel, CurriculumPathwayImportJsonResponse,
    CopyCurriculumPathwayModel, CurriculumPathwayResponseModel2,
    GetCurriculumPathwayAliasResponseModel)
from schemas.upload_pathway import (PathwayImportJsonResponse)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from services.json_import import json_import
from services.bulk_import import bulk_import, delete_hierarchy_handler
from services.helper import transform_dict, get_all_nodes_for_alias
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES, ALL_ALIASES, UM_BASE_URL

router = APIRouter(tags=["Curriculum Pathway"])

# pylint: disable = broad-except
router = APIRouter(tags=["Curriculum Pathway"], responses=ERROR_RESPONSES)


@router.get(
    "/curriculum-pathway/search",
    response_model=CurriculumPathwaySearchResponseModel)
def search_curriculum_pathway(name: Optional[str] = None):
  """Search for curriculum pathway based on the name
  ### Args:
  name: `str`
    Name of the curriculum pathway. Defaults to None.
  ### Raises:
  ValueError:
    Raised when input angles are outside range. <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong.
  ### Returns:
  List of curriculum pathways: \
  `CurriculumPathwaySearchResponseModel`
  """
  if name:
    # fetch curriculum pathway that matches name
    curriculum_pathways = CurriculumPathway.find_by_name(name)
    result = [
        curriculum_pathway.get_fields(reformat_datetime=True)
        for curriculum_pathway in curriculum_pathways
    ]
    return {
        "success": True,
        "message": "Successfully fetched the curriculum pathways",
        "data": result
    }
  else:
    raise BadRequest("Missing or invalid request parameters")


@router.get(
    "/curriculum-pathways",
    response_model=AllCurriculumPathwaysResponseModel,
    name="Get all Curriculum Pathways",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_curriculum_pathways(
                            alias: str = None,
                            fetch_archive: bool = None,
                            learning_opportunity: str = None,
                            learning_experience: str = None,
                            parent_curriculum_pathway: str = None,
                            child_curriculum_pathway: str = None,
                            is_active: bool = None,
                            author: str = None,
                            version: int = None,
                            skip: int = Query(0, ge=0, le=2000),
                            limit: int = Query(10, ge=1, le=100)):
  """The get curriculum pathways endpoint will return an array learning
  experiences from firestore
  ### Args:
  parent_curriculum_pathway: `str`
    UUID of the curriculum pathway that is a parent node <br/>
  child_curriculum_pathway: `str`
    UUID of the curriculum pathway that is a child node <br/>
  learning_opportunity: `str`
    UUID of the learning opportunity <br/>
  learning_experience: `str`
    UUID of the learning experience <br/>
  is_active: `bool`
    Flag to determine whether to fetch active pathway or not
  version: `int`
    Version of the data object <br/>
  author: `str`
    Name of the Author of the data object <br/>
  skip: `int`
    Number of experiences to be skipped <br/>
  limit: `int`
    Size of curriculum pathway array to be returned <br/>
  ### Raises:
  ValueError:
    Raised when input angles are outside range. <br/>
  Exception 500
    Internal Server Error Raised. Raised if something went wrong
  ### Returns:
  Array of Curriculum Pathway: `AllCurriculumPathwaysResponseModel`
  """
  try:
    array_flag = 0
    if alias:
      collection_manager = CurriculumPathway.collection.filter(
        "alias", "==", alias).filter("is_deleted", "==", False)
    else:
      collection_manager = CurriculumPathway.collection.filter(
        "is_deleted", "==", False)

    if learning_opportunity:
      collection_manager = collection_manager.filter(
          "parent_nodes.learning_opportunities", "array_contains",
          learning_opportunity)
      array_flag += 1

    if parent_curriculum_pathway:
      collection_manager = collection_manager.filter(
          "parent_nodes.curriculum_pathways", "array_contains",
          parent_curriculum_pathway)
      array_flag += 1

    if child_curriculum_pathway:
      collection_manager = collection_manager.filter(
          "child_nodes.curriculum_pathways", "array_contains",
          child_curriculum_pathway)
      array_flag += 1

    if learning_experience:
      collection_manager = collection_manager.filter(
          "child_nodes.learning_experiences", "array_contains",
          learning_experience)
      array_flag += 1

    if version:
      collection_manager = collection_manager.filter("version", "==", version)

    if author:
      collection_manager = collection_manager.filter("author", "==", author)

    if is_active is not None:
      collection_manager = collection_manager.filter(
        "is_active", "==", is_active)

    if array_flag > 1:
      raise ValidationError(
          "Please use only one of the following fields for filter at a "
          "time - author, learning_experience, learning_opportunity, version"
      )
    if fetch_archive:
      collection_manager = collection_manager.filter("is_archived", "==", True)
    elif fetch_archive is False:
      collection_manager = collection_manager.filter("is_archived", "==", False)

    curriculum_pathways = collection_manager.order("-created_time").offset(
        skip).fetch(limit)
    curriculum_pathways = [
        i.get_fields(reformat_datetime=True) for i in curriculum_pathways
    ]
    return {
        "success": True,
        "message": "Data fetched successfully",
        "data": curriculum_pathways
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


@router.get("/curriculum-pathway/{uuid}/nodes",
    response_model=GetCurriculumPathwayAliasResponseModel,
    responses={404: {
      "model": NotFoundErrorResponseModel
    }})
def fetch_all_nodes_for_alias(uuid: str, alias: Optional[str] = "discipline"):
  """
  This endpoint fetches all nodes belonging to the given alias eg. discipline.

  Parameters:
    uuid: (str) - uuid of the program (pathway).
    alias (optional): (str) - alias for which all the nodes are to be fetched.
                              Defaults to "discipline".
  Raises:
    ResourceNotFoundException: If the program (pathway) does not exist.
    Exception 500: Internal Server Error. Raised if something went wrong

  Returns:
    List of nodes of alias type
  """
  try:
    response = []
    if alias not in ALL_ALIASES:
      raise ValidationError(
        f"Invalid \"alias\" provided. Valid aliases are {ALL_ALIASES}")
    nodes = get_all_nodes_for_alias(uuid, "curriculum_pathways", alias, [])
    if nodes is None:
      raise ValidationError((f"Cannot fetch {alias} from {uuid} as it belongs "
                            f"to {alias}. Please use different uuid or alias."))
    else:
      for node in nodes:
        response.append(
          {
            "uuid": node["uuid"],
            "name": node["name"],
            "alias": node["alias"],
          }
        )

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
    "/curriculum-pathway/{uuid}",
    response_model=Union[CurriculumPathwayResponseModel,
                         CurriculumPathwayResponseModel2],
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_curriculum_pathway(uuid: str,
                           learner_id: Optional[str] = None,
                           fetch_tree: Optional[bool] = False,
                           frontend_response: Optional[bool] = True,
                           achievements: Optional[bool] = False,
                           references: Optional[bool] = False,
                           prerequisites: Optional[bool] = False
                           ):
  """The get curriculum pathway endpoint will return the curriculum pathway
  from firestore of which uuid is provided
  ### Args:
  uuid: `str`
    Unique identifier for curriculum pathway
  fetch_all_versions: `bool`
    Flag to determine whether to fetch all versions or not
  learner_id: `str`
    Query parameter to update the learning hierarchy with learner
    profile progress data
  frontend_response: `bool`
    Boolean flag to change the response to frontend's needs i.e.
    from nested dictionary
    to list of dictionary
  achievements: `bool`
    Boolean flag to expand achievements object  if True
  references: `bool`
    Boolean flag to expand references object  if True
  prerequisites: `bool`
    Boolean flag to expand prerequisites object  if True
  ### Raises:
  ResourceNotFoundException:
    If the curriculum pathway does not exist. <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Curriculum Pathway: `CurriculumPathwayResponseModel`
  """
  try:
    curriculum_pathway = CurriculumPathway.find_by_uuid(uuid)
    curriculum_pathway = curriculum_pathway.get_fields(reformat_datetime=True)
    curriculum_pathway["child_nodes_count"] = \
      sum(len(curriculum_pathway["child_nodes"][child_key]) for child_key in \
      curriculum_pathway["child_nodes"])
    learner_profile = None

    if learner_id:
      learner_profile = LearnerProfile.find_by_learner_id(learner_id)
      # ParentChildNodesHandler.current_progress = current_progress
    if fetch_tree:
      expansion_map = []
      expansion_list = []
      expansion_map.append("child_nodes")
      if references:
        expansion_map.append("references")
      if prerequisites:
        expansion_map.append("prerequisites")
      if achievements:
        expansion_list.append("achievements")
      curriculum_pathway = ParentChildNodesHandler.load_nodes_data(
        curriculum_pathway,
        "curriculum_pathways",
        learner_profile,
        expansion_map,
        expansion_list
        )
      curriculum_pathway = \
        ParentChildNodesHandler.load_immediate_parent_nodes_data(
              curriculum_pathway, learner_profile)
      if learner_id:
        count_completed_child_nodes = 0
        for child_key in curriculum_pathway["child_nodes"]:
          for child in curriculum_pathway["child_nodes"][child_key]:
            if "status" in child and child["status"].lower() == "completed":
              count_completed_child_nodes += 1
        curriculum_pathway["completed_child_nodes_count"] = \
          count_completed_child_nodes
      if frontend_response is True:
        curriculum_pathway = [transform_dict(curriculum_pathway)]

    return {
        "success": True,
        "message": "Successfully fetched the curriculum pathway",
        "data": curriculum_pathway
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
    "/curriculum-pathway",
    response_model=CurriculumPathwayResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def create_curriculum_pathway(input_curriculum_pathway: CurriculumPathwayModel):
  """The create curriculum pathway endpoint will add the curriculum pathway to
  the firestore if it does not exist.If the curriculum pathway exist then it
  will update the curriculum pathway
  ### Args:
  input_curriculum_pathway: `CurriculumPathwayModel`
    Input curriculum pathway to be inserted
  ### Raises:
  ResourceNotFoundException:
    If the curriculum pathway does not exist <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  UUID: `str`
    Unique identifier for curriculum pathway
  """
  try:
    input_curriculum_pathway_dict = {**input_curriculum_pathway.dict()}

    ParentChildNodesHandler.validate_parent_child_nodes_references(
        input_curriculum_pathway_dict)

    new_curriculum_pathway = CurriculumPathway()
    new_curriculum_pathway = new_curriculum_pathway.from_dict(
        input_curriculum_pathway_dict)
    new_curriculum_pathway.uuid = ""
    new_curriculum_pathway = CommonAPIHandler.check_item_is_locked(
        new_curriculum_pathway)
    new_curriculum_pathway.save()

    new_curriculum_pathway.uuid = new_curriculum_pathway.id
    new_curriculum_pathway.root_version_uuid = \
      new_curriculum_pathway.id
    new_curriculum_pathway.update()

    curriculum_pathway_fields = new_curriculum_pathway.get_fields(
        reformat_datetime=True)
    ParentChildNodesHandler.update_child_references(
        curriculum_pathway_fields, CurriculumPathway, operation="add")
    ParentChildNodesHandler.update_parent_references(
        curriculum_pathway_fields, CurriculumPathway, operation="add")

    return {
        "success": True,
        "message": "Successfully created the curriculum pathway",
        "data": curriculum_pathway_fields
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
    "/curriculum-pathway/{uuid}",
    response_model=CurriculumPathwayResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_curriculum_pathway(
    uuid: str,
    input_curriculum_pathway: UpdateCurriculumPathwayModel,
    request: Request,
    create_version: bool = False):
  """Update a curriculum pathway
  ### Args:
  input_curriculum_pathway: `UpdateCurriculumPathwayModel`
    Required body of the curriculum pathway
  ### Raises:
  ResourceNotFoundException:
    If the curriculum pathway does not exist <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Updated Curriculum Pathway: `CurriculumPathwayResponseModel`
  """
  try:
    input_cp_dict = {**input_curriculum_pathway.dict()}
    pathway = CurriculumPathway.find_by_uuid(uuid)
    # Update the previous active pathway status to False
    if input_cp_dict.get("is_active", None) and pathway.alias == "program":
      active_pathway = CurriculumPathway.find_active_pathway("program")
      if active_pathway:
        active_pathway.is_active = False
        active_pathway.update()

    if create_version:
      updated_doc_fields = \
        CommonAPIHandler.update_and_create_version(CurriculumPathway,
                                                   uuid,
                                                   input_cp_dict)
    else:
      # Updating the original doc
      updated_doc_fields = \
        CommonAPIHandler.update_document(CurriculumPathway,
                                         uuid,
                                         input_cp_dict)
    response = None
    if input_cp_dict.get("is_active", None) and pathway.alias == "program":
      nodes = fetch_all_nodes_for_alias(uuid, "discipline")["data"]
      headers = {"Authorization": request.headers.get("Authorization")}
      api_url = \
    f"{UM_BASE_URL}/association-groups/active-curriculum-pathway/update-all"
      response = put_method(url=api_url,
                            request_body={"program_id": uuid,
                                          "disciplines": nodes},
                            token=headers.get("Authorization"))

    if response and response.status_code != 200:
      #pylint: disable=broad-exception-raised
      raise Exception("Failed to update Association Groups. " +\
                      "Please update manually")
    return {
        "success": True,
        "message": "Successfully updated the curriculum pathway",
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
    "/curriculum-pathway/{uuid}",
    response_model=DeleteCurriculumPathway,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_curriculum_pathway(uuid: str):
  """Delete a curriculum pathway from firestore
  ### Args:
  uuid: `str`
    Unique ID of the curriculum pathway
  ### Raises:
  ResourceNotFoundException:
    If the curriculum pathway does not exist. <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Success/Fail Message: `JSON`
  """
  try:
    curriculum_pathway = CurriculumPathway.find_by_uuid(uuid)
    curriculum_pathway_fields = curriculum_pathway.get_fields(
        reformat_datetime=True)

    ParentChildNodesHandler.validate_parent_child_nodes_references(
        curriculum_pathway_fields)
    ParentChildNodesHandler.update_child_references(
        curriculum_pathway_fields, CurriculumPathway, operation="remove")
    ParentChildNodesHandler.update_parent_references(
        curriculum_pathway_fields, CurriculumPathway, operation="remove")

    CurriculumPathway.delete_by_uuid(curriculum_pathway.uuid)
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
    "/curriculum-pathway/import/json",
    response_model=CurriculumPathwayImportJsonResponse,
    name="Import Curriculum Pathway from JSON file",
    responses={413: {
        "model": PayloadTooLargeResponseModel
    }})
async def import_curriculum_pathways(json_file: UploadFile = File(...)):
  """Create curriculum pathways from json file
  ### Args:
  json_file: `UploadFile`
    Upload json file consisting of curriculum pathways.
  ### Raises:
  Exception 500:
    Internal Server Error. Raised if something fails
  ### Returns:
    Curriculum Pathway UUID: `CurriculumPathwayImportJsonResponse`
  """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
        f"File size is too large: {json_file.filename}"
      )
    await json_file.seek(0)
    final_output = json_import(
        json_file=json_file,
        json_schema=BasicCurriculumPathwayModel,
        model_obj=CurriculumPathway,
        object_name="curriculum pathways")
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
    "/curriculum-pathway/copy/{uuid}",
    response_model=CopyCurriculumPathwayModel,
    name="Copy a curriculum pathway",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def copy_curriculum_pathway(uuid: str):
  """Copy a curriculum pathway

  ### Args:
  uuid: `str`
    Unique identifier for curriculum pathway

  ### Raises:
  ResourceNotFoundException:
    If the curriculum pathway does not exist <br/>
  Exception 500:
    Internal Server Error if something went wrong

  ### Returns:
  Curriculum Pathway: `CurriculumPathwayModel`
  """
  try:
    curriculum_pathway_fields = CommonAPIHandler.create_copy(
        CurriculumPathway, uuid)
    return {
        "success": True,
        "message": "Successfully copied the curriculum pathway",
        "data": curriculum_pathway_fields
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
    "/curriculum-pathway/bulk-import/json",
    response_model=PathwayImportJsonResponse,
    name="Import Learning Hierarchy from JSON file",
    responses={413: {
        "model": PayloadTooLargeResponseModel
    }})
async def bulk_import_pathway(req: Request, json_file: UploadFile = File(...)):
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
        f"File size is too large: {json_file.filename}"
      )
    await json_file.seek(0)
    headers = {"Authorization": req.headers.get("authorization")}
    final_output = bulk_import(headers, json_file=json_file)
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


@router.delete(
    "/learning-hierarchy/{cp_id}",
    response_model=DeleteLearningPathway,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_hierarchy(cp_id: str,
                    delete_achievements: bool = False,
                    delete_skills: bool = False,
                    delete_competencies: bool = False):
  """Delete a curriculum pathway from firestore
  ### Args:
  uuid: `str`
    Unique ID of the curriculum pathway
  ### Raises:
  ResourceNotFoundException:
    If the curriculum pathway does not exist. <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Success/Fail Message: `JSON`
  """
  try:
    delete_hierarchy_handler(cp_id,
                            "curriculum_pathways",
                            delete_achievements,
                            delete_skills,
                            delete_competencies)

    return {}
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
