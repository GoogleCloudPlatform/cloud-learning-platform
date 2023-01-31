"""LTI Content Item endpoints"""
from fastapi import APIRouter
from config import ERROR_RESPONSES
from common.models import LTIContentItem, Tool
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 ConflictError)
from common.utils.logging_handler import Logger
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, Conflict)
from schemas.content_item_schema import (LTIContentItemModel,
                                         LTIContentItemResponseModel,
                                         UpdateLTIContentItemModel,
                                         DeleteLTIContentItem,
                                         LTIContentItemSearchResponseModel,
                                         AllLTIContentItemsResponseModel)
from schemas.error_schema import NotFoundErrorResponseModel
from services.line_item_service import create_new_content_item

router = APIRouter(
    tags=["Content Item CRUD Endpoints"], responses=ERROR_RESPONSES)


@router.get(
    "/content-item/search", response_model=LTIContentItemSearchResponseModel)
def search_content_item(tool_id: str):
  """Search for Content item based on the given search fields
  ### Args:
  tool_id: `str`
    Name of the Tool. Defaults to None.
  ### Raises:
  Exception 500:
    Internal Server Error. Raised if something went wrong.
  ### Returns:
  List of Content Items: `LTIContentItemSearchResponseModel`
  """
  result = []
  try:
    content_item = LTIContentItem.find_by_tool_id(tool_id)
    if content_item:
      tool_data = content_item.get_fields(reformat_datetime=True)
      tool_data["id"] = content_item.id
      result = [tool_data]
    return {
        "success": True,
        "message": "Successfully fetched the content items",
        "data": result
    }
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.get(
    "/content-items",
    name="Get all content items",
    response_model=AllLTIContentItemsResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_all_content_items(skip: int = 0, limit: int = 10):
  """The get content items endpoint will return an array of content
  items from firestore
  ### Args:
  skip: `int`
    Number of content items to be skipped <br/>
  limit: `int`
    Size of content items array to be returned <br/>
  ### Raises:
  ValidationError:
    Raised when any incorrect input field is provided. <br/>
  Exception 500
    Internal Server Error Raised. Raised if something went wrong
  ### Returns:
  Array of LTIContentItems: `AllLTIContentItemsResponseModel`
  """
  try:
    collection_manager = LTIContentItem.collection.filter(
        "deleted_at_timestamp", "==", None)

    content_items = collection_manager.order("-created_time").offset(
        skip).fetch(limit)
    content_items_list = []
    for i in content_items:
      content_item_data = i.get_fields(reformat_datetime=True)
      content_item_data["id"] = i.id
      content_items_list.append(content_item_data)

    return {
        "success": True,
        "message": "Content items has been fetched successfully",
        "data": content_items_list
    }
  except ValidationError as e:
    Logger.error(e)
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.get(
    "/content-item/{content_item_id}",
    name="Get a specific content item",
    response_model=LTIContentItemResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_content_item(content_item_id: str):
  """The get content item endpoint will return the content item
  from firestore of which content_item_id is provided
  ### Args:
  content_item_id: `str`
    Unique identifier for content item
  ### Raises:
  ResourceNotFoundException:
    If the content_item does not exist. <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  LTIContentItem: `LTIContentItemResponseModel`
  """
  try:
    content_item = LTIContentItem.find_by_id(content_item_id)
    content_item_fields = content_item.get_fields(reformat_datetime=True)
    content_item_fields["id"] = content_item.id

    msg = f"Content item with '{content_item_id}' has been fetched successfully"
    return {"success": True, "message": msg, "data": content_item_fields}
  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.post(
    "/content-item",
    name="Register a Content item",
    response_model=LTIContentItemResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def create_content_item(input_content_item: LTIContentItemModel):
  """The create content item endpoint will add the content_item to the
  firestore if it does not exist.If the content item exist then it will
  update the content item
  ### Args:
  input_content_item: `LTIContentItemModel`
    Input content item to be inserted
  ### Raises:
  ResourceNotFoundException:
    If the tool linked with the content item does not exist <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  UUID: `str`
    Unique identifier for content_item
  """
  try:
    input_content_item_dict = {**input_content_item.dict()}
    Tool.find_by_id(input_content_item_dict.get("tool_id"))

    content_item_fields = create_new_content_item(input_content_item_dict)

    return {
        "success": True,
        "message": "Content item has been created successfully",
        "data": {
            **content_item_fields
        }
    }
  except ConflictError as e:
    Logger.error(e)
    raise Conflict(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.put(
    "/content-item/{content_item_id}",
    response_model=LTIContentItemResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_content_item(content_item_id: str,
                        input_content_item: UpdateLTIContentItemModel):
  """Update a content_item
  ### Args:
  input_content_item: `UpdateLTIContentItemModel`
    Required body of the content item
  ### Raises:
  ResourceNotFoundException:
    If the tool linked with the content item does not exist <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Updated LTIContentItem: `LTIContentItemResponseModel`
  """
  try:
    existing_content_item = LTIContentItem.find_by_id(content_item_id)
    content_item_fields = existing_content_item.get_fields()

    input_content_item_dict = {**input_content_item.dict()}

    if input_content_item_dict.get("tool_id"):
      Tool.find_by_id(input_content_item_dict.get("tool_id"))

    for key, value in input_content_item_dict.items():
      content_item_fields[key] = value
    for key, value in content_item_fields.items():
      setattr(existing_content_item, key, value)
    existing_content_item.update()
    content_item_fields = existing_content_item.get_fields(
        reformat_datetime=True)
    content_item_fields["id"] = existing_content_item.id
    return {
        "success": True,
        "message": "Successfully updated the content item",
        "data": content_item_fields
    }
  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.delete(
    "/content-item/{content_item_id}",
    response_model=DeleteLTIContentItem,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_content_item(content_item_id: str):
  """Delete a content item from firestore
  ### Args:
  content_item_id: `str`
    Unique ID of the content item
  ### Raises:
  ResourceNotFoundException:
    If the content item does not exist. <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Success/Fail Message: `JSON`
  """
  try:
    LTIContentItem.find_by_id(content_item_id)
    LTIContentItem.delete_by_id(content_item_id)
    return {}
  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e
