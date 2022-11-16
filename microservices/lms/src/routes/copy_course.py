""" User endpoints """
from re import I
from fastapi import APIRouter, HTTPException,status, Response
from common.utils.logging_handler import Logger
from fastapi.encoders import jsonable_encoder
from google.api_core.exceptions import PermissionDenied
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from schemas.course_details import CourseDetails
from schemas.section import SectionDetails
from schemas.update_section import UpdateSection
from services import classroom_crud
from common.models.section import Section
from common.models.course_template import CourseTemplate
from common.models.cohort import Cohort
import traceback
import os.path
import os
import datetime
from common.utils.http_exceptions import ResourceNotFound, InternalServerError

# disabling for linting to pass
# pylint: disable = broad-except

router = APIRouter(prefix="/course", tags=["Course"])

SUCCESS_RESPONSE = {"status": "Success"}
FAILED_RESPONSE = {"status": "Failed"}


@router.get("/get_courses/")
def get_courses():
  """Get courses list

  Args:
    course_id (Course): Course_id of a course that needs to copied

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    List of courses in classroom ,
    {'status': 'Failed'} if the user creation raises an exception
  """
  try: 
    course_list = classroom_crud.get_course_list()
    SUCCESS_RESPONSE["result"]= list(course_list)
    return SUCCESS_RESPONSE
  except Exception as e:
    Logger.error(e)
    err = traceback.format_exc().replace("\n", " ")
    print(err)
    raise HTTPException(status_code=500) from e



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
    course_id = input_course_details_dict['course_id']
    # Get course by course id
    current_course =  classroom_crud.get_course_by_id(course_id)
    if current_course is None:
      return "No course found "
    # Create a new course
    new_course = classroom_crud.create_course(current_course["name"],current_course["description"],current_course["section"],current_course["ownerId"]) 
    # Get topics of current course
    topics = classroom_crud.get_topics(course_id)
    if topics is not None:
      classroom_crud.create_topics(new_course["id"],topics)
    # Get coursework of current course and create a new course
    coursework_list  = classroom_crud.get_coursework(course_id)
    if coursework_list is not None:
      classroom_crud.create_coursework(new_course["id"],coursework_list)

    SUCCESS_RESPONSE["new_course"] = new_course
    return SUCCESS_RESPONSE
  except Exception as e:
    Logger.error(e)
    print(e)
    raise HTTPException(status_code=500,data =e) from e

@router.post("/create_section/")
def create_section(sections_details: SectionDetails,response:Response):
  """Create section API

  Args:
    name (section): Section name
    description (str):Description
    classroom_template_id(str)
    cohort_id
    teachers_list
  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    {"status":"Success","new_course":{}}: Returns new course details,
    {'status': 'Failed'} if the user creation raises an exception
  """
  try:
    input_sections_details_dict = {**sections_details.dict()}
    section_name = input_sections_details_dict['name']
    description = input_sections_details_dict['description']
    teachers_list = input_sections_details_dict['teachers_list']
    course_template_id = input_sections_details_dict['course_template']
    cohort_id = input_sections_details_dict['cohort']
    print(1)
    print(course_template_id)
    course_template_details = CourseTemplate.find_by_uuid(course_template_id)
    if course_template_details == None:
      raise ResourceNotFound(
                f'Course Template with uuid {course_template_id} is not found')
    print("course_template",course_template_details)
    cohort_details = Cohort.find_by_uuid(cohort_id)
    print(2)
    if cohort_details == None:
      print(3)
      raise ResourceNotFound(
                f'cohort with uuid {cohort_id} is not found')
    
    name = course_template_details.name
    # Get course by course id for copying from master course
    print("This is classroom Id ",course_template_details.classroom_id)
    current_course =  classroom_crud.get_course_by_id(course_template_details.classroom_id)
    print("*1")
    if current_course is None:
      raise ResourceNotFound(
                f'classroom  with uuid {course_template_details.classroom_id} is not found')
    # Create a new course
    print("*2")
    new_course = classroom_crud.create_course(name,description,section_name,"me") 
    # Get topics of current course
    topics = classroom_crud.get_topics(course_template_details.classroom_id)
    print("*3")
    if topics is not None:
      classroom_crud.create_topics(new_course["id"],topics)
    # Get coursework of current course and create a new course
    coursework_list  = classroom_crud.get_coursework(course_template_details.classroom_id)
    if coursework_list is not None:
      classroom_crud.create_coursework(new_course["id"],coursework_list)
     
    # Save the new record of seecion in firestore
    section = Section()
    section.name = name
    section.section = section_name
    section.description=description
    # Reference document can be get using get() method   
    section.course_template = course_template_details
    section.cohort=cohort_details
    section.classroom_id=new_course["id"]
    section.classroom_code=new_course["enrollmentCode"]
    section.teachers_list=teachers_list
    section.created_timestamp=datetime.datetime.now()
    section.uuid = section.save().id
    print(section.id)
    section.save()
    SUCCESS_RESPONSE["new_course"] = new_course
    return SUCCESS_RESPONSE
  except ResourceNotFound as err :
    Logger.error(err)
    raise  ResourceNotFound(str(err)) from err
  except Exception as e:
    Logger.error(e)
    print(e)
    raise InternalServerError(str(e)) from e

@router.get("/list_section/")
def list_section(cohort_id:str):
  """Create section API

  Args:
    name (section): Section name
    description (str):Description
    classroom_template_id(str)
    cohort_id
    teachers_list
  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    {"status":"Success","new_course":{}}: Returns new course details,
    {'status': 'Failed'} if the user creation raises an exception
  """
  try:

    # Get cohort Id and create a reference of cohort object

    # cohort=Cohort.collection.filter("uuid","==",cohort_id).get()
    cohort=Cohort.find_by_uuid(cohort_id)
    if cohort == None:
      raise ResourceNotFound(
                f'Cohort with uuid {cohort_id} is not found')
    # Using the cohort object reference key query sections model to get a list 
    # of section of a perticular cohort
    result = Section.collection.filter("cohort","==",cohort.key).fetch()
    print("Result of sections filter",result)
    sections_list = list(map(lambda x: x.to_dict(),result))
    
    SUCCESS_RESPONSE["data"] = sections_list
    return SUCCESS_RESPONSE
  except ResourceNotFound as err :
    Logger.error(err)
    print(err)
    raise  ResourceNotFound(str(err)) from err
  except Exception as e:
    Logger.error(e)
    print(e)
    raise HTTPException(status_code=500,data =e) from e


@router.get("/get_section/")
def get_section(section_id:str):
  """Create section API

  Args:
    section_id (str): section_id in firestore
   
  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    {"status":"Success","new_course":{}}: Returns new course details,
    {'status': 'Failed'} if the user creation raises an exception
  """
  try:
    section_details=[]
    section_details = Section.find_by_uuid(section_id)
    if section_details == None:
      raise ResourceNotFound(
                f'Section with uuid {section_id} is not found')
    # Get course by course id
    # print ("RESULT OF COHORT DETAILS ......",cohort_details)
    SUCCESS_RESPONSE["section_details"] = section_details
    return SUCCESS_RESPONSE
  except ResourceNotFound as err :
    Logger.error(err)
    print(err)
    raise  ResourceNotFound(str(err)) from err
  except Exception as e:
    Logger.error(e)
    print(e)
    raise HTTPException(status_code=500,data =e) from e

@router.post("/update_section/")
def update_section(sections_details: UpdateSection):
  """Create section API

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
    {"status":"Success","data":{}}: Returns new course details,
    {'status': 'Failed'} if the user creation raises an exception
  """
  try:

    input_sections_details_dict = {**sections_details.dict()}
    section_name = input_sections_details_dict["section_name"]
    uuid = input_sections_details_dict["uuid"]
    description = input_sections_details_dict["description"]
    course_id = input_sections_details_dict["course_id"]
    course_state= input_sections_details_dict["course_state"]
    section = Section.find_by_uuid(uuid)
    if section == None:
      raise ResourceNotFound(
                f'Section with uuid {uuid} is not found')
    
    new_course = classroom_crud.update_course(course_id,section_name,description,course_state) 
    if new_course == None:
      raise ResourceNotFound(
                f'Course with Course_id {course_id} is not found in classroom')
    section.section = section_name
    section.description=description
    section.last_updated_timestamp=datetime.datetime.now()
    section.save()
    SUCCESS_RESPONSE["data"] = new_course
    return SUCCESS_RESPONSE
  except ResourceNotFound as err :
    Logger.error(err)
    print(err)
    raise  ResourceNotFound(str(err)) from err
  except Exception as e:
    Logger.error(e)
    print(e)
    raise HTTPException(status_code=500,data =e) from e

