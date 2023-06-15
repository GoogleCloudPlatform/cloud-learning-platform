# Copyright 2023 Google LLC
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
Module to add cohort in Fireo
"""
from fireo.fields import TextField, ListField, IDField, BooleanField
from common.models import BaseModel

# constants used as tags for chat history
CHAT_HUMAN = "HumanInput"
CHAT_AI = "AIOutput"

class UserChat(BaseModel):
  """
  UserChat ORM class
  """
  id = IDField()
  user_id = TextField(required=True)
  title = TextField(required=False)
  llm_type = TextField(required=True)
  history = ListField(default=[])

  class Meta:
    ignore_none_field = False
    collection_name = BaseModel.DATABASE_PREFIX + "user_chats"

  @classmethod
  def find_by_user(cls,
                   userid,
                   skip=0,
                   order_by="-created_time",
                   limit=1000):
    """
    Fetch all chats for user

    Args:
        userid (str): User id
        skip (int, optional): number of chats to skip.
        order_by (str, optional): order list according to order_by field.
        limit (int, optional): limit till cohorts to be fetched.

    Returns:
        List[UserChat]: List of chats for user.

    """
    objects = cls.collection.filter(
        "user_id", "==", userid).filter(
            "deleted_at_timestamp", "==",
            None).order(order_by).offset(skip).fetch(limit)
    return list(objects)


class UserQuery(BaseModel):
  """
  UserQuery ORM class
  """
  id = IDField()
  user_id = TextField(required=True)
  title = TextField(required=False)
  query_engine_id = TextField(required=True)
  history = ListField(default=[])

  class Meta:
    ignore_none_field = False
    collection_name = BaseModel.DATABASE_PREFIX + "user_queries"

  @classmethod
  def find_by_user(cls,
                   userid,
                   skip=0,
                   order_by="-created_time",
                   limit=1000):
    """
    Fetch all queries for user

    Args:
        userid (str): User id
        skip (int, optional): number of chats to skip.
        order_by (str, optional): order list according to order_by field.
        limit (int, optional): limit till cohorts to be fetched.

    Returns:
        List[UserQuery]: List of queries for user.

    """
    objects = cls.collection.filter(
        "user_id", "==", userid).filter(
            "deleted_at_timestamp", "==",
            None).order(order_by).offset(skip).fetch(limit)
    return list(objects)


class QueryEngine(BaseModel):
  """
  QueryEngine ORM class
  """
  id = IDField()
  created_by = TextField(required=True)
  is_public = BooleanField(default=False)
  name = TextField(required=True)
  query_engine = TextField(required=True)
  history = ListField(default=[])

  class Meta:
    ignore_none_field = False
    collection_name = BaseModel.DATABASE_PREFIX + "query_engines"

  @classmethod
  def get_all_public(cls,
                     skip=0,
                     order_by="-created_time",
                     limit=1000):
    """
    Fetch all public query engines

    Args:

    Returns:
        List[QueryEngine]: List of public query engines

    """
    objects = cls.collection.filter(
        "is_public", "==", "true").filter(
            "deleted_at_timestamp", "==",
            None).order(order_by).offset(skip).fetch(limit)
    return list(objects)

  @classmethod
  def find_by_name(cls, name):
    """
    Fetch a specific query engine by name

    Args:
        name (str): Query engine name

    Returns:
        QueryEngine: query engine object

    """
    q_engine = cls.collection.filter(
        "name", "==", name).filter(
            "deleted_at_timestamp", "==",
            None).fetch()
    return q_engine


class QueryResult(BaseModel):
  """
  QueryResult ORM class.  Results consist of a list of query reference
  ids.
  """
  id = IDField()
  query_engine_id = TextField(required=True)
  query_engine = TextField(required=True)
  results = ListField(default=[])

  class Meta:
    ignore_none_field = False
    collection_name = BaseModel.DATABASE_PREFIX + "query_results"

  @classmethod
  def load_references(cls, query_result: str):
    references = []
    for ref in query_result.results:
      obj = cls.collection.filter(
          "id", "==", ref.id).filter(
              "deleted_at_timestamp", "==", None)
      if obj is not None:
        references.append(obj)
    return references


class QueryReference(BaseModel):
  """
  QueryReference ORM class.  Each reference consists of a text query
  response and a link to a source document.
  """
  id = IDField()
  query_engine_id = TextField(required=True)
  query_engine = TextField(required=True)
  query_response = TextField(required=True)
  reference_link = TextField(required=True)

  class Meta:
    ignore_none_field = False
    collection_name = BaseModel.DATABASE_PREFIX + "query_references"

