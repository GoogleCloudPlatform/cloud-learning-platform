import datetime
import behave
import requests
from e2e.test_config import API_URL
from environment import wait


#---------------------------lms-notifications replay---------------
@behave.given(
    "A user has access to the portal and wants to replay all messages")
@wait(60)
def step_impl_01(context):
  context.url = f'{API_URL}/lms-notifications/replay'
  start_datetime= datetime.datetime.utcnow() - datetime.timedelta(minutes=15)
  context.payload = {
      "start_date": start_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
      "end_date": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
  }


@behave.when("API request is send replay lms-notification using valid start-date end-date"
             )
def step_impl_02(context):

  resp = requests.post(context.url, headers=context.header,
                       json=context.payload)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Messages will be fetch from Big query and send to the Pub/Sub")
def step_impl_03(context):
  assert context.status == 202, "Status 202"
