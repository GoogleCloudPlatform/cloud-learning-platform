""" Hepler functions for classroom crud API """
from google.oauth2 import service_account
from googleapiclient.discovery import build
from config import CLASSROOM_ADMIN_EMAIL, PUB_SUB_PROJECT_ID, DATABASE_PREFIX
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
    "https://www.googleapis.com/auth/classroom.rosters.readonly",
    "https://www.googleapis.com/auth/classroom.profile.emails",
    "https://www.googleapis.com/auth/classroom.profile.photos"
]
def get_user(user_id):
  """
  Args:
    user_id (_type_): _description_

  Returns:
    _type_: _description_
  """
  creds = service_account.Credentials.from_service_account_info(
      get_gke_pd_sa_key_from_secret_manager(), scopes=SCOPES)
  creds = creds.with_subject(CLASSROOM_ADMIN_EMAIL)
  service = build("classroom", "v1", credentials=creds)
  return service.userProfiles().get(userId=user_id).execute()

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
  creds = service_account.Credentials.from_service_account_info(
      get_gke_pd_sa_key_from_secret_manager(), scopes=REGISTER_SCOPES)
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
          "topicName": "projects/" +
          f"{PUB_SUB_PROJECT_ID}/topics/{DATABASE_PREFIX}classroom-messeges"
      }
  }
  return service.registrations().create(body=body).execute()
