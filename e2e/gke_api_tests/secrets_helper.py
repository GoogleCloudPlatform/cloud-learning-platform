""" Helper Functions"""
import json
import os
import random
from google.cloud import secretmanager
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

PROJECT_ID = os.getenv("PROJECT_ID", "")
# CLASSROOM_KEY = json.loads(os.environ.get("GKE_POD_SA_KEY"))
# CLASSROOM_ADMIN_EMAIL = os.environ.get("CLASSROOM_ADMIN_EMAIL")
PROJECT_ID="core-learning-services-dev"
USE_GMAIL_ACCOUNT_STUDENT_ENROLLMENT=bool(
  os.getenv("USE_GMAIL_ACCOUNT_STUDENT_ENROLLMENT","false").lower() in ("true",))
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

CLASSROOM_ADMIN_EMAIL = "lms_admin_teacher@dhodun.altostrat.com"

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
  "https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly",
  "https://www.googleapis.com/auth/drive.file",
  # "https://www.googleapis.com/auth/drive.appdata"
  ]



def get_required_emails_from_secret_manager():
  """Get Project user emails for e2e

  Args:
  Returns:
    return the emails in dict format
    """ ""

  client = secretmanager.SecretManagerServiceClient()
  test_user_secret_id = "org-test-user-1-username"
  test_user_2_secret_id = "org-test-user-2-username"
  test_user_secret_name = f"projects/{PROJECT_ID}/secrets/{test_user_secret_id}/versions/latest"
  test_user_response = client.access_secret_version(
      request={"name": test_user_secret_name})
  test_user_2_secret_name = f"projects/{PROJECT_ID}/secrets/{test_user_2_secret_id}/versions/latest"
  test_user_2_response = client.access_secret_version(
      request={"name": test_user_2_secret_name})
  data = {
      "teacher": test_user_2_response.payload.data.decode("UTF-8"),
      "instructional_designer": test_user_response.payload.data.decode("UTF-8")
  }
  return data

def get_gmail_student_email_and_token():
  student_email_token_name_mapping = {
    "personal-test-user-1-username": "add_student_token",
    "personal-test-user-2-username": "add_student_token_2",
    "personal-test-user-3-username":"add_student_token_3", 
    "personal-test-user-4-username":"add_student_token_4"}

  keys = [
          "personal-test-user-1-username",
          "personal-test-user-2-username",
          "personal-test-user-3-username",
          "personal-test-user-4-username"]

  test_user1 = random.choice(keys)
  student_email_secret_id = test_user1
  student_token_secret_id = student_email_token_name_mapping[test_user1]

  invite_student_email_secret_id = random.choice([ele for ele in keys if ele != test_user1])
  invite_student_email_token_secret_id = student_email_token_name_mapping[invite_student_email_secret_id]
  student_email_name = f"projects/{PROJECT_ID}/secrets/{student_email_secret_id}/versions/latest"
  student_token_name = f"projects/{PROJECT_ID}/secrets/{student_token_secret_id}/versions/latest"
  # Student Email to enroll student
  print("Get email and student name ",student_email_secret_id,invite_student_email_secret_id)
  client = secretmanager.SecretManagerServiceClient()
  student_email_response = client.access_secret_version(
      request={"name": student_email_name})
  student_token_response = client.access_secret_version(
      request={"name": student_token_name})
  # student email for invite fixture
  invite_student_email_name =  f"projects/{PROJECT_ID}/secrets/{invite_student_email_secret_id}/versions/latest"
  invite_student_email_response = client.access_secret_version(
      request={"name":invite_student_email_name})
  # Token for invite student
  invite_student_token_response = f"projects/{PROJECT_ID}/secrets/{invite_student_email_token_secret_id}/versions/latest"   
  invite_student_token_response = client.access_secret_version(
      request={"name":invite_student_token_response})
  student_creds_dict = get_access_token(student_token_response)
  invite_student_creds_dict = get_access_token(invite_student_token_response)
  data = {
      "email": student_email_response.payload.data.decode("UTF-8"),
      "access_token":student_creds_dict["token"],
      "invite_student_email":invite_student_email_response.payload.data.decode("UTF-8"),
      "invite_student_token": invite_student_creds_dict["token"]
  }
  print(data)
  return data

def get_student_email_and_token():
  """Get student email and token

    Returns:
        dict: returns a dict which contains student email and token
    """
  if USE_GMAIL_ACCOUNT_STUDENT_ENROLLMENT:
    return get_gmail_student_email_and_token()
  workspace_data=get_workspace_student_email_and_token()
  data={
    "email": workspace_data["email"],
    "access_token":workspace_data["access_token"],
    "invite_student_email":workspace_data["email"],
    "invite_student_token": workspace_data["access_token"]
  }
  print(data)
  return data

def get_access_token(credential_object):
  credentials_dict = json.loads(
      credential_object.payload.data.decode("UTF-8"))
  creds = Credentials.from_authorized_user_info(
      credentials_dict, scopes=credentials_dict["scopes"])
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
      credentials_dict = json.loads(creds.to_json())
  return credentials_dict




def get_workspace_student_email_and_token():
  """Get student workspace email and token

    Returns:
        dict: returns a dict which contains student email and token
    """
  client = secretmanager.SecretManagerServiceClient()
  student_email_secret_id = "lms-service-user"
  student_token_secret_id = "lms_user_student_token"
  student_email_name = f"projects/{PROJECT_ID}/secrets/{student_email_secret_id}/versions/latest"
  student_token_name = f"projects/{PROJECT_ID}/secrets/{student_token_secret_id}/versions/latest"
  student_email_response = client.access_secret_version(
      request={"name": student_email_name})
  student_token_response = client.access_secret_version(
      request={"name": student_token_name})
  credentials_dict = json.loads(
      student_token_response.payload.data.decode("UTF-8"))
  creds = Credentials.from_authorized_user_info(
      credentials_dict, scopes=credentials_dict["scopes"])
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
      credentials_dict = json.loads(creds.to_json())
  data = {
      "email": student_email_response.payload.data.decode("UTF-8"),
      "access_token": credentials_dict["token"]
  }
  return data

def get_user_email_and_password_for_e2e():
  client = secretmanager.SecretManagerServiceClient()
  user_email_password_secret_id = "e2e_test_email_password"
  user_email_password_secret_name = f"projects/{PROJECT_ID}/secrets/{user_email_password_secret_id}/versions/latest"
  user_email_password_response = client.access_secret_version(
      request={"name": user_email_password_secret_name})
  return json.loads(user_email_password_response.payload.data.decode(
      "UTF-8"))

def create_coursework(course_id,coursework_body):
  a_creds = service_account.Credentials.from_service_account_info(
      CLASSROOM_KEY, scopes=SCOPES)
  creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
  service = build("classroom", "v1", credentials=creds)
  body=coursework_body
  coursework = service.courses().courseWork().create(courseId=course_id,
                                                 body=body).execute()
  return coursework


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
  a_creds = service_account.Credentials.from_service_account_info(
CLASSROOM_KEY, scopes=SCOPES)
  creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
  discovery_doc = "https://forms.googleapis.com/$discovery/rest?version=v1"
  service = build("forms", "v1", credentials=creds,
                  discoveryServiceUrl=discovery_doc,
                    static_discovery=False)
  result = service.forms().create(body=form_body).execute()
  return result

def get_file(file_id):
  a_creds = service_account.Credentials.from_service_account_info(
CLASSROOM_KEY, scopes=SCOPES)
  creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
  service = build("drive", "v3", credentials=creds)
  response = service.files().get(fileId=file_id,  
    fields="name,webViewLink").execute()
  return response

def insert_file_into_folder(folder_id,file_id):

  a_creds = service_account.Credentials.from_service_account_info(
CLASSROOM_KEY, scopes=SCOPES)
  creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
  service = build("drive", "v2", credentials=creds)
  new_child = {'id': file_id}
  result= service.children().insert(
        folderId=folder_id, body=new_child).execute()
  print("MOved to another folder success",result)

insert_file_into_folder("1JZuikDnHvta7jJwnHSjWw5IcS7EK0QTG","1oZrH6Wc1TSMSQDwO17Y_TCf38Xdpw55PYRRVMMS0fBM")
# get_gmail_student_email_and_token()