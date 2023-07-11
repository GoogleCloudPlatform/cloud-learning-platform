"""
Feature: Adding users to the discipline association group
"""
import behave
import sys
from copy import deepcopy
from uuid import uuid4

sys.path.append("../")
from common.models import AssociationGroup, User, CurriculumPathway
from e2e.test_object_schemas import TEST_USER, TEST_USER_GROUP, TEST_ASSOCIATION_GROUP, TEST_CURRICULUM_PATHWAY, TEST_ADD_USERS_ASSOCIATION_GROUP
from e2e.test_config import API_URL_USER_MANAGEMENT, DEL_KEYS
from e2e.setup import post_method, get_method

UM_API_URL = f"{API_URL_USER_MANAGEMENT}/association-groups"


# Scenario: add the user into the discipline association group with the correct request payload
@behave.given("discipline association group already exist")
def step_impl_1(context):

  # create an discipline association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = str(uuid4())
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/discipline-association"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()

  context.discipline_association_uuid = context.res_data["data"]["uuid"]
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the association group"

  #create a user of discipline type
  context.user_dict = {**TEST_USER, "user_type": "instructor"}
  context.user_dict["email"] = f"{uuid4()}@gmail.com"
  context.url = f"{API_URL_USER_MANAGEMENT}/user"
  context.post_user_res = post_method(
      url=context.url, request_body=context.user_dict)
  assert context.post_user_res.status_code == 200
  context.user_id = context.post_user_res.json()["data"]["user_id"]


@behave.when(
    "an API request sent to add the user into the discipline association group with the correct request payload"
)
def step_impl_2(context):

  add_users = {"users": [context.user_id], "status": "active"}
  context.url = f"{UM_API_URL}/discipline-association/{context.discipline_association_uuid}/users/add"

  context.res = post_method(url=context.url, request_body=add_users)
  context.res_data = context.res.json()


@behave.then(
    "the corresponding discipline association group object will be updated and also contain the list of user"
)
def step_impl_3(context):

  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully added the users to the discipline association group"
  assert context.user_id in context.res_data["data"]["users"][0]["user"]


# Scenario: unable to add the user into the discipline association group with the incorrect request payload
@behave.given("discipline association group already exists")
def step_impl_1(context):

  # create an discipline association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = str(uuid4())
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/discipline-association"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  context.discipline_association_uuid = context.res_data["data"]["uuid"]
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the association group"


@behave.when(
    "an API request sent to add the user into the discipline association group with an incorrect request payload"
)
def step_impl_2(context):

  add_users = {"users": ["user_id"], "status": "active"}
  context.url = f"{UM_API_URL}/discipline-association/{context.discipline_association_uuid}/users/add"

  context.res = post_method(url=context.url, request_body=add_users)
  context.res_data = context.res.json()


@behave.then("a validation error will thrown")
def step_impl_3(context):

  assert context.res.status_code == 404
  assert context.res_data["success"] == False


# Scenario: unable to add the user into the discipline association group with the incorrect request payload
@behave.given("discipline association group already exists with a user added")
def step_impl_1(context):

  # create an discipline association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = str(uuid4())
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/discipline-association"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  context.discipline_association_uuid = context.res_data["data"]["uuid"]
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the association group"

  context.user_dict = {**TEST_USER, "user_type": "instructor"}
  context.user_dict["email"] = f"{uuid4()}@gmail.com"
  context.url = f"{API_URL_USER_MANAGEMENT}/user"
  context.post_user_res = post_method(
      url=context.url, request_body=context.user_dict)
  assert context.post_user_res.status_code == 200
  context.user_id = context.post_user_res.json()["data"]["user_id"]

  add_users = {"users": [context.user_id], "status": "active"}
  context.url = f"{UM_API_URL}/discipline-association/{context.discipline_association_uuid}/users/add"
  context.res = post_method(url=context.url, request_body=add_users)
  context.res_data = context.res.json()

  assert context.res.status_code == 200

@behave.when(
    "an API request sent to add the same existing user into the discipline association group"
) 
def step_impl_2(context):

  add_users = {"users": [context.user_id], "status": "active"}
  context.url = f"{UM_API_URL}/discipline-association/{context.discipline_association_uuid}/users/add"

  context.res = post_method(url=context.url, request_body=add_users)
  context.res_data = context.res.json()


@behave.then("a validation error will be thrown")
def step_impl_3(context):

  assert context.res.status_code == 422
  assert context.res_data["success"] == False
  assert context.res_data["message"
      ] == f"User {context.user_id} is already present in the discipline association group"


# Scenario: remove the user from the discipline association group with the correct request payload
@behave.given("discipline association group is an already exist")
def step_impl_1(context):

  # create an discipline association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = str(uuid4())
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/discipline-association"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  context.discipline_association_uuid = context.res_data["data"]["uuid"]
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the association group"

  #create a user of discipline type and add to the discipline group
  context.user_dict = {**TEST_USER, "user_type": "instructor"}
  context.user_dict["email"] = f"{uuid4()}@gmail.com"
  context.url = f"{API_URL_USER_MANAGEMENT}/user"
  context.post_user_res = post_method(
      url=context.url, request_body=context.user_dict)
  assert context.post_user_res.status_code == 200
  context.user_id = context.post_user_res.json()["data"]["user_id"]

  # add created user to discipline association group
  req_body = deepcopy(TEST_ADD_USERS_ASSOCIATION_GROUP)
  req_body["users"] = [context.user_id]
  context.url = f"{UM_API_URL}/discipline-association/{context.discipline_association_uuid}/users/add"
  context.res = post_method(url=context.url, request_body=req_body)
  context.res_data = context.res.json()
  assert context.res.status_code == 200
  assert context.res_data["success"] == True
  assert context.res_data[
      "message"] == "Successfully added the users to the discipline association group"


@behave.when(
    "an API request sent to remove the user from the discipline association group with the correct request payload"
)
def step_impl_2(context):

  remove_user = {"user": context.user_id}
  context.url = f"{UM_API_URL}/discipline-association/{context.discipline_association_uuid}/user/remove"

  context.res = post_method(url=context.url, request_body=remove_user)
  context.res_data = context.res.json()


@behave.then(
    "the user will remove from the corresponding discipline association group object"
)
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully removed the user from the discipline association group"
  assert len(context.res_data["data"]["users"]) == 0


# Scenario: 
@behave.given("discipline association group already exists with a user of instructor type and discipline")
def step_impl_1(context):
  # Create Instructor
  email_1 = str(uuid4())
  user_dict_1 = {**TEST_USER}
  user_dict_1["email"] = f"{email_1}@gmail.com"
  user_dict_1["user_type"] = "instructor"
  user_dict_1["user_type_ref"] = ""
  user_1 = User.from_dict(user_dict_1)
  user_1.user_id = ""
  user_1.save()
  user_1.user_id = user_1.id
  user_1.update()
  user_dict_1["user_id"] = user_1.id
  context.instructor_id = user_1.user_id

  # Create Curriculum Pathway - Discipline
  pathway_dict = deepcopy(TEST_CURRICULUM_PATHWAY)

  pathway_dict["alias"] = "discipline"
  for key in DEL_KEYS:
    if key in pathway_dict:
      del pathway_dict[key]
  cp = CurriculumPathway.from_dict(pathway_dict)
  cp.uuid = ""
  cp.save()
  cp.uuid = cp.id
  cp.update()
  context.discipline_id = cp.id

  # Create discipline association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  post_group = post_method(
      url=f"{UM_API_URL}/discipline-association", request_body=association_group_dict)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

  group = AssociationGroup.find_by_uuid(context.group_uuid)
  group.users = [{"user": context.instructor_id, "user_type": "instructor", "status": "active"}]
  group.associations = {
    "curriculum_pathways": [{"curriculum_pathway_id": context.discipline_id, "status": "active"}]
  }
  group.update()

  # Create Learner association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Learner Association Group - {uuid4()}"
  post_group = post_method(
      url=f"{UM_API_URL}/learner-association", request_body=association_group_dict)
  context.post_group_data = post_group.json()
  context.learner_group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

  learner_group = AssociationGroup.find_by_uuid(context.learner_group_uuid)
  learner_group.users = []
  learner_group.associations = {
    "instructors": [{"instructor": context.instructor_id,
                     "curriculum_pathway_id": context.discipline_id,
                     "status": "active"}],
    "coaches": []
  }
  learner_group.update()
  context.learner_group = learner_group


@behave.when("an API request sent to remove the user of instructor type from the discipline association group with correct request payload")
def step_impl_2(context):

  remove_user = {"user": context.instructor_id}
  context.url = f"{UM_API_URL}/discipline-association/{context.group_uuid}/user/remove"

  context.res = post_method(url=context.url, request_body=remove_user)
  context.res_data = context.res.json()


@behave.then("the user of instructor type will get removed from the corresponding discipline association group object")
def step_impl_3(context):

  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully removed the user from the discipline association group"
  assert len(context.res_data["data"]["users"]) == 0


@behave.then("the instructor will also get removed from the Learner Association Group where it exists")
def step_impl_3(context):
  learner_group_url = f"{UM_API_URL}/learner-association/{context.learner_group_uuid}"
  get_response = get_method(learner_group_url)
  get_response_data = get_response.json()
  assert get_response.status_code == 200
  assert len(get_response_data["data"]["associations"]["instructors"]) == 0



# Scenario: unable to remove the user from the discipline association group with the incorrect request payload
@behave.given("discipline association group is already been exist")
def step_impl_1(context):

  # create an discipline association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = str(uuid4())
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/discipline-association"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  context.discipline_association_uuid = context.res_data["data"]["uuid"]
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the association group"


@behave.when(
    "an API request sent to remove the user from the discipline association group with the incorrect request payload"
)
def step_impl_2(context):

  remove_user = {"user": "user_id"}
  context.url = f"{UM_API_URL}/discipline-association/{context.discipline_association_uuid}/user/remove"

  context.res = post_method(url=context.url, request_body=remove_user)
  context.res_data = context.res.json()


@behave.then("a validations error is thrown")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] == False
  assert context.res_data["message"] == f"User with uuid user_id "\
        f"is not a part of Association Group with uuid {context.discipline_association_uuid}"
