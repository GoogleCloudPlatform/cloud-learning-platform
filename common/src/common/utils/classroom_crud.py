""" Hepler functions for classroom crud API """
from asyncio.log import logger
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from common.utils.errors import InvalidTokenError,UserManagementServiceError,ResourceNotFoundException
from common.utils.http_exceptions import InternalServerError, CustomHTTPException
from common.utils.logging_handler import Logger

from common.models import Section,CourseEnrollmentMapping

from common.config import CLASSROOM_ADMIN_EMAIL, USER_MANAGEMENT_BASE_URL,PUB_SUB_PROJECT_ID,DATABASE_PREFIX
from common.utils import helper
import requests

SUCCESS_RESPONSE = {"status": "Success"}
FAILED_RESPONSE = {"status": "Failed"}
FEED_TYPE_DICT = {
    "COURSE_WORK_CHANGES": "courseWorkChangesInfo",
    "COURSE_ROSTER_CHANGES": "courseRosterChangesInfo"
}
REGISTER_SCOPES = [
    "https://www.googleapis.com/auth/classroom.push-notifications",
    "https://www.googleapis.com/auth/"+
    "classroom.student-submissions.students.readonly",
    "https://www.googleapis.com/auth/classroom.rosters.readonly"
]
SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses",
    "https://www.googleapis.com/auth/classroom.rosters",
    "https://www.googleapis.com/auth/classroom.topics",
    "https://www.googleapis.com/auth/classroom.coursework.students",
    "https://www.googleapis.com/auth/classroom.coursework.me",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/forms.body.readonly"
]


def get_credentials():
  classroom_key = helper.get_gke_pd_sa_key_from_secret_manager()
  creds = service_account.Credentials.from_service_account_info(classroom_key,
                                                                scopes=SCOPES)
  creds = creds.with_subject(CLASSROOM_ADMIN_EMAIL)

  return creds


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
  new_course["courseState"] = "ACTIVE"
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


def update_course(course_id, section_name, description, course_name=None):
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
    course = service.courses().update(id=course_id, body=course).execute()
    course_name = course.get("name")
    course_id = course.get("id")
    return course
  except HttpError as error:
    logger.error(error)
    raise HttpError from error


def update_course_state(course_id, course_state):
  """Update course state
  Possible states a course can be ACTIVE,ARCHIVED
  PROVISIONED,DECLINED,SUSPENDED
  Args: course_id ,course_state
  Returns:
    new created course details
    """
  service = build("classroom", "v1", credentials=get_credentials())
  course = service.courses().get(id=course_id).execute()
  course["course_state"] = course_state
  course = service.courses().update(id=course_id, body=course).execute()
  course_id = course.get("id")
  return course


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
  topic_id_map = {}
  for topic in topics:
    old_topic_id = topic["topicId"]
    topic_name = topic["name"]
    topic = {"name": topic_name}
    response = service.courses().topics().\
      create(courseId=course_id, body=topic).execute()
    topic_id_map[old_topic_id] = response["topicId"]
  Logger.info(f"Topics created for course_id{course_id}")
  return topic_id_map


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
  """Add teacher in a classroom
  Args:
    course_id(str): Unique classroom id
    teacher_email(str): teacher email which needs to be added
  Return:
    course(dict): returns a dict which contains classroom details
  """

  service = build("classroom", "v1", credentials=get_credentials())
  teacher = {"userId": teacher_email}
  course = service.courses().teachers().create(courseId=course_id,
                                               body=teacher).execute()
  return course


def delete_teacher(course_id, teacher_email):
  """delete teacher in a classroom
  Args:
    course_id(str): Unique classroom id
    teacher_email(str): teacher email which needs to be added
  Return:
    course(dict): returns a dict which contains classroom details
  """

  service = build("classroom", "v1", credentials=get_credentials())
  course = service.courses().teachers().delete(courseId=course_id,
                                               userId=teacher_email).execute()
  return course

def create_student_in_course(access_token,student_email,course_id,course_code):
  """
  Args:
    access_token(str): Oauth access token which contains student credentials
  Return:
    enrolled student object
  """
  service = build("classroom", "v1",\
     credentials=get_oauth_credentials(access_token))
  student = {"userId": student_email}
  result = service.courses().students().create(
      courseId=course_id, body=student, enrollmentCode=course_code).execute()
  return result

def get_person_information (access_token):
  """
  Args:
    access_token(str): Oauth access token which contains
    student credentials
  Return:
    profile: dictionary of users personal information
  """
  people_service = build("people", "v1",\
     credentials=get_oauth_credentials(access_token))
  profile = people_service.people().get(resourceName="people/me",
  personFields="metadata,photos,names").execute()
  return profile

def get_oauth_credentials(access_token):
  """
  Args:
    access_token(str): Oauth access token which contains student credentials
  Return:
    creds: user credential object
  """
  creds = Credentials(token=access_token)
  if not creds or not creds.valid:
    raise InvalidTokenError("Invalid access_token please provide a valid token")
  return creds

def enroll_student(headers ,access_token, course_id,student_email,course_code):
  """Add student to the classroom using student google auth token
  Args:
    headers :Bearer token
    access_token(str): Oauth access token which contains student credentials
    course_id(str): unique classroom id which is required to get the classroom
    student_email(str): student email id
    course_code(str): unique classroom enrollment code
  Raise:
    InvalidTokenError: Raised if the token is expired or not valid
  Return:
    dict: returns a dict which contains student and classroom details
  """
  # Call search by email usermanagement API to get the student data
  response = requests.get(f"\
  {USER_MANAGEMENT_BASE_URL}/user/search?email={student_email}",\
    headers=headers)
  # If the response is success check if student is inactive i.e  raise error
  if response.status_code == 200:
    searched_student = response.json()["data"]
    if searched_student != []:
      if searched_student[0]["status"]=="inactive":
        raise InternalServerError("Student inactive in \
          database is trying to enroll.Please update\
             the student status")

  # Given student is active then call create
  # student in classroom course function
  create_student_in_course(access_token,student_email,course_id,course_code)
  # Get the gaia ID , first name ,last_name of the student
  # Call_people api function
  profile = get_person_information(access_token)
  gaia_id = profile["metadata"]["sources"][0]["id"]
  # first_name=profile["names"][0]["givenName"]
  # last_name =profile["names"][0]["familyName"]
  # Call user API
  data = {
  "first_name":"",
  "last_name": "",
  "email":student_email,
  "user_type": "learner",
  "user_type_ref": "",
  "user_groups": [],
  "status": "active",
  "is_registered": True,
  "failed_login_attempts_count": 0,
  "access_api_docs": False,
  "gaia_id":gaia_id
  }
  # Check if searched user is [] ,i.e student is enrolling for first time
  # then call create user usermanagement API and return user data else
  # return searched user data
  if searched_student == []:
    response = requests.post(f"{USER_MANAGEMENT_BASE_URL}/user",
    json=data,headers=headers)
    if response.status_code != 200:
      raise UserManagementServiceError(response.json()["message"])
    return response.json()["data"]
  else :
    return searched_student[0]

def get_edit_url_and_view_url_mapping_of_form():
  """  Query google drive api and get all the forms a user owns
      return a dictionary of view link as keys and edit link as values
  """
  service = build("drive", "v3", credentials=get_credentials())
  page_token = None
  while True:
    response = service.files().list(
        q="mimeType=\"application/vnd.google-apps.form\"",
        spaces="drive",
        fields="nextPageToken, "
        "files(id, name,webViewLink,thumbnailLink)",
        pageToken=page_token).execute()
    view_link_and_edit_link_matching = {}
    for file in response.get("files", []):
      result = get_view_link_from_id(file.get("id"))
      view_link_and_edit_link_matching[result["responderUri"]] = \
        file.get("webViewLink")
    if page_token is None:
      break
  return view_link_and_edit_link_matching


def get_view_link_from_id(form_id):
  "Query google forms api  using form id and get view url of  google form"

  service = build("forms", "v1", credentials=get_credentials())
  result = service.forms().get(formId=form_id).execute()
  return result


def invite_teacher(course_id, teacher_email):
  """Invite teacher to google classroom using course id and email

  Args:
      course_id (str): google classroom unique id
      teacher_email (str): teacher email id

  Raises:
      CustomHTTPException: custom exception for HTTP exceptions
      InternalServerError: 500 Internal Server Error if something fails

  Returns:
      dict: response from create invitation method
  """
  service = build("classroom", "v1", credentials=get_credentials())
  body = {"courseId": course_id, "role": "TEACHER", "userId": teacher_email}
  try:
    course = service.invitations().create(body=body).execute()
    return course
  except HttpError as ae:
    raise CustomHTTPException(status_code=ae.resp.status,
                              success=False,
                              message=str(ae),
                              data=None) from ae
  except Exception as e:
    raise InternalServerError(str(e)) from e


def enable_notifications(course_id, feed_type):
  """_summary_

  Args:
      course_id (str): _description_
      feed_type (str): _description_

  Raises:
      InternalServerError: 500 Internal Server Error if something fails

  Returns:
      _type_: _description_
  """
  creds =service_account.Credentials.from_service_account_info(
      helper.get_gke_pd_sa_key_from_secret_manager(), scopes=REGISTER_SCOPES)
  creds = creds.with_subject(CLASSROOM_ADMIN_EMAIL)
  service = build("classroom", "v1", credentials=creds)
  body = {
      "feed": {
          "feedType": feed_type,
          FEED_TYPE_DICT.get(feed_type): {
              "courseId": course_id
          }
      },
      "cloudPubsubTopic": {
          "topicName":"projects/"+
          f"{PUB_SUB_PROJECT_ID}/topics/{DATABASE_PREFIX}classroom-messeges"
      }
  }
  return service.registrations().create(body=body).execute()

def list_student_section(section_id,headers):
  """List  student of section given firestore section id

  Args:
      section_id (str): firestore section id
  Returns:
      dict: list of students of section
  """
  section_details = []
  section_details = Section.find_by_id(section_id)
  result = CourseEnrollmentMapping.\
    fetch_all_by_section(section_details.key,"learner")
  users = []
  for record in result:
    user_id =record.user
    response = requests.\
      get(f"{USER_MANAGEMENT_BASE_URL}/user/{user_id}",headers=headers)
    users.append(response.json()["data"])
  return users

def delete_student(course_id, student_email):
  """Delete  student from google classroom using course id and email
  Args:
      course_id (str): google classroom unique id
      teacher_email (str): teacher email id
  Raises:
      CustomHTTPException: custom exception for HTTP exceptions
      InternalServerError: 500 Internal Server Error if something fails
  Returns:
      dict: response from create invitation method
  """
  service = build("classroom", "v1", credentials=get_credentials())
  student = {"userId": student_email}
  try:
    student = service.courses().students().delete(
                courseId=course_id,userId = student_email).execute()
    return student
  except HttpError as ae:
    raise CustomHTTPException(status_code=ae.resp.status,
                              success=False,
                              message=str(ae),
                              data=None) from ae
  except Exception as e:
    raise InternalServerError(str(e)) from e

def get_user_details(user_id, headers):
  """Get user from user collection
  Args:
      user_id (str): user_id from user collection
      headers : Auth headers

  Returns:
      dict: response from user API
  """

  response_get_student = requests.get\
      (f"{USER_MANAGEMENT_BASE_URL}/user/{user_id}",headers=headers)
  if response_get_student.status_code == 404:
    raise \
        ResourceNotFoundException(response_get_student.json()["message"])
  return response_get_student.json()
