""" User endpoints """
import datetime
from re import I
from fastapi import APIRouter, HTTPException
from common.utils.logging_handler import Logger
from fastapi.encoders import jsonable_encoder
from google.api_core.exceptions import PermissionDenied
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from schemas.user import Topic
from schemas.course_details import CourseDetails
from services import classroom_crud
import traceback
import os
from config import CLASSROOM_ADMIN_EMAIL
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

    # SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly',
    # 'https://www.googleapis.com/auth/classroom.rosters']

    # a_creds = service_account.Credentials.from_service_account_file(
    # 'utils/service.json', scopes=SCOPES)
    # creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
    # service = build('classroom', 'v1', credentials=creds)

    #     # Call the Classroom API
    # results = service.courses().list().execute()
    # courses = results.get('courses', [])
    # print("------This is result-----------")
    # course_details = list(courses)    
    course_list = classroom_crud.get_course_list()
    return list(course_list)

  except Exception as e:
    Logger.error(e)
    print(e)
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
    new_course = classroom_crud.create_course(current_course["name"],current_course["section"],current_course["ownerId"]) 
    print("New course is created",new_course)
    print("---------------------------------------------------------2")
    # Get topics of current course
    topics = classroom_crud.get_topics(course_id)
    print("------------------Topics----------",topics)
    if topics is not None:
      classroom_crud.create_topics(new_course["id"],topics)
    print("-------------topic create---------------------------3")
    # Get coursework of current course and create a new course
    coursework_list  = classroom_crud.get_coursework(course_id)
    if coursework_list is not None:
      classroom_crud.create_coursework(new_course["id"],coursework_list)
    print("-----------coursework created-----------------------------4")

    SUCCESS_RESPONSE["new_course"] = new_course
    return SUCCESS_RESPONSE
  except Exception as e:
    Logger.error(e)
    print(e)
    raise HTTPException(status_code=500,data =e) from e

