""" Hepler functions for classroom crud API """
from google.oauth2 import service_account
from googleapiclient.discovery import build
from config import CLASSROOM_ADMIN_EMAIL
from helper.secrets_helper import get_gke_pd_sa_key_from_secret_manager

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
    "https://www.googleapis.com/auth/classroom.profile.photos"
]

def get_service():
  """_summary_

  Returns:
    _type_: _description_
  """
  creds = service_account.Credentials.from_service_account_info(
      get_gke_pd_sa_key_from_secret_manager(), scopes=SCOPES)
  creds = creds.with_subject(CLASSROOM_ADMIN_EMAIL)
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
