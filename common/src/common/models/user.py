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
from common.utils.errors import ResourceNotFoundException
from fireo.fields import TextField,DateTime

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
PROJECT_ID = os.environ.get("PROJECT_ID", "")


class User(BaseModel):
  """
  User ORM class
  """
  uuid=TextField()
  auth_id=TextField(required=True)
  email=TextField(required=True)
  role=TextField()
  created_timestamp = DateTime()
  last_updated_timestamp = DateTime()

  class Meta:
    ignore_none_field = False
    collection_name = DATABASE_PREFIX + "user"

  @classmethod
  def find_by_email(cls, email):
    """Find a user using email (string)
    Args:
        email (string): User Email
    Returns:
        User: User Object
    """
    user= User.collection.filter("email", "==", email).get()
    if user is None:
      raise ResourceNotFoundException(f"User with email {email} is not found")
    return user

  @classmethod
  def find_by_uuid(cls, uuid):
    """Find a user using uuid (UUID)
    Args:
        uuid (string): User ID
    Returns:
        User: User Object
    """
    user=User.collection.filter("uuid", "==", uuid).get()
    if user is None:
      raise ResourceNotFoundException(f"User with uuid {uuid} is not found")
    return user
