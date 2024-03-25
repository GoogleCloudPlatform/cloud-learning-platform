""" Data Source end-points """

import traceback
from fastapi import APIRouter
from services.data_source import (update_data_source_fields,
                                  upsert_data_source_doc, get_data_sources)
from common.utils.logging_handler import Logger
from common.utils.errors import ResourceNotFoundException
from common.utils.http_exceptions import InternalServerError, ResourceNotFound
from schemas.data_source_schema import (DataSourceResponseModel,
                                        UpdateDataSourceRequestModel,
                                        UpdateDataSourceResponseModel,
                                        CreateDataSourceRequestModel,
                                        CreateDataSourceResponseModel)
from schemas.error_schema import NotFoundErrorResponseModel
from config import ERROR_RESPONSES
# pylint: disable = broad-except

router = APIRouter(
    prefix="/sources",
    tags=["Data Sources"],
    responses=ERROR_RESPONSES)


# pylint: disable=redefined-builtin
@router.get(
    "",
    response_model=DataSourceResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_datasources(type: str = ""):
  """The get data source endpoint will return the data source from firestore
    for the type provided as Query param. If no type provided, will return list
    of all docs in DataSource collection on firestore

  QueryParam:
      type (str): type of object for which sources are to be returned

  Raises:
      ResourceNotFoundException: If the domain does not exist
      Exception: 500 Internal Server Error if something goes wrong

  Returns:
      response_body: (dict) - Object Type, its sources and corresponding
                            index id in matching engine
  """
  try:
    response = get_data_sources(type)
    response_body = {
        "success": True,
        "message": "Successfully fetched the data sources",
        "data": response
    }
    Logger.info(response_body)
    return response_body
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post("", response_model=CreateDataSourceResponseModel)
def create_data_source(req_body: CreateDataSourceRequestModel):
  """The create data source end-point creates a new doc for given object type
    and source if not existing. Else will add the new source if doc for given
    object type already exists in firestore.

  Args:
    req_body (CreateDataSourceRequestModel): Required body updating data source
        object_type: (str) - object for which field is to be updated
        input_source: (str) - new source to be updated

  Raises:
      HTTPException: 500 Internal Server Error if something fails

  Returns:
      message: (str) - Success/Failure & updated fields
  """
  try:
    request_body = req_body.__dict__
    object_type = request_body.get("type")
    source = request_body.get("source")
    response = upsert_data_source_doc(object_type, source)
    Logger.info(response)
    return response
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.put("", response_model=UpdateDataSourceResponseModel)
def update_data_source(req_body: UpdateDataSourceRequestModel):
  """The update data source end-point updates the matching_engine_index_id
    field of data source document for given object type and source.

  Args:
    req_body (UpdateDataSourceRequestModel): Required body updating data source
        object_type: (str) - object for which field is to be updated
        input_source: (str) - new source to be updated
        matching_engine_id: (str) - new matching engine ID to be updated

  Raises:
      HTTPException: 500 Internal Server Error if something fails

  Returns:
      message: (str) - Success/Failure & updated fields
  """
  try:
    request_body = req_body.__dict__
    object_type = request_body.get("type")
    source = request_body.get("source")
    matching_engine_id = request_body.get("matching_engine_index_id", "")
    response = update_data_source_fields(object_type, source,
                                         matching_engine_id)
    Logger.info(response)
    return response
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
