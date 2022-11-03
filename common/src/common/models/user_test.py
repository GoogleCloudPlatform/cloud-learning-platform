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

from common.models import User
from common.testing.example_objects import TEST_USER


def test_new_user():
  # a placeholder unit test so github actions runs until we add more
  user = User.from_dict(TEST_USER)

  assert user.auth_id == TEST_USER["auth_id"]

def test_find_by_uuid():
  pass
