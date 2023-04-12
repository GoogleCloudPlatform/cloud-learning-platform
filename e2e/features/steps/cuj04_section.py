import uuid
import behave
import requests
from testing_objects.test_config import API_URL
from testing_objects.course_template import COURSE_TEMPLATE_INPUT_DATA 
from testing_objects.user import TEST_USER
from e2e.gke_api_tests.secrets_helper import get_student_email_and_token,get_workspace_student_email_and_token
from environment import create_course

# -------------------------------Enroll student to cohort-------------------------------------
# ----Positive Scenario-----


@behave.given("A user has access privileges and wants to enroll a student into a cohort")
def step_impl_1(context):
  # context.url = f'{API_URL}/sections/{context.sections.id}/students'
  context.url = f'{API_URL}/cohorts/{context.cohort.id}/students'
  context.payload = get_student_email_and_token()



@behave.when("API request is sent to enroll student to a section with correct request payload and valid cohort id")
def step_impl_2(context):
  resp = requests.post(context.url, json=context.payload,headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("Section will be fetch using the given id and student is enrolled using student credentials and a response model object will be return")
def step_impl_3(context):
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "Check success"

# -----Negative Scenario-----


@behave.given("A user has access to portal and needs to enroll a student into a cohort")
def setp_impl_4(context):
  context.url = f'{API_URL}/cohorts/fake_id_data/students'
  context.payload = get_student_email_and_token()


@behave.when("API request is sent to enroll student to a section with correct request payload and invalid cohort id")
def step_impl_5(context):
  resp = requests.post(context.url, json=context.payload,headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("Student will not be enrolled and API will throw a resource not found error")
def step_impl_6(context):
  assert context.status == 404, "Status 404"
  assert context.response["success"] is False, "Check success"

# ----

@behave.given("A user has access to the portal and wants to enroll a student into a cohort")
def step_impl_7(context):
  context.url = f'{API_URL}/cohorts/{context.cohort.id}/students'
  context.payload ={"email":"email@gmail.com","credentials":{"token":"token"}}


@behave.when("API request is sent to enroll student to a section with incorrect request payload and valid cohort id")
def step_impl_8(context):
  resp = requests.post(context.url, json=context.payload,headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("Student will not be enrolled and API will throw a validation error")
def step_impl_9(context):
  assert context.status == 422, "Status 422"
  assert context.response["success"] is False, "Check success"

# -----Positive Scenario--------


@behave.given("A user has access privileges and wants to enroll a student using his/her workspace email into a cohort")
def step_impl_10(context):
  context.url = f'{API_URL}/cohorts/{context.cohort.id}/students'
  context.payload = get_workspace_student_email_and_token()


@behave.when("API request is sent to enroll workspace email as a student to a cohort with correct request payload and valid cohort id")
def step_impl_11(context):
  resp = requests.post(context.url, json=context.payload,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("Section will be fetch using the given id and student is enrolled using student access token and his workspace email and a response model object will be return")
def step_impl_12(context):
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "Check success"

# -------------------------------enable notification to a course-------------------------------------
# ----Positive Scenario-----

@behave.given(
    "A user has access privileges and wants to enable notifications for a section"
)
def step_impl_13(context):
  context.url = f'{API_URL}/sections/{context.sections.id}/enable_notifications'

@behave.when(
    "API request is sent to enable notifications for a section using valid section id"
)
def step_impl_14(context):
  resp = requests.post(context.url,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Notifications will be enabled using unique section id and a response model object will be return"
)
def step_impl_15(context):
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "Check success"

# -----Negative Scenario-----

@behave.given(
    "A user has access to portal and needs to enable notifications for a section"
)
def step_impl_16(context):
  context.url = f'{API_URL}/sections/fake_section_id/enable_notifications'

@behave.when(
    "API request is sent to enable notifications for a section using invalid section id"
)
def step_impl_17(context):
  resp = requests.post(context.url,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Notifications will not be enabled and API will throw a resource not found error"
)
def step_impl_18(context):
  assert context.status == 404, "Status 404"
  assert context.response["success"] is False, "Check success"


# -------------------------------Retrieve assignment-------------------------------------
# ----Positive Scenario-----

@behave.given(
    "A user has access to portal and needs to retrieve a assignment using section id and assignment id"
)
def step_impl_19(context):
  context.url = f'{API_URL}/sections/{context.assignment["section_id"]}/assignments/{context.assignment["id"]}'


@behave.when(
    "API request is sent to retrieve assignment details of a section with correct section id and assignment id"
)
def step_impl_20(context):
  resp = requests.get(context.url,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Assignment Record corresponding to given assignment id will be returned successfully"
)
def step_impl_21(context):
  assert context.status == 200, "Status 200"
  assert context.response["id"] == context.assignment["id"], "Data id doesn't Match"
  assert context.response["classroom_id"] == context.assignment["courseId"], "Data classroom id doesn't Match"
  assert context.response["title"] == context.assignment["title"], "Data title doesn't Match"

#----Negative scenario-------


@behave.given(
    "A user has access to admin portal and wants to retrieve a assignment using assignment id and section id"
)
def setp_impl_22(context):
  context.url = f'{API_URL}/sections/fake_section_id/assignments/fake_assignment_id'


@behave.when(
    "API request is sent to retrieve assignment details by providing invalid section id"
)
def step_impl_23(context):
  resp = requests.get(context.url, headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Assignment details will not be returned and API will throw a resource not found error"
)
def step_impl_24(context):
  assert context.status == 404, "Status 404"
  assert context.response["success"] is False, "Check success"

# -------------------------------List teachers in section-------------------------------------
# ----Positive Scenario-----

@behave.given(
    "A user has access to admin portal and needs to retrieve the list of teachers with vailid section id"
)
def step_impl_31(context):
  context.url = f'{API_URL}/sections/{context.sections.id}/teachers'


@behave.when(
    "API request is sent which contains valid section id"
)
def step_impl_32(context):
  resp = requests.get(context.url,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "List of teachers will be given with there details"
)
def step_impl_33(context):
  assert context.status == 200, "Status 200"
  assert context.response["success"] == True, "Success status doesn't match"
  assert context.response["data"][0]["user_type"] == "faculty", "User type faculty doesn't match"

# -------------------------------List teachers in section negative -------------------------------------
# ----Positive Scenario-----

@behave.given(
    "A user has access to admin portal and needs to retrieve the list of teachers with invailid section id"
)
def step_impl_34(context):
  context.url = f'{API_URL}/sections/invalid_id/teachers'


@behave.when(
    "API request is sent which contains invalid section id"
)
def step_impl_35(context):
  resp = requests.get(context.url,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Section not found error is sent in response"
)
def step_impl_36(context):
  assert context.status == 404, "Status 404"

# -------------------------------Get teachers in section Positive-------------------------------------
# ----Positive Scenario-----

@behave.given(
    "A user has access to admin portal and needs to retrieve the details teacher with vailid section id and teacher_email"
)
def step_impl_37(context):
  context.url = f'{API_URL}/sections/{context.sections.id}/teachers/teachera@gmail.com'


@behave.when(
    "API request is sent which contains valid section id and teacher email"
)
def step_impl_38(context):
  resp = requests.get(context.url,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()

@behave.then(
    "Get the details of teacher from user collection"
)
def step_impl_39(context):
  assert context.status == 200, "Status 200"

# -----------------------------------Import grade coursework- Positive-------------------------------

@behave.given(
    "A teacher has access to portal and wants to  update grades of student for a coursework with form quize of a section"
)
def step_impl_40(context):
  context.url = f'{API_URL}/sections/{context.sections.id}/coursework/{context.coursework["id"]}'
  print("CONTEXT URL for import grade",context.url)

@behave.when(
    "API request is sent which has valid section_id and coursework_id"
)
def step_impl_41(context):
  resp = requests.post(context.url,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()
  print("Response of Import grade api ",context.response)

@behave.then(
    "Student grades updated in classroom"
)
def step_impl_42(context):
  assert context.status == 200, "Status 200"
  assert context.response["count"] == 1, "count not matching of update"


