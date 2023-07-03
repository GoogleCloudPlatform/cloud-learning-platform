"""To create ability tree of user"""

from common.models import (Course, Competency, SubCompetency,
  LearningObjective, LearningUnit, UserAbility)

def get_ability_tree(level, doc_id, user):
  """Returns ability tree of a user at particular level"""
  if level == "course":
    course = Course.find_by_id(doc_id)
    items_dict = {}
    items_dict["id"] = course.id
    items_dict["title"] = course.title
    course.load_children()
    ability = 0
    items_dict["competencies"] = []
    for competency in course.competencies:
      items_dict["competencies"].append(
          get_ability_tree("competency", competency.id, user))
      ability += items_dict["competencies"][-1]["ability"]
    items_dict["ability"] = ability / len(items_dict["competencies"])
  elif level == "competency":
    competency = Competency.find_by_id(doc_id)
    items_dict = {}
    items_dict["id"] = competency.id
    items_dict["title"] = competency.title
    competency.load_children()
    items_dict["sub_competencies"] = []
    ability = 0
    for sub_competency in competency.sub_competencies:
      items_dict["sub_competencies"].append(
          get_ability_tree("sub_competency", sub_competency.id, user))
      ability += items_dict["sub_competencies"][-1]["ability"]
    items_dict["ability"] = ability / len(items_dict["sub_competencies"])
  elif level == "sub_competency":
    sub_competency = SubCompetency.find_by_id(doc_id)
    items_dict = {}
    items_dict["id"] = sub_competency.id
    items_dict["title"] = sub_competency.title
    sub_competency.load_children()
    items_dict["learning_objectives"] = []
    ability = 0
    for learning_objective in sub_competency.learning_objectives:
      items_dict["learning_objectives"].append(
          get_ability_tree("learning_objective", learning_objective.id, user))
      ability += items_dict["learning_objectives"][-1]["ability"]
    items_dict["ability"] = ability / len(items_dict["learning_objectives"])
  elif level == "learning_objective":
    learning_objective = LearningObjective.find_by_id(doc_id)
    items_dict = {}
    items_dict["id"] = learning_objective.id
    items_dict["title"] = learning_objective.title
    learning_objective.load_children()
    items_dict["learning_units"] = []
    ability = 0
    for learning_unit in learning_objective.learning_units:
      items_dict["learning_units"].append(
          get_ability_tree("learning_unit", learning_unit.id, user))
      ability += items_dict["learning_units"][-1]["ability"]
    items_dict["ability"] = ability / len(items_dict["learning_units"])
  elif level == "learning_unit":
    learning_unit = LearningUnit.find_by_id(doc_id)
    lu_ability = UserAbility.collection.filter\
      (learning_unit=learning_unit.key).filter(user=user.key).get()
    if lu_ability:
      ability = lu_ability.ability
    else:
      ability = 0
    items_dict = {
      "id": learning_unit.id,
      "title": learning_unit.title,
      "ability": ability
      }
  return items_dict
