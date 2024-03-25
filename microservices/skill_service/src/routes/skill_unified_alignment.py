""" Route module for unified skill alignment """
#pylint: disable=broad-except
import traceback
from fastapi import APIRouter
from schemas.skill_unified_alignment_schema import (AlignByIdsRequestModel,
                                                    AlignByIdsResponseModel,
                                                    AlignByQueryRequestModel,
                                                    AlignByQueryResponseModel,
                                                    UnifiedBatchRequestModel)
from schemas.initaiate_batchjob_schema import BatchJobModel
from schemas.error_schema import NotFoundErrorResponseModel
from services.skill_unified_alignment.skill_unified_alignment import (
    SkillUnifiedAlignment)
from services.batch_job import initiate_batch_job
from services.data_source import get_data_sources
from config import (UNIFIED_ALIGNMENT_JOB_TYPE, DATABASE_PREFIX,
                    ERROR_RESPONSES, EMBEDDING_ENDPOINT_ID)
from common.utils.logging_handler import Logger
from common.models import Skill, KnowledgeServiceLearningContent
from common.utils.errors import ValidationError, ResourceNotFoundException
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          APINotImplemented,
                                          ResourceNotFound)

# pylint: disable=broad-exception-raised,consider-using-f-string,invalid-name

ERROR_RESPONSES[404] = {"model": NotFoundErrorResponseModel}

router = APIRouter(
    prefix="/unified-alignment",
    tags=["Skill Unified Alignment"],
    responses=ERROR_RESPONSES)


@router.post("/id", response_model=AlignByIdsResponseModel)
def align_by_id(req_body: AlignByIdsRequestModel):
  """
  Given the Firestore (Skill/Job/Knowledge/Curriculum) id(s), this method
  returns all the candidates to be mapped to the id(s).
  Args:
    req_body (AlignByIdsRequestModel): Required body of Unified Alignment.

  Raises:
    HTTPException: 500 Internal Server Error if something fails.

  Returns:
    [JSON] (AlignByIdsResponseModel): Mapping of given ids with Knowledge,
    Skill, Job, Curriculum items.
  """
  try:
    request_body = req_body.__dict__
    input_type = request_body["input_type"]
    alignment_sources = request_body["output_alignment_sources"]
    if input_type == "skill":
      for skill_id in request_body["ids"]:
        Skill.find_by_uuid(skill_id)
      allowed_output_alignment_keys = {"skill_sources", "learning_resource_ids"}
      if alignment_sources.keys() < allowed_output_alignment_keys:
        raise ValidationError("{0} missing in output_alignment_sources".\
        format(allowed_output_alignment_keys-alignment_sources.keys()))
      for key in alignment_sources.keys():
        if key not in allowed_output_alignment_keys:
          raise ValidationError("Invalid key {0} in output_alignment_sources. "
          "Only {1} are allowed for input_type skill.".\
          format(key, allowed_output_alignment_keys))
      if all(value == [] for value in alignment_sources.values()):
        raise ValidationError("No source is provided for alignment.")
      for key, value in alignment_sources.items():
        if len(value) == 1 and value[0] == "*":
          raise ValidationError(
              "\"*\" is not allowed as value in"
              " \"output_alignment_sources\". Please use specific "
              "source(s) as value.")
        if key == "skill_sources":
          data_sources = get_data_sources("skill")[0]
          SKILL_SOURCES = data_sources["source"]
          MATCHING_ENGINE_INDEX_IDS = data_sources["matching_engine_index_id"]
          for source in value:
            if source not in SKILL_SOURCES:
              raise ValidationError("{0} not a valid skill source. Allowed "
                                     "\"skill_sources\" are {1}.".format(
                                         source, SKILL_SOURCES))
            elif source not in MATCHING_ENGINE_INDEX_IDS:
              raise Exception("Index is not created for {0}. Please use {1} "
                              "to create index.".format(
                                  source,
                                  "skill-service/api/v1/skill/embeddings"))
        elif key == "learning_resource_ids":
          if len(value) > 1:
            raise ValidationError\
              ("Only 1 learning_resource_id is allowed currently")
          for source in value:
            KnowledgeServiceLearningContent.find_by_id(source)
      skill_alignment_sources = alignment_sources.get("skill_sources")
      learning_resource_ids = alignment_sources.get("learning_resource_ids")
      request_body["skill_alignment_sources"] = skill_alignment_sources
      request_body["learning_resource_ids"] = learning_resource_ids
    else:
      raise NotImplementedError("Only \"skill\" is allowed as \"input_type\"")
    alignment_obj = SkillUnifiedAlignment()
    response = alignment_obj.align_by_id(request_body)
    return response
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except NotImplementedError as e:
    raise APINotImplemented(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post("/query", response_model=AlignByQueryResponseModel)
def align_by_query(req_body: AlignByQueryRequestModel):
  """
  Given a query, this method returns all the candidates
  to be mapped to that query. Query can be a Skill/Knowledge/Job/Curriculum.
  Args:
    req_body (AlignByQueryRequestModel): Required body of Unified Alignment.

  Raises:
    HTTPException: 500 Internal Server Error if something fails.

  Returns:
    [JSON] (AlignByQueryResponseModel): Mapping of given query with
    Knowledge, Skill, Job, Curriculum.
  """
  try:
    request_body = req_body.__dict__
    input_type = request_body["input_type"]
    alignment_sources = request_body["output_alignment_sources"]
    if not request_body["name"] and not request_body["description"]:
      raise ValidationError\
        ("Both \"name\" and \"description\" cannot be empty.")
    if input_type == "skill":
      allowed_output_alignment_keys = {"skill_sources", "learning_resource_ids"}
      if alignment_sources.keys() < allowed_output_alignment_keys:
        raise ValidationError("{0} missing in output_alignment_sources".\
        format(allowed_output_alignment_keys-alignment_sources.keys()))
      for key in alignment_sources.keys():
        if key not in allowed_output_alignment_keys:
          raise ValidationError("Invalid key {0} in output_alignment_sources. "
          "Only {1} are allowed for input_type skill.".\
          format(key, allowed_output_alignment_keys))
      if all(value == [] for value in alignment_sources.values()):
        raise ValidationError("No source is provided for alignment.")
      for key, value in alignment_sources.items():
        if len(value) == 1 and value[0] == "*":
          raise ValidationError(
              "\"*\" is not allowed as value in"
              " \"output_alignment_sources\". Please use specific "
              "source(s) as value.")
        if key == "skill_sources":
          data_sources = get_data_sources("skill")[0]
          SKILL_SOURCES = data_sources["source"]
          MATCHING_ENGINE_INDEX_IDS = data_sources["matching_engine_index_id"]
          for source in value:
            if source not in SKILL_SOURCES:
              raise ValidationError("{0} not a valid skill source. Allowed "
                                     "\"skill_sources\" are {1}.".format(
                                         source, SKILL_SOURCES))
            elif source not in MATCHING_ENGINE_INDEX_IDS:
              raise Exception("Index is not created for {0}. Please use {1} "
                              "to create index.".format(
                                  source,
                                  "skill-service/api/v1/skill/embeddings"))
        elif key == "learning_resource_ids":
          if len(value) > 1:
            raise ValidationError\
              ("Only 1 learning_resource_id is allowed currently")
          for source in value:
            KnowledgeServiceLearningContent.find_by_id(source)
      skill_alignment_sources = alignment_sources.get("skill_sources")
      learning_resource_ids = alignment_sources.get("learning_resource_ids")
      request_body["skill_alignment_sources"] = skill_alignment_sources
      request_body["learning_resource_ids"] = learning_resource_ids
    else:
      raise NotImplementedError("Only \"skill\" is allowed as \"input_type\"")
    alignment_obj = SkillUnifiedAlignment()
    response = alignment_obj.align_by_query(request_body)
    return response
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except NotImplementedError as e:
    raise APINotImplemented(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post("/batch", response_model=BatchJobModel)
def align_by_ids_batch(req_body: UnifiedBatchRequestModel):
  """
  Given the Firestore Skill_ids, this method updates all the alignments
  for the given skill(s) in the Firestore.
  Args:
    req_body (RequestModel): Required body of Skill Alignment.

  Raises:
    HTTPException: 500 Internal Server Error if something fails.

  Returns: (BatchJobModel)
      job_name: name of the batchjob created
      status: status of batchjob
  """
  try:
    request_body = req_body.__dict__
    input_type = request_body["input_type"]
    input_ids = request_body.get("ids", [])
    source_name = request_body.get("source_name", [])
    alignment_sources = request_body["output_alignment_sources"]
    if (not input_ids and not source_name) or (input_ids and source_name):
      raise Exception("Either ids or source_name must be provided")
    response = {}
    if input_type == "skill":
      # skill to skill
      # skill to knowledge
      skill_sources = get_data_sources("skill")[0]
      SKILL_SOURCES = skill_sources["source"]
      if source_name:
        for source in source_name:
          if source not in SKILL_SOURCES:
            raise ValidationError\
              ("{0} is not a valid skill source. Allowed sources "
            "are {1}".format(source, SKILL_SOURCES))
      elif input_ids:
        for skill_id in request_body["ids"]:
          Skill.find_by_uuid(skill_id)
      allowed_output_alignment_keys = {"skill_sources", "learning_resource_ids"}
      if alignment_sources.keys() < allowed_output_alignment_keys:
        raise ValidationError("{0} missing in output_alignment_sources".\
        format(allowed_output_alignment_keys-alignment_sources.keys()))
      for key in alignment_sources.keys():
        if key not in allowed_output_alignment_keys:
          raise ValidationError("Invalid key {0} in output_alignment_sources. "
          "Only {1} are allowed for input_type skill.".\
          format(key, allowed_output_alignment_keys))
      if all(value == [] for value in alignment_sources.values()):
        raise ValidationError("No source is provided for alignment.")
      for key, value in alignment_sources.items():
        if len(value) == 1 and value[0] == "*":
          continue
        if key == "skill_sources":
          skill_sources = get_data_sources("skill")[0]
          SKILL_SOURCES = skill_sources["source"]
          MATCHING_ENGINE_INDEX_IDS = skill_sources["matching_engine_index_id"]
          for source in value:
            if source not in SKILL_SOURCES:
              raise ValidationError("{0} not a valid skill source. Allowed "
                                     "\"skill_sources\" are {1}.".format(
                                         source, SKILL_SOURCES))
            elif source not in MATCHING_ENGINE_INDEX_IDS:
              raise Exception("Index is not created for {0}. Please use {1} "
                              "to create index.".format(
                                  source,
                                  "skill-service/api/v1/skill/embeddings"))
        elif key == "learning_resource_ids":
          for source in value:
            KnowledgeServiceLearningContent.find_by_id(source)
    else:
      raise NotImplementedError("Only \"skill\" is allowed as \"input_type\"")
    env_vars = {"DATABASE_PREFIX": DATABASE_PREFIX,
                "EMBEDDING_ENDPOINT_ID": EMBEDDING_ENDPOINT_ID}
    response = initiate_batch_job(request_body, UNIFIED_ALIGNMENT_JOB_TYPE,
                                  env_vars)
    return response
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except NotImplementedError as e:
    raise APINotImplemented(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
