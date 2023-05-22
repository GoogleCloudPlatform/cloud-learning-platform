import behave
import requests
from testing_objects.test_config import API_URL
from testing_objects.course_template import COURSE_TEMPLATE_INPUT_DATA, DATABASE_PREFIX, emails


# -------------------------------CREATE Course Template-------------------------------------
# ----Positive Scenario-----
@behave.given(
    "A user has access privileges and needs to create a Course Template Record"
)
def step_impl_1(context):
  context.url = f'{API_URL}/course_templates'
  context.payload = COURSE_TEMPLATE_INPUT_DATA


@behave.when(
    "API request is sent to create Course Template Record with correct request payload"
)
def step_impl_2(context):
  resp = requests.post(url=context.url,
                       json=context.payload,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Course Template Record will be created in a third party tool and classroom master course will be create with provided payload and all metadata will be ingested and stored in Cousre Template service and id for learning experiences will be stored in Cousre Template service"
)
def step_impl_3(context):
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "Check success"
  assert context.response["course_template"]["classroom_code"] not in [
      "", None
  ], "Course Template classroom check"
  assert context.response["course_template"]["id"] not in [
      "", None
  ], "Course Template Firebase check"


# ----Negative Scenario-----


@behave.given(
    "A user has access to admin portal and wants to create a Course Template Record"
)
def step_impl_4(context):
  context.url = f'{API_URL}/course_templates'
  context.payload = {"name": "e2e_test_cases"}


@behave.when(
    "API request is sent to create Course Template Record with incorrect request payload"
)
def step_impl_5(context):
  resp = requests.post(context.url,
                       json=context.payload,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Course Template Record Record will not be created and Course Template API will throw a validation error"
)
def step_impl_6(context):
  assert context.status == 422, "Status 422"
  assert context.response["success"] is False, "Check success"


# -------------------------------Retrieve Course Template-------------------------------------
# ----Positive Scenario-----
@behave.given(
    "A user has access privileges and needs to retrieve a Course Template Record"
)
def setp_impl_7(context):
  COURSE_TEMPLATE_INPUT_DATA["id"] = context.course_template.id
  COURSE_TEMPLATE_INPUT_DATA[
      "classroom_id"] = context.course_template.classroom_id
  COURSE_TEMPLATE_INPUT_DATA[
      "classroom_code"] = context.course_template.classroom_code
  COURSE_TEMPLATE_INPUT_DATA[
      "classroom_url"] = context.course_template.classroom_url
  COURSE_TEMPLATE_INPUT_DATA["admin"] = context.course_template.admin
  context.test_data = COURSE_TEMPLATE_INPUT_DATA
  context.url = f'{API_URL}/course_templates/{context.course_template.id}'


@behave.when(
    "API request is sent to retrieve Course Template Record by providing correct id"
)
def step_impl_8(context):
  resp = requests.get(context.url, headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Course Template Record corresponding to given id will be returned successfully"
)
def step_impl_9(context):
  assert context.status == 200, "Status 200"
  assert context.response == context.test_data, "Data doesn't Match"


# ----Negative Scenario-----


@behave.given(
    "A user has access to admin portal and wants to retrieve a Course Template Record"
)
def setp_impl_10(context):
  context.url = f'{API_URL}/course_templates/fake_non_exist_id'


@behave.when(
    "API request is sent to retrieve Course Template Record by providing invalid id"
)
def step_impl_11(context):
  resp = requests.get(context.url, headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Course Template Record will not be returned and API will throw a resource not found error"
)
def step_impl_12(context):
  assert context.status == 404, "Status 404"
  assert context.response["success"] is False, "Check success"


# -------------------------------Update Course Template-------------------------------------
# ----Positive Scenario-----


@behave.given(
    "A user has access privileges and needs to update a Course Template Record"
)
def setp_impl_13(context):
  context.url = f'{API_URL}/course_templates/{context.course_template.id}'
  context.payload = {
      "name": f"{DATABASE_PREFIX}test_course_updated_name",
      "description": "updated_description"
  }


@behave.when(
    "API request is sent to update Course Template Record by providing correct id and request payload"
)
def step_impl_14(context):
  resp = requests.patch(context.url,
                        json=context.payload,
                        headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("Course Template Record will be updated successfully")
def step_impl_15(context):
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "Check success"
  assert context.response["course_template"]["name"] == context.payload[
      "name"], "Check updated data"
  assert context.response["course_template"]["description"] == context.payload[
      "description"], "Check updated data"


# ----Negative Scenario-----


@behave.given(
    "A user has access to admin portal and wants to update a Course Template Record"
)
def setp_impl_16(context):
  context.url = f'{API_URL}/course_templates/fake_non_exist_id'
  context.payload = {
      "name": "updated_name",
      "description": "updated_description"
  }


@behave.when(
    "API request is sent to delete Course Template Record by providing invalid id and valid payload"
)
def step_impl_17(context):
  resp = requests.patch(context.url,
                        json=context.payload,
                        headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Course Template Record will not be update and API will throw a resource not found error"
)
def step_impl_18(context):
  assert context.status == 404, "Status 404"
  assert context.response["success"] is False, "Check success"


# -------------------------------Delete Course Template-------------------------------------
# ----Positive Scenario-----
@behave.given(
    "A user has access privileges and needs to delete a Course Template Record"
)
def setp_impl_19(context):
  context.url = f'{API_URL}/course_templates/{context.course_template.id}'


@behave.when(
    "API request is sent to delete Course Template Record by providing correct id"
)
def step_impl_20(context):
  resp = requests.delete(context.url, headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("Course Template Record will be deleted successfully")
def step_impl_21(context):
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "Check success"


# ----Negative Scenario-----


@behave.given(
    "A user has access to admin portal and wants to delete a Course Template Record"
)
def setp_impl_22(context):
  context.url = f'{API_URL}/course_templates/fake_non_exist_id'


@behave.when(
    "API request is sent to delete Course Template Record by providing invalid id"
)
def step_impl_23(context):
  resp = requests.delete(context.url, headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Course Template Record will not be deleted and API will throw a resource not found error"
)
def step_impl_24(context):
  assert context.status == 404, "Status 404"
  assert context.response["success"] is False, "Check success"


# -------------------------------Fetch All Course Templates-------------------------------------


@behave.given(
    "A user has access privileges and needs to fetch all Course Template Records"
)
def step_impl_25(context):
  context.url = f'{API_URL}/course_templates'


@behave.when("API request is sent to fetch all Course Template Records")
def step_impl_26(context):
  resp = requests.get(context.url, headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Course Template API will return all existing Course Template Records successfully"
)
def step_impl_27(context):
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "Check success"


# -------------------------------Fetch All Cohort by Course Templates-------------------------------------
# ----Positive Scenario-----


@behave.given(
    "A user has access privileges and needs to fetch all Cohort Records using course template"
)
def step_impl_28(context):
  context.url = f'{API_URL}/course_templates/{context.cohort.course_template.id}/cohorts'


@behave.when(
    "API request is sent to fetch all Cohorts Records by providing Course template valid id"
)
def step_impl_29(context):
  resp = requests.get(context.url, headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Course Template list Cohort API will return all existing Cohort Records successfully"
)
def step_impl_30(context):
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "Check success"


# ----Negative Scenario-----


@behave.given(
    "A user has access to admin portal and wants to retrieve list of Cohort Records using course template"
)
def setp_impl_31(context):
  context.url = f'{API_URL}/course_templates/fake_non_exist_id'


@behave.when(
    "API request is sent to fetch all Cohorts Records by providing Course template invalid id"
)
def step_impl_32(context):
  resp = requests.delete(context.url, headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Course Template list Cohort API will throw a resource not found error")
def step_impl_33(context):
  assert context.status == 404, "Status 404"
  assert context.response["success"] is False, "Check success"


#-----------------------------------Delete teacher from section--------------------------------------
#---Positive scenario


@behave.given(
    "A user has access to admin portal and needs to delete the instructional designer with valid course template id and email"
)
def step_impl_34(context):
  context.url = f'{API_URL}/course_templates/{context.enrollment_mapping.course_template.id}/instructional_designers/{context.enrollment_mapping.user.email}'


@behave.when(
    "Delete request is sent which contains valid course template id and email")
def step_impl_35(context):
  resp = requests.delete(context.url, headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Set inactive instructional designer from enrollment mapping collection")
def step_impl_36(context):
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "check data"


#---negative scenario


@behave.given(
    "A user has access privileges wants to delete instructional designer with valid course template id and invalid indtructional designer id"
)
def step_impl_37(context):
  context.url = f'{API_URL}/course_templates/{context.course_template.id}/instructional_designers/12345678'


@behave.when(
    "API request is sent which contains valid course template id and invalid user id to delete instructional designer"
)
def step_impl_38(context):
  resp = requests.get(context.url, headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("Delete instructional designer API throw user not found error")
def step_impl_39(context):
  assert context.status == 404, "Status 404"
  assert context.response["success"] is False, "Check Data"


#---------------------------------Enroll teacher in a section-------------
@behave.given(
    "A user has access privileges wants to enroll the instructional designer using valid section id and email"
)
def step_impl_40(context):
  context.url = f'{API_URL}/course_templates/{context.course_templates.id}/instructional_designers'
  context.payload = {"email": emails["teacher"]}


@behave.when(
    "Post request is sent which contains valid course template id and payload which contains valid email"
)
def step_impl_41(context):
  resp = requests.post(context.url,
                       headers=context.header,
                       json=context.payload)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "The instruction designer enrolled in classroom and a enrollment mapping is created and return user details with enrollment details"
)
def step_impl_42(context):
  print(f"--------------------json: {context.payload}-----------------------")
  print(f"------------------Status: {context.status}------------------------")
  print(f"------------------data: {context.response}------------------------")
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "Check Data"
