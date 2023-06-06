""" Assessment Item endpoints """
from typing import Optional
from typing_extensions import Literal
from fastapi import APIRouter, UploadFile, File, Query
from common.models import AssessmentItem
from common.utils.logging_handler import Logger
from common.utils.sorting_logic import collection_sorting
from common.utils.common_api_handler import CommonAPIHandler
from common.utils.parent_child_nodes_handler import ParentChildNodesHandler
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from schemas.assessment_item_schema import (
    BasicAssessmentItemModel, AssessmentItemsImportJsonResponse,
    AssessmentItemModel, AssessmentItemModelResponse, UpdateAssessmentItemModel,
    DeleteAssessmentItem, AssessmentItemSearchModelResponse,
    AllAssessmentItemsModelResponse)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from services.json_import import json_import
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES

router = APIRouter(tags=["Assessment Items"], responses=ERROR_RESPONSES)

# pylint: disable = broad-except

@router.get(
    "/assessment-item/search", response_model=AssessmentItemSearchModelResponse)
def search_assessment_item(name: Optional[str] = None):
  """Search for assessment item based on the name

    Args:
        name(str): Name of the assessment. Defaults to None.

    Returns:
        AssessmentItemSearchModelResponse: List of assessment item objects
    """
  result = []
  if name:
    # fetch assessment item that matches name
    name_node_items = AssessmentItem.find_by_name(name)
    if name_node_items:
      result = [
          name_node_item.get_fields(reformat_datetime=True)
          for name_node_item in name_node_items
      ]
    return {
        "success": True,
        "message": "Successfully fetched the assessment item",
        "data": result
    }
  else:
    return BadRequest("Missing or invalid request parameters")


@router.get("/assessment-items", response_model=AllAssessmentItemsModelResponse)
def get_assessment_items(skip: int = Query(0, ge=0, le=2000),
                         limit: int = Query(10, ge=1, le=100),
                         sort_by: Optional[str] = "created_time",
                         sort_order: Optional[
                           Literal["ascending", "descending"]] = "descending"):
  """The get assessment items endpoint will return an array assessment items
    from firestore

    Args:
        skip (int): Number of objects to be skipped
        limit (int): Size of assessment item array to be returned
        sort_by (str): Data Model Fields name
        sort_order (str): ascending/descending

    Raises:
        Exception: 500 Internal Server Error if something went wrong

    Returns:
        AllAssessmentItemsModelResponse: Array of Assessment Item Object
    """
  try:
    collection_manager = AssessmentItem.collection
    assessment_items = collection_sorting(
      collection_manager=collection_manager, sort_by=sort_by,
      sort_order=sort_order, skip=skip, limit=limit)
    assessment_items = [
        i.get_fields(reformat_datetime=True) for i in assessment_items
    ]
    count = 10000
    response = {"records": assessment_items, "total_count": count}
    return {
        "success": True,
        "message": "Successfully fetched the assessment items",
        "data": response
    }
  except ValidationError as e:
    Logger.error(str(e))
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.error(str(e))
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(str(e))
    raise InternalServerError(str(e)) from e


@router.get(
    "/assessment-item/{uuid}",
    response_model=AssessmentItemModelResponse,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_assessment_item(uuid: str, fetch_tree: Optional[bool] = False):
  """The get assessment_item endpoint will return the assessment_item from
    firestore of which uuid is provided

    Args:
        uuid (str): Unique identifier for assessment_item

    Raises:
        ResourceNotFoundException: If the assessment_item does not exist
        Exception: 500 Internal Server Error if something went wrong

    Returns:
        AssessmentItemModel: AssessmentItem Object
    """
  try:
    assessment_item = AssessmentItem.find_by_id(uuid)
    assessment_item = assessment_item.get_fields(reformat_datetime=True)

    if fetch_tree:
      assessment_item = ParentChildNodesHandler.load_child_nodes_data(
          assessment_item)
      assessment_item = \
          ParentChildNodesHandler.load_immediate_parent_nodes_data(
              assessment_item)
    return {
        "success": True,
        "message": "Successfully fetched the assessment item",
        "data": assessment_item
    }
  except ResourceNotFoundException as e:
    Logger.error(str(e))
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(str(e))
    raise InternalServerError(str(e)) from e


@router.post("/assessment-item", response_model=AssessmentItemModelResponse)
def create_assessment_item(input_assessment_item: AssessmentItemModel):
  """The create assessment_item endpoint will add the assessment_item to the
    firestore if it does not exist.If the assessment_item exist then it will
    update the assessment_item.

    Args:
        input_assessment_item (AssessmentItemModel): input assessment_item to be
        inserted

    Raises:
        ResourceNotFoundException: If the assessment_item does not exist
        Exception: 500 Internal Server Error if something went wrong

    Returns:
        str: UUID(Unique identifier for assessment_item)
    """
  try:

    input_assessment_item_dict = {**input_assessment_item.dict()}

    ParentChildNodesHandler.validate_parent_child_nodes_references(
        input_assessment_item_dict)

    new_assessment_item = AssessmentItem()
    new_assessment_item = new_assessment_item.from_dict(
        input_assessment_item_dict)
    new_assessment_item.uuid = ""

    new_assessment_item.save()
    new_assessment_item.uuid = new_assessment_item.id
    new_assessment_item.update()
    assessment_item_fields = new_assessment_item.get_fields(
        reformat_datetime=True)

    ParentChildNodesHandler.update_child_references(
        assessment_item_fields, AssessmentItem, operation="add")
    ParentChildNodesHandler.update_parent_references(
        assessment_item_fields, AssessmentItem, operation="add")

    return {
        "success": True,
        "message": "Successfully created the assessment item",
        "data": assessment_item_fields
    }
  except Exception as e:
    Logger.error(str(e))
    raise InternalServerError(str(e)) from e


@router.put(
    "/assessment-item/{uuid}",
    response_model=AssessmentItemModelResponse,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_assessment_item(uuid: str,
                           input_assessment_item: UpdateAssessmentItemModel):
  """Update a assessment_item

    Args:
        input_assessment_item (AssessmentItemModel): Required body of
        assessment_item

    Raises:
        ResourceNotFoundException: If the assessment_item does not exist
        Exception: 500 Internal Server Error if something went wrong

    Returns:
        JSON: Success/Fail Message
    """
  try:

    input_assessment_dict = {**input_assessment_item.dict()}

    assessment_item_fields = CommonAPIHandler.update_document(
        AssessmentItem, uuid, input_assessment_dict)

    return {
        "success": True,
        "message": "Successfully updated the assessment item",
        "data": assessment_item_fields
    }
  except ResourceNotFoundException as e:
    Logger.error(str(e))
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(str(e))
    raise InternalServerError(str(e)) from e


@router.delete(
    "/assessment-item/{uuid}",
    response_model=DeleteAssessmentItem,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_assessment_item(uuid: str):
  """Delete a assessment_item from firestore

    Args:
        uuid (str): Unique id of the assessment_item

    Raises:
        ResourceNotFoundException: If the assessment_item does not exist
        Exception: 500 Internal Server Error if something went wrong

    Returns:
        JSON: Success/Fail Message
    """
  try:
    assessment_item = AssessmentItem.find_by_id(uuid)
    assessment_item_fields = assessment_item.get_fields(reformat_datetime=True)

    ParentChildNodesHandler.validate_parent_child_nodes_references(
        assessment_item_fields)
    ParentChildNodesHandler.update_child_references(
        assessment_item_fields, AssessmentItem, operation="remove")
    ParentChildNodesHandler.update_parent_references(
        assessment_item_fields, AssessmentItem, operation="remove")

    AssessmentItem.delete_by_uuid(assessment_item.uuid)

    return {
        "success": True,
        "message": "Successfully deleted the assessment item"
    }
  except ResourceNotFoundException as e:
    Logger.error(str(e))
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(str(e))
    raise InternalServerError(str(e)) from e


@router.post(
    "/assessment-item/import/json",
    response_model=AssessmentItemsImportJsonResponse,
    name="Import Assessment Items from JSON file",
    responses={413: {
        "model": PayloadTooLargeResponseModel
    }})
async def import_assessment_items(json_file: UploadFile = File(...)):
  """Create assessment_items from json file

  Args:
    json_file (UploadFile): Upload json file consisting of assessment_items.
    json_schema should match AssessmentItemModel

  Raises:
    Exception: 500 Internal Server Error if something fails
  """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
          f"File size is too large: {json_file.filename}")
    await json_file.seek(0)
    final_output = json_import(
        json_file=json_file,
        json_schema=BasicAssessmentItemModel,
        model_obj=AssessmentItem,
        object_name="assessment item")
    return final_output
  except PayloadTooLargeError as e:
    Logger.error(str(e))
    raise PayloadTooLarge(str(e)) from e
  except ValidationError as e:
    Logger.error(str(e))
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    Logger.error(str(e))
    raise InternalServerError(str(e)) from e
