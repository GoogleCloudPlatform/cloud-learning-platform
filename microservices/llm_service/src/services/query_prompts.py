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

""" Query Prompt Service """

from typing import List, Optional, Generator, Tuple, Dict
from common.utils.logging_handler import Logger
from common.models import (UserQuery, QueryResult,
                          QueryEngine, QueryDocument,
                          QueryDocumentChunk)
from common.utils.errors import (ResourceNotFoundException,
                                 ValidationError)
from common.utils.http_exceptions import InternalServerError
from vertexai.preview.language_models import (TextEmbeddingModel,
                                              ChatModel)
from langchain.text_splitter import CharacterTextSplitter
import langchain_service

from config import PROJECT_ID

def query_prompt(prompt: str) -> str:
  return ""

def query_with_context(user_query: UserQuery, prompt: str) -> str:
  return ""

def question_prompt(prompt: str, query_context: List[dict]) -> str:
  return ""
