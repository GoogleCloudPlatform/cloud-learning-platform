"""Custom Validations"""
from common.models import (
  Course, Competency, SubCompetency, LearningObjective, LearningUnit)
from common.utils.gcs_adapter import is_valid_path

def check_valid_request(request_body):
  """Check if a document for a particular level exists or not"""
  level = request_body.get("level", "learning_objective")
  level_id = request_body.get("id")
  level_class = None
  if level == "course":
    level_class = Course
  elif level == "competency":
    level_class = Competency
  elif level == "sub_competency":
    level_class = SubCompetency
  elif level == "learning_objective":
    level_class = LearningObjective
  elif level == "learning_unit":
    level_class = LearningUnit
  return level_class.find_by_id(level_id)

def check_file_exists(gcs_uri):
  """
    checks whether a blob exists or not
  """
  return is_valid_path(gcs_uri)
