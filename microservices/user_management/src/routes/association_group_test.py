"""
  Unit tests for association endpoints
"""
import os
from copy import deepcopy
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.routes.association_group import router
from testing.test_config import API_URL
from schemas.schema_examples import ( BASIC_ASSOCIATION_GROUP_EXAMPLE,
                                     ASSOCIATION_GROUP_EXAMPLE,
                                    FULL_USER_MODEL_EXAMPLE,
                                    BASIC_CURRICULUM_PATHWAY_EXAMPLE,
                                    FULL_DISCIPLINE_ASSOCIATION_GROUP_EXAMPLE,
                                    BASIC_USER_MODEL_EXAMPLE
                                    )
from common.models import AssociationGroup, CurriculumPathway, User
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/user-management/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/association-groups"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

def test_search_association_group(clean_firestore):
  association_group_dict = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  association_group_dict["association_type"] = "discipline"
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  params = {"search_query": association_group.name}

  url = f"{api_url}/search"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 200, "Status not 200"
  assert json_response["data"][0][
          "name"] == association_group.name, "Response not received"

def test_search_association_group_negative1(clean_firestore):
  association_group_dict = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  association_group_dict["association_type"] = "discipline"
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  params = {"search_query": association_group.name,  "skip":0, "limit":0}

  url = f"{api_url}/search"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 422, "Status not 422"
  assert json_response.get("success") is False, "Response is not False"

def test_search_association_group_negative2(clean_firestore):
  association_group_dict = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  association_group_dict["association_type"] = "discipline"
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  params = {"search_query": ""}

  url = f"{api_url}/search"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 422, "Status not 422"
  assert json_response.get("success") is False, "Response is not False"
  assert json_response.get("message") == "search_query cannot be empty"

def test_association_group(clean_firestore):
  association_group_dict = {**ASSOCIATION_GROUP_EXAMPLE}
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  params = {"skip": 0, "limit": 3 }

  url = f"{api_url}"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 200, "Status should be 200"
  retrieved_ids = [i.get("uuid") for i in json_response.get("data")]
  assert association_group.uuid in retrieved_ids, "Response received"

def test_association_group_with_negative_filter(clean_firestore):
  association_group_dict = {**ASSOCIATION_GROUP_EXAMPLE}
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  params = {"skip": 0, "limit": -3 }

  url = f"{api_url}"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 422, "Status should be 422"
  assert json_response.get(
      "message"
  ) == "Validation Failed"

def test_association_group_with_association_type_filter(clean_firestore):
  association_group_dict = {**ASSOCIATION_GROUP_EXAMPLE}
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  params = {"skip": 0, "limit": 1, "association_type": "discipline" }

  url = f"{api_url}"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 200, "Status should be 200"
  retrieved_association_type =[i.get("association_type")
    for i in json_response.get("data")]
  assert association_group.association_type in retrieved_association_type
  retrieved_ids = [i.get("uuid") for i in json_response.get("data")]
  assert association_group.uuid in retrieved_ids, "Response received"

def test_update_disciplines_with_active_pathway(clean_firestore):

  # Preparing Instructor Data
  user_dict = {**FULL_USER_MODEL_EXAMPLE}
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.user_type = "instructor"
  user.save()
  user.user_id = user.id
  user.update()
  users = [{"user": user.user_id, "status": "active"}]

  # Prepare Data for one program and discipline
  program_dict = deepcopy(BASIC_CURRICULUM_PATHWAY_EXAMPLE)
  program = CurriculumPathway.from_dict(program_dict)
  program.uuid = ""
  program.alias = "program"
  program.is_active = True
  program.save()
  program.uuid = program.id
  program.update()

  discipline_dict = deepcopy(BASIC_CURRICULUM_PATHWAY_EXAMPLE)
  discipline = CurriculumPathway.from_dict(discipline_dict)
  discipline.uuid = ""
  discipline.alias = "discipline"
  discipline.save()
  discipline.uuid = discipline.id
  discipline.parent_nodes = {"curriculum_pathways": [program.id]}
  discipline.update()

  program.child_nodes = {"curriculum_pathways": [discipline.id]}
  program.update()

  # Preparing Association Group Data
  # Discipline Association Group
  discipline_group_dict = deepcopy(FULL_DISCIPLINE_ASSOCIATION_GROUP_EXAMPLE)
  discipline_group = AssociationGroup.from_dict(discipline_group_dict)
  discipline_group.uuid = ""
  discipline_group.users = users
  discipline_group.associations["curriculum_pathways"] = [
    {"curriculum_pathway_id": discipline.id, "status": "active"}]
  discipline_group.save()
  discipline_group.uuid = discipline_group.id
  discipline_group.update()

  # Learner Association Group
  learner_group_dict = {**BASIC_ASSOCIATION_GROUP_EXAMPLE,
                            "association_type": "learner"}
  learner_group = AssociationGroup.from_dict(learner_group_dict)
  learner_group.uuid = ""
  learner_group.save()
  learner_group.associations = {
    "instructors": [{"instructor": user.id,
                     "curriculum_pathway_id": discipline.id,
                     "status": "active"}],
    "curriculum_pathway_id": program.id
  }
  learner_group.uuid = learner_group.id
  learner_group.update()

  # Preparing Data for program2
  program2_dict = deepcopy(BASIC_CURRICULUM_PATHWAY_EXAMPLE)
  program2 = CurriculumPathway.from_dict(program2_dict)
  program2.uuid = ""
  program2.alias = "program"
  program2.is_active = True
  program2.save()
  program2.uuid = program2.id
  program2.update()

  discipline2_dict = deepcopy(BASIC_CURRICULUM_PATHWAY_EXAMPLE)
  discipline2 = CurriculumPathway.from_dict(discipline2_dict)
  discipline2.uuid = ""
  discipline2.alias = "discipline"
  discipline2.save()
  discipline2.uuid = discipline2.id
  discipline2.parent_nodes = {"curriculum_pathways": [program2.id]}
  discipline2.update()

  program2.child_nodes = {"curriculum_pathways": [discipline.id]}
  program2.update()

  # Positive Scenario
  input_request = {
    "program_id": program2.id,
    "disciplines": [{"uuid": discipline2.id,
                     "name": discipline2.name,
                     "alias": discipline2.alias}]
  }
  program.is_active = False
  program.update()

  url = f"{api_url}/active-curriculum-pathway/update-all"
  resp = client_with_emulator.put(url, json=input_request)
  json_response = resp.json()

  assert resp.status_code == 200, f"Status Code = {resp.status_code}, not 200"
  assert json_response["data"] == [learner_group.id, discipline_group.id]

  # Negative Scenario: When given program_id is not active
  program2.is_active = False
  program2.update()

  url = f"{api_url}/active-curriculum-pathway/update-all"
  resp = client_with_emulator.put(url, json=input_request)
  json_response = resp.json()

  assert resp.status_code == 422, f"Status Code = {resp.status_code}, not 200"
  msg = "Input program_id is not active"
  assert json_response["message"] == msg

  # Negative Scenario: When given program_id does not have alias as program
  program2.alias = "unit"
  program2.is_active = True
  program2.update()

  url = f"{api_url}/active-curriculum-pathway/update-all"
  resp = client_with_emulator.put(url, json=input_request)
  json_response = resp.json()

  assert resp.status_code == 422, f"Status Code = {resp.status_code}, not 200"
  msg = f"Input pathway has alias as {program2.alias} instead of program"
  assert json_response["message"] == msg

  # Negative Scenario: When the discipline alias is not discipline
  input_request = {
    "program_id": program2.id,
    "disciplines": [{"uuid": discipline2.id,
                     "name": discipline2.name,
                     "alias": "unit"}]
  }
  url = f"{api_url}/active-curriculum-pathway/update-all"
  resp = client_with_emulator.put(url, json=input_request)
  json_response = resp.json()
  msg = "Validation Failed"
  assert resp.status_code == 422, f"Status Code = {resp.status_code}, not 200"
  assert json_response["message"] == msg


def test_get_users_by_usertype(clean_firestore):
  #create user
  user_dict = {**BASIC_USER_MODEL_EXAMPLE}
  user_dict["user_type"] = "coach"
  user_dict["user_type_ref"] = ""
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  user_dict["user_id"] = user.id

  #create association group
  association_group_dict = {**BASIC_ASSOCIATION_GROUP_EXAMPLE,
                            "association_type": "learner",
                            "associations": {"coaches": [],
                                      "instructors": [],
                                      "curriculum_pathway_id": ""}}
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  params = {"user_type": "coach"}

  url = f"{api_url}/{association_group.uuid}/addable-users"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"

  assert json_response.get("data")[0]["user_id"
                ] == user.id, "expected data not retrieved"

def test_get_users_by_usertype_for_learner(clean_firestore):
  "when the user of type learner present in an assocation group"
  #create user
  user_dict = {**BASIC_USER_MODEL_EXAMPLE}
  user_dict["user_type"] = "learner"
  user_dict["user_type_ref"] = ""
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  user_dict["user_id"] = user.id

  #association_group with above user_id
  association_group_dict = {**BASIC_ASSOCIATION_GROUP_EXAMPLE,
                            "association_type": "learner",
                            "users": [{
                                "user": user.id,
                                "status": "active",
                                "user_group_type": "learner"
                                }]
                            }

  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  #association_group that users will be added to
  association_group_dict1 = {**BASIC_ASSOCIATION_GROUP_EXAMPLE,
                            "association_type": "learner"}
  association_group1 = AssociationGroup.from_dict(association_group_dict1)
  association_group1.uuid = ""
  association_group1.save()
  association_group1.uuid = association_group1.id
  association_group1.update()

  params = {"user_type": "learner"}

  url = f"{api_url}/{association_group1.uuid}/addable-users"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"
  assert json_response.get("data"
                      ) == [], "expected data not retrieved"
