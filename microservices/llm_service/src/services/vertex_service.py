# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Classes for working with language models.

This module is *experimental* and can be changed in the future.
"""

import dataclasses

from typing import Any, Dict 

from google.cloud.aiplatform import base


_LOGGER = base.Logger(__name__)


class _LanguageModel:

    @classmethod
    def from_pretrained(
        cls, model_name: str, **kwargs: Dict[str, Any]
    ) -> "_LanguageModel":

        return cls(
            **kwargs,
        )


@dataclasses.dataclass
class TextGenerationResponse:

    text: str
    _prediction_response: Any

    def __repr__(self):
        return self.text


class TextGenerationModel(_LanguageModel):

    def predict(
        self,
        prompt: str
    ) -> "TextGenerationResponse":

        return TextGenerationResponse("")
        
        
class ChatModel(TextGenerationModel):

    def start_chat(
        self,
    ) -> "ChatSession":

        return ChatSession(
            model=self
        )

class ChatSession:

    def __init__(
        self,
        model: ChatModel,

    ):
        self._model = model

    def send_message(
        self,
        message: str,
    ) -> "TextGenerationResponse":

        response_obj = self._model.predict(
            prompt=message,
        )
        return response_obj
