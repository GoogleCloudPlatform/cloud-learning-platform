"""
Feature: Adding/Removing Discipline from Discipline Association Groups
"""
import behave
import sys
from copy import deepcopy
from uuid import uuid4

sys.path.append("../")
from common.models import CurriculumPathway, AssociationGroup, User
from test_object_schemas import TEST_ASSOCIATION_GROUP, TEST_CURRICULUM_PATHWAY, TEST_USER
from test_config import API_URL_USER_MANAGEMENT, DEL_KEYS
from setup import post_method, get_method, put_method, delete_method

UM_API_URL = f"{API_URL_USER_MANAGEMENT}/association-groups"

# Scenario : Add a Discipline to associations in an already created Discipline Association Group

@behave.given("A user has permission to user management and wants to add a discipline to the Discipline Association Group")
def step_impl_1(context):

  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"

  cp_dict = deepcopy(TEST_CURRICULUM_PATHWAY)
  cp = CurriculumPathway.from_dict(cp_dict)
  cp.alias = "discipline"
  cp.uuid = ""
  cp.save()
  cp.uuid = cp.id
  cp.update()
  context.cp_id = cp.id
  context.cp = cp

  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/discipline-association" 
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  assert context.res.status_code == 200, "Create Association Group Failed"
  context.association_group_uuid = context.res_data["data"]["uuid"]


@behave.when("API request is sent to add a Discipline to the Discipline Association Group with correct request payload")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association/{context.association_group_uuid}/discipline/add"
  context.request_body = {
    "curriculum_pathway_id": context.cp.id,
    "status": "active"
  }

  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()


@behave.then("Discipline Association Group object will be updated in the database with updated association from the request payload")
def step_impl_3(context):
  assert context.res.status_code == 200, f"Status Code = {context.res.status_code}"
  assert context.res_data["message"] == "Successfully added the discipline to the association group", f"{context.res_data['message']}"
  association_group_uuid = context.res_data["data"]["uuid"]
  url = f"{UM_API_URL}/discipline-association/{association_group_uuid}"
  request = get_method(url)
  group_data = request.json()
  assert request.status_code == 200
  assert group_data["success"] is True
  assert group_data["message"] == "Successfully fetched the association group"
  assert group_data["data"]["associations"] == {"curriculum_pathways": [context.request_body]}


# --- Add a Discipline to associations in an already created Discipline Association Group with invalid Discipline Association Group ID ---
@behave.given("A user has permission to user management and wants to add a discipline to the Discipline Association Group with invalid ID")
def step_impl_1(context):
  context.association_group_uuid = "wrong_id"
  context.url = f"{UM_API_URL}/discipline-association/{context.association_group_uuid}/discipline/add"
  context.request_body = {
    "curriculum_pathway_id": "abc",
    "status": "active"
  }

@behave.when("API request is sent to add a Discipline to the Discipline Association Group with correct request payload but invalid Discipline Association Group ID")
def step_impl_2(context):
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()


@behave.then("the API would raise ResourceNotFoundException")
def step_impl_3(context):
  assert context.res.status_code == 404


# --- Add a Discipline to associations in an already created Discipline Association Group with invalid request body ---
@behave.given("A user has permission to user management and wants to add a discipline to the Discipline Association Group with invalid request body")
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/discipline-association"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  assert context.res.status_code == 200, "Create Association Group Failed"
  context.association_group_uuid = context.res_data["data"]["uuid"]

@behave.when("API request is sent to add a Discipline to the Discipline Association Group with incorrect request payload")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association/{context.association_group_uuid}/discipline/add"
  context.request_body = {
    "curriculum_pathway_id": "abc",
    "status": "wrong_status"
  }
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()


@behave.then("the API would raise ValidationError")
def step_impl_3(context):
  assert context.res.status_code == 422


# --- Add a already associated Discipline to associations in an already created Discipline Association Group---
@behave.given("A user has permission to user management and wants to add an already associated discipline to the Discipline Association Group")
def step_impl_1(context):

  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"

  cp_dict = deepcopy(TEST_CURRICULUM_PATHWAY)
  cp = CurriculumPathway.from_dict(cp_dict)
  cp.alias = "discipline"
  cp.uuid = ""
  cp.save()
  cp.uuid = cp.id
  cp.update()
  context.cp_id = cp.id
  context.cp = cp

  context.payload = {"curriculum_pathway_id": cp.id, "status": "active"}
  context.request_body = association_group_dict

  context.url = f"{UM_API_URL}/discipline-association" 
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()

  assert context.res.status_code == 200, "Create Association Group Failed"
  context.association_group_uuid = context.res_data["data"]["uuid"]

  context.url = f"{UM_API_URL}/discipline-association/{context.association_group_uuid}/discipline/add"
  context.res = post_method(url=context.url, request_body=context.payload)
  assert context.res.status_code == 200, "Association of Discipline failed"


@behave.when("API request is sent to add already associated Discipline to the Discipline Association Group")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association/{context.association_group_uuid}/discipline/add"
  context.res = post_method(url=context.url, request_body=context.payload)
  context.res_data = context.res.json()


@behave.then("the API would raise ValidationError for the given discipline")
def step_impl_3(context):
  assert context.res.status_code == 422, f"Status Code = {context.res.status_code}"


# --- Remove a Discipline to associations in an already created Discipline Association Group---
@behave.given("A user has permission to user management and wants to remove a discipline to the Discipline Association Group")
def step_impl_1(context):

  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  
  cp_dict = deepcopy(TEST_CURRICULUM_PATHWAY)
  cp = CurriculumPathway.from_dict(cp_dict)
  cp.alias = "discipline"
  cp.uuid = ""
  cp.save()
  cp.uuid = cp.id
  cp.update()
  context.cp_id = cp.id
  context.cp = cp

  context.payload = {"curriculum_pathway_id": cp.id, "status": "active"}
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/discipline-association" 
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  assert context.res.status_code == 200, "Create Association Group Failed"
  context.association_group_uuid = context.res_data["data"]["uuid"]

  context.url = f"{UM_API_URL}/discipline-association/{context.association_group_uuid}/discipline/add"
  context.res = post_method(url=context.url, request_body=context.payload)
  context.res_data = context.res.json()
  assert context.res.status_code == 200, "Discipline Association to Group Failed"


@behave.when("API request is sent to remove a Discipline to the Discipline Association Group with correct request payload")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association/{context.association_group_uuid}/discipline/remove"
  context.payload = {"curriculum_pathway_id": context.cp_id}
  context.res = post_method(url=context.url, request_body=context.payload)
  context.res_data = context.res.json()


@behave.then("Discipline Association Group object will be updated in the database and the discipline will be removed")
def step_impl_3(context):
  assert context.res.status_code == 200, f"Status Code = {context.res.status_code}"
  assert context.res_data["data"]["associations"] == {"curriculum_pathways": []}, "Association not removed successfully"


# ---Remove a Discipline to associations in an already created Discipline Association Group with invalid association group ID---
@behave.given("A user has permission to user management and wants to remove a discipline to the Discipline Association Group with invalid association group ID")
def step_impl_1(context):

  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  context.payload = {"curriculum_pathway_id": "abc", "status": "active"}
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/discipline-association" 
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  assert context.res.status_code == 200, "Create Association Group Failed"
  context.association_group_uuid = context.res_data["data"]["uuid"]


@behave.when("API request is sent to remove a Discipline to the Discipline Association Group with invalid assoication group ID")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association/wrong_id/discipline/remove"
  context.res = post_method(url=context.url, request_body=context.payload)
  context.res_data = context.res.json()


@behave.then("the API would raise ResourceNotFoundException with 404 status code")
def step_impl_3(context):
  assert context.res.status_code == 404, f"Status Code = {context.res.status_code}"


# ---Remove a Discipline to associations in an already created Discipline Association Group with invalid payload---
@behave.given("A user has permission to user management and wants to remove a discipline to the Discipline Association Group with invalid payload")
def step_impl_1(context):

  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/discipline-association" 
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  assert context.res.status_code == 200, "Create Association Group Failed"
  context.association_group_uuid = context.res_data["data"]["uuid"]

  cp_dict = deepcopy(TEST_CURRICULUM_PATHWAY)
  cp = CurriculumPathway.from_dict(cp_dict)
  cp.alias = "discipline"
  cp.uuid = ""
  cp.save()
  cp.uuid = cp.id
  cp.update()
  context.cp_id = cp.id
  context.cp = cp

@behave.when("API request is sent to remove a Discipline to the Discipline Association Group with invalid payload")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association/{context.association_group_uuid}/discipline/remove"
  context.payload = {"curriculum_pathway_id": context.cp_id}
  context.res = post_method(url=context.url, request_body=context.payload)
  context.res_data = context.res.json()


@behave.then("the API would raise ValidationError with 422 status code")
def step_impl_3(context):
  assert context.res.status_code == 422, f"Status Code = {context.res.status_code}"



# Scenario: Remove the Discipline from the discipline association group with the correct request payload
@behave.given("Discipline association group already exists with a user (instructor) actively associated to a discipline")
def step_impl_1(context):
  # Create Instructor
  email_1 = str(uuid4())
  user_dict_1 = {**TEST_USER}
  user_dict_1["email"] = f"{email_1}@gmail.com"
  user_dict_1["user_type"] = "faculty"
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
  group.users = [{"user": context.instructor_id, "user_group_type": "instructor", "status": "active"}]
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


@behave.when("an API request sent to remove the Discipline from the discipline association group with correct request payload")
def step_impl_2(context):

  remove_discipline = {"curriculum_pathway_id": context.discipline_id}
  context.url = f"{UM_API_URL}/discipline-association/{context.group_uuid}/discipline/remove"

  context.res = post_method(url=context.url, request_body=remove_discipline)
  context.res_data = context.res.json()
  print(context.res)
  print(context.res_data)


@behave.then("discipline will get removed from the corresponding discipline association group object")
def step_impl_3(context):

  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully removed the discipline from the association group"
  assert len(context.res_data["data"]["associations"]["curriculum_pathways"]) == 0


@behave.then("the user of instructor type associated to the discipline will also get removed from all Learner Association Group where it exists")
def step_impl_3(context):
  learner_group_url = f"{UM_API_URL}/learner-association/{context.learner_group_uuid}"
  get_response = get_method(learner_group_url)
  get_response_data = get_response.json()
  assert get_response.status_code == 200
  assert len(get_response_data["data"]["associations"]["instructors"]) == 0