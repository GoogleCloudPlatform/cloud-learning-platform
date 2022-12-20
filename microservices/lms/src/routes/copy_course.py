""" User endpoints """
import traceback
import datetime
from fastapi import APIRouter
from common.utils.logging_handler import Logger
from common.models.section import Section
from common.models.course_template import CourseTemplate
from common.models.cohort import Cohort
from common.utils.errors import ResourceNotFoundException, InvalidTokenError
from common.utils.http_exceptions import ResourceNotFound, InternalServerError, InvalidToken, CustomHTTPException
from googleapiclient.errors import HttpError
from services import classroom_crud
from services.classroom_crud import (
                            get_edit_url_and_view_url_mapping_of_form)
from schemas.course_details import CourseDetails
from schemas.section import (SectionDetails, AddStudentToSectionModel,
 AddStudentResponseModel,DeleteSectionResponseModel,SectionListResponseModel,
 CreateSectiontResponseModel,GetSectiontResponseModel,
 UpdateSectionResponseModel)
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ConflictResponseModel,
                                  ValidationErrorResponseModel)
from schemas.update_section import UpdateSection
from services import classroom_crud
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


@router.get("/get_courses/",response_model= SectionListResponseModel)
def get_courses():
  """Get courses list
  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    List of courses in classroom ,
    {'status': 'Failed'} if the user creation raises an exception
  """
  try:
    course_list = classroom_crud.get_course_list()
    return {"data" :  list(course_list)}
  except Exception as e:
    Logger.error(e)
    error=traceback.format_exc().replace("\n", " ")
    Logger.error(error)
    raise InternalServerError(str(e)) from e




@router.post("",response_model= CreateSectiontResponseModel)
def create_section(sections_details: SectionDetails):
  """Create section API
  Args:
    name (section): Section name
    description (str):Description
    classroom_template_id(str):course_template_id uuid from firestore
    cohort_id(str):cohort uuid from firestore
    teachers_list(list):List of teachers to be added
  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    {"status":"Success","new_course":{}}: Returns new course details,
    {'status': 'Failed'} if the user creation raises an exception
  """
  try:
    course_template_details = CourseTemplate.find_by_uuid(
        sections_details.course_template)
    if course_template_details is None:
      raise ResourceNotFound(
          "Course Template with uuid" +
          " {sections_details.course_template} is not found")
    cohort_details = Cohort.find_by_uuid(sections_details.cohort)

    if cohort_details is None:
      raise ResourceNotFound(
          f"cohort with uuid {sections_details.cohort} is not found")

    name = course_template_details.name
    # Get course by course id for copying from master course
    current_course = classroom_crud.get_course_by_id(
        course_template_details.classroom_id)
    if current_course is None:
      raise ResourceNotFound(
          "classroom  with uuid" +
          f" {course_template_details.classroom_id} is not found")
    # Create a new course

    new_course = classroom_crud.create_course(name,
                                              sections_details.description,
                                              sections_details.name, "me")
    # Get topics of current course
    topics = classroom_crud.get_topics(course_template_details.classroom_id)
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
        coursework["topicId"]=topic_id_map[coursework["topicId"]]
      #Check if a material is present in coursework
      if "materials" in coursework.keys():
        # Calling function to get edit_url and view url of
        # google form which returns
        # a dictionary of view_links as keys and edit
        #  likns as values of google form
        url_mapping=get_edit_url_and_view_url_mapping_of_form()
        # Loop to check if a material in courssework has a google
        # form attached to it
        # update the  view link to edit link and attach it as a form
        for material in coursework["materials"]:
          if "form" in material.keys():
            material["link"]={
              "title":material["form"]["title"],
              "url":url_mapping[material["form"]["formUrl"]]
            }
            # remove form from  material dict
            material.pop("form")
            # material["form"]["formUrl"]=
            # url_mapping[material["form"]["formUrl"]]
    # Create coursework in new course
    if coursework_list is  not None:
      classroom_crud.create_coursework(new_course["id"], coursework_list)

    for teacher_email in sections_details.teachers_list:
      classroom_crud.add_teacher(new_course["id"], teacher_email)
    # Save the new record of seecion in firestore
    section = Section()
    section.name = name
    section.section = sections_details.name
    section.description = sections_details.description
    # Reference document can be get using get() method
    section.course_template = course_template_details
    section.cohort = cohort_details
    section.classroom_id = new_course["id"]
    section.classroom_code = new_course["enrollmentCode"]
    section.teachers_list = sections_details.teachers_list
    section.created_timestamp = datetime.datetime.now()
    section.uuid = section.save().id
    section.save()
    new_section =  convert_section_to_section_model(section)
    return {"data" :new_section }
  except ResourceNotFound as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except Exception as e:
    error =traceback.format_exc().replace("\n", " ")
    Logger.error(error)
    Logger.error(e)
    raise InternalServerError(str(e)) from e

@router.get("/cohort/{cohort_id}/sections",
response_model=SectionListResponseModel)
def list_section(cohort_id: str):
  """ Get a list of sections of one cohort from db

  Args:
    cohort_id(str):cohort uuid from firestore db
  Raises:
    HTTPException: 500 Internal Server Error if something fails
    ResourceNotFound: 404 Resource not found exception
  Returns:
    {"status":"Success","data":{}}: Returns list of sections
    {'status': 'Failed',"data":null}
  """
  try:

    # Get cohort Id and create a reference of cohort object

    cohort = Cohort.find_by_uuid(cohort_id)
    if cohort is None:
      raise ResourceNotFoundException(
          f"Cohort with uuid {cohort_id} is not found")
    # Using the cohort object reference key query sections model to get a list
    # of section of a perticular cohort
    result = Section.collection.filter("cohort", "==", cohort.key).fetch()
    sections_list = list(map(convert_section_to_section_model, result))
    return {"data" :  sections_list}
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except Exception as e:
    Logger.error(e)
    err = traceback.format_exc().replace("\n", " ")
    raise InternalServerError(str(e)) from e


@router.get("/{section_id}",response_model=GetSectiontResponseModel)
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
    section_details = Section.find_by_uuid(section_id)
    if section_details is None:
      raise ResourceNotFoundException(
          f"Section with uuid {section_id} is not found")
    # Get course by course id
    new_section =  convert_section_to_section_model(section_details)
    return {"data" :new_section}
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
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
    section_details = Section.find_by_uuid(section_id)
    if section_details:
      classroom_crud.update_course_state(section_details.classroom_id,\
        "ARCHIVED")
      section_details = Section.archive_by_uuid(section_id)
      return {
        "message": f"Successfully archived the Section with uuid {section_id}"
      }

    else:
      raise ResourceNotFoundException(
          f"Section with uuid {section_id} is not found")
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except HttpError as ae:
    print("In Except")
    print(ae)
    raise CustomHTTPException(status_code=ae.resp.status,
                              success=False,
                              message=str(ae),
                              data=None) from ae
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.get("",response_model=SectionListResponseModel)
def section_list():
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
    sections = Section.collection.filter("is_deleted", "==", False).fetch()
    sections_list = list(map(convert_section_to_section_model, sections))
    return {"data" :  sections_list}
  except Exception as e:
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise InternalServerError(str(e)) from e

@router.patch("", response_model=UpdateSectionResponseModel)
def update_section(sections_details: UpdateSection):
  """Update section API

  Args:
    uuid(str): uuid of the section in firestore
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

    section = Section.find_by_uuid(sections_details.uuid)
    if section is None:
      raise ResourceNotFound(
          f"Section with uuid {sections_details.uuid} is not found")

    new_course = classroom_crud.update_course(sections_details.course_id,
                                              sections_details.section_name,
                                              sections_details.description,
                                              sections_details.course_state)
    if new_course is None:
      raise ResourceNotFound(
          "Course with Course_id"
          f" {sections_details.course_id} is not found in classroom")
    section.section = sections_details.section_name
    section.description = sections_details.description
    section.last_updated_timestamp = datetime.datetime.utcnow()
    section.save()
    updated_section =  convert_section_to_section_model(section)
    return {"data" :updated_section}
  except ResourceNotFound as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e

@router.post("/{sections_id}/students", response_model=AddStudentResponseModel)
def enroll_student_section(sections_id: str,
                           input_data: AddStudentToSectionModel):
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
    section = Section.find_by_uuid(sections_id)
    if section is None:
      raise ResourceNotFoundException(
          f"Section with uuid {sections_id} is not found")
    classroom_crud.enroll_student(token={**input_data.credentials.dict()},
                                  student_email=input_data.email,
                                  course_id=section.classroom_id,
                                  course_code=section.classroom_code)
    return {
        "message":
        f"Successfully Added the Student with email {input_data.email}"
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
        coursework["topicId"]=topic_id_map[coursework["topicId"]]
      #Check if a material is present in coursework
      if "materials" in coursework.keys():
        # Calling function to get edit_url and view url of google
        #  form which returns
        # a dictionary of view_links as keys and edit likns as
        # values of google form
        url_mapping = get_edit_url_and_view_url_mapping_of_form()
        # Loop to check if a material in courssework has
        #  a google form attached to it
        # update the  view link to edit link and attach it as a form
        for material in coursework["materials"]:
          if "form" in material.keys():
            material["link"]={
              "title":material["form"]["title"],
              "url":url_mapping[material["form"]["formUrl"]]
            }
            # remove form from  material dict
            material.pop("form")
            # material["form"]["formUrl"]=
            # url_mapping[material["form"]["formUrl"]]
    # Create coursework in new course
    if coursework_list is  not None:
      classroom_crud.create_coursework(new_course["id"], coursework_list)
    SUCCESS_RESPONSE["new_course"] = new_course
    SUCCESS_RESPONSE["coursework_list"] = coursework_list
    return SUCCESS_RESPONSE
  except Exception as e:
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise InternalServerError(str(e)) from e