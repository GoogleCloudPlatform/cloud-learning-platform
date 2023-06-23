"""Fetches all learning unit from a given level and doc id"""

from common.models import Course, Competency, SubCompetency, LearningObjective, LearningUnit

def get_all_learning_units(level, doc_id):
  """Fetches all learning unit ids from a given level"""
  if level == "course":
    course = Course.find_by_id(doc_id)
    course.load_children()
    learning_units = []
    for competency in course.competencies:
      learning_units.extend(
          get_all_learning_units("competency", competency.id))
  elif level == "competency":
    competency = Competency.find_by_id(doc_id)
    competency.load_children()
    learning_units = []
    for sub_competency in competency.sub_competencies:
      learning_units.extend(
          get_all_learning_units("sub_competency", sub_competency.id))
  elif level == "sub_competency":
    sub_competency = SubCompetency.find_by_id(doc_id)
    sub_competency.load_children()
    learning_units = []
    for learning_objective in sub_competency.learning_objectives:
      learning_units.extend(
          get_all_learning_units("learning_objective", learning_objective.id))
  elif level == "learning_objective":
    learning_objective = LearningObjective.find_by_id(doc_id)
    learning_objective.load_children()
    learning_units = []
    for learning_unit in learning_objective.learning_units:
      learning_units.extend(
          get_all_learning_units("learning_unit", learning_unit.id))
  elif level == "learning_unit":
    learning_unit = LearningUnit.find_by_id(doc_id)
    learning_units = [learning_unit.id]
  return learning_units
