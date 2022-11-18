# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
  Tests for User endpoints
"""
import os
import json
import datetime

# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from common.testing.firestore_emulator import firestore_emulator, clean_firestore
from common.testing.client_with_emulator import client_with_emulator
from common.models import User
from schemas.schema_examples import USER_EXAMPLE
from testing.test_config import BASE_URL
import mock

# assigning url

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"
SUCCESS_RESPONSE = {"status": "Success"}


def test_get_user(client_with_emulator):
  user_dict = USER_EXAMPLE
  user = User.from_dict(user_dict)
  user.save()

  url = BASE_URL + f"/users/{user.uuid}"
  data = USER_EXAMPLE
  resp = client_with_emulator.get(url)
  json_response = json.loads(resp.text)

  assert resp.status_code == 200, "Status 200"
  assert json_response == data, "Return data doesn't match."


def test_get_nonexist_user(client_with_emulator):
  uuid = "non_exist_uuid"
  url = BASE_URL + f"/users/{uuid}"
  data = {
    "success": False,
    "message": f"User with uuid {uuid} is not found",
    "data": None
  }
  resp = client_with_emulator.get(url)
  json_response = json.loads(resp.text)
  assert resp.status_code == 404, "Status 404"
  assert json_response == data, "Return data doesn't match."


def test_post_user_new(client_with_emulator):
  input_user = USER_EXAMPLE
  url = BASE_URL + "/users"
  with mock.patch("routes.user.Logger"):
    resp = client_with_emulator.post(url, json=input_user)
  print(resp.json())
  assert resp.status_code == 200, "Status 200"

  # now see if GET endpoint returns same data
  input_user["uuid"]=resp.json()
  url = BASE_URL + f"/users/{input_user['uuid']}"
  resp = client_with_emulator.get(url)
  json_response = json.loads(resp.text)
  assert json_response == input_user

  # now check and confirm it is properly in the databse
  loaded_user = User.find_by_uuid(input_user["uuid"])
  loaded_user_dict = loaded_user.to_dict()

  # popping id and key for equivalency test
  loaded_user_dict.pop("id")
  loaded_user_dict.pop("key")
  loaded_user_dict.pop("is_deleted")
  loaded_user_dict.pop("deleted_at_timestamp")

  timestamp = datetime.datetime.utcnow()

  # remove the timestamps since they aren't returned in the API
  # response doesn't include
  acceptable_sec_diff = 15
  created_timestamp = loaded_user_dict.pop("created_timestamp")
  last_updated_timestamp = loaded_user_dict.pop("last_updated_timestamp")

  assert (timestamp.second - created_timestamp.second) < acceptable_sec_diff
  assert (timestamp.second - 
                last_updated_timestamp.second) < acceptable_sec_diff
  # assert that rest of the fields are equivalent
  assert loaded_user_dict == input_user


def test_put_user(client_with_emulator):
  # create new user with POST to get timestamps
  input_user = USER_EXAMPLE
  url = BASE_URL + "/users"
  with mock.patch("routes.user.Logger"):
    resp = client_with_emulator.post(url, json=input_user)

  # modify user
  input_user["role"] = "User Admin"
  input_user["uuid"]=resp.json()

  url = BASE_URL + "/users"
  resp_data = SUCCESS_RESPONSE
  with mock.patch("routes.user.Logger"):
    resp = client_with_emulator.put(url, json=input_user)

  json_response = json.loads(resp.text)
  assert resp.status_code == 200, "Status 200"
  assert json_response == resp_data, "Response received"

  # now make sure user is updated and updated_timestamp is changed
  url = BASE_URL + f"/users/{input_user['uuid']}"
  resp = client_with_emulator.get(url)
  json_response = json.loads(resp.text)

  assert json_response == input_user

  # assert timestamp has been updated
  # loading from DB since not surfaced in API
  loaded_user = User.find_by_uuid(input_user["uuid"])
  created_timestamp = loaded_user.created_timestamp
  last_updated_timestamp = loaded_user.last_updated_timestamp
  assert created_timestamp < last_updated_timestamp


def test_put_user_negative(client_with_emulator):
  user_dict = USER_EXAMPLE
  user = User.from_dict(user_dict)
  user.save()

  input_user = USER_EXAMPLE
  input_user["uuid"] = "U2DDBkl3Ayg0PWudzhI"

  url = BASE_URL + "/users"
  with mock.patch("routes.user.Logger"):
    resp = client_with_emulator.put(url, json=input_user)

  assert resp.status_code == 404, "Status 404"


def test_delete_user(client_with_emulator):
  user_dict = USER_EXAMPLE
  user = User.from_dict(user_dict)
  user.save()

  # confirm in backend with API
  url = BASE_URL + f"/users/{user.uuid}"
  resp = client_with_emulator.get(url)
  assert resp.status_code == 200, "Status 200"

  # now delete user with API
  url = BASE_URL + f"/users/{user.uuid}"
  with mock.patch("routes.user.Logger"):
    resp = client_with_emulator.delete(url)

  assert resp.status_code == 200, "Status 200"

  # now confirm user gone with API
  url = BASE_URL + f"/users/{user.uuid}"
  resp = client_with_emulator.get(url)
  assert resp.status_code == 404, "Status 404"


def test_delete_user_negative(client_with_emulator):
  user_dict = USER_EXAMPLE
  user = User.from_dict(user_dict)
  user.save()

  url = BASE_URL + "/users/U2DDBkl3Ayg0PWudzhIi"
  with mock.patch("routes.user.Logger"):
    resp = client_with_emulator.delete(url)

  data = {
    "success": False,
    "message": "User with uuid U2DDBkl3Ayg0PWudzhIi is not found",
    "data": None
  }
  resp = client_with_emulator.delete(url)
  json_response = json.loads(resp.text)
  assert resp.status_code == 404, "Status 404"
  assert json_response == data, "Response received"
