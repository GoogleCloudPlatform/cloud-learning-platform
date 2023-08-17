import os

from google.oauth2.credentials import Credentials

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# SCOPES = [
#     'https://www.googleapis.com/auth/classroom.rosters',
#     "https://www.googleapis.com/auth/userinfo.email",
#     "https://www.googleapis.com/auth/userinfo.profile",
#     # 'https://www.googleapis.com/auth/classroom.courses',
# ]

SCOPES =[
"https://www.googleapis.com/auth/classroom.rosters", 
"https://www.googleapis.com/auth/userinfo.email",
"https://www.googleapis.com/auth/userinfo.profile",
"openid",
"https://www.googleapis.com/auth/classroom.coursework.me",
"https://www.googleapis.com/auth/classroom.courses",
"https://www.googleapis.com/auth/classroom.coursework.students",
"https://www.googleapis.com/auth/classroom.courseworkmaterials",
"https://www.googleapis.com/auth/classroom.topics"
]
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'


def list_courses(creds):
  service = build('classroom', 'v1', credentials=creds)

  results = service.courses().list(pageSize=10).execute()
  courses = results.get('courses', [])

  if not courses:
    print('No courses found.')
    return
  return courses


def enter_course(creds):
  service = build('classroom', 'v1', credentials=creds)
  body = {"userId": "me"}
  course_id = "COURSE_ID"
  enrollment_code = "ztdkcvq"
  service.courses().students().create(courseId=course_id,
                                      enrollmentCode=enrollment_code,
                                      body=body).execute()


def accept_invite(creds):
  service = build('classroom', 'v1', credentials=creds)
  INVITE_ID = "INSERT_EHRE"
  service.invitations().accept(id=service).execute()


def get_creds():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

  # If there are no (valid) credentials available, let the user log in.
  # if not creds or not creds.valid:
  #   if creds and creds.expired and creds.refresh_token:
  #     creds.refresh(Request())
  #   else:
  flow = InstalledAppFlow.from_client_secrets_file('credentials.json',
                                                    SCOPES)
  creds = flow.run_local_server(port=3008)
  # Save the credentials for the next run
  print("Creds Generated success")
  print(creds.to_json())
  with open('token.json', 'w') as token:
    token.write(creds.to_json())

  return creds


# psuedo code for fast API
# class Creds(BaseModel):
#     token: str
#     email: str
#     first_name: str


# @router.post("/sections/{section_id}/students", response_model=[])
# def add_student(section_id, creds: Creds):
def add_student(creds):
  service = build('classroom', 'v1', credentials=creds)
  # send email and not "me" so we verify token matches
  student = {"userId": creds.email}
  service.courses().students().create(
      courseId="INSERT_COURSE_ID",
      body=student,
      enrollmentCode="INSERT_ENROLLMENT_CODE").execute()


def main():
  creds = get_creds()
  # accept_invite(creds)
  # add_student(creds)
  print(creds.to_json())


if __name__ == "__main__":
  main()