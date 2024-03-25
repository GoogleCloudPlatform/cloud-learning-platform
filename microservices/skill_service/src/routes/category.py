""" Category endpoints """
from typing import Optional
from fastapi import APIRouter, UploadFile, File
from common.models import Category
from common.utils.parent_child_nodes_handler import ParentChildNodesHandler
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound,
                                          PayloadTooLarge)
from schemas.category_schema import (
    CategoryModel, UpdateCategoryModel, GetCategoryResponseModel,
    PostCategoryResponseModel, UpdateCategoryResponseModel,
    CategoryImportJsonResponse, DeleteCategory, AllCategoryResponseModel,
    BasicCategoryModel)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from services.json_import import json_import
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES
# pylint: disable = broad-except

router = APIRouter(
    tags=["Category"],
    responses=ERROR_RESPONSES)


@router.get(
    "/categories",
    response_model=AllCategoryResponseModel,
    name="Get all Categories")
def get_categories(source_name: Optional[str] = None,
                   skip: int = 0,
                   limit: int = 10):
  """The get categories endpoint will return an array categories from
  firestore

  Args:
      skip (int): Number of objects to be skipped
      limit (int): Size of category array to be returned

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      AllCategoryResponseModel: Array of Category Object
  """
  try:
    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")

    if limit < 1:
      raise ValidationError("Invalid value passed to \"limit\" \
        query parameter")
    collection_manager = Category.collection
    if source_name:
      collection_manager = collection_manager.filter("source_name", "==",
                                                     source_name)
    categories = collection_manager.order("-created_time").offset(skip).fetch(
        limit)
    categories = [i.get_fields(reformat_datetime=True) for i in categories]
    return {
        "success": True,
        "message": "Data fetched successfully",
        "data": categories
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/category/{uuid}",
    response_model=GetCategoryResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_category(uuid: str,
                fetch_tree: Optional[bool] = False):
  """The get category endpoint will return the category from firestore of which
  uuid is provided

  Args:
      uuid (str): Unique identifier for category
      fetch_tree: `bool`
        Flag to determine whether to fetch tree or not

  Raises:
      ResourceNotFoundException: If the category does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      GetCategoryResponseModel: Category Object
  """
  try:
    category = Category.find_by_uuid(uuid)
    category_fields = category.get_fields(reformat_datetime=True)

    if fetch_tree:
      ParentChildNodesHandler.load_child_nodes_data(category_fields)
      ParentChildNodesHandler.load_immediate_parent_nodes_data(category_fields)

    return {
        "success": True,
        "message": "Successfully fetched the category",
        "data": category_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post("/category", response_model=PostCategoryResponseModel)
def create_category(input_category: CategoryModel):
  """The create category endpoint will add the category in request body to the
  firestore

  Args:
      input_category (CategoryModel): input category to be inserted

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      PostCategoryResponseModel: Category Object
  """
  try:
    input_category_dict = {**input_category.dict()}
    ParentChildNodesHandler.validate_parent_child_nodes_references(
        input_category_dict)

    new_category = Category()
    new_category = new_category.from_dict(input_category_dict)
    new_category.uuid = ""
    new_category.save()
    new_category.uuid = new_category.id
    new_category.update()

    category_fields = new_category.get_fields(reformat_datetime=True)
    ParentChildNodesHandler.update_child_references(
        category_fields, Category, operation="add")
    ParentChildNodesHandler.update_parent_references(
        category_fields, Category, operation="add")

    return {
        "success": True,
        "message": "Successfully created the category",
        "data": category_fields
    }

  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/category/{uuid}",
    response_model=UpdateCategoryResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_category(uuid: str, input_category: UpdateCategoryModel):
  """Update a category with the uuid passed in the request body

  Args:
      input_category (CategoryModel): Required body of the category

  Raises:
      ResourceNotFoundException: If the category does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      UpdateCategoryResponseModel: Category Object
  """
  try:
    existing_category = Category.find_by_uuid(uuid)

    input_category_dict = {**input_category.dict(exclude_unset=True)}
    category_fields = existing_category.get_fields()

    ParentChildNodesHandler.compare_and_update_nodes_references(
        input_category_dict, category_fields, Category)

    for key, value in input_category_dict.items():
      category_fields[key] = value
    for key, value in category_fields.items():
      setattr(existing_category, key, value)

    existing_category.update()
    category_fields = existing_category.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully updated the category",
        "data": category_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/category/{uuid}",
    response_model=DeleteCategory,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_category(uuid: str):
  """Delete a category with the given uuid from firestore

  Args:
      uuid (str): Unique id of the category

  Raises:
      ResourceNotFoundException: If the category does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      JSON: Success/Fail Message
  """
  try:
    category = Category.find_by_uuid(uuid)
    category_fields = category.get_fields(reformat_datetime=True)

    ParentChildNodesHandler.validate_parent_child_nodes_references(
        category_fields)
    ParentChildNodesHandler.update_child_references(
        category_fields, Category, operation="remove")
    ParentChildNodesHandler.update_parent_references(
        category_fields, Category, operation="remove")

    Category.collection.delete(category.key)

    return {"success": True, "message": "Successfully deleted the category"}

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/category/import/json",
    response_model=CategoryImportJsonResponse,
    name="Import Categories from JSON file",
    responses={413: {
        "model": PayloadTooLargeResponseModel
    }})
async def import_categories(json_file: UploadFile = File(...)):
  """Create categories from json file

  Args:
    json_file (UploadFile): Upload json file consisting of categories.
    json_schema should match CategoryModel

  Raises:
    Exception: 500 Internal Server Error if something fails

  Returns:
    CategoryImportJsonResponse: Array of uuid's
  """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
        f"File size is too large: {json_file.filename}"
      )
    await json_file.seek(0)
    final_output = json_import(
        json_file=json_file,
        json_schema=BasicCategoryModel,
        model_obj=Category,
        object_name="categories")
    return final_output
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
