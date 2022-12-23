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
from fireo.fields import TextField, NumberField, ListField, BooleanField
from common.models import BaseModel
from common.utils.errors import ResourceNotFoundException

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
PROJECT_ID = os.environ.get("PROJECT_ID", "")


def check_user_type(field_val):
  """validator method for user type field"""
  user_types = ["learner", "faculty", "other"]
  if field_val.lower() in user_types:
    return True
  return (False, "User Type must be one of " +
          ",".join("'" + i + "'" for i in user_types))


def check_status(field_val):
  """validator method for status field"""
  status = ["active", "inactive"]
  if field_val.lower() in ["active", "inactive"]:
    return True
  return (False,
          "Status must be one of " + ",".join("'" + i + "'" for i in status))


class TempUser(BaseModel):
  """User Class"""
  user_id = TextField(required=True)
  first_name = TextField(required=True)
  last_name = TextField(required=True)
  email = TextField(required=True)
  user_type = TextField(required=True, validator=check_user_type)
  user_type_ref = TextField()
  user_groups = ListField()
  status = TextField(validator=check_status)
  is_registered = BooleanField()
  failed_login_attempts_count = NumberField()
  access_api_docs = BooleanField(default=False)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "users"
    ignore_none_field = False

  @classmethod
  def find_by_user_id(cls, user_id):
    """Find the user using user_id
    Args:
        user_id (string): user_id of user
    Returns:
        user Object
    """
    user = TempUser.collection.filter("user_id", "==", user_id).get()
    if user is None:
      raise ResourceNotFoundException(f"User with user_id {user_id} not found")
    return user

  @classmethod
  def find_by_email(cls, email):
    """Find the user using email
    Args:
        email (string): user's email address
    Returns:
        User: User Object
    """
    return cls.collection.filter("email", "==", email).get()
