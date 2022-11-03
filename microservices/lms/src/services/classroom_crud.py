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
from schemas.user import Topic
import traceback
from google.protobuf.json_format import MessageToDict
from config import CLASSROOM_ADMIN_EMAIL
# disabling for linting to pass
# pylint: disable = broad-except



SUCCESS_RESPONSE = {"status": "Success"}
FAILED_RESPONSE = {"status": "Failed"}


def create_course(name,section,owner_id):
    SCOPES = ["https://www.googleapis.com/auth/classroom.courses",
    "https://www.googleapis.com/auth/classroom.courses.readonly"]

    a_creds = service_account.Credentials.from_service_account_file(
    "utils/service.json", scopes=SCOPES)
    creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
    service = build("classroom", "v1", credentials=creds)
    print("******In create course function")
    new_course = {}
    new_course["name"]=name
    new_course["section"]=section
    # new_course["description"]=course["description"]
    # new_course["room"]=course["room"]
    new_course["ownerId"]=owner_id
    # new_course["descriptionHeading"]=course["description_heading"]

    course = service.courses().create(body=new_course).execute()
    course_name = course.get("name")
    course_id = course.get("id")
    print(f"Course created: {course_name} ,{course_id}")
    return course
    
def get_course_by_id(course_id):
    SCOPES = ["https://www.googleapis.com/auth/classroom.courses",
    "https://www.googleapis.com/auth/classroom.courses.readonly"]
    a_creds = service_account.Credentials.from_service_account_file(
    "utils/service.json", scopes=SCOPES)
    creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
    try:
        service = build("classroom", "v1", credentials=creds)
        course = service.courses().get(id=course_id).execute()
        return course

    except HttpError as error:
        logger.error(error)
        return None

def get_course_list():    
    SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.rosters']
    a_creds = service_account.Credentials.from_service_account_file(
    "utils/service.json", scopes=SCOPES)
    creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
    service = build("classroom", "v1", credentials=creds)
    results = service.courses().list().execute()
    courses = results.get('courses', [])
    return courses

def get_topics(course_id):
    print(" GET TOPICS of old course")
    SCOPES = ['https://www.googleapis.com/auth/classroom.topics',
  'https://www.googleapis.com/auth/classroom.topics.readonly']
    a_creds = service_account.Credentials.from_service_account_file(
    "utils/service.json", scopes=SCOPES)
    creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
    service = build("classroom", "v1", credentials=creds)
    topics = []
    page_token = None
    while True:
        response = service.courses().topics().list(
        pageToken=page_token,
        courseId=course_id).execute()
        print("response topics",response)
        topics = topics.extend(response.get('topic', []))
        page_token = response.get('nextPageToken', None)
        if not page_token:
            break
    if response:
        topics = response["topic"] 
        return topics
    

def create_topics(course_id , topics):
 
    SCOPES = ['https://www.googleapis.com/auth/classroom.topics',
  'https://www.googleapis.com/auth/classroom.topics.readonly']
    a_creds = service_account.Credentials.from_service_account_file(
    "utils/service.json", scopes=SCOPES)
    creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
    service = build("classroom", "v1", credentials=creds)
    print("Inside create topic function")
    for topic in topics:
        topic_name = topic["name"]
        topic = {
        "name": topic_name}
        response = service.courses().topics().create(
        courseId=course_id,
        body=topic).execute()
    print('Topic created: ', response['name'])
    return "success"

def get_coursework(course_id):
    SCOPES = ['https://www.googleapis.com/auth/classroom.coursework.students',
    'https://www.googleapis.com/auth/classroom.coursework.students.readonly']
    print("Inside get courseWork Api")
    a_creds = service_account.Credentials.from_service_account_file(
    "utils/service.json", scopes=SCOPES)
    creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
    service = build("classroom", "v1", credentials=creds)
    coursework_list = service.courses().courseWork().list(courseId=course_id).execute()
    print(coursework_list)
    if coursework_list:
        coursework_list = coursework_list['courseWork']
    return coursework_list

def create_coursework(course_id, coursework_list):
    SCOPES = ['https://www.googleapis.com/auth/classroom.coursework.students',
    'https://www.googleapis.com/auth/classroom.coursework.students.readonly']
    print("Inside create coursework func")
    a_creds = service_account.Credentials.from_service_account_file(
    "utils/service.json", scopes=SCOPES)
    creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
    service = build("classroom", "v1", credentials=creds)
    for coursework_item  in coursework_list:
        print("--------------------------------------------")
        print("In for loop 1",coursework_item)
        print(type(coursework_item))
        # coursework_item['courseId'] = new_course_id
        # coursework_item.pop("id")
        coursework = service.courses().courseWork().create(courseId=course_id, body=coursework_item).execute()
    print("In for loop 2")
    
def delete_course_by_id(course_id):
    SCOPES = ["https://www.googleapis.com/auth/classroom.courses",
    "https://www.googleapis.com/auth/classroom.courses.readonly"]
    a_creds = service_account.Credentials.from_service_account_file(
    "utils/service.json", scopes=SCOPES)
    creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
    service = build("classroom", "v1", credentials=creds)
    course = service.courses().delete(id=course_id).execute()
    course_name = course.get("name")
    print(f"Course Found: {course_name}")
    return course

