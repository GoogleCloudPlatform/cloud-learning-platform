"""
  Unit tests for Discipline association group endpoints
"""
import os
from copy import deepcopy
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import,invalid-name
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.discipline_association_group import router
from testing.test_config import API_URL
from schemas.schema_examples import (BASIC_ASSOCIATION_GROUP_EXAMPLE,
                                      BASIC_USER_MODEL_EXAMPLE,
                                      TEST_CURRICULUM_PATHWAY,
                                      FULL_DISCIPLINE_ASSOCIATION_GROUP_EXAMPLE,
                                      FULL_USER_MODEL_EXAMPLE,
                                      BASIC_CURRICULUM_PATHWAY_EXAMPLE)
from common.models import AssociationGroup, UserGroup, User, CurriculumPathway
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/user-management/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/association-groups/discipline-association"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_get_association_group(clean_firestore):
  """Get an association group with correct uuid"""
  association_group_dict = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  association_group_dict["association_type"] = "discipline"
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
  association_group_dict = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  association_group_dict["association_type"] = "discipline"
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
  retrieved_ids = [i.get("uuid") for i in json_response.get("data")]
  assert association_group.uuid in retrieved_ids, "expected data not retrieved"

def test_get_all_association_groups_negative(clean_firestore):
  association_group_dict = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  association_group_dict["association_type"] = "discipline"
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

def test_get_all_association_groups_negative_param(clean_firestore):
  association_group_dict = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  association_group_dict["association_type"] = "discipline"
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


def test_post_association_group(clean_firestore):
  # Create discipline association group:
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
  assert post_json_response["data"]["association_type"] == "discipline"
  assert post_json_response["data"]["associations"] == {
      "curriculum_pathways": []
  }
  # now see if GET endpoint returns same data
  url = f"{api_url}/{uuid}"
  get_resp = client_with_emulator.get(url)
  get_json_response = get_resp.json()
  del get_json_response["data"]["created_time"]
  del get_json_response["data"]["last_modified_time"]
  assert get_json_response.get("data") == post_json_response.get("data")


def test_post_association_group_negative(clean_firestore):
  # Create discipline association group:
  input_group = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  input_group["name"] = "Association Group1"
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_group)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  post_json_response = post_resp.json()
  del post_json_response["data"]["created_time"]
  del post_json_response["data"]["last_modified_time"]
  uuid = post_json_response.get("data").get("uuid")
  assert post_json_response["data"]["association_type"] == "discipline"
  assert post_json_response["data"]["associations"] == {
      "curriculum_pathways": []
  }
  # now see if GET endpoint returns same data
  url = f"{api_url}/{uuid}"
  get_resp = client_with_emulator.get(url)
  get_json_response = get_resp.json()
  del get_json_response["data"]["created_time"]
  del get_json_response["data"]["last_modified_time"]
  assert get_json_response.get("data") == post_json_response.get("data")

  input_group = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  input_group["name"] = "Association Group1"
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_group)
  post_resp_json = post_resp.json()

  assert post_resp_json.get("success") is False, "Success not False"
  assert post_resp.status_code == 409
  assert post_resp_json.get("message") == \
    "AssociationGroup with the given name: Association Group1 already exists"


def test_update_association_group(clean_firestore):
  association_group_dict = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  association_group_dict["association_type"] = "discipline"
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
  association_group_dict = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  association_group_dict["name"] = "Association Group"
  association_group_dict["association_type"] = "discipline"
  association_group_1 = AssociationGroup.from_dict(association_group_dict)
  association_group_1.uuid = ""
  association_group_1.save()
  association_group_1.uuid = association_group_1.id
  association_group_1.update()
  association_group_uuid = association_group_1.id

  association_group_dict = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  association_group_dict["name"] = "new discipline group name"
  association_group_dict["association_type"] = "discipline"
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
    "AssociationGroup with the given name: Association Group already exists"


def test_update_association_group_negative_2(clean_firestore):
  association_group_dict = deepcopy(BASIC_ASSOCIATION_GROUP_EXAMPLE)
  association_group_dict["name"] = "Learner Group 2"
  association_group_dict["association_type"] = "discipline"
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
  association_group_dict["name"] = "New association group name"
  del association_group_dict["association_type"]
  resp = client_with_emulator.put(url, json=association_group_dict)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_delete_association_group(clean_firestore):
  instructor_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_type_ref": ""}
  instructor = User.from_dict(instructor_dict)
  instructor.user_id = ""
  instructor.save()
  instructor.user_id = instructor.id
  instructor.update()
  instructor_dict["user_id"] = instructor.id

  cp_dict = {**TEST_CURRICULUM_PATHWAY}
  cp = CurriculumPathway.from_dict(cp_dict)
  cp.uuid = ""
  cp.alias = "discipline"
  cp.save()
  cp.uuid = cp.id
  cp.update()

  association_group_dict = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  association_group_dict["association_type"] = "discipline"
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.users = [{"user": instructor.user_id, "status": "active"}]
  association_group.associations = {"curriculum_pathways": [{
    "curriculum_pathway_id": cp.id,
    "status": "active"
  }]}
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()


  learner_association_group_dict = {
      **BASIC_ASSOCIATION_GROUP_EXAMPLE, "association_type": "learner"
  }
  learner_association_group = AssociationGroup.from_dict(
    learner_association_group_dict)
  learner_association_group.uuid = ""
  learner_association_group.save()
  learner_association_group.uuid = learner_association_group.id
  learner_association_group.update()
  learner_association_group_uuid = learner_association_group.id

  learner_association_group.users = []
  learner_association_group.associations = {"instructors": [
    {
      "instructor": instructor.user_id,
      "curriculum_pathway_id": cp.id,
      "status": "inactive"
    }]
  }
  learner_association_group.update()

  url = f"{api_url}/{association_group.uuid}"
  resp = client_with_emulator.delete(url)
  del_json_response = resp.json()
  expected_data = {
      "success": True,
      "message": "Successfully deleted the association group"
  }
  assert resp.status_code == 200, "Status code not 200"
  assert del_json_response == expected_data, "Expected response not same"

  get_learner_association_group =  AssociationGroup.find_by_uuid(
                                  learner_association_group_uuid)
  assert get_learner_association_group.associations["instructors"] == []


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


def test_add_discipline_to_discipline_association_group(clean_firestore):
  association_group_dict = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  association_group_dict["association_type"] = "discipline"
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  cp_dict = {**TEST_CURRICULUM_PATHWAY}
  cp = CurriculumPathway.from_dict(cp_dict)
  cp.uuid = ""
  cp.alias = "discipline"
  cp.save()
  cp.uuid = cp.id
  cp.update()

  url = f"{api_url}/{association_group.id}/discipline/add"
  request_body = {
    "curriculum_pathway_id": cp.id,
    "status": "active"
  }
  resp = client_with_emulator.post(url, json=request_body)
  json_response = resp.json()["data"]
  assert resp.status_code == 200, f"Status {resp.status_code}"
  assert json_response["associations"][
    "curriculum_pathways"] == [request_body], "Associations not same"

  # test for adding same discipline ID again
  resp = client_with_emulator.post(url, json=request_body)
  assert resp.status_code == 422, f"Status Code = {resp.status_code}"

  # test for ResourceNotFound
  url = f"{api_url}/wrong_id/discipline/add"
  resp = client_with_emulator.post(url, json=request_body)
  json_response = resp.json()["data"]
  assert resp.status_code == 404, f"Status Code = {resp.status_code}"

  # test for ValidationError
  url = f"{api_url}/{association_group.uuid}/discipline/add"
  request_body = {"wrong": "wrong"}
  resp = client_with_emulator.post(url, json=request_body)
  assert resp.status_code == 422, f"Status Code = {resp.status_code}"


def test_remove_discipline_from_discipline_association_group(clean_firestore):

  # assertion to successfully remove a discipline
  association_group_dict = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  association_group_dict["association_type"] = "discipline"

  cp_dict = {**TEST_CURRICULUM_PATHWAY}
  cp = CurriculumPathway.from_dict(cp_dict)
  cp.uuid = ""
  cp.alias = "discipline"
  cp.save()
  cp.uuid = cp.id
  cp.update()

  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.associations = {"curriculum_pathways": [{
    "curriculum_pathway_id": cp.id,
    "status": "active"
  }]}
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  url = f"{api_url}/{association_group.uuid}/discipline/remove"
  request_body = {
    "curriculum_pathway_id": cp.id
  }
  resp = client_with_emulator.post(url, json=request_body)
  json_response = resp.json()["data"]
  assert resp.status_code == 200, f"Status {resp.status_code}"
  assert json_response["associations"]["curriculum_pathways"] == [], \
  "Associations not same"

  # test for ResourceNotFound
  url = f"{api_url}/wrong_id/discipline/remove"
  resp = client_with_emulator.post(url, json=request_body)
  json_response = resp.json()["data"]
  assert resp.status_code == 404, f"Status Code = {resp.status_code}"

  # test for ValidationError
  url = f"{api_url}/{association_group.uuid}/discipline/remove"
  request_body = {"wrong": "wrong"}
  resp = client_with_emulator.post(url, json=request_body)
  assert resp.status_code == 422, f"Status Code = {resp.status_code}"

  cp.alias = "unit"
  cp.update()
  url = f"{api_url}/{association_group.uuid}/discipline/remove"
  request_body = {"curriculum_pathway_id": cp.id}
  resp = client_with_emulator.post(url, json=request_body)
  assert resp.status_code == 422, f"Status Code = {resp.status_code}"

def create_user_and_group(user_group_name, user_type):
  """Test function to check post route"""
  user_dict = User.from_dict({
      **BASIC_USER_MODEL_EXAMPLE, "user_type": user_type
  })
  user_dict.user_id = ""
  user_dict.save()
  user_dict.user_id = user_dict.id
  user_dict.update()
  user_id1 = user_dict.user_id

  user_dict = User.from_dict({
      **BASIC_USER_MODEL_EXAMPLE, "user_type": user_type
  })
  user_dict.user_id = ""
  user_dict.save()
  user_dict.user_id = user_dict.id
  user_dict.update()
  user_id2 = user_dict.user_id

  GROUP_EXAMPLE = {"name": user_group_name, "users": [user_id1, user_id2]}

  group_dict = UserGroup.from_dict({**GROUP_EXAMPLE})
  group_dict.uuid = ""
  group_dict.save()
  group_dict.user_id = group_dict.id
  group_dict.update()

  return [user_id1, user_id2]


def test_add_user_to_discipline_association_group(clean_firestore):
  # Create discipline association group:
  input_group = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_group)
  post_resp_json = post_resp.json()
  uuid = post_resp_json.get("data").get("uuid")
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  add_users = create_user_and_group("instructor group", "instructor")
  add_users = {"users": add_users, "status": "active"}
  url = api_url + f"/{uuid}/users/add"
  post_resp = client_with_emulator.post(url, json=add_users)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"
  assert len(post_resp_json.get("data").get("users")) == 2
  assert post_resp_json["data"]["users"][0]["user"] in add_users["users"]


def test_remove_user_from_discipline_association_group(clean_firestore):
  input_group = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_group)
  post_resp_json = post_resp.json()
  uuid = post_resp_json.get("data").get("uuid")
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  # Add users to the association group
  add_users = create_user_and_group("instructor group", "instructor")
  add_users = {"users": add_users, "status": "active"}
  url = api_url + f"/{uuid}/users/add"
  post_resp = client_with_emulator.post(url, json=add_users)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"
  assert len(post_resp_json.get("data").get("users")) == 2
  assert post_resp_json["data"]["users"][0]["user"] in add_users["users"]

  # Remove user from the assication group
  url = api_url + f"/{uuid}/user/remove"
  remove_user = {"user": add_users["users"][0]}
  post_resp = client_with_emulator.post(url, json=remove_user)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"
  assert len(post_resp_json.get("data").get("users")) == 1
  assert add_users["users"][0] != post_resp_json["data"]["users"][0]["user"]


def test_update_association_status(clean_firestore):
  user_dict_1 = {**BASIC_USER_MODEL_EXAMPLE}
  user_dict_1["user_type_ref"] = ""
  user_1 = User.from_dict(user_dict_1)
  user_1.user_id = ""
  user_1.save()
  user_1.user_id = user_1.id
  user_1.update()
  user_dict_1["user_id"] = user_1.id

  user_dict_2 = {**BASIC_USER_MODEL_EXAMPLE}
  user_dict_2["user_type_ref"] = ""
  user_2 = User.from_dict(user_dict_2)
  user_2.user_id = ""
  user_2.save()
  user_2.user_id = user_2.id
  user_2.update()
  user_dict_2["user_id"] = user_2.id

  association_group_dict = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  association_group_dict["association_type"] = "discipline"
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()
  association_group_uuid = association_group.id

  association_group.users = [{
    "user": user_1.user_id, "status": "active", "user_type": "instructor"
      }]
  association_group.associations = {}
  association_group.update()

  url = f"{api_url}/{association_group_uuid}/user-association/status"
  request_body = {
    "user": {"user_id": user_1.user_id, "status": "inactive"}
  }

  resp = client_with_emulator.put(url, json=request_body)
  update_response = resp.json()

  assert update_response.get("success") is True, "Success not true"
  assert update_response["message"] == \
                "Successfully updated the association group"
  assert update_response["data"]["users"][0]["status"] == "inactive"


def test_update_association_status_negative_1(clean_firestore):
  user_dict_1 = {**BASIC_USER_MODEL_EXAMPLE}
  user_dict_1["user_type_ref"] = ""
  user_1 = User.from_dict(user_dict_1)
  user_1.user_id = ""
  user_1.save()
  user_1.user_id = user_1.id
  user_1.update()
  user_dict_1["user_id"] = user_1.id

  user_dict_2 = {**BASIC_USER_MODEL_EXAMPLE}
  user_dict_2["user_type_ref"] = ""
  user_2 = User.from_dict(user_dict_2)
  user_2.user_id = ""
  user_2.save()
  user_2.user_id = user_2.id
  user_2.update()
  user_dict_2["user_id"] = user_2.id

  association_group_dict = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  association_group_dict["association_type"] = "discipline"
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()
  association_group_uuid = association_group.id

  association_group.users = [{
      "user": user_1.user_id, "status": "active"
      }]
  association_group.update()

  url = f"{api_url}/{association_group_uuid}/user-association/status"
  request_body = {
    "user": {"user_id": "random_uuid", "status": "inactive"}
  }

  resp = client_with_emulator.put(url, json=request_body)
  update_response = resp.json()

  assert update_response.get("success") is False, "Success not False"
  assert update_response["message"] == \
    "User for given user_id is not present in the discipline association group"


def test_update_association_status_negative_2(clean_firestore):
  user_dict_1 = {**BASIC_USER_MODEL_EXAMPLE}
  user_dict_1["user_type_ref"] = ""
  user_1 = User.from_dict(user_dict_1)
  user_1.user_id = ""
  user_1.save()
  user_1.user_id = user_1.id
  user_1.update()
  user_dict_1["user_id"] = user_1.id

  user_dict_2 = {**BASIC_USER_MODEL_EXAMPLE}
  user_dict_2["user_type_ref"] = ""
  user_2 = User.from_dict(user_dict_2)
  user_2.user_id = ""
  user_2.save()
  user_2.user_id = user_2.id
  user_2.update()
  user_dict_2["user_id"] = user_2.id

  association_group_dict = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  association_group_dict["association_type"] = "discipline"
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()
  association_group_uuid = association_group.id

  association_group.users = [{
      "user": user_1.user_id, "status": "active"}]
  association_group.update()

  url = f"{api_url}/{association_group_uuid}/user-association/status"
  request_body = {
    "user": {"user_id": user_1.user_id, "status": "random_status"}
  }

  resp = client_with_emulator.put(url, json=request_body)
  update_response = resp.json()

  assert update_response.get("success") is False, "Success not False"
  assert update_response["message"] == "Validation Failed"


def test_get_instructors_associated_to_discipline(clean_firestore):
  """Get list of instructors associated with a discipline"""
  user_dict = {**FULL_USER_MODEL_EXAMPLE}
  users = []
  for i in range(4):
    user = User.from_dict(user_dict)
    user.user_id = ""
    user.save()
    user.user_id = user.id
    user.update()

    users.append({"user": user.user_id, "status": "active"})
    users[i]["user_type"] = "assessor" if i%2 == 0 else "instructor"

  curriculum_pathway_dict = deepcopy(BASIC_CURRICULUM_PATHWAY_EXAMPLE)
  curriculum_pathway = CurriculumPathway.from_dict(curriculum_pathway_dict)
  curriculum_pathway.uuid = "disc_id_2"
  curriculum_pathway.save()

  association_group_dict = deepcopy(FULL_DISCIPLINE_ASSOCIATION_GROUP_EXAMPLE)
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.users = users
  association_group.associations["curriculum_pathways"] = [
    {"curriculum_pathway_id": "disc_id_1", "status": "active"},
    {"curriculum_pathway_id": "disc_id_2", "status": "active"},
    {"curriculum_pathway_id": "disc_id_3", "status": "active"}]
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  url = f"{api_url}/discipline/disc_id_2/users"
  params = {"user_type": "instructor"}
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()

  assert resp.status_code == 200, "Status 200"
  assert len(json_response["data"]) == 2, "expected data not retrieved"


def test_add_user_to_discipline_association_group_negative(clean_firestore):
  # Create discipline association group:
  input_group = {**BASIC_ASSOCIATION_GROUP_EXAMPLE}
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_group)
  post_resp_json = post_resp.json()
  uuid = post_resp_json.get("data").get("uuid")
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  add_users = create_user_and_group("instructor group", "instructor")
  add_users = {"users": add_users, "status": "active"}
  url = api_url + f"/{uuid}/users/add"
  post_resp = client_with_emulator.post(url, json=add_users)
  post_resp_json = post_resp.json()
  assert post_resp.status_code == 200, "Status 200"

  url = api_url + f"/{uuid}/users/add"
  post_response = client_with_emulator.post(url, json=add_users)
  post_response_json = post_response.json()
  assert post_response_json.get("success") is False
  assert post_response.status_code == 422, "Status not 422"

def test_get_instructors_associated_to_discipline_negative(clean_firestore):
  """Get curriculum pathway with incorrect uuid"""
  uuid = "random_uuid"
  data = {
      "success": False,
      "message": f"Curriculum Pathway with uuid {uuid} not found",
      "data": None
  }

  url = f"{api_url}/discipline/{uuid}/users"
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == data, "Response received"
