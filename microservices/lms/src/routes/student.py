""" Student endpoints """
import traceback
from fastapi import APIRouter, Request
from googleapiclient.errors import HttpError
from services import student_service
from common.utils.logging_handler import Logger
from common.utils.errors import (ResourceNotFoundException,
ValidationError,InvalidTokenError)
from common.utils.http_exceptions import (CustomHTTPException,InternalServerError,
                             ResourceNotFound, BadRequest,InvalidToken,Conflict)
from common.models import CourseEnrollmentMapping,Section,Cohort
from common.utils import classroom_crud
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ConflictResponseModel,
                                  ValidationErrorResponseModel)
from schemas.section import(StudentListResponseModel,\
   DeleteStudentFromSectionResponseModel)
from schemas.student import(AddStudentResponseModel,\
  AddStudentToCohortModel,GetStudentDetailsResponseModel,\
    GetProgressPercentageResponseModel)

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

section_student_router = APIRouter(prefix="/sections",
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

cohort_student_router = APIRouter(prefix="/cohorts",
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

@section_student_router.get("/{section_id}/get_progress_percentage/{user}",
                            response_model=GetProgressPercentageResponseModel)
def get_progress_percentage(section_id: str, user: str, request: Request):
  """Get progress percentage

  Args:
    section_id : section id for which progess is required
    user : email id or user id for whol progress is required

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    A number indicative of the percentage of the course completed
    by the student,
    {'status': 'Failed'} if any exception is raised
  """
  try:
    headers = {"Authorization": request.headers.get("Authorization")}
    user_id = student_service.get_user_id(user=user, headers=headers)
    submitted_course_work_list = 0
    course_work_list = len(classroom_crud.get_course_work_list(section_id))
    submitted_course_work = classroom_crud.get_submitted_course_work_list(
        section_id, user_id,headers)
    for x in submitted_course_work:
      if x["state"] == "TURNED_IN":
        submitted_course_work_list = submitted_course_work_list + 1
    return {"data":\
    round((submitted_course_work_list / course_work_list) * 100, 2)}

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


@section_student_router.get("/{section_id}/students/{user}",
                            response_model=GetStudentDetailsResponseModel)
def get_student_in_section(section_id: str, user: str, request: Request):
  """ Get student details of one section from db
  Args:
    section_id(str):section id from firestore db
    user(str):user email or user id from firestore db
  Raises:
    HTTPException: 500 Internal Server Error if something fails
    ResourceNotFound: 404 Resource not found exception
  Returns:
    {"status":"Success","data":{}}: Returns list of students in section
    {'status': 'Failed',"data":null}
  """
  try:
    headers = {"Authorization": request.headers.get("Authorization")}
    user_id = student_service.get_user_id(user=user, headers=headers)
    users = classroom_crud.\
      if_user_exists_in_section\
        (section_id=section_id,user_id=user_id,headers=headers)
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



@section_student_router.get("/{section_id}/students",
 response_model=StudentListResponseModel)
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

@section_student_router.delete("/{section_id}/students/{user}",
response_model=DeleteStudentFromSectionResponseModel)
def delete_student(section_id: str,user:str,request: Request):
  """Get a section details from db\n
  Args:
      section_id (str): section_id in firestore\n
      user (str): user_id in firestore User collection or email ID of the user
  Raises:
      HTTPException: 500 Internal Server Error if something fails
      HTTPException: 404 user with section id is not found
  Returns:
    {"status":"Success","data":{course_enrollment_id}},
    {'status': 'Failed'} if the user creation raises an exception
  """
  try:
    headers = {"Authorization": request.headers.get("Authorization")}
    section_details = Section.find_by_id(section_id)
    user_id=student_service.get_user_id(user=user,headers=headers)
    result = CourseEnrollmentMapping.\
      find_course_enrollment_record(section_details.key,user_id)
    if result is None:
      raise ResourceNotFoundException\
      ("User not found in course Enrollment Collection")
    course_id = section_details.classroom_id
    response_get_student = classroom_crud.get_user_details(user_id,headers)
    student_email =  response_get_student["data"]["email"]
    classroom_crud.delete_student(course_id=course_id,\
      student_email=student_email)
    result.status = "inactive"
    result.update()
    return{"data":result.id}
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


@cohort_student_router.post("/{cohort_id}/students",
response_model=AddStudentResponseModel)
def enroll_student_section(cohort_id: str,
                           input_data: AddStudentToCohortModel,
                           request: Request):
  """
  Args:
    input_data(AddStudentToSectionModel):
      An AddStudentToSectionModel object which contains email and credentials
  Raises:
    InternalServerError: 500 Internal Server Error if something fails
    ResourceNotFound : 404 if the section or classroom does not exist
    Conflict: 409 if the student already exists
  Returns:
    AddStudentResponseModel: if the student successfully added,
    NotFoundErrorResponseModel: if the section and course not found,
    ConflictResponseModel: if any conflict occurs,
    InternalServerErrorResponseModel: if the add student raises an exception
  """
  try:
    cohort = Cohort.find_by_id(cohort_id)
    sections = Section.collection.filter("cohort","==",cohort.key).fetch()
    sections = list(sections)
    if cohort.enrolled_students_count >= cohort.max_students:
      raise Conflict(
    "Cohort Max count reached hence student cannot be erolled in this cohort"
    )
    if len(sections) == 0:
      raise ResourceNotFoundException("Given CohortId\
         does not have any sections")
    section = student_service.get_section_with_minimum_student(sections)

    headers = {"Authorization": request.headers.get("Authorization")}
    user_object = classroom_crud.enroll_student(
        headers=headers,
        access_token=input_data.access_token,
        student_email=input_data.email,
        course_id=section.classroom_id,
        course_code=section.classroom_code)
    cohort = section.cohort
    cohort.enrolled_students_count += 1
    cohort.update()
    section.enrolled_students_count +=1
    section.update()

    course_enrollment_mapping = CourseEnrollmentMapping()
    course_enrollment_mapping.section = section
    course_enrollment_mapping.user = user_object["user_id"]
    course_enrollment_mapping.status = "active"
    course_enrollment_mapping.role = "learner"
    course_enrollment_id = course_enrollment_mapping.save().id
    response_dict = {}
    response_dict = {"course_enrollment_id":course_enrollment_id,
        "student_email":input_data.email,"section_id":section.id,
        "cohort_id":cohort_id}
    return {
        "message":
        f"Successfully Added the Student with email {input_data.email}",
        "data" : response_dict
    }

  except InvalidTokenError as ive:
    raise InvalidToken(str(ive)) from ive
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except Conflict as conflict:
    Logger.error(conflict)
    raise Conflict(str(conflict)) from conflict
  except HttpError as ae:
    raise CustomHTTPException(status_code=ae.resp.status,
                              success=False,
                              message=str(ae),
                              data=None) from ae
  except Exception as e:
    Logger.error(e)
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise InternalServerError(str(e)) from e
