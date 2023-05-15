""" Student endpoints """
import traceback
from fastapi import APIRouter, Request
from utils.user_helper import get_user_email
from common.utils.logging_handler import Logger
from common.utils.bq_helper import run_query
from common.utils.cache_service import set_key, get_key
from common.utils.errors import (ResourceNotFoundException,
ValidationError)
from common.utils.http_exceptions import (InternalServerError,
                                          BadRequest,ResourceNotFound)
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ConflictResponseModel,
                                  ValidationErrorResponseModel)
from schemas.analytics import AnalyticsResponse
from config import BQ_DATASET,PROJECT_ID,BQ_TABLE_DICT
from utils.helper import convert_query_result_to_analytics_model

router = APIRouter(prefix="/analytics",
                   tags=["Students"],
                   responses={
                       500: {
                           "model": InternalServerErrorResponseModel
                       },
                       404: {
                           "model": NotFoundErrorResponseModel
                       },
                       409: {
                           "model": ConflictResponseModel
                       },
                       422: {
                           "model": ValidationErrorResponseModel
                       }
                   })

TABLE_ID=f"`{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE_DICT['BQ_ANALYTICS_VIEW']}`"

@router.get("/students/{student_id}",
            response_model=AnalyticsResponse)
def get_student_analytics(student_id: str,request: Request):
  """Get Student analytics by student id
  Args:
      student_id (str): Student email or id from firestore db
  Raises:
      BadRequest: _description_
      ResourceNotFound: 404 Resource not found exception
      InternalServerError: 500 Internal Server Error if something fails

  Returns:
      _type_: _description_
  """
  try:
    headers = {"Authorization": request.headers.get("Authorization")}
    user_email,user_id=get_user_email(
      student_id,headers)
    res_data=get_key(f"analytics::{user_email}::{user_id}::response")
    if res_data:
      return AnalyticsResponse(
        user=res_data["user"],
        section_list=res_data["section_list"])
    result= run_query(
      query=f"Select * from {TABLE_ID} where "+
      f"user_email_address=\"{user_email}\" order by course_id;")
    res_data=convert_query_result_to_analytics_model(result,
                                          student_id,user_id)
    set_key(f"analytics::{user_email}::{user_id}::response",
            res_data.dict(),3600)
    return res_data
  except ValidationError as ve:
    Logger.error(ve)
    raise BadRequest(str(ve)) from ve
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except Exception as e:
    Logger.error(e)
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise InternalServerError(str(e)) from e
