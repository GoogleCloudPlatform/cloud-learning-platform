"""Line item  Endpoints"""
from fastapi import APIRouter
from config import ERROR_RESPONSES
from common.models import LineItem, Result, Score
from common.utils.errors import (ResourceNotFoundException, ValidationError)
from common.utils.http_exceptions import (InternalServerError, ResourceNotFound)
from schemas.line_item_schema import (LineItemModel, LineItemResponseModel,
                                      UpdateLineItemModel, DeleteLineItem,
                                      FullLineItemModel, BasicScoreModel,
                                      ScoreResponseModel, ResultResponseModel)
from schemas.error_schema import NotFoundErrorResponseModel
from typing import List

router = APIRouter(tags=["Line item"], responses=ERROR_RESPONSES)


@router.get(
    "/{context_id}/line_items",
    name="Get all line items",
    response_model=List[FullLineItemModel],
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_all_line_items(resource_id: str = None,
                       resource_link_id: str = None,
                       tag: str = None,
                       skip: int = 0,
                       limit: int = 10):
  """The get line items endpoint will return an array of line items
  from firestore
  ### Args:
  skip: `int`
    Number of line items to be skipped <br/>
  limit: `int`
    Size of line items array to be returned <br/>
  resource_id: `str`
    Tool resource ID in a line item <br/>
  resource_link_id: `str`
    Platform's resource link ID in a line item <br/>
  tag: `str`
    Tag associated with the line item <br/>
  ### Raises:
  ValueError:
    Raised when input args are outside range. <br/>
  Exception:
    Internal Server Error Raised. Raised if something went wrong
  ### Returns:
  Array of line items: `AllLineItemsResponseModel`
  """
  try:
    # TODO: Add API call to check if the context_id (course_id) exists
    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")

    if limit < 1:
      raise ValidationError("Invalid value passed to \"limit\" query parameter")

    collection_manager = LineItem.collection

    if resource_id:
      collection_manager = collection_manager.filter("resource_id", "==",
                                                     resource_id)
    if resource_link_id:
      collection_manager = collection_manager.filter("resource_link_id", "==",
                                                     resource_link_id)
    if tag:
      collection_manager = collection_manager.filter("tag", "==", tag)

    line_items = collection_manager.order("-created_time").offset(skip).fetch(
        limit)
    line_items = [i.get_fields(reformat_datetime=True) for i in line_items]

    return line_items
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/{context_id}/line_items/{uuid}",
    name="Get a specific line item",
    response_model=LineItemResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_line_item(uuid: str):
  """The get line item endpoint will return the line item
  from firestore of which uuid is provided
  ### Args:
  uuid: `str`
    Unique identifier for line item
  ### Raises:
  ResourceNotFoundException:
    If the line item does not exist. <br/>
  Exception:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  LineItem: `LineItemResponseModel`
  """
  try:
    # TODO: Add API call to check if the context_id (course_id) exists
    line_item = LineItem.find_by_uuid(uuid)
    line_item_fields = line_item.get_fields(reformat_datetime=True)
    return line_item_fields
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/{context_id}/line_items",
    name="Add a Line item",
    response_model=LineItemResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def create_line_item(input_line_item: LineItemModel):
  """The create line item endpoint will add a new line item to the firestore.
  ### Args:
  input_line_item: `LineItemModel`
    Input line item to be inserted
  ### Raises:
  ResourceNotFoundException:
    If the line item does not exist <br/>
  Exception:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Line item Data: `LineItemResponseModel`
  """
  try:
    # TODO: Add API call to check if the context_id (course_id) exists
    input_line_item_dict = {**input_line_item.dict()}

    new_line_item = LineItem()
    new_line_item = new_line_item.from_dict(input_line_item_dict)
    new_line_item.uuid = ""
    new_line_item.save()
    new_line_item.uuid = new_line_item.id
    new_line_item.update()
    line_item_fields = new_line_item.get_fields(reformat_datetime=True)

    return line_item_fields
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/{context_id}/line_items/{uuid}",
    response_model=LineItemResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_line_item(uuid: str, input_line_item: UpdateLineItemModel):
  """Update a line item
  ### Args:
  uuid: `str`
    Unique identifier for line item
  input_line_item: `UpdateLineItemModel`
    Required body of the line item
  ### Raises:
  ResourceNotFoundException:
    If the line item does not exist <br/>
  Exception:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Updated line item: `LineItemResponseModel`
  """
  try:
    # TODO: Add API call to check if the context_id (course_id) exists
    existing_line_item = LineItem.find_by_uuid(uuid)
    line_item_fields = existing_line_item.get_fields()
    print("line_item_fields", line_item_fields)
    input_line_item_dict = {**input_line_item.dict()}

    for key, value in input_line_item_dict.items():
      line_item_fields[key] = value
    for key, value in line_item_fields.items():
      setattr(existing_line_item, key, value)
    existing_line_item.update()
    line_item_fields = existing_line_item.get_fields(reformat_datetime=True)

    return line_item_fields

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/{context_id}/line_items/{uuid}",
    response_model=DeleteLineItem,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_line_item(uuid: str):
  """Delete a line item from firestore
  ### Args:
  uuid: `str`
    Unique ID of the line item
  ### Raises:
  ResourceNotFoundException:
    If the line item does not exist. <br/>
  Exception:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Success/Fail Message: `JSON`
  """
  try:
    # TODO: Add API call to check if the context_id (course_id) exists
    LineItem.delete_by_id(uuid)
    return {}
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/{context_id}/line_items/{line_item_id}/results",
    name="Get the result of a specific line item",
    response_model=ResultResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_result_of_line_item(line_item_id: str):
  """The get result of line item endpoint will return the result of a
  line item from firestore
  ### Args:
  line_item_id: `str`
    Unique identifier for line item
  ### Raises:
  ResourceNotFoundException:
    If the line item does not exist. <br/>
  Exception:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Result: `ResultResponseModel`
  """
  try:
    # TODO: Add API call to check if the context_id (course_id) exists
    result = Result.find_by_line_item_id(line_item_id)
    result_fields = result.get_fields(reformat_datetime=True)
    return result_fields
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/{context_id}/line_items/{line_item_id}/scores",
    name="Add a score for a Line item",
    response_model=ScoreResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def create_score_for_line_item(line_item_id: str, input_score: BasicScoreModel):
  """The create score for line item endpoint will add a score for a line item
  to the firestore.
  ### Args:
  input_score: `BasicScoreModel`
    Input line item to be inserted
  ### Raises:
  ResourceNotFoundException:
    If the line item does not exist <br/>
  Exception:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Score Data: `ScoreResponseModel`
  """
  try:
    # TODO: Add API call to check if the context_id (course_id) exists
    LineItem.find_by_id(line_item_id)
    input_score_dict = {**input_score.dict()}

    new_score = Score()
    new_score = new_score.from_dict(input_score_dict)
    new_score.save()
    score_fields = new_score.get_fields(reformat_datetime=True)

    return score_fields
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
