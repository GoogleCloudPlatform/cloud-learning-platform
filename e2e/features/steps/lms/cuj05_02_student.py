import uuid
import behave
import requests
from e2e.test_config import API_URL
from common.models import CourseEnrollmentMapping

# ------------------------------Delete student to Section-------------------------------------


@behave.given("A section has a students enrolled and has course enrollment mapping present")
def step_impl_1(context):
  context.url = f'{API_URL}/sections/{context.enroll_student_data["section_id"]}/students/{context.enroll_student_data["user_id"]}'


@behave.when("API request with valid section Id and user id is sent to delete student")
def step_impl_2(context):
  resp = requests.delete(context.url,headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("Student is marked as inactive in course enrollment mapping and removed from google classroom using user id")
def step_impl_3(context):
  assert context.status == 200, "Status 200"


#----delete using email---------

@behave.given("A user wants to remove a student from a section using email id")
def step_impl_4(context):
  context.url = f'{API_URL}/sections/{context.enroll_student_data["section_id"]}/students/{context.enroll_student_data["email"]}'


@behave.when("API request with valid section Id and email is sent to delete student")
def step_impl_5(context):
  resp = requests.delete(context.url, headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("Student is marked as inactive in course enrollment mapping and removed from google classroom using email id")
def step_impl_6(context):
  print(f"______DELETE USING EMAIL RESPONSE______:{context.response},{context.status}")
  if context.status!=200:
    print(f"Course Mapping: {CourseEnrollmentMapping.find_by_id(context.enroll_student_data['course_enrollment_mapping_id']).to_dict()}")
  assert context.status == 200, "Status 200"

#----Negative delete using email---------

@behave.given("A user has access to portal and wants to remove a student from a section using invalid email id")
def step_impl_7(context):
  context.url = f'{API_URL}/sections/{context.sections.id}/students/xyz@gmail.com'


@behave.when("API request with valid section Id and Invalid email is sent to delete student")
def step_impl_8(context):
  resp = requests.delete(context.url, headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("API returns student not found in this section error")
def step_impl_9(context):
  print(f"______DELETE USING EMAIL RESPONSE______:{context.response},{context.status}")
  assert context.status == 404, "Status 404"
  
# -----------------------------------------Student difference detailed report---------------------------------
# ---exists in classrooom not in db-----------
@behave.given("A user has access to portal and wants to fetch the list of students exists in Classroom not in DB")
def step_impl_10(context):
  context.url = f'{API_URL}/student/exists_in_classroom_not_in_db'


@behave.when("API request is sent to get the list of students")
def step_impl_11(context):
  resp = requests.get(context.url, headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("List of students details will be fetched from bq views")
def step_impl_12(context):
  print(f'--------------Status: {context.status}--------------------')
  print(f'--------------Data: {context.response}--------------------')
  assert context.status == 200, "Status 200"
  assert context.response["data"] !=[]

# ---exists in db not in classroom-----------
@behave.given("A user has access to portal and wants to fetch the list of students exists in DB not in classroom")
def step_impl_13(context):
  context.url = f'{API_URL}/student/exists_in_db_not_in_classroom'


@behave.when("API request is sent to fetch the list of students records")
def step_impl_14(context):
  resp = requests.get(context.url, headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("List of student records will be fected from bq views")
def step_impl_15(context):
  print(f'--------------Status: {context.status}--------------------')
  print(f'--------------Data: {context.response}--------------------')
  assert context.status == 200, "Status 200"
  assert context.response["data"] !=[]