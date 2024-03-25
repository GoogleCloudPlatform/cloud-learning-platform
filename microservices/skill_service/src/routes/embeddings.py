"""Endpoints for creating embeddings"""

# pylint: disable = broad-except,invalid-name

import traceback
from typing import Dict
from fastapi import APIRouter
from schemas.initaiate_batchjob_schema import BatchJobModel
from schemas.create_embeddings_schema import PopulateEmbdRequestModel
from schemas.error_schema import ConflictResponseModel
from services.batch_job import initiate_batch_job
from services.data_source import get_data_sources
from common.utils.logging_handler import Logger
from common.models import KnowledgeServiceLearningContent
from common.utils.errors import ValidationError, ConflictError
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          Conflict)
from config import (POPULATE_SKILL_EMBEDDING_JOB_TYPE, EMBEDDING_ENDPOINT_ID,
                    MATCHING_ENGINE_BUCKET_NAME,
                    POPULATE_KNOWLEDGE_EMBEDDING_JOB_TYPE,
                    CREATE_KG_EMBEDDING_JOB_TYPE, SKILL_GRAPH_LEVELS,
                    KNOWLEDGE_GRAPH_LEVELS, ERROR_RESPONSES)

router = APIRouter(
    prefix="",
    tags=["Create embeddings"],
    responses=ERROR_RESPONSES)


@router.post(
    "/embeddings",
    response_model=Dict[str, BatchJobModel],
    responses={409: {
        "model": ConflictResponseModel
    }})
def create_embeddings(req_body: PopulateEmbdRequestModel):
  """
  Function to populate database with the embeddings for skills, knowledge graph,
  and learning_resource_ids

  Args:
    req_body (PopulateEmbeddingsRequestModel): Required body for populating
    embeddings

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns: dict(str, BatchJobModel)
    str: term for which the batchjob will create embeddings. Eg. "skill_emsi",
          "concept", "category" etc.
    BatchJobModel:
      job_name: name of the batchjob created
      status: status of batchjob
  """
  try:
    response_dict = {}
    request_body = req_body.__dict__
    SKILL_SOURCES = get_data_sources("skill")[0]["source"]
    # Skill Graph embedding creation
    skill_levels = request_body["skill_graph"]["level"]
    skill_source_names = request_body["skill_graph"]["source"]
    if skill_levels == ["*"]:
      skill_levels = SKILL_GRAPH_LEVELS
    if skill_source_names == ["*"]:
      skill_source_names = SKILL_SOURCES
    for level in skill_levels:
      if level not in SKILL_GRAPH_LEVELS:
        raise ValidationError(
            f"Undefined level \"{level}\" in skill level."
            f" Allowed skill levels are: {SKILL_GRAPH_LEVELS}")
    for source in skill_source_names:
      if source not in SKILL_SOURCES:
        raise ValidationError(f"Undefined source \"{source}\" in skill source."
                               f" Allowed skill sources are: {SKILL_SOURCES}")
    for level in skill_levels:
      if skill_source_names:
        for skill_source in skill_source_names:
          request = {"level": level, "source_name": skill_source}
          response_dict[level + "_" + skill_source] = initiate_batch_job(
              request, POPULATE_SKILL_EMBEDDING_JOB_TYPE, {
                  "EMBEDDING_ENDPOINT_ID": EMBEDDING_ENDPOINT_ID,
                  "MATCHING_ENGINE_BUCKET_NAME": MATCHING_ENGINE_BUCKET_NAME
              })
      else:
        request = {"level": level, "source_name": skill_source_names}
        response_dict[level] = initiate_batch_job(
            request, POPULATE_SKILL_EMBEDDING_JOB_TYPE, {
                "EMBEDDING_ENDPOINT_ID": EMBEDDING_ENDPOINT_ID,
                "MATCHING_ENGINE_BUCKET_NAME": MATCHING_ENGINE_BUCKET_NAME
            })

    # Knowledge Graph embedding creation
    knowledge_levels = request_body["knowledge_graph"]["level"]
    if knowledge_levels == ["*"]:
      knowledge_levels = KNOWLEDGE_GRAPH_LEVELS
    for level in knowledge_levels:
      if level not in KNOWLEDGE_GRAPH_LEVELS:
        raise ValidationError(
            f"Undefined level \"{level}\" "
            f"in knowledge_graph level. "
            f"Allowed knowledge_graph levels are: {KNOWLEDGE_GRAPH_LEVELS}")
    for level in knowledge_levels:
      request = {"level": level}
      response_dict[level] = initiate_batch_job(
          request, CREATE_KG_EMBEDDING_JOB_TYPE, {
              "EMBEDDING_ENDPOINT_ID": EMBEDDING_ENDPOINT_ID,
              "MATCHING_ENGINE_BUCKET_NAME": MATCHING_ENGINE_BUCKET_NAME
          })

    # Learning Resource embedding creation
    learning_resource_ids = request_body["learning_resource"]["ids"]
    if learning_resource_ids == ["*"]:
      raise ValidationError("\"*\" is not allowed in learning_resource_ids.")
    for learning_resource_id in learning_resource_ids:
      KnowledgeServiceLearningContent.find_by_id(learning_resource_id)
    if learning_resource_ids:
      request = {"learning_resource_ids": learning_resource_ids}
      response_dict["learning_resource_ids"] = initiate_batch_job(
          request, POPULATE_KNOWLEDGE_EMBEDDING_JOB_TYPE, {
              "EMBEDDING_ENDPOINT_ID": EMBEDDING_ENDPOINT_ID,
              "MATCHING_ENGINE_BUCKET_NAME": MATCHING_ENGINE_BUCKET_NAME
          })
    return response_dict
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ConflictError as e:
    raise Conflict(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
