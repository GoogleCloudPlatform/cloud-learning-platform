"""
Learner can track current employer information in student learner profile
"""
import behave
import sys
from copy import copy

sys.path.append("../")
from e2e.test_object_schemas import LEARNER_OBJECT_TEMPLATE
from e2e.test_config import API_URL_LEARNER_PROFILE_SERVICE
from e2e.setup import post_method, get_method, delete_method

API_URL = API_URL_LEARNER_PROFILE_SERVICE

# --------------------------- Positive ----------------------------------

@behave.given("A learner is employed by a sponsoring employer partner")
def step_impl_1(context):
  """Defining the payload required for creating a learner account along with the employer details"""
  learner_dict = copy(LEARNER_OBJECT_TEMPLATE)
  learner_dict["email_address"] = "jondoe_c1f1s1@gmail.com"
  context.payload = learner_dict
  context.url = f"{API_URL}/learner"


@behave.when("The Learner Account is created")
def step_impl_2(context):
  """Creating the learner account with the provided payload"""
  context.post_res = post_method(url=context.url, request_body=context.payload)
  context.post_res_data = context.post_res.json()


@behave.then(
    "the employer information (name, address, and contact info) is ingested into the SLP from the SNHU admin Salesforce record of the learner account"
)
def step_impl_3(context):
  """Validating the employer information when the learner account is created"""
  assert context.post_res.status_code == 200
  assert context.post_res_data.get("success") is True
  assert context.post_res_data.get(
      "message") == "Successfully created the learner"
  assert context.post_res_data.get("data").get(
      "employer_id") == context.payload.get("employer_id")
  assert context.post_res_data.get("data").get(
      "employer") == context.payload.get("employer")
  assert context.post_res_data.get("data").get(
      "employer_email") == context.payload.get("employer_email")

  context.get_req_path_param = context.post_res_data.get("data").get("uuid")


@behave.then(
    "made visible to the learner through the learner-facing profile interface.")
def step_impl_4(context):
  """Validating the employer information when the learner access the learner information"""
  context.get_res = get_method(url=context.url + "/" +
                               context.get_req_path_param)
  context.get_res_data = context.post_res.json()
  assert context.get_res.status_code == 200
  assert context.get_res_data["success"] is True

  assert context.get_res_data.get("data").get(
      "employer") == context.payload.get("employer")
  assert context.get_res_data.get("data").get(
      "employer_email") == context.payload.get("employer_email")
  assert context.get_res_data.get("data").get(
      "employer_id") == context.payload.get("employer_id")
  # delete Learner
  delete_method(url=context.url + "/" + context.get_req_path_param)

# --------------------------- Negative ----------------------------------

@behave.given("A learner is not employed by a sponsoring employer partner")
def step_impl_1(context):
  """Defining the payload required for creating a learner account along with the employer details"""
  learner_dict = copy(LEARNER_OBJECT_TEMPLATE)
  learner_dict["email_address"] = "jondoe_c1f1s1_n@gmail.com"
  learner_dict["employer_id"] = ""
  learner_dict["employer"] = ""
  learner_dict["employer_email"] = "testid@employer.com"
  context.payload = learner_dict
  context.url = f"{API_URL}/learner"


@behave.when("The Learner Account is added")
def step_impl_2(context):
  """Creating the learner account with the provided payload"""
  context.post_res = post_method(url=context.url, request_body=context.payload)
  context.post_res_data = context.post_res.json()


@behave.then(
    "the employer information (name, address, and contact info) is not ingested into the SLP from the SNHU admin Salesforce record of the learner account"
)
def step_impl_3(context):
  """Validating the employer information when the learner account is created"""
  assert context.post_res.status_code == 200
  assert context.post_res_data.get("success") is True
  assert context.post_res_data.get(
      "message") == "Successfully created the learner"
  assert context.post_res_data.get("data").get(
      "employer_id") == context.payload.get("employer_id")
  assert context.post_res_data.get("data").get(
      "employer") == context.payload.get("employer")
  assert context.post_res_data.get("data").get(
      "employer_email") == context.payload.get("employer_email")

  context.get_req_path_param = context.post_res_data.get("data").get("uuid")


@behave.then(
    "Employer information is not visible to the learner through the learner-facing profile interface.")
def step_impl_4(context):
  """Validating the employer information when the learner access the learner information"""
  context.get_res = get_method(url=context.url + "/" +
                               context.get_req_path_param)
  context.get_res_data = context.post_res.json()
  assert context.get_res.status_code == 200
  assert context.get_res_data["success"] is True

  assert context.get_res_data.get("data").get(
      "employer") == context.payload.get("employer")
  assert context.get_res_data.get("data").get(
      "employer_email") == context.payload.get("employer_email")
  assert context.get_res_data.get("data").get(
      "employer_id") == context.payload.get("employer_id")
  # delete Learner
  delete_method(url=context.url + "/" + context.get_req_path_param)
