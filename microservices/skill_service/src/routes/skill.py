""" Skill endpoints """
import traceback
from typing import Optional
from fastapi import APIRouter, UploadFile, File
from common.models import Skill
from common.utils.logging_handler import Logger
from common.utils.parent_child_nodes_handler import ParentChildNodesHandler
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from services.json_import import json_import
from schemas.skill_schema import (SkillModel, UpdateSkillModel, DeleteSkill,
                                  GetSkillResponseModel, PostSkillResponseModel,
                                  UpdateSkillResponseModel,
                                  SkillImportJsonResponse,
                                  AllSkillsResponseModel, BasicSkillModel)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES
# pylint: disable = broad-except

router = APIRouter(
    tags=["Skill"],
    responses=ERROR_RESPONSES)


@router.get(
    "/skills", response_model=AllSkillsResponseModel, name="Get All Skills")
def get_skills(creator: Optional[str] = None,
               source_name: Optional[str] = None,
               skip: int = 0,
               limit: int = 10):
  """The get skills endpoint will return an array skills from firestore

  Args:
      skip (int): Number of objects to be skipped
      limit (int): Size of skill array to be returned

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      AllSkillsResponseModel: Array of Skill Object
  """
  try:
    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")

    if limit < 1:
      raise ValidationError\
        ("Invalid value passed to \"limit\" query parameter")
    collection_manager = Skill.collection
    if creator:
      collection_manager = collection_manager.filter("creator", "==", creator)
    if source_name:
      collection_manager = collection_manager.filter("source_name", "==",
                                                      source_name)
    skills = collection_manager.order("-created_time").offset(skip).fetch(limit)
    skills = [i.get_fields(reformat_datetime=True) for i in skills]
    return {
        "success": True,
        "message": "Data fetched successfully",
        "data": skills
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.get(
    "/skill/{uuid}",
    response_model=GetSkillResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_skill(uuid: str,
              fetch_tree: Optional[bool] = False):
  """The get skill endpoint will return the skill from firestore of which uuid
  is provided

  Args:
      uuid (str): Unique identifier for skill
      fetch_tree: `bool`
        Flag to determine whether to fetch tree or not
  Raises:
      ResourceNotFoundException: If the skill does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      GetSkillResponseModel: Skill Object
  """
  try:
    skill = Skill.find_by_uuid(uuid)
    skill_fields = skill.get_fields(reformat_datetime=True)

    if fetch_tree:
      ParentChildNodesHandler.load_child_nodes_data(skill_fields)
      ParentChildNodesHandler.load_immediate_parent_nodes_data(skill_fields)

    return {
        "success": True,
        "message": "Successfully fetched the skill",
        "data": skill_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.post("/skill", response_model=PostSkillResponseModel)
def create_skill(input_skill: SkillModel):
  """The post skill endpoint will add the given skill in request body to the
  firestore

  Args:
      input_skill (SkillModel): input skill to be inserted

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      PostSkillResponseModel: Skill Object
  """
  try:
    input_skill_dict = {**input_skill.dict()}

    ParentChildNodesHandler.validate_parent_child_nodes_references(
      input_skill_dict)

    new_skill = Skill()
    new_skill = new_skill.from_dict(input_skill_dict)
    new_skill.uuid = ""
    new_skill.save()
    new_skill.uuid = new_skill.id
    new_skill.update()

    skill_fields = new_skill.get_fields(reformat_datetime=True)
    ParentChildNodesHandler.update_child_references(
        skill_fields, Skill, operation="add")
    ParentChildNodesHandler.update_parent_references(
        skill_fields, Skill, operation="add")

    return {
        "success": True,
        "message": "Successfully created the skill",
        "data": skill_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.put(
    "/skill/{uuid}",
    response_model=UpdateSkillResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_skill(uuid: str, input_skill: UpdateSkillModel):
  """Update a skill with the uuid passed in the request body

  Args:
      input_skill (SkillModel): Required body of the skill

  Raises:
      ResourceNotFoundException: If the skill does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      UpdateSkillResponseModel: Skill Object
  """
  try:
    existing_skill = Skill.find_by_uuid(uuid)

    input_skill_dict = {**input_skill.dict(exclude_unset=True)}
    skill_fields = existing_skill.get_fields()

    ParentChildNodesHandler.compare_and_update_nodes_references(
        input_skill_dict, skill_fields, Skill)

    for key, value in input_skill_dict.items():
      skill_fields[key] = value
    for key, value in skill_fields.items():
      setattr(existing_skill, key, value)

    existing_skill.update()
    skill_fields = existing_skill.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully updated the skill",
        "data": skill_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.delete(
    "/skill/{uuid}",
    response_model=DeleteSkill,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_skill(uuid: str):
  """Delete a skill with the given uuid from firestore

  Args:
      uuid (str): Unique id of the skill

  Raises:
      ResourceNotFoundException: If the skill does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      JSON: Success/Fail Message
  """
  try:
    skill = Skill.find_by_uuid(uuid)
    skill_fields = skill.get_fields(reformat_datetime=True)

    ParentChildNodesHandler.validate_parent_child_nodes_references(skill_fields)
    ParentChildNodesHandler.update_child_references(
        skill_fields, Skill, operation="remove")
    ParentChildNodesHandler.update_parent_references(
        skill_fields, Skill, operation="remove")

    Skill.collection.delete(skill.key)

    return {"success": True, "message": "Successfully deleted the skill"}

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/skill/import/json",
    response_model=SkillImportJsonResponse,
    name="Import Skills from JSON file",
    responses={413: {
        "model": PayloadTooLargeResponseModel
    }})
async def import_skills(json_file: UploadFile = File(...)):
  """Create skills from json file

  Args:
    json_file (UploadFile): Upload json file consisting of skills.
    json_schema should match SkillModel

  Raises:
    Exception: 500 Internal Server Error if something fails

  Returns:
      SkillImportJsonResponse: Array of uuid's
  """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
        f"File size is too large: {json_file.filename}"
      )
    await json_file.seek(0)
    final_output = json_import(
        json_file=json_file,
        json_schema=BasicSkillModel,
        model_obj=Skill,
        object_name="skills")
    return final_output
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
