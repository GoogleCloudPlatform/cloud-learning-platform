""" Helper functions for classroom crud API """
import requests
from asyncio.log import logger
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from common.utils.jwt_creds import JwtCredentials
from common.utils.errors import InvalidTokenError, UserManagementServiceError, ResourceNotFoundException
from common.utils.http_exceptions import InternalServerError
from common.utils.logging_handler import Logger
from common.models import Section

from common.config import CLASSROOM_ADMIN_EMAIL, USER_MANAGEMENT_BASE_URL, PUB_SUB_PROJECT_ID, DATABASE_PREFIX
# pylint: disable=line-too-long

SUCCESS_RESPONSE = {"status": "Success"}
FAILED_RESPONSE = {"status": "Failed"}
FEED_TYPE_DICT = {
    "COURSE_WORK_CHANGES": "courseWorkChangesInfo",
    "COURSE_ROSTER_CHANGES": "courseRosterChangesInfo"
}

SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses",
    "https://www.googleapis.com/auth/classroom.rosters",
    "https://www.googleapis.com/auth/classroom.topics",
    "https://www.googleapis.com/auth/classroom.coursework.students",
    "https://www.googleapis.com/auth/classroom.coursework.me",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/forms.body.readonly",
    "https://www.googleapis.com/auth/classroom.profile.photos",
    "https://www.googleapis.com/auth/classroom.courseworkmaterials",
    "https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly",
    "https://www.googleapis.com/auth/classroom.push-notifications",
    "https://www.googleapis.com/auth/classroom.student-submissions."+
    "students.readonly",
    "https://www.googleapis.com/auth/classroom.rosters.readonly"
]

def get_default_service_account_email():
  metadata_url = "http://metadata.google.internal/computeMetadata/v1/"
  metadata_headers = {"Metadata-Flavor": "Google"}
  url = f"{metadata_url}instance/service-accounts"
  r = requests.get(url, headers=metadata_headers)
  service_account_email = r.text.split("/")[1].strip()
  return service_account_email

def get_credentials(email=CLASSROOM_ADMIN_EMAIL):
  google_oauth_token_endpoint = "https://oauth2.googleapis.com/token"
  service_account_email = get_default_service_account_email()
  creds = JwtCredentials.from_default_with_subject(
    subject=email,
    service_account_email=service_account_email,
    token_uri=google_oauth_token_endpoint,
    scopes=SCOPES)
  return creds

def create_course(name, description, section, owner_id):
  """Create course Function in classroom

  Args: course_name, description of course, section, owner_id of course
  Returns:
    new created course details
  """

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
  """

  try:
    service = build("classroom", "v1", credentials=get_credentials())
    course = service.courses().get(id=course_id).execute()

    return course

  except HttpError as error:
    logger.error(error)
    return None


def drive_copy(file_id, target_folder_id, name):
  """copy the file in the target_folder 
  Args: 
  file_id : (str) google drive file _id
  target_folder_id:(str) folder_id of destination folder
  name:(str) file name of the copied file
  Returns:
    new created file details dictionary with name,mimeType,WebViewLink
    id of file 
  """

  copied_file = {"name": name, "parents": [target_folder_id]}
  service = build("drive", "v3", credentials=get_credentials())
  form_copy = service.files().copy(fileId=file_id,
                                   fields="webViewLink,name,mimeType,id",
                                   body=copied_file).execute()
  return form_copy


def copy_material(drive_file_dict, target_folder_id):
  """copy the file in the target_folder 
  Args: 
  drive_file_dict : (str) drive file details dictionary given by get
      coursework API 
  target_folder_id:(str) folder_id of destination folder 
  Returns:
    new created drive_file_dict with new copied file id in target folder 
  """
  file_id = drive_file_dict["driveFile"]["driveFile"]["id"]
  if "title" not in drive_file_dict["driveFile"]["driveFile"].keys():
    raise ResourceNotFoundException(f"File with id {file_id} not found")
  name = drive_file_dict["driveFile"]["driveFile"]["title"]
  result = drive_copy(file_id=file_id,
                      target_folder_id=target_folder_id,
                      name=name)
  new_id = result["id"]
  drive_file_dict["driveFile"]["driveFile"]["id"] = new_id
  drive_file_dict["driveFile"]["driveFile"].pop("alternateLink")
  if "thumbnaiUrl" in drive_file_dict["driveFile"]["driveFile"].keys():
    drive_file_dict["driveFile"]["driveFile"].pop("thumbnailUrl")
  return drive_file_dict


def update_course(course_id, section_name, description, course_name=None):
  """Update course Function in classroom

  Args: section_name, description of course, section, owner_id of course
  Returns:
    new created course details
  """

  service = build("classroom", "v1", credentials=get_credentials())
  try:
    course = service.courses().get(id=course_id).execute()
    if course_name is not None:
      course["name"] = course_name
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
  """

  service = build("classroom", "v1", credentials=get_credentials())
  results = service.courses().list().execute()
  courses = results.get("courses", [])
  return courses


def get_topics(course_id):
  """Get list of topics from classroom

  Args:course_id
  Returns:
    returns list of topics of given course in classroom
  """

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
  """

  service = build("classroom", "v1", credentials=get_credentials())
  topic_id_map = {}
  for topic in topics:
    old_topic_id = topic["topicId"]
    topic_name = topic["name"]
    topic = {"name": topic_name}
    response = service.courses().topics().create(courseId=course_id,
                                                 body=topic).execute()
    topic_id_map[old_topic_id] = response["topicId"]
  Logger.info(f"Topics created for course_id{course_id}")
  return topic_id_map


def get_coursework_list(course_id):
  """Get  list of coursework from classroom

  Args: course_id
  Returns:
    returns list of coursework of given course in classroom
  """

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


def list_coursework_submissions_user(course_id, coursework_id, user_id):
  """Get  list of coursework from classroom

  Args: course_id: classroom course_id
  coursework_id: coursework_id of claaassroom coursework
  user_id : email or the numeric identifier for the user or me
  Returns:
    returns list of coursework of given course in classroom
    """ ""

  service = build("classroom", "v1", credentials=get_credentials())
  submissions = []
  page_token = None
  while True:
    coursework = service.courses().courseWork()
    response = coursework.studentSubmissions().list(pageToken=page_token,
                                                    courseId=course_id,
                                                    courseWorkId=coursework_id,
                                                    userId=user_id).execute()
    submissions.extend(response.get("studentSubmissions", []))
    page_token = response.get("nextPageToken", None)
    if not page_token:
      break
  return submissions


def patch_student_submission(course_id, coursework_id, student_submission_id,
                             assigned_grade, draft_grade):
  """Get  list of coursework from classroom

  Args: course_id
  Returns:
    returns list of coursework of given course in classroom
    """ ""
  service = build("classroom", "v1", credentials=get_credentials())
  student_submission = {
      "assignedGrade": assigned_grade,
      "draftGrade": draft_grade
  }
  patch_result = service.courses().courseWork().studentSubmissions().patch(
      courseId=course_id,
      courseWorkId=coursework_id,
      id=student_submission_id,
      updateMask="assignedGrade,draftGrade",
      body=student_submission).execute()
  return patch_result


def get_coursework_material_list(course_id):
  """Get  list of coursework from classroom

  Args: course_id
  Returns:
    returns list of coursework of given course in classroom
  """

  service = build("classroom", "v1", credentials=get_credentials())
  try:
    coursework_list = service.courses().courseWorkMaterials().list(
        courseId=course_id).execute()
    if coursework_list:
      coursework_list = coursework_list["courseWorkMaterial"]
    return coursework_list
  except HttpError as error:
    logger.error(error)
    return None


def create_coursework(course_id, coursework):
  """create coursework in a classroom course

  Args:
    course_id: where coursework need to be created
    coursework : list of dictionary of coursework to be created
  Returns:
    returns success
  """

  service = build("classroom", "v1", credentials=get_credentials())
  data = service.courses().courseWork().create(courseId=course_id,
                                               body=coursework).execute()
  Logger.info("Create coursework method worked")
  return data


def create_coursework_material(course_id, coursework_material_list):
  """create coursework in a classroom course

  Args:
    course_id: where coursework need to be created
    coursework : list of dictionary of coursework to be created
  Returns:
    returns success
  """
  Logger.info("In Create coursework Material")
  service = build("classroom", "v1", credentials=get_credentials())
  for coursework_item in coursework_material_list:
    _ = service.courses().courseWorkMaterials().create(
        courseId=course_id, body=coursework_item).execute()
  Logger.info("Create coursework Material worked")
  return "success"


def delete_course_by_id(course_id):
  """Delete a course from classroom

  Args: course_id
  Returns:
    []
  """

  service = build("classroom", "v1", credentials=get_credentials())
  course = service.courses().delete(id=course_id).execute()
  return course


def get_course_work_list(section_id):
  """Returns an array of objects containing all the coursework details of a
    course

    Args:
      course_id: unique id of the course for which the coursework needs to
        be fetched
    Returns:
      returns success
  """

  section_details = Section.find_by_id(section_id)
  service = build("classroom", "v1", credentials=get_credentials())

  coursework_list = service.courses().courseWork().list(
      courseId=section_details.classroom_id).execute()
  if coursework_list:
    coursework_list = coursework_list["courseWork"]
  return coursework_list


def get_submitted_course_work_list(section_id,
                                   user_id,
                                   headers,
                                   course_work_id="-"):
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
  """

  section_details = Section.find_by_id(section_id)
  response = requests.get(f"{USER_MANAGEMENT_BASE_URL}/user/{user_id}",
                          headers=headers,
                          timeout=60)
  user_email = response.json()["data"]["email"]
  service = build("classroom", "v1", credentials=get_credentials())

  submitted_course_work_list = service.courses().courseWork(
  ).studentSubmissions().list(courseId=section_details.classroom_id,
                              courseWorkId=course_work_id,
                              userId=user_email).execute()
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


def create_student_in_course(access_token, student_email, course_id,
                             course_code):
  """
  Args:
    access_token(str): Oauth access token which contains student credentials
  Return:
    enrolled student object
  """
  service = build("classroom",
                  "v1",
                  credentials=get_oauth_credentials(access_token))
  student = {"userId": student_email}
  result = service.courses().students().create(
      courseId=course_id, body=student, enrollmentCode=course_code).execute()
  return result


def get_person_information(access_token):
  """
  Args:
    access_token(str): Oauth access token which contains
    student credentials
  Return:
    profile: dictionary of users personal information
  """
  people_service = build("people", "v1",\
     credentials=get_oauth_credentials(access_token))
  profile = people_service.people().get(
      resourceName="people/me",
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
    raise InvalidTokenError(
        "Invalid access_token please provide a valid token")
  return creds


def enroll_student(headers, access_token, course_id, student_email,
                   course_code):
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
  # Call search by email user-management API to get the student data
  response = requests.get(
      f"{USER_MANAGEMENT_BASE_URL}/user/search/email?email={student_email}",
      headers=headers,
      timeout=60)
  # If the response is success check if student is inactive i.e  raise error
  searched_student = []
  if response.status_code == 200:
    searched_student = response.json()["data"]
    if searched_student != []:
      if searched_student[0]["status"] == "inactive":
        raise InternalServerError(
            "Student inactive in database is trying to enroll.Please update the student status"
        )

  # Given student is active then call create
  # student in classroom course function

  access_token_details = requests.get(
      f"https://oauth2.googleapis.com/tokeninfo?access_token={access_token}",
      timeout=60)
  Logger.info(
      f"Enroll{student_email},classroom_id {course_id},classroom_code {course_code}{access_token_details.json()}"
  )
  create_student_in_course(access_token, student_email, course_id, course_code)
  # Get the gaia ID, first name, last_name of the student
  # Call_people api function
  profile = get_person_information(access_token)
  gaia_id = profile["metadata"]["sources"][0]["id"]
  # Call user API
  data = {
      "first_name": profile["names"][0]["givenName"],
      "last_name": profile["names"][0]["familyName"],
      "email": student_email,
      "user_type": "learner",
      "user_groups": [],
      "status": "active",
      "is_registered": True,
      "failed_login_attempts_count": 0,
      "access_api_docs": False,
      "gaia_id": gaia_id,
      "photo_url": profile["photos"][0]["url"]
  }
  # Check if searched user is [] ,i.e student is enrolling for first time
  # then call create user user-management API and return user data else
  # return searched user data
  if searched_student == []:
    response = requests.post(f"{USER_MANAGEMENT_BASE_URL}/user",
                             json=data,
                             headers=headers,
                             timeout=60)
    if response.status_code != 200:
      raise UserManagementServiceError(response.json()["message"])
    return response.json()["data"]
  else:
    return searched_student[0]


def get_edit_url_and_view_url_mapping_of_form():
  """  Query google drive api and get all the forms a user owns
      return a dictionary of view link as keys and edit link as values
  """
  service = build("drive", "v3", credentials=get_credentials())
  page_token = None
  count =0
  view_link_and_edit_link_matching = {}
  while True:
    page_size = 75
    response = service.files().list(
        q="mimeType=\"application/vnd.google-apps.form\"",
        spaces="drive",
        pageSize=page_size,
        fields="nextPageToken, "
        "files(id, name,webViewLink,thumbnailLink)",
        pageToken=page_token).execute()
    for file in response.get("files", []):
      count=count+1
      result = get_view_link_from_id(file.get("id"))
      view_link_and_edit_link_matching[result["responderUri"]] = \
      {"webViewLink":file.get("webViewLink"),"file_id":file.get("id")}
    if "nextPageToken" in response.keys():
      Logger.info(f"Listed google forms count is {count}")
      page_token = response["nextPageToken"]
    else:
      Logger.info(f"Listed all  google forms {count}")
      page_token = None
    if page_token is None:
      break
  Logger.info(f"Total count of google forms {count}")
  return view_link_and_edit_link_matching


def get_file(file_id):
  service = build("drive", "v3", credentials=get_credentials())
  response = service.files().get(fileId=file_id, fields="*").execute()
  return response


def get_view_link_from_id(form_id):
  """Query google forms api using form id and get view url of google form"""

  service = build("forms", "v1", credentials=get_credentials())
  result = service.forms().get(formId=form_id).execute()
  return result


def retrieve_all_form_responses(form_id):
  "Query google forms api  using form id and get view url of  google form"
  discovery_doc = "https://forms.googleapis.com/$discovery/rest?version=v1"
  service = build("forms",
                  "v1",
                  credentials=get_credentials(),
                  discoveryServiceUrl=discovery_doc,
                  static_discovery=False)
  result = service.forms().responses().list(formId=form_id).execute()
  return result


def invite_user(course_id, email, role):
  """Invite teacher to google classroom using course id and email

  Args:
      course_id (str): google classroom unique id
      teacher_email (str): teacher email id

  Returns:
      dict: response from create invitation method
  """
  Logger.info(f"Inviting User {email} in course {course_id} as {role}")
  service = build("classroom", "v1", credentials=get_credentials())
  body = {"courseId": course_id, "role": role, "userId": email}
  invitation = service.invitations().create(body=body).execute()
  return invitation


def get_invite(invitation_id):
  """Invite teacher to google classroom using course id and email

  Args:
      course_id (str): google classroom unique id
      teacher_email (str): teacher email id

  Returns:
      dict: response from create invitation method
  """
  service = build("classroom", "v1", credentials=get_credentials())
  invitation = service.invitations().get(id=invitation_id).execute()
  return invitation


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
  creds = get_credentials(CLASSROOM_ADMIN_EMAIL)
  service = build("classroom", "v1", credentials=creds)
  body = {
      "feed": {
          "feedType": feed_type,
          FEED_TYPE_DICT.get(feed_type): {
              "courseId": course_id
          }
      },
      "cloudPubsubTopic": {
          "topicName":
          f"projects/{PUB_SUB_PROJECT_ID}/topics/{DATABASE_PREFIX}classroom-notifications"
      }
  }
  return service.registrations().create(body=body).execute()


def delete_student(course_id, student_email):
  """Delete student from google classroom using course id and email
  Args:
      course_id (str): google classroom unique id
      teacher_email (str): teacher email id
  Returns:
      dict: response from create invitation method
  """
  service = build("classroom", "v1", credentials=get_credentials())
  student = {"userId": student_email}
  student = service.courses().students().delete(
      courseId=course_id, userId=student_email).execute()
  return student


def get_user_details(user_id, headers):
  """Get user from user collection
  Args:
      user_id (str): user_id from user collection
      headers: Auth headers

  Returns:
      dict: response from user API
  """

  response_get_student = requests.get(
      f"{USER_MANAGEMENT_BASE_URL}/user/{user_id}",
      headers=headers,
      timeout=60)
  if response_get_student.status_code == 404:
    raise ResourceNotFoundException(response_get_student.json()["message"])
  return response_get_student.json()


def get_user_details_by_email(user_email, headers):
  """Get user from user collection
  Args:
      user_email (str): user email id
      headers : Auth headers

  Returns:
      dict: response from user API
  """

  response_get_student = requests.get(
      f"{USER_MANAGEMENT_BASE_URL}/user/search/email?email={user_email}",
      headers=headers,
      timeout=60)
  if response_get_student.status_code == 404:
    raise ResourceNotFoundException(response_get_student.json()["message"])
  return response_get_student.json()


def acceept_invite(invitation_id, email):
  """Accept invite sent to user

  Args:
      invitation_id (str): google classroom invitation Id from invite
      user response
      email (str): user email id

  Returns:
      dict: response from create invitation method
  """
  service = build("classroom", "v1",
    credentials=get_credentials(email))
  course = service.invitations().accept(id=invitation_id).execute()
  return course


def get_user_profile_information(user_email):
  """
   Args:
      user_email: email of user
    Returns:
      profile_information: User profile information of the user
  """
  service = build("classroom", "v1", credentials=get_credentials())

  profile_information = service.userProfiles().get(userId=user_email).execute()
  if not profile_information["photoUrl"].startswith("https:"):
    profile_information[
        "photoUrl"] = "https:" + profile_information["photoUrl"]
  return profile_information


def get_course_work(course_id, course_work_id):
  """get course work by course id and course work id
  Args:
    course_id (str): _description_
    course_work_id (str): _description_
  Returns:
    dict: _description_
  """
  service = service = build("classroom", "v1", credentials=get_credentials())
  return service.courses().courseWork().get(courseId=course_id,
                                            id=course_work_id).execute()


def delete_course_work(course_id, course_work_id):
  """delete course work by course id and course work id
  Args:
    course_id (str): Id of the course
    course_work_id (str): Id of the course work to be deleted
  Returns:
    dict: empty dict if success
  """
  service = service = build("classroom", "v1", credentials=get_credentials())
  data = service.courses().courseWork().delete(courseId=course_id,
                                               id=course_work_id).execute()
  Logger.info(
      f"Deleted course work - {course_work_id} in course - {course_id}")
  return data


def update_course_work(course_id, course_work_id, update_mask, updated_body):
  """update course work by course id and course work id
  Args:
    course_id (str): Id of the course
    course_work_id (str): Id of the course work to be deleted
    update_mask (str): Fields(Concat multiple fields if any) to be updated in the coursework
    updated_body(dict): Updated field object data
  Returns:
    dict: empty dict if success
  """
  service = service = build("classroom", "v1", credentials=get_credentials())
  data = service.courses().courseWork().patch(
      courseId=course_id,
      id=course_work_id,
      body=updated_body,
      updateMask=update_mask).execute()
  Logger.info(
      f"Updated course work - {course_work_id} in course - {course_id}")
  return data


def post_grade_of_the_user(section_id: str,
                           course_work_id: str,
                           submission_id: str,
                           assigned_grade: float = None,
                           draft_grade: float = None):
  """
   Args:
      section_id: Unique ID of the section
      course_work_id: Google classroom course work id
      submission_id: Google classroom submission id of a student
      assigned_grade: Final grade assigned to the user
      draft_grade: Draft grade given to the user
  Returns:
      dict: Output response from the classroom for post grade
  """
  service = build("classroom", "v1", credentials=get_credentials())

  section_details = Section.find_by_id(section_id)
  course_id = section_details.classroom_id

  student_submission = {}

  if assigned_grade is not None:
    student_submission["assignedGrade"] = assigned_grade

  if draft_grade is not None:
    student_submission["draftGrade"] = draft_grade

  output = service.courses().courseWork().studentSubmissions().patch(
      courseId=course_id,
      courseWorkId=course_work_id,
      id=submission_id,
      updateMask="assignedGrade,draftGrade",
      body=student_submission).execute()

  return output

def delete_drive_folder(folder_id):
  service= build("drive", "v3", credentials=get_credentials())
  result=service.files().delete(fileId=folder_id).execute()
  return result
