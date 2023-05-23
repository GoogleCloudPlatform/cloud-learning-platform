"""
Feature: CRUD for managing Discipline Association Group in user management
"""
import behave
import sys
from copy import deepcopy
from uuid import uuid4

sys.path.append("../")
from common.models import AssociationGroup, User, CurriculumPathway
from e2e.test_object_schemas import (TEST_ASSOCIATION_GROUP, TEST_USER,
                                TEST_CURRICULUM_PATHWAY, TEST_CURRICULUM_PATHWAY_2)
from e2e.test_config import (API_URL_USER_MANAGEMENT, DEL_KEYS)
from e2e.setup import create_immutable_user_groups, post_method, get_method, put_method, delete_method

UM_API_URL = f"{API_URL_USER_MANAGEMENT}/association-groups"

# -------------------------------CREATE GROUP----------------------------------

@behave.given("A user has permission to user management and wants to create a Discipline Association Group")
def step_impl_1(context):

  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  context.request_body = association_group_dict


@behave.when("API request is sent to create Discipline Association Group with correct request payload")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association"

  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()


@behave.then("Discipline Association Group object will be created in the database as per given request payload")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["message"] == "Successfully created the association group"
  association_group_uuid = context.res_data["data"]["uuid"]
  url = f"{UM_API_URL}/discipline-association/{association_group_uuid}"
  request = get_method(url)
  group_data = request.json()
  assert request.status_code == 200
  assert group_data["success"] is True
  assert group_data["message"] == "Successfully fetched the association group"
  assert group_data["data"]["name"] == context.request_body["name"]
  assert group_data["data"]["association_type"] == "discipline"
  assert group_data["data"]["associations"] == {"curriculum_pathways": []}


# --- Negative Scenario 1 ---
@behave.given("A user has permission to user management and wants to create a Discipline Association Group with incorrect payload")
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  context.payload = association_group_dict
  del context.payload["name"]
  context.url = f"{UM_API_URL}/discipline-association"


@behave.when("API request is sent to create Discipline Association Group with incorrect request payload")
def step_impl_2(context):
  context.res = post_method(url=context.url, request_body=context.payload)
  context.res_data = context.res.json()


@behave.then("Discipline Association Group object will not be created and a validation error is thrown")
def step_impl_3(context):
  assert context.res.status_code == 422
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Validation Failed"
  assert context.res_data["data"][0]["msg"] == "field required"
  assert context.res_data["data"][0]["type"] == "value_error.missing"


# --- Negative Scenario 2 ---
@behave.given("A user has permission to user management and wants to create a Discipline Association Group with name already existing in database")
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  context.association_group_name = association_group_dict["name"]
  context.url = f"{UM_API_URL}/discipline-association"
  post_res = post_method(url=context.url, request_body=association_group_dict)
  assert post_res.status_code == 200
  post_res_data = post_res.json()
  assert post_res_data["success"] is True

  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = context.association_group_name
  context.payload = association_group_dict

@behave.when("API request is sent to create Discipline Association Group with name already existing in database")
def step_impl_2(context):
  context.res = post_method(url=context.url, request_body=context.payload)
  context.res_data = context.res.json()


@behave.then("Discipline Association Group object will not be created and a conflict error is thrown")
def step_impl_3(context):
  assert context.res.status_code == 409
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == \
    f"AssociationGroup with the given name: {context.association_group_name} already exists"

# -------------------------------GET GROUP-------------------------------------
# --- Positive Scenario ---
@behave.given("A user has access privileges to User management and needs to fetch a Discipline Association Group")
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/discipline-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  context.association_group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200


@behave.when("API request is sent to fetch Discipline Association Group by providing correct uuid")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association/{context.association_group_uuid}"
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Discipline Association Group object corresponding to given uuid will be returned successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == "Successfully fetched the association group"
  assert context.res_data["data"] == context.post_group_data["data"]


# --- Negative Scenario_1 ---
@behave.given("A user has access to User management and needs to fetch a Discipline Association Group")
def step_impl_1(context):
  invalid_group_uuid = "random_id"
  context.url = f"{UM_API_URL}/discipline-association/{invalid_group_uuid}"


@behave.when("API request is sent to fetch Discipline Association Group by providing invalid uuid")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Discipline Association Group object will not be returned and Resource not found error will be thrown by User management")
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False, "success not False"
  assert context.res_data["message"] == \
        "AssociationGroup with uuid random_id not found"


# --- Negative Scenario_2 ---
@behave.given("A user has access to User management and needs to fetch a Association Group of Discipline Type")
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/learner-association",
      request_body=context.payload)
  context.post_group_data = post_group.json()
  context.association_group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200


@behave.when("API request is sent to fetch Discipline Association Group by providing uuid for Learner Association Group")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association/{context.association_group_uuid}"
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Discipline Association Group object will not be returned and Validation error will be thrown by User management")
def step_impl_3(context):
  assert context.res.status_code == 422
  context.res_data = context.res.json()
  assert context.res_data["success"] is False, "success not False"
  assert context.res_data["message"] == \
    f"AssociationGroup for given uuid: {context.association_group_uuid} is not discipline type"


#-------------------------------GET ALL GROUPS-----------------------------------
# --- Positive Scenario ---
@behave.given("A user has access to User management and needs to fetch all Discipline Association Groups")
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/discipline-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200
  context.url = f"{UM_API_URL}/discipline-associations"


@behave.when("API request is sent to fetch all Discipline Association Groups")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("User management will return all existing Discipline Association Group objects successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == \
              "Successfully fetched the association groups"
  fetched_uuids = [i.get("uuid") for i in context.res_data.get(
    "data")["records"]]
  assert context.group_uuid in fetched_uuids


# --- Negative Scenario ---
@behave.given("A user can access User management and needs to fetch all Discipline Association Groups")
def step_impl_1(context):
  context.url = f"{UM_API_URL}/discipline-associations"
  context.params = params = {"skip": "-1", "limit": "10"}


@behave.when("API request is sent to fetch all Discipline Association Groups with incorrect params")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()


@behave.then("No Discipline Association Groups will be fetched and User management will throw a Validation error")
def step_impl_3(context):
  assert context.res.status_code == 422, "Status not 422"
  assert context.res_data.get("message") == \
    "Validation Failed", \
    "unknown response received"


#-------------------------------UPDATE GROUP-------------------------------------
# --- Positive Scenario ---
@behave.given("A user has access to User management and needs to update a Discipline Association Group")
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/discipline-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200


@behave.when("API request is sent to update Discipline Association Group with correct request payload")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association/{context.group_uuid}"
  updated_data = context.payload
  updated_data["description"] = "updated description"
  updated_data["name"] = f"Updated Discipline Association Group - {uuid4()}"
  context.association_group_name = updated_data["name"]
  context.res = put_method(url=context.url, request_body=updated_data)
  context.res_data = context.res.json()


@behave.then("The corresponding Discipline Association Group object will be updated successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == \
                "Successfully updated the association group"
  assert context.res_data["data"]["description"] == "updated description"
  assert context.res_data["data"]["name"] == context.association_group_name


# --- Negative Scenario_1 ---
@behave.given("A user has access privileges to User management and needs to update a Discipline Association Group")
def step_impl_1(context):
  invalid_group_uuid = "random_id"
  context.url = f"{UM_API_URL}/discipline-association/{invalid_group_uuid}"


@behave.when("API request is sent to update Discipline Association Group by providing invalid uuid")
def step_impl_2(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"

  context.res = put_method(url=context.url, request_body=association_group_dict)
  context.res_data = context.res.json()


@behave.then("Discipline Association Group object will not be updated and User management will throw a resource not found error")
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == \
            "AssociationGroup with uuid random_id not found"


# --- Negative Scenario_2 ---
@behave.given("A user has permission to user management and wants to update name in Discipline Group thats already exists in database")
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  context.association_group_name = association_group_dict["name"]
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/discipline-association", request_body=context.payload)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200


@behave.when("API request is sent to update Discipline Association Group with name already existing in database")
def step_impl_2(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = context.association_group_name
  association_group_dict["description"] = "Updated description"
  context.url = f"{UM_API_URL}/discipline-association/{context.group_uuid}"
  context.res = put_method(url=context.url, request_body=association_group_dict)
  context.res_data = context.res.json()


@behave.then("Discipline Association Group object will not be updated and a conflict error is thrown")
def step_impl_3(context):
  assert context.res.status_code == 409
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == \
    f"AssociationGroup with the given name: {context.association_group_name} already exists"


# --- Negative Scenario_3 ---
@behave.given("A user has access to User management and needs to update a Association Group of Discipline Type")
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Learner Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/learner-association",
      request_body=context.payload)
  context.post_group_data = post_group.json()
  context.association_group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200


@behave.when("API request is sent to update Discipline Association Group by providing uuid for Learner Association Group")
def step_impl_2(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  association_group_dict["description"] = "Updated description"
  context.url = f"{UM_API_URL}/discipline-association/{context.association_group_uuid}"
  context.res = put_method(url=context.url, request_body=association_group_dict)
  context.res_data = context.res.json()


@behave.then("Discipline Association Group object will not be updated and Validation error will be thrown by User management")
def step_impl_3(context):
  assert context.res.status_code == 422
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == \
    f"AssociationGroup for given uuid: {context.association_group_uuid} is not discipline type"


#-------------------------------DELETE GROUP-------------------------------------
# --- Positive Scenario ---
@behave.given("A user has access to User management and needs to delete a Discipline Association Group")
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
  


@behave.when("API request is sent to delete Discipline Association Group by providing correct uuid")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association/{context.group_uuid}"
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Discipline Association Group object will be deleted successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == \
                "Successfully deleted the association group"
  
@behave.then("the discipline association will also get removed from all Learner Association Group where it exists")
def step_impl_3(context):
  learner_group_url = f"{UM_API_URL}/learner-association/{context.learner_group_uuid}"
  get_response = get_method(learner_group_url)
  get_response_data = get_response.json()
  assert get_response.status_code == 200
  assert len(get_response_data["data"]["associations"]["instructors"]) == 0


# --- Negative Scenario_1 ---
@behave.given("A user has access privileges to User management and needs to delete an Discipline Association Group")
def step_impl_1(context):
  invalid_group_uuid = "random_id"
  context.url = f"{UM_API_URL}/discipline-association/{invalid_group_uuid}"


@behave.when("API request is sent to delete Discipline Association Group by providing invalid uuid")
def step_impl_2(context):
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Discipline Association Group object will not be deleted and User management will throw a resource not found error")
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "AssociationGroup with uuid random_id not found"


# --- Negative Scenario_2 ---
@behave.given("A user has access to User management and needs to delete a Association Group of Discipline Type")
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Learner Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
      url=f"{UM_API_URL}/learner-association",
      request_body=context.payload)
  context.post_group_data = post_group.json()
  context.association_group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200


@behave.when("API request is sent to delete Discipline Association Group by providing uuid for Learner Association Group")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association/{context.association_group_uuid}"
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Discipline Association Group object will not be deleted and Validation error will be thrown by User management")
def step_impl_3(context):
  assert context.res.status_code == 422
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == f"AssociationGroup for given uuid: {context.association_group_uuid} is not discipline type"


#-------------------------------GET ALL USERS-------------------------------------
# --- Positive Scenario 1---
@behave.given("A user has access to User management and needs to fetch all users belonging to given discipline")
def step_impl_1(context):
  # ------create users-----------
  users_uuids = []
  for i in range(5):
    users_dict = deepcopy(TEST_USER)
    users_dict["email"] = f"e2e-ag-{uuid4()}@gmail.com"

    post_users = post_method(
      url=f"{API_URL_USER_MANAGEMENT}/user",
      request_body=users_dict
    )
    post_users_data = post_users.json()
    users_uuids.append(post_users_data["data"]["user_id"])
    assert post_users.status_code == 200

  users = []
  for i, uuid in enumerate(users_uuids):
    doc = {"user": uuid, "status": ""}
    doc["user_type"] = "assessor" if i%2 == 1 else "instructor"
    users.append(doc)

  # ---------create curriculum pathway-------------
  curriculum_pathway_dict = deepcopy(TEST_CURRICULUM_PATHWAY_2)
  curriculum_pathway_dict["name"] = f"Test CP - {uuid4()}"
  curriculum_pathway_dict["alias"] = "discipline"
  
  cp = CurriculumPathway.from_dict(curriculum_pathway_dict)
  cp.uuid = ""
  cp.save()
  cp.uuid = cp.id
  cp.update()
  context.discipline_uuid = cp.id
  associations = {
    "curriculum_pathways": [{"curriculum_pathway_id":context.discipline_uuid,"status":"active"}]
  }

  # -----------create association group----------------
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
    url=f"{UM_API_URL}/discipline-association",
    request_body=context.payload
  )
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]

  group = AssociationGroup.find_by_uuid(context.group_uuid)
  group.users = users
  group.associations = associations
  group.update()

  assert post_group.status_code == 200


@behave.when("API request is sent to fetch all users by providing uuid for discipline")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association/{context.discipline_uuid}/users"
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()
  

@behave.then("Users associated with provided discipline uuid will be returned")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] == True
  assert context.res_data["message"] == "Successfully fetched the users"
  assert len(context.res_data["data"]) == 5


# --- Positive Scenario 2---
@behave.given("A user has access to User management and needs to fetch all instructors belonging to given discipline")
def step_impl_1(context):
  # ------create users-----------
  users_uuids = []
  for i in range(5):
    users_dict = deepcopy(TEST_USER)
    users_dict["email"] = f"e2e-ag-{uuid4()}@gmail.com"

    post_users = post_method(
      url=f"{API_URL_USER_MANAGEMENT}/user",
      request_body=users_dict
    )
    post_users_data = post_users.json()
    users_uuids.append(post_users_data["data"]["user_id"])
    assert post_users.status_code == 200

  users = []
  for i, uuid in enumerate(users_uuids):
    doc = {"user": uuid, "status": ""}
    doc["user_type"] = "assessor" if i%2 == 1 else "instructor"
    users.append(doc)

  # ---------create curriculum pathway-------------
  curriculum_pathway_dict = deepcopy(TEST_CURRICULUM_PATHWAY_2)
  curriculum_pathway_dict["name"] = f"Test CP - {uuid4()}"
  curriculum_pathway_dict["alias"] = "discipline"
  
  cp = CurriculumPathway.from_dict(curriculum_pathway_dict)
  cp.uuid = ""
  cp.save()
  cp.uuid = cp.id
  cp.update()
  context.discipline_uuid = cp.id
  associations = {
  "curriculum_pathways": [
    {"curriculum_pathway_id": context.discipline_uuid, "status": "active"}]
  }

  # -----------create association group----------------
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(
    url=f"{UM_API_URL}/discipline-association",
    request_body=context.payload
  )
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]

  group = AssociationGroup.find_by_uuid(context.group_uuid)
  group.users = users
  group.associations = associations
  group.update()

  assert post_group.status_code == 200


@behave.when("API request is sent to fetch all instructors by providing uuid for discipline")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association/discipline/{context.discipline_uuid}/users"
  params = {"user_type": "instructor"}
  context.res = get_method(url=context.url, query_params=params)
  context.res_data = context.res.json()
  

@behave.then("Instructors associated with provided discipline uuid will be returned")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] == True
  assert context.res_data["message"] == "Successfully fetched the users"
  assert len(context.res_data["data"]) == 3


# --- Negative Scenario 1---
@behave.given("A user has access to User management and needs to fetch all assessors belonging to given discipline using non-existent discipline uuid")
def step_impl_1(context):
  context.discipline_uuid = "random_uuid"


@behave.when("API request is sent to fetch all assessors by providing non-existent uuid for discipline")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association/discipline/{context.discipline_uuid}/users"
  params = {"user_type": "assessor"}
  context.res = get_method(url=context.url, query_params=params)
  context.res_data = context.res.json()
  

@behave.then("Assessors will not be returned and resource not found error will be thrown")
def step_impl_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] == False
  assert context.res_data["message"] == f"Curriculum Pathway with uuid {context.discipline_uuid} not found"
  assert context.res_data["data"] == None


# --- Negative Scenario 2---
@behave.given("A user has access to User management and needs to fetch all assessors belonging to given discipline")
def step_impl_1(context):
  context.discipline_uuid = "random_uuid"


@behave.when("API request is sent to fetch all assessors by providing incorrect filter parameter")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association/discipline/{context.discipline_uuid}/users"
  params = {"user_type": "instruct"}
  context.res = get_method(url=context.url, query_params=params)
  context.res_data = context.res.json()
  

@behave.then("Assessors will not be returned and validation error will be thrown")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] == False
  assert context.res_data["message"] == "Validation Failed"


# --- Negative Scenario 3---
@behave.given("A user has access to User management and needs to fetch all instructors belonging to given discipline whose alias is not discipline")
def step_impl_1(context):
  # ---------create curriculum pathway-------------
  curriculum_pathway_dict = deepcopy(TEST_CURRICULUM_PATHWAY_2)
  curriculum_pathway_dict["name"] = f"Test CP - {uuid4()}"
  curriculum_pathway_dict["alias"] = "program"
  
  cp = CurriculumPathway.from_dict(curriculum_pathway_dict)
  cp.uuid = ""
  cp.save()
  cp.uuid = cp.id
  cp.update()
  context.discipline_uuid = cp.id


@behave.when("API request is sent to fetch all instructors by providing invalid discipline uuid")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association/discipline/{context.discipline_uuid}/users"
  params = {"user_type": "instructor"}
  context.res = get_method(url=context.url, query_params=params)
  context.res_data = context.res.json()
  

@behave.then("Instructors will not be returned and validation error will be thrown for invalid alias")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] == False
  assert context.res_data["message"] == f"Given curriculum pathway id {context.discipline_uuid} is not of discipline type"
  assert context.res_data["data"] == None


#-----------------------UPDATE USER/ASSOCIATION STATUS--------------------
# --- Positive Scenario 1 ---
@behave.given("A Discipline Association Group exists and user has access to User management to update User/Association Status")
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


@behave.when("API request is sent to update User/Association Status of a Discipline Association Group with correct request payload")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association/{context.group_uuid}/user-association/status"
  request_body = {
    "user": {"user_id": context.instructor_id, "status": "inactive"},
    "curriculum_pathway": {"curriculum_pathway_id": context.discipline_id, "status": "inactive"}
  }
  context.res = put_method(url=context.url, request_body=request_body)
  context.res_data = context.res.json()


@behave.then("The status of User/Association within the Discipline Association Group object will be updated successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == \
                "Successfully updated the association group"
  assert context.res_data["data"]["users"][0]["status"] == "inactive"
  assert context.res_data["data"]["associations"]["curriculum_pathways"][0][
    "status"] == "inactive", f"{context.res_data['data']['associations']}"


# --- Positive Scenario 2 ---
@behave.given("A Discipline Association Group exists and user has access to User management to update User Status")
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


@behave.when("API request is sent to update Status of user type of instructor in Discipline Association Group with correct request payload")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association/{context.group_uuid}/user-association/status"
  request_body = {
    "user": {"user_id": context.instructor_id, "status": "inactive"},
    "curriculum_pathway": {"curriculum_pathway_id": context.discipline_id, "status": "inactive"}
  }
  context.res = put_method(url=context.url, request_body=request_body)
  context.res_data = context.res.json()

@behave.then("The status of Instructor type of User within the Discipline Association Group object will be updated successfully")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == \
                "Successfully updated the association group"
  assert context.res_data["data"]["users"][0]["status"] == "inactive"
  assert context.res_data["data"]["associations"]["curriculum_pathways"][0][
    "status"] == "inactive", f"{context.res_data['data']['associations']}"


@behave.then("status of the same Instructor existing in Learner ASsociation Group object will also be updated successfully")
def step_impl_3(context):
  learner_group_url = f"{UM_API_URL}/learner-association/{context.learner_group_uuid}"
  get_response = get_method(learner_group_url)
  get_response_data = get_response.json()
  assert get_response_data["data"]["associations"][
                  "instructors"][0]["status"] == "inactive"


# --- Positive Scenario 3 ---
@behave.given("A Discipline Association Group exists and user has access to User management to update assocaition status")
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


@behave.when("API request is sent to de-activate a discipline in Discipline Association Group with correct request payload")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association/{context.group_uuid}/user-association/status"
  request_body = {
    "curriculum_pathway": {"curriculum_pathway_id": context.discipline_id, "status": "inactive"}
  }
  context.res = put_method(url=context.url, request_body=request_body)
  context.res_data = context.res.json()

@behave.then("The status of discipline within the Discipline Association Group object will be updated as inactive")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data["message"] == \
                "Successfully updated the association group"
  assert context.res_data["data"]["associations"]["curriculum_pathways"][0][
    "status"] == "inactive", f"{context.res_data['data']['associations']}"


@behave.then("status of the same Instructor associated to the disicpline existing in any Learner ASsociation Group object will also be updated as Inactive")
def step_impl_3(context):
  learner_group_url = f"{UM_API_URL}/learner-association/{context.learner_group_uuid}"
  get_response = get_method(learner_group_url)
  get_response_data = get_response.json()
  assert get_response_data["data"]["associations"][
                  "instructors"][0]["status"] == "inactive"




# --- Negative Scenario_1 ---
@behave.given("A Discipline Association Group exists and user has access to update User/Association Status")
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

  invalid_group_uuid = "random_id"
  context.url = f"{UM_API_URL}/discipline-association/{invalid_group_uuid}/user-association/status"


@behave.when("API request is sent to update User/Association status within Discipline Association Group by providing invalid group uuid")
def step_impl_2(context):
  request_body = {
    "user": {"user_id": context.instructor_id, "status": "inactive"},
    "curriculum_pathway": {"curriculum_pathway_id": context.discipline_id, "status": "inactive"}
  }
  context.res = put_method(url=context.url, request_body=request_body)
  context.res_data = context.res.json()


@behave.then("User/Association Status will not be updated and a resource not found error will be returned")
def step_impl_3(context):
  assert context.res.status_code == 404
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == \
            "AssociationGroup with uuid random_id not found"


# --- Negative Scenario_2 ---
@behave.given("A Discipline Association Group exists and user has access privileges to update User/Association Status")
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


@behave.when("API request is sent to update User/Association status within Discipline Association Group by providing invalid document id")
def step_impl_2(context):
  request_body = {
    "user": {"user_id": "random_user_id", "status": "inactive"}
  }
  context.url = f"{UM_API_URL}/discipline-association/{context.group_uuid}/user-association/status"
  context.res = put_method(url=context.url, request_body=request_body)
  context.res_data = context.res.json()


@behave.then("User/Association Status will not be updated and a Validation error will be returned")
def step_impl_3(context):
  assert context.res.status_code == 422
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == \
    "User for given user_id is not present in the discipline association group"


# --- Negative Scenario_3 ---
@behave.given("A Discipline Association Group exists and user has privileges to update User/Association Status")
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


@behave.when("API request is sent to update User/Association status within Discipline Association Group by providing invalid status")
def step_impl_2(context):
  request_body = {
    "user": {"user_id": context.instructor_id, "status": "random_status"}
  }
  context.url = f"{UM_API_URL}/discipline-association/{context.group_uuid}/user-association/status"
  context.res = put_method(url=context.url, request_body=request_body)
  context.res_data = context.res.json()


@behave.then("User/Association Status will not get updated and User management will return a Validation Error")
def step_impl_3(context):
  assert context.res.status_code == 422
  context.res_data = context.res.json()
  assert context.res_data["success"] is False
  assert context.res_data["message"] == "Validation Failed"
