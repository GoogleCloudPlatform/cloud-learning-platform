"""Route for deploy"""
from fastapi import APIRouter
from utils.http_exceptions import (InternalServerError, CustomHTTPException)
from schemas.deploy_schema import (DeployIndexModel,UndeployIndexModel)
from services.deploy import DeployIndexService
from config import ERROR_RESPONSES

router = APIRouter(prefix="/deploy",
  responses=ERROR_RESPONSES)

# pylint: disable = broad-except

@router.post("")
def deploy_index(input_params: DeployIndexModel):
  """This route deploys an index to an index endpoint

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      OperationModel: Operation Object
  """
  try:
    input_params = {**input_params.dict()}
    operation = DeployIndexService().deploy_index(input_params)
    return {
        "success": True,
        "message": "Successfully triggered a job to deploy\
        the index to given index endpoint",
        "data": operation
    }
  except Exception as e:
    if hasattr(e, "code"):
      raise CustomHTTPException(
        status_code=e.code, message=e.message,
        success=False, data=None) from e
    else:
      raise InternalServerError(str(e)) from e

@router.delete("")
def undeploy_index(input_params: UndeployIndexModel):
  """This route undeploys an index from given index endpoint

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      OperationModel: Operation Object
  """
  try:
    input_params = {**input_params.dict()}
    operation = DeployIndexService().undeploy_index(input_params)
    return {
        "success": True,
        "message": "Successfully triggered a job to\
         undeploy index from index endpoint",
        "data": operation
    }
  except Exception as e:
    if hasattr(e, "code"):
      raise CustomHTTPException(
        status_code=e.code, message=e.message,
        success=False, data=None) from e
    else:
      raise InternalServerError(str(e)) from e


@router.get("/operation")
def get_index_deployment_operation(name: str):
  """This route fetches the index deployment operation status

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      OperationModel: operation Object
  """
  try:
    operation = DeployIndexService().get_index_deployment_operation(name)
    return {
        "success": True,
        "message": "Successfully fetched the index deployment operation",
        "data": operation
    }
  except Exception as e:
    if hasattr(e, "code"):
      raise CustomHTTPException(
        status_code=e.code, message=e.message,
        success=False, data=None) from e
    else:
      raise InternalServerError(str(e)) from e
