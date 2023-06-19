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

# pylint: disable = broad-except,unused-import

""" Query endpoints """
import traceback
from typing import Optional
from fastapi import APIRouter
from common.utils.logging_handler import Logger
from common.utils.errors import (ResourceNotFoundException,
                                 ValidationError,
                                 PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from common.models import QueryEngine, UserQuery
from schemas.llm_schema import (LLMQueryModel,
                                LLMQueryEngineModel,
                                LLMQueryEngineResponse,
                                LLMGetQueryEnginesResponse,
                                LLMQueryResponse)

from services.query_service import query_generate, query_engine_build
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES

router = APIRouter(prefix="/query", tags=["LLMs"], responses=ERROR_RESPONSES)


@router.get(
    "",
    name="Get all Query engines",
    response_model=LLMGetQueryEnginesResponse)
def get_query_list():
  """
  Get available Query engines

  Returns:
      LLMGetQueryEnginesResponse
  """
  query_engines = QueryEngine.collection.fetch()
  query_engine_data = [{"name": qe.name, "id": qe.id} for qe in query_engines]
  try:
    return {
      "success": True,
      "message": "Successfully retrieved query engines",
      "data": query_engine_data
    }
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "",
    name="Create a query engine",
    response_model=LLMQueryEngineResponse)
async def query_engine_create(gen_config: LLMQueryEngineModel):
  """
  Start a query engine build job

  Args:
      LLMQueryEngineModel

  Returns:
      LLMQueryEngineResponse
  """
  genconfig_dict = {**gen_config.dict()}

  doc_url = genconfig_dict.get("doc_url")
  if doc_url is None or doc_url == "":
    return BadRequest("Missing or invalid payload parameters")

  query_engine = genconfig_dict.get("query_engine")

  try:
    result = await query_engine_build(doc_url, query_engine)

    return {
        "success": True,
        "message": "Successfully generated text",
        "content": result
    }
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/{queryid}",
    name="Make a query to a query engine",
    response_model=LLMQueryResponse)
async def query(gen_config: LLMQueryModel):
  """
  Send a query to a query engine and return the response

  Args:
      LLMQueryModel

  Returns:
      LLMQueryResponse
  """
  genconfig_dict = {**gen_config.dict()}

  prompt = genconfig_dict.get("prompt")
  if prompt is None or prompt == "":
    return BadRequest("Missing or invalid payload parameters")

  if len(prompt) > PAYLOAD_FILE_SIZE:
    return PayloadTooLargeError(
      f"Prompt must be less than {PAYLOAD_FILE_SIZE}")

  query_engine = genconfig_dict.get("query_engine")

  try:
    query_result, query_references = await query_generate(prompt, query_engine)

    return {
        "success": True,
        "message": "Successfully generated text",
        "data": {
            "query_result": str(query_result),
            "query_references": str(query_references)
        }
    }
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/user/{user_queryid}",
    name="Make a query to a query engine based on a prior user query",
    response_model=LLMQueryEngineResponse)
async def query_continue(user_queryid: str, gen_config: LLMQueryModel):
  """
  Send a query to a query engine with a prior user query as context

  Args:
      LLMUserQueryModel

  Returns:
      LLMQueryResponse
  """
  genconfig_dict = {**gen_config.dict()}

  prompt = genconfig_dict.get("prompt")
  if prompt is None or prompt == "":
    return BadRequest("Missing or invalid payload parameters")

  if len(prompt) > PAYLOAD_FILE_SIZE:
    return PayloadTooLargeError(
      f"Prompt must be less than {PAYLOAD_FILE_SIZE}")

  try:
    user_query = UserQuery.find_by_id(user_queryid)
    query_engine = user_query.query_engine

    query_result, query_references = await query_generate(prompt, query_engine)

    return {
        "success": True,
        "message": "Successfully generated text",
        "data": {
            "query_result": str(query_result),
            "query_references": str(query_references)
        }
    }
  except Exception as e:
    raise InternalServerError(str(e)) from e


