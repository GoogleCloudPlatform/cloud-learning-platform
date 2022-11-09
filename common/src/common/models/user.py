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

import datetime
import os

from common.models import BaseModel
from fireo.fields import TextField,DateTime,BooleanField

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
  is_deleted = BooleanField(default=False)
  created_timestamp = DateTime()
  last_updated_timestamp = DateTime()
  deleted_at_timestamp = DateTime()

  class Meta:
    ignore_none_field = False
    collection_name = DATABASE_PREFIX + "users"

  @classmethod
  def find_by_email(cls, email):
    """Find a user using email (string)
    Args:
        email (string): User Email
    Returns:
        User: User Object
    """
    user = User.collection.filter("email", "==", email).filter(
        "is_deleted", "==", False).get()
    return user

  @classmethod
  def find_by_uuid(cls, uuid):
    """Find a user using uuid (UUID)
    Args:
        uuid (string): User ID
    Returns:
        User: User Object
    """
    user = User.collection.filter("uuid", "==", uuid).filter(
        "is_deleted", "==", False).get()
    return user

  @classmethod
  def archive_by_uuid(cls, uuid):
    '''Soft Delete a User by using uuid
      Args:
          uuid (String): User ID
      '''
    user = User.collection.filter("uuid", "==", uuid).filter(
        "is_deleted", "==", False).get()
    if user is None:
      return False
    else:
      user.is_deleted = True
      user.deleted_at_timestamp = datetime.datetime.utcnow()
      user.update()
      return True
