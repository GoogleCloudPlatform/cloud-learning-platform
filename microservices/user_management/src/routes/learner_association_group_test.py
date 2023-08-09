"""
  Unit tests for Learner association group endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import

import os

from copy import deepcopy
from fastapi import FastAPI
from fastapi.testclient import TestClient
from uuid import uuid4
from routes.learner_association_group import router
from testing.test_config import API_URL
from schemas.schema_examples import (BASIC_ASSOCIATION_GROUP_EXAMPLE,
                        BASIC_USER_MODEL_EXAMPLE,
                        ADD_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
                        BASIC_GROUP_MODEL_EXAMPLE,
                        BASIC_CURRICULUM_PATHWAY_EXAMPLE,
                        FULL_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
                        REMOVE_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE)

from common.models import AssociationGroup, User, UserGroup, CurriculumPathway
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/user-management/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/association-groups/learner-association"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_get_association_group(clean_firestore):
  """Get an association group with correct uuid"""
  association_group_dict = {
      **BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "learner"
  }
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  url = f"{api_url}/{association_group.uuid}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  assert json_response["data"]["association_type"] == \
         association_group_dict["association_type"]
  assert json_response["data"]["name"] == association_group_dict["name"]
  assert json_response["data"]["description"] == \
         association_group_dict["description"]


def test_get_association_group_negative(clean_firestore):
  """Get an association group with incorrect uuid"""
  uuid = "random_uuid"
  url = f"{api_url}/{uuid}"
  data = {
      "success": False,
      "message": f"AssociationGroup with uuid {uuid} not found",
      "data": None
  }

  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 404, "Status 404"
  assert json_response == data, "Response received"


def test_get_all_association_groups(clean_firestore):
  association_group_dict = {
      **BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "learner"
  }
  # association group
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  params_1 = {"skip": 0, "limit": "30"}
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params_1)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"
  retrieved_ids = [i.get("uuid") for i in json_response.get("data")["records"]]
  assert association_group.uuid in retrieved_ids, "expected data not retrieved"


def test_get_all_association_groups_negative_param(clean_firestore):
  association_group_dict = {
      **BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "learner"
  }
  # association group
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  params_1 = {"skip": 0, "limit": "-3"}
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params_1)
  json_response = resp.json()
  assert resp.status_code == 422, "Status should be 422"
  assert json_response["message"] == "Validation Failed"


def test_get_all_association_groups_negative(clean_firestore):
  association_group_dict = {
      **BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "learner"
  }
  # association group
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  params_1 = {"skip": 0, "limit": "105"}
  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params_1)
  json_response = resp.json()
  assert resp.status_code == 422, "Status should be 422"
  assert json_response["message"] == "Validation Failed"


def test_get_all_learner_ids_of_association_group(clean_firestore):
  # create learner
  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  user_obj = {
    "user": user.user_id,
    "status": "active"
  }
  association_group_dict = deepcopy(FULL_LEARNER_ASSOCIATION_GROUP_EXAMPLE)
  association_group_dict["association_type"] = "learner"
  association_group_dict["users"].append(user_obj)

  # create association group
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  params = {"skip": 0, "limit": 100, "fetch_tree": False}
  url = f"{api_url}/{association_group.uuid}/learners"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  assert json_response["data"]["records"][0].get("user") == user.user_id
  assert json_response["data"]["records"][0].get("status") == "active"


def test_get_all_learners_of_association_group(clean_firestore):
  # create learner
  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  user_obj = {
    "user": user.user_id,
    "status": "active"
  }
  association_group_dict = deepcopy(FULL_LEARNER_ASSOCIATION_GROUP_EXAMPLE)
  association_group_dict["association_type"] = "learner"
  association_group_dict["users"].append(user_obj)

  # create association group
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  params = {"skip": 0, "limit": 100, "fetch_tree": True}
  url = f"{api_url}/{association_group.uuid}/learners"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  print(json_response)
  assert resp.status_code == 200, "Status 200"
  assert json_response["data"]["records"][0].get(
      "user").get("user_id") == user.user_id
  assert json_response["data"]["records"][0].get("status") == "active"

def test_get_all_learners_of_association_group_with_status_param(
    clean_firestore):
  # create learner
  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  user_obj = {
    "user": user.user_id,
    "status": "inactive"
  }
  association_group_dict = deepcopy(FULL_LEARNER_ASSOCIATION_GROUP_EXAMPLE)
  association_group_dict["association_type"] = "learner"
  association_group_dict["users"].append(user_obj)

  # create association group
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  params = {"skip": 0, "limit": 100, "fetch_tree": True, "status": "inactive"}
  url = f"{api_url}/{association_group.uuid}/learners"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  print(json_response)
  assert resp.status_code == 200, "Status 200"
  assert json_response["data"]["records"][0].get(
      "user").get("user_id") == user.user_id
  assert json_response["data"]["records"][0].get("status") == "inactive"

def test_sort_all_learners_of_association_group(clean_firestore):
  # create learner
  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  user_obj = {
    "user": user.user_id,
    "status": "active"
  }
  association_group_dict = deepcopy(FULL_LEARNER_ASSOCIATION_GROUP_EXAMPLE)
  association_group_dict["association_type"] = "learner"
  association_group_dict["users"].append(user_obj)

  # create association group
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  params = {"skip": 0, "limit": 100, "fetch_tree": True,
            "sort_by": "email", "sort_order": "ascending"}
  url = f"{api_url}/{association_group.uuid}/learners"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  assert json_response["data"]["records"][0].get(
      "user").get("user_id") == user.user_id
  assert json_response["data"]["records"][0].get("status") == "active"


def test_get_all_learners_of_association_group_negative(clean_firestore):
  association_group_dict = deepcopy(FULL_LEARNER_ASSOCIATION_GROUP_EXAMPLE)
  association_group_dict["association_type"] = "learner"

  # create association group
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  params = {"skip": 0, "limit": 100, "fetch_tree": True}
  url = f"{api_url}/random_uuid/learners"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response["message"] == \
          "AssociationGroup with uuid random_uuid not found"
  assert json_response["success"] is False
  assert json_response["data"] is None


def test_get_all_coach_ids_of_association_group(clean_firestore):
  # create coach
  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  user_dict["user_type"] = "coach"
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  user_obj = {
    "coach": user.user_id,
    "status": "active"
  }
  association_group_dict = deepcopy(FULL_LEARNER_ASSOCIATION_GROUP_EXAMPLE)
  association_group_dict["association_type"] = "learner"
  association_group_dict["associations"]["coaches"].append(user_obj)

  # create association group
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  params = {"skip": 0, "limit": 100, "fetch_tree": False}
  url = f"{api_url}/{association_group.uuid}/coaches"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  assert json_response["data"]["records"][0].get("coach") == user.user_id
  assert json_response["data"]["records"][0].get("status") == "active"

def test_get_all_coach_ids_of_association_group_with_status_param(
    clean_firestore):
  # create coach
  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  user_dict["user_type"] = "coach"
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  user_obj = {
    "coach": user.user_id,
    "status": "inactive"
  }
  association_group_dict = deepcopy(FULL_LEARNER_ASSOCIATION_GROUP_EXAMPLE)
  association_group_dict["association_type"] = "learner"
  association_group_dict["associations"]["coaches"].append(user_obj)

  # create association group
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  params = {"skip": 0, "limit": 100, "fetch_tree": False,"status": "inactive"}
  url = f"{api_url}/{association_group.uuid}/coaches"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  assert json_response["data"]["records"][0].get("coach") == user.user_id
  assert json_response["data"]["records"][0].get("status") == "inactive"

def test_sort_all_coach_of_association_group(clean_firestore):
  # create coach
  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  user_dict["user_type"] = "coach"
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  user_obj = {
    "coach": user.user_id,
    "status": "active"
  }
  association_group_dict = deepcopy(FULL_LEARNER_ASSOCIATION_GROUP_EXAMPLE)
  association_group_dict["association_type"] = "learner"
  association_group_dict["associations"]["coaches"].append(user_obj)

  # create association group
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  params = {"skip": 0, "limit": 100, "fetch_tree": True,
            "sort_by": "last_name", "sort_oder": "descending"}
  url = f"{api_url}/{association_group.uuid}/coaches"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  assert json_response["data"]["records"][0].get("coach")["user_id"] == \
         user.user_id
  assert json_response["data"]["records"][0].get("status") == "active"



def test_get_all_coaches_of_association_group(clean_firestore):
  # create coach
  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  user_dict["user_type"] = "coach"
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  user_obj = {
    "coach": user.user_id,
    "status": "active"
  }
  association_group_dict = deepcopy(FULL_LEARNER_ASSOCIATION_GROUP_EXAMPLE)
  association_group_dict["association_type"] = "learner"
  association_group_dict["associations"]["coaches"].append(user_obj)

  # create association group
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  params = {"skip": 0, "limit": 100, "fetch_tree": True}
  url = f"{api_url}/{association_group.uuid}/coaches"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  assert json_response["data"]["records"][0].get(
      "coach").get("user_id") == user.user_id
  assert json_response["data"]["records"][0].get("status") == "active"


def test_get_all_coaches_of_association_group_negative(clean_firestore):
  association_group_dict = deepcopy(FULL_LEARNER_ASSOCIATION_GROUP_EXAMPLE)
  association_group_dict["association_type"] = "learner"

  # create association group
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  params = {"skip": 0, "limit": 100, "fetch_tree": True}
  url = f"{api_url}/random_uuid/coaches"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response["message"] == \
          "AssociationGroup with uuid random_uuid not found"
  assert json_response["success"] is False
  assert json_response["data"] is None


def test_get_all_instructor_ids_of_association_group(clean_firestore):
  # create coach
  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  user_dict["user_type"] = "instructor"
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  user_obj = {
    "instructor": user.user_id,
    "curriculum_pathway_id": "curr_path_id",
    "status": "active"
  }
  association_group_dict = deepcopy(FULL_LEARNER_ASSOCIATION_GROUP_EXAMPLE)
  association_group_dict["association_type"] = "learner"
  association_group_dict["associations"]["instructors"].append(user_obj)

  # create association group
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  params = {"skip": 0, "limit": 100, "fetch_tree": False}
  url = f"{api_url}/{association_group.uuid}/instructors"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  assert json_response["data"]["records"][0].get("instructor") == user.user_id
  assert json_response["data"]["records"][0].get(
      "curriculum_pathway_id") == "curr_path_id"
  assert json_response["data"]["records"][0].get("status") == "active"


def test_sort_all_instructor_of_association_group(clean_firestore):
  user_dict_1 = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  user_1 = User.from_dict(user_dict_1)
  user_1.user_id = ""
  user_1.save()
  user_1.user_id = user_1.id
  user_1.update()
  user_dict_1["user_id"] = user_1.id

  user_dict_2 = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  user_2 = User.from_dict(user_dict_2)
  user_2.user_id = ""
  user_2.save()
  user_2.user_id = user_2.id
  user_2.update()
  user_dict_2["user_id"] = user_2.id

  # Create curriculum pathway
  curriculum_pathway_id = create_curriculum_pathway(
    payload=BASIC_CURRICULUM_PATHWAY_EXAMPLE).uuid

  # Create Discipline Association Group
  discipline_group_dict = {
    **BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "discipline"
  }
  discipline_group = AssociationGroup.from_dict(discipline_group_dict)
  discipline_group.uuid = ""
  discipline_group.save()
  discipline_group.uuid = discipline_group.id
  discipline_group.update()

  discipline_group.users = [{"user": user_2.user_id, "status": "active"}]
  discipline_group.associations = {
    "curriculum_pathways": [{
      "curriculum_pathway_id": curriculum_pathway_id, "status": "active"
    }]
  }
  discipline_group.update()

  # Create Learner Association Group
  association_group_dict = {
    **BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "learner"
  }
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()
  association_group_uuid = association_group.id

  association_group.users = [{
    "user": user_1.user_id, "status": "active"
  }]
  association_group.associations = {"instructors": [
    {
      "instructor": user_2.user_id,
      "curriculum_pathway_id": curriculum_pathway_id,
      "status": "inactive"
    }]
  }
  association_group.update()

  url = f"{api_url}/{association_group_uuid}/user-association/status"
  request_body = {
    "instructor": {"instructor_id": user_2.user_id,
                   "curriculum_pathway_id": curriculum_pathway_id,
                   "status": "active"}
  }

  client_with_emulator.put(url, json=request_body)

  params = {"skip": 0, "limit": 100, "fetch_tree": True,
            "sort_by": "first_name", "sort_order": "ascending"}
  url = f"{api_url}/{association_group.uuid}/instructors"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  assert json_response["data"]["records"][0].get("instructor")["user_id"] == \
         user_2.user_id
  assert json_response["data"]["records"][0].get(
      "curriculum_pathway_id").get("uuid") == curriculum_pathway_id
  assert json_response["data"]["records"][0].get("status") == "active"


def test_get_all_instructors_of_association_group(clean_firestore):
  # create coach
  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  user_dict["user_type"] = "instructor"
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  # create curriculum pathway
  pathway = create_curriculum_pathway(BASIC_CURRICULUM_PATHWAY_EXAMPLE)

  user_obj = {
    "instructor": user.user_id,
    "curriculum_pathway_id": pathway.uuid,
    "status": "active"
  }
  association_group_dict = deepcopy(FULL_LEARNER_ASSOCIATION_GROUP_EXAMPLE)
  association_group_dict["association_type"] = "learner"
  association_group_dict["associations"]["instructors"].append(user_obj)

  # create association group
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  params = {"skip": 0, "limit": 100, "fetch_tree": True}
  url = f"{api_url}/{association_group.uuid}/instructors"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  assert json_response["data"]["records"][0].get("instructor").get(
                              "user_id") == user.user_id
  assert json_response["data"]["records"][0].get("curriculum_pathway_id").get(
                              "uuid") == pathway.uuid
  assert json_response["data"]["records"][0].get("status") == "active"

def test_get_all_instructors_of_association_group_with_status_param(
    clean_firestore):
  # create coach
  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  user_dict["user_type"] = "instructor"
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()

  # create curriculum pathway
  pathway = create_curriculum_pathway(BASIC_CURRICULUM_PATHWAY_EXAMPLE)

  user_obj = {
    "instructor": user.user_id,
    "curriculum_pathway_id": pathway.uuid,
    "status": "inactive"
  }
  association_group_dict = deepcopy(FULL_LEARNER_ASSOCIATION_GROUP_EXAMPLE)
  association_group_dict["association_type"] = "learner"
  association_group_dict["associations"]["instructors"].append(user_obj)

  # create association group
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  params = {"skip": 0, "limit": 100, "fetch_tree": True, "status": "inactive"}
  url = f"{api_url}/{association_group.uuid}/instructors"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  assert json_response["data"]["records"][0].get("instructor").get(
                              "user_id") == user.user_id
  assert json_response["data"]["records"][0].get("curriculum_pathway_id").get(
                              "uuid") == pathway.uuid
  assert json_response["data"]["records"][0].get("status") == "inactive"


def test_get_all_instructors_of_association_group_negative(clean_firestore):
  association_group_dict = deepcopy(FULL_LEARNER_ASSOCIATION_GROUP_EXAMPLE)
  association_group_dict["association_type"] = "learner"

  # create association group
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  params = {"skip": 0, "limit": 100, "fetch_tree": True}
  url = f"{api_url}/random_uuid/instructors"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response["message"] == \
          "AssociationGroup with uuid random_uuid not found"
  assert json_response["success"] is False
  assert json_response["data"] is None


def test_post_association_group(clean_firestore):
  # Create learner association group:
  create_curriculum_pathway(
    payload={**BASIC_CURRICULUM_PATHWAY_EXAMPLE,
             "is_active": True, "alias": "program",
             "is_deleted": False})
  input_group = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_group)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  post_json_response = post_resp.json()
  del post_json_response["data"]["created_time"]
  del post_json_response["data"]["last_modified_time"]
  uuid = post_json_response.get("data").get("uuid")
  assert post_json_response["data"]["association_type"] == "learner"

  # now see if GET endpoint returns same data
  url = f"{api_url}/{uuid}"
  get_resp = client_with_emulator.get(url)
  get_json_response = get_resp.json()
  del get_json_response["data"]["created_time"]
  del get_json_response["data"]["last_modified_time"]
  assert get_json_response.get("data") == post_json_response.get("data")


def test_post_association_group_negative(clean_firestore):
  # Create learner association group:
  active_cp=create_curriculum_pathway(
    payload={**BASIC_CURRICULUM_PATHWAY_EXAMPLE,
             "is_active": True, "alias": "program",
              "is_deleted": False})
  input_group = {**BASIC_ASSOCIATION_GROUP_EXAMPLE, "name": "Learner Group1"}
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_group)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  post_json_response = post_resp.json()
  del post_json_response["data"]["created_time"]
  del post_json_response["data"]["last_modified_time"]
  uuid = post_json_response.get("data").get("uuid")
  assert post_json_response["data"]["association_type"] == "learner"
  assert post_json_response["data"]["associations"] == {
      "coaches": [],
      "instructors": [],
      "curriculum_pathway_id": active_cp.uuid
  }
  # now see if GET endpoint returns same data
  url = f"{api_url}/{uuid}"
  get_resp = client_with_emulator.get(url)
  get_json_response = get_resp.json()
  del get_json_response["data"]["created_time"]
  del get_json_response["data"]["last_modified_time"]
  assert get_json_response.get("data") == post_json_response.get("data")

  # Create association group with same name:
  input_group = {**BASIC_ASSOCIATION_GROUP_EXAMPLE, "name": "Learner Group1"}
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_group)
  post_resp_json = post_resp.json()

  assert post_resp_json.get("success") is False, "Success not False"
  assert post_resp.status_code == 409
  assert post_resp_json.get("message") == \
         "AssociationGroup with the given name: Learner Group1 already exists"


def test_update_association_group(clean_firestore):
  association_group_dict = {
      **BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "learner"
  }
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()
  association_group_uuid = association_group.id

  url = f"{api_url}/{association_group_uuid}"
  updated_data = deepcopy(association_group_dict)
  del updated_data["association_type"]
  updated_data["name"] = "new group name"
  updated_data["description"] = "new group description"
  resp = client_with_emulator.put(url, json=updated_data)
  update_response = resp.json()

  assert update_response.get("success") is True, "Success not true"
  assert update_response["message"] == \
         "Successfully updated the association group"
  assert update_response["data"]["name"] == "new group name"
  assert update_response["data"]["description"] == "new group description"


def test_update_association_group_negative_1(clean_firestore):
  association_group_dict = {
      **BASIC_ASSOCIATION_GROUP_EXAMPLE, "name": "Association Group",
      "association_type": "learner"
  }
  association_group_1 = AssociationGroup.from_dict(association_group_dict)
  association_group_1.uuid = ""
  association_group_1.save()
  association_group_1.uuid = association_group_1.id
  association_group_1.update()
  association_group_uuid = association_group_1.id

  association_group_dict = {
      **BASIC_ASSOCIATION_GROUP_EXAMPLE, "name": "new group name",
      "association_type": "learner"
  }
  association_group_2 = AssociationGroup.from_dict(association_group_dict)
  association_group_2.uuid = ""
  association_group_2.save()
  association_group_2.uuid = association_group_2.id
  association_group_2.update()

  url = f"{api_url}/{association_group_uuid}"
  updated_data = deepcopy(association_group_dict)
  del updated_data["association_type"]
  updated_data["name"] = "Association Group"
  updated_data["description"] = "new group description"
  resp = client_with_emulator.put(url, json=updated_data)
  update_response = resp.json()

  assert update_response.get("success") is False, "Success not False"
  assert resp.status_code == 409
  assert update_response.get("message") == \
         "AssociationGroup with the given name: Association Group already " \
         "exists"


def test_update_association_group_negative_2(clean_firestore):
  association_group_dict = deepcopy(BASIC_ASSOCIATION_GROUP_EXAMPLE)
  association_group_dict["name"] = "Learner Group 2"
  association_group_dict["association_type"] = "learner"
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()
  uuid = "random_id"

  url = f"{api_url}/{uuid}"
  response = {
      "success": False,
      "message": "AssociationGroup with uuid random_id not found",
      "data": None
  }
  del association_group_dict["association_type"]
  association_group_dict["name"] = "New association group name"
  resp = client_with_emulator.put(url, json=association_group_dict)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_delete_association_group(clean_firestore):
  association_group_dict = {
      **BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "learner"
  }
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  url = f"{api_url}/{association_group.uuid}"
  resp = client_with_emulator.delete(url)
  del_json_response = resp.json()
  expected_data = {
      "success": True,
      "message": "Successfully deleted the association group"
  }
  assert resp.status_code == 200, "Status code not 200"
  assert del_json_response == expected_data, "Expected response not same"


def test_delete_association_group_negative(clean_firestore):
  uuid = "random_uuid"
  url = f"{api_url}/{uuid}"
  response = {
      "success": False,
      "message": "AssociationGroup with uuid random_uuid not found",
      "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_update_association_status_1(clean_firestore):
  user_dict_1 = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  user_1 = User.from_dict(user_dict_1)
  user_1.user_id = ""
  user_1.save()
  user_1.user_id = user_1.id
  user_1.update()
  user_dict_1["user_id"] = user_1.id

  user_dict_2 = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  user_2 = User.from_dict(user_dict_2)
  user_2.user_id = ""
  user_2.save()
  user_2.user_id = user_2.id
  user_2.update()
  user_dict_2["user_id"] = user_2.id

  # Create curriculum pathway
  curriculum_pathway_id = create_curriculum_pathway(
    payload=BASIC_CURRICULUM_PATHWAY_EXAMPLE).uuid

  association_group_dict = {
      **BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "learner"
  }
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()
  association_group_uuid = association_group.id

  association_group.users = [{"user": user_1.user_id, "status": "active"}]
  association_group.associations = {
      "instructors": [{
          "instructor": user_2.user_id,
          "curriculum_pathway_id": "",
          "status": "active"
      }]
  }
  association_group.update()

  url = f"{api_url}/{association_group_uuid}/user-association/status"
  request_body = {
    "user": {"user_id": user_1.user_id, "status": "inactive"},
    "instructor": {"instructor_id": user_2.user_id,
                   "curriculum_pathway_id": curriculum_pathway_id,
                   "status": "inactive"}
  }

  resp = client_with_emulator.put(url, json=request_body)
  update_response = resp.json()

  assert update_response.get("success") is True, "Success not true"
  assert update_response["message"] == \
         "Successfully updated the association group"
  assert update_response["data"]["users"][0]["status"] == "inactive"
  assert update_response["data"]["associations"]["instructors"][0][
      "status"] == "inactive"


def test_update_association_status_2(clean_firestore):
  user_dict_1 = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  user_1 = User.from_dict(user_dict_1)
  user_1.user_id = ""
  user_1.save()
  user_1.user_id = user_1.id
  user_1.update()
  user_dict_1["user_id"] = user_1.id

  user_dict_2 = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  user_2 = User.from_dict(user_dict_2)
  user_2.user_id = ""
  user_2.save()
  user_2.user_id = user_2.id
  user_2.update()
  user_dict_2["user_id"] = user_2.id

  # Create curriculum pathway
  curriculum_pathway_id = create_curriculum_pathway(
    payload=BASIC_CURRICULUM_PATHWAY_EXAMPLE).uuid

  # Create Discipline Association Group
  discipline_group_dict = {
      **BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "discipline"
  }
  discipline_group = AssociationGroup.from_dict(discipline_group_dict)
  discipline_group.uuid = ""
  discipline_group.save()
  discipline_group.uuid = discipline_group.id
  discipline_group.update()

  discipline_group.users = [{"user": user_2.user_id, "status": "active"}]
  discipline_group.associations = {
    "curriculum_pathways": [{
    "curriculum_pathway_id": curriculum_pathway_id, "status": "active"
    }]
  }
  discipline_group.update()

  # Create Learner Association Group
  association_group_dict = {
      **BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "learner"
  }
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()
  association_group_uuid = association_group.id

  association_group.users = [{
    "user": user_1.user_id, "status": "active"
  }]
  association_group.associations = {"instructors": [
    {
      "instructor": user_2.user_id,
      "curriculum_pathway_id": curriculum_pathway_id,
      "status": "inactive"
    }]
  }
  association_group.update()

  url = f"{api_url}/{association_group_uuid}/user-association/status"
  request_body = {
    "instructor": {"instructor_id": user_2.user_id,
                   "curriculum_pathway_id":curriculum_pathway_id,
                   "status": "active"}
  }

  resp = client_with_emulator.put(url, json=request_body)
  update_response = resp.json()

  assert update_response.get("success") is True, "Success not true"
  assert update_response["message"] == \
         "Successfully updated the association group"
  assert update_response["data"]["associations"]["instructors"][0][
      "status"] == "active"


def test_update_association_status_negative_1(clean_firestore):
  user_dict_1 = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  user_1 = User.from_dict(user_dict_1)
  user_1.user_id = ""
  user_1.save()
  user_1.user_id = user_1.id
  user_1.update()
  user_dict_1["user_id"] = user_1.id

  user_dict_2 = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  user_2 = User.from_dict(user_dict_2)
  user_2.user_id = ""
  user_2.save()
  user_2.user_id = user_2.id
  user_2.update()
  user_dict_2["user_id"] = user_2.id

  association_group_dict = {
      **BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "learner"
  }
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()
  association_group_uuid = association_group.id

  association_group.users = [{"user": user_1.user_id, "status": "active"}]
  association_group.associations = {
      "instructors": [{
          "instructor": user_2.user_id,
          "status": "active"
      }]
  }
  association_group.update()

  url = f"{api_url}/{association_group_uuid}/user-association/status"
  request_body = {"user": {"user_id": "random_uuid", "status": "inactive"}}

  resp = client_with_emulator.put(url, json=request_body)
  update_response = resp.json()

  mes = "User for given user_id is not present in the learner association group"
  assert update_response.get("success") is False, "Success not False"
  assert update_response["message"] == mes


def test_update_association_status_negative_2(clean_firestore):
  user_dict_1 = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  user_1 = User.from_dict(user_dict_1)
  user_1.user_id = ""
  user_1.save()
  user_1.user_id = user_1.id
  user_1.update()
  user_dict_1["user_id"] = user_1.id

  user_dict_2 = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  user_2 = User.from_dict(user_dict_2)
  user_2.user_id = ""
  user_2.save()
  user_2.user_id = user_2.id
  user_2.update()
  user_dict_2["user_id"] = user_2.id

  association_group_dict = {
      **BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "learner"
  }
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()
  association_group_uuid = association_group.id

  association_group.users = [{"user": user_1.user_id, "status": "active"}]
  association_group.associations = {
      "instructors": [{
          "instructor": user_2.user_id,
          "status": "active"
      }]
  }
  association_group.update()

  url = f"{api_url}/{association_group_uuid}/user-association/status"
  request_body = {
      "instructor": {
          "user_id": user_2.user_id,
          "status": "random_status"
      }
  }

  resp = client_with_emulator.put(url, json=request_body)
  update_response = resp.json()

  assert update_response.get("success") is False, "Success not False"
  assert update_response["message"] == "Validation Failed"


def test_update_association_status_negative_3(clean_firestore):
  user_dict_1 = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  user_1 = User.from_dict(user_dict_1)
  user_1.user_id = ""
  user_1.save()
  user_1.user_id = user_1.id
  user_1.update()
  user_dict_1["user_id"] = user_1.id

  user_dict_2 = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  user_2 = User.from_dict(user_dict_2)
  user_2.user_id = ""
  user_2.save()
  user_2.user_id = user_2.id
  user_2.update()
  user_dict_2["user_id"] = user_2.id

  # Create curriculum pathway
  curriculum_pathway_id = create_curriculum_pathway(
    payload=BASIC_CURRICULUM_PATHWAY_EXAMPLE).uuid

  # Create Discipline Association Group
  discipline_group_dict = {
      **BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "discipline"
  }
  discipline_group = AssociationGroup.from_dict(discipline_group_dict)
  discipline_group.uuid = ""
  discipline_group.save()
  discipline_group.uuid = discipline_group.id
  discipline_group.update()

  # Set the user (instructor) in discipline group to be inactive
  discipline_group.users = [{"user": user_2.user_id, "status": "inactive"}]
  discipline_group.associations = {
    "curriculum_pathways": [{
    "curriculum_pathway_id": curriculum_pathway_id, "status": "active"
    }]
  }
  discipline_group.update()

  # Create Learner Association Group
  association_group_dict = {
      **BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "learner"
  }
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()
  association_group_uuid = association_group.id

  association_group.users = [{
    "user": user_1.user_id, "status": "active"
  }]
  association_group.associations = {"instructors": [
    {
      "instructor": user_2.user_id,
      "curriculum_pathway_id": curriculum_pathway_id,
      "status": "inactive"
    }]
  }
  association_group.update()

  url = f"{api_url}/{association_group_uuid}/user-association/status"
  request_body = {
    "instructor": {"instructor_id": user_2.user_id,
                   "curriculum_pathway_id":curriculum_pathway_id,
                   "status": "active"}
  }

  resp = client_with_emulator.put(url, json=request_body)
  update_response = resp.json()

  error_message = "Instructor for given instructor_id " + \
    f"{user_2.user_id} is not actively associated with the given " + \
    f"curriculum_pathway_id {curriculum_pathway_id} in " + \
    "discipline association group"

  assert resp.status_code == 422
  assert update_response.get("success") is False, "Success not False"
  assert update_response["message"] == error_message


def create_user_and_group(user_group_name, user_type1, user_type2 ):
  """Function to check POST route"""
  user_dict1 = User.from_dict({
      **BASIC_USER_MODEL_EXAMPLE, "user_type": user_type1
  })
  user_dict1.user_id = ""
  user_dict1.save()
  user_dict1.user_id = user_dict1.id
  user_dict1.update()
  user_id1 = user_dict1.user_id

  user_dict2 = User.from_dict({
      **BASIC_USER_MODEL_EXAMPLE, "user_type": user_type2
  })
  user_dict2.user_id = ""
  user_dict2.save()
  user_dict2.user_id = user_dict2.id
  user_dict2.update()
  user_id2 = user_dict2.user_id

  group_example = {**BASIC_GROUP_MODEL_EXAMPLE,
                  "name": user_group_name, "users": [user_id1, user_id2]}

  group_dict = UserGroup.from_dict(group_example)
  group_dict.uuid = ""
  group_dict.save()
  group_dict.uuid = group_dict.id
  group_dict.update()


  user_dict1.user_groups = [group_dict.uuid]
  user_dict1.update()

  user_dict2.user_groups = [group_dict.uuid]
  user_dict2.update()

  return [user_id1, user_id2]


def test_add_user_to_learner_association_group(clean_firestore):
  # Create learner association group:
  input_group = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_group)
  post_resp_json = post_resp.json()
  uuid = post_resp_json.get("data").get("uuid")
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  add_users = create_user_and_group("learner", "learner", "learner")
  add_users = {"users": add_users, "status": "active"}
  url = api_url + f"/{uuid}/users/add"
  post_resp = client_with_emulator.post(url, json=add_users)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"
  assert len(post_resp_json.get("data").get("users")) == 2
  assert post_resp_json["data"]["users"][0]["user"] in add_users["users"]


def test_remove_user_from_learner_association_group(clean_firestore):
  input_group = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_group)
  post_resp_json = post_resp.json()
  uuid = post_resp_json.get("data").get("uuid")
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  # Add users to the association group
  add_users = create_user_and_group("learner", "learner", "learner")
  add_users = {"users": add_users, "status": "active"}
  url = api_url + f"/{uuid}/users/add"
  post_resp = client_with_emulator.post(url, json=add_users)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"
  assert len(post_resp_json.get("data").get("users")) == 2
  assert post_resp_json["data"]["users"][0]["user"] in add_users["users"]

  # Remove user from the association group
  url = api_url + f"/{uuid}/user/remove"
  remove_user = {"user": add_users["users"][0]}
  post_resp = client_with_emulator.post(url, json=remove_user)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"
  assert len(post_resp_json.get("data").get("users")) == 1
  assert add_users["users"][0] != post_resp_json["data"]["users"][0]["user"]


def test_add_coach_to_learner_association_group(clean_firestore):
  # Create learner association group:
  input_group = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_group)
  post_resp_json = post_resp.json()
  uuid = post_resp_json.get("data").get("uuid")
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  # Add coach to the association group
  add_coaches = create_user_and_group("coach", "coach", "coach")
  add_coaches = {"coaches": [add_coaches[0]], "status": "active"}
  url = api_url + f"/{uuid}/coaches/add"
  post_resp = client_with_emulator.post(url, json=add_coaches)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"
  assert len(post_resp_json.get("data").get("associations").get("coaches")) == 1
  assert post_resp_json.get("data").get("associations").get(
      "coaches")[0]["coach"] in add_coaches["coaches"]


def test_add_two_coach_to_learner_association_group(clean_firestore):
  # Create learner association group:
  input_group = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_group)
  post_resp_json = post_resp.json()
  uuid = post_resp_json.get("data").get("uuid")
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  # Add coach to the association group
  add_coaches = create_user_and_group("coach", "coach", "coach")
  add_coaches = {"coaches": add_coaches, "status": "active"}
  url = api_url + f"/{uuid}/coaches/add"
  post_resp = client_with_emulator.post(url, json=add_coaches)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is False, "Success not false"
  assert post_resp.status_code == 422, "Status 422"
  assert post_resp_json.get("message") == "Only one coach can be associated " \
                                          "with the Learner Association Group"


def test_remove_coach_from_learner_association_group(clean_firestore):
  # Create learner association group:
  input_group = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_group)
  post_resp_json = post_resp.json()
  uuid = post_resp_json.get("data").get("uuid")
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  # Add coach to the association group
  add_coaches = create_user_and_group("coach", "coach", "coach")
  add_coaches = {"coaches": [add_coaches[0]], "status": "active"}
  url = api_url + f"/{uuid}/coaches/add"
  post_resp = client_with_emulator.post(url, json=add_coaches)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"
  assert len(post_resp_json.get("data").get("associations").get("coaches")) == 1
  assert post_resp_json.get("data").get("associations").get(
      "coaches")[0]["coach"] in add_coaches["coaches"]

  # Remove coach from the association group
  url = api_url + f"/{uuid}/coach/remove"
  remove_coach = {"coach": add_coaches["coaches"][0]}
  post_resp = client_with_emulator.post(url, json=remove_coach)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"
  assert len(post_resp_json.get("data").get("associations").get("coaches")) == 0


def create_curriculum_pathway(payload) -> any:
  """
  Function to create the curriculum pathway

  Parameters
  ----------
  payload: dict

  Returns
  -------
  CurriculumPathway: Any
  """
  curriculum_pathway = CurriculumPathway.from_dict(payload)
  curriculum_pathway.uuid = ""
  curriculum_pathway.version = 1
  curriculum_pathway.save()
  curriculum_pathway.uuid = curriculum_pathway.id
  curriculum_pathway.update()
  return curriculum_pathway


def create_disciplines_and_programs():
  """Function to create curriculum pathways"""
  pathway_id = create_curriculum_pathway(payload={
      **BASIC_CURRICULUM_PATHWAY_EXAMPLE, "alias": "discipline"
  }).uuid

  pathway_id_1 = create_curriculum_pathway(payload={
      **BASIC_CURRICULUM_PATHWAY_EXAMPLE, "alias": "discipline"
  }).uuid

  pathway_id_2 = create_curriculum_pathway(payload={
      **BASIC_CURRICULUM_PATHWAY_EXAMPLE, "alias": "discipline"
  }).uuid

  program_id = create_curriculum_pathway(payload={
      **BASIC_CURRICULUM_PATHWAY_EXAMPLE, "alias": "program"
  }).uuid

  return pathway_id, pathway_id_1, pathway_id_2, program_id


def create_user_record(payload: dict) -> any:
  """
  Function to create the user

  Parameters
  ----------
  payload: dict

  Returns
  -------
  User: Any
  """
  user_dict = User.from_dict(payload)
  user_dict.user_id = ""
  user_dict.save()
  user_dict.user_id = user_dict.id
  user_dict.update()

  group_example = {**BASIC_GROUP_MODEL_EXAMPLE,
                  "name": payload["user_type"], "users": [user_dict.id]}

  group_dict = UserGroup.from_dict(group_example)
  group_dict.uuid = ""
  group_dict.save()
  group_dict.uuid = group_dict.id
  group_dict.update()

  user_dict.user_groups = [group_dict.uuid]
  user_dict.update()

  return user_dict


def create_learner_association_group(payload: dict,
                                     program_id: str = "") -> any:
  """
  Function to create learner association group

  Parameters
  ----------
  payload: dict

  Returns
  -------
  AssociationGroup: Any
  """
  association = AssociationGroup.from_dict(payload)
  association.uuid = ""
  association.save()
  if association.association_type == "learner":
    association.associations = {}
    association.associations["curriculum_pathway_id"] = program_id
    association.associations["instructors"] = []
    association.associations["coaches"] = []
  association.uuid = association.id
  association.update()
  return association


def test_add_instructor_positive_1(mocker, clean_firestore):
  """
  Add Instructor with correct request payload
  """

  # Create curriculum pathway
  curriculum_pathway_id, _, _, program_id = create_disciplines_and_programs()

  mocker.patch(
      "routes.learner_association_group.get_all_discipline_for_given_program",
      return_value=[curriculum_pathway_id])
  # Create User as type faculty
  user = {**BASIC_USER_MODEL_EXAMPLE, "user_type": "instructor"}
  instructor_id = create_user_record(payload=user).user_id

  # Create Learner Association Group
  data = {**BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "learner"}
  assoc_id = create_learner_association_group(data, program_id).uuid

  # Create Discipline Association Group
  data = {**BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "discipline"}
  discipline_assoc = create_learner_association_group(data)

  discipline_assoc.users = [{
      "user": instructor_id,
      "user_type": "instructor",
      "status": "active"
  }]
  discipline_assoc.associations = {
    "curriculum_pathways": [
    {"curriculum_pathway_id": curriculum_pathway_id, "status": "active"}
    ]
  }
  discipline_assoc.update()

  # Adding Instructors
  payload = {**ADD_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
             "instructors": [instructor_id],
             "curriculum_pathway_id": curriculum_pathway_id}
  url = f"{api_url}/{assoc_id}/instructors/add"
  post_resp = client_with_emulator.post(url=url, json=payload)
  post_resp_json = post_resp.json()

  mes = "Successfully added the instructors to the learner association group"

  assert post_resp.status_code == 200
  assert post_resp_json.get("success") is True
  assert post_resp_json.get("message") == mes
  assert post_resp_json.get("data").get("associations").get("instructors")[
           0]["instructor"] == [instructor_id][0]
  assert post_resp_json.get("data").get("associations").get("instructors")[
           0]["curriculum_pathway_id"] == curriculum_pathway_id
  assert post_resp_json.get("data").get("associations").get("instructors")[
           0]["status"] == "active"


def test_add_instructor_positive_2(mocker, clean_firestore):
  """
  Add Instructor for various curriculum pathway
  """
  # Create curriculum pathway
  pathway_id, pathway_id_1, pathway_id_2, program_id = \
    create_disciplines_and_programs()

  mocker.patch(
      "routes.learner_association_group.get_all_discipline_for_given_program",
      return_value=[pathway_id,pathway_id_1, pathway_id_2])

  # Create User as type faculty
  user = {**BASIC_USER_MODEL_EXAMPLE, "user_type": "instructor"}
  instructor_id = create_user_record(payload=user).user_id

  # Create Learner Association Group
  data = {**BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "learner"}
  assoc_id = create_learner_association_group(
      payload=data, program_id=program_id).uuid

  # Create Discipline Association Group
  data = {**BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "discipline"}
  discipline_assoc = create_learner_association_group(payload=data)

  discipline_assoc.users = [{
      "user": instructor_id,
      "user_type": "instructor",
      "status": "active"
  }]
  discipline_assoc.associations = {
    "curriculum_pathways": [
    {"curriculum_pathway_id": pathway_id, "status": "active"}
    ]
  }
  discipline_assoc.update()

  # Adding Instructors for various curriculum pathway
  payload = {
      **ADD_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
      "instructors": [instructor_id],
      "curriculum_pathway_id": pathway_id
  }
  url = f"{api_url}/{assoc_id}/instructors/add"
  client_with_emulator.post(url=url, json=payload)

  discipline_assoc.associations["curriculum_pathways"].append(
    {"curriculum_pathway_id": pathway_id_2, "status": "active"})
  discipline_assoc.update()

  payload = {
      **ADD_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
      "instructors": [instructor_id],
      "curriculum_pathway_id": pathway_id_2
  }
  url = f"{api_url}/{assoc_id}/instructors/add"
  post_resp = client_with_emulator.post(url=url, json=payload)
  post_resp_json = post_resp.json()

  mes = "Successfully added the instructors to the learner association group"

  assert post_resp.status_code == 200
  assert post_resp_json.get("success") is True
  assert post_resp_json.get("message") == mes
  assert len(
      post_resp_json.get("data").get("associations").get("instructors")) == 2


def test_add_instructor_positive_3(mocker, clean_firestore):
  """
  Add Instructor for existing removed instructor curriculum pathway
  """
  # Create curriculum pathway
  curriculum_pathway_id, _, pathway_id_2, program_id = \
    create_disciplines_and_programs()

  mocker.patch(
      "routes.learner_association_group.get_all_discipline_for_given_program",
      return_value=[curriculum_pathway_id, pathway_id_2])

  # Create User as type faculty
  user = {**BASIC_USER_MODEL_EXAMPLE, "user_type": "instructor"}
  instructor_id = create_user_record(payload=user).user_id

  # Create Learner Association Group
  data = {**BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "learner"}
  assoc_id = create_learner_association_group(
      payload=data, program_id=program_id).uuid

  # Create Discipline Association Group
  data = {**BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "discipline"}
  discipline_assoc = create_learner_association_group(payload=data)

  discipline_assoc.users = [{
      "user": instructor_id,
      "user_type": "instructor",
      "status": "active"
  }]
  discipline_assoc.associations = {
    "curriculum_pathways": [
    {"curriculum_pathway_id": curriculum_pathway_id, "status": "active"}
    ]
  }
  discipline_assoc.update()

  # Adding Instructors for various curriculum pathway
  payload = {**ADD_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
             "instructors": [instructor_id],
             "curriculum_pathway_id": curriculum_pathway_id}
  url = f"{api_url}/{assoc_id}/instructors/add"
  client_with_emulator.post(url=url, json=payload)

  # Removing Instructor
  payload = {**REMOVE_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
             "instructor": instructor_id,
             "curriculum_pathway_id": curriculum_pathway_id}
  url = f"{api_url}/{assoc_id}/instructor/remove"
  client_with_emulator.post(url=url, json=payload)

  # Again Adding Instructor for same curriculum pathway
  payload = {**ADD_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
             "instructors": [instructor_id],
             "curriculum_pathway_id": curriculum_pathway_id}
  url = f"{api_url}/{assoc_id}/instructors/add"
  post_resp = client_with_emulator.post(url=url, json=payload)
  post_resp_json = post_resp.json()

  mes = "Successfully added the instructors to the learner association group"

  assert post_resp.status_code == 200
  assert post_resp_json.get("success") is True
  assert post_resp_json.get("message") == mes
  assert post_resp_json.get("data").get("associations").get("instructors")[
           0]["instructor"] == instructor_id
  assert post_resp_json.get("data").get("associations").get("instructors")[
           0]["curriculum_pathway_id"] == curriculum_pathway_id
  assert post_resp_json.get("data").get("associations").get("instructors")[
           0]["status"] == "active"


def test_add_multiple_instructor_negative(clean_firestore):
  """
  Adding Multiple Instructors
  """
  payload = {
      **ADD_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
      "instructors": ["12w231212", "1212s312"]
  }
  url = f"{api_url}/1234/instructors/add"
  post_resp = client_with_emulator.post(url=url, json=payload)
  post_resp_json = post_resp.json()

  assert post_resp.status_code == 404
  assert post_resp_json.get("success") is False


def test_add_instructor_negative_2(clean_firestore):
  """
  Adding Incorrect Instructors
  """
  payload = {
      **ADD_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
      "instructors": ["12w231212"]
  }
  url = f"{api_url}/1234/instructors/add"
  post_resp = client_with_emulator.post(url=url, json=payload)
  post_resp_json = post_resp.json()

  assert post_resp.status_code == 404
  assert post_resp_json.get("success") is False


def test_add_instructor_negative_3(clean_firestore):
  """
  Adding incorrect instructors with incorrect user type
  """
  user = {**BASIC_USER_MODEL_EXAMPLE, "user_type": "learner"}
  instructor_id = create_user_record(payload=user).user_id

  # Adding Instructors
  payload = {
      **ADD_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
      "instructors": [instructor_id]
  }
  url = f"{api_url}/12w13q13q/instructors/add"
  post_resp = client_with_emulator.post(url=url, json=payload)
  post_resp_json = post_resp.json()

  assert post_resp.status_code == 404
  assert post_resp_json.get("success") is False


def test_add_instructor_negative_4(clean_firestore):
  """
  Adding instructors with incorrect curriculum pathway ID
  """
  user = {**BASIC_USER_MODEL_EXAMPLE, "user_type": "faculty"}
  instructor_id = create_user_record(payload=user).user_id

  # Adding Instructors
  payload = {
      **ADD_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
      "instructors": [instructor_id],
      "curriculum_pathway_id": "12s2312s21"
  }
  url = f"{api_url}/12w13q13q/instructors/add"
  post_resp = client_with_emulator.post(url=url, json=payload)
  post_resp_json = post_resp.json()

  assert post_resp.status_code == 404
  assert post_resp_json.get("success") is False


def test_add_instructor_negative_5(clean_firestore):
  """
  Adding instructors with incorrect curriculum pathway ID
  """
  # Create User as type faculty
  user = {**BASIC_USER_MODEL_EXAMPLE, "user_type": "faculty"}
  instructor_id = create_user_record(payload=user).user_id

  # Create Learner Association Group
  data = {**BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "discipline"}
  assoc_id = create_learner_association_group(payload=data).uuid

  # Create curriculum pathway
  curriculum_pathway_id = create_curriculum_pathway(
    payload=BASIC_CURRICULUM_PATHWAY_EXAMPLE).uuid

  # Adding Instructors
  payload = {**ADD_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
             "instructors": [instructor_id],
             "curriculum_pathway_id": curriculum_pathway_id}
  url = f"{api_url}/{assoc_id}/instructors/add"
  post_resp = client_with_emulator.post(url=url, json=payload)
  post_resp_json = post_resp.json()

  assert post_resp.status_code == 422
  assert post_resp_json.get("success") is False


def test_add_instructor_negative_6(mocker, clean_firestore):
  """
  Add Instructor with correct request payload
  """

  # Create curriculum pathway
  curriculum_pathway_id, _, pathway_id_2, program_id = \
    create_disciplines_and_programs()

  mocker.patch(
      "routes.learner_association_group.get_all_discipline_for_given_program",
      return_value=[curriculum_pathway_id, pathway_id_2])

  # Create User as type faculty
  user = {**BASIC_USER_MODEL_EXAMPLE, "user_type": "instructor"}
  instructor_id = create_user_record(payload=user).user_id

  # Create Learner Association Group
  data = {**BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "learner"}
  assoc_id = create_learner_association_group(
      payload=data, program_id=program_id).uuid

  # Create Discipline Association Group
  data = {**BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "discipline"}
  discipline_assoc = create_learner_association_group(payload=data)

  discipline_assoc.users = [{
      "user": instructor_id,
      "user_type": "instructor",
      "status": "inactive"
  }]
  discipline_assoc.associations = {
    "curriculum_pathways": [
    {"curriculum_pathway_id": curriculum_pathway_id, "status": "active"}
    ]
  }
  discipline_assoc.update()

  # Adding Instructors
  payload = {**ADD_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
             "instructors": [instructor_id],
             "curriculum_pathway_id": curriculum_pathway_id}
  url = f"{api_url}/{assoc_id}/instructors/add"
  post_resp = client_with_emulator.post(url=url, json=payload)
  post_resp_json = post_resp.json()

  error_message = "Instructors for given instructor_ids " + \
    f"{[instructor_id]} are not actively associated with the given " + \
    f"curriculum_pathway_id {curriculum_pathway_id} in " + \
    "discipline association group"

  assert post_resp.status_code == 422
  assert post_resp_json.get("success") is False
  assert post_resp_json.get("message") == error_message


def test_remove_instructor_positive_1(mocker, clean_firestore):
  """
  Remove Instructor with correct payload
  """
  # Create curriculum pathway
  curriculum_pathway_id, _, pathway_id_2, program_id = \
    create_disciplines_and_programs()

  mocker.patch(
      "routes.learner_association_group.get_all_discipline_for_given_program",
      return_value=[curriculum_pathway_id, pathway_id_2])

  # Create User as type faculty
  user = {**BASIC_USER_MODEL_EXAMPLE, "user_type": "instructor"}
  instructor_id = create_user_record(payload=user).user_id

  # Create Learner Association Group
  data = {**BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "learner"}
  assoc_id = create_learner_association_group(
      payload=data, program_id=program_id).uuid

  # Create Discipline Association Group
  data = {**BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "discipline"}
  discipline_assoc = create_learner_association_group(payload=data)

  discipline_assoc.users = [{
      "user": instructor_id,
      "user_type": "instructor",
      "status": "active"
  }]
  discipline_assoc.associations = {
    "curriculum_pathways": [
    {"curriculum_pathway_id": curriculum_pathway_id, "status": "active"}
    ]
  }
  discipline_assoc.update()

  # Adding Instructors for various curriculum pathway
  payload = {**ADD_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
             "instructors": [instructor_id],
             "curriculum_pathway_id": curriculum_pathway_id}
  url = f"{api_url}/{assoc_id}/instructors/add"
  client_with_emulator.post(url=url, json=payload)

  # Removing Instructor
  payload = {**REMOVE_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
             "instructor": instructor_id,
             "curriculum_pathway_id": curriculum_pathway_id}
  url = f"{api_url}/{assoc_id}/instructor/remove"
  res = client_with_emulator.post(url=url, json=payload)

  mes = "Successfully removed the instructors from the learner association " \
        "group"
  assert res.status_code == 200
  assert res.json()["success"] is True
  assert res.json()["message"] == mes


def test_remove_instructor_positive_2(mocker, clean_firestore):
  """
  Remove Instructor from multiple instructors
  """
  # Create curriculum pathway
  pathway_id, pathway_id_1, pathway_id_2, program_id = \
    create_disciplines_and_programs()

  mocker.patch(
      "routes.learner_association_group.get_all_discipline_for_given_program",
      return_value=[pathway_id, pathway_id_1, pathway_id_2])

  # Create User as type faculty
  user = {**BASIC_USER_MODEL_EXAMPLE, "user_type": "instructor"}
  instructor_id = create_user_record(payload=user).user_id

  # Create Learner Association Group
  data = {**BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "learner"}
  assoc_id = create_learner_association_group(
      payload=data, program_id=program_id).uuid

  # Create Discipline Association Group
  data = {**BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "discipline"}
  discipline_assoc = create_learner_association_group(payload=data)

  discipline_assoc.users = [{
      "user": instructor_id,
      "user_type": "instructor",
      "status": "active"
  }]
  discipline_assoc.associations = {
    "curriculum_pathways": [
    {"curriculum_pathway_id": pathway_id_1, "status": "active"}
    ]
  }
  discipline_assoc.update()

  # Adding Instructors for various curriculum pathway
  payload = {
      **ADD_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
      "instructors": [instructor_id],
      "curriculum_pathway_id": pathway_id_1
  }
  url = f"{api_url}/{assoc_id}/instructors/add"
  client_with_emulator.post(url=url, json=payload)

  discipline_assoc.associations["curriculum_pathways"].append(
    {"curriculum_pathway_id": pathway_id_2, "status": "active"})
  discipline_assoc.update()

  payload = {
      **ADD_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
      "instructors": [instructor_id],
      "curriculum_pathway_id": pathway_id_2
  }
  url = f"{api_url}/{assoc_id}/instructors/add"
  client_with_emulator.post(url=url, json=payload)

  # Removing Instructor
  payload = {
      **REMOVE_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
      "instructor": instructor_id,
      "curriculum_pathway_id": pathway_id_2
  }
  url = f"{api_url}/{assoc_id}/instructor/remove"
  res = client_with_emulator.post(url=url, json=payload)
  mes = "Successfully removed the instructors from the learner association " \
        "group"
  assert res.status_code == 200
  assert res.json()["success"] is True
  assert res.json()["message"] == mes


def test_remove_instructor_negative_1(clean_firestore):
  """
  Remove Instructor with incorrect instructor ID
  """

  # Removing Instructor
  payload = {
      **REMOVE_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
      "instructor_id": "1qw22e3",
      "curriculum_pathway_id": "12s2323qsq"
  }
  url = f"{api_url}/1s2edq/instructor/remove"
  res = client_with_emulator.post(url=url, json=payload)

  assert res.status_code == 422
  assert res.json()["success"] is False


def test_remove_instructor_negative_3(clean_firestore):
  """
  Remove Instructor with incorrect curriculum pathway ID
  """

  # Create User as type learner
  user = {**BASIC_USER_MODEL_EXAMPLE, "user_type": "instructor"}
  instructor_id = create_user_record(payload=user).user_id

  # Removing Instructor
  payload = {
      **REMOVE_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
      "instructor": instructor_id,
      "curriculum_pathway_id": "12s2323qsq"
  }
  url = f"{api_url}/1s2edq/instructor/remove"
  res = client_with_emulator.post(url=url, json=payload)

  assert res.status_code == 404
  assert res.json()["success"] is False


def test_remove_instructor_negative_4(clean_firestore):
  """
  Remove Instructor with incorrect association ID
  """

  # Create User as type learner
  user = {**BASIC_USER_MODEL_EXAMPLE, "user_type": "instructor"}
  instructor_id = create_user_record(payload=user).user_id

  # Create curriculum pathway
  curriculum_pathway_id = create_curriculum_pathway(
    payload=BASIC_CURRICULUM_PATHWAY_EXAMPLE).uuid

  # Removing Instructor
  payload = {**REMOVE_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
             "instructor": instructor_id,
             "curriculum_pathway_id": curriculum_pathway_id}
  url = f"{api_url}/1s2edq/instructor/remove"
  res = client_with_emulator.post(url=url, json=payload)

  assert res.status_code == 404
  assert res.json()["success"] is False


def test_remove_instructor_negative_5(clean_firestore):
  """
  Remove Instructor with incorrect association type
  """

  # Create User as type learner
  user = {**BASIC_USER_MODEL_EXAMPLE, "user_type": "faculty"}
  instructor_id = create_user_record(payload=user).user_id

  # Create curriculum pathway
  curriculum_pathway_id = create_curriculum_pathway(
    payload=BASIC_CURRICULUM_PATHWAY_EXAMPLE).uuid

  # Create Learner Association Group
  data = {**BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "discipline"}
  assoc_id = create_learner_association_group(payload=data).uuid

  # Removing Instructor
  payload = {**REMOVE_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
             "instructor": instructor_id,
             "curriculum_pathway_id": curriculum_pathway_id}
  url = f"{api_url}/{assoc_id}/instructor/remove"
  res = client_with_emulator.post(url=url, json=payload)

  assert res.status_code == 422
  assert res.json()["success"] is False


def test_remove_instructor_negative_6(mocker, clean_firestore):
  """
  Remove instructor from empty instructor
  """
  pathway_id, _, _, program_id = create_disciplines_and_programs()

  mocker.patch(
      "routes.learner_association_group.get_all_discipline_for_given_program",
      return_value=[pathway_id])

  # Create User as type faculty
  user = {**BASIC_USER_MODEL_EXAMPLE, "user_type": "instructor"}
  instructor_id = create_user_record(payload=user).user_id

  # Create Learner Association Group
  data = {**BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "learner"}
  assoc_id = create_learner_association_group(payload=data,
                                              program_id=program_id).uuid

  # Create curriculum pathway
  curriculum_pathway_id = create_curriculum_pathway(
    payload=BASIC_CURRICULUM_PATHWAY_EXAMPLE).uuid

  # Create Discipline Association Group
  data = {**BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "discipline"}
  discipline_assoc = create_learner_association_group(payload=data)

  discipline_assoc.users = [{
      "user": instructor_id,
      "user_type": "instructor",
      "status": "active"
  }]
  discipline_assoc.associations = {
    "curriculum_pathways": [
    {"curriculum_pathway_id": curriculum_pathway_id, "status": "active"}
    ]
  }
  discipline_assoc.update()

  # Adding Instructors for various curriculum pathway
  payload = {**ADD_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
             "instructors": [instructor_id],
             "curriculum_pathway_id": curriculum_pathway_id}
  url = f"{api_url}/{assoc_id}/instructors/add"
  client_with_emulator.post(url=url, json=payload)

  # Removing Instructor
  payload = {**REMOVE_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
             "instructor": instructor_id,
             "curriculum_pathway_id": curriculum_pathway_id}
  url = f"{api_url}/{assoc_id}/instructor/remove"
  client_with_emulator.post(url=url, json=payload)

  res = client_with_emulator.post(url=url, json=payload)

  assert res.status_code == 422
  assert res.json().get("success") is False


def test_remove_instructor_negative_7(mocker, clean_firestore):
  """
  Remove instructor with wrong instructor ID
  """
  curriculum_pathway_id, _, _, program_id = create_disciplines_and_programs()

  mocker.patch(
      "routes.learner_association_group.get_all_discipline_for_given_program",
      return_value=[curriculum_pathway_id])

  # Create User as type faculty
  user = {**BASIC_USER_MODEL_EXAMPLE, "user_type": "instructor"}
  instructor_id = create_user_record(payload=user).user_id
  instructor_2 = create_user_record(payload=user).user_id

  # Create Learner Association Group
  data = {**BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "learner"}
  assoc_id = create_learner_association_group(
      payload=data, program_id=program_id).uuid

  # Adding Instructors for various curriculum pathway
  payload = {**ADD_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
             "instructors": [instructor_id],
             "curriculum_pathway_id": curriculum_pathway_id}
  url = f"{api_url}/{assoc_id}/instructors/add"
  client_with_emulator.post(url=url, json=payload)

  # Removing Instructor
  payload = {**REMOVE_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
             "instructor_id": instructor_2,
             "curriculum_pathway_id": curriculum_pathway_id}
  url = f"{api_url}/{assoc_id}/instructor/remove"
  res = client_with_emulator.post(url=url, json=payload)

  assert res.status_code == 422
  assert res.json().get("success") is False


def test_remove_instructor_negative_8(mocker, clean_firestore):
  """
  Remove instructor wrong curriculum pathway ID
  """
  curriculum_pathway_id, pathway_id_1, pathway_2, program_id = \
    create_disciplines_and_programs()

  mocker.patch(
      "routes.learner_association_group.get_all_discipline_for_given_program",
      return_value=[curriculum_pathway_id, pathway_id_1, pathway_2])

  # Create User as type faculty
  user = {**BASIC_USER_MODEL_EXAMPLE, "user_type": "instructor"}
  instructor_id = create_user_record(payload=user).user_id

  # Create Learner Association Group
  data = {**BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "learner"}
  assoc_id = create_learner_association_group(payload=data,
                                              program_id=program_id).uuid

  # Create curriculum pathway
  curriculum_pathway_id = create_curriculum_pathway(
    payload=BASIC_CURRICULUM_PATHWAY_EXAMPLE).uuid
  pathway_2 = create_curriculum_pathway(
    payload=BASIC_CURRICULUM_PATHWAY_EXAMPLE).uuid

  # Create Discipline Association Group
  data = {**BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "discipline"}
  discipline_assoc = create_learner_association_group(payload=data)

  discipline_assoc.users = [{
      "user": instructor_id,
      "user_type": "instructor",
      "status": "active"
  }]
  discipline_assoc.associations = {
    "curriculum_pathways": [
        {"curriculum_pathway_id": curriculum_pathway_id, "status": "active"}
    ]
  }
  discipline_assoc.update()

  # Adding Instructors for various curriculum pathway
  payload = {**ADD_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
             "instructors": [instructor_id],
             "curriculum_pathway_id": curriculum_pathway_id}
  url = f"{api_url}/{assoc_id}/instructors/add"
  client_with_emulator.post(url=url, json=payload)

  # Removing Instructor
  payload = {
      **REMOVE_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
      "instructor": instructor_id,
      "curriculum_pathway_id": pathway_2
  }
  url = f"{api_url}/{assoc_id}/instructor/remove"

  res = client_with_emulator.post(url=url, json=payload)

  assert res.status_code == 422
  assert res.json().get("success") is False

def test_get_all_the_learner_for_instructor(clean_firestore):
  users = create_user_and_group("instructor", "instructor", "learner")

  association_group_dict = {
      **BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "learner"
  }
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.users = [{"user": users[1], "status": "active"}]
  association_group.associations = {
      "instructors": [{
          "instructor": users[0],
          "curriculum_pathway_id": "",
          "status": "active"
      }]
  }
  association_group.update()

  url = f"{api_url}/instructor/{users[0]}/learners"
  res = client_with_emulator.get(url=url)
  res_data = res.json()
  assert res.status_code == 200
  assert res_data["success"] is True
  assert res_data["message"] == "Successfully fetched the learners "\
        "for the given instructor"
  assert users[1] in res_data["data"]

def test_get_all_the_learner_for_coach(clean_firestore):
  users = create_user_and_group("coach", "coach", "learner")



  association_group_dict = {
      **BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "learner"
  }
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.users = [{"user": users[1], "status": "active"}]
  association_group.associations = {
      "coaches": [{
          "coach": users[0],
          "status": "active"
      }]
  }
  association_group.update()

  url = f"{api_url}/coach/{users[0]}/learners"
  res = client_with_emulator.get(url=url)
  res_data = res.json()
  assert res.status_code == 200
  assert res_data["success"] is True
  assert res_data["message"] == "Successfully fetched the learners "\
        "for the given coach"
  assert users[1] in res_data["data"]

def test_get_all_the_learner_for_coach_and_instructor_negative(clean_firestore):
  user_dict_1 = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  user_1 = User.from_dict(user_dict_1)
  user_1.user_id = ""
  user_1.save()
  user_1.user_id = user_1.id
  user_1.update()
  user_dict_1["user_id"] = user_1.id

  random_instructor_id = str(uuid4())

  association_group_dict = {
      **BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "learner"
  }
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.users = [{"user": user_1.user_id, "status": "active"}]
  association_group.update()

  url = f"{api_url}/instructor/{random_instructor_id}/learners"
  res = client_with_emulator.get(url=url)
  res_data = res.json()
  assert res.status_code == 404
  assert res_data["success"] is False
  assert res_data["message"] == f"User with user_id "\
    f"{random_instructor_id} not found"
  assert res_data["data"] is None
