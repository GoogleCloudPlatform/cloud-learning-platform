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
"""LTI Service Data Models"""
import os
from fireo.fields import TextField, ListField, BooleanField, MapField, DateTime
from common.models import BaseModel
from common.utils.errors import ResourceNotFoundException

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
PROJECT_ID = os.environ.get("PROJECT_ID", "")


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
  created_timestamp = DateTime()
  last_updated_timestamp = DateTime()

  class Meta:
    collection_name = DATABASE_PREFIX + "tools"
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
  created_timestamp = DateTime()
  last_updated_timestamp = DateTime()

  class Meta:
    collection_name = DATABASE_PREFIX + "platforms"
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
  created_timestamp = DateTime()
  last_updated_timestamp = DateTime()

  class Meta:
    collection_name = DATABASE_PREFIX + "lti_content_items"
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
  created_timestamp = DateTime()
  last_updated_timestamp = DateTime()

  class Meta:
    collection_name = DATABASE_PREFIX + "lti_sessions"
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
