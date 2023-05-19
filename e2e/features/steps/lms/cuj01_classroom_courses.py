import behave
import requests
from testing_objects.test_config import API_URL
from testing_objects.course_template import COURSE_TEMPLATE_INPUT_DATA
from environment import create_course

# -------------------------------Fetch All Courses-------------------------------------
# ----Positive Scenario-----


@behave.given(
    "A user has access privileges and needs to fetch all Courses Records"
)
def step_impl_01(context):
  context.url = f'{API_URL}/classroom_courses'


@behave.when(
    "API request is sent to fetch all Courses Records"
)
def step_impl_02(context):
  resp = requests.get(context.url, headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Classroom Courses API will return all existing Courses Records successfully"
)
def step_impl_03(context):
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "Check success"


# -------------------------------Copy Course-------------------------------------
# ----Positive Scenario-----
@behave.given(
    "A user has access privileges and wants to create a Copy of existing Classroom Course"
)
def step_impl_4(context):
  course = create_course(
      COURSE_TEMPLATE_INPUT_DATA["name"], "testing_section",
      COURSE_TEMPLATE_INPUT_DATA["description"])
  context.url = f'{API_URL}/classroom_courses/copy_course'
  context.payload = {
      "course_id": course["id"]
  }


@behave.when(
    "API request is sent to Copy Course with correct request payload"
)
def step_impl_5(context):
  resp = requests.post(
      url=context.url, json=context.payload, headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Existing course details will be fetch and using that details new course will be created and Copy course will send the details of new course"
)
def step_impl_6(context):
  print(f"____________Status:{context.status}_________________")
  print(f"____________Response:{context.response}_________________")
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "Check success"

# -------------------------------enable notification to a course-------------------------------------
# ----Positive Scenario-----

@behave.given(
    "A user has access privileges and wants to enable notifications for a course"
)
def step_impl_7(context):
  course = create_course(
      COURSE_TEMPLATE_INPUT_DATA["name"], "testing_section",
      COURSE_TEMPLATE_INPUT_DATA["description"])
  context.url = f'{API_URL}/classroom_courses/{course["id"]}/enable_notifications'
  


@behave.when(
    "API request is sent to enable notifications for a course using valid course id"
)
def step_impl_8(context):
  resp = requests.post(context.url,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Notifications will be enabled using unique course id and a response model object will be return"
)
def step_impl_9(context):
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "Check success"


# ----negative Scenario-----

@behave.given(
    "A user has access to portal and needs to enable notifications for a course"
)
def step_impl_10(context):
  context.url = f'{API_URL}/classroom_courses/fake_id/enable_notifications'


@behave.when(
    "API request is sent to enable notifications for a section using invalid course id"
)
def step_impl_11(context):
  resp = requests.post(context.url,
                      headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Course Notifications will not be enabled and API will throw a resource not found error"
)
def step_impl_12(context):
  assert context.status == 404, "Status 404"
  assert context.response["success"] is False, "Check success"

# -------------------------------Fetch Course by id-------------------------------------
# ----Positive Scenario-----


@behave.given(
    "A user has access privileges and needs to fetch Course Record"
)
def step_impl_13(context):
  context.course = create_course(
      COURSE_TEMPLATE_INPUT_DATA["name"], "retrieve section",
      COURSE_TEMPLATE_INPUT_DATA["description"])
  context.url = f'{API_URL}/classroom_courses/{context.course["id"]}'


@behave.when(
    "API request is sent to fetch Course Record using valid id"
)
def step_impl_14(context):
  resp = requests.get(context.url, headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Classroom Courses API will return existing Course Record by id successfully"
)
def step_impl_15(context):
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "Check success"
  assert context.response["data"]["id"] == context.course["id"], "Check course id"
  assert context.response["data"]["name"] == context.course["name"], "Check course name"

# ----Negative Scenario-----


@behave.given(
    "A user has access privileges and wants to fetch Course Record"
)
def step_impl_16(context):
  context.url = f'{API_URL}/classroom_courses/12345678'


@behave.when(
    "API request is sent to fetch Course Record using invalid id"
)
def step_impl_17(context):
  resp = requests.get(context.url, headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Classroom Courses API will throw an error course not found"
)
def step_impl_18(context):
  assert context.status == 404, "Status 404"
  assert context.response["success"] is False, "Check success"
