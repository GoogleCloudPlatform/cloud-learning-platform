""" Mastery endpoints """
from fastapi import APIRouter
from copy import deepcopy
from common.utils.http_exceptions import APINotImplemented
from schemas.mastery_schema import MasteryScoresResponse
from config import ERROR_RESPONSES
# pylint: disable = broad-except

ERROR_RESPONSE_DICT = deepcopy(ERROR_RESPONSES)
del ERROR_RESPONSE_DICT[422]

router = APIRouter(prefix="/mastery",
tags=["Mastery"], responses=ERROR_RESPONSE_DICT)


@router.post("", response_model=MasteryScoresResponse)
def compute_mastery_score(learner_profile_id: str):
  """The compute mastery score endpoint will compute the mastery score for a
  given student learner profile

  Args:
      learner_profile_id:
      learner profile id for which the score needs to be computed

  Raises:
      ResourceNotFoundException: If the learner profile id does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      str: UUID (Unique identifier for learner profile)
  """
  raise APINotImplemented()


@router.post("/train")
def train_mastery_model():
  """The train mastery endpoint will train the mastery model

  Raises:
      ResourceNotFoundException: If the mastery does not exist
      Exception: 500 Internal Server Error if something went wrong
  """
  raise APINotImplemented()
