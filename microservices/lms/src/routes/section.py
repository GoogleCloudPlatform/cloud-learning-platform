""" Section endpoints """
import traceback
import datetime
from common.models import Cohort, CourseTemplate, Section, CourseEnrollmentMapping
from common.utils.errors import ResourceNotFoundException, ValidationError
from common.utils.http_exceptions import (ClassroomHttpException,
                                          InternalServerError,
                                          ResourceNotFound, BadRequest,Conflict
                                          )
from common.utils import classroom_crud
from common.utils.logging_handler import Logger
from common.utils.bq_helper import insert_rows_to_bq
from fastapi import APIRouter, Request,BackgroundTasks,status
from googleapiclient.errors import HttpError
from schemas.classroom_courses import EnableNotificationsResponse
from schemas.error_schema import (ConflictResponseModel,
                                  InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ValidationErrorResponseModel)
from schemas.section import (
    DeleteSectionResponseModel,
    GetSectiontResponseModel, SectionDetails, SectionListResponseModel,
    UpdateSectionResponseModel,TeachersListResponseModel,
    GetTeacherResponseModel,AssignmentModel,GetCourseWorkList,
    ImportGradeResponseModel,
    EnrollTeacherSection,DeleteTeacherFromSectionResponseModel,
    UpdateEnrollmentStatusSectionModel)
from schemas.update_section import UpdateSection
from services.section_service import copy_course_background_task,\
update_grades,add_teacher
from utils.helper import (convert_section_to_section_model,
                          convert_assignment_to_assignment_model,
                          FEED_TYPES,
                    convert_coursework_to_short_coursework_model)
from utils.user_helper import (course_enrollment_user_model,
                               get_user_id,check_user_can_enroll_in_section)
from config import BQ_TABLE_DICT,BQ_DATASET
# disabling for linting to pass
# pylint: disable = broad-except

router = APIRouter(prefix="/sections",
                   tags=["Sections"],
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

@router.post("",
             status_code=status.HTTP_202_ACCEPTED)
def create_section(sections_details: SectionDetails,
                  request: Request,
                   background_tasks: BackgroundTasks
                   ):
  """Create section API
  Args:
    name (section): Section name
    description (str):Description
    classroom_template_id(str):course_template_id id from firestore
    cohort_id(str):cohort id from firestore
    teachers(list):List of teachers to be added
  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    {"status":"Success","new_course":{}}: Returns new course details,
    {'status': 'Failed'} if the user creation raises an exception
  """
  try:
    headers = {"Authorization": request.headers.get("Authorization")}
    course_template_details = CourseTemplate.find_by_id(
        sections_details.course_template)
    cohort_details = Cohort.find_by_id(sections_details.cohort)
    # Get course by course id for copying from master course
    current_course = classroom_crud.get_course_by_id(
        course_template_details.classroom_id)
    if current_course is None:
      raise ResourceNotFoundException(
          "classroom  with id" +
          f" {course_template_details.classroom_id} is not found")
    background_tasks.add_task(copy_course_background_task,
                              course_template_details,
                             sections_details,
                             cohort_details,
                             headers,message = "started process")
    Logger.info(f"Background Task called for the cohort id {cohort_details.id}\
                course template {course_template_details.id} with\
                 section name{sections_details.name}")
    return { "success": True,
            "message": "Section will be created shortly",
            "data": None}
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except HttpError as hte:
    Logger.error(hte)
    raise ClassroomHttpException(status_code=hte.resp.status,
                              message=str(hte)) from hte
  except Exception as e:
    error = traceback.format_exc().replace("\n", " ")
    Logger.error(error)
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.get("/{section_id}", response_model=GetSectiontResponseModel)
def get_section(section_id: str):
  """Get a section details from db

  Args:
      section_id (str): section_id in firestore
  Raises:
      HTTPException: 500 Internal Server Error if something fails
      ResourceNotFound: 404 Section with section id is not found
  Returns:
    {"status":"Success","new_course":{}}: Returns section details from  db,
    {'status': 'Failed'} if the user creation raises an exception
  """
  try:
    section_details = []
    section_details = Section.find_by_id(section_id)
    # Get course by course id
    new_section = convert_section_to_section_model(section_details)
    return {"data": new_section}
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except HttpError as ae:
    Logger.error(ae)
    raise ClassroomHttpException(status_code=ae.resp.status,
                              message=str(ae)) from ae
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e

@router.get("/{section_id}/teachers",response_model=TeachersListResponseModel)
def get_teachers_list(section_id: str):
  """Get a list of teachers for a section details from db

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
    # headers = {"Authorization": request.headers.get("Authorization")}
    section_details = Section.find_by_id(section_id)
    teacher_list=CourseEnrollmentMapping.fetch_all_by_section(
      section_details.key,"faculty")
    data = [
        course_enrollment_user_model(i) for i in teacher_list
    ]
    return {"data": data}
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except HttpError as ae:
    Logger.error(ae)
    raise ClassroomHttpException(status_code=ae.resp.status,
                              message=str(ae)) from ae
  except Exception as e:
    Logger.error(e)
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(e)
    raise InternalServerError(str(e)) from e

@router.post("/{section_id}/teachers",
response_model=GetTeacherResponseModel)
def enroll_teacher(section_id: str,request: Request,
                   teacher_details: EnrollTeacherSection):
  """_summary_

  Args:
      section_id (str): _description_
      request (Request): _description_
      teacher_details (EnrollTeacherSection): _description_

  Raises:
      Conflict: _description_
      ResourceNotFound: _description_
      Conflict: _description_
      ClassroomHttpException: _description_
      InternalServerError: _description_

  Returns:
      _type_: _description_
  """
  try:
    teacher_email = teacher_details.email
    headers = {"Authorization": request.headers.get("Authorization")}
    section = Section.find_by_id(section_id)
    if not check_user_can_enroll_in_section(teacher_email,headers,section):
      raise Conflict(f"User {teacher_email} is already"
                     +f" in this section {section.id} as a leaner or faculty")

    result=add_teacher(headers,section,teacher_email)
    if result.invitation_id:
      return {
        "message": f"Successfully invited the teacher using {teacher_email}",
        "data": course_enrollment_user_model(result)
    }
    return {
        "message": f"Successfully enrolled the teacher using {teacher_email}",
        "data": course_enrollment_user_model(result)
    }

  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except Conflict as conflict:
    Logger.error(conflict)
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise Conflict(str(conflict)) from conflict
  except HttpError as ae:
    Logger.error(ae)
    raise ClassroomHttpException(status_code=ae.resp.status,
                              message=str(ae)) from ae
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e

@router.get("/{section_id}/teachers/{teacher}",
response_model=GetTeacherResponseModel)
def get_teacher(section_id: str,teacher:str,request: Request):
  """Get teacher for a section .If teacher is present in given section
    get teacher details else throw
  Args:
      section_id (str): section_id in firestore
      teacher(str): teachers email or Id
  Raises:
      HTTPException: 500 Internal Server Error if something fails
      HTTPException: 404 Section with section id is not found
      HTTPException: 404 Teacher with teacher email is not found
  Returns:
    GetTeacherResponseModel: object which contains user details
  """
  try:
    headers = {"Authorization": request.headers.get("Authorization")}
    user_id = get_user_id(user=teacher, headers=headers)
    section = Section.find_by_id(section_id)
    result=CourseEnrollmentMapping.\
    find_course_enrollment_record(section.key,user_id,"faculty")
    if result is None:
      raise ResourceNotFoundException(
          f"Teacher not found in this section {section_id}")
    return {
        "message": f"Successfully get teacher details by {teacher}",
        "data": course_enrollment_user_model(result)
    }
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except HttpError as ae:
    Logger.error(ae)
    raise ClassroomHttpException(status_code=ae.resp.status,
                              message=str(ae)) from ae
  except Exception as e:
    Logger.error(e)
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(e)
    raise InternalServerError(str(e)) from e

@router.delete("/{section_id}/teachers/{teacher}",
response_model=DeleteTeacherFromSectionResponseModel)
def delete_teacher(section_id: str,teacher:str,request: Request):
  """Delete teacher for a section
  Args:
      section_id (str): section_id in firestore
      teacher(str): teachers email or Id
  Raises:
      HTTPException: 500 Internal Server Error if something fails
      HTTPException: 404 Section with section id is not found
      HTTPException: 404 Teacher with teacher email is not found
  Returns:
      DeleteTeacherFromSectionResponseModel: response
  """
  try:
    headers = {"Authorization": request.headers.get("Authorization")}
    user_id = get_user_id(user=teacher, headers=headers)
    section = Section.find_by_id(section_id)
    result=CourseEnrollmentMapping.find_active_enrolled_teacher_record(
     section_key = section.key,user_id = user_id)
    if result is None:
      raise ResourceNotFoundException(
          f"Teacher not found in this section {section_id}")
    classroom_crud.delete_teacher(section.classroom_id,result.user.email)
    result.status="inactive"
    result.update()
    return {
        "message": ("Successfully deleted the teacher from the section"
        + f" {section_id} using {teacher}")
    }
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except HttpError as ae:
    Logger.error(ae)
    raise ClassroomHttpException(status_code=ae.resp.status,
                              message=str(ae)) from ae
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e

@router.delete("/{section_id}", response_model=DeleteSectionResponseModel)
def delete_section(section_id: str):
  """Get a section details from db and archive record
  from section collection and
  google classroom course

  Args:
      section_id (str): section_id in firestore
  Raises:
      HTTPException: 500 Internal Server Error if something fails
      ResourceNotFound: 404 Section with section id is not found
  Returns:
    {"message": "Successfully deleted section"}
  """
  try:
    section_details = Section.find_by_id(section_id)
    classroom_crud.update_course_state(section_details.classroom_id,\
      "ARCHIVED")
    section_details.status = "ARCHIVED"
    section_details.enrollment_status="CLOSED"
    section_details.update()
    Section.soft_delete_by_id(section_id)
    rows=[{
      "sectionId":section_details.id,
      "courseId":section_details.classroom_id,
      "classroomUrl":section_details.classroom_url,
      "name":section_details.section,
      "description":section_details.description,
      "cohortId":section_details.cohort.id,
      "courseTemplateId":section_details.course_template.id,
      "status":section_details.status,
      "enrollmentStatus": section_details.enrollment_status,
      "maxStudents": section_details.max_students,
      "timestamp":datetime.datetime.utcnow()
    }]
    insert_rows_to_bq(rows=rows,
                      dataset=BQ_DATASET,
                      table_name=BQ_TABLE_DICT["BQ_COLL_SECTION_TABLE"])
    return {
        "message": f"Successfully archived the Section with id {section_id}"
    }
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except HttpError as ae:
    Logger.error(ae)
    raise ClassroomHttpException(status_code=ae.resp.status,
                              message=str(ae)) from ae
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.get("", response_model=SectionListResponseModel)
def section_list(skip: int = 0, limit: int = 10):
  """Get a all section details from db

  Args:
  Raises:
      HTTPException: 500 Internal Server Error if something fails
      HTTPException:
        500 If refereced course_template and cohort object does not exists in db
  Returns:
    {"status":"Success","new_course":{}}: Returns section details from  db,
    {'status': 'Failed'} if the user creation raises an exception
  """
  try:
    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")
    if limit < 1:
      raise ValidationError(
          "Invalid value passed to \"limit\" query parameter")

    sections = Section.fetch_all(skip, limit)
    sections_list = list(map(convert_section_to_section_model, sections))
    return {"data": sections_list}
  except ValidationError as ve:
    raise BadRequest(str(ve)) from ve
  except Exception as e:
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise InternalServerError(str(e)) from e


@router.patch("", response_model=UpdateSectionResponseModel)
def update_section(sections_details: UpdateSection):
  """Update section API

  Args:
    id(str): id of the section in firestore
    course_state:Updated course state it can be any one of
    [ACTIVE,ARCHIVED,PROVISIONED,DECLINED,SUSPENDED]
    section_name (section): Section name
    description (str):Description
    course_id(str):course_id of google classroom
  Raises:
    HTTPException: 500 Internal Server Error if something fails
    ResourceNotFound : 404 if course_id or section_id is not found
  Returns:
    {"status":"Success","data":{}}: Returns Updated course details,
    {'status': 'Failed'} if the user creation raises an exception
  """
  try:
    section = Section.find_by_id(sections_details.id)
    new_course = classroom_crud.update_course(sections_details.course_id,
                                              sections_details.section_name,
                                              sections_details.description)
    if new_course is None:
      raise ResourceNotFoundException(
          "Course with Course_id"
          f" {sections_details.course_id} is not found in classroom")
    section.section = sections_details.section_name
    section.description = sections_details.description
    section.max_students = sections_details.max_students
    section.update()
    updated_section = convert_section_to_section_model(section)
    rows=[{
      "sectionId":sections_details.id,\
      "courseId":sections_details.course_id,\
      "classroomUrl":updated_section["classroom_url"],\
        "name":sections_details.section_name,\
        "description":sections_details.description,\
          "cohortId":updated_section["cohort"].split("/")[1],\
          "courseTemplateId":updated_section["course_template"].split("/")[1],\
            "status":section.status,
            "enrollmentStatus": section.enrollment_status,
            "maxStudents": section.max_students,
          "timestamp":datetime.datetime.utcnow()
    }]
    insert_rows_to_bq(
      rows=rows,
      dataset=BQ_DATASET,
      table_name=BQ_TABLE_DICT["BQ_COLL_SECTION_TABLE"]
      )
    return {"data": updated_section}
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except HttpError as hte:
    Logger.error(hte)
    raise ClassroomHttpException(status_code=hte.resp.status,
                              message=str(hte)) from hte
  except Exception as e:
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(e)
    raise InternalServerError(str(e)) from e

@router.patch("/{section_id}/update_classroom_code",
              response_model=GetSectiontResponseModel)
def update_section_classroom_code(section_id:str):
  """_summary_

  Args:
      section_id (str): _description_
      classroom_code (str): _description_

  Raises:
      ResourceNotFound: _description_
      InternalServerError: _description_

  Returns:
      _type_: _description_
  """
  try:
    section=Section.find_by_id(section_id)
    course=classroom_crud.get_course_by_id(section.classroom_id)
    if course is None:
      raise ResourceNotFoundException(
          "Classroom with section id" +
          f" {section_id} is not found")
    section.classroom_code=course["enrollmentCode"]
    section.update()
    return {
      "message":"Successfully updated the classroom code",
      "data":convert_section_to_section_model(section)
      }
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e

@router.post("/{section_id}/enable_notifications",
             response_model=EnableNotificationsResponse)
def section_enable_notifications_pub_sub(section_id:str):
  """Resgister section with a pub/sub topic

  Args:
      section_id (str): unique section id
  Raises:
      InternalServerError: 500 Internal Server Error if something fails
      ResourceNotFound: 404 Section with section id is not found
      ClassroomHttpException: raise error according to the HTTPError exception
  Returns:
      _type_: _description_
  """
  try:
    section = Section.find_by_id(section_id)
    responses = [
        classroom_crud.enable_notifications(
            section.classroom_id, i) for i in FEED_TYPES
    ]
    return {
          "message":
          "Successfully enable the notifications of the course using section "
          + f"{section_id} id",
          "data":responses
      }
  except ValidationError as ve:
    raise BadRequest(str(ve)) from ve
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except HttpError as hte:
    raise ClassroomHttpException(status_code=hte.resp.status,
                              message=str(hte)) from hte
  except InternalServerError as ie:
    raise InternalServerError(str(ie)) from ie
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.get("/{section_id}/assignments/{assignment_id}",
            response_model=AssignmentModel)
def get_assignment(section_id: str, assignment_id: str):
  """Get course work details using section id and course work id
  Args:
      section_id (str): section unique id
      assignment_id (str): course work/assignment unique id
  Raises:
      InternalServerError: 500 Internal Server Error if something fails
      ClassroomHttpException: raise error according to the HTTPError exception
      ResourceNotFound: 404 Section with section id is not found
  Returns:
      AssignmentModel: AssignmentModel object which
        contains all the course work details
  """
  try:
    section = Section.find_by_id(section_id)
    assignment = classroom_crud.get_course_work(course_id=section.classroom_id,
                                                course_work_id=assignment_id)
    return convert_assignment_to_assignment_model(assignment)
  except HttpError as hte:
    raise ClassroomHttpException(status_code=hte.resp.status,
                              message=str(hte)) from hte
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e

@router.get("/{section_id}/get_coursework_list",
            response_model=GetCourseWorkList)
def get_coursework_list(section_id: str):
  """Get course work details using section id
  Args:
      section_id (str): section unique id
  Raises:
      InternalServerError: 500 Internal Server Error if something fails
      ClassroomHttpException: raise error according to the HTTPError exception
      ResourceNotFound: 404 Section with section id is not found
  Returns:
      AssignmentModel: AssignmentModel object which
        contains all the course work details
  """
  try:
    data=[]
    course_work_list = classroom_crud.get_course_work_list\
      (section_id=section_id)
    for x in course_work_list:
      data.append(convert_coursework_to_short_coursework_model(x))
    return {"data":data}
  except HttpError as hte:
    raise ClassroomHttpException(status_code=hte.resp.status,
                              message=str(hte)) from hte
@router.patch("/{section_id}/coursework/{coursework_id}",
              response_model=ImportGradeResponseModel,
              status_code=status.HTTP_202_ACCEPTED)
def import_grade(section_id: str,coursework_id:str,
                 background_tasks: BackgroundTasks):
  """Get a section details from db and use the coursework Id
  Args:
      section_id (str): section_id in firestore
      coursework_id(str): coursework_id of coursework in classroom
  Raises:
      HTTPException: 500 Internal Server Error if something fails
      ResourceNotFound: 404 Section with section id is not found or
        coursework is not found
  Returns:
    {"status":"Success","new_course":{}}: Returns section details from  db,
    {'status': 'Failed'} if the user creation raises an exception
  """
  try:
    section = Section.find_by_id(section_id)
    result = classroom_crud.get_course_work(
    section.classroom_id,coursework_id)
    #Get url mapping of google forms view links and edit ids
    is_google_form_present = False
    if "materials" in result.keys():
      for material in result["materials"]:
        if "form" in material.keys():
          is_google_form_present = True
          background_tasks.add_task(update_grades,material,
                                    section,coursework_id)

      if is_google_form_present:
        return {
           "message":"Grades for coursework will be updated shortly"}
      else:
        raise ResourceNotFoundException(
          f"Form is not present for coursework_id {coursework_id}"
          )
    else:
      raise ResourceNotFoundException(
          f"Form is not present for coursework_id {coursework_id}"
          )
  except HttpError as hte:
    Logger.error(hte)
    message = str(hte)
    if hte.resp.status == 404:
      message = "Coursework not found"
    raise ClassroomHttpException(status_code=hte.resp.status,
                              message=message) from hte
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except Exception as e:
    Logger.error(e)
    error = traceback.format_exc().replace("\n", " ")
    Logger.error(error)
    raise InternalServerError(str(e)) from e

@router.patch("/{section_id}/change_enrollment_status/{enrollment_status}",
              response_model=UpdateEnrollmentStatusSectionModel)
def update_enrollment_status(section_id:str,enrollment_status: str):
  """Update enrollment status for a section

  Args:
    section_id(str): id of the section in firestore
    status: enrollment status of the section
    [OPEN,CLOSED]
  Raises:
    HTTPException: 500 Internal Server Error if something fails
    ResourceNotFound : 404 if course_id or section_id is not found
  Returns:
    {"status":"Success","data":{}}: Returns Updated course details,
    {'status': 'Failed'} if the user creation raises an exception.
  """
  try:
    if enrollment_status in ("OPEN","CLOSED"):
      section = Section.find_by_id(section_id)
      section.enrollment_status = enrollment_status
      section.update()
      updated_section = convert_section_to_section_model(section)
      rows=[{
      "sectionId":section.id,\
      "courseId":section.course_id,\
      "classroomUrl":updated_section["classroom_url"],\
        "name":section.section_name,\
        "description":section.description,\
          "cohortId":updated_section["cohort"].split("/")[1],\
          "courseTemplateId":updated_section["course_template"].split("/")[1],\
            "status":section.status,
            "enrollmentStatus": updated_section.enrollment_status,
            "maxStudents": section.max_students,
          "timestamp":datetime.datetime.utcnow()
          }]
      insert_rows_to_bq(
      rows=rows,
      dataset=BQ_DATASET,
      table_name=BQ_TABLE_DICT["BQ_COLL_SECTION_TABLE"]
      )
      return {"data": updated_section}
    else:
      raise ValidationError("Accepted parameters are only 'OPEN' and 'CLOSED'")

  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except HttpError as hte:
    Logger.error(hte)
    raise ClassroomHttpException(status_code=hte.resp.status,
                              message=str(hte)) from hte
  except Exception as e:
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(e)
    raise InternalServerError(str(e)) from e
