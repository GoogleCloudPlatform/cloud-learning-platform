""" Student endpoints """
import traceback
from fastapi import APIRouter, HTTPException, Request
from common.utils.logging_handler import Logger
from common.utils.errors import (ResourceNotFoundException, ValidationError)
from common.utils.http_exceptions import (InternalServerError,
                                          ResourceNotFound, BadRequest)
from services import classroom_crud
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ConflictResponseModel,
                                  ValidationErrorResponseModel)
from schemas.section import StudentListResponseModel

# disabling for linting to pass
# pylint: disable = broad-except

router = APIRouter(prefix="/student",
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

SUCCESS_RESPONSE = {"status": "Success"}
FAILED_RESPONSE = {"status": "Failed"}


@router.get("/get_progress_percentage/")
def get_progress_percentage(course_id: int, student_email: str):
  """Get progress percentage

  Args:
    course_id :
      course_id of the course for which progress needs to be determined
    student_email : student_email of the student

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    A number indicative of the percentage of the course completed
    by the student,
    {'status': 'Failed'} if any exception is raised
  """
  try:
    submitted_course_work_list = 0
    course_work_list = len(classroom_crud.get_course_work_list(course_id))
    submitted_course_work = classroom_crud.get_submitted_course_work_list(
        course_id, student_email)
    for x in submitted_course_work:
      if x["state"] == "TURNED_IN":
        submitted_course_work_list = submitted_course_work_list + 1

    SUCCESS_RESPONSE["result"] = {
        "progress_percentage":
        round((submitted_course_work_list / course_work_list) * 100, 2)
    }
    return SUCCESS_RESPONSE

  except Exception as e:
    Logger.error(e)
    traceback.format_exc().replace("\n", " ")
    raise HTTPException(status_code=500) from e


section_student_router = APIRouter(prefix="/sections/{section_id}/students",
                                   tags=["Students"],
                                   responses={
                                       500: {
                                           "model":
                                           InternalServerErrorResponseModel
                                       },
                                       404: {
                                           "model": NotFoundErrorResponseModel
                                       },
                                       409: {
                                           "model": ConflictResponseModel
                                       },
                                       422: {
                                           "model":
                                           ValidationErrorResponseModel
                                       }
                                   })


@section_student_router.get("", response_model=StudentListResponseModel)
def list_students_in_section(section_id: str, request: Request):
  """ Get a list of students of one section from db

  Args:
    section_id(str):section id from firestore db
  Raises:
    HTTPException: 500 Internal Server Error if something fails
    ResourceNotFound: 404 Resource not found exception
  Returns:
    {"status":"Success","data":{}}: Returns list of students in section
    {'status': 'Failed',"data":null}
  """
  try:
    headers = {"Authorization": request.headers.get("Authorization")}
    users = classroom_crud.\
      list_student_section(section_id=section_id,headers=headers)
    return {"data": users}
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except ValidationError as ve:
    raise BadRequest(str(ve)) from ve
  except Exception as e:
    Logger.error(e)
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise InternalServerError(str(e)) from e
