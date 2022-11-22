""" Hepler functions for classroom crud API """
from asyncio.log import logger

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from common.utils.logging_handler import Logger
from config import CLASSROOM_ADMIN_EMAIL
from utils import helper

SUCCESS_RESPONSE = {"status": "Success"}
FAILED_RESPONSE = {"status": "Failed"}

SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses",
    "https://www.googleapis.com/auth/classroom.rosters",
    "https://www.googleapis.com/auth/classroom.topics",
    "https://www.googleapis.com/auth/classroom.coursework.students",
    "https://www.googleapis.com/auth/classroom.coursework.me"
]


def get_credentials():
  CLASSROOM_KEY = helper.get_gke_pd_sa_key_from_secret_manager()
  creds = service_account.Credentials.from_service_account_info(CLASSROOM_KEY,
                                                                scopes=SCOPES)
  creds = creds.with_subject(CLASSROOM_ADMIN_EMAIL)


def create_course(name, description, section, owner_id):
  """Create course Function in classroom

  Args: course_name ,description of course, section,owner_id of course
  Returns:
    new created course details
    """ ""

  service = build("classroom", "v1", credentials=get_credentials())
  new_course = {}
  new_course["name"] = name
  new_course["section"] = section
  new_course["description"] = description
  new_course["ownerId"] = owner_id
  course = service.courses().create(body=new_course).execute()
  return course


def get_course_by_id(course_id):
  """Get course by Id function from classroom

    Args: course_id
  Returns:
        course details
    """ ""

  try:
    service = build("classroom", "v1", credentials=get_credentials())
    course = service.courses().get(id=course_id).execute()

    return course

  except HttpError as error:
    logger.error(error)
    return None


def update_course(course_id,
                  section_name,
                  description,
                  course_state,
                  course_name=None):
  """Update course Function in classroom

  Args: section_name ,description of course, section,owner_id of course
  Returns:
    new created course details
    """ ""

  service = build("classroom", "v1", credentials=get_credentials())
  try:
    new_course = {}
    course = service.courses().get(id=course_id).execute()
    if course_name is not None:
      new_course["name"] = course_name
    course["section"] = section_name
    course["description"] = description
    course["course_state"] = course_state
    course = service.courses().update(id=course_id, body=course).execute()
    course_name = course.get("name")
    course_id = course.get("id")
    return course
  except HttpError as error:
    logger.error(error)
    raise HttpError from error


def get_course_list():
  """Get courses list from classroom

  Args:
  Returns:
    list of courses in classroom
    """ ""

  service = build("classroom", "v1", credentials=get_credentials())
  results = service.courses().list().execute()
  courses = results.get("courses", [])
  return courses


def get_topics(course_id):
  """Get  list of topics from classroom

  Args:course_id
  Returns:
    returns list of topics of given course in classroom
    """ ""

  service = build("classroom", "v1", credentials=get_credentials())
  try:
    topics = []
    page_token = None
    while True:
      response = service.courses().topics().list(pageToken=page_token,
                                                 courseId=course_id).execute()
      topics = topics.extend(response.get("topic", []))
      page_token = response.get("nextPageToken", None)
      if not page_token:
        break
    if response:
      topics = response["topic"]
      return topics
  except HttpError as error:
    logger.error(error)
    return None


def create_topics(course_id, topics):
  """create topic in course

  Args:
  course_id: where topics need to be created
  topics : list of dictionary of topics to be created
  Returns:
    returns success
    """ ""

  service = build("classroom", "v1", credentials=get_credentials())
  for topic in topics:
    topic_name = topic["name"]
    topic = {"name": topic_name}
    service.courses().topics().create(courseId=course_id, body=topic).execute()
  Logger.info(f"Topics created for course_id{course_id}")
  return "success"


def get_coursework(course_id):
  """Get  list of coursework from classroom

  Args: course_id
  Returns:
    returns list of coursework of given course in classroom
    """ ""

  service = build("classroom", "v1", credentials=get_credentials())
  try:
    coursework_list = service.courses().courseWork().list(
        courseId=course_id).execute()
    if coursework_list:
      coursework_list = coursework_list["courseWork"]
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
    """ ""

  service = build("classroom", "v1", credentials=get_credentials())
  for coursework_item in coursework_list:
    _ = service.courses().courseWork().create(courseId=course_id,
                                              body=coursework_item).execute()
  Logger.info("Create coursework method worked")
  return "success"


def delete_course_by_id(course_id):
  """Delete a course from classroom

  Args: course_id
  Returns:
    []
    """ ""

  service = build("classroom", "v1", credentials=get_credentials())
  course = service.courses().delete(id=course_id).execute()
  return course


def get_course_work_list(course_id):
  """Returns an array of objects containing all the coursework details of a
    course

    Args:
      course_id: unique id of the course for which the coursework needs to
        be fetched
    Returns:
      returns success
      """ ""

  service = build("classroom", "v1", credentials=get_credentials())

  coursework_list = service.courses().courseWork().list(
      courseId=course_id).execute()
  if coursework_list:
    coursework_list = coursework_list["courseWork"]
  return coursework_list


def get_submitted_course_work_list(course_id, student_email):
  """Returns an array of objects containing all the coursework of a course
    assigned to the student with the status if else the coursework has
    been submitted by the student or not

    Args:
      course_id: unique id of the course for which the coursework needs to
        be fetched
      student_email : email id of the student for which the coursework needs
        to be fetched
    Returns:
      returns success
      """ ""

  service = build("classroom", "v1", credentials=get_credentials())

  submitted_course_work_list = service.courses().courseWork(
  ).studentSubmissions().list(courseId=course_id,
                              courseWorkId="-",
                              userId=student_email).execute()
  if submitted_course_work_list:
    submitted_course_work_list = submitted_course_work_list[
        "studentSubmissions"]
  return submitted_course_work_list


def add_teacher(course_id, teacher_email):
  service = build("classroom", "v1", credentials=get_credentials())
  teacher = {"userId": teacher_email}
  course = service.courses().teachers().create(courseId=course_id,
                                               body=teacher).execute()
  return course
