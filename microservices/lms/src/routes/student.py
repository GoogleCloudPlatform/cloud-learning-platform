""" Student endpoints """
import traceback
from fastapi import APIRouter, Request
from googleapiclient.errors import HttpError
from services import student_service,section_service
from utils.user_helper import (
  course_enrollment_user_model,get_user_id,
  check_user_can_enroll_in_section)
from common.utils.logging_handler import Logger
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 InvalidTokenError)
from common.utils.http_exceptions import (ClassroomHttpException,
                                          InternalServerError,
                                          ResourceNotFound, BadRequest,
                                          InvalidToken, Conflict)
from common.models import (CourseEnrollmentMapping, Section, Cohort, User)
from common.utils import classroom_crud
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ConflictResponseModel,
                                  ValidationErrorResponseModel)
from schemas.section import(StudentListResponseModel,\
   DeleteStudentFromSectionResponseModel)
from schemas.student import(AddStudentResponseModel,
  AddStudentModel,GetStudentDetailsResponseModel,
    GetProgressPercentageResponseModel,InviteStudentToSectionResponseModel,
    UpdateInviteResponseModel)

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
                                          "model": ValidationErrorResponseModel
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
    user_id = get_user_id(user=user, headers=headers)
    submitted_course_work_list = 0
    course_work_list = len(classroom_crud.get_course_work_list(section_id))
    submitted_course_work = classroom_crud.get_submitted_course_work_list(
        section_id, user_id, headers)
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
    {"status":"Success","data":{}}:
    {'status': 'Failed',"data":null}
  """
  try:
    headers = {"Authorization": request.headers.get("Authorization")}
    user_id = get_user_id(user=user, headers=headers)
    section = Section.find_by_id(section_id)
    result=CourseEnrollmentMapping.\
    find_course_enrollment_record(section.key,user_id,"learner")
    if result is None:
      raise ResourceNotFoundException(
          f"Student not found in this section {section_id}")
    # users = classroom_crud.\
    #   if_user_exists_in_section\
    #     (section_id=section_id,user_id=user_id,headers=headers)
    return {
        "message": f"Successfully get student details by {user}",
        "data": course_enrollment_user_model(result)
    }
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except ValidationError as ve:
    Logger.error(ve)
    raise BadRequest(str(ve)) from ve
  except Exception as e:
    Logger.error(e)
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise InternalServerError(str(e)) from e


@cohort_student_router.get("/{cohort_id}/students/{user}",
                           response_model=GetStudentDetailsResponseModel)
def get_student_in_cohort(cohort_id: str, user: str, request: Request):
  """ Get student details of one cohort from db
  Args:
    cohort_id(str):cohort id from firestore db
    user(str):user email or user id from firestore db
  Raises:
    HTTPException: 500 Internal Server Error if something fails
    ResourceNotFound: 404 Resource not found exception
  Returns:
    {"status":"Success","data":{}}
    {'status': 'Failed',"data":null}
  """
  try:
    headers = {"Authorization": request.headers.get("Authorization")}
    user_id = get_user_id(user=user, headers=headers)
    cohort = Cohort.find_by_id(cohort_id)
    course_mapping = None
    list_section = Section.collection.filter("cohort", "==",
                                             cohort.key).fetch()
    for section in list_section:
      course_mapping = CourseEnrollmentMapping.find_course_enrollment_record(
          section_key=section.key, user_id=user_id,role="learner")
      if course_mapping:
        return {
            "data":
            course_enrollment_user_model(course_mapping)
        }
    if not course_mapping:
      raise ResourceNotFoundException(
          f"User {user} not found for cohort {cohort_id}")
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except ValidationError as ve:
    Logger.error(ve)
    raise BadRequest(str(ve)) from ve
  except Exception as e:
    Logger.error(e)
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise InternalServerError(str(e)) from e


@section_student_router.get("/{section_id}/students",
                            response_model=StudentListResponseModel)
def list_students_in_section(section_id: str):
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
    section = Section.find_by_id(section_id)
    results=CourseEnrollmentMapping.\
    fetch_all_by_section(section.key,"learner")
    data = [
        course_enrollment_user_model(i) for i in results
    ]
    Logger.info(data)
    return {"data": data}
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except ValidationError as ve:
    Logger.error(ve)
    raise BadRequest(str(ve)) from ve
  except Exception as e:
    Logger.error(e)
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise InternalServerError(str(e)) from e


@section_student_router.delete(
    "/{section_id}/students/{user}",
    response_model=DeleteStudentFromSectionResponseModel)
def delete_student(section_id: str, user: str, request: Request):
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
    user_id = get_user_id(user=user, headers=headers)
    result = CourseEnrollmentMapping.\
      find_active_enrolled_student_record(section_details.key,user_id)
    if result is None:
      raise ResourceNotFoundException\
      (
      f"User {user_id} not found in course Enrollment\
        Collection for section{section_id}"
      )
    course_id = section_details.classroom_id
    response_get_student = classroom_crud.get_user_details(user_id, headers)
    student_email = response_get_student["data"]["email"]
    classroom_crud.delete_student(course_id=course_id,\
      student_email=student_email)
    result.status = "inactive"
    result.update()
    # Update enrolled student count in section
    section_details.enrolled_students_count = section_details.\
      enrolled_students_count-1
    section_details.update()
    # Update enrolled student count in cohort
    cohort_details = Cohort.find_by_id(section_details.cohort.key)
    cohort_details.enrolled_students_count = cohort_details.\
      enrolled_students_count -1
    cohort_details.update()
    return {"data": result.id}
  except ResourceNotFoundException as err:
    Logger.error(err)
    error = traceback.format_exc().replace("\n", " ")
    Logger.error(error)
    raise ResourceNotFound(str(err)) from err
  except HttpError as ae:
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise ClassroomHttpException(status_code=ae.resp.status,
                                 message=str(ae)) from ae
  except Exception as e:
    Logger.error(e)
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise InternalServerError(str(e)) from e


@cohort_student_router.post("/{cohort_id}/students",
                            response_model=AddStudentResponseModel)
def enroll_student_cohort(cohort_id: str, input_data: AddStudentModel,
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
    sections = Section.collection.filter("cohort", "==", cohort.key).filter(
    "enrollment_status","==","OPEN").filter("status","==","ACTIVE").fetch()
    sections = list(sections)
    headers = {"Authorization": request.headers.get("Authorization")}
    if cohort.enrolled_students_count >= cohort.max_students:
      raise Conflict("Cohort Max count reached hence student cannot" +
                     " be erolled in this cohort")
    if len(sections) == 0:
      raise ResourceNotFoundException("Given CohortId\
         does not have any sections")
    if not student_service.check_student_can_enroll_in_cohort(
        email=input_data.email, headers=headers, sections=sections):
      raise Conflict(f"Student {input_data.email} is already\
                      enrolled for cohort {cohort_id}")
    section = student_service.get_section_with_minimum_student(sections)
    if section is None:
      raise Conflict("Max count reached for all sctions is reached hence" +
                  "student cannot be erolled in this cohort")
    Logger.info(f"Section with minimum student is {section.id},\
                enroll student intiated for {input_data.email}")
    user_object = classroom_crud.enroll_student(
        headers=headers,
        access_token=input_data.access_token,
        student_email=input_data.email,
        course_id=section.classroom_id,
        course_code=section.classroom_code)
    cohort = section.cohort
    cohort.enrolled_students_count += 1
    cohort.update()
    section.enrolled_students_count += 1
    section.update()

    course_enrollment_mapping = CourseEnrollmentMapping()
    course_enrollment_mapping.section = section
    course_enrollment_mapping.user = User.find_by_user_id(
        user_object["user_id"])
    course_enrollment_mapping.status = "active"
    course_enrollment_mapping.role = "learner"
    course_enrollment_id = course_enrollment_mapping.save().id
    response_dict = {}
    response_dict = {
        "course_enrollment_id": course_enrollment_id,
        "student_email": input_data.email,
        "section_id": section.id,
        "cohort_id": cohort_id,
        "classroom_id": section.classroom_id,
        "classroom_url": section.classroom_url
    }
    return {
        "message":
        f"Successfully Added the Student with email {input_data.email}",
        "data": response_dict
    }

  except InvalidTokenError as ive:
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise InvalidToken(str(ive)) from ive
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except Conflict as conflict:
    Logger.error(conflict)
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise Conflict(str(conflict)) from conflict
  except HttpError as ae:
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    if ae.resp.status == 409:
      raise ClassroomHttpException(
          status_code=ae.resp.status,
          message="Student already exist in classroom") from ae
    else:
      raise ClassroomHttpException(status_code=ae.resp.status,
                                   message="Can't enroll student to classroom,\
  Please check organizations policy or authentication scopes") from ae
  except Exception as e:
    Logger.error(e)
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise InternalServerError(str(e)) from e


@section_student_router.post("/{section_id}/students",
                             response_model=AddStudentResponseModel)
def enroll_student_section(section_id: str, input_data: AddStudentModel,
                           request: Request):
  """
  Args:
    input_data(AddStudentModel):
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
    section = Section.find_by_id(section_id)
    headers = {"Authorization": request.headers.get("Authorization")}
    section_service.validate_section(section)
    cohort = section.cohort
    if cohort.enrolled_students_count >= cohort.max_students:
      raise ValidationError("Cohort Max count reached hence student cannot" +
            "be erolled in this cohort")
    if not check_user_can_enroll_in_section(
        email=input_data.email, headers=headers, section=section):
      raise Conflict(f"User {input_data.email} is already\
                      enrolled for section {section_id}")
    Logger.info(f"Section {section.id},\
                enroll student intiated for {input_data.email}")
    user_object = classroom_crud.enroll_student(
        headers=headers,
        access_token=input_data.access_token,
        student_email=input_data.email,
        course_id=section.classroom_id,
        course_code=section.classroom_code)
    cohort = section.cohort
    cohort.enrolled_students_count += 1
    cohort.update()
    section.enrolled_students_count += 1
    section.update()

    course_enrollment_mapping = CourseEnrollmentMapping()
    course_enrollment_mapping.section = section
    course_enrollment_mapping.user = User.find_by_user_id(
        user_object["user_id"])
    course_enrollment_mapping.status = "active"
    course_enrollment_mapping.role = "learner"
    course_enrollment_id = course_enrollment_mapping.save().id
    response_dict = {}
    response_dict = {
        "course_enrollment_id": course_enrollment_id,
        "student_email": input_data.email,
        "section_id": section.id,
        "cohort_id": section.cohort.id,
        "classroom_id": section.classroom_id,
        "classroom_url": section.classroom_url
    }
    return {
        "message":
        f"Successfully Added the Student with email {input_data.email}",
        "data": response_dict
    }
  except InvalidTokenError as ive:
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise InvalidToken(str(ive)) from ive
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except Conflict as conflict:
    Logger.error(conflict)
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise Conflict(str(conflict)) from conflict
  except HttpError as ae:
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    # if ae.resp.status == 409:
    #   raise ClassroomHttpException(status_code=ae.resp.status,
    # message="Student already exist in classroom") from ae
    # else :
    raise ClassroomHttpException(status_code=ae.resp.status,
                                 message="Can't enroll student to classroom,\
  Please check organizations policy or authentication scopes") from ae
  except ValidationError as ve:
    Logger.error(ve)
    raise BadRequest(str(ve)) from ve
  except Exception as e:
    Logger.error(e)
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise InternalServerError(str(e)) from e


@section_student_router.post("/{section_id}/invite/{student_email}",
                             response_model=InviteStudentToSectionResponseModel
                             )
def invite_student(section_id: str, student_email: str, request: Request):
  """
  Args:
    section_id:firestore id of section where student is invited
    student email:student email
  Raises:
    InternalServerError: 500 Internal Server Error if something fails
    ResourceNotFound : 404 if the section or classroom does not exist
    Conflict: 409 if the student already exists
  Returns:
    InviteStudentToSectionResponseModel: if the student successfully invited,
    NotFoundErrorResponseModel: if the section and course not found,
    ConflictResponseModel: if any conflict occurs,
    InternalServerErrorResponseModel: if the add student raises an exception
  """
  try:
    section = Section.find_by_id(section_id)
    headers = {"Authorization": request.headers.get("Authorization")}
    section_service.validate_section(section)
    #TODO: add logic for cohort max count
    cohort = section.cohort
    if cohort.enrolled_students_count >= cohort.max_students:
      raise Conflict("Cohort Max count reached hence student cannot" +
                     " be erolled in this cohort")
    invitation_details = student_service.invite_student(
        section=section, student_email=student_email, headers=headers)
    return {
        "message":
        f"Successfully Added the Student with email {student_email}",
        "data": invitation_details
    }
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except Conflict as conflict:
    Logger.error(conflict)
    raise Conflict(str(conflict)) from conflict
  except HttpError as ae:
    raise ClassroomHttpException(status_code=ae.resp.status,
                                 message=str(ae)) from ae
  except ValidationError as ve:
    Logger.error(ve)
    raise BadRequest(str(ve)) from ve
  except Exception as e:
    Logger.error(e)
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise InternalServerError(str(e)) from e


@cohort_student_router.post("/{cohort_id}/invite/{student_email}",
                            response_model=InviteStudentToSectionResponseModel)
def invite_student_cohort(cohort_id: str, student_email: str,
                          request: Request):
  """
  Args:
    cohort_id: firestore id of chort where student invited
    student_email : student email
  Raises:
    InternalServerError: 500 Internal Server Error if something fails
    ResourceNotFound : 404 if the section or classroom does not exist
    Conflict: 409 if the student already exists
  Returns:
    InviteStudentToSectionResponseModel:if the student successfully invited,
    NotFoundErrorResponseModel: if the section and course not found,
    ConflictResponseModel: if any conflict occurs,
    InternalServerErrorResponseModel: if the add student raises an exception
  """
  try:
    cohort = Cohort.find_by_id(cohort_id)
    sections = Section.collection.filter("cohort", "==", cohort.key).filter(
    "enrollment_status","==","OPEN").filter("status","==","ACTIVE").fetch()
    sections = list(sections)
    headers = {"Authorization": request.headers.get("Authorization")}
    if cohort.enrolled_students_count >= cohort.max_students:
      raise Conflict("Cohort Max count reached hence student " +
                     "cannot be erolled in this cohort")
    if len(sections) == 0:
      raise ResourceNotFoundException("Given CohortId\
         does not have any sections")
    if not student_service.check_student_can_enroll_in_cohort(
    email=student_email, headers=headers, sections=sections):
      raise Conflict(f"User {student_email} is already\
                      registered for cohort {cohort_id}")
    section = student_service.get_section_with_minimum_student(sections)
    if section is None:
      raise Conflict(
    "Max count reached for all sctions is reached hence student cannot" +
                     " be erolled in this cohort")
    Logger.info(f"Section with minimum student is {section.id},\
                enroll student intiated for {student_email}")
    headers = {"Authorization": request.headers.get("Authorization")}
    invitation_details = student_service.invite_student(
        section=section, student_email=student_email, headers=headers)
    return {
        "message":
  f"Successfully Added the Student with email {student_email}",
        "data": invitation_details
    }
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except Conflict as conflict:
    Logger.error(conflict)
    raise Conflict(str(conflict)) from conflict
  except HttpError as ae:
    raise ClassroomHttpException(status_code=ae.resp.status,
                                 message=str(ae)) from ae
  except Exception as e:
    Logger.error(e)
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise InternalServerError(str(e)) from e


@section_student_router.patch("/update_invites",
                              response_model=UpdateInviteResponseModel)
def update_invites():
  """
  Args:
  Raises:
    InternalServerError: 500 Internal Server Error if something fails
    ResourceNotFound : 404 if the section or classroom does not exist
    Conflict: 409 if the student already exists
  Returns:
    : if the student successfully added,
    NotFoundErrorResponseModel: if the section and course not found,
    ConflictResponseModel: if any conflict occurs,
    InternalServerErrorResponseModel: if the add student raises an exception
  """
  try:
    # headers = {"Authorization": request.headers.get("Authorization")}
    course_records = CourseEnrollmentMapping.collection.filter(
        "status", "==", "invited").fetch()
    updated_list_inviations = []
    for course_record in course_records:
      Logger.info(f"course_record {course_record.section.id}, " +
                  f"user_id {course_record.user.id}")
      if course_record.invitation_id is not None:
        try:
          result = classroom_crud.get_invite(course_record.invitation_id)
          Logger.info(
              f"Invitation {result} found for User id {course_record.user.id},\
          course_enrollment_id {course_record.id} database will be updated\
          once invite is accepted.")
        except HttpError as ae:
          Logger.info(f"Get invite response status code {ae.resp.status}")
          Logger.info(
              f"Could not get the invite for user_id {course_record.user.id}\
          section_id{course_record.section.id}\
           course_enrollment id {course_record.id}")
          # user_details = classroom_crud.get_user_details(
          #     user_id=course_record.user, headers=headers)
          # Logger.info(f"User record found for User {user_details}")
          user_profile = classroom_crud.get_user_profile_information(
              course_record.user.email)
          user_ref = course_record.user
          Logger.info(user_ref.to_dict())
          # Check if gaia_id is "" if yes so update personal deatils
          if user_ref.gaia_id == "":
            user_ref.first_name = user_profile["name"]["givenName"]
            user_ref.last_name = user_profile["name"]["familyName"]
            user_ref.gaia_id = user_profile["id"]
            user_ref.photo_url = user_profile["photoUrl"]
            user_ref.update()
          course_record.status = "active"
          course_record.update()
          # Update section enrolled student count
          section = Section.find_by_id(course_record.section.key)
          section.enrolled_students_count += 1
          section.update()
          # Update COhort enrolled student count
          cohort = Cohort.find_by_id(section.cohort.key)
          cohort.enrolled_students_count += 1
          cohort.update()
          updated_list_inviations.append(course_record.key)
          Logger.info(
              f"Successfully  updated the invitations {updated_list_inviations}"
          )
    return {
        "message": "Successfully  updated the invitations",
        "data": {
            "list_coursenrolment": updated_list_inviations
        }
    }
  except ResourceNotFoundException as err:
    error = traceback.format_exc().replace("\n", " ")
    Logger.error(error)
    raise ResourceNotFound(str(err)) from err
  except Conflict as conflict:
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise Conflict(str(conflict)) from conflict
  except HttpError as ae:
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise ClassroomHttpException(status_code=ae.resp.status,
                                 message=str(ae)) from ae
  except Exception as e:
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise InternalServerError(str(e)) from e
