import os
import behave
import requests
from e2e.test_config import API_URL
from e2e.utils.course_template import COURSE_TEMPLATE_INPUT_DATA
from environment import create_course,wait
from common.utils.bq_helper import run_query
PROJECT_ID = os.getenv("PROJECT_ID", "")
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
BQ_DATASET = DATABASE_PREFIX +  "lms_analytics"
# -------------------------------Roaster Changes-------------------------------------

@behave.given(
    "A user has been added to classroom as a student"
)
@wait(60)
def step_impl_01(context):
  context.user_id=context.analytics_data['student_data']['email']
  context.course_id=context.analytics_data['student_data']['classroom_id']


@behave.when(
    "Pipline got messages related to roster changes"
)
def step_impl_02(context):
  q1 = f"select * from `{PROJECT_ID}.{BQ_DATASET}.lms-notifications` where JSON_VALUE(data.email)=\"{context.user_id}\""
  q2=f"select * from {PROJECT_ID}.{BQ_DATASET}.userCollectionView where emailAddress=\"{context.user_id}\""
  print(f"q1:---{q1},q2:----{q2}")
  qurey_result=run_query(q2
    )
  noti_query_result = run_query(q1
  )
  context.users=[dict(row) for row in qurey_result]
  context.notification=[dict(row) for row in noti_query_result]


@behave.then(
    "Pipline get user related details from classroom and store user details and Push filter message to lms notifications"
)
def step_impl_03(context):
  user=context.users[0]
  message = context.notification[0]
  assert user["id"]==context.analytics_data["student_data"]["gaia_id"]
  print(
      f'-----------------{context.notification}---{len(context.notification)}--------'
  )
  print(f'-----------------{message["data"]["email"]}-----------')

# -------------------------------Course Work Changes-------------------------------------

@behave.given(
    "A teacher created a course work"
)
def step_impl_04(context):
  context.course_work_id=context.analytics_data['course_work']['id']
  context.user_id = context.analytics_data['student_data']['email']


@behave.when(
    "Pipline got messages related to create Course work"
)
def step_impl_05(context):
  qurey_result=run_query(f"select * from {PROJECT_ID}.{BQ_DATASET}.courseWorkCollectionView where id=\"{context.course_work_id}\"")
  context.course_work=[dict(row) for row in qurey_result]


@behave.then(
    "Pipline get course work details from classroom and store course work details and Push filter message to lms notifications"
)
def step_impl_06(context):
  course_work=context.course_work[0]
  assert course_work["courseId"]==context.analytics_data["course_work"]["courseId"]
  assert course_work["title"]==context.analytics_data["course_work"]["title"]

  # -------------------------------Submitted Course Work Changes-------------------------------------

@behave.given(
    "A student submitted a course work"
)
def step_impl_07(context):
  context.submission_id=context.analytics_data['submission']['id']


@behave.when(
    "Pipline got messages related to Submitted Course work"
)
def step_impl_08(context):
  qurey_result=run_query(f"select * from {PROJECT_ID}.{BQ_DATASET}.submittedCourseWorkCollectionView where submission_id=\"{context.submission_id}\"")
  noti_query_result = run_query(
      f"select * from {PROJECT_ID}.{BQ_DATASET}.lms-notifications where JSON_VALUE(data.email)=\"{context.user_id}\""
  )
  context.submission=[dict(row) for row in qurey_result][0]
  context.notification=[dict(row) for row in noti_query_result]


@behave.then(
    "Pipline get submitted course work details from classroom and store Submitted Course Work details and Push filter message to lms notifications"
)
def step_impl_09(context):
  assert context.submission["submission_course_id"]==context.analytics_data["course_details"]["id"]
  assert context.submission["submission_course_work_id"]==context.analytics_data["course_work"]["id"]
  assert context.submission["submission_user_id"]==context.analytics_data["student_data"]["gaia_id"]
  # assert context.notification[0]["data"]["email"]==context.user_id