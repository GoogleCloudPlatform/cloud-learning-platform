"""
  Unit tests for Learner Profile endpoints
"""
import os
import json
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.learner_profile import router
from testing.test_config import (API_URL, TESTING_FOLDER_PATH)
from schemas.schema_examples import (BASIC_LEARNER_PROFILE_EXAMPLE,
                                     BASIC_LEARNER_EXAMPLE,
                                     BASIC_ACHIEVEMENT_EXAMPLE)
from common.models import LearnerProfile, Learner, Achievement
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/learner-profile-service/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/learner-profile"
api_url_with_learner = f"{API_URL}/learner"

LEARNER_PROFILE_TESTDATA_FILENAME = os.path.join(TESTING_FOLDER_PATH,
                                                 "learner_profiles.json")

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_get_learner_profile(clean_firestore):
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner_dict["email_address"] = "jon_doe_tglp@gmail.com"
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()
  learner_id = learner.id

  learner_profile_dict = {**BASIC_LEARNER_PROFILE_EXAMPLE,
                          "learner_id": learner_id}
  learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  learner_profile.uuid = ""
  learner_profile.save()
  learner_profile.uuid = learner_profile.id
  learner_profile.update()
  learner_profile_dict["uuid"] = learner_profile.id
  learner_profile_dict["is_archived"] = False

  # pylint: disable-next = line-too-long
  url = f"{api_url_with_learner}/{learner_id}/learner-profile"
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  del json_response["data"]["created_time"]
  del json_response["data"]["last_modified_time"]
  assert resp.status_code == 200, "Status 200"
  assert json_response.get("data") == learner_profile_dict, "Response received"


def test_get_learner_profile_negative_1(clean_firestore):
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner_dict["email_address"] = "jon_doe_tglpn@gmail.com"
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()
  learner_id = learner.id

  url = f"{api_url_with_learner}/{learner_id}/learner-profile"
  expected_response = {
    "success": False,
    "message": f"LearnerProfile with learner id {learner_id} not found",
    "data": None
  }

  resp = client_with_emulator.get(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == expected_response, "Response received"


def test_get_learner_profile_negative_2(clean_firestore):
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner_dict["email_address"] = "jon_doe_tglp@gmail.com"
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()
  learner_id = learner.id

  learner_profile_dict = {**BASIC_LEARNER_PROFILE_EXAMPLE,
                          "learner_id": learner_id}
  learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  learner_profile.uuid = ""
  learner_profile.is_deleted = True
  learner_profile.save()
  learner_profile.uuid = learner_profile.id
  learner_profile.update()
  learner_profile_dict["uuid"] = learner_profile.id
  learner_profile_dict["is_archived"] = False

  # pylint: disable-next = line-too-long
  url = f"{api_url_with_learner}/{learner_id}/learner-profile"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  expected_response = {
    "success": False,
    "message": f"LearnerProfile with learner id {learner_id} not found",
    "data": None
  }

  assert resp.status_code == 404, "Status 404"
  assert json_response == expected_response, "Response received"


def test_get_all_learner_profiles(clean_firestore):
  learner_profile_dict = {**BASIC_LEARNER_PROFILE_EXAMPLE}

  if "Teamwork" not in learner_profile_dict["learning_goals"]:
    learner_profile_dict["learning_goals"] = learner_profile_dict[
      "learning_goals"].append("Teamwork")

  # learner_profile
  learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  learner_profile.uuid = ""
  learner_profile.save()
  learner_profile.uuid = learner_profile.id
  learner_profile.update()

  # deleted learner profile
  deleted_learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  deleted_learner_profile.uuid = ""
  deleted_learner_profile.is_deleted = True
  deleted_learner_profile.save()
  deleted_learner_profile.uuid = deleted_learner_profile.id
  deleted_learner_profile.update()

  # archived learner profile
  archived_learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  archived_learner_profile.uuid = ""
  archived_learner_profile.is_archived = True
  archived_learner_profile.save()
  archived_learner_profile.uuid = archived_learner_profile.id
  archived_learner_profile.update()
  params = {"skip": 0, "limit": "30", "fetch_archive": False}

  url = f"{api_url}"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  retrieved_ids = [i.get("uuid") for i in json_response.get("data")["records"]]

  assert len(retrieved_ids) > 0, \
    "Atleast one result should be there"
  assert learner_profile.uuid in \
         retrieved_ids, "expected data not retrived"
  assert deleted_learner_profile.uuid not in \
         retrieved_ids, "unexpected data retrived"
  assert archived_learner_profile.uuid not in retrieved_ids, \
    "is_archived not working"


def test_get_all_learner_profiles_with_filters(clean_firestore):
  learner_profile_dict = {**BASIC_LEARNER_PROFILE_EXAMPLE}

  if "Teamwork" not in learner_profile_dict["learning_goals"]:
    learner_profile_dict["learning_goals"].append("Teamwork")

  learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  learner_profile.uuid = ""
  learner_profile.save()
  learner_profile.uuid = learner_profile.id
  learner_profile.update()
  learner_profile_dict["uuid"] = learner_profile.id

  # deleted learner profile
  deleted_learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  deleted_learner_profile.uuid = ""
  deleted_learner_profile.is_deleted = True
  deleted_learner_profile.save()
  deleted_learner_profile.uuid = deleted_learner_profile.id
  deleted_learner_profile.update()

  filter_params = {"learning_goal": "Teamwork"}
  url = f"{api_url}"
  resp = client_with_emulator.get(url, params=filter_params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"

  retrieved_ids = [i.get("uuid") for i in json_response.get("data")["records"]]
  assert len(
    json_response.get("data")["records"]) > 0, "Results should not be empty"
  assert learner_profile.uuid in \
         retrieved_ids, "expected data not retrived"
  assert deleted_learner_profile.uuid not in \
    retrieved_ids, "unexpected data retrived"
  for i in json_response.get("data")["records"]:
    assert "Teamwork" in i["learning_goals"],\
      "Filtered output is wrong"


def test_get_all_learner_profiles_with_filters_negative(clean_firestore):
  filter_params = {"skip": -1, "learning_goal": "Teamwork"}

  url = f"{api_url}"
  resp = client_with_emulator.get(url, params=filter_params)
  json_response = resp.json()
  assert resp.status_code == 422, "Status should be 422"
  assert json_response.get(
    "message"
    # pylint: disable-next = line-too-long
  ) == "Validation Failed"


def test_get_learner_profile_with_learner_id(clean_firestore):
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner_dict["email_address"] = "jon_doe_tglpwli@gmail.com"
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()
  learner_id = learner.id

  # learner_profile
  learner_profile_dict = {**BASIC_LEARNER_PROFILE_EXAMPLE,
                          "learner_id": learner_id}
  learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  learner_profile.uuid = ""
  learner_profile.save()
  learner_profile.uuid = learner_profile.id
  learner_profile.update()
  learner_profile_id = learner_profile.id

  url = f"{api_url_with_learner}/{learner_id}/learner-profile"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"
  assert json_response.get("data").get(
    "uuid") == learner_profile_id, "Learner profile id does not match"


def test_get_learner_profile_with_learner_id_negative1(clean_firestore):
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner_dict["email_address"] = "jon_doe_tglpwli@gmail.com"
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()
  learner_id = learner.id

  # deleted learner profile
  learner_profile_dict = {**BASIC_LEARNER_PROFILE_EXAMPLE,
                          "learner_id": learner_id}
  deleted_learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  deleted_learner_profile.uuid = ""
  deleted_learner_profile.is_deleted = True
  deleted_learner_profile.save()
  deleted_learner_profile.uuid = deleted_learner_profile.id
  deleted_learner_profile.update()

  url = f"{api_url_with_learner}/{learner_id}/learner-profile"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 404, "Status should be 404"
  assert json_response.get("message") == (f"LearnerProfile with learner id "
                                          f"{learner_id} not found"), \
    "LearnerProfile should be present with the given learner id"


def test_get_learner_profile_with_learner_id_negative2(clean_firestore):
  learner_id = "random_learner_id"
  url = f"{api_url_with_learner}/{learner_id}/learner-profile"
  resp = client_with_emulator.get(url)
  json_response = resp.json()

  assert resp.status_code == 404, "Status should be 404"
  assert json_response.get(
    "message"
  ) == f"Learner with uuid {learner_id} not found", \
    "Learner should be present with the given learner id"


def test_post_learner_profile(clean_firestore):
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner_dict["email_address"] = "jon_doe_tplp@gmail.com"
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()
  learner_id = learner.id

  input_learner_profile = BASIC_LEARNER_PROFILE_EXAMPLE
  url = f"{api_url_with_learner}/{learner_id}/learner-profile"
  post_resp = client_with_emulator.post(url, json=input_learner_profile)
  post_resp_json = post_resp.json()

  assert post_resp_json.get("success") is True, "Success not true"
  assert post_resp.status_code == 200, "Status 200"

  post_json_response = json.loads(post_resp.text)
  del post_json_response["data"]["created_time"]
  del post_json_response["data"]["last_modified_time"]
  uuid = post_json_response.get("data").get("uuid")

  # now see if GET endpoint returns same data
  url = f"{api_url_with_learner}/{learner_id}/learner-profile"
  get_resp = client_with_emulator.get(url)
  get_json_response = json.loads(get_resp.text)
  del get_json_response["data"]["created_time"]
  del get_json_response["data"]["last_modified_time"]
  assert get_json_response.get("data") == post_json_response.get("data")

  # now check and confirm it is properly in the database
  loaded_learner_profile = LearnerProfile.find_by_uuid(uuid)
  loaded_learner_profile_dict = loaded_learner_profile.to_dict()

  # popping id and key for equivalency test
  loaded_learner_profile_dict.pop("id")
  loaded_learner_profile_dict.pop("key")
  loaded_learner_profile_dict.pop("created_by")
  loaded_learner_profile_dict.pop("created_time")
  loaded_learner_profile_dict.pop("last_modified_by")
  loaded_learner_profile_dict.pop("last_modified_time")
  loaded_learner_profile_dict.pop("is_deleted")

  # assert that rest of the fields are equivalent
  assert loaded_learner_profile_dict == post_json_response.get("data")

def test_update_learner_profile(clean_firestore):
  achievement_dict = {**BASIC_ACHIEVEMENT_EXAMPLE}
  achievement = Achievement.from_dict(achievement_dict)
  achievement.uuid = ""
  achievement.save()
  achievement.uuid = achievement.id
  achievement.update()
  achievement_uuid = achievement.id

  learner_dict = BASIC_LEARNER_EXAMPLE
  learner_dict["email_address"] = "jon_doe_tulp@gmail.com"
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()
  learner_id = learner.id

  learner_profile_dict = {**BASIC_LEARNER_PROFILE_EXAMPLE,
                          "learner_id": learner_id}
  learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  learner_profile.uuid = ""
  learner_profile.save()
  learner_profile.uuid = learner_profile.id
  learner_profile.update()

  # pylint: disable-next = line-too-long
  url = f"{api_url_with_learner}/{learner_id}/learner-profile"
  updated_data = learner_profile_dict
  updated_data["achievements"] = [achievement_uuid]
  del updated_data["enrollment_information"]
  del updated_data["learner_id"]

  resp = client_with_emulator.put(url, json=updated_data)
  json_response_update_req = resp.json()

  assert resp.status_code == 200, "Status should be 200"
  assert json_response_update_req.get(
    "message"
  ) == "Successfully updated the learner profile", "Expected response not same"
  assert achievement_uuid in json_response_update_req.get("data").get(
    "achievements")


def test_update_learner_profile_negative_1(clean_firestore):
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner_dict["email_address"] = "jon_doe_tulp@gmail.com"
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()
  learner_id = learner.id

  learner_profile_dict = {**BASIC_LEARNER_PROFILE_EXAMPLE,
                          "learner_id": learner_id}
  learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  learner_profile.uuid = ""
  learner_profile.save()
  learner_profile.uuid = learner_profile.id
  learner_profile.update()

  # pylint: disable-next = line-too-long
  url = f"{api_url_with_learner}/{learner_id}/learner-profile"
  updated_data = learner_profile_dict
  updated_data["education_history"] = {
    "degree": "Associate Degree in Computer Science"
  }
  del updated_data["enrollment_information"]
  del updated_data["learner_id"]

  resp = client_with_emulator.put(url, json=updated_data)

  assert resp.status_code == 422, "Status should be 422"


def test_update_learner_profile_negative_2(clean_firestore):
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner_dict["email_address"] = "jon_doe_tulpn@gmail.com"
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()
  learner_id = learner.id

  learner_profile_dict = {**BASIC_LEARNER_PROFILE_EXAMPLE,
                          "learner_id": learner_id}
  learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  learner_profile.uuid = ""
  learner_profile.save()
  learner_profile.uuid = learner_profile.id
  learner_profile.update()
  del learner_profile_dict["learner_id"]
  del learner_profile_dict["enrollment_information"]

  random_learner_id = "U2DDBkl3Ayg0PWudzhI"

  # pylint: disable-next = line-too-long
  url = f"{api_url_with_learner}/{random_learner_id}/learner-profile"
  response = {
    "success": False,
    "message": "Learner with uuid U2DDBkl3Ayg0PWudzhI not found",
    "data": None
  }

  resp = client_with_emulator.put(url, json=learner_profile_dict)
  json_response = resp.json()

  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_delete_learner_profile(clean_firestore):
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner_dict["email_address"] = "jon_doe_tdlp@gmail.com"
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()
  learner_id = learner.id

  learner_profile_dict = {**BASIC_LEARNER_PROFILE_EXAMPLE,
                          "learner_id": learner_id}
  learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  learner_profile.uuid = ""
  learner_profile.save()
  learner_profile.uuid = learner_profile.id
  learner_profile.update()
  learner_profile_dict["uuid"] = learner_profile.id

  uuid = learner_profile.uuid
  learner_profile_dict["uuid"] = uuid

  url = f"{api_url_with_learner}/{learner_id}/learner-profile"
  resp = client_with_emulator.delete(url)
  del_json_response = resp.json()

  expected_data = {
    "success": True,
    "message": "Successfully deleted the learner profile"
  }
  deleted_learner_profile = LearnerProfile.find_by_uuid(
    learner_profile.uuid, is_deleted=True)
  assert resp.status_code == 200, "Status code not 200"
  assert deleted_learner_profile.is_deleted is True, "Document was not deleted"
  assert del_json_response == expected_data, "Expected response not same"


def test_delete_learner_profile_negative(clean_firestore):
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner_dict["email_address"] = "jon_doe_tdlpn@gmail.com"
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  random_learner_id = "U2DDBkl3Ayg0PWudzhI"
  # pylint: disable-next = line-too-long
  url = f"{api_url_with_learner}/{random_learner_id}/learner-profile"
  response = {
    "success": False,
    "message": "Learner with uuid U2DDBkl3Ayg0PWudzhI not found",
    "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = resp.json()
  assert resp.status_code == 404, "Status 404"
  assert json_response == response, "Expected response not same"


def test_import_learner_profiles(clean_firestore):
  url = f"{api_url}/import/json"
  with open(
    LEARNER_PROFILE_TESTDATA_FILENAME,
    encoding="UTF-8") as learner_profiles_json_file:
    resp = client_with_emulator.post(
      url, files={"json_file": learner_profiles_json_file})

  json_response = resp.json()
  assert resp.status_code == 200, "Status not 200"
  assert isinstance(json_response.get("data"), list), "Response is not a list"
  assert len(json_response.get("data")) > 0, "Empty list returned"


def test_search_learner_profile(clean_firestore):
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner_dict["email_address"] = "jon_doe_tslp@gmail.com"
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  learner_profile_dict = {**BASIC_LEARNER_PROFILE_EXAMPLE,
                          "learner_id": learner.id}
  learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  learner_profile.uuid = ""
  learner_profile.save()
  learner_profile.uuid = learner_profile.id
  learner_profile.update()
  learner_profile_dict["uuid"] = learner_profile.id

  # deleted learner profile
  deleted_learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  deleted_learner_profile.uuid = ""
  deleted_learner_profile.is_deleted = True
  deleted_learner_profile.save()
  deleted_learner_profile.uuid = deleted_learner_profile.id
  deleted_learner_profile.update()

  params = {"learner_id": learner.id}

  url = f"{api_url}/search"
  resp = client_with_emulator.get(url, params=params)
  json_response = resp.json()
  assert resp.status_code == 200, "Status 200"
  retrieved_ids = [i.get("uuid") for i in json_response.get("data")]
  assert learner_profile.uuid in \
         retrieved_ids, "expected data not retrived"
  assert deleted_learner_profile.uuid not in \
         retrieved_ids, "unexpected data retrived"
  assert json_response.get("data")[0].get(
    "learner_id") == learner.id, "Response received"
