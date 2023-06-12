""" Hepler functions for classroom crud API """
from googleapiclient.discovery import build
from config import CLASSROOM_ADMIN_EMAIL
from helper.secrets_helper import get_gke_pd_sa_key_from_secret_manager
from common.utils.jwt_creds import JwtCredentials
from common.utils import classroom_crud

FEED_TYPE_DICT = {
    "COURSE_WORK_CHANGES": "courseWorkChangesInfo",
    "COURSE_ROSTER_CHANGES": "courseRosterChangesInfo"
}
REGISTER_SCOPES = [
    "https://www.googleapis.com/auth/classroom.push-notifications",
    "https://www.googleapis.com/auth/" +
    "classroom.student-submissions.students.readonly",
    "https://www.googleapis.com/auth/classroom.rosters.readonly"
]
SCOPES = [
    "https://www.googleapis.com/auth/classroom.rosters",
    "https://www.googleapis.com/auth/classroom.coursework.students.readonly",
    "https://www.googleapis.com/auth/classroom.coursework.me.readonly",
    "https://www.googleapis.com/auth/classroom.rosters.readonly",
    "https://www.googleapis.com/auth/classroom.profile.emails",
    "https://www.googleapis.com/auth/classroom.profile.photos",
    "https://www.googleapis.com/auth/classroom.courseworkmaterials",
    "https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly"
]


def get_service():
  """_summary_

  Returns:
    _type_: _description_
  """
  google_oauth_token_endpoint = "https://oauth2.googleapis.com/token"
  service_account_email = classroom_crud.get_default_service_account_email()
  creds = JwtCredentials.from_default_with_subject(
    CLASSROOM_ADMIN_EMAIL,
    service_account_email,
    google_oauth_token_endpoint,
    scopes=SCOPES)
  return build("classroom", "v1", credentials=creds,num_retries=15)

def get_user(user_id):
  """ get user details from classroom
  Args:
    user_id (String): Guy id of a user

  Returns:
    dict: User details
  """
  service=get_service()
  return service.userProfiles().get(userId=user_id).execute()

def get_course_work(course_id,course_work_id):
  """get course work details

  Args:
    course_id (str): _description_
    course_work_id (str): _description_

  Returns:
    _type_: _description_
  """
  service=get_service()
  return service.courses().courseWork().get(
    courseId=course_id,id=course_work_id).execute()

def get_course_work_material(course_id,course_work_id):
  """get course work material details

  Args:
    course_id (str): _description_
    course_work_id (str): _description_

  Returns:
    _type_: _description_
  """
  service=get_service()
  return service.courses().courseWorkMaterials().get(
    courseId=course_id,id=course_work_id).execute()


def get_student_submissions(course_id, course_work_id,submissions_id):
  """_summary_

  Args:
    course_id (_type_): _description_
    course_work_id (_type_): _description_
    submissions_id (_type_): _description_

  Returns:
    _type_: _description_
  """
  service = get_service()
  return service.courses().courseWork().studentSubmissions().get(
    courseId=course_id, courseWorkId=course_work_id,id=submissions_id).execute()
