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

from fireo.fields import TextField, IDField, ListField, BooleanField
from common.models import BaseModel
from common.utils.errors import ResourceNotFoundException

class User(BaseModel):
  """
  User ORM class
  """
  id=IDField()
  auth_id=TextField(required=True)
  email=TextField(required=True)
  role=TextField()

  class Meta:
    ignore_none_field = False
    collection_name = BaseModel.DATABASE_PREFIX + "users"

  @classmethod
  def find_by_email(cls, email):
    """Find a user using email (string)
    Args:
        email (string): User Email
    Returns:
        User: User Object
    """
    user = User.collection.filter("email", "==", email).filter(
        "deleted_at_timestamp", "==", None).get()
    if user is None:
      raise ResourceNotFoundException(f"User with email {email} is not found")
    return user


class UserGroup(BaseModel):
  """UserGroup Class"""
  uuid = TextField(required=True)
  name = TextField(required=True)
  description = TextField()
  alias = TextField(default="security groups")
  users = ListField(default=[])
  roles = ListField(default=[])
  permissions = ListField(default=[])
  applications = ListField(default=[])
  is_immutable = BooleanField(default=False)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "user_groups"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    """Find the group using uuid
    Args:
        uuid (string): uuid of group
    Returns:
        group Object
    """
    group = cls.collection.filter("uuid", "==", uuid).get()
    if group is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with uuid {uuid} not found")
    return group

  @classmethod
  def find_by_name(cls, name):
    """Find the UserGroup using name
    Args:
        name (string): node item name
    Returns:
        UserGroup: UserGroup Object
    """
    return cls.collection.filter("name", "==", name).get()


class Permission(BaseModel):
  """Permission Class"""
  uuid = TextField(required=True)
  name = TextField(required=True)
  description = TextField()
  application_id = TextField(required=True)
  module_id = TextField(required=True)
  action_id = TextField(required=True)
  user_groups = ListField(default=[])

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "permissions"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    """Find the permission using uuid
    Args:
        uuid (string): uuid of permission
    Returns:
        permission Object
    """
    permission = cls.collection.filter("uuid", "==", uuid).get()
    if permission is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with uuid {uuid} not found")
    return permission

  @classmethod
  def find_by_name(cls, name):
    """Find the Permission using name
    Args:
        name (string): node item name
    Returns:
        Permission: Permission Object
    """
    return cls.collection.filter("name", "==", name).get()


class Application(BaseModel):
  """Application Class"""
  uuid = TextField(required=True)
  name = TextField(required=True)
  description = TextField()
  modules = ListField(default=[])

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "applications"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    """Find the application using uuid
    Args:
        uuid (string): uuid of application
    Returns:
        Application Object
    """
    application = cls.collection.filter("uuid", "==", uuid).get()
    if application is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with uuid {uuid} not found")
    return application

  @classmethod
  def find_by_name(cls, name):
    """Find the application using name
    Args:
        name (string): node item name
    Returns:
        Application: Application Object
    """
    return cls.collection.filter("name", "==", name).get()


def check_action_type(field_val):
  """validator method for action_type field"""
  action_types = ["main", "other"]
  if field_val.lower() in action_types:
    return True
  return (False, "action_type must be one of " +
          ",".join("'" + i + "'" for i in action_types))


class Action(BaseModel):
  """Action Class"""
  uuid = TextField(required=True)
  name = TextField(required=True)
  description = TextField()
  action_type = TextField(validator=check_action_type)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "actions"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    """Find the scope using uuid
    Args:
        uuid (string): uuid of scope
    Returns:
        scope Object
    """
    scope = cls.collection.filter("uuid", "==", uuid).get()
    if scope is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with uuid {uuid} not found")
    return scope

  @classmethod
  def find_by_name(cls, name):
    """Find the Action using name
    Args:
        name (string): node item name
    Returns:
        Action: Action Object
    """
    return cls.collection.filter("name", "==", name).get()

class Module(BaseModel):
  """Module Class"""
  uuid = TextField(required=True)
  name = TextField(required=True)
  description = TextField()
  actions = ListField(default=[])

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "modules"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    """Find the module using uuid
    Args:
        uuid (string): uuid of module
    Returns:
        module Object
    """
    module = cls.collection.filter("uuid", "==", uuid).get()
    if module is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with uuid {uuid} not found")
    return module

  @classmethod
  def find_by_name(cls, name):
    """Find the module using name
    Args:
        name (string): node item name
    Returns:
        Module: Module Object
    """
    return cls.collection.filter("name", "==", name).get()
