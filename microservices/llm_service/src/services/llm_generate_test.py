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
  Unit tests for Langchain Service endpoints
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import,unused-variable,ungrouped-imports
import os
import pytest
from unittest import mock
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.models import UserChat

FAKE_GENERATE_PARAMS = {
    "llm_type": "LLM Test",
    "prompt": "test prompt"
  }

FAKE_GENERATE_RESPONSE = "test generation"

with mock.patch("services.llm_generate.langchain_llm_generate",
    return_value = FAKE_GENERATE_RESPONSE):
  with mock.patch("services.llm_generate.google_llm_predict",
      return_value = FAKE_GENERATE_RESPONSE):
    from services.llm_generate import llm_generate

with mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect=mock.MagicMock()) as mok:
  with mock.patch("langchain.chat_models.ChatOpenAI"):
    with mock.patch("langchain.llms.Cohere"):
      from config import LLM_TYPES

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"
os.environ["OPENAI_API_KEY"] = "fake-key"
os.environ["COHERE_API_KEY"] = "fake-key"

def test_llm_generate(clean_firestore):
  pass
