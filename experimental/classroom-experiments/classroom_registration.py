import os

from google.oauth2.credentials import Credentials

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/classroom.push-notifications",
    "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly",
    "https://www.googleapis.com/auth/classroom.rosters.readonly",
    "https://www.googleapis.com/auth/classroom.rosters",
    "https://www.googleapis.com/auth/classroom.courses"
]


def get_creds():
  creds = None
  if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file('credentials.json',
                                                       SCOPES)
      creds = flow.run_local_server(port=3008)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
      token.write(creds.to_json())


#   creds = None
#   flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
#   creds = flow.run_local_server(port=3008)

  return creds


def invite_func(creds):
  service = build('classroom', 'v1', credentials=creds)

  body = {
      "courseId": "598013753709",
      "userId": "dhodun@google.com",
      "role": "TEACHER"
  }

  service.invitations().create(body=body).execute()


def registration_func(creds):
  service = build('classroom', 'v1', credentials=creds)
  # register course_work_changes
  body = {
      "feed": {
          "feedType": "COURSE_WORK_CHANGES",
          "courseWorkChangesInfo": {
              "courseId": "579547971345"
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
              "courseId": "579547971345"
          }
      },
      "cloudPubsubTopic": {
          "topicName":
          "projects/gcp-classroom-dev/topics/classroom-messeges"
      }
  }
  service.registrations().create(body=body).execute()
  print("success course roster changes!")


def course_update(creds):
  service = build('classroom', 'v1', credentials=creds)
  body = {"name": "test1"}
  service.courses().patch(id=598013753709, updateMask="name",
                          body=body).execute()


if __name__ == "__main__":
  creds = get_creds()
  #   invite_func(creds)
  course_update(creds)
#   registration_func(creds)
