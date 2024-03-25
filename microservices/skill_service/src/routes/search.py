""" Route module for serach at any level in Skill Graph """

import traceback
from fastapi import APIRouter
from services.search.search import SearchSkillGraph
from schemas.search_schema import (SemanticSearchRequestModel,
                                   SemanticSearchResponseModel)
from common.utils.logging_handler import Logger
from common.utils.errors import ValidationError
from common.utils.http_exceptions import InternalServerError, BadRequest
from config import SKILL_GRAPH_LEVELS, ERROR_RESPONSES

router = APIRouter(
    tags=["Search in Skill Graph"],
    responses=ERROR_RESPONSES)


@router.post("/semantic-search", response_model=SemanticSearchResponseModel)
def semantic_search_by_query(req_body: SemanticSearchRequestModel):
  """Given a query this function
    return candidates from every level in skill graph

  Args:
    req_body (SemanticSearchRequestModel): Required body for search

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON] (SemanticSearchResponseModel): list of dicts containing
    maps at each level in skill graph
  """
  try:
    request_body = req_body.__dict__
    query = request_body.get("query", "")
    levels = request_body.get("levels", SKILL_GRAPH_LEVELS)
    top_k = request_body.get("top_k", 5)
    data = {
        "query": query,
    }
    for level in levels:
      Logger.info(f"Searching for Level: {level}")
      level_data = SearchSkillGraph(level).get_search_results(query, top_k)
      data[level] = level_data
    return {"data": data}
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
