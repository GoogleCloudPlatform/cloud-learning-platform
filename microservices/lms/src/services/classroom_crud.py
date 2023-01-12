""" Hepler functions for classroom crud API """
from asyncio.log import logger
from google.oauth2 import service_account
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from common.utils.errors import InvalidTokenError,UserManagementServiceError
from common.utils.http_exceptions import InternalServerError, CustomHTTPException
from common.utils.logging_handler import Logger
from config import CLASSROOM_ADMIN_EMAIL,USER_MANAGEMENT_BASE_URL
from utils import helper
import requests

SUCCESS_RESPONSE = {"status": "Success"}
FAILED_RESPONSE = {"status": "Failed"}

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

  creds = google.oauth2.credentials.Credentials(token=access_token)
  if not creds or not creds.valid:
    raise InvalidTokenError("Invalid access_token please provide a valid token")
  service = build("classroom", "v1", credentials=creds)
  student = {"userId": student_email}
  service.courses().students().create(
      courseId=course_id, body=student, enrollmentCode=course_code).execute()
  # Get the gaia ID of the course
  people_service = build("people", "v1", credentials=creds)
  profile = people_service.people().get(resourceName="people/me",
  personFields="metadata").execute()
  gaia_id = profile["metadata"]["sources"][0]["id"]
# Call user API
  data = {
  "first_name": "",
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
  response = requests.post(f"{USER_MANAGEMENT_BASE_URL}/user",
  json=data,headers=headers)
  if response.status_code != 200:
    raise UserManagementServiceError(response.json()["message"])
  return response.json()["data"]

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
