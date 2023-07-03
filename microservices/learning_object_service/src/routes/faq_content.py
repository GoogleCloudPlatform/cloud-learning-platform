""" FAQ endpoints """
import traceback
from fastapi import APIRouter, Query
from schemas.error_schema import NotFoundErrorResponseModel
from schemas.faq_schema import (GetFAQResponseModel, SearchFAQResponseModel,
                                UpdateFAQResponseModel, DeleteFAQResponseModel,
                                CreateFAQResponseModel, FAQModel)
from common.models import FAQContent, CurriculumPathway
from common.utils.errors import (ResourceNotFoundException, ValidationError)
from common.utils.http_exceptions import (BadRequest, ResourceNotFound)
from common.utils.logging_handler import Logger
from common.utils.gcs_adapter import is_valid_path
from common.utils.sorting import (get_sorted_list)
from common.utils.pagination import (get_slice)
from config import (CONTENT_SERVING_BUCKET, ERROR_RESPONSES, FAQ_BASE_PATH)

# pylint: disable = line-too-long
# pylint: disable = broad-except
router = APIRouter(tags=["FAQ Content"], responses=ERROR_RESPONSES)

@router.get(
    "/faq/{uuid}",
    name="Get FAQ by UUID",
    response_model=GetFAQResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_faq_by_uuid(uuid: str):
  """Get FAQ by UUID"""
  try:
    faq_content = FAQContent.find_by_uuid(uuid)
    faq_content_dict = faq_content.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully Fetched FAQ by UUID",
        "data": faq_content_dict
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e

@router.get(
    "/faq",
    name="Get All FAQs",
    response_model=SearchFAQResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def filter_faq(skip: int = Query(0, ge=0, le=2000),
               limit: int = Query(10, ge=1, le=100),
               curriculum_pathway_id: str = None):
  """Get all FAQs"""
  try:
    collection_manager = FAQContent.collection.filter("is_deleted", "==", False)
    if curriculum_pathway_id is not None:

      _ = CurriculumPathway.find_by_uuid(curriculum_pathway_id)
      collection_manager = collection_manager.filter("curriculum_pathway_id", "==",
                                                      curriculum_pathway_id)

    sorted_list = get_sorted_list(collection_manager, sort_order="descending")
    faq_contents = get_slice(sorted_list,skip,limit)

    return {
        "success": True,
        "message": "Successfully Fetched FAQs",
        "data": faq_contents
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e

@router.post(
    "/faq",
    name="Create FAQ",
    response_model=CreateFAQResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def create_faq(input_faq: FAQModel):
  """create faq

    Args:
      input_faq (FAQModel): input faq to be inserted
      curriculum_pathway_id in input_faq should be of alias type program

    Returns:
      CreateFAQResponseModel: faq object
  """
  try:

    input_faq_dict = input_faq.dict()

    if input_faq.dict().get("curriculum_pathway_id") is not None:
      curriculum_pathway = CurriculumPathway.find_by_uuid(input_faq_dict["curriculum_pathway_id"])
      if curriculum_pathway.alias != "program":
        raise ValidationError("The curriculum_pathway_id is not of alias type program")

    collection_manager = FAQContent.collection.filter("is_deleted", "==", False)
    collection_manager = collection_manager.filter("curriculum_pathway_id", "==",
                                                      input_faq_dict["curriculum_pathway_id"])
    faq_doc = collection_manager.get()

    if faq_doc is not None:
      msg = f"""Curriculum Pathway {input_faq_dict["curriculum_pathway_id"]}"""
      msg += " is already linked to an FAQ."
      raise ValidationError(msg)

    # Validate FAQ resource_path
    if input_faq_dict.get("resource_path") is not None:
      input_path = input_faq_dict["resource_path"]

      # Resolve resource_path discrepencies
      actual_path = ""
      if FAQ_BASE_PATH in input_path:
        actual_path = input_path
      else:
        actual_path = f"{FAQ_BASE_PATH}/{input_path}"

      # Check if new path is valid
      path_exists = is_valid_path(f"gs://{CONTENT_SERVING_BUCKET}/{actual_path}")
      if path_exists is False:
        raise ResourceNotFoundException(
          "Provided resource path does not exist on GCS bucket")

    new_faq_content = FAQContent()
    new_faq_content = new_faq_content.from_dict({**input_faq_dict})
    new_faq_content.uuid = ""

    new_faq_content.save()
    new_faq_content.uuid = new_faq_content.id

    new_faq_content.update()

    faq_content_dict = new_faq_content.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully Created FAQ",
        "data": faq_content_dict
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e

@router.put(
    "/faq/{faq_uuid}",
    name="Update FAQ",
    response_model=UpdateFAQResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_faq(faq_uuid: str, input_faq: FAQModel):
  """
    Update faq

    -------------------------------------------------------
    Args:
      faq_uuid: UUID of the FAQ document
      input_faq (FAQModel): input faq to be inserted

    -------------------------------------------------------
    Returns:
      UpdateFAQResponseModel: faq object
  """
  try:

    faq_doc = FAQContent.find_by_uuid(faq_uuid)

    input_faq_dict = input_faq.dict(exclude_unset=True)

    # Handle Curriculum Pathway ID change
    if input_faq_dict.get("curriculum_pathway_id") is not None:

      # check if new Curriculum Pathway id is Valid
      curriculum_pathway = CurriculumPathway.find_by_uuid(input_faq_dict["curriculum_pathway_id"])
      if curriculum_pathway.alias != "program":
        raise ValidationError("The curriculum_pathway_id is not of alias type program")

      # check if Curriculum Pathway is already in use
      collection_manager = FAQContent.collection.filter("is_deleted", "==", False)
      collection_manager = collection_manager.filter("curriculum_pathway_id", "==",
                                                        input_faq_dict["curriculum_pathway_id"])
      existing_faq_with_cp = collection_manager.get()

      if existing_faq_with_cp is not None:
        if existing_faq_with_cp.uuid != faq_doc.uuid:
          msg = f"""Curriculum Pathway {input_faq_dict["curriculum_pathway_id"]}"""
          msg += " is already linked to an FAQ."
          raise ValidationError(msg)

    # Handle Resource Path change
    if input_faq_dict.get("resource_path") is not None:
      input_path = input_faq_dict["resource_path"]

      # Resolve resource_path discrepencies
      actual_path = ""
      if FAQ_BASE_PATH in input_path:
        actual_path = input_path
      else:
        actual_path = f"{FAQ_BASE_PATH}/{input_path}"

      # Check if new path is valid
      path_exists = is_valid_path(f"gs://{CONTENT_SERVING_BUCKET}/{actual_path}")
      if path_exists is False:
        raise ResourceNotFoundException(
          "Provided resource path does not exist on GCS bucket")

    # Update fields of FAQ document
    for key,value in input_faq_dict.items():
      setattr(faq_doc, key,value)

    faq_doc.update()

    faq_content_dict = faq_doc.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully updated FAQ",
        "data": faq_content_dict
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e

@router.delete(
    "/faq/{faq_uuid}",
    name="Delete FAQ",
    response_model=DeleteFAQResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_faq(faq_uuid: str):
  """
    Delete Faq document
    -------------------------------------------------------
    Args:
      faq_uuid (str): UUID of the FAQ document

    -------------------------------------------------------
    Note:
      This API does not delete the FAQ contents from CGS

  """
  try:

    _=FAQContent.find_by_uuid(faq_uuid)

    # TODO: delete FAQ contents from GCS

    FAQContent.delete_by_id(faq_uuid)

    return {
        "success": True,
        "message": "Successfully deleted FAQ"
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e

@router.put(
    "/faq/{faq_uuid}/developer-api",
    name="Update FAQ Developer API",
    response_model=UpdateFAQResponseModel,
    include_in_schema=False,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_faq_developer_api(faq_uuid: str, input_faq: FAQModel):
  """
    Update faq Developer API

    -------------------------------------------------------
    Args:
      faq_uuid: UUID of the FAQ document
      input_faq (FAQModel): input faq to be inserted

    -------------------------------------------------------
    Returns:
      UpdateFAQResponseModel: faq object
  """
  try:

    faq_doc = FAQContent.find_by_uuid(faq_uuid)

    input_faq_dict = input_faq.dict()

    # Update fields of FAQ document
    for key,value in input_faq_dict.items():
      setattr(faq_doc, key,value)

    faq_doc.update()

    faq_content_dict = faq_doc.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully updated FAQ",
        "data": faq_content_dict
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e
