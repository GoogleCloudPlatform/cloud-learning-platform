import behave
import requests
from testing_objects.test_config import API_URL
from environment import wait

#----------Positive---------------
@behave.given("A user has access to the portal and wants student analytics data")
@wait(20)
def step_impl_01(context):
  context.email=context.analytics_data['student_data']['email']
  context.url=f'{API_URL}/analytics/students/{context.email}'


@behave.when("API request is send get analytics data using valid student email")
def step_impl_02(context):

  resp = requests.get(context.url,headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("Analytics data will be fetch from Big query view using student email")
def step_impl_03(context):
  assert context.status == 200, "Status 200"
  assert context.response["user"]["user_email_address"]== context.analytics_data['student_data']['email'],"Check Data"
  assert context.response["user"]["user_gaia_id"]== context.analytics_data['student_data']["gaia_id"],"Check Data"
  assert context.response["section_list"][0]["course_work_list"][0]["course_work_id"]== context.analytics_data["submission"]["courseWorkId"],"Check Data"
  assert context.response["section_list"][0]["course_work_list"][0]["submission_id"]== context.analytics_data["submission"]["id"],"Check Data"


@behave.given("A user has access privileges and wants to get student analytics data")
def step_impl_04(context):
  context.user_id=context.analytics_data["student_data"]["user_id"]
  context.url = f'{API_URL}/analytics/students/{context.user_id}'

@behave.when("API request is send get analytics data using valid student id")
def step_impl_05(context):

  resp = requests.get(context.url, headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()

@behave.then("Get student email using user API and using that email analytics data will be fetch from bq view")
def step_impl_06(context):
  assert context.status == 200, "Status 200"
  assert context.response["user"]["user_email_address"]== context.analytics_data['student_data']['email'],"Check Data 1"
  assert context.response["user"]["user_gaia_id"]== context.analytics_data['student_data']["gaia_id"],"Check Data 2"
  assert context.response["section_list"][0]["course_work_list"][0]["course_work_id"]== context.analytics_data["submission"]["courseWorkId"],"Check Data 3"
  assert context.response["section_list"][0]["course_work_list"][0]["submission_id"]== context.analytics_data["submission"]["id"],"Check Data 4"
  

#----------Negative---------------

@behave.given("A user has access privileges to the portal and wants to get student analytics data")
def step_impl_07(context):
  context.url = f'{API_URL}/analytics/students/dfg2345'

@behave.when("API request is send get analytics data using invalid student id")
def step_impl_08(context):

  resp = requests.get(context.url,headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("API throw not found error")
def step_impl_09(context):
  assert context.status == 404, "Status 404"
  assert context.response["success"] is False, "Checks failure"


@behave.given("A user has access to the portal and wants to get student analytics data")
def step_impl_10(context):
  
  context.url = f'{API_URL}/analytics/students/xyz@gmail.com'

@behave.when("API request is send get analytics data using invalid student email")
def step_impl_11(context):
  resp = requests.get(context.url,headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("API will throw user not found by this id error")
def step_impl_12(context):
  assert context.status == 404, "Status 404"
  assert context.response["success"] is False, "Checks failure"


