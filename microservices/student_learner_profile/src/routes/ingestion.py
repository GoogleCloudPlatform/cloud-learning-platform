""" Data Ingestion API """
from fastapi import APIRouter
from common.utils.http_exceptions import APINotImplemented

# pylint: disable = broad-except

router = APIRouter(prefix="/import", tags=["Ingestion API"])


@router.post("/{source}")
def import_learner_profile(source: str):
  """Batch Job to import learner profile to firestore

  Args:
    source(str): Source from where learner profile needs to be imported.

  Returns:
    LearnerProfiles(List): List of learner profiles imported.
  """
  raise APINotImplemented()
