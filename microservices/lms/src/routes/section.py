""" Section endpoints """
import traceback
from common.models import Cohort, CourseTemplate, Section, CourseEnrollmentMapping
from common.utils.errors import InvalidTokenError, ResourceNotFoundException, ValidationError
from common.utils.http_exceptions import (CustomHTTPException,
                                          InternalServerError, InvalidToken,
                                          ResourceNotFound, BadRequest)
from common.utils import classroom_crud
from common.utils.logging_handler import Logger
from fastapi import APIRouter, Request
from googleapiclient.errors import HttpError
from schemas.course_details import CourseDetails, EnableNotificationsDetails, EnableNotificationsResponse
from schemas.error_schema import (ConflictResponseModel,
                                  InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ValidationErrorResponseModel)
from schemas.section import (
    AddStudentResponseModel, AddStudentToSectionModel,
    CreateSectiontResponseModel, DeleteSectionResponseModel,
    GetSectiontResponseModel, SectionDetails, SectionListResponseModel,
    ClassroomCourseListResponseModel, UpdateSectionResponseModel)
from schemas.update_section import UpdateSection
from services import student_service ,common_service
from utils.helper import convert_section_to_section_model

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


@router.get("/get_courses/", response_model=ClassroomCourseListResponseModel)
def get_courses(skip: int = 0, limit: int = 10):
  """Get courses list
  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    List of courses in classroom ,
    {'status': 'Failed'} if the user creation raises an exception
  """
  try:
    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")
    if limit < 1:
      raise ValidationError(
          "Invalid value passed to \"limit\" query parameter")
    course_list = classroom_crud.get_course_list()
    return {"data": list(course_list)[skip:limit]}
  except ValidationError as ve:
    raise BadRequest(str(ve)) from ve
  except HttpError as hte:
    Logger.error(hte)
    raise CustomHTTPException(status_code=hte.resp.status,
                              success=False,
                              message=str(hte),
                              data=None) from hte
  except Exception as e:
    Logger.error(e)
    error = traceback.format_exc().replace("\n", " ")
    Logger.error(error)
    raise InternalServerError(str(e)) from e


@router.post("", response_model=CreateSectiontResponseModel)
def create_section(sections_details: SectionDetails,request: Request):
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
    name = course_template_details.name
    # Get course by course id for copying from master course
    current_course = classroom_crud.get_course_by_id(
        course_template_details.classroom_id)
    if current_course is None:
      raise ResourceNotFoundException(
          "classroom  with id" +
          f" {course_template_details.classroom_id} is not found")
    # Create a new course

    new_course = classroom_crud.create_course(name,
                                              sections_details.description,
                                              sections_details.name, "me")
    # Get topics of current course
    topics = classroom_crud.get_topics(course_template_details.classroom_id)
    # add new_course to pubsub topic for both course work and roaster changes
    classroom_crud.enable_notifications(new_course["id"],
                                        "COURSE_WORK_CHANGES")
    classroom_crud.enable_notifications(new_course["id"],
                                        "COURSE_ROSTER_CHANGES")
    #If topics are present in course create topics returns a dict
    # with keys a current topicID and new topic id as values
    if topics is not None:
      topic_id_map = classroom_crud.create_topics(new_course["id"], topics)
    # Get coursework of current course and create a new course
    coursework_list = classroom_crud.get_coursework(
        course_template_details.classroom_id)
    for coursework in coursework_list:
      #Check if a coursework is linked to a topic if yes then
      # replace the old topic id to new topic id using topic_id_map
      if "topicId" in coursework.keys():
        coursework["topicId"] = topic_id_map[coursework["topicId"]]
      #Check if a material is present in coursework
      if "materials" in coursework.keys():
        # Calling function to get edit_url and view url of
        # google form which returns
        # a dictionary of view_links as keys and edit
        #  likns as values of google form
        url_mapping = classroom_crud.get_edit_url_and_view_url_mapping_of_form()
        # Loop to check if a material in courssework has a google
        # form attached to it
        # update the  view link to edit link and attach it as a form
        for material in coursework["materials"]:
          if "form" in material.keys():
            material["link"] = {
                "title": material["form"]["title"],
                "url": url_mapping[material["form"]["formUrl"]]
            }
            # remove form from  material dict
            material.pop("form")
            # material["form"]["formUrl"]=
            # url_mapping[material["form"]["formUrl"]]
    # Create coursework in new course
    if coursework_list is not None:
      classroom_crud.create_coursework(new_course["id"], coursework_list)

    # add Instructional designer
    sections_details.teachers.append(
        course_template_details.instructional_designer)

    for teacher_email in sections_details.teachers:
      # classroom_crud.add_teacher(new_course["id"], teacher_email)
      invitation_object = classroom_crud.invite_teacher(new_course["id"],
                            teacher_email)
    # Storing classroom details
      print("This is invitation API response ")
      print(invitation_object)
      classroom_crud.acceept_invite(invitation_object["id"],teacher_email)
      print("Invite Accepted")
      user_profile = classroom_crud.get_user_profile_information(teacher_email)
      # classroom_crud.add_teacher(new_course["id"], teacher_email)
      print("User profile Information ______",user_profile)
      gaid = user_profile["id"]
      name =  user_profile["name"]["givenName"]
      last_name =  user_profile["name"]["givenName"]
      photo_url =  user_profile["photoUrl"]
      print(f"Gaid {gaid} first name {name} last name \
        {last_name} photo url {photo_url}")
    # Save the new record of seecion in firestore
      data = {
      "first_name":user_profile["name"]["givenName"],
      "last_name": user_profile["name"]["lastName"],
      "email":teacher_email,
      "user_type": "faculty",
      "user_type_ref": "",
      "user_groups": [],
      "status": "active",
      "is_registered": True,
      "failed_login_attempts_count": 0,
      "access_api_docs": False,
      "gaia_id":user_profile["id"]
        }
      common_service.create_teacher(headers,data)
    section = Section()
    section.name = name
    section.section = sections_details.name
    section.description = sections_details.description
    # Reference document can be get using get() method
    section.course_template = course_template_details
    section.cohort = cohort_details
    section.classroom_id = new_course["id"]
    section.classroom_code = new_course["enrollmentCode"]
    section.classroom_url = new_course["alternateLink"]
    section.teachers = sections_details.teachers
    section.enrolled_students_count=0
    section.save()
    new_section = convert_section_to_section_model(section)
    return {"data": new_section}
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except HttpError as hte:
    Logger.error(hte)
    raise CustomHTTPException(status_code=hte.resp.status,
                              success=False,
                              message=str(hte),
                              data=None) from hte
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
      HTTPException: 404 Section with section id is not found
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
    raise CustomHTTPException(status_code=ae.resp.status,
                              success=False,
                              message=str(ae),
                              data=None) from ae
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
      HTTPException: 404 Section with section id is not found
  Returns:
    {"message": "Successfully deleted section"}
  """
  try:
    section_details = Section.find_by_id(section_id)
    classroom_crud.update_course_state(section_details.classroom_id,\
      "ARCHIVED")
    Section.soft_delete_by_id(section_id)
    return {
        "message": f"Successfully archived the Section with id {section_id}"
    }
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
    print(err)
    raise InternalServerError(str(e)) from e


@router.patch("", response_model=UpdateSectionResponseModel)
def update_section(sections_details: UpdateSection,request: Request):
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
    print("1")
    headers = {"Authorization": request.headers.get("Authorization")}
    section = Section.find_by_id(sections_details.id)
    new_course = classroom_crud.update_course(sections_details.course_id,
                                              sections_details.section_name,
                                              sections_details.description)
    if new_course is None:
      raise ResourceNotFoundException(
          "Course with Course_id"
          f" {sections_details.course_id} is not found in classroom")
    add_teacher_list = list(
        set(sections_details.teachers) - set(section.teachers))
    print("ADD teachers list ",add_teacher_list)
    for i in add_teacher_list:
      # classroom_crud.add_teacher(sections_details.course_id, i)
      invitation_object = classroom_crud.invite_teacher(
                            sections_details.course_id,i)
      # Storing classroom details
      print("This is invitation API response ")
      print(invitation_object)
      classroom_crud.acceept_invite(invitation_object["id"],i)
      user_profile = classroom_crud.get_user_profile_information(i)
      data = {
      "first_name":user_profile["name"]["givenName"],
      "last_name": user_profile["name"]["givenName"],
      "email":i,
      "user_type": "faculty",
      "user_type_ref": "",
      "user_groups": [],
      "status": "active",
      "is_registered": True,
      "failed_login_attempts_count": 0,
      "access_api_docs": False,
      "gaia_id":user_profile["id"]
        }
      common_service.create_teacher(headers,data)
      print("Invite Accepted userprofile is",user_profile)
    remove_teacher_list = list(
        set(section.teachers) - set(sections_details.teachers))
    for i in remove_teacher_list:
      classroom_crud.delete_teacher(sections_details.course_id, i)
    section.section = sections_details.section_name
    section.description = sections_details.description
    section.teachers = sections_details.teachers
    section.update()
    updated_section = convert_section_to_section_model(section)
    return {"data": updated_section}
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except HttpError as hte:
    Logger.error(hte)
    raise CustomHTTPException(status_code=hte.resp.status,
                              success=False,
                              message=str(hte),
                              data=None) from hte
  except Exception as e:
    err = traceback.format_exc().replace("\n", " ")
    print(err)
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.post("/{cohort_id}/students", response_model=AddStudentResponseModel)
def enroll_student_section(cohort_id: str,
                           input_data: AddStudentToSectionModel,
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
    if len(sections) == 0:
      raise ResourceNotFoundException("Given CohortId\
         does not have any sections")
    section = student_service.get_section_with_minimum_student(sections)

    headers = {"Authorization": request.headers.get("Authorization")}
    user_object = classroom_crud.enroll_student(
        headers,
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
    return {
        "message":
        f"Successfully Added the Student with email {input_data.email}",
        "data" : course_enrollment_id
    }
  except InvalidTokenError as ive:
    raise InvalidToken(str(ive)) from ive
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
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


@router.post("/copy_course/")
def copy_courses(course_details: CourseDetails):
  """Copy course  API

  Args:
    course_id (Course): Course_id of a course that needs to copied

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    {"status":"Success","new_course":{}}: Returns new course details,
    {'status': 'Failed'} if the user creation raises an exception
  """
  try:
    input_course_details_dict = {**course_details.dict()}
    course_id = input_course_details_dict["course_id"]
    # Get course by course id
    current_course = classroom_crud.get_course_by_id(course_id)
    if current_course is None:
      return "No course found "
    # Create a new course
    new_course = classroom_crud.create_course(current_course["name"],
                                              current_course["description"],
                                              current_course["section"],
                                              current_course["ownerId"])

    # Get topics of current course
    topics = classroom_crud.get_topics(course_id)
    #If topics are present in course create topics returns a dict
    # with keys a current topicID and new topic id as values
    if topics is not None:
      topic_id_map = classroom_crud.create_topics(new_course["id"], topics)
    # Get coursework of current course and create a new course
    coursework_list = classroom_crud.get_coursework(course_id)
    for coursework in coursework_list:
      #Check if a coursework is linked to
      #  a topic if yes then
      # replace the old topic id to new
      # topic id using topic_id_map
      if "topicId" in coursework.keys():
        coursework["topicId"] = topic_id_map[coursework["topicId"]]
      #Check if a material is present in coursework
      if "materials" in coursework.keys():
        # Calling function to get edit_url and view url of google
        #  form which returns
        # a dictionary of view_links as keys and edit likns as
        # values of google form
        url_mapping = classroom_crud.get_edit_url_and_view_url_mapping_of_form()
        # Loop to check if a material in courssework has
        #  a google form attached to it
        # update the  view link to edit link and attach it as a form
        for material in coursework["materials"]:
          if "form" in material.keys():
            material["link"] = {
                "title": material["form"]["title"],
                "url": url_mapping[material["form"]["formUrl"]]
            }
            # remove form from  material dict
            material.pop("form")
            # material["form"]["formUrl"]=
            # url_mapping[material["form"]["formUrl"]]
    # Create coursework in new course
    if coursework_list is not None:
      classroom_crud.create_coursework(new_course["id"], coursework_list)
    SUCCESS_RESPONSE["new_course"] = new_course
    SUCCESS_RESPONSE["coursework_list"] = coursework_list
    return SUCCESS_RESPONSE
  except HttpError as hte:
    Logger.error(hte)
    raise CustomHTTPException(status_code=hte.resp.status,
                              success=False,
                              message=str(hte),
                              data=None) from hte
  except Exception as e:
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise InternalServerError(str(e)) from e


@router.post("/enable_notifications",
             response_model=EnableNotificationsResponse)
def section_enable_notifications_pub_sub(
    enable_notifications_details: EnableNotificationsDetails):
  """Resgister course with a pub/sub topic

  Args:
      enable_notifications_details (EnableNotificationsDetails):
      An object of the EnableNotificationsDetails
      Model which contains required details
  Raises:
      InternalServerError: 500 Internal Server Error if something fails
      CustomHTTPException: raise error according to the HTTPError exception
  Returns:
      _type_: _description_
  """
  try:
    # check both the id's
    if (not enable_notifications_details.course_id
        and not enable_notifications_details.section_id):
      raise ValidationError("Either Section id or course id is required")
    # if course_id is empty and section id is passed then get course_id
    if not enable_notifications_details.course_id:
      section = Section.find_by_id(enable_notifications_details.section_id)
      enable_notifications_details.course_id = section.classroom_id

    response = classroom_crud.enable_notifications(
        enable_notifications_details.course_id,
        enable_notifications_details.feed_type)
    if enable_notifications_details.section_id:
      return {
          "message":
          "Successfully enable the notifications of the course using section "
          + f"{enable_notifications_details.section_id} id",
          "data":
          response
      }
    return {
        "message":
        "Successfully enable the notifications of the course using " +
        f"{enable_notifications_details.course_id} id",
        "data": response
    }
  except ValidationError as ve:
    raise BadRequest(str(ve)) from ve
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except InternalServerError as ie:
    raise InternalServerError(str(ie)) from ie
  except HttpError as hte:
    raise CustomHTTPException(status_code=hte.resp.status,
                              success=False,
                              message=str(hte),
                              data=None) from hte
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e

