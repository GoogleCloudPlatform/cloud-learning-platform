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
  LLM Service config file
"""
# pylint: disable=unspecified-encoding
import os
from common.utils.logging_handler import Logger
from schemas.error_schema import (UnauthorizedResponseModel,
                                  InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel)
from google.cloud import secretmanager
from langchain.chat_models import ChatOpenAI
from services.vertex_language_models import TextGenerationModel, ChatModel


secrets = secretmanager.SecretManagerServiceClient()

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80
PROJECT_ID = os.environ.get("PROJECT_ID", "cloud-learning-services-dev")
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")

try:
  with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace","r",
            encoding="utf-8",errors="ignore") as \
    ns_file:
    namespace = ns_file.readline()
    JOB_NAMESPACE = namespace
except FileNotFoundError as e:
  JOB_NAMESPACE = "default"
  Logger.info("Namespace File not found, setting job namespace as default")

CONTAINER_NAME = os.getenv("CONTAINER_NAME")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")

API_BASE_URL = os.getenv("API_BASE_URL")

SERVICE_NAME = os.getenv("SERVICE_NAME")

ENABLE_OPENAI_LLM = os.getenv("ENABLE_OPENAI_LLM", "true")
if ENABLE_OPENAI_LLM is None or ENABLE_OPENAI_LLM == "":
  ENABLE_OPENAI_LLM = True
Logger.info(f"ENABLE_OPENAI_LLM = {ENABLE_OPENAI_LLM}")

ENABLE_GOOGLE_LLM = (os.getenv("ENABLE_GOOGLE_LLM", "false").lower() == "true")
if ENABLE_GOOGLE_LLM is None or ENABLE_GOOGLE_LLM == "":
  ENABLE_OPENAI_LLM = False
Logger.info(f"ENABLE_GOOGLE_LLM = {ENABLE_GOOGLE_LLM}")

PAYLOAD_FILE_SIZE = 2097152  #2MB

ERROR_RESPONSES = {
    500: {
        "model": InternalServerErrorResponseModel
    },
    401: {
        "model": UnauthorizedResponseModel
    },
    422: {
        "model": ValidationErrorResponseModel
    }
}

# LLM configuration

OPENAI_API_KEY = secrets.access_secret_version(
    request={
        "name": "projects/" + PROJECT_ID +
                "/secrets/openai-api-key/versions/latest"
    }).payload.data.decode("utf-8")

GOOGLE_API_KEY = secrets.access_secret_version(
    request={
        "name": "projects/" + PROJECT_ID +
                "/secrets/google-api-access-token/versions/latest"
    }).payload.data.decode("utf-8")

OPENAI_LLM_TYPE_GPT3_5 = "OpenAI-GPT3.5"
OPENAI_LLM_TYPE_GPT4 = "OpenAI-GPT4"
VERTEX_LLM_TYPE_BISON_001 = "VertexAI-Bison-001"
VERTEX_LLM_TYPE_BISON_ALPHA = "VertexAI-Bison-alpha"

LLM_TYPES = []
OPENAI_LLM_TYPES = [OPENAI_LLM_TYPE_GPT3_5, OPENAI_LLM_TYPE_GPT4] 
GOOGLE_LLM_TYPES = [VERTEX_LLM_TYPE_BISON_001, VERTEX_LLM_TYPE_BISON_ALPHA]

if ENABLE_OPENAI_LLM:
  #LLM_TYPES = LLM_TYPES.extend(OPENAI_LLM_TYPES)
  LLM_TYPES = OPENAI_LLM_TYPES

if ENABLE_GOOGLE_LLM:
  LLM_TYPES = LLM_TYPES.extend(GOOGLE_LLM_TYPES)

Logger.info(f"LLM types loaded {LLM_TYPES}")

LANGCHAIN_LLM = {}
if ENABLE_OPENAI_LLM:
  LANGCHAIN_LLM = {
    OPENAI_LLM_TYPE_GPT3_5: ChatOpenAI(openai_api_key=OPENAI_API_KEY,
                                model_name="gpt-3.5-turbo"),
    OPENAI_LLM_TYPE_GPT4: ChatOpenAI(openai_api_key=OPENAI_API_KEY,
                                model_name="gpt-4")                              
  }

GOOGLE_LLM = {}
if ENABLE_GOOGLE_LLM:
  GOOGLE_LLM = {
    VERTEX_LLM_TYPE_BISON_001: 
      TextGenerationModel.from_pretrained("text-bison-001"),
    VERTEX_LLM_TYPE_BISON_ALPHA:
      ChatModel.from_pretrained("text-bison-alpha")
  }
