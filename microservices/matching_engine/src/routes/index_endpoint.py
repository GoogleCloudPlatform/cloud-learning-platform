"""Route for index endpoint"""
from fastapi import APIRouter#, UploadFile, File
from schemas.index_endpoint_schema import (CreateIndexEndpointModel)
from utils.http_exceptions import (InternalServerError, CustomHTTPException)
from services.index_endpoint import IndexEndpointService
from config import ERROR_RESPONSES

router = APIRouter(prefix="/index-endpoint",
  responses=ERROR_RESPONSES)

# pylint: disable = broad-except


@router.get("")
def get_all_index_endpoints():
  """This route fetches all the index endpoints created in \
  matching engine service

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      List of IndexEndpointModel: IndexEndpoint Object
  """
  try:
    index_endpoints = IndexEndpointService().get_all_index_endpoints()
    return {
        "success": True,
        "message": "Successfully fetched all index endpoints",
        "data": index_endpoints
    }
  except Exception as e:
    if hasattr(e, "code"):
      raise CustomHTTPException(
        status_code=e.code, message=e.message,
        success=False, data=None) from e
    else:
      raise InternalServerError(str(e)) from e

@router.post("")
def create_index_endpoint(input_params: CreateIndexEndpointModel):
  """This route triggers an operation to create \
  index endpoint in matching engine service

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      OperationModel: Operation Object
  """
  try:
    input_params = {**input_params.dict()}
    operation = IndexEndpointService().create_index_endpoint(
      input_params["display_name"])
    return {
        "success": True,
        "message": "Successfully triggered a job to create ann index endpoint",
        "data": operation
    }
  except Exception as e:
    if hasattr(e, "code"):
      raise CustomHTTPException(
        status_code=e.code, message=e.message,
        success=False, data=None) from e
    else:
      raise InternalServerError(str(e)) from e

@router.get("/{index_endpoint_id}")
def get_index_endpoint(index_endpoint_id: str):
  """This route fetches an index endpoint given id
  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      IndexEndpointModel: IndexEndpoint Object
  """
  try:
    index_endpoint = IndexEndpointService().get_index_endpoint(
      index_endpoint_id)
    return {
        "success": True,
        "message": "Successfully fetched the index endpoint",
        "data": index_endpoint
    }
  except Exception as e:
    if hasattr(e, "code"):
      raise CustomHTTPException(
        status_code=e.code, message=e.message,
        success=False, data=None) from e
    else:
      raise InternalServerError(str(e)) from e

@router.delete("/{index_endpoint_id}")
def delete_index_endpoint(index_endpoint_id: str):
  """This route deletes an index endpoint given index_endpoint_id

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      OperationModel: Operation Object
  """
  try:
    operation = IndexEndpointService().delete_index_endpoint(index_endpoint_id)
    return {
        "success": True,
        "message": "Successfully triggered operation to delete index endpoint",
        "data": operation
    }
  except Exception as e:
    if hasattr(e, "code"):
      raise CustomHTTPException(
        status_code=e.code, message=e.message,
        success=False, data=None) from e
    else:
      raise InternalServerError(str(e)) from e

@router.get("/operation/{name}")
def get_index_endpoint_operation(name: str):
  """This route fetches the index endpoint operation status

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      OperationModel: Operation Object
  """
  try:
    operation = IndexEndpointService().get_index_endpoint_operation(name)
    return {
        "success": True,
        "message": "Successfully fetched the index endpoint operation",
        "data": operation
    }
  except Exception as e:
    if hasattr(e, "code"):
      raise CustomHTTPException(
        status_code=e.code, message=e.message,
        success=False, data=None) from e
    else:
      raise InternalServerError(str(e)) from e
