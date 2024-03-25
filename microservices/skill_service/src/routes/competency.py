""" Competency endpoints """
import traceback
from typing import Optional, List
from fastapi import APIRouter, UploadFile, File, Query
from common.models import SkillServiceCompetency, Skill
from common.utils.logging_handler import Logger
from common.utils.parent_child_nodes_handler import ParentChildNodesHandler
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from schemas.competency_schema import (
    CompetencyModel, GetCompetencyResponseModel, PostCompetencyResponseModel,
    UpdateCompetencyResponseModel, CompetencyImportJsonResponse,
    UpdateCompetencyModel, DeleteCompetency, AllCompetencyResponseModel,
    BasicCompetencyModel, CompetenciesSkillsResponse)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from services.json_import import json_import
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES
# pylint: disable = broad-except

router = APIRouter(
    tags=["Competency"],
    responses=ERROR_RESPONSES)


@router.get(
    "/competencies",
    response_model=AllCompetencyResponseModel,
    name="Get all Competencies")
def get_competencies(level: Optional[str] = None,
                     subject_code: Optional[str] = None,
                     course_code: Optional[str] = None,
                     source_name: Optional[str] = None,
                     skip: int = 0,
                     limit: int = 10):
  """The get competencies endpoint will return an array competencies from
  firestore

  Args:
      skip (int): Number of objects to be skipped
      limit (int): Size of competency array to be returned

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      AllCompetencyResponseModel: Array of Competency Object
  """
  try:
    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")

    if limit < 1:
      raise ValidationError\
        ("Invalid value passed to \"limit\" query parameter")

    collection_manager = SkillServiceCompetency.collection
    if level:
      collection_manager = collection_manager.filter("level", "==", level)
    if subject_code:
      collection_manager = collection_manager.filter("subject_code", "==",
                                                     subject_code)
    if course_code:
      collection_manager = collection_manager.filter("course_code", "==",
                                                     course_code)
    if source_name:
      collection_manager = collection_manager.filter("source_name", "==",
                                                     source_name)
    competencies = collection_manager.order("-created_time").offset(skip).fetch(
        limit)
    competencies = [i.get_fields(reformat_datetime=True) for i in competencies]
    return {
        "success": True,
        "message": "Data fetched successfully",
        "data": competencies
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
    "/competency/{uuid}",
    response_model=GetCompetencyResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_competency(uuid: str,
                  fetch_tree: Optional[bool] = False):
  """The get competency endpoint will return the competency from firestore of
  which uuid is provided

  Args:
      uuid (str): Unique identifier for competency
      fetch_tree: `bool`
        Flag to determine whether to fetch tree or not

  Raises:
      ResourceNotFoundException: If the competency does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      GetCompetencyResponseModel: Competency Object
  """
  try:
    competency = SkillServiceCompetency.find_by_uuid(uuid)
    competency_fields = competency.get_fields(reformat_datetime=True)

    if fetch_tree:
      ParentChildNodesHandler.load_child_nodes_data(competency_fields)
      ParentChildNodesHandler.load_immediate_parent_nodes_data(
          competency_fields)

    return {
        "success": True,
        "message": "Successfully fetched the competency",
        "data": competency_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/competency",
    response_model=PostCompetencyResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def create_competency(input_competency: CompetencyModel):
  """The post competency endpoint will add the competency in request body to the
  firestore

  Args:
      input_competency (CompetencyModel): input competency to be inserted

  Raises:
      ResourceNotFoundException: If the competency does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      PostCompetencyResponseModel: Skill Object
  """
  try:
    input_competency_dict = {**input_competency.dict()}
    ParentChildNodesHandler.validate_parent_child_nodes_references(
        input_competency_dict)

    new_competency = SkillServiceCompetency()
    new_competency = new_competency.from_dict(input_competency_dict)
    new_competency.uuid = ""
    new_competency.save()
    new_competency.uuid = new_competency.id
    new_competency.update()

    competency_fields = new_competency.get_fields(reformat_datetime=True)
    ParentChildNodesHandler.update_child_references(
        competency_fields, SkillServiceCompetency, operation="add")
    ParentChildNodesHandler.update_parent_references(
        competency_fields, SkillServiceCompetency, operation="add")

    return {
        "success": True,
        "message": "Successfully created the competency",
        "data": competency_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.put(
    "/competency/{uuid}",
    response_model=UpdateCompetencyResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_competency(uuid: str, input_competency: UpdateCompetencyModel):
  """Update a competency with the uuid passed in the request body

  Args:
      input_competency (UpdateCompetencyModel): Required body of the competency

  Raises:
      ResourceNotFoundException: If the competency does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      UpdateCompetencyResponseModel: Competency Object
  """
  try:
    existing_competency = SkillServiceCompetency.find_by_uuid(uuid)

    input_competency_dict = {**input_competency.dict(exclude_unset=True)}
    competency_fields = existing_competency.get_fields()

    ParentChildNodesHandler.compare_and_update_nodes_references(
        input_competency_dict, competency_fields, SkillServiceCompetency)

    for key, value in input_competency_dict.items():
      competency_fields[key] = value
    for key, value in competency_fields.items():
      setattr(existing_competency, key, value)

    existing_competency.update()
    competency_fields = existing_competency.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully updated the competency",
        "data": competency_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.delete(
    "/competency/{uuid}",
    response_model=DeleteCompetency,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_competency(uuid: str):
  """Delete a competency with the given uuid from firestore

  Args:
      uuid (str): Unique id of the competency

  Raises:
      ResourceNotFoundException: If the competency does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      JSON: Success/Fail Message
  """
  try:
    competency = SkillServiceCompetency.find_by_uuid(uuid)
    competency_fields = competency.get_fields(reformat_datetime=True)

    ParentChildNodesHandler.validate_parent_child_nodes_references(
        competency_fields)
    ParentChildNodesHandler.update_child_references(
        competency_fields, SkillServiceCompetency, operation="remove")
    ParentChildNodesHandler.update_parent_references(
        competency_fields, SkillServiceCompetency, operation="remove")

    SkillServiceCompetency.collection.delete(competency.key)

    return {"success": True, "message": "Successfully deleted the competency"}

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/competency/import/json",
    response_model=CompetencyImportJsonResponse,
    name="Import Competencies from JSON file",
    responses={413: {
        "model": PayloadTooLargeResponseModel
    }})
async def import_competencies(json_file: UploadFile = File(...)):
  """Create competencies from json file

  Args:
    json_file (UploadFile): Upload json file consisting of competencies.
    json_schema should match CompetencyModel

  Raises:
    Exception: 500 Internal Server Error if something fails

  Returns:
      CompetencyImportJsonResponse: Array of uuid's
  """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
        f"File size is too large: {json_file.filename}"
      )
    await json_file.seek(0)
    final_output = json_import(
        json_file=json_file,
        json_schema=BasicCompetencyModel,
        model_obj=SkillServiceCompetency,
        object_name="competencies")
    return final_output
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
    "/competencies/fetch_skills",
    response_model=CompetenciesSkillsResponse,
    name="Fetch all skills for list of competencies",
    responses={404: {
        "model": NotFoundErrorResponseModel
}}
)
def fetch_skills_from_competencies(
      competencies: List[str] = Query(default=[])):
  """Fetch skills from competencies

  Args:
    input_competencies (CompetenciesSkillsRequest): Request Model for
            list of competencies
  Raises:
    ResourceNotFoundException: If the competency does not exist
    Exception: 500 Internal Server Error if something went wrong

  Returns:
    CompetenciesSkillsResponse: Dictionary of competency_uuid as key and list
              of skill_uuid and skill_name as values
  """
  try:
    if not competencies:
      raise ValidationError("Atleast one competency id should provided in "+
                            "the query parameters")
    competency_to_skills = {}
    for competency_uuid in competencies:
      competency = SkillServiceCompetency.find_by_uuid(competency_uuid)
      skill_uuids = competency.child_nodes.get("skills", [])
      skills = []
      for skill_uuid in skill_uuids:
        skill = Skill.find_by_uuid(skill_uuid)
        skills.append({
            "skill_name": skill.name,
            "skill_id": skill.uuid})
      competency_to_skills[competency_uuid] = skills
    return {
      "success": True,
      "message": "Successfully fetched the child skills of competencies",
      "data": competency_to_skills
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
