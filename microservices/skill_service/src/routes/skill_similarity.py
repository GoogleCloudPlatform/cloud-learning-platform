""" Route module for skill similarity """

import traceback
from fastapi import APIRouter
from schemas.skill_similarity_schema import (SimilarityScoreRequestModel,
                                             SimilarityScoreResponseModel)
from schemas.error_schema import NotFoundErrorResponseModel
from services.skill_similarity import SkillSimilarity
from services.data_source import get_data_sources
from common.utils.logging_handler import Logger
from common.utils.errors import ValidationError, ResourceNotFoundException
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound)
from config import ERROR_RESPONSES

# pylint: disable = broad-except,consider-using-f-string,invalid-name

router = APIRouter(
    prefix="/skill/similarity",
    tags=["Skill Similarity"],
    responses=ERROR_RESPONSES)


@router.post(
    "",
    response_model=SimilarityScoreResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_similarity_score(req_body: SimilarityScoreRequestModel):
  """Given 2 firestore skill_ids, this function returns
    the similarity score between them

  Args:
    req_body (SimilarityScoreRequestModel): Required body of
    Skill Similarity

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON] (SimilarityScoreResponseModel): similarity score for
    the two skills
  """

  try:
    request_body = req_body.__dict__
    skill_id_1 = request_body["id_1"]
    skill_id_2 = request_body["id_2"]
    data_source = request_body["data_source"]
    ALLOWED_SKILL_SOURCES = get_data_sources("skill")[0]["source"]
    ALLOWED_SKILL_SOURCES_WO_E2E = [
      source for source in ALLOWED_SKILL_SOURCES if "e2e" not in source
    ]
    if data_source not in ALLOWED_SKILL_SOURCES:
      raise ValidationError("{0} not a valid skill source. Allowed "
                      "\"skill_sources\" are {1}.".format(
                          data_source, ALLOWED_SKILL_SOURCES_WO_E2E))
    # Create object and get similarity score
    similarity_obj = SkillSimilarity()
    skill_text_1, skill_text_2 = similarity_obj.get_skill_data(
        skill_id_1, skill_id_2, data_source)
    similarity_score = similarity_obj.get_skill_similarity(
        skill_text_1, skill_text_2)
    score = {"similarity_score": similarity_score}
    return {"data": score}
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
