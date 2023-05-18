"""
Feature: CRUD for managing Learner Association Group in user management
"""
import behave
import sys
import json
from copy import deepcopy
from uuid import uuid4

sys.path.append("../")
from common.models import User, AssociationGroup, CurriculumPathway
from test_object_schemas import (TEST_ASSOCIATION_GROUP, TEST_USER,
                                 TEST_ADD_INSTRUCTOR, TEST_REMOVE_INSTRUCTOR,
                                 TEST_CURRICULUM_PATHWAY,
                                 TEST_LEARNER_ASSOCIATION_GROUP)
from test_config import API_URL_USER_MANAGEMENT, API_URL_LEARNING_OBJECT_SERVICE
from environment import TEST_LEARNING_HIERARCHY_PATH
from setup import post_method, get_method, put_method, delete_method

UM_API_URL = f"{API_URL_USER_MANAGEMENT}/association-groups"

# -------------------------------CREATE GROUP----------------------------------


@behave.given(
    "A user has permission to user management and wants to create a Learner Association Group"
)
def step_impl_1(context):

  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Learner Association Group - {uuid4()}"
  context.request_body = association_group_dict


@behave.when(
    "API request is sent to create Learner Association Group with correct request payload"
)
def step_impl_2(context):
  context.url = f"{UM_API_URL}/learner-association"

  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()


@behave.then(
    "Learner Association Group object will be created in the database as per given request payload"
)
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the association group"
  association_group_uuid = context.res_data["data"]["uuid"]
  url = f"{UM_API_URL}/learner-association/{association_group_uuid}"
  request = get_method(url)
  group_data = request.json()
  assert request.status_code == 200
  assert group_data["success"] is True
  assert group_data["message"] == "Successfully fetched the association group"
  assert group_data["data"]["name"] == context.request_body["name"]
  assert group_data["data"]["association_type"] == "learner"


# --- Negative Scenario 1 ---
@behave.given(
    "A user has permission to user management and wants to create a Learner Association Group with incorrect payload"
)
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Learner Association Group - {uuid4()}"
  context.payload = association_group_dict
  del context.payload["name"]
  context.url = f"{UM_API_URL}/learner-association"


@behave.when(
    "API request is sent to create Learner Association Group with incorrect request payload"
)
def step_impl_2(context):
  context.res = post_method(url=context.url, request_body=context.payload)
  context.res_data = context.res.json()


@behave.then(
    "Learner Association Group object will not be created and a validation error is thrown"
)
def step_impl_3(context):
  assert context.res.status_code == 422
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Validation Failed"
  assert context.res_data["data"][0]["msg"] == "field required"
  assert context.res_data["data"][0]["type"] == "value_error.missing"


# --- Negative Scenario 2 ---
@behave.given(
    "A user has permission to user management and wants to create a Learner Association Group with name already existing in database"
)
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Learner Association Group - {uuid4()}"
  context.association_group_name = association_group_dict["name"]
  context.url = f"{UM_API_URL}/learner-association"
  post_res = post_method(url=context.url, request_body=association_group_dict)
  post_res_data = post_res.json()
  assert post_res.status_code == 200
  assert post_res_data["success"] is True

  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = context.association_group_name
  context.payload = association_group_dict


@behave.when(
    "API request is sent to create Learner Association Group with name already existing in database"
)
def step_impl_2(context):
  context.res = post_method(url=context.url, request_body=context.payload)
  context.res_data = context.res.json()


@behave.then(
    "Learner Association Group object will not be created and a conflict error is thrown"
)
def step_impl_3(context):
  assert context.res.status_code == 409
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == \
    f"AssociationGroup with the given name: {context.association_group_name} already exists"


# -------------------------------GET GROUP-------------------------------------
# --- Positive Scenario ---
@behave.given(
    "A user has access privileges to User management and needs to fetch a Learner Association Group"
)
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Learner Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/learner-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  context.association_group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200


@behave.when(
    "API request is sent to fetch Learner Association Group by providing correct uuid"
)
def step_impl_2(context):
  context.url = f"{UM_API_URL}/learner-association/{context.association_group_uuid}"
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then(
    "Learner Association Group object corresponding to given uuid will be returned successfully"
)
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data[
      "message"] == "Successfully fetched the association group"
  assert context.res_data["data"] == context.post_group_data["data"]


# --- Negative Scenario_1 ---
@behave.given(
    "A user has access to User management and needs to fetch a Learner Association Group"
)
def step_impl_1(context):
  invalid_group_uuid = "random_id"
  context.url = f"{UM_API_URL}/learner-association/{invalid_group_uuid}"


@behave.when(
    "API request is sent to fetch Learner Association Group by providing invalid uuid"
)
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then(
    "Learner Association Group object will not be returned and Resource not found error will be thrown by User management"
)
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False, "success not False"
  assert context.res_data["message"] == \
        "AssociationGroup with uuid random_id not found"


# --- Negative Scenario_2 ---
@behave.given(
    "A user has access to User management and needs to fetch a Association Group of Learner Type"
)
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/discipline-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  context.association_group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200


@behave.when(
    "API request is sent to fetch Learner Association Group by providing uuid for Discipline Association Group"
)
def step_impl_2(context):
  context.url = f"{UM_API_URL}/learner-association/{context.association_group_uuid}"
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then(
    "Learner Association Group object will not be returned and Validation error will be thrown by User management"
)
def step_impl_3(context):
  assert context.res.status_code == 422
  context.res_data = context.res.json()
  assert context.res_data["success"] is False, "success not False"
  assert context.res_data["message"] == \
    f"AssociationGroup for given uuid: {context.association_group_uuid} is not learner type"


#-------------------------------GET ALL GROUPS-----------------------------------
# --- Positive Scenario ---
@behave.given(
    "A user has access to User management and needs to fetch all Learner Association Groups"
)
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Learner Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/learner-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200
  context.url = f"{UM_API_URL}/learner-associations"


@behave.when("API request is sent to fetch all Learner Association Groups")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then(
    "User management will return all existing Learner Association Group objects successfully"
)
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == \
              "Successfully fetched the association groups"
  fetched_uuids = [i.get("uuid") for i in context.res_data.get("data")["records"]]
  assert context.group_uuid in fetched_uuids


# --- Negative Scenario ---
@behave.given(
    "A user can access User management and needs to fetch all Learner Association Groups"
)
def step_impl_1(context):
  context.url = f"{UM_API_URL}/learner-associations"
  context.params = params = {"skip": "-1", "limit": "10"}


@behave.when(
    "API request is sent to fetch all Learner Association Groups with incorrect params"
)
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()


@behave.then(
    "No Learner Association Groups will be fetched and User management will throw a Validation error"
)
def step_impl_3(context):
  assert context.res.status_code == 422, "Status not 422"
  assert context.res_data.get("message") == \
    "Validation Failed", \
    "unknown response received"


#-------------------------------UPDATE GROUP-------------------------------------
# --- Positive Scenario ---
@behave.given(
    "A user has access to User management and needs to update a Learner Association Group"
)
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Learner Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/learner-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200


@behave.when(
    "API request is sent to update Learner Association Group with correct request payload"
)
def step_impl_2(context):
  context.url = f"{UM_API_URL}/learner-association/{context.group_uuid}"
  updated_data = context.payload
  updated_data["description"] = "updated description"
  updated_data["name"] = f"Updated Learner Association Group - {uuid4()}"
  context.association_group_name = updated_data["name"]
  context.res = put_method(url=context.url, request_body=updated_data)
  context.res_data = context.res.json()


@behave.then(
    "The corresponding Learner Association Group object will be updated successfully"
)
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == \
                "Successfully updated the association group"
  assert context.res_data["data"]["description"] == "updated description"
  assert context.res_data["data"]["name"] == context.association_group_name


# --- Negative Scenario_1 ---
@behave.given(
    "A user has access privileges to User management and needs to update a Learner Association Group"
)
def step_impl_1(context):
  invalid_group_uuid = "random_id"
  context.url = f"{UM_API_URL}/learner-association/{invalid_group_uuid}"


@behave.when(
    "API request is sent to update Learner Association Group by providing invalid uuid"
)
def step_impl_2(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Learner Association Group - {uuid4()}"

  context.res = put_method(url=context.url, request_body=association_group_dict)
  context.res_data = context.res.json()


@behave.then(
    "Learner Association Group object will not be updated and User management will throw a resource not found error"
)
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == \
            "AssociationGroup with uuid random_id not found"


# --- Negative Scenario_2 ---
@behave.given(
    "A user has permission to user management and wants to update name thats already exists in database"
)
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Learner Association Group - {uuid4()}"
  context.association_group_name = association_group_dict["name"]
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/learner-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200


@behave.when(
    "API request is sent to update Learner Association Group with name already existing in database"
)
def step_impl_2(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = context.association_group_name
  association_group_dict["description"] = "Updated description"
  context.url = f"{UM_API_URL}/learner-association/{context.group_uuid}"
  context.res = put_method(url=context.url, request_body=association_group_dict)
  context.res_data = context.res.json()


@behave.then(
    "Learner Association Group object will not be updated and a conflict error is thrown"
)
def step_impl_3(context):
  assert context.res.status_code == 409
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == \
    f"AssociationGroup with the given name: {context.association_group_name} already exists"


# --- Negative Scenario_3 ---
@behave.given(
    "A user has access to User management and needs to update a Association Group of Learner Type"
)
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/discipline-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  context.association_group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200


@behave.when(
    "API request is sent to update Learner Association Group by providing uuid for Discipline Association Group"
)
def step_impl_2(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Learner Association Group - {uuid4()}"
  association_group_dict["description"] = "Updated description"
  context.url = f"{UM_API_URL}/learner-association/{context.association_group_uuid}"
  context.res = put_method(url=context.url, request_body=association_group_dict)
  context.res_data = context.res.json()


@behave.then(
    "Learner Association Group object will not be updated and Validation error will be thrown by User management"
)
def step_impl_3(context):
  assert context.res.status_code == 422
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == \
    f"AssociationGroup for given uuid: {context.association_group_uuid} is not learner type"


#-------------------------------DELETE GROUP-------------------------------------
# --- Positive Scenario ---
@behave.given(
    "A user has access to User management and needs to delete a Learner Association Group"
)
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Learner Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/learner-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200


@behave.when(
    "API request is sent to delete Learner Association Group by providing correct uuid"
)
def step_impl_2(context):
  context.url = f"{UM_API_URL}/learner-association/{context.group_uuid}"
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Learner Association Group object will be deleted successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == \
                "Successfully deleted the association group"


# --- Negative Scenario_1 ---
@behave.given(
    "A user has access privileges to User management and needs to delete an Learner Association Group"
)
def step_impl_1(context):
  invalid_group_uuid = "random_id"
  context.url = f"{UM_API_URL}/learner-association/{invalid_group_uuid}"


@behave.when(
    "API request is sent to delete Learner Association Group by providing invalid uuid"
)
def step_impl_2(context):
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()


@behave.then(
    "Learner Association Group object will not be deleted and User management will throw a resource not found error"
)
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data[
      "message"] == "AssociationGroup with uuid random_id not found"


# --- Negative Scenario_2 ---
@behave.given(
    "A user has access to User management and needs to delete a Association Group of Learner Type"
)
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/discipline-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  context.association_group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200


@behave.when(
    "API request is sent to delete Learner Association Group by providing uuid for Discipline Association Group"
)
def step_impl_2(context):
  context.url = f"{UM_API_URL}/learner-association/{context.association_group_uuid}"
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()


@behave.then(
    "Learner Association Group object will not be deleted and Validation error will be thrown by User management"
)
def step_impl_3(context):
  assert context.res.status_code == 422
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data[
      "message"] == f"AssociationGroup for given uuid: {context.association_group_uuid} is not learner type"


#-----------------------UPDATE USER/ASSOCIATION STATUS--------------------
# --- Positive Scenario ---
@behave.given(
    "A Learner Association Group exists and user has access to User management to update User/Association Status"
)
def step_impl_1(context):
  # Create Learner
  email_1 = str(uuid4())
  user_dict_1 = {**TEST_USER}
  user_dict_1["email"] = f"{email_1}@gmail.com"
  user_dict_1["user_type"] = "learner"
  user_dict_1["user_type_ref"] = ""
  user_1 = User.from_dict(user_dict_1)
  user_1.user_id = ""
  user_1.save()
  user_1.user_id = user_1.id
  user_1.update()
  user_dict_1["user_id"] = user_1.id
  context.learner_id = user_1.user_id

  email_2 = str(uuid4())
  user_dict_2 = {**TEST_USER}
  user_dict_2["email"] = f"{email_2}@gmail.com"
  user_dict_2["user_type"] = "coach"
  user_dict_2["user_type_ref"] = ""
  user_2 = User.from_dict(user_dict_2)
  user_2.user_id = ""
  user_2.save()
  user_2.user_id = user_2.id
  user_2.update()
  user_dict_2["user_id"] = user_2.id
  context.coach_id = user_2.user_id

  # Create learner association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Learner Association Group - {uuid4()}"
  post_group = post_method(
      url=f"{UM_API_URL}/learner-association",
      request_body=association_group_dict)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

  group = AssociationGroup.find_by_uuid(context.group_uuid)
  group.users = [{"user": context.learner_id, "status": "active"}]
  group.associations = {
      "coaches": [{
          "coach": context.coach_id,
          "status": "active"
      }],
      "instructors": []
  }
  group.update()


@behave.when(
    "API request is sent to update User/Association Status of a Learner Association Group with correct request payload"
)
def step_impl_2(context):
  context.url = f"{UM_API_URL}/learner-association/{context.group_uuid}/user-association/status"
  request_body = {
      "user": {
          "user_id": context.learner_id,
          "status": "inactive"
      },
      "coach": {
          "coach_id": context.coach_id,
          "status": "inactive"
      }
  }
  context.res = put_method(url=context.url, request_body=request_body)
  context.res_data = context.res.json()


@behave.then(
    "The status of User/Association within the Learner Association Group object will be updated successfully"
)
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == \
                "Successfully updated the association group"
  assert context.res_data["data"]["users"][0]["status"] == "inactive"
  assert context.res_data["data"]["associations"]["coaches"][0][
      "status"] == "inactive"


# --- Positive Scenario - 2---
@behave.given(
    "A Learner Association Group, Discipline Association Group exists with actively associated user & discipline"
)
def step_impl_1(context):
  # Create Learner
  email_1 = str(uuid4())
  user_dict_1 = {**TEST_USER}
  user_dict_1["email"] = f"{email_1}@gmail.com"
  user_dict_1["user_type"] = "learner"
  user_dict_1["user_type_ref"] = ""
  user_1 = User.from_dict(user_dict_1)
  user_1.user_id = ""
  user_1.save()
  user_1.user_id = user_1.id
  user_1.update()
  user_dict_1["user_id"] = user_1.id
  context.learner_id = user_1.user_id

  email_2 = str(uuid4())
  user_dict_2 = {**TEST_USER}
  user_dict_2["email"] = f"{email_2}@gmail.com"
  user_dict_2["user_type"] = "instructor"
  user_dict_2["user_type_ref"] = ""
  user_2 = User.from_dict(user_dict_2)
  user_2.user_id = ""
  user_2.save()
  user_2.user_id = user_2.id
  user_2.update()
  user_dict_2["user_id"] = user_2.id
  context.instructor_id = user_2.user_id

  # Create Curriculum Pathway - Discipline
  payload = deepcopy(TEST_CURRICULUM_PATHWAY)
  payload["alias"] = "discipline"
  curriculum_pathway = CurriculumPathway.from_dict(payload)
  curriculum_pathway.uuid = ""
  curriculum_pathway.version = 1
  curriculum_pathway.save()
  curriculum_pathway.uuid = curriculum_pathway.id
  curriculum_pathway.update()
  context.curriculum_pathway_id = curriculum_pathway.uuid

  # Create Discipline association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  post_group = post_method(
      url=f"{UM_API_URL}/discipline-association",
      request_body=association_group_dict)
  context.post_group_data = post_group.json()
  discipline_group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

  group = AssociationGroup.find_by_uuid(discipline_group_uuid)
  group.users = [{"user": context.instructor_id, "status": "active"}]
  group.associations = {
    "curriculum_pathways": [{"curriculum_pathway_id": context.curriculum_pathway_id,
                             "status": "active"}]
  }
  group.update()

  # Create learner association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Learner Association Group - {uuid4()}"
  post_group = post_method(
      url=f"{UM_API_URL}/learner-association",
      request_body=association_group_dict)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

  group = AssociationGroup.find_by_uuid(context.group_uuid)
  group.users = [{"user": context.learner_id, "status": "active"}]
  group.associations = {
    "coaches": [],
    "instructors": [{"instructor": context.instructor_id,
                     "curriculum_pathway_id": context.curriculum_pathway_id,
                     "status": "inactive"}]
  }
  group.update()


@behave.when(
    "API request is sent to activate an instructor for given instructor_id and curriculum_pathway_id"
)
def step_impl_2(context):
  context.url = f"{UM_API_URL}/learner-association/{context.group_uuid}/user-association/status"
  request_body = {
    "instructor": {"instructor_id": context.instructor_id,
                   "curriculum_pathway_id": context.curriculum_pathway_id,
                   "status": "active"}
  }
  context.res = put_method(url=context.url, request_body=request_body)
  context.res_data = context.res.json()


@behave.then(
    "The instructor for given instructor_id and curriculum_pathway_id within the Learner Association Group object will be activated successfully"
)
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == \
                "Successfully updated the association group"
  assert context.res_data["data"]["associations"]["instructors"][0][
      "status"] == "active"


# --- Negative Scenario_1 ---
@behave.given(
    "A Learner Association Group exists and user has access to update User/Association Status"
)
def step_impl_1(context):
  # Create Learner
  email_1 = str(uuid4())
  user_dict_1 = {**TEST_USER}
  user_dict_1["email"] = f"{email_1}@gmail.com"
  user_dict_1["user_type"] = "learner"
  user_dict_1["user_type_ref"] = ""
  user_1 = User.from_dict(user_dict_1)
  user_1.user_id = ""
  user_1.save()
  user_1.user_id = user_1.id
  user_1.update()
  user_dict_1["user_id"] = user_1.id
  context.learner_id = user_1.user_id

  email_2 = str(uuid4())
  user_dict_2 = {**TEST_USER}
  user_dict_2["email"] = f"{email_2}@gmail.com"
  user_dict_2["user_type"] = "coach"
  user_dict_2["user_type_ref"] = ""
  user_2 = User.from_dict(user_dict_2)
  user_2.user_id = ""
  user_2.save()
  user_2.user_id = user_2.id
  user_2.update()
  user_dict_2["user_id"] = user_2.id
  context.coach_id = user_2.user_id

  # Create learner association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Learner Association Group - {uuid4()}"
  post_group = post_method(
      url=f"{UM_API_URL}/learner-association",
      request_body=association_group_dict)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

  group = AssociationGroup.find_by_uuid(context.group_uuid)
  group.users = [{"user": context.learner_id, "status": "active"}]
  group.associations = {
      "coaches": [{
          "coach": context.coach_id,
          "status": "active"
      }],
      "instructors": []
  }
  group.update()

  invalid_group_uuid = "random_id"
  context.url = f"{UM_API_URL}/learner-association/{invalid_group_uuid}/user-association/status"


@behave.when(
    "API request is sent to update User/Association status within Learner Association Group by providing invalid group uuid"
)
def step_impl_2(context):
  request_body = {
      "user": {
          "user_id": context.learner_id,
          "status": "inactive"
      },
      "coach": {
          "coach_id": context.coach_id,
          "status": "inactive"
      }
  }
  context.res = put_method(url=context.url, request_body=request_body)
  context.res_data = context.res.json()


@behave.then(
    "User/Association Status will not be updated and User management will throw a resource not found error"
)
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == \
            "AssociationGroup with uuid random_id not found"


# --- Negative Scenario_2 ---
@behave.given(
    "A Learner Association Group exists and user has access privileges to update User/Association Status"
)
def step_impl_1(context):
  # Create Learner
  email_1 = str(uuid4())
  user_dict_1 = {**TEST_USER}
  user_dict_1["email"] = f"{email_1}@gmail.com"
  user_dict_1["user_type"] = "learner"
  user_dict_1["user_type_ref"] = ""
  user_1 = User.from_dict(user_dict_1)
  user_1.user_id = ""
  user_1.save()
  user_1.user_id = user_1.id
  user_1.update()
  user_dict_1["user_id"] = user_1.id
  context.learner_id = user_1.user_id

  email_2 = str(uuid4())
  user_dict_2 = {**TEST_USER}
  user_dict_2["email"] = f"{email_2}@gmail.com"
  user_dict_2["user_type"] = "coach"
  user_dict_2["user_type_ref"] = ""
  user_2 = User.from_dict(user_dict_2)
  user_2.user_id = ""
  user_2.save()
  user_2.user_id = user_2.id
  user_2.update()
  user_dict_2["user_id"] = user_2.id
  context.coach_id = user_2.user_id

  # Create learner association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Learner Association Group - {uuid4()}"
  post_group = post_method(
      url=f"{UM_API_URL}/learner-association",
      request_body=association_group_dict)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

  group = AssociationGroup.find_by_uuid(context.group_uuid)
  group.users = [{"user": context.learner_id, "status": "active"}]
  group.associations = {
      "coaches": [{
          "coach": context.coach_id,
          "status": "active"
      }],
      "instructors": []
  }
  group.update()


@behave.when(
    "API request is sent to update User/Association status within Learner Association Group by providing invalid document id"
)
def step_impl_2(context):
  request_body = {
      "user": {
          "user_id": "random_user_id",
          "status": "inactive"
      },
      "coach": {
          "coach_id": context.coach_id,
          "status": "inactive"
      }
  }
  context.url = f"{UM_API_URL}/learner-association/{context.group_uuid}/user-association/status"
  context.res = put_method(url=context.url, request_body=request_body)
  context.res_data = context.res.json()


@behave.then(
    "User/Association Status will not be updated and User management will throw a Validation error"
)
def step_impl_3(context):
  assert context.res.status_code == 422
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == \
    "User for given user_id is not present in the learner association group"


# --- Negative Scenario_3 ---
@behave.given(
    "A Learner Association Group exists and user has privileges to update User/Association Status"
)
def step_impl_1(context):
  # Create Learner
  email_1 = str(uuid4())
  user_dict_1 = {**TEST_USER}
  user_dict_1["email"] = f"{email_1}@gmail.com"
  user_dict_1["user_type"] = "learner"
  user_dict_1["user_type_ref"] = ""
  user_1 = User.from_dict(user_dict_1)
  user_1.user_id = ""
  user_1.save()
  user_1.user_id = user_1.id
  user_1.update()
  user_dict_1["user_id"] = user_1.id
  context.learner_id = user_1.user_id

  email_2 = str(uuid4())
  user_dict_2 = {**TEST_USER}
  user_dict_2["email"] = f"{email_2}@gmail.com"
  user_dict_2["user_type"] = "coach"
  user_dict_2["user_type_ref"] = ""
  user_2 = User.from_dict(user_dict_2)
  user_2.user_id = ""
  user_2.save()
  user_2.user_id = user_2.id
  user_2.update()
  user_dict_2["user_id"] = user_2.id
  context.coach_id = user_2.user_id

  # Create learner association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Learner Association Group - {uuid4()}"
  post_group = post_method(
      url=f"{UM_API_URL}/learner-association",
      request_body=association_group_dict)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

  group = AssociationGroup.find_by_uuid(context.group_uuid)
  group.users = [{"user": context.learner_id, "status": "active"}]
  group.associations = {
      "coaches": [{
          "coach_id": context.coach_id,
          "status": "active"
      }],
      "instructors": []
  }
  group.update()


@behave.when(
    "API request is sent to update User/Association status within Learner Association Group by providing invalid status"
)
def step_impl_2(context):
  request_body = {
      "user": {
          "user_id": context.learner_id,
          "status": "random_status"
      },
      "coach": {
          "coach_id": context.coach_id,
          "status": "inactive"
      }
  }
  context.url = f"{UM_API_URL}/learner-association/{context.group_uuid}/user-association/status"
  context.res = put_method(url=context.url, request_body=request_body)
  context.res_data = context.res.json()


@behave.then(
    "User/Association Status will not be updated and User management will return a Validation error"
)
def step_impl_3(context):
  assert context.res.status_code == 422
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Validation Failed"


# --- Neative Scenario_4 ---
@behave.given(
    "A Learner Association Group, Discipline Association Group exists with user & discipline in inactive status"
)
def step_impl_1(context):
  # Create Learner
  email_1 = str(uuid4())
  user_dict_1 = {**TEST_USER}
  user_dict_1["email"] = f"{email_1}@gmail.com"
  user_dict_1["user_type"] = "learner"
  user_dict_1["user_type_ref"] = ""
  user_1 = User.from_dict(user_dict_1)
  user_1.user_id = ""
  user_1.save()
  user_1.user_id = user_1.id
  user_1.update()
  user_dict_1["user_id"] = user_1.id
  context.learner_id = user_1.user_id

  email_2 = str(uuid4())
  user_dict_2 = {**TEST_USER}
  user_dict_2["email"] = f"{email_2}@gmail.com"
  user_dict_2["user_type"] = "instructor"
  user_dict_2["user_type_ref"] = ""
  user_2 = User.from_dict(user_dict_2)
  user_2.user_id = ""
  user_2.save()
  user_2.user_id = user_2.id
  user_2.update()
  user_dict_2["user_id"] = user_2.id
  context.instructor_id = user_2.user_id

  # Create Curriculum Pathway - Discipline
  payload = deepcopy(TEST_CURRICULUM_PATHWAY)
  payload["alias"] = "discipline"
  curriculum_pathway = CurriculumPathway.from_dict(payload)
  curriculum_pathway.uuid = ""
  curriculum_pathway.version = 1
  curriculum_pathway.save()
  curriculum_pathway.uuid = curriculum_pathway.id
  curriculum_pathway.update()
  context.curriculum_pathway_id = curriculum_pathway.uuid

  # Create Discipline association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  post_group = post_method(
      url=f"{UM_API_URL}/discipline-association",
      request_body=association_group_dict)
  context.post_group_data = post_group.json()
  discipline_group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

  group = AssociationGroup.find_by_uuid(discipline_group_uuid)
  group.users = [{"user": context.instructor_id, "status": "inactive"}]
  group.associations = {
    "curriculum_pathways": [{"curriculum_pathway_id": context.curriculum_pathway_id,
                             "status": "active"}]
  }
  group.update()

  # Create learner association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Learner Association Group - {uuid4()}"
  post_group = post_method(
      url=f"{UM_API_URL}/learner-association",
      request_body=association_group_dict)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

  group = AssociationGroup.find_by_uuid(context.group_uuid)
  group.users = [{"user": context.learner_id, "status": "active"}]
  group.associations = {
    "coaches": [],
    "instructors": [{"instructor": context.instructor_id,
                     "curriculum_pathway_id": context.curriculum_pathway_id,
                     "status": "inactive"}]
  }
  group.update()


@behave.when(
    "API request is sent to activate an instructor for given instructor_id")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/learner-association/{context.group_uuid}/user-association/status"
  request_body = {
    "instructor": {"instructor_id": context.instructor_id,
                   "curriculum_pathway_id": context.curriculum_pathway_id,
                   "status": "active"}
  }
  context.res = put_method(url=context.url, request_body=request_body)
  context.res_data = context.res.json()


@behave.then(
    "The instructor for given instructor_id and curriculum_pathway_id will not get activated and ValidationError will be thrown"
)
def step_impl_3(context):
  error_message = "Instructor for given instructor_id " + \
    f"{context.instructor_id} is not actively associated with the given " + \
    f"curriculum_pathway_id {context.curriculum_pathway_id} in discipline association group"
  assert context.res.status_code == 422
  assert context.res_data["success"] is False, "Success is not False"
  assert context.res_data["message"] == error_message


@behave.given(
    "A user has permission to access user management, create correct request payload to add instructor and instructor is associated actively in discipline association group"
)
def step_impl_1(context) -> None:
  """
  construct request payload for API test to add instructor
  Returns
  -------
  None
  """
  #inserting the learning hierarchy
  context.json_file = TEST_LEARNING_HIERARCHY_PATH
  context.url = f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway/bulk-import/json"
  with open(context.json_file, encoding="UTF-8") as hierarchy_data:
    context.res = post_method(
        url=context.url, files={"json_file": hierarchy_data})

  assert context.res.status_code == 200, "Hierarchy Ingestion Failed"
  context.res_data = context.res.json()
  program_id = context.res_data["data"][0]
  context.res = get_method(
      url=f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway/{program_id}/nodes"
  )
  assert context.res.status_code == 200
  context.res_data = context.res.json()
  context.curriculum_pathway_id = context.res_data["data"][0]["uuid"]

  #make curriculam pathway as active
  context.res = put_method(
      url=f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway/{context.curriculum_pathway_id}",
      request_body = {"is_active": True}
  )
  assert context.res.status_code == 200

  context.res = get_method(
      url=f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway/{context.curriculum_pathway_id}"
  )
  assert context.res.status_code == 200
  context.res_data = context.res.json()
  assert context.res_data["data"]["is_active"] is True

  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Learner Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/learner-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

  email_1 = str(uuid4())
  user_dict_1 = {
      **TEST_USER, "email": f"{email_1}@gmail.com",
      "user_type": "instructor",
      "user_type_ref": ""
  }
  user_1 = User.from_dict(user_dict_1)
  user_1.user_id = ""
  user_1.save()
  user_1.user_id = user_1.id
  user_1.update()
  user_dict_1["user_id"] = user_1.id
  context.instructor_id = user_1.user_id

  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/discipline-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  discipline_group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

  discipline_group = AssociationGroup.find_by_uuid(discipline_group_uuid)
  discipline_group.users = [{
      "user": context.instructor_id,
      "user_type": "instructor",
      "status": "active"
  }]
  discipline_group.associations = {
    "curriculum_pathways": [
    {"curriculum_pathway_id": context.curriculum_pathway_id, "status": "active"}
    ]
  }
  discipline_group.update()


@behave.when("API request sent to add instructor to the learning association "
             "group")
def step_impl_2(context) -> None:
  """
  Send API request to add instructor
  Returns
  -------
  None
  """

  input_data = TEST_ADD_INSTRUCTOR
  input_data["instructors"] = [context.instructor_id]
  input_data["curriculum_pathway_id"] = context.curriculum_pathway_id
  context.post_group = post_method(url=f"{UM_API_URL}/learner-association"
                                       f"/{context.group_uuid}/instructors/add",
                                       request_body=input_data)
  context.post_group_data = context.post_group.json()


@behave.then("ensure the API response the instructor has been added")
def step_impl_3(context) -> None:
  """
  Ensure the API Response
  Returns
  -------
  None
  """
  assert context.post_group.status_code == 200
  assert context.post_group_data["success"] is True
  assert context.post_group_data["data"]["associations"]["instructors"] != []


@behave.given("A user has permission to access user management, create "
              "incorrect request payload to add instructor")
def step_impl_1(context) -> None:
  """
  construct request payload for API test to add instructor
  Returns
  -------
  None
  """

  context.input_data = {**TEST_ADD_INSTRUCTOR}


@behave.when("API request sent to add instructor to the learning association "
             "group with incorrect payload")
def step_impl_2(context) -> None:
  """
  Send API request to add instructor
  Returns
  -------
  None
  """

  context.post_group = post_method(
      url=f"{UM_API_URL}/learner-association"
      f"/123223323/instructors/add",
      request_body=context.input_data)
  context.post_group_data = context.post_group.json()


@behave.then("ensure the API response failed to add instructor")
def step_impl_3(context) -> None:
  """
  Ensure the API Response
  Returns
  -------
  None
  """
  assert context.post_group.status_code == 404
  assert context.post_group_data["success"] is False
  assert context.post_group_data["data"] is None


@behave.given(
    "A user has permission to access user management, create correct request payload to add instructor and instructor is not associated actively in discipline association group"
)
def step_impl_1(context) -> None:
  """
  construct request payload for API test to add instructor
  Returns
  -------
  None
  """
  #inserting the learning hierarchy
  context.json_file = TEST_LEARNING_HIERARCHY_PATH
  context.url = f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway/bulk-import/json"
  with open(context.json_file, encoding="UTF-8") as hierarchy_data:
    context.res = post_method(
        url=context.url, files={"json_file": hierarchy_data})

  assert context.res.status_code == 200, "Hierarchy Ingestion Failed"
  context.res_data = context.res.json()
  program_id = context.res_data["data"][0]
  context.res = get_method(
      url=f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway/{program_id}/nodes"
  )
  assert context.res.status_code == 200
  context.res_data = context.res.json()
  context.curriculum_pathway_id = context.res_data["data"][0]["uuid"]

  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Learner Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/learner-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

  email_1 = str(uuid4())
  user_dict_1 = {
      **TEST_USER, "email": f"{email_1}@gmail.com",
      "user_type": "instructor",
      "user_type_ref": ""
  }
  user_1 = User.from_dict(user_dict_1)
  user_1.user_id = ""
  user_1.save()
  user_1.user_id = user_1.id
  user_1.update()
  user_dict_1["user_id"] = user_1.id
  context.instructor_id = user_1.user_id

  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/discipline-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  discipline_group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

  discipline_group = AssociationGroup.find_by_uuid(discipline_group_uuid)
  discipline_group.users = [{
      "user": context.instructor_id,
      "user_type": "instructor",
      "status": "inactive"
  }]
  discipline_group.associations = {
    "curriculum_pathways": [
    {"curriculum_pathway_id": context.curriculum_pathway_id, "status": "active"}
    ]
  }
  discipline_group.update()


@behave.when(
    "API request sent to add instructor to the learner association group")
def step_impl_2(context) -> None:
  """
  Send API request to add instructor
  Returns
  -------
  None
  """

  input_data = TEST_ADD_INSTRUCTOR
  input_data["instructors"] = [context.instructor_id]
  input_data["curriculum_pathway_id"] = context.curriculum_pathway_id
  context.post_group = post_method(url=f"{UM_API_URL}/learner-association"
                                       f"/{context.group_uuid}/instructors/add",
                                       request_body=input_data)
  context.post_group_data = context.post_group.json()


@behave.then(
    "instructor will not get added and a ValidationError will be thrown")
def step_impl_3(context) -> None:
  """
  Ensure the API Response
  Returns
  -------
  None
  """
  error_message = "Instructors for given instructor_ids " + \
    f"{[context.instructor_id]} are not actively associated with the given " + \
    f"curriculum_pathway_id {context.curriculum_pathway_id} in discipline association group"
  assert context.post_group.status_code == 422
  assert context.post_group_data["success"] is False
  assert context.post_group_data["message"] == error_message



#-----------------GET ALL USERS FOR STAFF (INSTRUCTORS/COACH)----------------
# --- Positive Scenario ---
@behave.given(
    "A user has access to User management and needs to fetch all users associated to a valid instructor from all Learner Association Groups"
)
def step_impl_1(context):

  #inserting the learning hierarchy
  context.json_file = TEST_LEARNING_HIERARCHY_PATH
  context.url = f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway/bulk-import/json"
  with open(context.json_file, encoding="UTF-8") as hierarchy_data:
    context.res = post_method(
        url=context.url, files={"json_file": hierarchy_data})

  assert context.res.status_code == 200, "Hierarchy Ingestion Failed"
  context.res_data = context.res.json()
  context.program_id = context.res_data["data"][0]
  context.res = get_method(
      url=f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway/{context.program_id}/nodes"
  )
  assert context.res.status_code == 200
  context.res_data = context.res.json()
  context.curriculum_pathway_id = context.res_data["data"][0]["uuid"]

  #make program as active
  context.res = put_method(
      url=f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway/{context.program_id}",
      request_body = {"is_active": True}
  )
  assert context.res.status_code == 200

  context.res = get_method(
      url=f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway/{context.program_id}"
  )
  assert context.res.status_code == 200
  context.res_data = context.res.json()
  assert context.res_data["data"]["is_active"] is True

  # Create an empty learner association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Learner Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/learner-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

  # Create an instructor
  email_instructor = str(uuid4())
  instructor_dict = {
      **TEST_USER, "email": f"{email_instructor}@gmail.com",
      "user_type": "instructor",
      "user_type_ref": ""
  }
  instructor = User.from_dict(instructor_dict)
  instructor.user_id = ""
  instructor.save()
  instructor.user_id = instructor.id
  instructor.update()
  context.instructor_id = instructor.id

  context.staff_type = instructor_dict["user_type"]

  # Create a blank discipline association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/discipline-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  discipline_group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

  # Add instructor to the discipline association for the discipline id
  discipline_group = AssociationGroup.find_by_uuid(discipline_group_uuid)
  discipline_group.users = [{
      "user": context.instructor_id,
      "user_type": "instructor",
      "status": "active"
  }]
  discipline_group.associations = {
    "curriculum_pathways": [
    {"curriculum_pathway_id": context.curriculum_pathway_id, "status": "active"}
    ]
  }
  discipline_group.update()

  # Create learners to be added to learner association group
  # Create a learner
  email_user_1 = str(uuid4())
  user_dict_1 = {**TEST_USER, "email": f"{email_user_1}@gmail.com",
      "user_type_ref": ""}
  user_1 = User.from_dict(user_dict_1)
  user_1.user_id = ""
  user_1.save()
  user_1.user_id = user_1.id
  user_1.update()
  user_dict_1["user_id"] = user_1.id

  # Create another learner
  email_user_2 = str(uuid4())
  user_dict_2 = {**TEST_USER, "email": f"{email_user_2}@gmail.com",
      "user_type_ref": ""}
  user_2 = User.from_dict(user_dict_2)
  user_2.user_id = ""
  user_2.save()
  user_2.user_id = user_2.id
  user_2.update()

  # Add all the learners in a set
  context.set_users = set([user_1.id, user_2.id])

  # Add the instructor to the learner association group for the discipline
  input_data = TEST_ADD_INSTRUCTOR
  input_data["instructors"] = [context.instructor_id]
  input_data["curriculum_pathway_id"] = context.curriculum_pathway_id
  context.post_group = post_method(url=f"{UM_API_URL}/learner-association"
                                       f"/{context.group_uuid}/instructors/add",
                                       request_body=input_data)
  context.post_group_data = context.post_group.json()
  assert context.post_group.status_code == 200
  assert context.post_group_data["success"] is True
  assert len(context.post_group_data["data"]["associations"]["instructors"]) == 1

  # Add the users to the learner association group
  input_data = {}
  input_data["users"] = [user_1.id, user_2.id]
  input_data["status"] = "active"
  context.post_group = post_method(url=f"{UM_API_URL}/learner-association"
                                       f"/{context.group_uuid}/users/add",
                                       request_body=input_data)
  context.post_group_data = context.post_group.json()
  assert context.post_group.status_code == 200
  assert context.post_group_data["success"] is True
  assert len(context.post_group_data["data"]["users"]) == 2

  context.url = f"{UM_API_URL}/learner-association/instructor/"+\
    f"{context.instructor_id}/learners"


@behave.when(
  "API request is sent to fetch all users associated to a valid active instructor"
)
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()  

@behave.then(
  "User management will return a list of all active users associated to the instructor"
)
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == \
          "Successfully fetched the learners for the given instructor"
  fetched_uuids = context.res_data.get("data")
  assert (set(fetched_uuids) & context.set_users) == context.set_users,\
    "All users associated to the coach are not fetched from Association Group"


# --- Positive Scenario ---
@behave.given(
    "A user has access to User management and needs to fetch all users associated to a valid coach from all Learner Association Groups"
)
def step_impl_1(context):

  # Create a learner
  user_dict_1 = {**TEST_USER, "user_type_ref": ""}
  user_1 = User.from_dict(user_dict_1)
  user_1.user_id = ""
  user_1.save()
  user_1.user_id = user_1.id
  user_1.update()
  user_dict_1["user_id"] = user_1.id

  # Create another learner
  user_dict_2 = {**TEST_USER, "user_type_ref": ""}
  user_2 = User.from_dict(user_dict_2)
  user_2.user_id = ""
  user_2.save()
  user_2.user_id = user_2.id
  user_2.update()

  # Add all the learners in a set
  context.set_users = set([user_1.id, user_2.id])

  # Create a coach
  coach_dict = {**TEST_USER, "user_type": "coach",
                  "user_type_ref": ""}
  coach = User.from_dict(coach_dict)
  coach.user_id = ""
  coach.save()
  coach.user_id = coach.id
  coach.update()

  context.staff_type = coach_dict["user_type"]

  # Add all users and coach to an association group
  association_group_dict = {**TEST_LEARNER_ASSOCIATION_GROUP}
  association_group_dict["users"] = [{"user": user_1.id, "status": "active"},
                  {"user": user_2.id, "status": "active"}]
  association_group_dict["associations"]["coaches"] = \
                  [{"coach": coach.id, "status": "active"}]

  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()
  context.payload = association_group_dict

  context.url = f"{UM_API_URL}/learner-association/coach/"+\
    f"{coach.id}/learners"


@behave.when("API request is sent to fetch all users associated to a valid active coach")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()  


@behave.then("User management will return a list of all active users associated to the coach")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == \
          "Successfully fetched the learners for the given coach"
  fetched_uuids = context.res_data.get("data")
  assert (set(fetched_uuids) & context.set_users) == context.set_users,\
    "All users associated to the coach are not fetched from Association Group"


# --- Negative Scenario ---
@behave.given(
    "A user has access to User management and needs to fetch all users associated to an invalid coach from all Learner Association Groups"
)
def step_impl_1(context):

  context.coach_id = str(uuid4())
  context.url = f"{UM_API_URL}/learner-association/coach/"+\
    f"{context.coach_id}/learners"


@behave.when("API request is sent to fetch all users associated to an invalid coach")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()  


@behave.then("Users will not be returned and Resource not found error will be thrown by User management")
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False, "success not False"
  assert context.res_data["message"] == \
      f"User with user_id {context.coach_id} not found"




@behave.given(
    "A user has permission to access user management, create correct request payload to remove instructor"
)
def step_impl_1(context) -> None:
  """
  construct request payload for API test to add instructor
  Returns
  -------
  None
  """
  #inserting the learning hierarchy
  context.json_file = TEST_LEARNING_HIERARCHY_PATH
  context.url = f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway/bulk-import/json"
  with open(context.json_file, encoding="UTF-8") as hierarchy_data:
    context.res = post_method(
        url=context.url, files={"json_file": hierarchy_data})

  assert context.res.status_code == 200, "Hierarchy Ingestion Failed"
  context.res_data = context.res.json()
  program_id = context.res_data["data"][0]
  context.res = get_method(
      url=f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway/{program_id}/nodes"
  )
  assert context.res.status_code == 200
  context.res_data = context.res.json()
  context.curriculum_pathway_id = context.res_data["data"][0]["uuid"]

  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Learner Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/learner-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

  email_1 = str(uuid4())
  user_dict_1 = {
      **TEST_USER, "email": f"{email_1}@gmail.com",
      "user_type": "instructor",
      "user_type_ref": ""
  }
  user_1 = User.from_dict(user_dict_1)
  user_1.user_id = ""
  user_1.save()
  user_1.user_id = user_1.id
  user_1.update()
  user_dict_1["user_id"] = user_1.id
  context.instructor_id = user_1.user_id

  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/discipline-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  discipline_group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

  discipline_group = AssociationGroup.find_by_uuid(discipline_group_uuid)
  discipline_group.users = [{
      "user": context.instructor_id,
      "user_type": "instructor",
      "status": "active"
  }]
  discipline_group.associations = {
    "curriculum_pathways": [
    {"curriculum_pathway_id": context.curriculum_pathway_id, "status": "active"}
    ]
  }
  discipline_group.update()


@behave.when(
    "API request sent to remove instructor to the learning association group")
def step_impl_2(context) -> None:
  """
  Send API request to add instructor
  Returns
  -------
  None
  """

  input_data = TEST_ADD_INSTRUCTOR
  input_data["instructors"] = [context.instructor_id]
  input_data["curriculum_pathway_id"] = context.curriculum_pathway_id
  res = post_method(url=f"{UM_API_URL}/learner-association"
                                   f"/{context.group_uuid}/instructors/add",
                                       request_body=input_data)
  data = TEST_REMOVE_INSTRUCTOR
  data["instructor"] = context.instructor_id
  data["curriculum_pathway_id"] = context.curriculum_pathway_id
  context.post_group = post_method(url=f"{UM_API_URL}/learner-association"
                                   f"/{context.group_uuid}/instructor/remove",
                                   request_body=data)
  context.post_group_data = context.post_group.json()


@behave.then("ensure the API response the instructor has been removed")
def step_impl_3(context) -> None:
  """
  Ensure the API Response
  Returns
  -------
  None
  """
  assert context.post_group.status_code == 200
  assert context.post_group_data["success"] is True


@behave.given("A user has permission to access user management, create "
              "incorrect request payload to remove instructor")
def step_impl_1(context) -> None:
  """
  construct request payload for API test to add instructor
  Returns
  -------
  None
  """

  context.input_data = {**TEST_REMOVE_INSTRUCTOR}


@behave.when("API request sent to remove instructor to the learning "
             "association group with incorrect payload")
def step_impl_2(context) -> None:
  """
  Send API request to add instructor
  Returns
  -------
  None
  """

  context.post_group = post_method(
      url=f"{UM_API_URL}/learner-association"
      f"/123223323/instructor/remove",
      request_body=context.input_data)
  context.post_group_data = context.post_group.json()


@behave.then("ensure the API response failed to remove instructor")
def step_impl_3(context) -> None:
  """
  Ensure the API Response
  Returns
  -------
  None
  """

  assert context.post_group.status_code == 404
  assert context.post_group_data["success"] is False
  assert context.post_group_data["data"] is None


@behave.given(
    "A user had permission to access user management, create incorrect request payload to add instructor"
)
def step_impl_1(context) -> None:
  """
  construct request payload for API test to add instructor
  Returns
  -------
  None
  """
  #inserting the learning hierarchy
  context.json_file = TEST_LEARNING_HIERARCHY_PATH
  context.url = f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway/bulk-import/json"
  with open(context.json_file, encoding="UTF-8") as hierarchy_data:
    context.res = post_method(
        url=context.url, files={"json_file": hierarchy_data})

  assert context.res.status_code == 200, "Hierarchy Ingestion Failed"
  context.res_data = context.res.json()
  program_id = context.res_data["data"][0]
  context.res = get_method(
      url=f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway/{program_id}/nodes"
  )
  assert context.res.status_code == 200
  context.res_data = context.res.json()
  context.pathway_id = context.res_data["data"][0]["uuid"]

  # creating learner association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Learner Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/learner-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

  # creating the user
  context.user_dict = {
      **TEST_USER, "email": f"{uuid4()}@gmail.com",
      "user_type": "faculty"
  }
  context.url = f"{API_URL_USER_MANAGEMENT}/user"
  context.post_user_res = post_method(
      url=context.url, request_body=context.user_dict)
  assert context.post_user_res.status_code == 200
  context.post_user_res_dict = context.post_user_res.json()["data"]
  context.faculty_id = context.post_user_res_dict["user_id"]

  payload = TEST_CURRICULUM_PATHWAY
  curriculum_pathway = CurriculumPathway.from_dict(payload)
  curriculum_pathway.alias = "discipline"
  curriculum_pathway.uuid = ""
  curriculum_pathway.version = 1
  curriculum_pathway.save()
  curriculum_pathway.uuid = curriculum_pathway.id
  curriculum_pathway.update()

  context.discipline_pathway_id = curriculum_pathway.uuid


@behave.when(
    "API request sent to add instructor in the learning association group incorrect discipline_id in the payload"
)
def step_impl_2(context) -> None:
  """
  Send API request to add instructor
  Returns
  -------
  None
  """

  input_data = TEST_ADD_INSTRUCTOR
  input_data["instructors"] = [context.faculty_id]
  input_data["curriculum_pathway_id"] = context.discipline_pathway_id
  context.post_group = post_method(
      url=f"{UM_API_URL}/learner-association"
      f"/{context.group_uuid}/instructors/add",
      request_body=input_data)
  context.post_group_data = context.post_group.json()


@behave.then("validation error will thrown")
def step_impl_3(context) -> None:
  """
  Ensure the API Response
  Returns
  -------
  None
  """
  assert context.post_group.status_code == 422
  assert context.post_group_data["success"] is False
