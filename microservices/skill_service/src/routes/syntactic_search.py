""" Route module for search at any level in Skill Graph """

from fastapi import APIRouter
from schemas.search_schema import (KeywordSearchRequestModel,
                                   KeywordSearchResponseModel)
from schemas.error_schema import NotFoundErrorResponseModel
from services.search.search import SearchSkillGraph
from common.utils.logging_handler import Logger
from common.utils.errors import ResourceNotFoundException, ValidationError
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound)
from config import SKILL_GRAPH_LEVELS, ERROR_RESPONSES
# pylint: disable = broad-except

router = APIRouter(
    tags=["Search in Skill Graph"],
    responses=ERROR_RESPONSES)


@router.post(
    "/syntactic-search",
    response_model=KeywordSearchResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def syntactic_search_by_query(req_body: KeywordSearchRequestModel):
  """Search for skills based on the name or keyword

  Args:
      req_body (KeywordSearchRequestModel): Required body for search

  Returns:
      KeywordSearchResponseModel: Array of skill objects
  """
  try:
    request_body = req_body.__dict__
    name = request_body.get("name", "")
    keyword = request_body.get("keyword", "")
    levels = request_body.get("levels", SKILL_GRAPH_LEVELS)
    search_result = {}
    if not name and not keyword:
      raise ValidationError("Both Name and Keyword cannot be empty.")
    for level in levels:
      result = []
      Logger.info(f"Searching for Level: {level}")
      level_obj = SearchSkillGraph(level).get_level_obj()

      if name:
        # fetch skill that matches name
        name_node_items = level_obj.find_by_name(name)
        if name_node_items:
          result = [
              name_node_item.get_fields(reformat_datetime=True)
              for name_node_item in name_node_items
          ]

      if keyword:
        # fetch skill that contains keyword
        keyword_node_items = level_obj.find_by_keywords(keyword)
        if keyword_node_items:
          result.extend([
              keyword_node_item.get_fields(reformat_datetime=True)
              for keyword_node_item in keyword_node_items
          ])

      if name and keyword:
        result = list({v["uuid"]: v for v in result}.values())
      search_result[level] = result

    return {
        "success": True,
        "message": "Successfully fetched the skills",
        "data": search_result
    }

  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
