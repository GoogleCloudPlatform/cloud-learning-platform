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
from fastapi import APIRouter, Depends
from common.schemas.batch_job_schemas import BatchJobModel
from common.utils.auth_service import validate_token
from common.utils.batch_jobs import initiate_batch_job
from common.utils.config import JOB_TYPE_QUERY_ENGINE_BUILD
from common.utils.logging_handler import Logger
from common.utils.errors import (ResourceNotFoundException,
                                 ValidationError,
                                 PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from common.models import QueryEngine, User, UserQuery
from schemas.llm_schema import (LLMQueryModel,
                                LLMUserAllQueriesResponse,
                                LLMUserQueryResponse,
                                UserQueryUpdateModel,
                                LLMQueryEngineModel,
                                LLMQueryEngineResponse,
                                LLMGetQueryEnginesResponse,
                                LLMQueryResponse)

from services.query_service import query_generate, query_engine_build
from config import (PROJECT_ID, DATABASE_PREFIX, PAYLOAD_FILE_SIZE,
                    ERROR_RESPONSES, DEFAULT_QUERY_EMBEDDING_MODEL,
                    ENABLE_OPENAI_LLM, ENABLE_COHERE_LLM,
                    DEFAULT_QUERY_CHAT_MODEL)

router = APIRouter(prefix="/query", tags=["LLMs"], responses=ERROR_RESPONSES)


@router.get(
    "",
    name="Get all Query engines",
    response_model=LLMGetQueryEnginesResponse)
def get_engine_list():
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
      "message": "Successfully retrieved query engine types",
      "data": query_engine_data
    }
  except Exception as e:
    raise InternalServerError(str(e)) from e

@router.get(
    "/user/{user_id}",
    name="Get all Queries for a user",
    response_model=LLMUserAllQueriesResponse)
def get_query_list(user_id: str, skip: int = 0, limit: int = 20):
  """
  Get user queries for authenticated user.  Query data does not include
  history to slim payload.  To retrieve query history use the
  get single query endpoint.

  Args:
    skip: `int`
      Number of tools to be skipped <br/>
    limit: `int`
      Size of tools array to be returned <br/>

  Returns:
      LLMUserAllQueriesResponse
  """
  try:
    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")

    if limit < 1:
      raise ValidationError("Invalid value passed to \"limit\" query parameter")

    # TODO: RBAC check. This call allows the authenticated user to access
    # other user queries
    user = User.collection.filter("user_id", "==", user_id).get()
    if user is None:
      raise ResourceNotFoundException(f"User {user_id} not found ")

    user_queries = UserQuery.find_by_user(user.user_id, skip=skip, limit=limit)

    query_list = []
    for i in user_queries:
      query_data = i.get_fields(reformat_datetime=True)
      query_data["id"] = i.id
      # don't inculde chat history to slim return payload
      del query_data["history"]
      query_list.append(query_data)

    return {
      "success": True,
      "message": f"Successfully retrieved user queries for user {user.user_id}",
      "data": query_list
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e

@router.get(
    "/{query_id}",
    name="Get user query",
    response_model=LLMUserQueryResponse)
def get_chat(query_id: str):
  """
  Get a specific user query by id

  Returns:
      LLMUserQueryResponse
  """
  try:
    user_query = UserQuery.find_by_id(query_id)
    query_data = user_query.get_fields(reformat_datetime=True)
    query_data["id"] = user_query.id

    return {
      "success": True,
      "message": f"Successfully retrieved user query {query_id}",
      "data": query_data
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
  "/{query_id}",
  name="Update user query"
)
def update_query(query_id: str, input_query: UserQueryUpdateModel):
  """Update a user query

  Args:
    input_query (UserQueryUpdateModel): fields in body of query to update.
      The only field that can be updated is the title.

  Raises:
    ResourceNotFoundException: If the UserQuery does not exist
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: {'success': 'True'} if the user query is updated,
    NotFoundErrorResponseModel if the user query not found,
    InternalServerErrorResponseModel if the update raises an exception
  """
  existing_query = UserQuery.find_by_id(query_id)
  if existing_query is None:
    raise ResourceNotFoundException(f"Query {query_id} not found")

  try:
    input_query_dict = {**input_query.dict()}

    for key in input_query_dict:
      if input_query_dict.get(key) is not None:
        setattr(existing_query, key, input_query_dict.get(key))
    existing_query.update()

    return {
      "success": True,
      "message": f"Successfully updated user query {query_id}",
    }
  except ResourceNotFoundException as re:
    raise ResourceNotFound(str(re)) from re
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.post(
    "/engine",
    name="Create a query engine",
    response_model=BatchJobModel)
async def query_engine_create(gen_config: LLMQueryEngineModel,
                              user_data: dict = Depends(validate_token)):
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
    return BadRequest("Missing or invalid payload parameters: doc_url")

  query_engine = genconfig_dict.get("query_engine")
  if query_engine is None or query_engine == "":
    return BadRequest("Missing or invalid payload parameters: query_engine")

  is_public = genconfig_dict.get("is_public", True)

  user_id = user_data.get("user_id")

  try:
    data = {
      "doc_url": doc_url,
      "query_engine": query_engine,
      "user_id": user_id,
      "is_public": is_public,
      "llm_type": genconfig_dict.get("llm_type", DEFAULT_QUERY_EMBEDDING_MODEL)
    }
    env_vars = {
      "DATABASE_PREFIX": DATABASE_PREFIX,
      "PROJECT_ID": PROJECT_ID,
      "ENABLE_OPENAI_LLM": str(ENABLE_OPENAI_LLM),
      "ENABLE_COHERE_LLM": str(ENABLE_COHERE_LLM)
    }
    response = initiate_batch_job(data, JOB_TYPE_QUERY_ENGINE_BUILD, env_vars)
    Logger.info(response)
    return response
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/engine/{query_engine_id}",
    name="Make a query to a query engine",
    response_model=LLMQueryResponse)
async def query(query_engine_id: str,
                gen_config: LLMQueryModel,
                user_data: dict = Depends(validate_token)):
  """
  Send a query to a query engine and return the response

  Args:
      LLMQueryModel

  Returns:
      LLMQueryResponse
  """
  q_engine = QueryEngine.find_by_id(query_engine_id)
  if q_engine is None:
    raise ResourceNotFoundException(f"Engine {query_engine_id} not found")

  genconfig_dict = {**gen_config.dict()}

  prompt = genconfig_dict.get("prompt")
  if prompt is None or prompt == "":
    return BadRequest("Missing or invalid payload parameters")

  if len(prompt) > PAYLOAD_FILE_SIZE:
    return PayloadTooLargeError(
      f"Prompt must be less than {PAYLOAD_FILE_SIZE}")

  llm_type = genconfig_dict.get("llm_type")
  if llm_type is None or llm_type == "":
    llm_type = DEFAULT_QUERY_CHAT_MODEL

  user = User.find_by_email(user_data.get("email"))

  try:
    query_result, query_references = await query_generate(user.id, prompt,
                                                          q_engine, llm_type)
    return {
        "success": True,
        "message": "Successfully generated text",
        "data": {
            "query_result": query_result,
            "query_references": query_references
        }
    }
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/{user_query_id}",
    name="Make a query to a query engine based on a prior user query",
    response_model=LLMQueryResponse)
async def query_continue(user_query_id: str, gen_config: LLMQueryModel):
  """
  Send a query to a query engine with a prior user query as context

  Args:
      user_query_id: id of previous user query
      LLMQueryModel

  Returns:
      LLMQueryResponse
  """
  user_query = UserQuery.find_by_id(user_query_id)
  if user_query is None:
    raise ResourceNotFoundException(f"Query {user_query_id} not found")

  genconfig_dict = {**gen_config.dict()}

  prompt = genconfig_dict.get("prompt")
  if prompt is None or prompt == "":
    return BadRequest("Missing or invalid payload parameters")

  if len(prompt) > PAYLOAD_FILE_SIZE:
    return PayloadTooLargeError(
      f"Prompt must be less than {PAYLOAD_FILE_SIZE}")

  llm_type = genconfig_dict.get("llm_type")
  if llm_type is None or llm_type == "":
    llm_type = DEFAULT_QUERY_CHAT_MODEL

  try:
    q_engine = QueryEngine.find_by_id(user_query.query_engine_id)

    query_result, query_references = await query_generate(user_query.user_id,
                                                          prompt,
                                                          q_engine,
                                                          llm_type,
                                                          user_query)
    return {
        "success": True,
        "message": "Successfully generated text",
        "data": {
            "query_result": query_result,
            "query_references": query_references
        }
    }
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
