import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.cloud import secretmanager


SCOPES = [
    "https://www.googleapis.com/auth/classroom.push-notifications",
    "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly",
    "https://www.googleapis.com/auth/classroom.rosters.readonly",
    "https://www.googleapis.com/auth/classroom.rosters",
    "https://www.googleapis.com/auth/classroom.courses"
]

PROJECT_ID = os.getenv("PROJECT_ID", "")
CLASSROOM_KEY = json.loads(os.environ.get("GKE_CLASSROOM_POD_SA_KEY"))

def get_email(index):
  client = secretmanager.SecretManagerServiceClient()
  e2e_admin_teacher_id = f"e2e-admin-teacher-{index}-username"
  e2e_admin_teacher_secret_name = f"projects/{PROJECT_ID}/secrets/{e2e_admin_teacher_id}/versions/latest"
  user_email_password_response = client.access_secret_version(
      request={"name": e2e_admin_teacher_secret_name})
  return user_email_password_response.payload.data.decode("UTF-8")

def get_creds(e2e_admin_email):
  credentials = None
  a_creds = service_account.Credentials.from_service_account_info(
    CLASSROOM_KEY,scopes=SCOPES)
  credentials = a_creds.with_subject(e2e_admin_email)
  return credentials


def registration_func(creds, course_id):
  service = build("classroom", "v1", credentials=creds)
  # register course_work_changes
  body = {
      "feed": {
          "feedType": "COURSE_WORK_CHANGES",
          "courseWorkChangesInfo": {
              "courseId": course_id
          }
      },
      "cloudPubsubTopic": {
          "topicName":
          "projects/gcp-classroom-dev/topics/classroom-messeges"
      }
  }
  service.registrations().create(body=body).execute()
  print("success course work changes!")

  # register course_work_changes
  body = {
      "feed": {
          "feedType": "COURSE_ROSTER_CHANGES",
          "courseRosterChangesInfo": {
              "courseId": course_id
          }
      },
      "cloudPubsubTopic": {
          "topicName":
          "projects/gcp-classroom-dev/topics/classroom-messeges"
      }
  }
  service.registrations().create(body=body).execute()
  print("success course roster changes!")


def create_course(course_name, creds):
  service = build("classroom", "v1", credentials=creds)

  course = {"name": course_name, "ownerId": "me"}
  try:
    course = service.courses().create(body=course).execute()
    print(f"Course created:  {(course.get('name'), course.get('id'))}")
    return course
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error


def delete_course(course, creds):
  service = build("classroom", "v1", credentials=creds)

  try:
    service.courses().delete(id=course.get("id"))
    print(f"Course deleted:  {(course.get('name'), course.get('id'))}")
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error


if __name__ == "__main__":
  for i in range(1,5):
    try:
      email = get_email(i)
      print(f"Started script for {email.split('@')[0]}")
      credential = get_creds(email)
      course_details = create_course("test_pub/sub", credential)
      registration_func(credential, course_details["id"])
      delete_course(course_details, credential)
      print(f"Done for {email.split('@')[0]}")
    except HttpError as hte:
      print(f"An error occured for teacher no:{i}\nerror:{hte}")
