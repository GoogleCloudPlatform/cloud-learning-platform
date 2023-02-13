import uuid
import behave
import requests
from testing_objects.test_config import API_URL
from testing_objects.course_template import COURSE_TEMPLATE_INPUT_DATA
from e2e.gke_api_tests.secrets_helper import get_student_email_and_token,get_workspace_student_email_and_token
from environment import create_course

# -------------------------------Enroll student to Section-------------------------------------
# ----Positive Scenario-----


@behave.given("A user has access privileges and wants to enroll a student into a section")
def step_impl_1(context):
  # context.url = f'{API_URL}/sections/{context.sections.id}/students'
  print("IN ENROLL STUDNET_ chort ID",context.cohort.id)
  context.url = f'{API_URL}/cohorts/{context.cohort.id}/students'
  context.payload = get_student_email_and_token()



@behave.when("API request is sent to enroll student to a section with correct request payload and valid section id")
def step_impl_2(context):
  resp = requests.post(context.url, json=context.payload,headers=context.header)
  print("THIS IS RESPONSE FROM ENROLLL STUDNET POSITIVE__")
  print(resp.json())
  context.status = resp.status_code
  context.response = resp.json()
  print("ADD_STUDENT RESPONSE _________",resp.json())


@behave.then("Section will be fetch using the given id and student is enrolled using student credentials and a response model object will be return")
def step_impl_3(context):
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "Check success"

# -----Negative Scenario-----


@behave.given("A user has access to portal and needs to enroll a student into a section")
def setp_impl_4(context):
  context.url = f'{API_URL}/sections/fake_id_data/students'
  context.payload = get_student_email_and_token()


@behave.when("API request is sent to enroll student to a section with correct request payload and invalid section id")
def step_impl_5(context):
  resp = requests.post(context.url, json=context.payload,headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("Student will not be enrolled and API will throw a resource not found error")
def step_impl_6(context):
  assert context.status == 404, "Status 404"
  assert context.response["success"] is False, "Check success"

# ----

@behave.given("A user has access to the portal and wants to enroll a student into a section")
def step_impl_7(context):
  context.url = f'{API_URL}/sections/{context.sections.id}/students'
  context.payload ={"email":"email@gmail.com","credentials":{"token":"token"}}


@behave.when("API request is sent to enroll student to a section with incorrect request payload and valid section id")
def step_impl_8(context):
  resp = requests.post(context.url, json=context.payload,headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("Student will not be enrolled and API will throw a validation error")
def step_impl_9(context):
  assert context.status == 422, "Status 422"
  assert context.response["success"] is False, "Check success"

# -----Positive Scenario--------


@behave.given("A user has access privileges and wants to enroll a student using his/her workspace email into a section")
def step_impl_10(context):
  print("FOR WORKSPACE EMAIL cohort ID")
  context.url = f'{API_URL}/cohorts/{context.cohort.id}/students'
  context.payload = get_workspace_student_email_and_token()


@behave.when("API request is sent to enroll workspace email as a student to a section with correct request payload and valid section id")
def step_impl_11(context):
  resp = requests.post(context.url, json=context.payload,
                       headers=context.header)
  print("THIS IS RESPONSE FOR WORKSPACE ",resp.json())
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("Section will be fetch using the given id and student is enrolled using student access token and his workspace email and a response model object will be return")
def step_impl_12(context):
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "Check success"

# -------------------------------enable notification to a course-------------------------------------
# ----Positive Scenario-----

@behave.given(
    "A user has access privileges and wants to enable notifications for a course"
)
def step_impl_13(context):
  context.url = f'{API_URL}/sections/enable_notifications'
  course=create_course(
        COURSE_TEMPLATE_INPUT_DATA["name"],"testing_section",
        COURSE_TEMPLATE_INPUT_DATA["description"])
  context.payload = {
      "course_id": course["id"],
      "feed_type": "COURSE_WORK_CHANGES"
  }


@behave.when(
    "API request is sent to enable notifications for a course with correct request payload which contains valid course id"
)
def step_impl_14(context):
  resp = requests.post(context.url,
                       json=context.payload,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Notifications will be enabled using unique course id and feed type and a response model object will be return"
)
def step_impl_15(context):
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "Check success"

# ----

@behave.given(
    "A user has access privileges and wants to enable notifications for a course using section id"
)
def step_impl_16(context):
  context.url = f'{API_URL}/sections/enable_notifications'
  context.payload = {
      "section_id": context.sections.id,
      "feed_type": "COURSE_WORK_CHANGES"
  }


@behave.when(
    "API request is sent to enable notifications for a course with correct request payload which contains valid section id"
)
def step_impl_17(context):
  resp = requests.post(context.url,
                       json=context.payload,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Notifications will be enabled using unique section id and feed type and a response model object will be return"
)
def step_impl_18(context):
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "Check success"

# -----Negative Scenario-----

@behave.given(
    "A user has access to portal and needs to enable notifications for a course using section id"
)
def step_impl_16(context):
  context.url = f'{API_URL}/sections/enable_notifications'
  context.payload = {
      "section_id": "fake_section_id",
      "feed_type": "COURSE_WORK_CHANGES"
  }


@behave.when(
    "API request is sent to enable notifications for a course with correct request payload which contains invalid section id"
)
def step_impl_17(context):
  resp = requests.post(context.url,
                       json=context.payload,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Notifications will not be enabled and API will throw a resource not found error"
)
def step_impl_18(context):
  assert context.status == 404, "Status 404"
  assert context.response["success"] is False, "Check success"

# ----

@behave.given(
    "A user has access to portal and needs to enable notifications for a course using payload"
)
def step_impl_19(context):
  context.url = f'{API_URL}/sections/enable_notifications'
  context.payload = {
      "section_id": "",
      "course_id": "",
      "feed_type": "COURSE_WORK_CHANGES"
  }


@behave.when(
    "API request is sent to enable notifications for a course with incorrect request payload"
)
def step_impl_20(context):
  resp = requests.post(context.url,
                       json=context.payload,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Notifications will not be enabled and API will throw a validation error"
)
def step_impl_21(context):
  assert context.status == 422, "Status 422"
  assert context.response["success"] is False, "Check success"
