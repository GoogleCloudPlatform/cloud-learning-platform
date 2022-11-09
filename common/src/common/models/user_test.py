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
Unit Tests for user ORM object
"""
# disabling these rules, as they cause issues with pytest fixtures
# pylint: disable=unused-import
# pylint: disable=unused-argument,redefined-outer-name
from common.models import User
from common.testing.example_objects import TEST_USER
from common.testing.firestore_emulator import client_with_emulator, firestore_emulator, clean_firestore


def test_new_user(client_with_emulator):
  # a placeholder unit test so github actions runs until we add more
  new_user = User.from_dict(TEST_USER)
  new_user.save()
  new_user.uuid=new_user.id
  new_user.update()
  user=User.find_by_uuid(new_user.uuid)
  assert user.auth_id == TEST_USER["auth_id"]
  assert user.email==TEST_USER["email"]

def test_find_by_email(client_with_emulator):
  '''test for finding user by email method'''
  new_user = User.from_dict(TEST_USER)
  new_user.save()
  new_user.uuid = new_user.id
  TEST_USER["uuid"]=new_user.uuid
  new_user.update()
  user = User.find_by_uuid(new_user.email)
  assert user.auth_id == TEST_USER["auth_id"]
  assert user.uuid == TEST_USER["uuid"]

def test_delete_user(client_with_emulator):
  '''test for soft delete method'''
  new_user = User.from_dict(TEST_USER)
  new_user.save()
  new_user.uuid = new_user.id
  new_user.update()
  assert User.archive_by_uuid('fakeuuid') is False, "User not found"
  assert User.archive_by_uuid(new_user.uuid) is True, "User successfully deleted"
  