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
# pylint: disable=unspecified-encoding,line-too-long
import os
from common.utils.logging_handler import Logger
from schemas.error_schema import (UnauthorizedResponseModel,
                                  InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel)
from google.cloud import secretmanager
from langchain.chat_models import ChatOpenAI
from langchain.llms import Cohere

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

PAYLOAD_FILE_SIZE = 1024

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

def get_environ_flag(env_flag_str, default=True):
  default_str = str(default)
  evn_val = os.getenv(env_flag_str, default_str)
  if evn_val is None or evn_val == "":
    evn_val = default_str
  evn_flag = evn_val.lower() == "true"
  Logger.info(f"{env_flag_str} = {evn_flag}")
  return evn_flag

ENABLE_OPENAI_LLM = get_environ_flag("ENABLE_OPENAI_LLM", True)

ENABLE_GOOGLE_LLM = get_environ_flag("ENABLE_GOOGLE_LLM", True)

ENABLE_COHERE_LLM = get_environ_flag("ENABLE_COHERE_LLM", True)


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
  OPENAI_API_KEY = secrets.access_secret_version(
      request={
          "name": "projects/" + PROJECT_ID +
                  "/secrets/openai-api-key/versions/latest"
      }).payload.data.decode("utf-8")
  OPENAI_API_KEY = OPENAI_API_KEY.strip()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if COHERE_API_KEY is None:
  COHERE_API_KEY = secrets.access_secret_version(
      request={
          "name": "projects/" + PROJECT_ID +
                  "/secrets/cohere-api-key/versions/latest"
      }).payload.data.decode("utf-8")
  COHERE_API_KEY = COHERE_API_KEY.strip()

def load_google_access_token():
  google_access_token = secrets.access_secret_version(
      request={
          "name": "projects/" + PROJECT_ID +
                  "/secrets/google-api-access-token/versions/latest"
      }).payload.data.decode("utf-8")
  google_access_token = google_access_token.strip()
  return google_access_token

OPENAI_LLM_TYPE_GPT3_5 = "OpenAI-GPT3.5"
OPENAI_LLM_TYPE_GPT4 = "OpenAI-GPT4"
COHERE_LLM_TYPE = "Cohere"
VERTEX_LLM_TYPE_BISON_TEXT = "VertexAI-Text"
VERTEX_LLM_TYPE_BISON_CHAT = "VertexAI-Chat"

LLM_TYPES = []
#OPENAI_LLM_TYPES = [OPENAI_LLM_TYPE_GPT3_5, OPENAI_LLM_TYPE_GPT4]
OPENAI_LLM_TYPES = [OPENAI_LLM_TYPE_GPT3_5]
COHERE_LLM_TYPES = [COHERE_LLM_TYPE]
GOOGLE_LLM_TYPES = [VERTEX_LLM_TYPE_BISON_TEXT, VERTEX_LLM_TYPE_BISON_CHAT]

# these LLMs are trained as chat models
CHAT_LLM_TYPES = [OPENAI_LLM_TYPE_GPT3_5, VERTEX_LLM_TYPE_BISON_CHAT]

if ENABLE_OPENAI_LLM:
  LLM_TYPES.extend(OPENAI_LLM_TYPES)

if ENABLE_COHERE_LLM:
  LLM_TYPES.extend(COHERE_LLM_TYPES)

if ENABLE_GOOGLE_LLM:
  LLM_TYPES.extend(GOOGLE_LLM_TYPES)

LANGCHAIN_LLM = {}
if ENABLE_OPENAI_LLM:
  LANGCHAIN_LLM.update({
    OPENAI_LLM_TYPE_GPT3_5: ChatOpenAI(openai_api_key=OPENAI_API_KEY,
                                model_name="gpt-3.5-turbo"),
    OPENAI_LLM_TYPE_GPT4: ChatOpenAI(openai_api_key=OPENAI_API_KEY,
                                model_name="gpt-4"),
    COHERE_LLM_TYPE: Cohere(cohere_api_key=COHERE_API_KEY, max_tokens=1024)
  })

GOOGLE_LLM = {}
if ENABLE_GOOGLE_LLM:
  GOOGLE_LLM = {
    VERTEX_LLM_TYPE_BISON_TEXT: "text-bison@001",
    VERTEX_LLM_TYPE_BISON_CHAT: "chat-bison@001"
  }

Logger.info(f"LLM types loaded {LLM_TYPES}")
