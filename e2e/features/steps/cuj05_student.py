import uuid
import behave
import requests
from testing_objects.test_config import API_URL
from testing_objects.course_template import COURSE_TEMPLATE_INPUT_DATA
from environment import create_course

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

# ------------------------------Delete student to Section-------------------------------------


@behave.given("A section has a students enrolled and has course enrollment mapping present")
def step_impl_4(context):
  context.url = f'{API_URL}/sections/{context.enroll_student_data["section_id"]}/students/{context.enroll_student_data["user_id"]}'


@behave.when("API request with valid section Id and user id is sent to delete student")
def step_impl_5(context):
  resp = requests.delete(context.url,headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("Student is marked as inactive in course enrollment mapping and removed from google classroom using user id")
def step_impl_6(context):
  assert context.status == 200, "Status 200"


#----delete using email---------

@behave.given("A user wants to remove a student from a section using email id")
def step_impl_7(context):
  context.url = f'{API_URL}/sections/{context.enroll_student_data["section_id"]}/students/{context.enroll_student_data["email"]}'


@behave.when("API request with valid section Id and email is sent to delete student")
def step_impl_8(context):
  resp = requests.delete(context.url, headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("Student is marked as inactive in course enrollment mapping and removed from google classroom using email id")
def step_impl_9(context):
  print(f"______DELETE USING EMAIL RESPONSE______:{context.response},{context.status}")
  assert context.status == 200, "Status 200"
  