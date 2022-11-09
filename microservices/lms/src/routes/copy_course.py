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
from google.oauth2.credentials import Credentials
from schemas.course_details import CourseDetails
from services import classroom_crud
import traceback
import os
# from config import CLASSROOM_KEY
import argparse
import requests
import os.path
import os
import google.auth
from config import CLASSROOM_ADMIN_EMAIL,PROJECT_ID
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

@router.post("/create_course/")
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
    result = classroom_crud.create_course("Maths_test1","a","me")
    SUCCESS_RESPONSE["result"]= result
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
    new_course = classroom_crud.create_course(current_course["name"],current_course["section"],current_course["ownerId"]) 
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



@router.post("/get_data_metadata_server_d/")
def get_data_metadata_server():
  try:
    SCOPES = [
      'https://www.googleapis.com/auth/classroom.courses.readonly',
      'https://www.googleapis.com/auth/classroom.rosters',
      'https://www.googleapis.com/auth/classroom.courses'
  ]

    creds = google.auth.default(scopes=SCOPES)
    service = build("classroom", "v1", credentials=creds)
    results = service.courses().list().execute()
    courses = results.get('courses', [])
    print(courses)
    return "success"
  except Exception as e:
    Logger.error(e)
    err = traceback.format_exc().replace("\n", " ")
    print(err)
    raise HTTPException(status_code=500,data =e) from e


@router.post("/get_data_metadata_server_s/")
def get_data_metadata_server():
  try:

    METADATA_URL = 'http://metadata.google.internal/computeMetadata/v1/'
    METADATA_HEADERS = {'Metadata-Flavor': 'Google'}
    SERVICE_ACCOUNT = 'default'
    url = '{}instance/service-accounts/{}/token'.format(
        METADATA_URL, SERVICE_ACCOUNT)
    # Request an access token from the metadata server.
    r = requests.get(url, headers=METADATA_HEADERS)
    r.raise_for_status() 
    # Extract the access token from the response.
    access_token = r.json()['access_token']
    print(access_token)
    class_url = "https://classroom.googleapis.com/v1/courses"

    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.rosters',
    'https://www.googleapis.com/auth/classroom.rosters']
    creds = Credentials(access_token,scopes =SCOPES)

    service = build("classroom", "v1", credentials=creds)
    results = service.courses().list().execute()
    courses = results.get('courses', [])
    return courses
  except Exception as e:
    Logger.error(e)
    err = traceback.format_exc().replace("\n", " ")
    print(err)
    raise HTTPException(status_code=500,data =e) from e

