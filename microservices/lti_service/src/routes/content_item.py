"""LTI Content Item endpoints"""
from typing import Optional
from fastapi import APIRouter
from config import ERROR_RESPONSES
from common.models import LTIContentItem, Tool
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 ConflictError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, Conflict)
from schemas.content_item_schema import (LTIContentItemModel,
                                         LTIContentItemResponseModel,
                                         UpdateLTIContentItemModel,
                                         DeleteLTIContentItem,
                                         LTIContentItemSearchResponseModel,
                                         AllLTIContentItemsResponseModel)
from schemas.error_schema import NotFoundErrorResponseModel

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
      result = [content_item.get_fields(reformat_datetime=True)]
    return {
        "success": True,
        "message": "Successfully fetched the content items",
        "data": result
    }
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/content-items",
    name="Get all content items",
    response_model=AllLTIContentItemsResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_all_content_items(skip: int = 0,
                          limit: int = 10,
                          fetch_archive: Optional[bool] = None):
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
        "is_deleted", "==", False)
    if fetch_archive is not None:
      collection_manager = collection_manager\
                            .filter("is_archived", "==", fetch_archive)

    content_items = collection_manager.order("-created_timestamp").offset(
        skip).fetch(limit)
    content_items = [
        i.get_fields(reformat_datetime=True) for i in content_items
    ]

    return {
        "success": True,
        "message": "Content items has been fetched successfully",
        "data": content_items
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/content-item/{uuid}",
    name="Get a specific content item",
    response_model=LTIContentItemResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_content_item(uuid: str):
  """The get content item endpoint will return the content item
  from firestore of which uuid is provided
  ### Args:
  uuid: `str`
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
    content_item = LTIContentItem.find_by_uuid(uuid)
    content_item_fields = content_item.get_fields(reformat_datetime=True)
    return {
        "success": True,
        "message": f"Content item with '{uuid}' has been fetched successfully",
        "data": content_item_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
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
    Tool.find_by_uuid(input_content_item_dict.get("tool_id"))

    new_content_item = LTIContentItem()
    new_content_item = new_content_item.from_dict(input_content_item_dict)
    new_content_item.uuid = ""
    new_content_item.save()
    new_content_item.uuid = new_content_item.id
    new_content_item.update()
    content_item_fields = new_content_item.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Content item has been created successfully",
        "data": {
            **content_item_fields
        }
    }
  except ConflictError as e:
    raise Conflict(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/content-item/{uuid}",
    response_model=LTIContentItemResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_content_item(uuid: str,
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
    existing_content_item = LTIContentItem.find_by_uuid(uuid)
    content_item_fields = existing_content_item.get_fields()

    input_content_item_dict = {**input_content_item.dict()}

    if input_content_item_dict.get("tool_id"):
      Tool.find_by_uuid(input_content_item_dict.get("tool_id"))

    for key, value in input_content_item_dict.items():
      content_item_fields[key] = value
    for key, value in content_item_fields.items():
      setattr(existing_content_item, key, value)
    existing_content_item.update()
    content_item_fields = existing_content_item.get_fields(
        reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully updated the content item",
        "data": content_item_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/content-item/{uuid}",
    response_model=DeleteLTIContentItem,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_content_item(uuid: str):
  """Delete a content item from firestore
  ### Args:
  uuid: `str`
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
    LTIContentItem.delete_by_uuid(uuid)
    return {}
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
