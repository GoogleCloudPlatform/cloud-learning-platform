""" Learner Progress endpoints """
import traceback
from fastapi import APIRouter
from typing import Union
from common.models import LearnerProfile
from common.utils.collection_references import collection_references
from common.utils.parent_child_nodes_handler import ParentChildNodesHandler
from common.utils.errors import (ResourceNotFoundException)
from common.utils.http_exceptions import (InternalServerError,
                                          ResourceNotFound)
from common.utils.logging_handler import Logger
from schemas.progress_schema import (
  NodeTypeModel,
  LearningResourceProgressResponse,
  LearningObjectProgressResponse,
  LearningExperienceProgressResponse,
  CurriculumPathwayProgressResponse)
from schemas.error_schema import NotFoundErrorResponseModel
from config import ERROR_RESPONSES

# pylint: disable = broad-except
router = APIRouter(tags=["Learner"], responses=ERROR_RESPONSES)


@router.get(
    "/learner/{learner_id}/progress",
    response_model=Union[LearningResourceProgressResponse,
                        LearningObjectProgressResponse,
                        LearningExperienceProgressResponse,
                        CurriculumPathwayProgressResponse],
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_learner_progress(learner_id: str, node_id: str,
        node_type: NodeTypeModel):
  """Function to return learner progress for a given node
  ### Args:
  learner_id: `str`
    unique identifier for the learner
  node_id: `str`
    Unique identifier for given node level
  node_type: `str`
    type of learning hierarchy node. Supports the following \
    "curriculum_pathways", "learning_experiences", "learning_objects" and \
    "learning_resources"
  ### Raises:
  ResourceNotFoundException:
    If the node of node type does not exist. <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Returns:
  learner_progress_response : Union[LearningResourceProgressResponse,
                        LearningObjectProgressResponse,
                        LearningExperienceProgressResponse,
                        CurriculumPathwayProgressResponse]
  """
  try:
    root_node = collection_references[node_type].find_by_id(node_id)
    root_node = root_node.get_fields(reformat_datetime=True)
    learner_profile = None
    if learner_id:
      learner_profile = LearnerProfile.find_by_learner_id(learner_id)

    # Variable to identify if recent child nodes are to be added in response
    # and if child nodes are to be sorted based on recent activity
    # Currently, added only when node_type == curriculum_pathways
    root_node = ParentChildNodesHandler.load_hierarchy_progress(
        root_node, node_type, learner_profile)
    return {
        "success": True,
        "message": f"Successfully fetched the {node_type} progress for the"
        " given learner",
        "data": root_node
    }
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
