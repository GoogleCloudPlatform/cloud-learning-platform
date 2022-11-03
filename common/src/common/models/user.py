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
User object in the ORM
"""

import os

from common.models import BaseModel
from fireo.fields import TextField

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
PROJECT_ID = os.environ.get("PROJECT_ID", "")


# sample class
class User(BaseModel):
  """User ORM class
  """
  user_id = TextField()
  first_name = TextField()
  middle_name = TextField()
  last_name = TextField()
  date_of_birth = TextField()
  email_address = TextField()
  created_timestamp = TextField()
  last_updated_timestamp = TextField()

  class Meta:
    ignore_none_field = False
    collection_name = DATABASE_PREFIX + "users"

  # pylint: enable= line-too-long

  @classmethod
  def find_by_user_id(cls, uuid):
    """Find a user using user_id (UUID)
    Args:
        uuid (string): User ID
    Returns:
        User: User Object
    """
    return User.collection.filter("user_id", "==", uuid).get()
