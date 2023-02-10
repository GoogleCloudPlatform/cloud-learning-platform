""" Helper Functions"""
import json
import os
import random
from google.cloud import secretmanager
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

PROJECT_ID = os.getenv("PROJECT_ID", "")


def get_required_emails_from_secret_manager():
  """Get Project user emails for e2e

  Args:
  Returns:
    return the emails in dict format
    """ ""

  client = secretmanager.SecretManagerServiceClient()
  test_user_secret_id = "test-user-1-username"
  # lms_user_secret_id = "lms-service-user"
  lms_user_secret_id = "lms-admin-teacher-username"
  test_user_secret_name = f"projects/{PROJECT_ID}/secrets/{test_user_secret_id}/versions/latest"
  test_user_response = client.access_secret_version(
      request={"name": test_user_secret_name})
  lms_user_secret_name = f"projects/{PROJECT_ID}/secrets/{lms_user_secret_id}/versions/latest"
  lms_user_response = client.access_secret_version(
      request={"name": lms_user_secret_name})
  data = {
      "admin": lms_user_response.payload.data.decode("UTF-8"),
      "instructional_designer": test_user_response.payload.data.decode("UTF-8")
  }
  return data


def get_student_email_and_token():
  """Get student email and token

    Returns:
        dict: returns a dict which contains student email and token
    """
  student_email_token_name_mapping = {
    "personal-test-user-1-username": "add_student_token","personal-test-user-2-username": "add_student_token_2",
    "personal-test-user-3-username":"add_student_token_3", "personal-test-user-4-username":"add_student_token_4"}
  
#   random_idex=random.choice(["personal-test-user-1-username","personal-test-user-2-username"])
  random_index=random.choice(["personal-test-user-1-username","personal-test-user-2-username",
    "personal-test-user-3-username", "personal-test-user-4-username"
  ])
  client = secretmanager.SecretManagerServiceClient()
#   student_email_secret_id = "personal-test-user-1-username"
  # student_email_secret_id = "personal-test-user-2-username"
  student_email_secret_id = random_index
  student_token_secret_id = student_email_token_name_mapping[random_index]
  print("________Student Email and token for E2E__________",student_email_secret_id,student_token_secret_id)
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
      "access_token":credentials_dict["token"]
  }
  return data


def get_workspace_student_email_and_token():
  """Get student workspace email and token

    Returns:
        dict: returns a dict which contains student email and token
    """
  client = secretmanager.SecretManagerServiceClient()
  student_email_secret_id = "org-test-user-1-username"
  student_token_secret_id = "enroll_workspace_student"
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

