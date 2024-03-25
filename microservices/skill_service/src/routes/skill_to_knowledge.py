""" Skill to Knowledge alignment endpoints """
from fastapi import APIRouter
from schemas.skill_to_knowledge_schema import (
    SkillToPassageByIdRequestModel, SkillToPassageByQueryRequestModel,
    SkillToPassageQueryResponseModel, SkillToPassageIdResponseModel)
from services.skill_to_knowledge.skill_to_passage import SkillKnowledgeAlignment
import traceback
from common.utils.logging_handler import Logger
from common.utils.errors import ValidationError
from common.utils.http_exceptions import InternalServerError, BadRequest
from config import ERROR_RESPONSES

router = APIRouter(
    prefix="/skill/knowledge-alignment",
    tags=["Skill to Knowledge"],
    responses=ERROR_RESPONSES)


@router.post("/passage/id",
            response_model=SkillToPassageIdResponseModel,
            include_in_schema=False)
def map_skill_to_passages_by_id(req_body: SkillToPassageByIdRequestModel):
  """Maps the skill uuid with the relevant passages

  Args:
    req_body (RequestModel): Required body of Skill to Knowledge request

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: generated mappings from skill to paragraph,
    error message if the skill to knowledge mapping raises an exception
  """

  try:
    alignment_obj = SkillKnowledgeAlignment()
    mapped_passages = alignment_obj.get_similar_passages(req_body.__dict__)
    return mapped_passages
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post("/passage/query",
            response_model=SkillToPassageQueryResponseModel,
            include_in_schema=False)
def map_skill_to_passages_by_query(req_body: SkillToPassageByQueryRequestModel):
  """Maps the skill name/statement with the relevant passages

  Args:
    req_body (RequestModel): Required body of Skill to Knowledge request

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: generated mappings from skill to paragraph,
    error message if the skill to knowledge mapping raises an exception
  """

  try:
    alignment_obj = SkillKnowledgeAlignment()
    mapped_passages = alignment_obj.get_similar_passages(req_body.__dict__)
    return mapped_passages
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
