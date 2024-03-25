"""Route for query"""
from fastapi import APIRouter
from utils.http_exceptions import (InternalServerError, CustomHTTPException)
from schemas.query_schema import (QueryModel)
from services.query import IndexQueryService
from config import ERROR_RESPONSES

router = APIRouter(prefix="/query",
  responses=ERROR_RESPONSES)

# pylint: disable = broad-except


@router.post("/result")
def query_index(input_params: QueryModel):
  """This route fetches all the indexes created in ANN service

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      dict of Neighbor Object
  """
  try:
    input_params = {**input_params.dict()}
    response = IndexQueryService().match(input_params)
    return {
        "success": True,
        "message": "Successfully fetched all nearest neighbors of given query",
        "data": response
    }
  except Exception as e:
    if hasattr(e, "code"):
      raise CustomHTTPException(
        status_code=e.code, message=e.message,
        success=False, data=None) from e
    else:
      raise InternalServerError(str(e)) from e

# @router.post("/batch-result")#, response_model=CategoryModelResponse)
# def batch_query_index(input_params: BatchQueryModel):
#   """This route fetches all the indexes created in ANN service

#   Raises:
#       Exception: 500 Internal Server Error if something went wrong

#   Returns:
#       Nested dict of Neighbor Object
#   """
#   try:
#     input_params = {**input_params.dict()}
#     response = IndexQueryService().batch_query(input_params)
#     return {
#         "success": True,
#         "message": "Successfully fetched all nearest neighbors \
#         of for all queries in the batch",
#         "data": response
#     }
#   except Exception as e:
#     if hasattr(e, "code"):
#       raise CustomHTTPException(
#         status_code=e.code, message=e.message,
#         success=False, data=None) from e
#     else:
#       raise InternalServerError(str(e)) from e
