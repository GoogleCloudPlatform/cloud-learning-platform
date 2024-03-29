"""Results Endpoints - Admin"""
import traceback
from fastapi import APIRouter
from fastapi.security import HTTPBearer
from config import ERROR_RESPONSES, LTI_ISSUER_DOMAIN
from common.models import LineItem, Result
from common.utils.errors import (ResourceNotFoundException, InvalidTokenError)
from common.utils.logging_handler import Logger
from common.utils.http_exceptions import (InternalServerError, ResourceNotFound,
                                          Unauthenticated)
from schemas.results_schema import (UpdateResultModel,
                                    GetAllResultsResponseModel,
                                    ResultResponseModel)
from schemas.error_schema import NotFoundErrorResponseModel
from services.line_item_service import get_line_item_results, get_result_of_line_item
from typing import Optional
# pylint: disable=unused-argument, use-maxsplit-arg, line-too-long

auth_scheme = HTTPBearer(auto_error=False)

router = APIRouter(
    tags=["Results - Admin"], prefix="/admin", responses=ERROR_RESPONSES)


@router.get(
    "/{context_id}/line_items/{line_item_id}/results",
    name="Get all the results of a specific line item",
    response_model=GetAllResultsResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_results_of_line_item_for_admin(
    context_id: str,
    line_item_id: str,
    skip: int = 0,
    limit: int = 10,
    user_id: Optional[str] = None,
    is_grade_sync_completed: Optional[bool] = None):
  """The get all results of a line item endpoint will return all the
  results of a line item from firestore
  ### Args:
  line_item_id: `str`
    Unique identifier for line item
  skip: `int`
    Number of results to be skipped <br/>
  limit: `int`
    Size of results array to be returned <br/>
  user_id: `str`
    Unique identifier of the user <br/>
  ### Raises:
  ResourceNotFoundException:
    If the line item does not exist. <br/>
  Exception:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Result: `ResultResponseModel`
  """
  try:
    line_item = LineItem.find_by_id(line_item_id)

    if line_item.contextId != context_id:
      raise ResourceNotFoundException(
          f"Line item with id {line_item_id} in {context_id} not found")

    result_fields = get_line_item_results(
        context_id=context_id,
        line_item_id=line_item_id,
        user_id=user_id,
        is_grade_sync_completed=is_grade_sync_completed,
        skip=skip,
        limit=limit)

    return {
        "success": True,
        "data": result_fields,
        "message": "Sucessfully fetched results"
    }

  except InvalidTokenError as e:
    Logger.error(e)
    raise Unauthenticated(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
    "/{context_id}/line_items/{line_item_id}/results/{result_id}",
    name="Get the specific result of a line item",
    response_model=ResultResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_result_for_admin(context_id: str, line_item_id: str, result_id: str):
  """The get result of a line item endpoint will return the specific result
  of a line item from firestore
  ### Args:
  line_item_id: `str`
    Unique identifier for line item
  result_id: `str`
    Unique identifier for result
  ### Raises:
  ResourceNotFoundException:
    If the line item does not exist. <br/>
  Exception:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Result: `ResultResponseModel`
  """
  try:
    result_fields = get_result_of_line_item(
        context_id=context_id, line_item_id=line_item_id, result_id=result_id)

    return {
        "success": True,
        "data": result_fields,
        "message": "Sucessfully fetched result details"
    }

  except InvalidTokenError as e:
    Logger.error(e)
    raise Unauthenticated(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.patch(
    "/{context_id}/line_items/{line_item_id}/results/{result_id}",
    name="Update the specific result of a line item",
    response_model=ResultResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_result(context_id: str, line_item_id: str, result_id: str,
                  input_result: UpdateResultModel):
  """The get result of a line item endpoint will return the specific result
  of a line item from firestore
  ### Args:
  line_item_id: `str`
    Unique identifier for line item
  result_id: `str`
    Unique identifier for result
  ### Raises:
  ResourceNotFoundException:
    If the line item does not exist. <br/>
  Exception:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Result: `ResultResponseModel`
  """
  try:
    line_item = LineItem.find_by_id(line_item_id)

    if line_item.contextId != context_id:
      raise ResourceNotFoundException(
          f"Line item with id {line_item_id} in {context_id} not found")

    result = Result.find_by_id(result_id)
    if result.lineItemId != line_item_id:
      raise ResourceNotFoundException(
          "Incorrect result id provided for the given line item")

    input_result_dict = {**input_result.dict()}
    for key in input_result_dict:
      if input_result_dict[key] is not None:
        setattr(result, key, input_result_dict[key])

    result.update()

    result_fields = result.get_fields(reformat_datetime=True)
    result_fields[
        "id"] = f"{LTI_ISSUER_DOMAIN}/lti/api/v1/{context_id}/line_items/{line_item_id}/results/{result.id}"

    result_fields[
        "scoreOf"] = f"{LTI_ISSUER_DOMAIN}/lti/api/v1/{context_id}/line_items/{line_item_id}"

    return {
        "success": True,
        "data": result_fields,
        "message": "Sucessfully udpated result details"
    }

  except InvalidTokenError as e:
    Logger.error(e)
    raise Unauthenticated(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
