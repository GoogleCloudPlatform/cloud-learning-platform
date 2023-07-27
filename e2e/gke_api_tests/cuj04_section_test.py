"""Course template list and Course template CRUD API e2e tests"""
import os
import pytest
import json

import requests
from common.utils.errors import ResourceNotFoundException
from secrets_helper import get_required_emails_from_secret_manager
from googleapiclient.discovery import build
from google.oauth2 import service_account
from common.testing.example_objects import create_fake_data, TEST_COURSE_TEMPLATE2, TEST_COHORT2, TEST_SECTION2
from common.utils.jwt_creds import JwtCredentials
from testing_objects.test_config import API_URL
from testing_objects.token_fixture import get_token,sign_up_user

DATABASE_PREFIX = os.environ.get("DATABASE_PREFIX")
EMAILS = get_required_emails_from_secret_manager()



def create_course(name, description, section, owner_id):
  """Create course Function in classroom

  Args: course_name ,description of course, section,owner_id of course
  Returns:
    new created course details
    """ ""
  SCOPES = [
      "https://www.googleapis.com/auth/classroom.courses",
      "https://www.googleapis.com/auth/classroom.courses.readonly"
  ]
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
  a_creds = service_account.Credentials.from_service_account_info(
      CLASSROOM_KEY, scopes=SCOPES)
  creds = a_creds.with_subject(CLASSROOM_ADMIN_EMAIL)
  service = build("classroom", "v1", credentials=creds)
  new_course = {}
  new_course["name"] = name
  new_course["section"] = section
  new_course["description"] = description
  # new_course["room"]=course["room"]
  new_course["ownerId"] = owner_id
  # new_course["descriptionHeading"]=course["description_heading"]
  course = service.courses().create(body=new_course).execute()
  course_name = course.get("name")
  course_id = course.get("id")
  print("___________Course creaated___________________",course)
  return course

def test_create_section(get_token):

  """
  create a Course template and cohort is created  by  user  
  then user clicks on create section button and makes a section 
  by providing section name ,description,course_template_id,cohort_id
  and list of teachers .A record is created in database and a course
  with details of course template is created in classroom
  """
  # Create fake classroom in google classroom
  course = create_course(DATABASE_PREFIX + "test_course", "This is test",
                         "test", "me")
  # Create fake Mastr course in Firestore
  classroom_id = course["id"]
  test_course_template_dict = TEST_COURSE_TEMPLATE2
  test_course_template_dict["name"] = DATABASE_PREFIX + "test_course"
  test_course_template_dict["instructional_designer"] = EMAILS["instructional_designer"]
  fake_data = create_fake_data(test_course_template_dict, TEST_COHORT2,
                               TEST_SECTION2, classroom_id)
  url = f"{API_URL}/sections"

  data = {
      "name": "e2e_test_section",
      "description": "string",
      "course_template": fake_data[0].id,
      "cohort": fake_data[1].id,
      "max_students":25
  }
  resp = requests.post(url=url, json=data, headers=get_token)
  resp_json = resp.json()
  assert resp.status_code == 202, "Status 202"


def test_create_section_course_template_not_found(get_token):
  """ 
  create a Course template and cohort is created  by  user  
  then user clicks on create section button and makes a section 
  by providing section name ,description,course_template_id,cohort_id
  and list of teachers .Given course template id is wrong and course template 
  id not found error is thrown
  """
  # Create fake classroom in google classroom
  course = create_course(DATABASE_PREFIX + "test_course", "This is test",
                         "test", "me")
  # Create fake Mastr course in Firestore
  classroom_id = course["id"]
  fake_data = create_fake_data(TEST_COURSE_TEMPLATE2, TEST_COHORT2,
                               TEST_SECTION2, classroom_id)
  url = f"{API_URL}/sections"

  data = {
      "name": "string",
      "description": "string",
      "course_template": "fake_template_id_new",
      "cohort": fake_data[1].id,
      "max_students":25
  }

  resp = requests.post(url=url, json=data, headers=get_token)
  resp_json = resp.json()
  assert resp.status_code == 404


def test_get_section(get_token):
  """
    Get a sections details for a  section by giving section_id as query paramter
  """
  course = create_course(DATABASE_PREFIX + "test_course", "This is test",
                         "test", "me")
  classroom_id = course["id"]
  fake_data = create_fake_data(TEST_COURSE_TEMPLATE2, TEST_COHORT2,
                               TEST_SECTION2, classroom_id)
  url = f"{API_URL}/sections/{fake_data[2].id}"
  resp = requests.get(url=url, headers=get_token)
  resp_json = resp.json()
  assert resp.status_code == 200, "Status 200"


def test_list_sections(get_token):
  """
    List all the sections
  """
  course = create_course(DATABASE_PREFIX + "test_course", "This is test",
                         "test", "me")
  classroom_id = course["id"]
  create_fake_data(TEST_COURSE_TEMPLATE2, TEST_COHORT2, TEST_SECTION2,
                   classroom_id)
  url = f"{API_URL}/sections?skip=0&limit=10"
  print("List sections API url----",url)
  resp = requests.get(url=url, headers=get_token)
  resp_json = resp.json()
  print("This is response JSo list secctions",resp_json)
  assert resp.status_code == 200, "Status 200"


def test_update_section(get_token):
  """ 
  User click on edit button for a section 
  User Updates the section name ,description,course_state by providing expected 
  values and details get updated in firestore and classroom course
  """
  # Create fake classroom in google classroom
  course = create_course(DATABASE_PREFIX + "test_course", "This is test",
                         "test", "me")
  # Create fake Mastr course in Firestore
  classroom_id = course["id"]
  fake_data = create_fake_data(TEST_COURSE_TEMPLATE2, TEST_COHORT2,
                               TEST_SECTION2, classroom_id)
  url = f"{API_URL}/sections"

  data = {
      "id": fake_data[2].id,
      "course_id": classroom_id,
      "section_name": "section_updated",
      "description": "test_description_updated",
      "max_students":25
  }
  resp = requests.patch(url=url, json=data, headers=get_token)
  resp_json = resp.json()
  assert resp.status_code == 200, "Status 200"


def test_update_section_course_not_found_in_classroom(get_token):
  """
  User click on edit button for a section
  User Updates the section name ,description,course_state by providing expected
  values but given course_id of classroom is incorrect so it gives course not found error
  """
  # Create fake classroom in google classroom
  course = create_course(DATABASE_PREFIX + "test_course", "This is test",
                         "test", "me")
  # Create fake Mastr course in Firestore
  classroom_id = course["id"]
  fake_data = create_fake_data(TEST_COURSE_TEMPLATE2, TEST_COHORT2,
                               TEST_SECTION2, classroom_id)
  url = f"{API_URL}/sections"

  data = {
      "id": fake_data[2].id,
      "course_id": "test1222",
      "section_name": "section_updated",
      "description": "test_description_updated",
      "max_students":25
  }
  resp = requests.patch(url=url, json=data, headers=get_token)
  assert resp.status_code == 500
