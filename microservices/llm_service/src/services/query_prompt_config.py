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

""" Query prompt templates """

from langchain.prompts import PromptTemplate

prompt_template = \
"""Use the following pieces of context to answer the question at the end. """ \
"""If you don't know the answer, just say that you don't know, don't """ \
"""try to make up an answer.

Context:
{context}

Question: {question}
Helpful Answer:"""

QUESTION_PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

