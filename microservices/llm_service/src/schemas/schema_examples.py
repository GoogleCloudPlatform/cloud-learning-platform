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

""" Schema examples and test objects for unit tests """
# pylint: disable = line-too-long

LLM_GENERATE_EXAMPLE = {
  "llm_type": "",
  "prompt": "",
  "context": "",
  "primer":  ""
}

QUERY_EXAMPLE = {
  "prompt": "test prompt",
  "llm_type": "VertexAI-Chat"
}

USER_QUERY_EXAMPLE = {
  "id": "asd98798as7dhjgkjsdfh",
  "user_id": "fake-user-id",
  "title": "Test query",
  "llm_type": "VertexAI-Chat",
  "query_engine_id": "asd98798as7dhjgkjsdfh",
  "history": [
    {"HumanQuestion": "test input 1"},
    {
      "AIResponse": "test response 1",
      "AIReferences": [
        {
          "query_engine_id": "asd98798as7dhjgkjsdfh",
          "query_engine": "query-engine-test",
          "document_id": "efghxxzzyy1234",
          "chunk_id": "abcdxxzzyy1234"
        }
      ]
    },
    {"HumanQuestion": "test input 2"},
    {
      "AIResponse": "test response 2",
      "AIReferences": [
        {
          "query_engine_id": "asd98798as7dhjgkjsdfh",
          "query_engine": "query-engine-test",
          "document_id": "efghxxzzyy5678",
          "chunk_id": "abcdxxzzyy5678"
        }
      ]
    }
  ]
}

QUERY_ENGINE_EXAMPLE = {
  "id": "asd98798as7dhjgkjsdfh",
  "name": "query-engine-test",
  "llm_type": "VertexAI-Chat",
  "created_by": "fake-user-id",
  "is_public": True,
  "index_id": "projects/83285581741/locations/us-central1/indexes/682347240495461171",
  "index_name": "query_engine_test_MEindex",
  "endpoint": "projects/83285581741/locations/us-central1/indexEndpoints/420294037177840435"
}

QUERY_RESULT_EXAMPLE = {
  "id": "asd98798as7dhjgkjsdfh",
  "query_engine_id": "asd98798as7dhjgkjsdfh",
  "query_engine": "query-engine-test",
  "response": "test response",
  "query_refs": ["abcd1234", "defg5678"],
  "archived_at_timestamp": None,
  "archived_by": None,
  "created_by": "fake-user-id",
  "created_time": "2023-07-04 19:22:50.799741+00:00"
}

CHAT_EXAMPLE = {
  "id": "asd98798as7dhjgkjsdfh",
  "user_id": "fake-user-id",
  "title": "Test chat",
  "llm_type": "VertexAI-Chat",
  "history": [
    {"HumanInput": "test input 1"},
    {"AIOutput": "test response 1"},
    {"HumanInput": "test input 2"},
    {"AIOutput": "test response 2"}
  ],
  "created_time": "2023-05-05 09:22:49.843674+00:00",
  "last_modified_time": "2023-05-05 09:22:49.843674+00:00"
}

USER_EXAMPLE = {
    "id": "fake-user-id",
    "first_name": "Test",
    "last_name": "Tester",
    "user_id": "fake-user-id",
    "auth_id": "fake-user-id",
    "email": "user@gmail.com",
    "role": "Admin",
    "user_type": "learner",
    "status": "active"
}
