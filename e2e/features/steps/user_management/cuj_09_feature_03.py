"""
Feature: Adding users and coaches to the learner association group
"""
import behave
import sys
from copy import deepcopy
from uuid import uuid4

sys.path.append("../")
from e2e.test_object_schemas import TEST_USER, TEST_USER_GROUP, TEST_ASSOCIATION_GROUP
from e2e.test_config import API_URL_USER_MANAGEMENT
from e2e.setup import post_method, get_method

UM_API_URL = f"{API_URL_USER_MANAGEMENT}/association-groups"


# Scenario: add the user into the learner association group with the correct request payload
@behave.given("learner association group already exist")
def step_impl_1(context):

  # create an learner association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = str(uuid4())
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/learner-association"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()

  context.learner_association_uuid = context.res_data["data"]["uuid"]
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the association group"

  # create a user of learner type
  context.user_dict = deepcopy(TEST_USER)
  context.user_dict["email"] = f"{uuid4()}@gmail.com"
  context.url = f"{API_URL_USER_MANAGEMENT}/user"
  context.post_user_res = post_method(
      url=context.url, request_body=context.user_dict)
  assert context.post_user_res.status_code == 200
  context.user_id = context.post_user_res.json()["data"]["user_id"]


@behave.when(
    "an API request sent to add the user into the learner association group with the correct request payload"
)
def step_impl_2(context):

  add_users = {"users": [context.user_id], "status": "active"}
  context.url = f"{UM_API_URL}/learner-association/{context.learner_association_uuid}/users/add"

  context.res = post_method(url=context.url, request_body=add_users)
  context.res_data = context.res.json()


@behave.then(
    "the corresponding learner association group object will be updated and also contain the list of user"
)
def step_impl_3(context):

  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully added the users to the learner association group"
  assert context.user_id in context.res_data["data"]["users"][0]["user"]


# Scenario: unable to add the user into the learner association group with the incorrect request payload
@behave.given("learner association group already exists")
def step_impl_1(context):

  # create an learner association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = str(uuid4())
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/learner-association"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  context.learner_association_uuid = context.res_data["data"]["uuid"]
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the association group"


@behave.when(
    "an API request sent to add the user into the learner association group with an incorrect request payload"
)
def step_impl_2(context):

  add_users = {"users": ["user_id"], "status": "active"}
  context.url = f"{UM_API_URL}/learner-association/{context.learner_association_uuid}/users/add"

  context.res = post_method(url=context.url, request_body=add_users)
  context.res_data = context.res.json()


@behave.then("a validation error thrown")
def step_impl_3(context):

  assert context.res.status_code == 404
  assert context.res_data["success"] == False


# Scenario: remove the user from the learner association group with the correct request payload
@behave.given("learner association group is an already exist")
def step_impl_1(context):

  # create an learner association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = str(uuid4())
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/learner-association"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  context.learner_association_uuid = context.res_data["data"]["uuid"]
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the association group"

  #create a user of learner type
  context.user_dict = deepcopy(TEST_USER)
  context.user_dict["email"] = f"{uuid4()}@gmail.com"
  context.url = f"{API_URL_USER_MANAGEMENT}/user"
  context.post_user_res = post_method(
      url=context.url, request_body=context.user_dict)
  assert context.post_user_res.status_code == 200
  context.user_id = context.post_user_res.json()["data"]["user_id"]

  # Add learner to Learner association group
  add_user_url = f"{UM_API_URL}/learner-association/{context.learner_association_uuid}/users/add"
  add_user_payload = {
                      "users": [context.user_id],
                      "status": "active"
                      }
  post_res = post_method(url=add_user_url, request_body=add_user_payload)
  assert post_res.status_code == 200


@behave.when(
    "an API request sent to remove the user from the learner association group with the correct request payload"
)
def step_impl_2(context):

  remove_user = {"user": context.user_id}
  context.url = f"{UM_API_URL}/learner-association/{context.learner_association_uuid}/user/remove"

  context.res = post_method(url=context.url, request_body=remove_user)
  context.res_data = context.res.json()


@behave.then(
    "the user will remove from the corresponding learner association group object"
)
def step_impl_3(context):

  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully removed the user from the learner association group"
  assert len(context.res_data["data"]["users"]) == 0



# Scenario: unable to remove user from learner association group when user does not exist in learner association group
@behave.given("learner association group already exists with no users added")
def step_impl_1(context):

  # create an learner association group with no users added
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = str(uuid4())
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/learner-association"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  context.learner_association_uuid = context.res_data["data"]["uuid"]
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the association group"


@behave.when(
    "an API request sent to remove a user that does not exist in the learner association group"
)
def step_impl_2(context):

  remove_user = {"user": "random_uuid"}
  context.url = f"{UM_API_URL}/learner-association/{context.learner_association_uuid}/user/remove"

  context.res = post_method(url=context.url, request_body=remove_user)
  context.res_data = context.res.json()


@behave.then(
  "a ValidationError stating that the user does not exist in Learner association group will be thrown"
)
def step_impl_3(context):
  error_message = "The given user_id random_uuid does not exist in the Learner " + \
    f"Association Group for given uuid {context.learner_association_uuid}"
  assert context.res.status_code == 422
  assert context.res_data["message"] == error_message



# Scenario: add coach into the learner association group with the correct request payload
@behave.given("learner association group already exist of type learner")
def step_impl_1(context):

  # create an learner association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = str(uuid4())
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/learner-association"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  context.learner_association_uuid = context.res_data["data"]["uuid"]
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the association group"

  #create a user of coach type
  context.user_dict = {**TEST_USER, "user_type": "coach"}
  context.user_dict["email"] = f"{uuid4()}@gmail.com"
  context.url = f"{API_URL_USER_MANAGEMENT}/user"
  context.post_user_res = post_method(
      url=context.url, request_body=context.user_dict)
  assert context.post_user_res.status_code == 200
  context.coach_id = context.post_user_res.json()["data"]["user_id"]


@behave.when(
    "a API request sent to add the coach into the learner association group with the correct request payload"
)
def step_impl_2(context):

  add_coach = {"coaches": [context.coach_id], "status": "active"}
  context.url = f"{UM_API_URL}/learner-association/{context.learner_association_uuid}/coaches/add"

  context.res = post_method(url=context.url, request_body=add_coach)
  context.res_data = context.res.json()


@behave.then(
    "the corresponding learner association group object will be updated and also contain the list of coach"
)
def step_impl_3(context):

  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully added the coaches to the learner association group"
  assert context.coach_id in context.res_data["data"]["associations"][
      "coaches"][0]["coach"]


# Scenario: unable to add coach into the learner association group with the incorrect request payload
@behave.given("learner association group already exists of type learner")
def step_impl_1(context):

  # create an learner association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = str(uuid4())
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/learner-association"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  context.learner_association_uuid = context.res_data["data"]["uuid"]
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the association group"


@behave.when(
    "an API request sent to add the coach into the learner association group with the incorrect request payload"
)
def step_impl_2(context):

  add_users = {"coaches": ["coach_id"], "status": "active"}
  context.url = f"{UM_API_URL}/learner-association/{context.learner_association_uuid}/coaches/add"

  context.res = post_method(url=context.url, request_body=add_users)
  context.res_data = context.res.json()


@behave.then("validation error is thrown")
def step_impl_3(context):

  assert context.res.status_code == 404
  assert context.res_data["success"] == False


# Scenario: remove the coach from the learner association group with the correct request payload
@behave.given("learner association group is already existing")
def step_impl_1(context):

  # create an learner association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = str(uuid4())
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/learner-association"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  context.learner_association_uuid = context.res_data["data"]["uuid"]
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the association group"

  #create a user of coach type
  context.user_dict = {**TEST_USER, "user_type": "coach"}
  context.user_dict["email"] = f"{uuid4()}@gmail.com"
  context.url = f"{API_URL_USER_MANAGEMENT}/user"
  context.post_user_res = post_method(
      url=context.url, request_body=context.user_dict)
  assert context.post_user_res.status_code == 200
  context.coach_id = context.post_user_res.json()["data"]["user_id"]

  # Add coach to Learner association group
  add_coach_url = f"{UM_API_URL}/learner-association/{context.learner_association_uuid}/coaches/add"
  add_coach_payload = {
                      "coaches": [context.coach_id],
                      "status": "active"
                      }
  post_res = post_method(url=add_coach_url, request_body=add_coach_payload)
  assert post_res.status_code == 200


@behave.when(
    "an API request sent to remove the coach from the learner association group with the correct request payload"
)
def step_impl_2(context):

  remove_user = {"coach": context.coach_id}
  context.url = f"{UM_API_URL}/learner-association/{context.learner_association_uuid}/coach/remove"

  context.res = post_method(url=context.url, request_body=remove_user)
  context.res_data = context.res.json()


@behave.then(
    "the coach will remove from the corresponding learner association group object"
)
def step_impl_3(context):

  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully removed the coach from the learner association group"
  assert context.coach_id not in context.res_data["data"]["associations"][
      "coaches"]



# Scenario: unable to remove coach from learner association group when coach does not exist in learner association group
@behave.given("learner association group already exists with no coaches added")
def step_impl_1(context):

  # create an learner association group with no coaches added
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = str(uuid4())
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/learner-association"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  context.learner_association_uuid = context.res_data["data"]["uuid"]
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the association group"


@behave.when(
    "an API request sent to remove the coach that does not exist in the learner association group"
)
def step_impl_2(context):

  remove_user = {"coach": "random_uuid"}
  context.url = f"{UM_API_URL}/learner-association/{context.learner_association_uuid}/coach/remove"

  context.res = post_method(url=context.url, request_body=remove_user)
  context.res_data = context.res.json()


@behave.then(
  "a ValidationError stating that the coach does not exist in Learner association group will be thrown"
)
def step_impl_3(context):
  error_message = "The given coach_id random_uuid does not exist in the Learner " + \
    f"Association Group for given uuid {context.learner_association_uuid}"

  assert context.res.status_code == 422
  assert context.res_data["message"] == error_message
