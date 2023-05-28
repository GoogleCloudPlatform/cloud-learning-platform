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
  "primer":  "",
}

CHAT_EXAMPLE = {
  "id": "asd98798as7dhjgkjsdfh",
  "user_id": "dhjgkjsdfhasd98798as7",
  "title": "Test chat",
  "llm_type": "VertexAI-Text-alpha",
  "history": [
    "test input 1",
    "test response 1",
    "test input 2",
    "test response 2"
  ],
  "created_time": "2023-05-05 09:22:49.843674+00:00",
  "last_modified_time": "2023-05-05 09:22:49.843674+00:00"
}
