import os

from google.oauth2.credentials import Credentials

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/classroom.push-notifications"]


def get_creds():
  creds = None
  flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
  creds = flow.run_local_server(port=3008)

  return creds


def registration_func(creds):
  service = build('classroom', 'v1', credentials=creds)
  body = {
      "feed": {
          "feedType": "COURSE_WORK_CHANGES",
          "courseWorkChangesInfo": {
              "courseId": "579547971345"
          }
      },
      "cloudPubsubTopic": {
          "topicName":
          "projects/core-learning-services-dev/topics/classroom-messeges"
      }
  }
  service.registrations().create(body=body).execute()


if __name__ == "__main__":
  creds = get_creds()
  # accept_invite(creds)
  registration_func(creds)
