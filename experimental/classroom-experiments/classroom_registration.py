import os

from google.oauth2.credentials import Credentials

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/classroom.push-notifications",
    # "https://www.googleapis.com/auth/classroom.coursework.students.readonly",
    "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly",
    "https://www.googleapis.com/auth/classroom.rosters.readonly"
]


def get_creds():
  creds = None
  flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
  creds = flow.run_local_server(port=3008)

  return creds


def registration_func(creds):
  service = build('classroom', 'v1', credentials=creds)
  # register course_work_changes
  body = {
      "feed": {
          "feedType": "COURSE_WORK_CHANGES",
          "courseWorkChangesInfo": {
              "courseId": "579547971345"
              # "courseId": "NTgxMjAwNjMxMTEw"
          }
      },
      "cloudPubsubTopic": {
          "topicName":
          "projects/core-learning-services-dev/topics/classroom-messeges"
          # "projects/improper-pay-test-6/topics/classroom-test"
      }
  }
  service.registrations().create(body=body).execute()
  print("success course work changes!")

  # register course_work_changes
  body = {
      "feed": {
          "feedType": "COURSE_ROSTER_CHANGES",
          "courseRosterChangesInfo": {
              "courseId": "579547971345"
          }
      },
      "cloudPubsubTopic": {
          "topicName":
          "projects/core-learning-services-dev/topics/classroom-messeges"
      }
  }
  service.registrations().create(body=body).execute()
  print("success course roster changes!")


if __name__ == "__main__":
  creds = get_creds()
  # accept_invite(creds)
  registration_func(creds)
