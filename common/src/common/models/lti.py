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
"""Module to add common helper methods to all FireO objects"""
import os
from datetime import datetime
import fireo
from fireo.models import Model
from fireo.fields import DateTime, TextField, ListField, BooleanField, MapField, NumberField
from common.utils.errors import ResourceNotFoundException


# pylint: disable = too-few-public-methods,pointless-string-statement,arguments-renamed,invalid-name
class BaseModel(Model):
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


"""
  -----------------------
  LTI Service Data Models
  -----------------------
"""


class Tool(BaseModel):
  """LTI Tool Data Model"""
  uuid = TextField(required=True)
  name = TextField(required=True)
  description = TextField()
  tool_url = TextField(required=True)
  tool_login_url = TextField(required=True)
  client_id = TextField(required=True)
  public_key_type = TextField(required=True)
  tool_public_key = TextField()
  tool_keyset_url = TextField()
  content_selection_url = TextField()
  redirect_uris = ListField(required=True)
  deployment_id = TextField(required=True)
  is_archived = BooleanField(default=False)
  is_deleted = BooleanField(default=False)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "tools"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid, is_deleted=False):
    tool = cls.collection.filter("uuid", "==",
                                 uuid).filter("is_deleted", "==",
                                              is_deleted).get()
    if tool is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with uuid {uuid} not found")
    return tool

  @classmethod
  def find_by_client_id(cls, client_id, is_deleted=False):
    tool = cls.collection.filter("client_id", "==",
                                 client_id).filter("is_deleted", "==",
                                                   is_deleted).get()
    if tool is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with client_id {client_id} not found")
    return tool

  @classmethod
  def find_by_tool_url(cls, tool_url, is_deleted=False):
    tool = cls.collection.filter("tool_url", "==",
                                 tool_url).filter("is_deleted", "==",
                                                  is_deleted).get()
    return tool

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


class Platform(BaseModel):
  """LTI Platform Data Model"""
  uuid = TextField(required=True)
  name = TextField(required=True)
  description = TextField()
  issuer = TextField(required=True)
  client_id = TextField(required=True)
  platform_keyset_url = TextField(required=True)
  platform_auth_url = TextField(required=True)
  platform_token_url = TextField(required=True)
  deployment_ids = ListField(required=True)
  is_archived = BooleanField(default=False)
  is_deleted = BooleanField(default=False)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "platforms"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid, is_deleted=False):
    platform = cls.collection.filter("uuid", "==",
                                     uuid).filter("is_deleted", "==",
                                                  is_deleted).get()
    if platform is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with uuid {uuid} not found")
    return platform

  @classmethod
  def find_by_issuer(cls, issuer, is_deleted=False):
    platform = cls.collection.filter("issuer", "==",
                                     issuer).filter("is_deleted", "==",
                                                    is_deleted).get()
    return platform

  @classmethod
  def find_by_client_id(cls, client_id, is_deleted=False):
    platform = cls.collection.filter("client_id", "==",
                                     client_id).filter("is_deleted", "==",
                                                       is_deleted).get()
    return platform

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


class LTIContentItem(BaseModel):
  """LTI Content Item Data Model"""
  uuid = TextField(required=True)
  tool_id = TextField(required=True)
  content_item_type = TextField(required=True)
  content_item_info = MapField(required=True)
  is_archived = BooleanField(default=False)
  is_deleted = BooleanField(default=False)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "lti_content_items"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid, is_deleted=False):
    lti_content_item = cls.collection.filter("uuid", "==", uuid).filter(
        "is_deleted", "==", is_deleted).get()
    if lti_content_item is None:
      raise ResourceNotFoundException(
          f"LTI Content item with uuid {uuid} not found")
    return lti_content_item

  @classmethod
  def delete_by_uuid(cls, uuid):
    doc = cls.collection.filter("uuid", "==",
                                uuid).filter("is_deleted", "==", False).get()
    if doc is not None:
      doc.is_deleted = True
      doc.update()
    else:
      raise ResourceNotFoundException(
          f"LTI Content item with uuid {uuid} not found")

  @classmethod
  def find_by_tool_id(cls, tool_id):
    lti_content_item_doc = cls.collection.filter(
        "tool_id", "==", tool_id).filter("is_deleted", "==", False).get()
    return lti_content_item_doc


class LTISession(BaseModel):
  """LTI Session Data Model"""
  uuid = TextField(required=True)
  state = TextField(required=True)
  nonce = TextField(required=True)
  user_id = TextField(required=True)
  client_id = TextField(required=True)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "lti_sessions"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    session = cls.collection.filter("uuid", "==", uuid).get()
    if session is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with uuid {uuid} not found")
    return session

  @classmethod
  def find_by_client_id(cls, client_id):
    session = cls.collection.filter("client_id", "==", client_id).get()
    if session is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with client_id {client_id} not found")
    return session

  @classmethod
  def find_by_nonce(cls, nonce):
    session = cls.collection.filter("nonce", "==", nonce).get()
    if session is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with nonce {nonce} not found")
    return session


class LineItem(BaseModel):
  """LTI Line Item Data Model"""
  uuid = TextField()
  startDateTime = TextField()
  endDateTime = TextField()
  scoreMaximum = NumberField()
  label = TextField()
  tag = TextField()
  resourceId = TextField()
  resourceLinkId = TextField()

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "line_items"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    line_item = cls.collection.filter("uuid", "==", uuid).get()
    if line_item is None:
      raise ResourceNotFoundException(f"Line item with uuid {uuid} not found")
    return line_item


class Result(BaseModel):
  """LTI Result Data Model"""
  uuid = TextField()
  userId = TextField()
  resultScore = NumberField()
  resultMaximum = NumberField()
  comment = TextField()
  scoreOf = TextField()

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "results"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    result = cls.collection.filter("uuid", "==", uuid).get()
    if result is None:
      raise ResourceNotFoundException(f"Result with uuid {uuid} not found")
    return result


class Score(BaseModel):
  """LTI Score Data Model"""
  uuid = TextField()
  userId = TextField()
  scoreGiven = NumberField()
  scoreMaximum = NumberField()
  comment = TextField()
  timestamp = TextField()
  activityProgress = TextField()
  gradingProgress = TextField()

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "scores"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    score = cls.collection.filter("uuid", "==", uuid).get()
    if score is None:
      raise ResourceNotFoundException(f"Score with uuid {uuid} not found")
    return score
