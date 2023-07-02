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
Models for LLM Query Engines
"""
from typing import List
from fireo.fields import (TextField, ListField, IDField,
                          BooleanField, NumberField)
from common.models import BaseModel

# constants used as tags for query history
QUERY_HUMAN = "HumanQuestion"
QUERY_AI_RESPONSE = "AIResponse"
QUERY_AI_REFERENCES = "AIReferences"

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

  def update_history(self, prompt: str, response: str, references: List[dict]):
    """ Update history with query and response """
    self.history.append(
      {QUERY_HUMAN: prompt}
    )
    self.history.append(
      {
        QUERY_AI_RESPONSE: response,
        QUERY_AI_REFERENCES: references
      }
    )
    self.update()

class QueryEngine(BaseModel):
  """
  QueryEngine ORM class
  """
  id = IDField()
  name = TextField(required=True)
  llm_type = TextField(required=True)
  created_by = TextField(required=True)
  is_public = BooleanField(default=False)
  index_id = TextField(required=False)
  index_name = TextField(required=False)
  endpoint = TextField(required=False)

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
            None).get()
    return q_engine

  @property
  def deployed_index_name(self):
    return f"deployed_{self.index_name}"


class QueryReference(BaseModel):
  """
  QueryReference ORM class. This class represents a single query reference.
  It points to a specific chunk of text in one of the indexed documents.

  """
  id = IDField()
  query_engine_id = TextField(required=True)
  query_engine = TextField(required=True)
  document_id = TextField(required=True)
  chunk_id = TextField(required=True)

  class Meta:
    ignore_none_field = False
    collection_name = BaseModel.DATABASE_PREFIX + "query_references"


class QueryResult(BaseModel):
  """
  QueryResult ORM class.  Each query result consists of a text query
  response and a list of links to source query documents, as a
  list of query reference ids.
  """
  id = IDField()
  query_engine_id = TextField(required=True)
  query_engine = TextField(required=True)
  query_refs = ListField(default=[])
  response = TextField(required=True)

  class Meta:
    ignore_none_field = False
    collection_name = BaseModel.DATABASE_PREFIX + "query_results"

  def load_references(self) -> List[QueryReference]:
    references = []
    for ref in self.get("query_refs"):
      obj = QueryReference.find_by_id(ref)
      if obj is not None:
        references.append(obj)
    return references


class QueryDocument(BaseModel):
  """
  QueryDocument ORM class.
  """
  id = IDField()
  query_engine_id = TextField(required=True)
  query_engine = TextField(required=True)
  doc_url = TextField(required=True)
  index_start = NumberField(required=True)
  index_end = NumberField(required=True)

  class Meta:
    ignore_none_field = False
    collection_name = BaseModel.DATABASE_PREFIX + "query_documents"


class QueryDocumentChunk(BaseModel):
  """
  QueryDocumentChunk ORM class.
  """
  id = IDField()
  query_engine_id = TextField(required=True)
  query_document_id = TextField(required=True)
  index = NumberField(required=True)
  text = TextField(required=True)

  class Meta:
    ignore_none_field = False
    collection_name = BaseModel.DATABASE_PREFIX + "query_document_chunks"

  @classmethod
  def find_by_index(cls, query_engine_id, index):
    """
    Fetch a document chunk for a query engine by index

    Args:
        query_engine_id (str): Query engine id
        index (str): QueryDocumentChunk index

    Returns:
        QueryDocumentChunk: query engine object

    """
    q_chunk = cls.collection.filter(
        "query_engine_id", "==", query_engine_id).filter(
            "index", "==", index).filter(
            "deleted_at_timestamp", "==",
            None).get()
    return q_chunk
