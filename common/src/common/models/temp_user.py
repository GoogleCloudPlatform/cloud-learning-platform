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
from datetime import datetime
import fireo
from fireo.models import Model
from fireo.fields import DateTime, TextField, NumberField, ListField, \
  BooleanField,MapField
from common.utils.errors import ResourceNotFoundException

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
PROJECT_ID = os.environ.get("PROJECT_ID", "")


def check_user_type(field_val):
  """validator method for user type field"""
  user_types = ["learner", "faculty", "robot",
            "assessor", "admin", "coach", "instructor",
              "lxe", "curriculum_designer"]
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


# pylint: disable = too-few-public-methods,pointless-string-statement,arguments-renamed,invalid-name
class TempBaseModel(Model):
  """BaseModel to add common helper methods to all FireO objects

  An interface, intended to be subclassed.

  """
  created_time = DateTime(auto=True)
  last_modified_time = DateTime(auto=True)
  created_by = TextField(default="")
  last_modified_by = TextField(default="")
  DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")

  def save(self, input_datetime=None, transaction=None, batch=None, merge=None):
    """overrides default method to save items with timestamp"""
    if input_datetime:
      datetime_value = input_datetime
    else:
      datetime_value = datetime.now()
    self.created_time = datetime_value
    self.last_modified_time = datetime_value
    super().save(transaction=transaction, batch=batch, merge=merge)

  def update(self, input_datetime=None, key=None, transaction=None, batch=None):
    """overrides default method to update items with timestamp"""
    if input_datetime:
      datetime_value = input_datetime
    else:
      datetime_value = datetime.now()
    self.last_modified_time = datetime_value
    super().update(key=key, transaction=transaction, batch=batch)

  def get_fields(self, reformat_datetime=False):
    """overrides default method to fix data type for datetime fields"""
    fields = super()._get_fields()
    if reformat_datetime:
      fields["created_time"] = str(fields["created_time"])
      fields["last_modified_time"] = str(fields["last_modified_time"])
    return fields

  class Meta:
    abstract = True

  @classmethod
  def find_by_id(cls, doc_id):
    """Looks up in the Database and returns an object of this type by
    id (not key)

    An interface, intended to be subclassed.

    Args:
      doc_id (string): the document id without collection_name (i.e. not the
      key)

    Returns:
      [any]: an instance of object returned by the database, type is the
      subclassed Model
    """
    key = fireo.utils.utils.generateKeyFromId(cls, doc_id)
    obj = cls.collection.get(key)
    if obj:
      return obj
    else:
      raise ResourceNotFoundException(f"Invalid {cls.__name__} ID: {doc_id}")

  @classmethod
  def delete_by_id(cls, doc_id):
    """Deletes from the Database the object of this type by id (not key)

    Args:
      doc_id (string): the document id without collection_name (i.e. not the
      key)

    Returns:
      None
    """
    key = fireo.utils.utils.generateKeyFromId(cls, doc_id)
    return cls.collection.delete(key)

  @classmethod
  def fetch_all_documents(cls, limit=1000):
    """Fetches all documents of the collection in batches

    Args:
      limit (int): the number of documents to fetch in a batch

    Returns:
      list (document objects): list of firestore document objects
    """
    all_docs = []
    docs = cls.collection.fetch(limit)
    while True:
      batch_docs = list(docs)
      if not batch_docs:
        break
      all_docs.extend(batch_docs)
      docs.next_fetch(limit)
    return all_docs

  @classmethod
  def delete_by_uuid(cls, uuid):
    doc = cls.collection.filter("uuid", "==",
                                uuid).filter("is_deleted", "==", False).get()
    if doc is not None:
      doc.is_deleted = True
      doc.update()
    else:
      raise ResourceNotFoundException(
          f"{cls.__name__} with uuid {uuid} not found")

  @classmethod
  def archive_by_uuid(cls, uuid, archive=True):
    doc = cls.collection.filter("uuid", "==",
                                uuid).filter("is_deleted", "==", False).get()
    if doc is not None:
      doc.is_archived = archive
      doc.update()
    else:
      raise ResourceNotFoundException\
        (f"{cls.__name__} with uuid {uuid} not found")


class TempUser(TempBaseModel):
  """User Class"""
  user_id = TextField(required=True)
  first_name = TextField(required=True)
  last_name = TextField(required=True)
  email = TextField(required=True)
  user_type = TextField(required=True, validator=check_user_type)
  user_type_ref = TextField(default="")
  user_groups = ListField()
  status = TextField(validator=check_status)
  is_registered = BooleanField()
  failed_login_attempts_count = NumberField()
  access_api_docs = BooleanField(default=False)
  gaia_id = TextField()
  photo_url = TextField()
  is_deleted = BooleanField(default=False)
  inspace_user = MapField(default={})

  class Meta:
    collection_name = TempBaseModel.DATABASE_PREFIX + "users"
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
