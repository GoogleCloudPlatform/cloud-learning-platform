""" Helper Functions"""

from google.cloud import secretmanager
import json

def get_required_emails_from_secret_manager():
    """Get Project user emails for e2e

  Args:
  Returns:
    return the emails in dict format
    """""

    client = secretmanager.SecretManagerServiceClient()
    test_user_secrets = {
        "id":1,
        "name":"test-user-1-username"
        }
    lms_user_secrets = {
        "id":1,
        "name":"lms-service-user"
        }
    test_user_secret_name = f"projects/core-learning-services-dev/secrets/{test_user_secrets['name']}/versions/{test_user_secrets['id']}"
    test_user_response = client.access_secret_version(
        request={"name": test_user_secret_name})
    lms_user_secret_name = f"projects/core-learning-services-dev/secrets/{lms_user_secrets['name']}/versions/{lms_user_secrets['id']}"
    lms_user_response = client.access_secret_version(
        request={"name": lms_user_secret_name})
    data={
        "admin": lms_user_response.payload.data.decode("UTF-8"),
        "instructional_designer": test_user_response.payload.data.decode("UTF-8")
    }
    return data

def get_student_email_and_token():
    """
    
    """
    client = secretmanager.SecretManagerServiceClient()
    student_email={
        "id": 1,
        "name": "personal-test-user-1-username"
    }
    student_token={
        "id": 1,
        "name": "add_student_token"
    }
    student_email_name = f"projects/core-learning-services-dev/secrets/{student_email['name']}/versions/{student_email['id']}"
    student_token_name = f"projects/core-learning-services-dev/secrets/{student_token['name']}/versions/{student_token['id']}"
    student_email_response = client.access_secret_version(
        request={"name": student_email_name})
    student_token_response = client.access_secret_version(
        request={"name": student_token_name})
    data = {
        "email": student_email_response.payload.data.decode("UTF-8"),
        "credentials": json.loads(student_token_response.payload.data.decode("UTF-8"))
    }
    return data