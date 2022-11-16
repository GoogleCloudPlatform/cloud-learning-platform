""" Hepler functions for classroom crud API """
from asyncio.log import logger
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
import traceback
import json
from google.protobuf.json_format import MessageToDict
from config import CLASSROOM_ADMIN_EMAIL,PROJECT_ID
# from google_auth_oauthlib.flow import Flow
from utils import helper

# disabling for linting to pass
# pylint: disable = broad-except



SUCCESS_RESPONSE = {"status": "Success"}
FAILED_RESPONSE = {"status": "Failed"}


def create_course(name,description,section,owner_id):
    """Create course Function in classroom

  Args: course_name ,description of course, section,owner_id of course
  Returns:
    new created course details
    """""
    SCOPES = ["https://www.googleapis.com/auth/classroom.courses",
    "https://www.googleapis.com/auth/classroom.courses.readonly"]
    CLASSROOM_KEY = helper.get_gke_pd_sa_key_from_secret_manager()
    a_creds = service_account.Credentials.from_service_account_info(CLASSROOM_KEY,scopes=SCOPES)
    CLASSROOM_ADMIN_EMAIL=="lms_service@dhodun.altostrat.com"
    creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)

    service = build("classroom", "v1", credentials=creds)
    new_course = {}
    new_course["name"]=name
    new_course["section"]=section
    new_course["description"]=description
    # new_course["room"]=course["room"]
    new_course["ownerId"]=owner_id
    # new_course["descriptionHeading"]=course["description_heading"]
    course = service.courses().create(body=new_course).execute()
    course_name = course.get("name")
    course_id = course.get("id")
    return course

def get_course_by_id(course_id):
    """Get course by Id function from classroom

    Args: course_id
  Returns:
        course details
    """""
    SCOPES = ["https://www.googleapis.com/auth/classroom.courses",
    "https://www.googleapis.com/auth/classroom.courses.readonly"]
    CLASSROOM_KEY = helper.get_gke_pd_sa_key_from_secret_manager()

    a_creds = service_account.Credentials.from_service_account_info(CLASSROOM_KEY,scopes=SCOPES)
    CLASSROOM_ADMIN_EMAIL="lms_service@dhodun.altostrat.com"
    print("Classroom Admin Email",CLASSROOM_ADMIN_EMAIL)
    creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
    try:
        print(course_id,len(course_id),type(course_id))
        service = build("classroom", "v1", credentials=creds)
        course = service.courses().get(id=course_id).execute()
        print("Course get method worked ...")
        print(course)
        return course

    except HttpError as error:
        logger.error(error)
        return None

def update_course(course_id,section_name,description,course_state,course_name=None):
    """Update course Function in classroom

  Args: section_name ,description of course, section,owner_id of course
  Returns:
    new created course details
    """""

    SCOPES = ["https://www.googleapis.com/auth/classroom.courses",
    "https://www.googleapis.com/auth/classroom.courses.readonly"]
    CLASSROOM_KEY = helper.get_gke_pd_sa_key_from_secret_manager()
    a_creds = service_account.Credentials.from_service_account_info(CLASSROOM_KEY,scopes=SCOPES)
    CLASSROOM_ADMIN_EMAIL="lms_service@dhodun.altostrat.com"
    creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
    service = build("classroom", "v1", credentials=creds)
    try:
      new_course = {}
      course = service.courses().get(id=course_id).execute()
      if course_name is not None:
        new_course["name"]=course_name
      course["section"]=section_name
      course["description"]=description
      course["course_state"]=course_state
      course = service.courses().update(id=course_id,body=course).execute()
      course_name = course.get("name")
      course_id = course.get("id")
      return course
    except HttpError as error:
        logger.error(error)
        print("________HTTP---------",HttpError.status_code)
        if HttpError.status_code == 404:
          return None
        else:
          raise HttpError


def get_course_list():    

    """Get courses list from classroom

  Args: 
  Returns:
    list of courses in classroom
    """""


    SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.rosters']
    CLASSROOM_KEY = helper.get_gke_pd_sa_key_from_secret_manager()
    a_creds = service_account.Credentials.from_service_account_info(CLASSROOM_KEY,scopes=SCOPES)
    creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
    service = build("classroom", "v1", credentials=creds)
    results = service.courses().list().execute()
    courses = results.get('courses', [])
    return courses

def get_topics(course_id):
    """Get  list of topics from classroom

  Args: course_id
  Returns:
    returns list of topics of given course in classroom
    """""
    SCOPES = ['https://www.googleapis.com/auth/classroom.topics',
  'https://www.googleapis.com/auth/classroom.topics.readonly']
    
    CLASSROOM_KEY = helper.get_gke_pd_sa_key_from_secret_manager()
    a_creds = service_account.Credentials.from_service_account_info(CLASSROOM_KEY,scopes=SCOPES)
    CLASSROOM_ADMIN_EMAIL="lms_service@dhodun.altostrat.com"
    creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
    service = build("classroom", "v1", credentials=creds)
    try:
      topics = []
      page_token = None
      while True:
          response = service.courses().topics().list(
          pageToken=page_token,
          courseId=course_id).execute()
          topics = topics.extend(response.get('topic', []))
          page_token = response.get('nextPageToken', None)
          if not page_token:
              break
      if response:
          topics = response["topic"] 
          print("Topic method worked ")
          return topics
    except HttpError as error:
        logger.error(error)
        return None


def create_topics(course_id , topics):
    """create topic in course

  Args: 
  course_id: where topics need to be created
  topics : list of dictionary of topics to be created
  Returns:
    returns success
    """""
    SCOPES = ['https://www.googleapis.com/auth/classroom.topics',
  'https://www.googleapis.com/auth/classroom.topics.readonly']

    CLASSROOM_KEY = helper.get_gke_pd_sa_key_from_secret_manager()
    a_creds = service_account.Credentials.from_service_account_info(CLASSROOM_KEY,scopes=SCOPES)
    CLASSROOM_ADMIN_EMAIL="lms_service@dhodun.altostrat.com"
    creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
    service = build("classroom", "v1", credentials=creds)
    print("This is before create topic")
    for topic in topics:
        topic_name = topic["name"]
        topic = {
        "name": topic_name}
        response = service.courses().topics().create(
        courseId=course_id,
        body=topic).execute()
    print("This is create topic method worked")
    return "success"

def get_coursework(course_id):
    """Get  list of coursework from classroom

  Args: course_id
  Returns:
    returns list of coursework of given course in classroom
    """""
    SCOPES = ['https://www.googleapis.com/auth/classroom.coursework.students',
    'https://www.googleapis.com/auth/classroom.coursework.students.readonly']
    CLASSROOM_KEY = helper.get_gke_pd_sa_key_from_secret_manager()
    CLASSROOM_ADMIN_EMAIL="lms_service@dhodun.altostrat.com"
    a_creds = service_account.Credentials.from_service_account_info(CLASSROOM_KEY,scopes=SCOPES)
    creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
    print("In coursework list method........")
    service = build("classroom", "v1", credentials=creds)
    try:
      coursework_list = service.courses().courseWork().list(courseId=course_id).execute()
      if coursework_list:
          coursework_list = coursework_list['courseWork']
          print("Coursework Method worked")
      return coursework_list
    except HttpError as error:
        logger.error(error)
        return None

def create_coursework(course_id, coursework_list):
    """create coursework in a classroom course

  Args: 
  course_id: where coursework need to be created
  coursework : list of dictionary of coursework to be created
  Returns:
    returns success
    """""
    SCOPES = ['https://www.googleapis.com/auth/classroom.coursework.students',
    'https://www.googleapis.com/auth/classroom.coursework.students.readonly']
    CLASSROOM_KEY = helper.get_gke_pd_sa_key_from_secret_manager()
    a_creds = service_account.Credentials.from_service_account_info(CLASSROOM_KEY,scopes=SCOPES)
    CLASSROOM_ADMIN_EMAIL="lms_service@dhodun.altostrat.com"
    creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
    service = build("classroom", "v1", credentials=creds)
    for coursework_item  in coursework_list:
        coursework = service.courses().courseWork().create(courseId=course_id, body=coursework_item).execute()
    print("Create coursework method worked")
    return "success"

def delete_course_by_id(course_id):
    """Delete a course from classroom

  Args: course_id
  Returns:
    []
    """""
    SCOPES = ["https://www.googleapis.com/auth/classroom.courses",
    "https://www.googleapis.com/auth/classroom.courses.readonly"]
    CLASSROOM_KEY = helper.get_gke_pd_sa_key_from_secret_manager()
    a_creds = service_account.Credentials.from_service_account_info(CLASSROOM_KEY,scopes=SCOPES)
    creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
    service = build("classroom", "v1", credentials=creds)
    course = service.courses().delete(id=course_id).execute()
    return course

def add_teacher(course_id,teacher_email):
  SCOPES = ['https://www.googleapis.com/auth/classroom.rosters']
  CLASSROOM_KEY = helper.get_gke_pd_sa_key_from_secret_manager()
  a_creds = service_account.Credentials.from_service_account_info(
      CLASSROOM_KEY, scopes=SCOPES)
  CLASSROOM_ADMIN_EMAIL="lms_service@dhodun.altostrat.com"
  creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
  service = build("classroom", "v1", credentials=creds)
  teacher = {"userId": teacher_email}
  print("In ADD teacher",course_id)
  course = service.courses().teachers().create(
      courseId=course_id, body=teacher).execute()
  return course

