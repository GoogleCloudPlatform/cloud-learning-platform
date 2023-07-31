"""
Classroom e2e helper file
"""
import json
import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials

# CLASSROOM_KEY = json.loads(os.environ.get("GKE_POD_SA_KEY"))
CLASSROOM_KEY = {
  "type": "service_account",
  "project_id": "core-learning-services-dev",
  "private_key_id": "4be7916d9af6fbe02c83583873d266325841f9a0",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCGyrinV/KcqVh9\nKa8F0YqzI5xTVhZhnP2PtletU91vfpJ2QJRNuRi9vjmw3W1kC4duTmx6A5uruUrX\nSp4usPMj2IO4Z0gH+B0V5VQgfs4WaKb1E+W+Ha7kwaGt7ayA24IC/CoZfe7l/cU4\nfQYnUPONW1aYf/HpNg3PUPCpwiSIg6YWUbbadqYm43ATkyLAFv9dLrmvh+wdn3u6\nurJPMvmQChLdyWFooF6L41CsNOH9OMnkDEZQ2ymOPxx9A+GYKKZUidFq6Mc23ePA\n3dBhTfXa3VsuTgR7+Py0vJ2kKN/P4UTTQqzZ6cUjCbKc3GBBqcUVJMSAwxjRA70B\nmDw5AqshAgMBAAECggEAFcydVnsTwqBkrkFai/9ahiRBOP0YO4svOtnLjj2c91Yq\nC7PgCD3iMXWdUOxOr7ppmb5XLth8iaY641yu/nAhsm9mxiD19kv7MDpZg7PeUqN0\nNPiV1Exqp5ZlNoLUvjZB7Yeoq1zBkTKcfclCgINIEFlwRNOUZRoX26qEcX/zdpxP\n3iCTKHO9DsSvVQ2y2B/4WoOyIv5kKJlV+aNHWQTtWV0X5r0eJwJWoV5Y6qf9hg7J\nFNWaRII9FxlZ+apJlQOVbEghoRLfVHFvASnjcUgLJ9JktqUsYRFEB1lzmLpODizj\nI/LS7JkE3lCR9ChYrObWmBBMmYAKEmJPrIizESm5jQKBgQC8EYRAACk9uTwjV5PH\n4FLxgfp7AXTolFp8qi6P4nf0w2JhnGNfwXSSArbyOW2zn95EEh2jYUV6CRNTp9xj\nbM59gbkhx6ISIQLVzgR1rtVIZDlVd/j/z0XKKPyRDxSaMpb56eEKVfRGLDWERh6g\nFz3WXQ3I51/+63EQjJD2cIYv0wKBgQC3esfIB/RXuelVDKTzsh7oMI90sa87sVPo\nv2kc1pA12PyVpwK3FsVyQhdGutRQ7UBDy1iR7efpsnjIfnx1ObH4U7tQCM3iGW+i\nYUGJYZg8PIPJ+vpxbkXBwnhEXzhKJMRa+j2/B72FjMkcwwl5m7AUtuiqQYbC+7ZS\nidbnQDHUuwKBgFSb3M+eQu+N4kxUHhwSA767JyEnqpzoAT2Mop4A2M65CA25+cse\nkX8O0Zdv1ra0+Z3OOJ9EJ6mbY6KDJldkoBE+xzc3ROa7Czd9E+yN105WKKUW8GLF\nsTQd9GKeUjp9AAc2/RNVUCwxv3HeyfBkBGHoQ0dbMIjTC27SjnUQco4ZAoGAMqXu\n/jXL6meElJiv9CGITJoTD6h48eZqfkZQUsib+HFUkE8Q/c+IY5kA6eJq94f2hIBe\ni7H7odRFaTsZShbKHP2oKFi11KMm4NEuESlip8YgryHb/nHtSaZQIreSR01M8rw/\nTTtqwrHxVkI0nGAwxBcVtOHvvGVVmAU60I009D8CgYEAgEKI+agn1FKNj1LR1Boq\nitIBouaapKArJN5tI43kuqHnkGmrl8aJS8y0iztkgIrJtTqreGugtTT8fMIVgacH\n05a0ODgR8z0/njUqfzlTw2yN4dt0lOy8EImWXJa+PR3kke+YojiTFCOzY62DJ5HC\nNZlBrN2IZI14DQFRrmBVosc=\n-----END PRIVATE KEY-----\n",
  "client_email": "gke-pod-sa@core-learning-services-dev.iam.gserviceaccount.com",
  "client_id": "104636564660654922211",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/gke-pod-sa%40core-learning-services-dev.iam.gserviceaccount.com"
}
CLASSROOM_ADMIN_EMAIL = os.environ.get("CLASSROOM_ADMIN_EMAIL")
WORKSPACE_ADMIN_EMAIL = os.environ.get("WORKSPACE_ADMIN_EMAIL")
USE_GMAIL_ACCOUNT_STUDENT_ENROLLMENT = bool(
    os.getenv("USE_GMAIL_ACCOUNT_STUDENT_ENROLLMENT", "false").lower() in (
        "true", ))

SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses",
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.coursework.students",
    "https://www.googleapis.com/auth/classroom.rosters",
    "https://www.googleapis.com/auth/classroom.coursework.me",
    "https://www.googleapis.com/auth/classroom.topics",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/forms.body.readonly",
    "https://www.googleapis.com/auth/classroom.profile.photos",
    "https://www.googleapis.com/auth/classroom.courseworkmaterials",
    "https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly"
]
def get_creds(use_teacher=False):
  """_summary_

  Returns:
      _type_: _description_
  """
  a_creds = service_account.Credentials.from_service_account_info(
      CLASSROOM_KEY, scopes=SCOPES)
  if use_teacher:
    return a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
  return a_creds.with_subject(WORKSPACE_ADMIN_EMAIL)

def create_course(name, section, description):
  """Create course Function in classroom

  Args: course_name ,description of course, section,owner_id of course
  Returns:
    new created course details
    """
  
  service = build("classroom", "v1", credentials=get_creds())
  new_course = {}
  new_course["name"] = name
  new_course["section"] = section
  new_course["description"] = description
  new_course["ownerId"] = CLASSROOM_ADMIN_EMAIL
  new_course["courseState"] = "ACTIVE"
  course = service.courses().create(body=new_course).execute()
  return course

def enroll_teacher_in_classroom(classroom_id,teacher_email):
  """enroll teacher in classroom"""
  service = build("classroom", "v1", credentials=get_creds())
  body = {"userId": teacher_email}
  teacher = service.courses().teachers().create(
    courseId=classroom_id,
    body=body).execute()
  profile_information = teacher["profile"]
  if not profile_information["photoUrl"].startswith("https:"):
    profile_information[
      "photoUrl"] = "https:" + profile_information["photoUrl"]
  return profile_information

def accept_invite(invitation_id, access_token=None, teacher_email=None):
  """Add student to the classroom using student google auth token
  Args:
    access_token(str): Oauth access token which contains student credentials
    invitation_id(str): unique classroom id which is required to get the classroom
    email(str): student email id
  Return:
    dict: returns a dict which contains student and classroom details
  """
  if access_token:
    creds = Credentials(token=access_token)
  else:
    a_creds = service_account.Credentials.from_service_account_info(
        CLASSROOM_KEY, scopes=SCOPES)
    creds = a_creds.with_subject(teacher_email)
  service = build("classroom", "v1", credentials=creds)
  data = service.invitations().accept(id=invitation_id).execute()
  return data


def invite_user(course_id, email, role):
  """Invite teacher to google classroom using course id and email

  Args:
      course_id (str): google classroom unique id
      teacher_email (str): teacher email id
  Returns:
      dict: response from create invitation method
  """
  service = build("classroom", "v1", credentials=get_creds(
    USE_GMAIL_ACCOUNT_STUDENT_ENROLLMENT))
  body = {"courseId": course_id, "role": role, "userId": email}
  invitation = service.invitations().create(body=body).execute()
  return invitation

def create_course_work(classroom_id,body):
  service = build("classroom", "v1", credentials=get_creds(True))
  return service.courses().courseWork().create(courseId=classroom_id,
                                                 body=body).execute()
def get_course_work_submission_list(classroom_id,course_work_id,user_id):
  service = build("classroom", "v1", credentials=get_creds(True))
  return service.courses().courseWork().studentSubmissions().list(
      courseId=classroom_id,
      courseWorkId=course_work_id,
      userId=user_id).execute()

def create_coursework_submission(access_token,course_id,coursework_id,submission_id):
  print("Submission creation started")
  creds = Credentials(token=access_token)
  service = build("classroom", "v1", credentials=creds)
  result = service.courses().courseWork().studentSubmissions().turnIn(
    courseId=course_id,
    courseWorkId=coursework_id,
    id=submission_id,body={}).execute()
  print("This is result Turn In done ",result)
  return result

def patch_course_work_submission(classroom_id,course_work_id,submission_id,update_mask,body):
  service = build("classroom", "v1", credentials=get_creds(True))
  return service.courses().courseWork().studentSubmissions().patch(
      courseId=classroom_id,
      courseWorkId=course_work_id,
      id=submission_id,
      updateMask=update_mask,
      body=body).execute()
def list_coursework_submission_user(access_token,course_id,coursework_id,user_id):
  creds = Credentials(token=access_token)
  print("Credentialss ",creds)
  service = build("classroom", "v1", credentials=creds)
  result = service.courses().courseWork().studentSubmissions().list(
    courseId=course_id,
    courseWorkId=coursework_id,
    userId=user_id).execute()
  print("This is result list assignrmt ",result["studentSubmissions"])
  return result["studentSubmissions"]

def create_google_form(title):
  form_body = {
    "info": {
        "title": title,
    }
  }
  discovery_doc = "https://forms.googleapis.com/$discovery/rest?version=v1"
  service = build("forms", "v1", credentials=get_creds(),
                  discoveryServiceUrl=discovery_doc,
                    static_discovery=False)
  result = service.forms().create(body=form_body).execute()
  return result

def get_file(file_id):
  service = build("drive", "v3", credentials=get_creds())
  response = service.files().get(fileId=file_id,  
    fields="name,webViewLink").execute()
  return response

def insert_file_into_folder(folder_id,file_id):
  service = build("drive", "v2", credentials=get_creds())
  new_child = {'id': file_id}
  result= service.children().insert(
        folderId=folder_id, body=new_child).execute()
  return result

def enroll_student_classroom(access_token, course_id, student_email,
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
  creds = Credentials(token=access_token)
  service = build("classroom", "v1", credentials=creds)
  student = {"userId": student_email}
  service.courses().students().create(courseId=course_id,
                                      body=student,
                                      enrollmentCode=course_code).execute()
  # Get the gaia ID of the course
  people_service = build("people", "v1", credentials=creds)
  profile = people_service.people().get(
      resourceName="people/me",
      personFields="metadata,photos,names").execute()
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
  return data
