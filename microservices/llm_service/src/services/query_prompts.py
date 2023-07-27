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

""" Query prompt generator methods """

from typing import List

from services.query_prompt_config import QUESTION_PROMPT

def question_prompt(prompt: str, query_context: List[dict]) -> str:
  """ Create question prompt with context for LLM """
  context_list = [ref["document_text"] for ref in query_context]
  text_context = "\n\n".join(context_list)
  question = QUESTION_PROMPT.format(question=prompt, context=text_context)
  return question
