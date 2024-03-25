"""Route for index"""
from fastapi import APIRouter
from schemas.index_schema import (CreateIndexModel,UpdateIndexModel)
from utils.http_exceptions import (InternalServerError, CustomHTTPException)
from services.index import IndexService
from config import ERROR_RESPONSES

router = APIRouter(prefix="/index",
  responses=ERROR_RESPONSES)

# pylint: disable = broad-except


@router.get("")
def get_all_indexes():
  """This route fetches all the indexes created in matching engine service

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      List of IndexModel: Index Object
  """
  try:
    indexes = IndexService().get_all_indexes()
    return {
        "success": True,
        "message": "Successfully fetched all indexes",
        "data": indexes
    }
  except Exception as e:
    if hasattr(e, "code"):
      raise CustomHTTPException(
        status_code=e.code, message=e.message,
        success=False, data=None) from e
    else:
      raise InternalServerError(str(e)) from e

@router.post("")
def create_index(input_params: CreateIndexModel):
  """This route triggers an operation to create index in matching engine service

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      OperationModel: Operation Object
  """
  try:
    input_params = {**input_params.dict()}
    operation = IndexService().create_index(input_params)
    return {
        "success": True,
        "message": "Successfully triggered a job to create ann index",
        "data": operation
    }
  except Exception as e:
    if hasattr(e, "code"):
      raise CustomHTTPException(
        status_code=e.code, message=e.message,
        success=False, data=None) from e
    else:
      raise InternalServerError(str(e)) from e

@router.get("/{index_id}")
def get_index(index_id: str):
  """This route fetches an index from matching engine service given index_id

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      IndexModel: Index Object
  """
  try:
    index = IndexService().get_index(index_id)
    return {
        "success": True,
        "message": "Successfully fetched the index",
        "data": index
    }
  except Exception as e:
    if hasattr(e, "code"):
      raise CustomHTTPException(
        status_code=e.code, message=e.message,
        success=False, data=None) from e
    else:
      raise InternalServerError(str(e)) from e

@router.put("/{index_id}")
def update_index(index_id: str, input_params: UpdateIndexModel):
  """This route triggers an operation to update a particular index

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      OperationModel: Operation Object
  """
  try:
    input_params = {**input_params.dict()}
    operation = IndexService().update_index(index_id, input_params)
    return {
        "success": True,
        "message": "Successfully triggered a job to update the index",
        "data": operation
    }
  except Exception as e:
    if hasattr(e, "code"):
      raise CustomHTTPException(
        status_code=e.code, message=e.message,
        success=False, data=None) from e
    else:
      raise InternalServerError(str(e)) from e

@router.delete("/{index_id}")
def delete_index(index_id: str):
  """This route deletes an index given index_id

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      OperationModel: Operation Object
  """
  try:
    operation = IndexService().delete_index(index_id)
    return {
        "success": True,
        "message": "Successfully triggered operation to delete the index",
        "data": operation
    }
  except Exception as e:
    if hasattr(e, "code"):
      raise CustomHTTPException(
        status_code=e.code, message=e.message,
        success=False, data=None) from e
    else:
      raise InternalServerError(str(e)) from e

@router.get("/operation/")
def get_index_operation(name: str):
  """This route fetches the index operation status

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      OperationModel: Operation Object
  """
  try:
    operation = IndexService().get_index_operation(name)
    return {
        "success": True,
        "message": "Successfully fetched the index operation",
        "data": operation
    }
  except Exception as e:
    if hasattr(e, "code"):
      raise CustomHTTPException(
        status_code=e.code, message=e.message,
        success=False, data=None) from e
    else:
      raise InternalServerError(str(e)) from e
