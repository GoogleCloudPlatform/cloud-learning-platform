""" Student endpoints """
import traceback
from fastapi import APIRouter, HTTPException, Request
from googleapiclient.errors import HttpError
from common.utils.logging_handler import Logger
from common.utils.errors import (ResourceNotFoundException, ValidationError)
from common.utils.http_exceptions import (CustomHTTPException,InternalServerError,
                                          ResourceNotFound, BadRequest)
from common.models import CourseEnrollmentMapping
from services import classroom_crud
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ConflictResponseModel,
                                  ValidationErrorResponseModel)
from schemas.section import StudentListResponseModel, DeleteStudentFromSectionResponseModel
from utils.helper import convert_course_enrollment_model
from config import USER_MANAGEMENT_BASE_URL
import requests

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

@router.delete("/{user_id}/section/{section_id}",
response_model=DeleteStudentFromSectionResponseModel)
def delete_student(section_id: str,user_id:str,request: Request):
  """Get a section details from db
  Args:
      section_id (str): section_id in firestore
  Raises:
      HTTPException: 500 Internal Server Error if something fails
      HTTPException: 404 Section with section id is not found
  Returns:
    {"status":"Success","new_course":{}}: Returns section details from  db,
    {'status': 'Failed'} if the user creation raises an exception
  """
  try:
    headers = {"Authorization": request.headers.get("Authorization")}
    result = CourseEnrollmentMapping.find_by_user(user_id=user_id)
    print("USSERRR !________________",result)
    if result == []:
      raise ResourceNotFoundException\
      ("User not found in course Enrollment Collection")
    course_enrollment_result = \
      list(map(convert_course_enrollment_model, result))
    print("COURSE ENROLLEMTT_______________",course_enrollment_result)
    record = None
    for record in course_enrollment_result:
      if section_id == record["section"]["id"]:
        course_id =  record["section"]["classroom_id"]
        response_get_student = \
        requests.get\
          (f"{USER_MANAGEMENT_BASE_URL}/user/{user_id}",headers=headers)
        print("Get student email response")
        if response_get_student.status_code == 404:
          raise \
            ResourceNotFoundException(response_get_student.json()["message"])
        student_email =  response_get_student.json()["data"]["email"]
        classroom_crud.delete_student(course_id=course_id,\
          student_email=student_email)
        print("Record ID")
        print(record["id"])
        course_enrollment = CourseEnrollmentMapping.find_by_id(record["id"])
        course_enrollment.status = "inactive"
        course_enrollment.update()
    return {"data": record["id"]}
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except HttpError as ae:
    Logger.error(ae)
    raise CustomHTTPException(status_code=ae.resp.status,
                              success=False,
                              message=str(ae),
                              data=None) from ae
  except Exception as e:
    Logger.error(e)
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise InternalServerError(str(e)) from e
