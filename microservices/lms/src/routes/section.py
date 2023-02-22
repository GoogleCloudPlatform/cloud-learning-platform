""" Section endpoints """
import traceback
from common.models import Cohort, CourseTemplate, Section
from common.utils.errors import ResourceNotFoundException, ValidationError
from common.utils.http_exceptions import (CustomHTTPException,
                                          InternalServerError,
                                          ResourceNotFound, BadRequest)
from common.utils import classroom_crud
from common.utils.logging_handler import Logger
from fastapi import APIRouter, Request
from googleapiclient.errors import HttpError
from schemas.classroom_courses import EnableNotificationsResponse
from schemas.error_schema import (ConflictResponseModel,
                                  InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ValidationErrorResponseModel)
from schemas.section import (
    CreateSectiontResponseModel, DeleteSectionResponseModel,
    GetSectiontResponseModel, SectionDetails, SectionListResponseModel,
    UpdateSectionResponseModel, AssignmentModel)
from schemas.update_section import UpdateSection
from services import common_service
from utils.helper import (convert_section_to_section_model,
                          convert_assignment_to_assignment_model,FEED_TYPES)

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
    # Get course by course id for copying from master course
    current_course = classroom_crud.get_course_by_id(
        course_template_details.classroom_id)
    if current_course is None:
      raise ResourceNotFoundException(
          "classroom  with id" +
          f" {course_template_details.classroom_id} is not found")
    # Create a new course
    print("Current Course ____",current_course)
    new_course = classroom_crud.create_course(course_template_details.name,
                                              sections_details.description,
                                              sections_details.name, "me")

    # Get topics of current course
    topics = classroom_crud.get_topics(course_template_details.classroom_id)
    # add new_course to pubsub topic for both course work and roaster changes
    # classroom_crud.enable_notifications(new_course["id"],
    #                                     "COURSE_WORK_CHANGES")
    # classroom_crud.enable_notifications(new_course["id"],
    #                                     "COURSE_ROSTER_CHANGES")
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

    # Get the list of courseworkMaterial
    coursework_material_list = classroom_crud.get_coursework_material(
      course_template_details.classroom_id)
    for coursework_material in coursework_material_list:
      #Check if a coursework material is linked to a topic if yes then
      # replace the old topic id to new topic id using topic_id_map
      if "topicId" in coursework_material.keys():
        coursework_material["topicId"] =topic_id_map[
          coursework_material["topicId"]]
      #Check if a material is present in coursework
      if "materials" in coursework_material.keys():
        # Calling function to get edit_url and view url of
        # google form which returns
        # a dictionary of view_links as keys and edit
        #  likns as values of google form
        url_mapping = classroom_crud.get_edit_url_and_view_url_mapping_of_form()
        # Loop to check if a material in courssework has a google
        # form attached to it
        # update the  view link to edit link and attach it as a form
        for material in coursework_material["materials"]:
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
    if coursework_material_list is not None:
      classroom_crud.create_coursework_material(new_course["id"],
      coursework_material_list)
    # add Instructional designer
    sections_details.teachers.append(
        course_template_details.instructional_designer)
    for teacher_email in sections_details.teachers:
      # classroom_crud.add_teacher(new_course["id"], teacher_email)
      invitation_object = classroom_crud.invite_teacher(new_course["id"],
                            teacher_email)
    # Storing classroom details
      classroom_crud.acceept_invite(invitation_object["id"],teacher_email)
      user_profile = classroom_crud.get_user_profile_information(teacher_email)
      # classroom_crud.add_teacher(new_course["id"], teacher_email)
      # gaid = user_profile["id"]
      # name =  user_profile["name"]["givenName"]
      # last_name =  user_profile["name"]["familyName"]
      # photo_url =  user_profile["photoUrl"]
    # Save the new record of seecion in firestore
      data = {
      "first_name":user_profile["name"]["givenName"],
      "last_name": user_profile["name"]["familyName"],
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
    section.name =course_template_details.name
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
      ResourceNotFound: 404 Section with section id is not found
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
    for i in add_teacher_list:
      # classroom_crud.add_teacher(sections_details.course_id, i)
      invitation_object = classroom_crud.invite_teacher(
                            sections_details.course_id,i)
      # Storing classroom details
      classroom_crud.acceept_invite(invitation_object["id"],i)
      user_profile = classroom_crud.get_user_profile_information(i)
      data = {
      "first_name":user_profile["name"]["givenName"],
      "last_name": user_profile["name"]["familyName"],
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
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.get("{section_id}/enable_notifications",
             response_model=EnableNotificationsResponse)
def section_enable_notifications_pub_sub(section_id:str):
  """Resgister section with a pub/sub topic

  Args:
      section_id (str): unique section id
  Raises:
      InternalServerError: 500 Internal Server Error if something fails
      ResourceNotFound: 404 Section with section id is not found
      CustomHTTPException: raise error according to the HTTPError exception
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
    raise CustomHTTPException(status_code=hte.resp.status,
                              success=False,
                              message=str(hte),
                              data=None) from hte
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
      CustomHTTPException: raise error according to the HTTPError exception
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
    raise CustomHTTPException(status_code=hte.resp.status,
                              success=False,
                              message=str(hte),
                              data=None) from hte
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e
