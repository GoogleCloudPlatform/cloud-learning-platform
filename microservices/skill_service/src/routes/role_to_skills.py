""" Route module for parsing skills from roles """

import traceback
from fastapi import APIRouter
from schemas.skill_parsing_schema import (SkillParsingByQueryRequestModel,
                                          SkillParsingByQueryResponseModel,
                                          SkillParsingByIdRequestModel,
                                          SkillParsingByIdResponseModel,
                                          AlignAllRequestModel)
from schemas.initaiate_batchjob_schema import BatchJobModel
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  ConflictResponseModel)
from services.skill_parsing.skill_parsing import SkillParser
from services.data_source import get_data_sources
from services.batch_job import initiate_batch_job
from common.models import EmploymentRole
from common.utils.logging_handler import Logger
from common.utils.errors import (ValidationError, ResourceNotFoundException,
                                 ConflictError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, Conflict)
from config import (DATABASE_PREFIX, ERROR_RESPONSES,
                    ROLE_SKILL_MAPPING_JOB_TYPE)

# pylint: disable = broad-exception-raised,consider-using-f-string,invalid-name

router = APIRouter(
    prefix="",
    tags=["Skill Parsing from EmploymentRoles"],
    responses=ERROR_RESPONSES)


@router.post(
    "/role/skill-alignment/query",
    response_model=SkillParsingByQueryResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def search_by_query(req_body: SkillParsingByQueryRequestModel):
  """Given a query this function return skills that are most relevant to
    the given role description

  Args:
    req_body (SkillParsingByQueryRequestModel): Required body for skill parsing

  Raises:
    JSONResponse: 500 Internal Server Error if something fails

  Returns:
    [JSON] (SkillParsingByQueryRequestModel): list of dicts containing
    skills with their name, description and score
  """
  try:
    request_body = req_body.__dict__
    alignment_sources = request_body.get("skill_alignment_sources", ["snhu"])
    ALLOWED_SKILL_SOURCES = get_data_sources("skill")[0]["source"]
    skill_dict = {}
    for alignment_source in alignment_sources:
      if alignment_source not in ALLOWED_SKILL_SOURCES:
        raise Exception("{0} not a valid skill source. Allowed "
                        "\"skill_sources\" are {1}.".format(
                            alignment_source, ALLOWED_SKILL_SOURCES))
      db_index = "skill" + "_" + alignment_source
      skill_parse_obj = SkillParser(source=alignment_source, db_index=db_index)
      skill_list = skill_parse_obj.get_relevant_skills(request_body)
      skill_dict[alignment_source] = skill_list
      response = {
          "name": request_body["name"],
          "description": request_body["description"],
          "aligned_skills": skill_dict
      }
      return {"data": response}
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/role/skill-alignment/id",
    response_model=SkillParsingByIdResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def align_skill_by_ids(req_body: SkillParsingByIdRequestModel):
  """Given firestore role_ids, this function returns skill candiates for
    mapping

  Args:
    req_body (SkillParsingByIdRequestModel): Required body for Skill Parsing

  Raises:
    JSONResponse: 500 Internal Server Error if something fails

  Returns:
    [JSON] (SkillParsingByIdResponseModel): list of top_k skills for each
    type of queried sources per ids
  """

  try:
    request_body = req_body.__dict__
    aligned_skills = {}
    ALLOWED_SKILL_SOURCES = get_data_sources("skill")[0]["source"]
    # Creating empty reponse object
    for role_id in request_body["ids"]:
      aligned_skills[role_id] = {}
      for source in request_body["skill_alignment_sources"]:
        aligned_skills[role_id][source] = []
    for source in request_body["skill_alignment_sources"]:
      if source not in ALLOWED_SKILL_SOURCES:
        raise Exception("{0} not a valid skill source. Allowed "
                        "\"skill_sources\" are {1}.".format(
                            source, ALLOWED_SKILL_SOURCES))
      db_index = "skill" + "_" + source
      skill_parse_obj = SkillParser(source=source, db_index=db_index)
      skills_list = skill_parse_obj.\
        parse_skills_by_role_ids(request_body, update_flag=False)
      Logger.info("skills here")
      Logger.info(skills_list)
      for r_id, skills in skills_list.items():
        aligned_skills[r_id][source].extend(skills)
    aligned_skill_dict = {"aligned_skills": aligned_skills}
    Logger.info(aligned_skill_dict)
    response = {"data": aligned_skill_dict}
    return response
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/role/skill-alignment/batch",
    response_model=BatchJobModel,
    responses={409: {
        "model": ConflictResponseModel
    }})
def batch_align_skill_by_ids(req_body: AlignAllRequestModel):
  """Given an alignment source, this function will
    run a batch job to align all roles with skills

  Args:
    req_body (AlignAllRequestModel): Required body of
      EmploymentRole to Skill Alignment

  Raises:
    JSONResponse: 500 Internal Server Error if something fails

  Returns: (BatchJobModel)
      job_name: name of the batchjob created
      status: status of batchjob
  """
  try:
    request_body = req_body.__dict__
    ALLOWED_SKILL_SOURCES = get_data_sources("skill")[0]["source"]
    ALLOWED_ROLE_SOURCES = get_data_sources("role")[0]["source"]
    if request_body["ids"]:
      for id_ in request_body["ids"]:
        EmploymentRole.find_by_id(id_)
    role_sources = request_body["source_name"]
    if role_sources:
      for source in role_sources:
        if source not in ALLOWED_ROLE_SOURCES:
          raise Exception("{0} not a valid role source. Allowed "
                          "\"role_sources\" are {1}.".format(
                              source, ALLOWED_ROLE_SOURCES))

    if "skill_alignment_sources" not in request_body:
      request_body["skill_alignment_sources"] = ALLOWED_SKILL_SOURCES
    else:
      for source in request_body["skill_alignment_sources"]:
        if source not in ALLOWED_SKILL_SOURCES:
          raise Exception("{0} not a valid skill source. Allowed "
                          "\"skill_sources\" are {1}.".format(
                              source, ALLOWED_SKILL_SOURCES))
    env_vars = {"DATABASE_PREFIX": DATABASE_PREFIX}
    response = initiate_batch_job(request_body, ROLE_SKILL_MAPPING_JOB_TYPE,
                                  env_vars)
    Logger.info(response)
    return response
  except ConflictError as e:
    raise Conflict(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
