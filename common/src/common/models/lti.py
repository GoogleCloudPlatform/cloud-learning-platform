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
from fireo.fields import TextField, ListField, BooleanField, MapField, NumberField, IDField
from common.utils.errors import ResourceNotFoundException
from common.models import BaseModel
# pylint: disable = invalid-name


class Tool(BaseModel):
  """LTI Tool Data Model"""
  id = IDField()
  name = TextField(required=True)
  description = TextField()
  tool_url = TextField(required=True)
  tool_login_url = TextField(required=True)
  client_id = TextField(required=True)
  public_key_type = TextField(required=True)
  deeplink_type = TextField(required=True)
  tool_public_key = TextField()
  tool_keyset_url = TextField()
  content_selection_url = TextField()
  redirect_uris = ListField(required=True)
  deployment_id = TextField(required=True)
  enable_grade_sync = BooleanField(default=False)
  enable_nrps = BooleanField(default=False)
  custom_params = TextField(default=None)
  validate_title_for_grade_sync = BooleanField(default=False)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "tools"
    ignore_none_field = False

  @classmethod
  def find_by_client_id(cls, client_id):
    tool = cls.collection.filter("client_id", "==", client_id).get()
    if tool is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with client_id {client_id} not found")
    return tool

  @classmethod
  def find_by_tool_url(cls, tool_url):
    tool = cls.collection.filter("tool_url", "==",
                                 tool_url).filter("deleted_at_timestamp", "==",
                                                  None).get()
    return tool


class Platform(BaseModel):
  """LTI Platform Data Model"""
  id = IDField()
  name = TextField(required=True)
  description = TextField()
  issuer = TextField(required=True)
  client_id = TextField(required=True)
  platform_keyset_url = TextField(required=True)
  platform_auth_url = TextField(required=True)
  platform_token_url = TextField(required=True)
  deployment_ids = ListField(required=True)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "platforms"
    ignore_none_field = False

  @classmethod
  def find_by_issuer(cls, issuer):
    platform = cls.collection.filter("issuer", "==",
                                     issuer).filter("deleted_at_timestamp",
                                                    "==", None).get()
    return platform

  @classmethod
  def find_by_client_id(cls, client_id):
    platform = cls.collection.filter("client_id", "==",
                                     client_id).filter("deleted_at_timestamp",
                                                       "==", None).get()
    return platform


class LTIContentItem(BaseModel):
  """LTI Content Item Data Model"""
  id = IDField()
  tool_id = TextField(required=True)
  content_item_type = TextField(required=True)
  content_item_info = MapField(required=True)
  context_id = TextField()

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "lti_content_items"
    ignore_none_field = False

  @classmethod
  def find_by_tool_id(cls, tool_id):
    lti_content_item_doc = cls.collection.filter(
        "tool_id", "==", tool_id).filter("deleted_at_timestamp", "==",
                                         None).get()
    return lti_content_item_doc

  @classmethod
  def filter_with_context_id_and_tool_id(cls, tool_id, context_id):
    lti_content_items = cls.collection.filter("tool_id", "==",tool_id)\
      .filter("context_id", "==", context_id)\
      .filter("deleted_at_timestamp", "==", None)\
      .fetch()
    return list(lti_content_items)


class LTISession(BaseModel):
  """LTI Session Data Model"""
  id = IDField()
  state = TextField(required=True)
  nonce = TextField(required=True)
  user_id = TextField(required=True)
  client_id = TextField(required=True)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "lti_sessions"
    ignore_none_field = False

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
  id = IDField()
  startDateTime = TextField()
  endDateTime = TextField()
  scoreMaximum = NumberField()
  label = TextField()
  tag = TextField()
  resourceId = TextField()
  resourceLinkId = TextField()
  contextId = TextField()

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "line_items"
    ignore_none_field = False

  @classmethod
  def find_by_resource_link_id(cls, resource_link_id):
    line_item = cls.collection.filter("resourceLinkId", "==",
                                      resource_link_id).get()
    return line_item


class Result(BaseModel):
  """LTI Result Data Model"""
  id = IDField()
  userId = TextField()
  resultScore = NumberField()
  resultMaximum = NumberField()
  comment = TextField()
  scoreOf = TextField()
  lineItemId = TextField()
  isGradeSyncCompleted = BooleanField(default=False)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "results"
    ignore_none_field = False

  @classmethod
  def find_by_line_item_id(cls, line_item_id):
    result = cls.collection.filter("lineItemId", "==", line_item_id)
    return result


class Score(BaseModel):
  """LTI Score Data Model"""
  id = IDField()
  userId = TextField()
  scoreGiven = NumberField()
  scoreMaximum = NumberField()
  comment = TextField()
  timestamp = TextField()
  activityProgress = TextField()
  gradingProgress = TextField()
  lineItemId = TextField()

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "scores"
    ignore_none_field = False
