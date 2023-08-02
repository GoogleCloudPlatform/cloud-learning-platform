""" Learner Achievements endpoint """
import traceback
from fastapi import APIRouter
from common.models import LearnerProfile, CurriculumPathway, Achievement
from common.utils.errors import (ResourceNotFoundException)
from common.utils.http_exceptions import (InternalServerError,
                                          ResourceNotFound)
from common.utils.logging_handler import Logger
import concurrent.futures
from schemas.achievement_schema import LearnerAchievementResponseModel
from schemas.error_schema import NotFoundErrorResponseModel
from config import ERROR_RESPONSES

# pylint: disable = broad-except
router = APIRouter(tags=["Learner"], responses=ERROR_RESPONSES)


@router.get(
  "/learner/{learner_id}/achievements",
  response_model=LearnerAchievementResponseModel,
  responses={404: {
    "model": NotFoundErrorResponseModel
  }})
def get_learner_achievements(learner_id: str, program_pathway_id: str):
  """Endpoint to return learner achievements for a program
  ### Args:
  learner_id: `str`
    unique identifier for the learner
  program_pathway_id: `str`
    Unique identifier for given program pathway
  ### Raises:
  ResourceNotFoundException:
    If the node of node type does not exist. <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Returns:
  LearnerAchievementResponseModel: List of learner achievements for the
   given program
  """
  try:
    pathway_node = CurriculumPathway.find_by_id(
      program_pathway_id)
    pathway_node = pathway_node.get_fields(reformat_datetime=True)
    learner_profile = LearnerProfile.find_by_learner_id(learner_id)
    learner_achievements = get_all_learner_achievements(
      pathway_node, learner_profile)
    return {
      "success": True,
      "message": "Successfully fetched the learner achievements"
                 " for the given pathway",
      "data": learner_achievements
    }
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


def get_all_learner_achievements(parent_node, learner_profile):
  """Returns all achievements for a given pathway node"""
  achievements_list = []
  if len(parent_node.get("achievements", [])) > 0:
    with concurrent.futures.ThreadPoolExecutor() as executor:
      futures = []
      for achievement_id in parent_node.get("achievements", []):
        future = executor.submit(
          get_achievement_fields, achievement_id, parent_node, learner_profile)
        futures.append(future)

      for future in concurrent.futures.as_completed(futures):
        achievement = future.result()
        achievements_list.append(achievement)

  else:
    for child_node_id in parent_node.get(
      "child_nodes", {}).get("curriculum_pathways", []):
      child_node = CurriculumPathway.find_by_id(
        child_node_id)
      child_node = child_node.get_fields(reformat_datetime=True)
      achievements_list.extend(get_all_learner_achievements(
        child_node, learner_profile
      ))
  return achievements_list


def get_achievement_fields(achievement_id, parent_node, learner_profile):
  """
  Returns the achievement fields for a given achievement
  ### Args:
  achievement_id: `str`
    unique identifier for the achievement
  parent_node: `dict`
    parent node of the achievement
  learner_profile: `LearnerProfile`
    learner profile of the user
  ### Raises:
  ResourceNotFoundException:
    If the node of node type does not exist. <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  LearnerAchievementResponseModel: LearnerAchievementResponseModel
  """
  achievement = Achievement.find_by_id(
    achievement_id).get_fields(reformat_datetime=True)
  achievement["parent_node"] = parent_node
  if achievement["uuid"] in learner_profile.achievements:
    achievement["status"] = "completed"
  else:
    achievement["status"] = "not completed"
  achievement["child_achievements"] = []
  for child_node_id in parent_node.get(
    "child_nodes", {}).get("curriculum_pathways", []):
    child_node = CurriculumPathway.find_by_id(
      child_node_id)
    child_node = child_node.get_fields(reformat_datetime=True)
    achievement["child_achievements"].extend(
      get_all_learner_achievements(
        child_node, learner_profile
      ))
  return achievement
