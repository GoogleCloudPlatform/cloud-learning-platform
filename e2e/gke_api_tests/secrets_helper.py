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


def get_student_email_and_token():
  """Get student email and token

    Returns:
        dict: returns a dict which contains student email and token
    """
  student_email_token_name_mapping = {
    "personal-test-user-1-username": "add_student_token",
    "personal-test-user-2-username": "add_student_token_2",
    "personal-test-user-3-username":"add_student_token_3", 
    "personal-test-user-4-username":"add_student_token_4"}

  keys = ["personal-test-user-1-username",
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

  # credentials_dict = json.loads(
  #     student_token_response.payload.data.decode("UTF-8"))
  # creds = Credentials.from_authorized_user_info(
  #     credentials_dict, scopes=credentials_dict["scopes"])
  # if not creds or not creds.valid:
  #   if creds and creds.expired and creds.refresh_token:
  #     creds.refresh(Request())
  #     credentials_dict = json.loads(creds.to_json())
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

get_student_email_and_token()