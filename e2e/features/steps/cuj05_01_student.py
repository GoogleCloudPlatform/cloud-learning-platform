import uuid
import behave
import requests
from testing_objects.test_config import API_URL
from e2e.gke_api_tests.secrets_helper import get_student_email_and_token

# ------------------------------list student to Section-------------------------------------



@behave.given("A section has a students enrolled")
def step_impl_1(context):
  context.url = f'{API_URL}/sections/{context.enroll_student_data["section_id"]}/students'


@behave.when("API request with valid section Id is sent")
def step_impl_2(context):
  resp = requests.get(context.url,headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()

@behave.then("Section will be fetch using the given id and list of studnets enrolled")
def step_impl_3(context):
    assert context.status == 200, "Status 200"





#-------------------------------Get student in cohort--------------------------------------
@behave.given("A section has a students enrolled in cohort")
def step_impl_10(context):
  context.url = f'{API_URL}/cohorts/{context.enroll_student_data["cohort_id"]}/students/{context.enroll_student_data["user_id"]}'

@behave.when("API request with valid cohort Id  user_id is sent")
def step_impl_11(context):
  resp = requests.get(context.url,headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()

@behave.then("student details will be fetch using the given id for cohort")
def step_impl_12(context):
    assert context.status == 200, "Status 200"
    assert context.response["data"]["cohort_id"] == context.enroll_student_data["cohort_id"]

#------------------------------Invite student to section------------------------------
@behave.given("A user is invited to a section using email")
def step_impl_13(context):
  student_email =get_student_email_and_token()
  context.url = f'{API_URL}/sections/{context.sections.id}/invite/{student_email["invite_student_email"]}'



@behave.when("API request is sent with valid section id and email")
def step_impl_14(context):
  resp = requests.post(context.url,headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("Invitation is sent to student via email and course enrollmet object with status invited is created")
def step_impl_15(context):
  assert context.status == 200, "Status 200"
  assert "invitation_id" in context.response["data"].keys()

#-------------------------------Update invites patch api--------------------------------------
@behave.given("A student is invited and has not accepted the invite via email")
def step_impl_16(context):
  context.url = f'{API_URL}/sections/update_invites'

@behave.when("cron job is triggered and calls update_invites endpoint")
def step_impl_17(context):
  resp = requests.patch(context.url,headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()

@behave.then("student details will be updated in user collection and course enrollment mapping once invite is accepted")
def step_impl_18(context):
    assert context.status == 200, "Status 200"

#------------------------------Invite student to cohort------------------------------
@behave.given("A user is invited to a cohort_id using email")
def step_impl_19(context):
  student_email =get_student_email_and_token()
  context.url = f'{API_URL}/cohorts/{context.sections.cohort.id}/invite/{student_email["invite_student_email"]}'



@behave.when("API request is sent with valid cohort id and email")
def step_impl_20(context):
  resp = requests.post(context.url,headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()



@behave.then("Invitation is sent to student via email and student invited to section with min enrolled student count")
def step_impl_21(context):
  print("This is invite student to cohort response code", context.status,context.response)
  assert context.status == 200, "Status 200"
  assert "invitation_id" in context.response["data"].keys()

# --------------------------------Enroll student to section-------------------------------


@behave.given("A user has access privileges and wants to enroll a student into a section")
def step_impl_22(context):
  context.url = f'{API_URL}/sections/{context.sections.id}/students'
  student_details = get_student_email_and_token()
  context.payload = {"email":student_details["email"],"access_token":student_details["access_token"]}



@behave.when("API request is sent to enroll student to a section with correct request payload and valid section id")
def step_impl_23(context):
  resp = requests.post(context.url, json=context.payload,headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("Student is enrolled in given section")
def step_impl_24(context):
  print("Enroll student to section payload",context.status,context.response)
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "Check success"

# Negative scenario invalid section id

@behave.given("A user has access to portal and needs to enroll a student into a section")
def setp_impl_25(context):
  context.url = f'{API_URL}/sections/fake_id_data/students'
  context.payload = get_student_email_and_token()


@behave.when("API request is sent to enroll student to a section with correct request payload and invalid section id")
def step_impl_26(context):
  resp = requests.post(context.url, json=context.payload,headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("Student is not enrolled and api returns section not found error")
def step_impl_27(context):
  assert context.status == 404, "Status 404"
  assert context.response["success"] is False, "Check success"

# Negative scenario incorrect request payload
@behave.given("A user has access to the portal and wants to enroll a student into a section")
def step_impl_28(context):
  context.url = f'{API_URL}/sections/{context.sections.id}/students'
  context.payload ={"email":"email@gmail.com","credentials":{"token":"token"}}


@behave.when("API request is sent to enroll student to a section with incorrect request payload and valid section id")
def step_impl_29(context):
  resp = requests.post(context.url, json=context.payload,headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("Student will not be enrolled and API will throw a validation error for request body")
def step_impl_30(context):
  assert context.status == 422, "Status 422"
  assert context.response["success"] is False, "Check success"

# Negative scenario student is already enrolled and trying to enroll again
@behave.given("A student is aleardy enrolled in course and trying to enroll in same course")
def step_impl_31(context):
  section_id = context.enroll_student_data["section_id"]
  student_email = context.enroll_student_data["email"]
  access_token = context.enroll_student_data["access_token"]
  context.url = f'{API_URL}/sections/{section_id}/students'
  context.payload = {"email": student_email,"access_token":access_token}


@behave.when("API request is sent to enroll student to a section with valid section id")
def step_impl_32(context):

  resp = requests.post(context.url, json=context.payload,headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("Student will not be enrolled and API will throw a conflict error")
def step_impl_33(context):
  print("A student is aleardy enrolled in course and trying to enroll in same course",context.status,context.response)
  assert context.status == 409, "Status 409"
  assert context.response["success"] is False, "Checks failure"



