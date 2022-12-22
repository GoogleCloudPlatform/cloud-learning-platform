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
import pytest
from common.models import User
from common.utils.errors import ResourceNotFoundException
from common.testing.example_objects import TEST_USER
from common.testing.firestore_emulator import firestore_emulator, clean_firestore


def test_new_user(clean_firestore):
  # a placeholder unit test so github actions runs until we add more
  new_user = User.from_dict(TEST_USER)
  new_user.save()
  user = User.find_by_id(new_user.id)
  assert user.auth_id == TEST_USER["auth_id"]
  assert user.email == TEST_USER["email"]


def test_find_by_email(clean_firestore):
  '''test for finding user by email method'''
  new_user = User.from_dict(TEST_USER)
  new_user.save()
  user = User.find_by_email(new_user.email)
  assert user.auth_id == TEST_USER["auth_id"]


def test_delete_user(clean_firestore):
  '''test for soft delete method'''
  new_user = User.from_dict(TEST_USER)
  new_user.save()
  assert User.find_by_id(new_user.id) is not None
  User.soft_delete_by_id(new_user.id)
  with pytest.raises(ResourceNotFoundException):
      User.soft_delete_by_id(new_user.id)
