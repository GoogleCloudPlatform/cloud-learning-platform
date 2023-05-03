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
User Data Model
"""
import regex
from common.models import BaseModel
from common.utils.errors import ResourceNotFoundException
from fireo.fields import (TextField)

USER_TYPES = [
    "learner", "faculty", "assessor", "admin", "coach", "instructor", "lxe",
    "curriculum_designer"
]


def validate_name(name):
  """Validator method to validate name"""
  if regex.fullmatch(r"[\D\p{L}\p{N}\s]+$", name):
    return True
  else:
    return (False, "Invalid name format")


def check_user_type(field_val):
  """validator method for user type field"""
  if field_val.lower() in USER_TYPES:
    return True
  return (False, "User Type must be one of " + ",".join("'" + i + "'"
                                                        for i in USER_TYPES))


def check_status(field_val):
  """validator method for status field"""
  status = ["active", "inactive"]
  if field_val.lower() in ["active", "inactive"]:
    return True
  return (False, "Status must be one of " + ",".join("'" + i + "'"
                                                     for i in status))


class User(BaseModel):
  """User Class for course enrollment mapping"""
  user_id = TextField(required=True)
  first_name = TextField(required=True, validator=validate_name)
  last_name = TextField(required=True, validator=validate_name)
  email = TextField(required=True, to_lowercase=True)
  user_type = TextField(required=True, validator=check_user_type)
  status = TextField(validator=check_status)
  gaia_id = TextField()
  photo_url = TextField()

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
    user = cls.collection.filter("user_id", "==", user_id).get()
    if user is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with user_id {user_id} not found")
    return user

  @classmethod
  def find_by_email(cls, email):
    """Find the user using email
    Args:
        email (string): user's email address
    Returns:
        User: User Object
    """
    if email:
      email = email.lower()
    return cls.collection.filter("email", "==", email).get()

  @classmethod
  def find_by_status(cls, status):
    """Find the user using status
    Args:
        status (string): user's status
    Returns:
        List of User objects
    """
    return cls.collection.filter("status", "==", status).fetch()

  @classmethod
  def find_by_gaia_id(cls, gaia_id):
    """Find the user using gaia id
    Args:
        gaia_id (string): user's gaia_id
    Returns:
        User: User Object
    """
    user = cls.collection.filter("gaia_id", "==", gaia_id).get()
    if user is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with gaia_id {gaia_id} not found")
    return user
