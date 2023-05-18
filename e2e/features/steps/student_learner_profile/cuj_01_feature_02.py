"""
Ingest skill graph from Credential Engine via API, break out skills and organize them in skill graph
"""

from setup import post_method, get_method, put_method, delete_method
from common.models import Learner
from test_object_schemas import LEARNER_OBJECT_TEMPLATE
import behave
import sys

sys.path.append("../")

from test_config import API_URL_LEARNER_PROFILE_SERVICE

API_URL = API_URL_LEARNER_PROFILE_SERVICE

#Scenario 1


@behave.given("Learner changed their personal infomation in the account.")
def step_impl_1(context):

  # Adding a learner
  learner_dict = {**LEARNER_OBJECT_TEMPLATE}
  learner_dict["email_address"] = "jondoe_c1f2s1@gmail.com"
  context.learner_payload = learner_dict
  context.learner_url = f"{API_URL}/learner"
  context.learner_post_res = post_method(
      url=context.learner_url, request_body=context.learner_payload)
  context.learner_post_res_data = context.learner_post_res.json()
  learner_id = context.learner_post_res_data["data"]["uuid"]

  context.url = f"{context.learner_url}/{learner_id}"

  new_learner_profile_dict = {}
  new_learner_profile_dict["preferred_first_name"] = "abc"
  new_learner_profile_dict["preferred_last_name"] = "def"
  new_learner_profile_dict["email_address"] = "abc.def@gmail.com"
  new_learner_profile_dict["organisation_email_id"] = "abc.def@foobar.com"
  context.updated_profile = new_learner_profile_dict

  # put request
  response = put_method(url=context.url, request_body=new_learner_profile_dict)
  assert response.status_code == 200, "Status 200"


@behave.when("Learner view their learner-facing profile interface.")
def step_impl_2(context):
  context.response = get_method(url=context.url)
  response = context.response.json()
  context.res_data = response


@behave.then(
    "the current information that is logged in the SLP is visible after it has been updated."
)
def step_impl_3(context):
  assert context.response.status_code == 200, "Status 200"
  assert context.res_data.get("success") is True, "Success not true"
  assert context.res_data.get(
      "message"
  ) == "Successfully fetched the learner", "Expected response not same"
  assert context.res_data.get("data").get(
      "preferred_first_name") == context.updated_profile.get(
          "preferred_first_name"), "Expected response not same"
  assert context.res_data.get("data").get(
      "preferred_last_name") == context.updated_profile.get(
          "preferred_last_name"), "Expected response not same"
  assert context.res_data.get("data").get(
      "email_address") == context.updated_profile.get(
          "email_address"), "Expected response not same"
  assert context.res_data.get("data").get(
      "organisation_email_id") == context.updated_profile.get(
          "organisation_email_id"), "Expected response not same"
  #delete learner
  delete_method(url=context.url)


#Scenario 2
@behave.given("Learner tries to update non-editable personal information")
def step_impl_4(context):

  # Adding a learner
  learner_dict = {**LEARNER_OBJECT_TEMPLATE}
  learner_dict["email_address"] = "jondoe_c1f2s2@gmail.com"
  learner_1 = Learner.from_dict(learner_dict)
  learner_1.save()
  learner_1.uuid = learner_1.id
  learner_id = learner_1.id
  learner_1.update()

  new_learner_profile_dict = {}
  new_learner_profile_dict["uuid"] = learner_id
  new_learner_profile_dict["first_name"] = "abc"
  context.updated_profile = new_learner_profile_dict
  context.learner_id = learner_id


@behave.when("the request is sent to SLP")
def step_impl_5(context):
  url = f"{API_URL}/learner"
  context.url = f"{url}/{context.learner_id}"
  # put request
  context.response = put_method(
      url=context.url, request_body=context.updated_profile)
  response = context.response.json()
  context.res_data = response


@behave.then(
    "SLP should return error message saying personal non-editable information cannot be updated."
)
def step_impl_6(context):
  assert context.response.status_code == 422, "Status 422"
  #delete learner
  delete_method(url=context.url)
