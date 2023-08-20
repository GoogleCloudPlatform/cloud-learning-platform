""" Helper Functions"""
import os
from google.cloud import secretmanager

PROJECT_ID = os.getenv("PROJECT_ID", "core-learning-services-dev")


def get_e2e_test_user():
  client = secretmanager.SecretManagerServiceClient()
  user_email_password_secret_id = "e2e_test_email_password"
  user_email_password_secret_name = f"projects/{PROJECT_ID}/secrets/{user_email_password_secret_id}/versions/latest"
  user_email_password_response = client.access_secret_version(
      request={"name": user_email_password_secret_name})
  return user_email_password_response.payload.data.decode("UTF-8")


def get_org_test_user():
  client = secretmanager.SecretManagerServiceClient()
  user_email_secret_id = "org-test-user-1-username"
  user_password_secret_id = "org-test-user-1-password"
  user_email_secret_name = f"projects/{PROJECT_ID}/secrets/{user_email_secret_id}/versions/latest"
  user_password_secret_name = f"projects/{PROJECT_ID}/secrets/{user_password_secret_id}/versions/latest"
  user_email_response = client.access_secret_version(
      request={"name": user_email_secret_name})
  user_password_response = client.access_secret_version(
      request={"name": user_password_secret_name})
  return {
      "email": user_email_response.payload.data.decode("UTF-8"),
      "password": user_password_response.payload.data.decode("UTF-8")
  }


def get_data():
  e2e_test_credentials = get_e2e_test_user()
  e2e_test_email = e2e_test_credentials.get("email")
  e2e_test_password = e2e_test_credentials.get("password")
  faculty_credentials = get_org_test_user()
  e2e_faculty_email = faculty_credentials.get("email")
  e2e_faculty_password = faculty_credentials.get("password")
  return f"""
      export E2E_TEST_EMAIL={e2e_test_email}
      export E2E_TEST_PASSWORD={e2e_test_password}
      export E2E_FACULTY_EMAIL={e2e_faculty_email}
      export E2E_FACULTY_PASSWORD={e2e_faculty_password}
  """


print(get_data())
