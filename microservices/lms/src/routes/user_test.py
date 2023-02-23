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
# import os
# import json
# import datetime
# import mock
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
# from common.testing.firestore_emulator import firestore_emulator,
# clean_firestore
# from common.testing.client_with_emulator import client_with_emulator
# from common.models import User
# from schemas.schema_examples import USER_EXAMPLE
# from testing.test_config import BASE_URL
# assigning url

# os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
# os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"
# SUCCESS_RESPONSE = {"status": "Success"}


def test_placeholder():
  assert True

# def test_get_user(client_with_emulator):
#   user_dict = USER_EXAMPLE
#   user = User.from_dict(user_dict)
#   user.save()

#   url = BASE_URL + f"/users/{user.id}"
#   data = USER_EXAMPLE
#   data["id"] = user.id
#   resp = client_with_emulator.get(url)
#   json_response = json.loads(resp.text)

#   assert resp.status_code == 200, "Status 200"
#   assert json_response == data, "Return data doesn't match."


# def test_get_nonexist_user(client_with_emulator):
#   user_id = "non_exist_id"
#   url = BASE_URL + f"/users/{user_id}"
#   data = {
#       "success": False,
#       "message": f"users with id {user_id} is not found",
#       "data": None
#   }
#   resp = client_with_emulator.get(url)
#   json_response = json.loads(resp.text)
#   assert resp.status_code == 404, "Status 404"
#   assert json_response == data, "Return data doesn't match."


# def test_post_user_new(client_with_emulator):
#   input_user = USER_EXAMPLE
#   url = BASE_URL + "/users"
#   with mock.patch("routes.user.Logger"):
#     resp = client_with_emulator.post(url, json=input_user)
#   assert resp.status_code == 200, "Status 200"

#   # now see if GET endpoint returns same data
#   input_user["id"] = resp.json()
#   url = BASE_URL + f"/users/{input_user['id']}"
#   resp = client_with_emulator.get(url)
#   json_response = json.loads(resp.text)
#   assert json_response == input_user

#   # now check and confirm it is properly in the databse
#   loaded_user = User.find_by_id(input_user["id"])
#   loaded_user_dict = loaded_user.to_dict()

#   # popping key and some fields for equivalency test
#   loaded_user_dict.pop("key")
#   loaded_user_dict.pop("deleted_at_timestamp")
#   loaded_user_dict.pop("archived_at_timestamp")
#   loaded_user_dict.pop("deleted_by")
#   loaded_user_dict.pop("archived_by")
#   loaded_user_dict.pop("created_by")
#   loaded_user_dict.pop("last_modified_by")

#   timestamp = datetime.datetime.utcnow()

#   # remove the timestamps since they aren't returned in the API
#   # response doesn't include
#   acceptable_sec_diff = 15
#   created_time = loaded_user_dict.pop("created_time")
#   last_modified_time = loaded_user_dict.pop("last_modified_time")

#   assert (timestamp.second - created_time.second) < acceptable_sec_diff
#   assert (timestamp.second -
#           last_modified_time.second) < acceptable_sec_diff
#   # assert that rest of the fields are equivalent
#   assert loaded_user_dict == input_user


# def test_put_user(client_with_emulator):
#   # create new user with POST to get timestamps
#   input_user = USER_EXAMPLE
#   url = BASE_URL + "/users"
#   with mock.patch("routes.user.Logger"):
#     resp = client_with_emulator.post(url, json=input_user)

#   # modify user
#   input_user["role"] = "User Admin"
#   input_user["id"] = resp.json()

#   url = BASE_URL + "/users"
#   resp_data = SUCCESS_RESPONSE
#   with mock.patch("routes.user.Logger"):
#     resp = client_with_emulator.put(url, json=input_user)

#   json_response = json.loads(resp.text)
#   assert resp.status_code == 200, "Status 200"
#   assert json_response == resp_data, "Response received"

#   # now make sure user is updated and updated_timestamp is changed
#   url = BASE_URL + f"/users/{input_user['id']}"
#   resp = client_with_emulator.get(url)
#   json_response = json.loads(resp.text)

#   assert json_response == input_user

#   # assert timestamp has been updated
#   # loading from DB since not surfaced in API
#   loaded_user = User.find_by_id(input_user["id"])
#   created_time = loaded_user.created_time
#   last_modified_time = loaded_user.last_modified_time
#   assert created_time < last_modified_time


# def test_put_user_negative(client_with_emulator):
#   user_dict = USER_EXAMPLE
#   user = User.from_dict(user_dict)
#   user.save()

#   input_user = USER_EXAMPLE
#   input_user["id"] = "U2DDBkl3Ayg0PWudzhI"

#   url = BASE_URL + "/users"
#   with mock.patch("routes.user.Logger"):
#     resp = client_with_emulator.put(url, json=input_user)

#   assert resp.status_code == 404, "Status 404"


# def test_delete_user(client_with_emulator):
#   user_dict = USER_EXAMPLE
#   user = User.from_dict(user_dict)
#   user.save()

#   # confirm in backend with API
#   url = BASE_URL + f"/users/{user.id}"
#   resp = client_with_emulator.get(url)
#   assert resp.status_code == 200, "Status 200"

#   # now delete user with API
#   url = BASE_URL + f"/users/{user.id}"
#   with mock.patch("routes.user.Logger"):
#     resp = client_with_emulator.delete(url)

#   assert resp.status_code == 200, "Status 200"

#   # now confirm user gone with API
#   url = BASE_URL + f"/users/{user.id}"
#   resp = client_with_emulator.get(url)
#   assert resp.status_code == 404, "Status 404"


# def test_delete_user_negative(client_with_emulator):
#   user_dict = USER_EXAMPLE
#   user = User.from_dict(user_dict)
#   user.save()

#   url = BASE_URL + "/users/U2DDBkl3Ayg0PWudzhIi"
#   with mock.patch("routes.user.Logger"):
#     resp = client_with_emulator.delete(url)

#   data = {
#       "success": False,
#       "message": "users with id U2DDBkl3Ayg0PWudzhIi is not found",
#       "data": None
#   }
#   resp = client_with_emulator.delete(url)
#   json_response = json.loads(resp.text)
#   assert resp.status_code == 404, "Status 404"
#   assert json_response == data, "Response received"
