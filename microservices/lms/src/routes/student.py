""" Student endpoints """
import traceback
import requests
from fastapi import APIRouter, Request
from googleapiclient.errors import HttpError
from services import student_service
from common.utils.logging_handler import Logger
from common.utils.errors import (ResourceNotFoundException,
ValidationError,InvalidTokenError)
from common.utils.http_exceptions import (CustomHTTPException,InternalServerError,
                             ResourceNotFound, BadRequest,InvalidToken,Conflict)
from common.models import CourseEnrollmentMapping,Section,Cohort,TempUser
from common.utils import classroom_crud
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ConflictResponseModel,
                                  ValidationErrorResponseModel)
from schemas.section import(StudentListResponseModel,\
   DeleteStudentFromSectionResponseModel)
from schemas.student import(AddStudentResponseModel,\
  AddStudentToCohortModel,GetStudentDetailsResponseModel,\
    GetProgressPercentageResponseModel,InviteStudentToSectionResponseModel)
from config import USER_MANAGEMENT_BASE_URL

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
    # print(users)
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
    # Update enrolled student count in section
    section_details.enrolled_students_count = section_details.\
      enrolled_students_count-1
    section_details.update()
    # Update enrolled student count in cohort
    cohort_details = Cohort.find_by_id(section_details.cohort.key)
    cohort_details.enrolled_students_count = cohort_details.\
      enrolled_students_count -1
    cohort_details.update()
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
    headers = {"Authorization": request.headers.get("Authorization")}
    if cohort.enrolled_students_count >= cohort.max_students:
      raise Conflict(
    "Cohort Max count reached hence student cannot be erolled in this cohort"
    )
    if len(sections) == 0:
      raise ResourceNotFoundException("Given CohortId\
         does not have any sections")
    if not student_service.check_student_can_enroll_in_cohort(
                                              email=input_data.email,
                                                     headers=headers,
                                                     sections=sections):
      raise Conflict(f"User {input_data.email} is already\
                      registered for cohort {cohort_id}")
    section = student_service.get_section_with_minimum_student(sections)

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
        "cohort_id":cohort_id,
        "classroom_id":section.classroom_id,
        "classroom_url":section.classroom_url}
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


@section_student_router.post("/{section_id}/invite/{student_email}",
                             response_model=InviteStudentToSectionResponseModel)
def invite_student(section_id: str,student_email:str,
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
    section = Section.find_by_id(section_id)
    headers = {"Authorization": request.headers.get("Authorization")}
    # invitation = classroom_crud.invite_user(course_id=section.classroom_id,
    #                                         email=student_email,
    #                                         role="STUDENT")
    # print(invitation)
    response = requests.get(f"\
    {USER_MANAGEMENT_BASE_URL}/user/search/email?email={student_email}",\
    headers=headers)
    print("RESPONSE OF SEARCH USER",response.json())

  # If the response is success check if student is inactive i.e  raise error
    if response.status_code == 200:
      print("11")
      searched_student = response.json()["data"]
      print("22")
      if searched_student == []:
        print("Increate user 5")
        # User does not exist in db call create User API
        body = {
            "first_name":"first_name",
            "last_name": "last_name",
            "email":student_email,
            "user_type": "learner",
            "user_type_ref": "",
            "user_groups": [],
            "status": "active",
            "is_registered": True,
            "failed_login_attempts_count": 0,
            "access_api_docs": False,
            "gaia_id":"",
            "photo_url":""
          }
        create_user_response = requests.post(f"{USER_MANAGEMENT_BASE_URL}/user",
        json=body,headers=headers)
        print("Create user ",create_user_response.status_code)
        print(create_user_response.json())
        user_id = create_user_response.json()["data"]["user_id"]
      else:
        if searched_student[0]["status"] =="inactive":
          print("33")
          raise InternalServerError("Student inactive in \
              database. Please update\
              the student status")    
        else:
          user_id = searched_student[0]["user_id"]
          check_already_invited = CourseEnrollmentMapping.find_course_enrollment_record(section_key=section.key,user_id=user_id)
          if check_already_invited:
            raise Conflict("STudent already Invited to this section")
      invitation = classroom_crud.invite_user(course_id=section.classroom_id,
                                            email=student_email,
                                            role="STUDENT")
      print(invitation)
      print("6")
      Logger.info("User with Email {student_email} present with user_id {user_id}")
      course_enrollment_mapping = CourseEnrollmentMapping()
      course_enrollment_mapping.section = section
      course_enrollment_mapping.user = user_id
      course_enrollment_mapping.status = "active"
      course_enrollment_mapping.role = "learner"
      course_enrollment_mapping.invitation_id = invitation["id"]
      course_enrollment_mapping.is_invitation_accepted = False
      course_enrollment_id = course_enrollment_mapping.save().id


    else:
      print("User Management service error_____",response.status_code)
      raise InternalServerError("User management Search User API Error")
    return {
        "message":
        f"Successfully Added the Student with email {student_email}",
        "data" : {"invitation_id": invitation["id"],
                  "course_enrollment_id":course_enrollment_id,
                  "user_id":user_id,
                  "section_id":section_id,
                  "cohort_id":section.cohort.key,
            "classroom_id":section.classroom_id,
            "classroom_url":section.classroom_url}
    }
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

@section_student_router.post("/update_invites")
def update_invites(request: Request):
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
    headers = {"Authorization": request.headers.get("Authorization")}
    course_records = CourseEnrollmentMapping.collection.filter("is_invitation_accepted","==",False).fetch()
    # course_records = list(course_records)
    updated_list_inviations =[]
    for course_record in course_records:
      print("--------------------------------------")
      print("In for Loop for invited  students")
      print(course_record.user)
      print(course_record.section.id) 
      print(course_record.invitation_id)
      print(course_record.is_invitation_accepted)
      if course_record.is_invitation_accepted == False and course_record.invitation_id is not None:
        print("If checking loop",course_record.section.id)
        print("-----------------------------------------")
        try:
          print("Get invite called for",course_record.section.id)
          result = classroom_crud.get_invite(course_record.invitation_id)
          print("Result of get invite___",result)
          Logger.info("In Invitation exi")
        except Exception as e:
          print("in except for ",course_record.section.id,course_record.invitation_id)
          Logger.error(f"Could not get the invite for user_id {course_record.user} \
                       section_id {course_record.section.id}")
          # continue
          user_details = classroom_crud.get_user_details(user_id=course_record.user,headers=headers)
          print("User Details _____",user_details)
          user_profile =classroom_crud.get_user_profile_information(user_details["data"]["email"])
          user_rec = TempUser.collection.filter("user_id","==",course_record.user).get()
          print("USer_record found Temp User ")
          # if user_rec.first_name == "first name":
          print("above gaid if")
          if user_rec.gaia_id == "":
            print("Gaid id",user_rec.gaia_id)
            print(user_profile["name"]["givenName"])
            user_rec.firstname =  user_profile["name"]["givenName"]
            user_rec.lastname = user_profile["name"]["familyName"]
            user_rec.gaia_id = user_profile["id"]
            user_rec.photo_url = user_profile["photoUrl"]
            user_rec.update()
          course_record.is_invitation_accepted = True
          course_record.update()
          # Update section enrolled student count
          section = Section.find_by_id(course_record.section.key)
          section.enrolled_students_count +=1
          section.update()
          cohort = Cohort.find_by_id(section.cohort.key)
          cohort.enrolled_students_count +=1
          cohort.update()
          # Update COhort enrolled student count
          updated_list_inviations.append(course_record.key)
          # continue
    return {
        "message":f"Successfully Added the Student with email",
        "data" : {"list_coursenrolment":updated_list_inviations}}

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
