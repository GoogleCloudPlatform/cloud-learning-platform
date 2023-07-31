"""
  Unit tests for Learner endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import

import os
import json

from uuid import uuid4
from copy import deepcopy
from fastapi import FastAPI
from urllib.parse import urlparse
from fastapi.testclient import TestClient

from routes.learner import router
from routes.achievement import router as achievement_router
from routes.learner_profile import router as lp_router
from testing.test_config import (API_URL, TESTING_FOLDER_PATH)
from testing.test_objects import (TEST_USER, TEST_LEARNER,
                                  TEST_DISCIPLINE, TEST_STAFF,
                                  DEL_KEYS, TEST_ASSOCIATION_GROUP)
from schemas.schema_examples import (BASIC_LEARNER_EXAMPLE,
                                     BASIC_ACHIEVEMENT_EXAMPLE,
                                     BASIC_LEARNER_PROFILE_EXAMPLE,
                                     BASIC_CURRICULUM_PATHWAY_EXAMPLE)
from common.models import (Learner, Achievement, LearnerProfile, User, Staff,
                           AssociationGroup, CurriculumPathway)
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/learner-profile-service/api/v1")
app.include_router(achievement_router, prefix="/learner-profile-service/api/v1")
app.include_router(lp_router, prefix="/learner-profile-service/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/learner"

LEARNER_TESTDATA_FILENAME = os.path.join(TESTING_FOLDER_PATH, "learners.json")

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_get_learner(clean_firestore):
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()
  learner_dict["uuid"] = learner.id
  learner_dict["is_archived"] = False

  url = f"{api_url}/{learner.uuid}"
  resp = client_with_emulator.get(url)

  json_response = resp.json()
  del json_response["data"]["created_time"]
  del json_response["data"]["last_modified_time"]

  assert resp.status_code == 200, "Status should be 200"
  assert json_response.get("data") == learner_dict, "Response received"


def test_get_learner_negative_1(clean_firestore):
  uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{uuid}"
  data = {
    "success": False,
    "message": f"Learner with uuid {uuid} not found",
    "data": None
  }

  resp = client_with_emulator.get(url)
  json_response = json.loads(resp.text)
  assert resp.status_code == 404, "Status should be 404"
  assert json_response == data, "Response received"


def test_get_learner_negative_2(clean_firestore):
  """Get deleted learner"""
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.is_deleted = True
  learner.save()
  learner.uuid = learner.id
  learner.update()
  learner_dict["uuid"] = learner.id
  learner_dict["is_archived"] = False

  url = f"{api_url}/{learner.uuid}"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  expected_output = {
    "success": False,
    "message": f"Learner with uuid {learner.uuid} not found",
    "data": None
  }

  assert resp.status_code == 404, "Status should be 404"
  assert json_response == expected_output, "Response received"


def test_post_learner(clean_firestore):
  input_learner = BASIC_LEARNER_EXAMPLE
  url = api_url
  post_resp = client_with_emulator.post(url, json=input_learner)
  post_resp_json = post_resp.json()
  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  post_json_response = json.loads(post_resp.text)
  del post_json_response["data"]["created_time"]
  del post_json_response["data"]["last_modified_time"]

  uuid = post_json_response.get("data").get("uuid")

  # now see if GET endpoint returns same data
  url = f"{api_url}/{uuid}"
  get_resp = client_with_emulator.get(url)
  get_json_response = json.loads(get_resp.text)
  del get_json_response["data"]["created_time"]
  del get_json_response["data"]["last_modified_time"]
  assert get_json_response.get("data") == post_json_response.get("data")

  # now check and confirm it is properly in the database
  loaded_learner = Learner.find_by_uuid(uuid)
  loaded_learner_dict = loaded_learner.to_dict()

  # popping id and key for equivalency test
  loaded_learner_dict.pop("id")
  loaded_learner_dict.pop("key")
  loaded_learner_dict.pop("created_by")
  loaded_learner_dict.pop("created_time")
  loaded_learner_dict.pop("last_modified_by")
  loaded_learner_dict.pop("last_modified_time")
  loaded_learner_dict.pop("is_deleted")

  # assert that rest of the fields are equivalent
  assert loaded_learner_dict == post_json_response.get("data")


def test_update_learner(clean_firestore):
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()
  learner_uuid = learner.id

  url = f"{api_url}/{learner_uuid}"
  updated_data = {"phone_number": {"mobile": {"phone_number_type": "Work"}}}
  updated_data["phone_number"]["mobile"]["phone_number_type"] = "Work"
  resp = client_with_emulator.put(url, json=updated_data)
  json_response_update_req = resp.json()

  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get(
    "message"
  ) == "Successfully updated the learner", "Expected response not same"
  assert json_response_update_req.get("data").get("phone_number").get(
    "mobile").get("phone_number_type") == "Work", "Expected response not same"


def test_update_learner_negative(clean_firestore):
  learner_dict = {"phone_number": {"mobile": {"phone_number_type": "Work"}}}
  learner_uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{learner_uuid}"
  response = {
    "success": False,
    "message": "Learner with uuid U2DDBkl3Ayg0PWudzhI not found",
    "data": None
  }
  resp = client_with_emulator.put(url, json=learner_dict)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_delete_learner(clean_firestore):
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()
  learner_dict["uuid"] = learner.id

  learner_profile_dict = {**BASIC_LEARNER_PROFILE_EXAMPLE}
  learner_profile_dict["learner_id"] = learner.id
  learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  learner_profile.uuid = ""
  learner_profile.save()
  learner_profile.uuid = learner_profile.id
  learner_profile.update()
  learner_profile_dict["uuid"] = learner_profile.id

  uuid = learner.uuid
  learner_dict["uuid"] = uuid

  url = f"{api_url}/{uuid}"
  resp = client_with_emulator.delete(url)
  del_json_response = resp.json()

  expected_data = {
    "success": True,
    "message": "Successfully deleted the learner"
  }
  deleted_learner = Learner.find_by_uuid(learner.uuid, is_deleted=True)
  deleted_learner_profile = LearnerProfile.find_by_uuid(
    learner_profile.uuid, is_deleted=True)
  assert resp.status_code == 200, "Status code not 200"
  assert deleted_learner.is_deleted is True, "Learner was not deleted"
  assert deleted_learner_profile.is_deleted is True, \
    "Learner profile was not deleted"
  assert del_json_response == expected_data, "Expected response not same"


def test_delete_learner_negative(clean_firestore):
  learner_uuid = "U2DDBkl3Ayg0PWudzhI"
  url = f"{api_url}/{learner_uuid}"
  response = {
    "success": False,
    "message": "Learner with uuid U2DDBkl3Ayg0PWudzhI not found",
    "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"

  learner_dict = BASIC_LEARNER_EXAMPLE
  learner = Learner.from_dict(learner_dict)
  learner.save()


def test_import_learners(clean_firestore):
  url = f"{api_url}/import/json"
  with open(LEARNER_TESTDATA_FILENAME, encoding="UTF-8") as learners_json_file:
    resp = client_with_emulator.post(
      url, files={"json_file": learners_json_file})

  json_response = resp.json()
  assert resp.status_code == 200, "Status not 200"
  assert isinstance(json_response.get("data"), list), "Response is not a list"
  assert len(json_response.get("data")) > 0, "Empty list returned"


def test_get_learners(clean_firestore):
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner_dict["first_name"] = "UpdatedFirstName"

  # learner
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  # deleted learner
  deleted_learner = Learner.from_dict(learner_dict)
  deleted_learner.uuid = ""
  deleted_learner.is_deleted = True
  deleted_learner.save()
  deleted_learner.uuid = deleted_learner.id
  deleted_learner.update()

  # archived learner
  archived_learner = Learner.from_dict(learner_dict)
  archived_learner.uuid = ""
  archived_learner.is_archived = True
  archived_learner.save()
  archived_learner.uuid = archived_learner.id
  archived_learner.update()
  params = {"skip": 0, "limit": "30", "fetch_archive": False}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  retrieved_ids = [i.get("uuid") for i in json_response.get("data")["records"]]
  assert learner.id in retrieved_ids, "expected data not retrieved"
  assert deleted_learner.id not in retrieved_ids, \
    "unexpected data is retrieved"
  assert archived_learner.uuid not in retrieved_ids, "is_archived not working"


def test_sort_learners(clean_firestore):
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner_dict["first_name"] = "UpdatedFirstName"

  # learner
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  # deleted learner
  deleted_learner = Learner.from_dict(learner_dict)
  deleted_learner.uuid = ""
  deleted_learner.is_deleted = True
  deleted_learner.save()
  deleted_learner.uuid = deleted_learner.id
  deleted_learner.update()

  # archived learner
  archived_learner = Learner.from_dict(learner_dict)
  archived_learner.uuid = ""
  archived_learner.is_archived = True
  archived_learner.save()
  archived_learner.uuid = archived_learner.id
  archived_learner.update()
  params = {"skip": 0, "limit": "30", "fetch_archive": False,
            "sort_by": "first_name", "sort_order": "ascending"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  retrieved_ids = [i.get("uuid") for i in json_response.get(
                              "data").get("records")]
  assert learner.id in retrieved_ids, "expected data not retrieved"
  assert deleted_learner.id not in retrieved_ids, \
    "unexpected data is retrieved"
  assert archived_learner.uuid not in retrieved_ids, "is_archived not working"


def test_sort_learners_negative(clean_firestore):
  params = {"skip": 0, "limit": "30", "fetch_archive": False,
            "sort_by": "first_name", "sort_order": "asc"}

  url = f"{api_url}s"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422
  assert json_response["success"] is False


def test_search_learner(clean_firestore):
  learner_dict = deepcopy(BASIC_LEARNER_EXAMPLE)
  learner_dict["email_address"] = "search_learner@email.com"
  # learner
  learner = Learner.from_dict(learner_dict)
  learner.first_name = "Jon"
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()
  learner_dict["uuid"] = learner.id

  # deleted learner
  deleted_learner = Learner.from_dict(learner_dict)
  deleted_learner.uuid = ""
  deleted_learner.is_deleted = True
  deleted_learner.save()
  deleted_learner.uuid = deleted_learner.id
  deleted_learner.update()

  url = f"{api_url}/search"

  # Search by first_name:
  params = {"first_name": "Jon"}
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  retrieved_ids = [i.get("uuid") for i in json_response.get("data")]
  assert learner.id in retrieved_ids, "expected data not retrieved"
  assert deleted_learner.id not in retrieved_ids, \
    "unexpected data is retrieved"

  # Search by email_address:
  params = {"email_address": "search_learner@email.com"}
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  retrieved_ids = [i.get("uuid") for i in json_response.get("data")]
  assert learner.id in retrieved_ids, "expected data not retrieved"
  assert deleted_learner.id not in retrieved_ids, \
    "unexpected data is retrieved"


def test_search_learner_negative_1(clean_firestore):
  url = f"{api_url}/search"
  params = {"email_address": "search_learner"}
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 422
  assert json_response["success"] is False
  assert json_response["data"] is None


def test_archive_learner(clean_firestore):
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.is_archived = False  # learner not archived initially
  learner.save()
  learner.uuid = learner.id
  learner.update()
  learner_uuid = learner.id

  learner_profile_dict = {**BASIC_LEARNER_PROFILE_EXAMPLE}
  learner_profile_dict["learner_id"] = learner_uuid
  learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  learner_profile.uuid = ""
  learner_profile.is_archived = False  # learner profile not archived initially
  learner_profile.save()
  learner_profile.uuid = learner_profile.id
  learner_profile.update()

  url = f"{api_url}/{learner_uuid}"
  updated_data = {}
  updated_data["is_archived"] = True  # archive learner
  resp = client_with_emulator.put(url, json=updated_data)
  json_response_update_req = resp.json()

  assert json_response_update_req.get("success") is True, "Success not true"
  assert json_response_update_req.get(
    "message"
  ) == "Successfully updated the learner", "Expected response not same"
  assert json_response_update_req.get("data").get(
    "is_archived") is True, "Expected response not same"

  url = f"{api_url}/{learner_uuid}/learner-profile"
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  assert json_response.get("data").get("is_archived") is True, \
    "learner-profile is not archived"


# Fetch Learning Heirarchy with learner id
positive_json_res = {
  "success": "true",
  "message": "Successfully fetched the curriculum pathway",
  "data": {
    **BASIC_CURRICULUM_PATHWAY_EXAMPLE, "uuid": "asd98798as7dhjgkjsdfh",
    "version": 1,
    "parent_version_uuid": "",
    "root_version_uuid": "",
    "is_archived": False,
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
  }
}

negative_json_res_1 = {
  "success": False,
  "message": "Learner with wrong_learner_id abc not found",
  "data": None
}

negative_json_res_2 = {
  "success": False,
  "message": "Curriculum Pathway with uuid wrong_cp_id not found",
  "data": None
}


def mocked_requests_get(*args, **kwargs):
  class MockResponse:

    def __init__(self, json_data, status_code):
      self.json_data = json_data
      self.status_code = status_code

    def json(self):
      return self.json_data

  parsed_url = urlparse(kwargs["url"])

  cp_uuid = parsed_url.path.split("/")[-1]
  learner_id = kwargs["query_params"]["learner_id"]

  if cp_uuid == "real_cp_uuid" and learner_id == "real_learner_id":
    return MockResponse(json_data=positive_json_res, status_code=200)

  if cp_uuid == "real_cp_uuid" and learner_id == "wrong_learner_id":
    return MockResponse(json_data=negative_json_res_1, status_code=500)

  if cp_uuid == "wrong_cp_uuid" and learner_id == "some_learner_id":
    return MockResponse(json_data=negative_json_res_2, status_code=500)

  return MockResponse(json_data={"detail": "Not Found"}, status_code=404)


def test_get_instructor(clean_firestore):
  # ADD INSTRUCTOR DETAILS
  instructor = User.from_dict(TEST_USER)
  instructor.user_type = "instructor"
  instructor.email = str(uuid4()) + "@gmail.com"
  instructor.user_id = ""
  instructor.save()
  instructor.user_id = instructor.id

  staff = Staff.from_dict(TEST_STAFF)
  staff.uuid = ""
  staff.save()
  staff.uuid = staff.id
  staff.update()

  instructor.user_type_ref = staff.id
  instructor.update()

  # ADD Learner Details
  learner = Learner.from_dict(TEST_LEARNER)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  learner_user = User.from_dict(TEST_USER)
  learner_user.user_type = "learner"
  learner_user.user_id = ""
  learner_user.user_type_ref = learner.id
  learner_user.save()
  learner_user.user_id = learner_user.id
  learner_user.update()

  # ADD DISCIPLINE DETAILS
  discipline = CurriculumPathway.from_dict(TEST_DISCIPLINE)
  discipline.uuid = ""
  discipline.save()
  discipline.uuid = discipline.id
  discipline.update()

  # ADD LEARNER ASSOCIATION GROUP DETAILS
  lag_body = {
    "name": "Test Learner Group",
    "description": "Test Learner Group",
    "users": [
      {
        "user": learner_user.user_id,
        "status": "active"
      }
    ],
    "association_type": "learner",
    "associations": {
      "coaches": [],
      "instructors": [{
        "instructor": instructor.id,
        "status": "active",
        "curriculum_pathway_id": discipline.id
      }]
    }
  }
  lag = AssociationGroup.from_dict(lag_body)
  lag.uuid = ""
  lag.save()
  lag.uuid = lag.id
  lag.update()

  # Check if API was successfully hit
  url = f"{api_url}/{learner.id}/curriculum-pathway/{discipline.id}/instructor"
  resp = client_with_emulator.get(url)
  assert resp.status_code == 200, f"Status Code = {resp.status_code}"
  resp_json = resp.json()["data"]

  # Check for data assertion
  assert resp_json["instructor_staff_id"] == staff.uuid

  # Negative Scenario when Learner ID not found
  url = f"{api_url}/learner/curriculum-pathway/{discipline.id}/instructor"
  resp = client_with_emulator.get(url)
  resp_data = resp.json()
  assert resp.status_code == 404, f"Status Code = {resp.status_code}"
  assert resp_data["message"] == "Learner with uuid learner not found", \
    f"Received message = {resp_data['message']}"

  # Negative Scenario when CP ID not found
  url = f"{api_url}/{learner.id}/curriculum-pathway/discipline/instructor"
  resp = client_with_emulator.get(url)
  resp_data = resp.json()
  assert resp.status_code == 404, f"Status Code = {resp.status_code}"
  assert resp_data["message"] == \
         "Curriculum Pathway with uuid discipline not found", \
    f"Received message = {resp_data['message']}"

  # Test for Validations
  # 1. Validating if the Learner exists in any of the groups

  # ADD New Learner Details
  new_learner = Learner.from_dict(TEST_LEARNER)
  new_learner.uuid = ""
  new_learner.save()
  new_learner.uuid = new_learner.id
  new_learner.update()

  new_learner_user = User.from_dict(TEST_USER)
  new_learner_user.user_type = "learner"
  new_learner_user.user_id = ""
  new_learner_user.user_type_ref = new_learner.id
  new_learner_user.save()
  new_learner_user.user_id = new_learner_user.id
  new_learner_user.update()

  url = f"{api_url}/{new_learner.id}/curriculum-pathway/" + \
        f"{discipline.id}/instructor"
  resp = client_with_emulator.get(url)
  resp_data = resp.json()
  assert resp.status_code == 422, f"Status Code = {resp.status_code}"
  assert resp_data["message"] == \
         f"Learner with User ID {new_learner_user.id} not " + \
         "found in any Association Groups", \
    f"Received message = {resp_data['message']}"

  # 2. Validating if the curriculum pathway has the alias as `discipline`
  discipline.alias = "program"
  discipline.update()

  url = f"{api_url}/{learner.id}/curriculum-pathway/{discipline.id}/instructor"
  resp = client_with_emulator.get(url)
  resp_data = resp.json()
  assert resp.status_code == 422, f"Status Code = {resp.status_code}"
  assert resp_data["message"] == \
         f"Pathway with {discipline.id} has alias as " + \
         f"{discipline.alias} instead of discipline", \
    f"Received message = {resp_data['message']}"
  discipline.alias = "discipline"
  discipline.update()

  # 3. Validation for No Active Instructors

  lag.associations = {
    "coaches": [],
    "instructors": [{
      "instructor": instructor.id,
      "status": "inactive",
      "curriculum_pathway_id": discipline.id
    }]
  }
  lag.update()
  url = f"{api_url}/{learner.id}/curriculum-pathway/{discipline.id}/instructor"
  resp = client_with_emulator.get(url)
  resp_data = resp.json()
  assert resp.status_code == 422, f"Status Code = {resp.status_code}"
  assert resp_data["message"] == \
         "No Active Instructors Available for the given CurriculumPathway " + \
         f"= {discipline.id} in AssociationGroup = {lag.id}", \
    f"Received message = {resp_data['message']}"


def test_get_instructors(clean_firestore):
  # ADD INSTRUCTOR DETAILS
  instructor = User.from_dict(TEST_USER)
  instructor.user_type = "instructor"
  instructor.email = str(uuid4()) + "@gmail.com"
  instructor.user_id = ""
  instructor.save()
  instructor.user_id = instructor.id

  staff = Staff.from_dict(TEST_STAFF)
  staff.uuid = ""
  staff.save()
  staff.uuid = staff.id
  staff.update()

  instructor.user_type_ref = staff.id
  instructor.update()

  # ADD Learner Details
  learner = Learner.from_dict(TEST_LEARNER)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  learner_user = User.from_dict(TEST_USER)
  learner_user.user_type = "learner"
  learner_user.user_id = ""
  learner_user.user_type_ref = learner.id
  learner_user.save()
  learner_user.user_id = learner_user.id
  learner_user.update()

  # ADD Learner_2 Details
  learner_2 = Learner.from_dict(TEST_LEARNER)
  learner_2.uuid = ""
  learner_2.save()
  learner_2.uuid = learner_2.id
  learner_2.update()

  learner_user_2 = User.from_dict(TEST_USER)
  learner_user_2.user_type = "learner"
  learner_user_2.user_id = ""
  learner_user_2.user_type_ref = learner_2.id
  learner_user_2.save()
  learner_user_2.user_id = learner_user_2.id
  learner_user_2.update()

  # ADD DISCIPLINE DETAILS
  discipline = CurriculumPathway.from_dict(TEST_DISCIPLINE)
  discipline.alias = "discipline"
  discipline.uuid = ""
  discipline.save()
  discipline.uuid = discipline.id
  discipline.update()

  # ADD PROGRAM DETAILS
  program = CurriculumPathway.from_dict(TEST_DISCIPLINE)
  program.alias = "program"
  program.uuid = ""
  program.save()
  program.uuid = program.id
  program.child_nodes["curriculum_pathways"] = [discipline.uuid]
  program.update()

  discipline.parent_nodes["curriculum_pathways"] = [program.uuid]
  discipline.update()

  # ADD LEARNER ASSOCIATION GROUP DETAILS
  lag_body = {
    "name": "Test Learner Group",
    "description": "Test Learner Group",
    "users": [
      {
        "user": learner_user.user_id,
        "status": "active"
      },
      {
        "user": learner_user_2.user_id,
        "status": "inactive"
      }
    ],
    "association_type": "learner",
    "associations": {
      "coaches": [],
      "instructors": [{
        "instructor": instructor.id,
        "status": "active",
        "curriculum_pathway_id": discipline.id
      }],
      "curriculum_pathway_id": program.uuid
    }
  }
  lag = AssociationGroup.from_dict(lag_body)
  lag.uuid = ""
  lag.save()
  lag.uuid = lag.id
  lag.update()

  # Check if API was successfully hit
  url = f"{api_url}/{learner.id}/curriculum-pathway/{program.id}/instructors"
  resp = client_with_emulator.get(url)
  assert resp.status_code == 200, f"Status Code = {resp.status_code}"
  resp_json = resp.json()["data"][0]

  # Check for data assertion
  assert resp_json["staff_id"] == staff.uuid
  assert resp_json["user_id"] == instructor.user_id
  assert resp_json["discipline_id"] == discipline.uuid

  # Check if API was successfully hit
  # Negative scenario when learner not \
  # actively associated with program in any LAG
  url = f"{api_url}/{learner_2.id}/curriculum-pathway/{program.id}/instructors"
  resp = client_with_emulator.get(url)
  assert resp.status_code == 422, f"Status Code = {resp.status_code}"

  # Negative Scenario when Learner ID not found
  url = f"{api_url}/learner/curriculum-pathway/{program.id}/instructors"
  resp = client_with_emulator.get(url)
  resp_data = resp.json()
  assert resp.status_code == 404, f"Status Code = {resp.status_code}"
  assert resp_data["message"] == "Learner with uuid learner not found", \
    f"Received message = {resp_data['message']}"

  # Negative Scenario when CP ID not found
  url = f"{api_url}/{learner.id}/curriculum-pathway/program/instructors"
  resp = client_with_emulator.get(url)
  resp_data = resp.json()
  assert resp.status_code == 404, f"Status Code = {resp.status_code}"
  assert resp_data["message"] == \
         "Curriculum Pathway with uuid program not found", \
    f"Received message = {resp_data['message']}"


def test_get_coach_details(clean_firestore):
  # Create Learner Type User & Learner
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  learner_user_dict = {**TEST_USER}
  learner_user_dict["user_type"] = "learner"
  learner_user_dict["user_type_ref"] = learner.uuid
  learner_user = User.from_dict(learner_user_dict)
  learner_user.user_id = ""
  learner_user.save()
  learner_user.user_type_ref = learner.uuid
  learner_user.user_id = learner_user.id
  learner_user.update()

  # Create Coach Type User & Staff
  staff_dict = TEST_STAFF
  staff = Staff.from_dict(staff_dict)
  staff.uuid = ""
  staff.save()
  staff.uuid = staff.id
  staff.update()

  staff_user_dict = {**TEST_USER}
  staff_user_dict["user_type"] = "coach"
  staff_user_dict["user_type_ref"] = staff.uuid
  staff_user = User.from_dict(staff_user_dict)
  staff_user.user_id = ""
  staff_user.save()
  staff_user.user_id = staff_user.id
  staff_user.update()

  # Create Association Group
  association_group_dict = {**TEST_ASSOCIATION_GROUP}
  association_group_dict["association_type"] = "learner"
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  # Update the user & coach in learner association group
  association_group.users = [{"user": learner_user.user_id, "status": "active"}]
  association_group.associations = {
    "coaches": [{"coach": staff_user.user_id, "status": "active"}],
    "instructors": [],
    "curriculum_pathway_id": ""
  }
  association_group.update()

  url = f"{api_url}/{learner.uuid}/coach"
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  assert resp.status_code == 200, "Status is not 200"
  assert json_response.get("success") is True
  assert json_response.get("message") == "Successfully fetched the coach"
  assert json_response.get("data").get("coach_staff_id") == staff.uuid


def test_get_coach_details_negative_1(clean_firestore):
  # Create Learner Type User & Learner
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  learner_user_dict = {**TEST_USER}
  learner_user_dict["user_type"] = "learner"
  learner_user_dict["user_type_ref"] = learner.uuid
  learner_user = User.from_dict(learner_user_dict)
  learner_user.user_id = ""
  learner_user.save()
  learner_user.user_type_ref = learner.uuid
  learner_user.user_id = learner_user.id
  learner_user.update()

  # Create Coach Type User & Staff
  staff_dict = TEST_STAFF
  staff = Staff.from_dict(staff_dict)
  staff.uuid = ""
  staff.save()
  staff.uuid = staff.id
  staff.update()

  staff_user_dict = {**TEST_USER}
  staff_user_dict["user_type"] = "coach"
  staff_user_dict["user_type_ref"] = staff.uuid
  staff_user = User.from_dict(staff_user_dict)
  staff_user.user_id = ""
  staff_user.save()
  staff_user.user_id = staff_user.id
  staff_user.update()

  # Create Association Group
  association_group_dict = {**TEST_ASSOCIATION_GROUP}
  association_group_dict["association_type"] = "learner"
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  # Update the user & coach in learner association group
  association_group.users = [{"user": learner_user.user_id, "status": "active"}]
  association_group.associations = {
    "coaches": [{"coach": staff_user.user_id, "status": "active"}],
    "instructors": [],
    "curriculum_pathway_id": ""
  }
  association_group.update()

  invalid_learner_id = "random_id"
  url = f"{api_url}/{invalid_learner_id}/coach"
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status is not 200"
  assert json_response.get("success") is False
  assert json_response.get("message") == \
         "Learner with uuid random_id not found"


def test_get_coach_details_negative_2(clean_firestore):
  # Create Learner Type User & Learner
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  learner_user_dict = {**TEST_USER}
  learner_user_dict["user_type"] = "learner"
  learner_user_dict["user_type_ref"] = learner.uuid
  learner_user = User.from_dict(learner_user_dict)
  learner_user.user_id = ""
  learner_user.save()
  learner_user.user_type_ref = learner.uuid
  learner_user.user_id = learner_user.id
  learner_user.update()

  # Create Coach Type User & Staff
  staff_dict = TEST_STAFF
  staff = Staff.from_dict(staff_dict)
  staff.uuid = ""
  staff.save()
  staff.uuid = staff.id
  staff.update()

  staff_user_dict = {**TEST_USER}
  staff_user_dict["user_type"] = "coach"
  staff_user_dict["user_type_ref"] = staff.uuid
  staff_user = User.from_dict(staff_user_dict)
  staff_user.user_id = ""
  staff_user.save()
  staff_user.user_id = staff_user.id
  staff_user.update()

  # Create Association Group
  association_group_dict = {**TEST_ASSOCIATION_GROUP}
  association_group_dict["association_type"] = "learner"
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  # Update the user & coach in learner association group
  association_group.users = [{"user": learner_user.user_id, "status": "active"}]
  association_group.associations = {
    "coaches": [{"coach": staff_user.user_id, "status": "active"}],
    "instructors": [],
    "curriculum_pathway_id": ""
  }
  association_group.update()

  # Create Another Learner Type User & Learner
  learner_dict_2 = BASIC_LEARNER_EXAMPLE
  learner_dict_2["email"] = "another.learner@email.com"
  learner_2 = Learner.from_dict(learner_dict_2)
  learner_2.uuid = ""
  learner_2.save()
  learner_2.uuid = learner_2.id
  learner_2.update()

  learner_user_dict_2 = {**TEST_USER}
  learner_user_dict_2["email"] = "another.learner@email.com"
  learner_user_dict_2["user_type"] = "learner"
  learner_user_dict_2["user_type_ref"] = learner_2.uuid
  learner_user_2 = User.from_dict(learner_user_dict_2)
  learner_user_2.user_id = ""
  learner_user_2.save()
  learner_user_2.user_type_ref = learner_2.uuid
  learner_user_2.user_id = learner_user_2.id
  learner_user_2.update()

  url = f"{api_url}/{learner_2.uuid}/coach"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  mes = f"User for given learner_id {learner_2.uuid} is not associated in " \
        f"any Learner Association Group"
  assert resp.status_code == 422, "Status is not 422"
  assert json_response.get("success") is False
  assert json_response.get("message") == mes


def test_get_coach_details_negative_3(clean_firestore):
  # Create Learner Type User & Learner
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  learner_user_dict = {**TEST_USER}
  learner_user_dict["user_type"] = "learner"
  learner_user_dict["user_type_ref"] = learner.uuid
  learner_user = User.from_dict(learner_user_dict)
  learner_user.user_id = ""
  learner_user.save()
  learner_user.user_type_ref = learner.uuid
  learner_user.user_id = learner_user.id
  learner_user.update()

  # Create Coach Type User & Staff
  staff_dict = TEST_STAFF
  staff = Staff.from_dict(staff_dict)
  staff.uuid = ""
  staff.save()
  staff.uuid = staff.id
  staff.update()

  staff_user_dict = {**TEST_USER}
  staff_user_dict["user_type"] = "coach"
  staff_user_dict["user_type_ref"] = staff.uuid
  staff_user = User.from_dict(staff_user_dict)
  staff_user.user_id = ""
  staff_user.save()
  staff_user.user_id = staff_user.id
  staff_user.update()

  # Create Association Group
  association_group_dict = {**TEST_ASSOCIATION_GROUP}
  association_group_dict["association_type"] = "learner"
  association_group = AssociationGroup.from_dict(association_group_dict)
  association_group.uuid = ""
  association_group.save()
  association_group.uuid = association_group.id
  association_group.update()

  # Update the user & coach in learner association group
  association_group.users = [{"user": learner_user.user_id, "status": "active"}]
  association_group.associations = {
    "coaches": [],
    "instructors": [],
    "curriculum_pathway_id": ""
  }
  association_group.update()

  url = f"{api_url}/{learner.uuid}/coach"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  mes = f"No active coach exists in Learner Association Group for user " \
        f"corresponding to given learner_id {learner.uuid}"
  assert resp.status_code == 422, "Status is not 422"
  assert json_response.get("success") is False
  assert json_response.get("message") == mes


def test_get_curriculum_pathway_id_for_the_learner(clean_firestore):
  # ADD Learner Details
  learner = Learner.from_dict(TEST_LEARNER)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  learner_user = User.from_dict(TEST_USER)
  learner_user.user_type = "learner"
  learner_user.user_id = ""
  learner_user.user_type_ref = learner.id
  learner_user.save()
  learner_user.user_id = learner_user.id
  learner_user.update()

  # ADD PROGRAM DETAILS
  program = CurriculumPathway.from_dict({**TEST_DISCIPLINE, "alias": "program"})
  program.uuid = ""
  program.save()
  program.uuid = program.id
  program.update()

  # ADD LEARNER ASSOCIATION GROUP DETAILS
  lag_body = {
    "name": "Test Learner Group",
    "description": "Test Learner Group",
    "users": [
      {
        "user": learner_user.user_id,
        "status": "active"
      }
    ],
    "association_type": "learner",
    "associations": {
      "coaches": [],
      "instructors": [],
      "curriculum_pathway_id": program.uuid
    }
  }
  lag = AssociationGroup.from_dict(lag_body)
  lag.uuid = ""
  lag.save()
  lag.uuid = lag.id
  lag.update()

  # Check if API was successfully hit
  url = f"{api_url}/{learner.id}/curriculum-pathway"
  resp = client_with_emulator.get(url)
  assert resp.status_code == 200, f"Status Code = {resp.status_code}"
  resp_json = resp.json()["data"]
  assert resp_json["curriculum_pathway_id"] == program.uuid


def test_get_curriculum_pathway_id_for_the_invalid_learner(clean_firestore):
  # Negative Scenario when Learner ID not found
  url = f"{api_url}/learner/curriculum-pathway"
  resp = client_with_emulator.get(url)
  resp_data = resp.json()
  assert resp.status_code == 404, f"Status Code = {resp.status_code}"
  assert resp_data["message"] == "Learner with uuid learner not found", \
    f"Received message = {resp_data['message']}"


def test_get_curriculum_pathway_id_for_the_learner_negative(clean_firestore):
  # Negative Scenario when CP ID not found
  # ADD Learner Details
  learner = Learner.from_dict(TEST_LEARNER)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  learner_user = User.from_dict(TEST_USER)
  learner_user.user_type = "learner"
  learner_user.user_id = ""
  learner_user.user_type_ref = learner.id
  learner_user.save()
  learner_user.user_id = learner_user.id
  learner_user.update()

  # ADD LEARNER ASSOCIATION GROUP DETAILS
  lag_body = {
    "name": "Test Learner Group",
    "description": "Test Learner Group",
    "users": [
      {
        "user": learner_user.user_id,
        "status": "active"
      }
    ],
    "association_type": "learner",
    "associations": {
      "coaches": [],
      "instructors": [],
      "curriculum_pathway_id": ""
    }
  }
  lag = AssociationGroup.from_dict(lag_body)
  lag.uuid = ""
  lag.save()
  lag.uuid = lag.id
  lag.update()

  url = f"{api_url}/{learner.id}/curriculum-pathway"
  resp = client_with_emulator.get(url)
  resp_data = resp.json()
  mes = f"No curriculum pathway id found for the given Learner with " \
        f"uuid {learner.id}"
  assert resp.status_code == 404, f"Status Code = {resp.status_code}"
  assert resp_data["message"] == mes


def test_get_curriculum_pathway_id_for_the_learner_negative2(clean_firestore):
  # When learner not added in the learner association group
  # ADD Learner Details
  learner = Learner.from_dict(TEST_LEARNER)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  learner_user = User.from_dict(TEST_USER)
  learner_user.user_type = "learner"
  learner_user.user_id = ""
  learner_user.user_type_ref = learner.id
  learner_user.save()
  learner_user.user_id = learner_user.id
  learner_user.update()

  # ADD LEARNER ASSOCIATION GROUP DETAILS
  lag_body = {
    "name": "Test Learner Group",
    "description": "Test Learner Group",
    "users": [],
    "association_type": "learner",
    "associations": {
      "coaches": [],
      "instructors": [],
      "curriculum_pathway_id": ""
    }
  }
  lag = AssociationGroup.from_dict(lag_body)
  lag.uuid = ""
  lag.save()
  lag.uuid = lag.id
  lag.update()

  # Check if API was successfully hit
  url = f"{api_url}/{learner.id}/curriculum-pathway"
  resp = client_with_emulator.get(url)
  resp_json = resp.json()
  mes = f"Given Learner with uuid {learner.uuid} is not present in any of " \
        f"the learner association group"
  assert resp.status_code == 404, f"Status Code = {resp.status_code}"
  assert resp_json["message"] == mes
