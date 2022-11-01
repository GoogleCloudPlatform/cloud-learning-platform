"""
Copyright 2022 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.rosters'
]
"""Shows basic usage of the Classroom API.
Prints the names of the first 10 courses the user has access to.
"""
a_creds = service_account.Credentials.from_service_account_file('service.json',
                                                                scopes=SCOPES)

ADMIN_EMAIL = "<INSERT_ADMIN_EMAIL>"
STUDENT_EMAIL = "<INSERT_STUDENT_EMAIL>"
COURSE_ID = "<INSERT_COURSE_ID"
ENROLLMENT_CODE = "<INSERT_ENROLLMENT_CODE>"

creds = a_creds.with_subject(ADMIN_EMAIL)

# creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.

# if os.path.exists('token.json'):
#     creds = Credentials.from_authorized_user_file('token.json', SCOPES)

# # If there are no (valid) credentials available, let the user log in.
# if not creds or not creds.valid:
#     if creds and creds.expired and creds.refresh_token:
#         creds.refresh(Request())
#     else:
#         flow = InstalledAppFlow.from_client_secrets_file(
#             'credentials.json', SCOPES)
#         creds = flow.run_local_server(port=3008)
#     # Save the credentials for the next run
#     # with open('token.json', 'w') as token:
#     #     token.write(creds.to_json())


def get_courses():
  service = build('classroom', 'v1', credentials=creds)
  try:
    service = build('classroom', 'v1', credentials=creds)

    # Call the Classroom API
    results = service.courses().list(pageSize=10).execute()
    courses = results.get('courses', [])

    if not courses:
      print('No courses found.')
      return
    return courses
  except HttpError as error:
    print('An error occurred: %s' % error)


def enroll_student(student_email, course_id, enrollment_code):
  service = build('classroom', 'v1', credentials=creds)
  status = False
  try:
    student = {'userId': student_email}

    course_id = course_id
    student = service.courses().students().create(
        courseId=course_id, enrollmentCode=enrollment_code,
        body=student).execute()
    print('''User {%s} was enrolled as a student in
            the course with ID "{%s}"''' %
          (student.get('profile').get('name').get('fullName'), course_id))
    status = True
  except HttpError as error:
    print('An error occurred: %s' % error)

  return status


def main():
  try:
    service = build('classroom', 'v1', credentials=creds)

    # Call the Classroom API
    results = service.courses().list(pageSize=10).execute()
    courses = results.get('courses', [])

    if not courses:
      print('No courses found.')
      # return
    # Prints the names of the first 10 courses.
    print('Courses:')
    for course in courses:
      print(course["name"], course["id"], course["alternateLink"])

    enroll_status = enroll_student(STUDENT_EMAIL, COURSE_ID, ENROLLMENT_CODE)
    print("Enrollment status", enroll_status)

    # enroll student

  except HttpError as error:
    print('An error occurred: %s' % error)


if __name__ == '__main__':
  main()
