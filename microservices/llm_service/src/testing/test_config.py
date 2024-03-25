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

""" Config used for testing in unit tests """
# pylint: disable=line-too-long
import os
from langchain.schema import (Generation, ChatGeneration, LLMResult)
from langchain.schema.messages import AIMessage

API_URL = "http://localhost/llm-service/api/v1"

TESTING_FOLDER_PATH = os.path.join(os.getcwd(), "testing")

FAKE_GENERATE_RESPONSE = "test generation"

FAKE_LANGCHAIN_GENERATION = Generation(text=FAKE_GENERATE_RESPONSE)

FAKE_CHAT_RESPONSE = ChatGeneration(message=AIMessage(
                                    content=FAKE_GENERATE_RESPONSE))

FAKE_GENERATE_RESULT = LLMResult(generations=[[FAKE_LANGCHAIN_GENERATION]])

FAKE_CHAT_RESULT = LLMResult(generations=[[FAKE_CHAT_RESPONSE]])
